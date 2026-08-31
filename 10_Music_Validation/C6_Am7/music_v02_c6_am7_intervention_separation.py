"""C6 / Am7 intervention separation for Music v0.2.

This fixture keeps the pitch-class set {C, E, G, A} and separates which
musical relation is intentionally changed: bass, register, context, or all of
them together. It does not treat the resulting structural candidate as confirmed
human hearing.
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
DEVICE_AUDIO_RELATIVE_PATH = "artifacts/audio/music_v02_c6_am7_intervention_separation.wav"
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_c6_am7_intervention_separation.json"

NOTE_FREQUENCY = {
    "A2": 110.00,
    "C2": 65.41,
    "C3": 130.81,
    "E3": 164.81,
    "G3": 196.00,
    "A3": 220.00,
    "C4": 261.63,
    "E4": 329.63,
    "G4": 392.00,
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
class InterventionCase:
    name: str
    state: VoicedState
    primary_intervention: str
    residual_changes: tuple[str, ...]
    preserved_relations: tuple[str, ...]
    changed_relations: tuple[str, ...]
    structural_prediction: str
    perceptual_hypothesis: str
    actual_listening_observation: str | None


@dataclass(frozen=True)
class SeparationObservation:
    source: VoicedState
    cases: tuple[InterventionCase, ...]
    device_audio_path: str
    manifest_path: str
    stop_lines: tuple[str, ...]


def source_state() -> VoicedState:
    return VoicedState(
        name="source_C6_stable",
        notes=("C3", "E3", "G3", "A3"),
        bass="C",
        preceding_context="C-centered arrival",
        following_context="C-centered continuation expected",
    )


def classify_state(state: VoicedState) -> str:
    if state.pitch_classes != PITCH_CLASS_SET:
        return "out_of_fixture"
    if state.bass == "A" and "A-centered" in state.following_context:
        return "Am7_candidate_with_context_support"
    if state.bass == "A":
        return "Am7_candidate_by_bass_relation"
    if "A-centered" in state.following_context:
        return "C6_candidate_with_Am7_context_pressure"
    return "C6_candidate"


def build_cases() -> tuple[InterventionCase, ...]:
    return (
        InterventionCase(
            name="context_only",
            state=VoicedState(
                name="context_only_state",
                notes=("C3", "E3", "G3", "A3"),
                bass="C",
                preceding_context="C-centered arrival retained",
                following_context="A-centered continuation becomes available",
            ),
            primary_intervention="following_context",
            residual_changes=(),
            preserved_relations=("pitch_class_set:{C,E,G,A}", "bass_relation:C", "register_gravity:C3"),
            changed_relations=("following_context:C-centered expectation->A-centered availability",),
            structural_prediction="C6 remains foregrounded, with Am7 context pressure added",
            perceptual_hypothesis="listener may hear the same sonority as slightly redirected, not yet rebased",
            actual_listening_observation=None,
        ),
        InterventionCase(
            name="register_only",
            state=VoicedState(
                name="register_only_state",
                notes=("C2", "E3", "G3", "A3"),
                bass="C",
                preceding_context="C-centered arrival",
                following_context="C-centered continuation expected",
            ),
            primary_intervention="register_gravity",
            residual_changes=(),
            preserved_relations=("pitch_class_set:{C,E,G,A}", "bass_relation:C", "C-centered context"),
            changed_relations=("register_gravity:C3->C2",),
            structural_prediction="C6 is reinforced by lower C register gravity",
            perceptual_hypothesis="listener may hear stronger C grounding rather than Am7 tilt",
            actual_listening_observation=None,
        ),
        InterventionCase(
            name="bass_primary",
            state=VoicedState(
                name="bass_primary_state",
                notes=("A2", "C3", "E3", "G3"),
                bass="A",
                preceding_context="C-centered arrival retained",
                following_context="C-centered continuation expected",
            ),
            primary_intervention="bass_relation",
            residual_changes=("register_gravity changes because bass A is lower than source C",),
            preserved_relations=("pitch_class_set:{C,E,G,A}", "following_context:C-centered expectation"),
            changed_relations=(
                "bass_relation:C->A",
                "register_gravity:C3->A2 residual",
                "preceding_context:C-centered arrival->C-centered arrival retained",
            ),
            structural_prediction="Am7 candidate appears by bass relation, but C-context resists full rebasing",
            perceptual_hypothesis="listener may hear an Am7 tilt with unresolved C-centered memory",
            actual_listening_observation=None,
        ),
        InterventionCase(
            name="full_tilt",
            state=VoicedState(
                name="full_tilt_state",
                notes=("A2", "C3", "E3", "G3"),
                bass="A",
                preceding_context="C-centered memory retained",
                following_context="A-centered continuation becomes available",
            ),
            primary_intervention="bass_register_context_bundle",
            residual_changes=(),
            preserved_relations=("pitch_class_set:{C,E,G,A}", "upper_common_relation:C-E-G"),
            changed_relations=(
                "bass_relation:C->A",
                "register_gravity:C3->A2",
                "preceding_context:C-centered arrival->C-centered memory retained",
                "following_context:C-centered expectation->A-centered availability",
            ),
            structural_prediction="Am7 candidate becomes available with bass, register, and context support",
            perceptual_hypothesis="listener may hear the clearest Am7 tilt in this case",
            actual_listening_observation=None,
        ),
    )


def render_chord_segment(notes: tuple[str, ...], seconds: float, amplitude: float = 0.20) -> list[int]:
    frame_count = int(SAMPLE_RATE * seconds)
    frames: list[int] = []
    fade_len = int(SAMPLE_RATE * 0.035)
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


def write_wave(path: Path, states: tuple[VoicedState, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames: list[int] = []
    for state in states:
        frames.extend(render_chord_segment(state.notes, 1.10))
        frames.extend([0] * int(SAMPLE_RATE * 0.16))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(struct.pack("<h", frame) for frame in frames))


def observe(device_audio_path: str = DEVICE_AUDIO_RELATIVE_PATH) -> SeparationObservation:
    source = source_state()
    cases = build_cases()

    assert source.pitch_classes == PITCH_CLASS_SET
    for case in cases:
        assert case.state.pitch_classes == PITCH_CLASS_SET
        assert case.actual_listening_observation is None
        assert classify_state(case.state) != "out_of_fixture"

    return SeparationObservation(
        source=source,
        cases=cases,
        device_audio_path=device_audio_path,
        manifest_path=MANIFEST_RELATIVE_PATH,
        stop_lines=(
            "intervention_axis_is_not_always_pure_in_audio_realization",
            "structural_prediction_is_not_actual_human_listening",
            "context_only_change_may_have_no_device_audio_difference",
            "classification_is_candidate_not_final_chord_truth",
        ),
    )


def observation_to_manifest(observation: SeparationObservation) -> dict[str, object]:
    return {
        "schema": "rdl_music_v02_intervention_separation_v0_1",
        "subject": "C6_Am7_intervention_separation",
        "source": asdict(observation.source),
        "source_classification": classify_state(observation.source),
        "cases": [
            {
                **asdict(case),
                "classification": classify_state(case.state),
            }
            for case in observation.cases
        ],
        "device_audio_path": observation.device_audio_path,
        "manifest_path": observation.manifest_path,
        "stop_lines": list(observation.stop_lines),
    }


def write_manifest(path: Path, observation: SeparationObservation) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(observation_to_manifest(observation), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    observation = observe()
    audio_path = repo_root / DEVICE_AUDIO_RELATIVE_PATH
    manifest_path = repo_root / MANIFEST_RELATIVE_PATH
    write_wave(audio_path, (observation.source, *(case.state for case in observation.cases)))
    write_manifest(manifest_path, observation)

    print("music_v02_c6_am7_intervention_separation_observed")
    print(f"source={observation.source.name}:{classify_state(observation.source)}")
    for case in observation.cases:
        print(
            f"case={case.name}:{classify_state(case.state)}; "
            f"primary={case.primary_intervention}; "
            f"changed={','.join(case.changed_relations)}; "
            f"actual={case.actual_listening_observation}"
        )
    print(f"device_audio_file={Path(observation.device_audio_path).name}")
    print(f"manifest_file={Path(observation.manifest_path).name}")


if __name__ == "__main__":
    main()