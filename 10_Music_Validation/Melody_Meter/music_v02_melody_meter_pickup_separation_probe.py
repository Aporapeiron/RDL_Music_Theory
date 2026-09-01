"""Melody-meter pickup separation probe for Music v0.2.

This probe separates three relations that were compressed in the first
melody-meter fixture:

- meter_reference: audible beat grid / bar downbeat clicks
- note_accent: local amplitude accent on notes
- pickup_offset: melody begins before the next downbeat

The preserved melody and contour remain identical.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import wave

ROOT = Path(__file__).resolve().parents[2]
AUDIO_RELATIVE_PATH = "artifacts/audio/music_v02_melody_meter_pickup_separation_probe.wav"
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_melody_meter_pickup_separation_probe.json"
SAMPLE_RATE = 44_100
BEAT_SECONDS = 0.42
PHRASE_GAP_SECONDS = 0.62
MELODY = ("C4", "D4", "E4", "G4", "E4", "D4", "C4", "G3")
DURATIONS = (1, 1, 1, 1, 1, 1, 1, 1)

NOTE_FREQUENCIES = {
    "G3": 195.998,
    "C4": 261.626,
    "D4": 293.665,
    "E4": 329.628,
    "G4": 391.995,
}


@dataclass(frozen=True)
class SeparatedMeterFrame:
    name: str
    beats_per_bar: int
    pickup_offset_beats: int
    meter_downbeat_positions: tuple[int, ...]
    note_accent_indices: tuple[int, ...]
    preserved_melody: tuple[str, ...]
    preserved_contour: tuple[int, ...]
    separated_relations: tuple[str, ...]
    structural_prediction: str
    perceptual_hypothesis: str
    actual_listening_observation: str | None
    candidate_classification: str


def contour(notes: tuple[str, ...]) -> tuple[int, ...]:
    values = [NOTE_FREQUENCIES[note] for note in notes]
    result: list[int] = []
    for before, after in zip(values, values[1:]):
        result.append(1 if after > before else -1 if after < before else 0)
    return tuple(result)


def build_frames() -> list[SeparatedMeterFrame]:
    preserved_contour = contour(MELODY)
    return [
        SeparatedMeterFrame(
            name="downbeat_note_accent_aligned",
            beats_per_bar=4,
            pickup_offset_beats=0,
            meter_downbeat_positions=(0, 4),
            note_accent_indices=(0, 4),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            separated_relations=("meter_reference", "note_accent"),
            structural_prediction="meter downbeat and note accent align, yielding stable periodic phrasing",
            perceptual_hypothesis="listener may hear the first note as arrival on the bar",
            actual_listening_observation=None,
            candidate_classification="aligned_downbeat_melody_candidate",
        ),
        SeparatedMeterFrame(
            name="true_one_beat_pickup",
            beats_per_bar=4,
            pickup_offset_beats=1,
            meter_downbeat_positions=(1, 5),
            note_accent_indices=(1, 5),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            separated_relations=("meter_reference", "pickup_offset", "note_accent_after_pickup"),
            structural_prediction="first note is before the audible downbeat; second note receives downbeat support",
            perceptual_hypothesis="listener may hear C4 as pickup and D4 as the first metrical arrival",
            actual_listening_observation=None,
            candidate_classification="true_pickup_reinterpretation_candidate",
        ),
        SeparatedMeterFrame(
            name="pickup_without_note_accent",
            beats_per_bar=4,
            pickup_offset_beats=1,
            meter_downbeat_positions=(1, 5),
            note_accent_indices=(),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            separated_relations=("meter_reference", "pickup_offset"),
            structural_prediction="pickup relation is carried by meter reference rather than note loudness",
            perceptual_hypothesis="listener may still hear weak upbeat entry because the grid arrives after C4",
            actual_listening_observation=None,
            candidate_classification="meter_only_pickup_candidate",
        ),
        SeparatedMeterFrame(
            name="accent_without_pickup",
            beats_per_bar=4,
            pickup_offset_beats=0,
            meter_downbeat_positions=(0, 4),
            note_accent_indices=(1, 5),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            separated_relations=("meter_reference", "note_accent_displaced"),
            structural_prediction="note accent is displaced while melody still begins on the audible downbeat",
            perceptual_hypothesis="listener may hear syncopation rather than true pickup",
            actual_listening_observation=None,
            candidate_classification="accent_displacement_without_pickup_candidate",
        ),
    ]


def sine_sample(frequency: float, index: int, duration: float) -> float:
    t = index / SAMPLE_RATE
    attack = min(t / 0.014, 1.0)
    release = min((duration - t) / 0.045, 1.0)
    envelope = max(0.0, min(attack, release))
    return math.sin(2.0 * math.pi * frequency * t) * envelope


def click_sample(index: int, duration: float, downbeat: bool) -> float:
    t = index / SAMPLE_RATE
    if t > duration:
        return 0.0
    frequency = 1550.0 if downbeat else 1050.0
    decay = math.exp(-t * 55.0)
    amp = 0.24 if downbeat else 0.13
    return amp * math.sin(2.0 * math.pi * frequency * t) * decay


def add_click(samples: list[float], start_frame: int, downbeat: bool) -> None:
    click_frames = int(SAMPLE_RATE * 0.055)
    for i in range(click_frames):
        pos = start_frame + i
        if pos < len(samples):
            samples[pos] += click_sample(i, 0.055, downbeat)


def add_note(samples: list[float], note: str, start_frame: int, beats: int, accented: bool) -> None:
    duration = BEAT_SECONDS * beats
    frames = int(SAMPLE_RATE * duration)
    amp = 0.34 if accented else 0.22
    for i in range(frames):
        pos = start_frame + i
        if pos < len(samples):
            samples[pos] += amp * sine_sample(NOTE_FREQUENCIES[note], i, duration)


def render_frame(frame: SeparatedMeterFrame) -> list[int]:
    total_beats = frame.pickup_offset_beats + sum(DURATIONS)
    total_frames = int(SAMPLE_RATE * (total_beats * BEAT_SECONDS + PHRASE_GAP_SECONDS))
    values = [0.0] * total_frames

    for beat in range(total_beats):
        add_click(values, int(beat * BEAT_SECONDS * SAMPLE_RATE), beat in frame.meter_downbeat_positions)

    note_start_beat = 0
    for index, (note, duration) in enumerate(zip(frame.preserved_melody, DURATIONS)):
        start_frame = int((note_start_beat + index) * BEAT_SECONDS * SAMPLE_RATE)
        add_note(values, note, start_frame, duration, index in frame.note_accent_indices)

    return [int(max(-0.95, min(0.95, sample)) * 32767) for sample in values]


def write_wave(frames: list[SeparatedMeterFrame], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples: list[int] = []
    for frame in frames:
        samples.extend(render_frame(frame))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(sample.to_bytes(2, "little", signed=True) for sample in samples))


def write_manifest(frames: list[SeparatedMeterFrame], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "rdl_music_v02_melody_meter_pickup_separation_probe_v0_1",
        "subject": "melody_meter_pickup_separation_probe",
        "preserved_material": {
            "melody": list(MELODY),
            "durations": list(DURATIONS),
            "contour": list(contour(MELODY)),
        },
        "frames": [asdict(frame) for frame in frames],
        "device_audio_path": AUDIO_RELATIVE_PATH,
        "manifest_path": MANIFEST_RELATIVE_PATH,
        "stop_lines": [
            "pickup_relation_is_not_identical_to_first_note_accent",
            "meter_reference_is_not_identical_to_note_accent_schedule",
            "click_track_is_device_fixture_not_human_meter_confirmation",
            "actual_listening_observation_remains_null_until_recorded",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    frames = build_frames()
    expected_contour = contour(MELODY)
    assert all(frame.preserved_melody == MELODY for frame in frames)
    assert all(frame.preserved_contour == expected_contour for frame in frames)
    assert frames[1].pickup_offset_beats == 1
    assert 0 not in frames[1].note_accent_indices
    assert all(frame.actual_listening_observation is None for frame in frames)
    audio_path = ROOT / AUDIO_RELATIVE_PATH
    manifest_path = ROOT / MANIFEST_RELATIVE_PATH
    write_wave(frames, audio_path)
    write_manifest(frames, manifest_path)
    print("music_v02_melody_meter_pickup_separation_probe_observed")
    for frame in frames:
        print(
            f"frame={frame.name}; pickup={frame.pickup_offset_beats}; "
            f"downbeats={frame.meter_downbeat_positions}; accents={frame.note_accent_indices}; "
            f"class={frame.candidate_classification}; actual={frame.actual_listening_observation}"
        )
    print(f"device_audio_file={audio_path.name}")
    print(f"manifest_file={manifest_path.name}")


if __name__ == "__main__":
    main()