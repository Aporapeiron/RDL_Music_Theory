"""Melody and meter identity probe for Music v0.2.

The pitch contour is kept identical while accent and metric placement change.
This is the first post-C6/Am7 Music target: it asks whether preserved melodic
material remains the same musical state when the metric relation changes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import wave

ROOT = Path(__file__).resolve().parents[2]
AUDIO_RELATIVE_PATH = "artifacts/audio/music_v02_melody_meter_identity_probe.wav"
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_melody_meter_identity_probe.json"
SAMPLE_RATE = 44_100
BEAT_SECONDS = 0.42
PHRASE_GAP_SECONDS = 0.55
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
class MeterFrame:
    name: str
    beats_per_bar: int
    accent_positions: tuple[int, ...]
    pickup_beats: int
    preserved_melody: tuple[str, ...]
    preserved_contour: tuple[int, ...]
    changed_relation: str
    structural_prediction: str
    perceptual_hypothesis: str
    actual_listening_observation: str | None
    candidate_classification: str


def contour(notes: tuple[str, ...]) -> tuple[int, ...]:
    values = [NOTE_FREQUENCIES[note] for note in notes]
    result: list[int] = []
    for before, after in zip(values, values[1:]):
        if after > before:
            result.append(1)
        elif after < before:
            result.append(-1)
        else:
            result.append(0)
    return tuple(result)


def build_frames() -> list[MeterFrame]:
    preserved_contour = contour(MELODY)
    return [
        MeterFrame(
            name="four_four_downbeat_stable",
            beats_per_bar=4,
            accent_positions=(0, 4),
            pickup_beats=0,
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            changed_relation="meter:4/4 downbeat alignment",
            structural_prediction="melody is framed as two balanced 4-beat units",
            perceptual_hypothesis="listener may hear stable periodic closure",
            actual_listening_observation=None,
            candidate_classification="melody_identity_stable_meter_candidate",
        ),
        MeterFrame(
            name="three_three_two_grouping",
            beats_per_bar=8,
            accent_positions=(0, 3, 6),
            pickup_beats=0,
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            changed_relation="accent grouping:3+3+2 over identical note order",
            structural_prediction="same contour is rephrased as asymmetric propulsion",
            perceptual_hypothesis="listener may hear the melody as more forward-leaning",
            actual_listening_observation=None,
            candidate_classification="same_melody_as_metric_rephrasing_candidate",
        ),
        MeterFrame(
            name="one_beat_pickup_shift",
            beats_per_bar=4,
            accent_positions=(1, 5),
            pickup_beats=1,
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            changed_relation="meter:one-beat pickup shifts accent relation",
            structural_prediction="same contour is heard as entering before the bar rather than on the bar",
            perceptual_hypothesis="listener may hear the first note as anacrusis rather than arrival",
            actual_listening_observation=None,
            candidate_classification="melody_identity_with_pickup_reinterpretation_candidate",
        ),
        MeterFrame(
            name="cadence_accent_displacement",
            beats_per_bar=4,
            accent_positions=(0, 3, 7),
            pickup_beats=0,
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            changed_relation="accent displaced toward local high point and final descent",
            structural_prediction="same contour foregrounds peak and descent more than periodic balance",
            perceptual_hypothesis="listener may hear melodic direction over meter regularity",
            actual_listening_observation=None,
            candidate_classification="same_melody_with_directional_accent_candidate",
        ),
    ]


def sine_sample(frequency: float, index: int, duration: float) -> float:
    t = index / SAMPLE_RATE
    attack = min(t / 0.018, 1.0)
    release = min((duration - t) / 0.05, 1.0)
    envelope = max(0.0, min(attack, release))
    return math.sin(2.0 * math.pi * frequency * t) * envelope


def render_note(note: str, beats: int, accented: bool) -> list[int]:
    duration = BEAT_SECONDS * beats
    frames = int(SAMPLE_RATE * duration)
    amp = 0.42 if accented else 0.24
    samples: list[int] = []
    for i in range(frames):
        value = amp * sine_sample(NOTE_FREQUENCIES[note], i, duration)
        samples.append(int(max(-0.95, min(0.95, value)) * 32767))
    return samples


def render_frame(frame: MeterFrame) -> list[int]:
    samples: list[int] = []
    beat_position = frame.pickup_beats
    for note, duration in zip(frame.preserved_melody, DURATIONS):
        accented = beat_position % frame.beats_per_bar in frame.accent_positions
        samples.extend(render_note(note, duration, accented))
        beat_position += duration
    samples.extend([0] * int(SAMPLE_RATE * PHRASE_GAP_SECONDS))
    return samples


def write_wave(frames: list[MeterFrame], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples: list[int] = []
    for frame in frames:
        samples.extend(render_frame(frame))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(sample.to_bytes(2, "little", signed=True) for sample in samples))


def write_manifest(frames: list[MeterFrame], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "rdl_music_v02_melody_meter_identity_probe_v0_1",
        "subject": "melody_meter_identity_preservation_probe",
        "preserved_material": {
            "melody": list(MELODY),
            "durations": list(DURATIONS),
            "contour": list(contour(MELODY)),
        },
        "frames": [asdict(frame) for frame in frames],
        "device_audio_path": AUDIO_RELATIVE_PATH,
        "manifest_path": MANIFEST_RELATIVE_PATH,
        "stop_lines": [
            "melodic_contour_preservation_is_not_meter_state_preservation",
            "accent_pattern_is_structural_fixture_not_actual_hearing",
            "candidate_classification_is_not_final_melodic_identity_truth",
            "actual_listening_observation_remains_null_until_recorded",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    frames = build_frames()
    expected_contour = contour(MELODY)
    assert all(frame.preserved_melody == MELODY for frame in frames)
    assert all(frame.preserved_contour == expected_contour for frame in frames)
    assert all(frame.actual_listening_observation is None for frame in frames)
    audio_path = ROOT / AUDIO_RELATIVE_PATH
    manifest_path = ROOT / MANIFEST_RELATIVE_PATH
    write_wave(frames, audio_path)
    write_manifest(frames, manifest_path)
    print("music_v02_melody_meter_identity_probe_observed")
    for frame in frames:
        print(
            f"frame={frame.name}; changed={frame.changed_relation}; "
            f"class={frame.candidate_classification}; actual={frame.actual_listening_observation}"
        )
    print(f"device_audio_file={audio_path.name}")
    print(f"manifest_file={manifest_path.name}")


if __name__ == "__main__":
    main()