"""Melody-meter syncopation probe for Music v0.2.

This fixture keeps the melodic pitch order and 4/4 meter reference fixed while
separating note-accent displacement from onset-phase displacement.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import wave

ROOT = Path(__file__).resolve().parents[2]
AUDIO_RELATIVE_PATH = "artifacts/audio/music_v02_melody_meter_syncopation_probe.wav"
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_melody_meter_syncopation_probe.json"
SAMPLE_RATE = 44_100
BEAT_SECONDS = 0.42
PHRASE_GAP_SECONDS = 0.64
NOTE_DURATION_BEATS = 0.72
MELODY = ("C4", "D4", "E4", "G4", "E4", "D4", "C4", "G3")

NOTE_FREQUENCIES = {
    "G3": 195.998,
    "C4": 261.626,
    "D4": 293.665,
    "E4": 329.628,
    "G4": 391.995,
}


@dataclass(frozen=True)
class SyncopationFrame:
    name: str
    beats_per_bar: int
    downbeat_origin: int
    onset_phase_beats: float
    note_accent_indices: tuple[int, ...]
    preserved_melody: tuple[str, ...]
    preserved_contour: tuple[int, ...]
    separated_relations: tuple[str, ...]
    structural_prediction: str
    perceptual_hypothesis: str
    actual_listening_observation: str | None
    candidate_classification: str

    @property
    def onset_positions(self) -> tuple[float, ...]:
        return tuple(self.onset_phase_beats + index for index in range(len(self.preserved_melody)))

    @property
    def downbeat_positions(self) -> tuple[int, ...]:
        return tuple(
            beat
            for beat in range(0, len(self.preserved_melody) + 1)
            if (beat - self.downbeat_origin) % self.beats_per_bar == 0
        )


def contour(notes: tuple[str, ...]) -> tuple[int, ...]:
    values = [NOTE_FREQUENCIES[note] for note in notes]
    result: list[int] = []
    for before, after in zip(values, values[1:]):
        result.append(1 if after > before else -1 if after < before else 0)
    return tuple(result)


def build_frames() -> list[SyncopationFrame]:
    preserved_contour = contour(MELODY)
    return [
        SyncopationFrame(
            name="onbeat_accent_aligned_reference",
            beats_per_bar=4,
            downbeat_origin=0,
            onset_phase_beats=0.0,
            note_accent_indices=(0, 4),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            separated_relations=("meter_reference", "onbeat_onset", "downbeat_note_accent"),
            structural_prediction="onsets and note accents align with the 4/4 reference",
            perceptual_hypothesis="listener may hear the melody as metrically settled",
            actual_listening_observation=None,
            candidate_classification="aligned_onbeat_reference_candidate",
        ),
        SyncopationFrame(
            name="accent_displaced_onbeat_onsets",
            beats_per_bar=4,
            downbeat_origin=0,
            onset_phase_beats=0.0,
            note_accent_indices=(1, 5),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            separated_relations=("meter_reference", "onbeat_onset", "note_accent_displacement"),
            structural_prediction="note accent is displaced while onset phase remains on the beat grid",
            perceptual_hypothesis="listener may hear syncopation pressure without onset displacement",
            actual_listening_observation=None,
            candidate_classification="accent_only_syncopation_candidate",
        ),
        SyncopationFrame(
            name="offbeat_onsets_without_note_accent",
            beats_per_bar=4,
            downbeat_origin=0,
            onset_phase_beats=0.5,
            note_accent_indices=(),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            separated_relations=("meter_reference", "offbeat_onset_phase", "no_note_accent"),
            structural_prediction="onsets fall between beats while note accent remains absent",
            perceptual_hypothesis="listener may hear metric suspension carried by onset phase alone",
            actual_listening_observation=None,
            candidate_classification="onset_phase_syncopation_candidate",
        ),
        SyncopationFrame(
            name="offbeat_onsets_with_note_accent",
            beats_per_bar=4,
            downbeat_origin=0,
            onset_phase_beats=0.5,
            note_accent_indices=(0, 4),
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            separated_relations=("meter_reference", "offbeat_onset_phase", "offbeat_note_accent"),
            structural_prediction="offbeat onset phase and note accent support the same displaced relation",
            perceptual_hypothesis="listener may hear the clearest syncopation candidate in this fixture",
            actual_listening_observation=None,
            candidate_classification="onset_accent_syncopation_candidate",
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


def add_note(samples: list[float], note: str, start_frame: int, accented: bool) -> None:
    duration = NOTE_DURATION_BEATS * BEAT_SECONDS
    frames = int(SAMPLE_RATE * duration)
    amp = 0.34 if accented else 0.22
    for i in range(frames):
        pos = start_frame + i
        if pos < len(samples):
            samples[pos] += amp * sine_sample(NOTE_FREQUENCIES[note], i, duration)


def render_frame(frame: SyncopationFrame) -> list[int]:
    total_beats = len(frame.preserved_melody) + 1
    total_frames = int(SAMPLE_RATE * (total_beats * BEAT_SECONDS + PHRASE_GAP_SECONDS))
    values = [0.0] * total_frames

    for beat in range(total_beats):
        downbeat = (beat - frame.downbeat_origin) % frame.beats_per_bar == 0
        add_click(values, int(beat * BEAT_SECONDS * SAMPLE_RATE), downbeat)

    for index, note in enumerate(frame.preserved_melody):
        onset = frame.onset_phase_beats + index
        start_frame = int(onset * BEAT_SECONDS * SAMPLE_RATE)
        add_note(values, note, start_frame, index in frame.note_accent_indices)

    return [int(max(-0.95, min(0.95, sample)) * 32767) for sample in values]


def frame_record(frame: SyncopationFrame) -> dict[str, object]:
    record = asdict(frame)
    record["onset_positions"] = list(frame.onset_positions)
    record["downbeat_positions"] = list(frame.downbeat_positions)
    return record


def write_wave(frames: list[SyncopationFrame], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples: list[int] = []
    for frame in frames:
        samples.extend(render_frame(frame))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(sample.to_bytes(2, "little", signed=True) for sample in samples))


def write_manifest(frames: list[SyncopationFrame], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "rdl_music_v02_melody_meter_syncopation_probe_v0_1",
        "subject": "melody_meter_syncopation_probe",
        "preserved_material": {
            "melody": list(MELODY),
            "contour": list(contour(MELODY)),
            "note_duration_beats": NOTE_DURATION_BEATS,
            "meter_reference": "4/4 click grid with downbeats at 0 and 4",
        },
        "frames": [frame_record(frame) for frame in frames],
        "device_audio_path": AUDIO_RELATIVE_PATH,
        "manifest_path": MANIFEST_RELATIVE_PATH,
        "stop_lines": [
            "syncopation_candidate_is_not_identical_to_note_accent_displacement",
            "onset_phase_displacement_is_not_identical_to_note_accent",
            "meter_reference_is_fixed_across_frames",
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
    assert all(frame.beats_per_bar == 4 for frame in frames)
    assert all(frame.downbeat_origin == 0 for frame in frames)
    assert frames[1].onset_phase_beats == 0.0
    assert frames[2].onset_phase_beats == 0.5
    assert not frames[2].note_accent_indices
    assert all(frame.actual_listening_observation is None for frame in frames)
    audio_path = ROOT / AUDIO_RELATIVE_PATH
    manifest_path = ROOT / MANIFEST_RELATIVE_PATH
    write_wave(frames, audio_path)
    write_manifest(frames, manifest_path)
    print("music_v02_melody_meter_syncopation_probe_observed")
    for frame in frames:
        print(
            f"frame={frame.name}; onset_phase={frame.onset_phase_beats}; "
            f"accents={frame.note_accent_indices}; class={frame.candidate_classification}; "
            f"actual={frame.actual_listening_observation}"
        )
    print(f"device_audio_file={audio_path.name}")
    print(f"manifest_file={manifest_path.name}")


if __name__ == "__main__":
    main()
