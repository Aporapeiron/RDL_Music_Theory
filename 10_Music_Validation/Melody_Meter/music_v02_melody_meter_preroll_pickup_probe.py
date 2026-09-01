"""Melody-meter pre-roll pickup probe for Music v0.2.

This probe asks whether pickup relation should be represented only by a local
meter offset, or by an already-established meter field before the melody enters.
The melody remains identical; pre-roll clicks create meter history before C4.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import wave

ROOT = Path(__file__).resolve().parents[2]
AUDIO_RELATIVE_PATH = "artifacts/audio/music_v02_melody_meter_preroll_pickup_probe.wav"
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_melody_meter_preroll_pickup_probe.json"
SAMPLE_RATE = 44_100
BEAT_SECONDS = 0.42
PHRASE_GAP_SECONDS = 0.7
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
class PrerollPickupFrame:
    name: str
    beats_per_bar: int
    preroll_beats: int
    melody_entry_beat: int
    first_downbeat_after_entry: int
    downbeat_origin: int
    note_accent_indices: tuple[int, ...]
    preserved_melody: tuple[str, ...]
    preserved_contour: tuple[int, ...]
    meter_history_relation: str
    structural_prediction: str
    perceptual_hypothesis: str
    actual_listening_observation: str | None
    candidate_classification: str


def contour(notes: tuple[str, ...]) -> tuple[int, ...]:
    values = [NOTE_FREQUENCIES[note] for note in notes]
    return tuple(1 if after > before else -1 if after < before else 0 for before, after in zip(values, values[1:]))


def build_frames() -> list[PrerollPickupFrame]:
    preserved_contour = contour(MELODY)
    return [
        PrerollPickupFrame(
            name="no_preroll_local_pickup",
            beats_per_bar=4,
            preroll_beats=0,
            melody_entry_beat=0,
            first_downbeat_after_entry=1,
            downbeat_origin=1,
            note_accent_indices=(1, 5),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            meter_history_relation="meter reference begins together with melody; pickup is local offset only",
            structural_prediction="pickup relation is available but meter history before C4 is absent",
            perceptual_hypothesis="listener may need the D4 downbeat to reinterpret C4 as pickup after it occurs",
            actual_listening_observation=None,
            candidate_classification="local_pickup_without_preroll_candidate",
        ),
        PrerollPickupFrame(
            name="two_beat_preroll_pickup",
            beats_per_bar=4,
            preroll_beats=2,
            melody_entry_beat=2,
            first_downbeat_after_entry=3,
            downbeat_origin=3,
            note_accent_indices=(1, 5),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            meter_history_relation="two clicks establish beats before melody enters on the beat before downbeat",
            structural_prediction="C4 enters into an already-audible meter field as pickup; D4 receives downbeat support",
            perceptual_hypothesis="listener may hear C4 as pickup more immediately than without pre-roll",
            actual_listening_observation=None,
            candidate_classification="preroll_supported_pickup_candidate",
        ),
        PrerollPickupFrame(
            name="four_beat_preroll_pickup",
            beats_per_bar=4,
            preroll_beats=4,
            melody_entry_beat=4,
            first_downbeat_after_entry=5,
            downbeat_origin=5,
            note_accent_indices=(1, 5),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            meter_history_relation="full bar of clicks establishes meter before pickup entry",
            structural_prediction="meter field is established before melody, strengthening pickup interpretation",
            perceptual_hypothesis="listener may hear the clearest anacrusis relation in this fixture",
            actual_listening_observation=None,
            candidate_classification="strong_preroll_pickup_candidate",
        ),
        PrerollPickupFrame(
            name="four_beat_preroll_downbeat_entry",
            beats_per_bar=4,
            preroll_beats=4,
            melody_entry_beat=4,
            first_downbeat_after_entry=4,
            downbeat_origin=4,
            note_accent_indices=(0, 4),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            meter_history_relation="full bar of clicks establishes meter, then melody enters on downbeat",
            structural_prediction="pre-roll exists, but C4 is arrival rather than pickup",
            perceptual_hypothesis="listener may hear stable downbeat entry despite same pre-roll duration",
            actual_listening_observation=None,
            candidate_classification="preroll_downbeat_entry_control_candidate",
        ),
    ]


def sine_sample(frequency: float, index: int, duration: float) -> float:
    t = index / SAMPLE_RATE
    attack = min(t / 0.014, 1.0)
    release = min((duration - t) / 0.045, 1.0)
    envelope = max(0.0, min(attack, release))
    return math.sin(2.0 * math.pi * frequency * t) * envelope


def click_sample(index: int, downbeat: bool) -> float:
    t = index / SAMPLE_RATE
    frequency = 1550.0 if downbeat else 1050.0
    decay = math.exp(-t * 55.0)
    amp = 0.24 if downbeat else 0.13
    return amp * math.sin(2.0 * math.pi * frequency * t) * decay


def add_click(samples: list[float], beat: int, downbeat: bool) -> None:
    start_frame = int(beat * BEAT_SECONDS * SAMPLE_RATE)
    click_frames = int(SAMPLE_RATE * 0.055)
    for i in range(click_frames):
        pos = start_frame + i
        if pos < len(samples):
            samples[pos] += click_sample(i, downbeat)


def add_note(samples: list[float], note: str, start_beat: int, beats: int, accented: bool) -> None:
    start_frame = int(start_beat * BEAT_SECONDS * SAMPLE_RATE)
    duration = beats * BEAT_SECONDS
    frames = int(duration * SAMPLE_RATE)
    amp = 0.34 if accented else 0.22
    for i in range(frames):
        pos = start_frame + i
        if pos < len(samples):
            samples[pos] += amp * sine_sample(NOTE_FREQUENCIES[note], i, duration)


def is_downbeat(frame: PrerollPickupFrame, beat: int) -> bool:
    return (beat - frame.downbeat_origin) % frame.beats_per_bar == 0


def render_frame(frame: PrerollPickupFrame) -> list[int]:
    total_beats = frame.melody_entry_beat + sum(DURATIONS)
    total_frames = int(SAMPLE_RATE * (total_beats * BEAT_SECONDS + PHRASE_GAP_SECONDS))
    values = [0.0] * total_frames

    for beat in range(total_beats):
        add_click(values, beat, is_downbeat(frame, beat))

    for index, (note, duration) in enumerate(zip(frame.preserved_melody, DURATIONS)):
        add_note(values, note, frame.melody_entry_beat + index, duration, index in frame.note_accent_indices)

    return [int(max(-0.95, min(0.95, sample)) * 32767) for sample in values]


def write_wave(frames: list[PrerollPickupFrame], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples: list[int] = []
    for frame in frames:
        samples.extend(render_frame(frame))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(sample.to_bytes(2, "little", signed=True) for sample in samples))


def write_manifest(frames: list[PrerollPickupFrame], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "rdl_music_v02_melody_meter_preroll_pickup_probe_v0_1",
        "subject": "melody_meter_preroll_pickup_probe",
        "preserved_material": {
            "melody": list(MELODY),
            "durations": list(DURATIONS),
            "contour": list(contour(MELODY)),
        },
        "frames": [asdict(frame) for frame in frames],
        "device_audio_path": AUDIO_RELATIVE_PATH,
        "manifest_path": MANIFEST_RELATIVE_PATH,
        "stop_lines": [
            "meter_history_is_not_identical_to_local_pickup_offset",
            "meter_phase_continuity_is_not_optional_for_preroll_pickup",
            "pre_roll_clicks_are_device_fixture_not_human_meter_confirmation",
            "pickup_candidate_is_not_actual_listening_observation",
            "actual_listening_observation_remains_null_until_recorded",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    frames = build_frames()
    expected_contour = contour(MELODY)
    assert all(frame.preserved_melody == MELODY for frame in frames)
    assert all(frame.preserved_contour == expected_contour for frame in frames)
    assert frames[1].downbeat_origin == frames[1].first_downbeat_after_entry
    assert frames[2].downbeat_origin == frames[2].first_downbeat_after_entry
    assert frames[3].downbeat_origin == frames[3].first_downbeat_after_entry
    assert frames[1].melody_entry_beat < frames[1].first_downbeat_after_entry
    assert frames[2].melody_entry_beat < frames[2].first_downbeat_after_entry
    assert frames[3].melody_entry_beat == frames[3].first_downbeat_after_entry
    assert not is_downbeat(frames[2], frames[2].melody_entry_beat)
    assert is_downbeat(frames[2], frames[2].first_downbeat_after_entry)
    assert is_downbeat(frames[3], frames[3].melody_entry_beat)
    assert all(frame.actual_listening_observation is None for frame in frames)
    audio_path = ROOT / AUDIO_RELATIVE_PATH
    manifest_path = ROOT / MANIFEST_RELATIVE_PATH
    write_wave(frames, audio_path)
    write_manifest(frames, manifest_path)
    print("music_v02_melody_meter_preroll_pickup_probe_observed")
    for frame in frames:
        print(
            f"frame={frame.name}; preroll={frame.preroll_beats}; entry={frame.melody_entry_beat}; "
            f"downbeat_after_entry={frame.first_downbeat_after_entry}; origin={frame.downbeat_origin}; class={frame.candidate_classification}; "
            f"actual={frame.actual_listening_observation}"
        )
    print(f"device_audio_file={audio_path.name}")
    print(f"manifest_file={manifest_path.name}")


if __name__ == "__main__":
    main()
