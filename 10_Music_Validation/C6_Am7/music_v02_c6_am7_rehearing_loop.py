"""C6 / Am7 small Music v0.2 loop.

This fixture keeps the pitch-class set {C, E, G, A}, changes only the bass
relation, generates a device-side audio rendering, and records the separation
between structural prediction, perceptual hypothesis, and actual human listening
observation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from math import pi, sin
from pathlib import Path
import struct
import wave


SAMPLE_RATE = 44_100
PITCH_CLASS_SET = frozenset({"C", "E", "G", "A"})
DEVICE_AUDIO_RELATIVE_PATH = "artifacts/audio/music_v02_c6_am7_rehearing_loop.wav"
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_c6_am7_rehearing_observation.json"

NOTE_FREQUENCY = {
    "A2": 110.00,
    "C3": 130.81,
    "E3": 164.81,
    "G3": 196.00,
    "A3": 220.00,
    "C4": 261.63,
    "E4": 329.63,
    "G4": 392.00,
    "A4": 440.00,
}

PITCH_CLASS = {note: note.rstrip("0123456789") for note in NOTE_FREQUENCY}


@dataclass(frozen=True)
class VoicedState:
    name: str
    notes: tuple[str, ...]
    bass: str
    preceding_context: str
    following_context: str

    @property
    def pitch_classes(self) -> frozenset[str]:
        return frozenset(PITCH_CLASS[note] for note in self.notes)


@dataclass(frozen=True)
class LoopObservation:
    source: VoicedState
    generated: VoicedState
    preserved_relations: tuple[str, ...]
    changed_relations: tuple[str, ...]
    structural_prediction: str
    perceptual_hypothesis: str
    actual_listening_observation: str | None
    device_audio_path: str
    observation_discrepancy_route: tuple[str, ...]


def c6_state() -> VoicedState:
    return VoicedState(
        name="C6_stable",
        notes=("C3", "E3", "G3", "A3"),
        bass="C",
        preceding_context="C-centered arrival",
        following_context="C-centered continuation expected",
    )


def am7_tilt_state() -> VoicedState:
    return VoicedState(
        name="Am7_tilt_candidate",
        notes=("A2", "C3", "E3", "G3"),
        bass="A",
        preceding_context="C-centered memory retained",
        following_context="A-centered continuation becomes available",
    )


def classify_chord(state: VoicedState) -> str:
    if state.pitch_classes != PITCH_CLASS_SET:
        return "out_of_fixture"
    if state.bass == "C":
        return "C6_candidate"
    if state.bass == "A":
        return "Am7_candidate"
    return "ambiguous_C6_Am7_candidate"


def render_chord_segment(notes: tuple[str, ...], seconds: float, amplitude: float = 0.22) -> list[int]:
    frame_count = int(SAMPLE_RATE * seconds)
    frames: list[int] = []
    fade_len = int(SAMPLE_RATE * 0.04)
    frequencies = [NOTE_FREQUENCY[note] for note in notes]
    for i in range(frame_count):
        t = i / SAMPLE_RATE
        envelope = 1.0
        if i < fade_len:
            envelope = i / fade_len
        elif frame_count - i < fade_len:
            envelope = (frame_count - i) / fade_len
        sample = sum(sin(2.0 * pi * freq * t) for freq in frequencies) / len(frequencies)
        frames.append(int(32767 * amplitude * envelope * sample))
    return frames


def write_wave(path: Path, segments: tuple[tuple[str, ...], ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames: list[int] = []
    for segment in segments:
        frames.extend(render_chord_segment(segment, 1.35))
        frames.extend([0] * int(SAMPLE_RATE * 0.20))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(struct.pack("<h", frame) for frame in frames))


def observation_to_manifest(observation: LoopObservation) -> dict[str, object]:
    return {
        "schema": "rdl_music_v02_rehearing_observation_v0_1",
        "subject": "C6_Am7_bass_relation_tilt",
        "source": asdict(observation.source),
        "generated": asdict(observation.generated),
        "preserved_relations": list(observation.preserved_relations),
        "changed_relations": list(observation.changed_relations),
        "structural_prediction": observation.structural_prediction,
        "perceptual_hypothesis": observation.perceptual_hypothesis,
        "actual_listening_observation": observation.actual_listening_observation,
        "device_audio_path": observation.device_audio_path,
        "observation_discrepancy_route": list(observation.observation_discrepancy_route),
        "stop_lines": [
            "discrepancy_is_not_immediate_prediction_failure",
            "discrepancy_is_not_immediate_xi",
            "structural_prediction_is_not_actual_human_listening",
            "device_audio_fixture_is_not_F_human",
            "Am7_candidate_is_not_confirmed_hearing",
        ],
    }


def write_manifest(path: Path, observation: LoopObservation) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(observation_to_manifest(observation), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def run_loop(output_path: Path, device_audio_path: str = DEVICE_AUDIO_RELATIVE_PATH) -> LoopObservation:
    source = c6_state()
    generated = am7_tilt_state()

    assert source.pitch_classes == PITCH_CLASS_SET
    assert generated.pitch_classes == PITCH_CLASS_SET
    assert classify_chord(source) == "C6_candidate"
    assert classify_chord(generated) == "Am7_candidate"
    assert source.pitch_classes == generated.pitch_classes
    assert source.bass != generated.bass

    write_wave(output_path, (source.notes, generated.notes, source.notes))

    return LoopObservation(
        source=source,
        generated=generated,
        preserved_relations=(
            "pitch_class_set:{C,E,G,A}",
            "upper_common_relation:C-E-G retained across the tilt",
        ),
        changed_relations=(
            "bass_relation:C->A",
            "register_gravity:C3->A2",
            "preceding_context:C-centered arrival->C-centered memory retained",
            "following_context:C-centered expectation->A-centered availability",
        ),
        structural_prediction="C6_candidate -> C6/Am7 ambiguity pressure -> Am7_candidate becomes available",
        perceptual_hypothesis="listener may hear the second chord as a bass-driven tilt toward Am7, while C-centered memory remains active",
        actual_listening_observation=None,
        device_audio_path=device_audio_path,
        observation_discrepancy_route=(
            "record_E_as_discrepancy_between_prediction_hypothesis_and_observation",
            "test_absorbability_in_current_M_B",
            "if_not_absorbed_hold_residual_as_H",
            "theta_decides_maintain_or_reorganize_update",
            "if_unrecovered_relation_remains_due_to_finite_B_hold_as_xi",
        ),
    )


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    output_path = repo_root / DEVICE_AUDIO_RELATIVE_PATH
    manifest_path = repo_root / MANIFEST_RELATIVE_PATH
    observation = run_loop(output_path)
    write_manifest(manifest_path, observation)

    print("music_v02_c6_am7_rehearing_loop_observed")
    print(f"source={observation.source.name}:{classify_chord(observation.source)}")
    print(f"generated={observation.generated.name}:{classify_chord(observation.generated)}")
    print("preserved=" + ", ".join(observation.preserved_relations))
    print("changed=" + ", ".join(observation.changed_relations))
    print(f"structural_prediction={observation.structural_prediction}")
    print(f"perceptual_hypothesis={observation.perceptual_hypothesis}")
    print(f"actual_listening_observation={observation.actual_listening_observation}")
    print("observation_discrepancy_route=" + " -> ".join(observation.observation_discrepancy_route))
    print(f"device_audio_file={Path(observation.device_audio_path).name}")
    print(f"observation_manifest_file={manifest_path.name}")


if __name__ == "__main__":
    main()
