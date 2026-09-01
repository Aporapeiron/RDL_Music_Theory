"""C6 / Am7 relation-weight probe for Music v0.2.

This script keeps the pitch-class set {C,E,G,A} and varies relation axes in
small combinations. It does not decide what a human listener heard. It records
structural pressure toward Am7 and C-centered resistance as device-side Music
fixtures for later actual listening observations.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import wave

ROOT = Path(__file__).resolve().parents[2]
AUDIO_RELATIVE_PATH = "artifacts/audio/music_v02_c6_am7_relation_weight_probe.wav"
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_c6_am7_relation_weight_probe.json"
SAMPLE_RATE = 44_100
SECONDS_PER_STATE = 1.15
SILENCE_SECONDS = 0.18

NOTE_FREQUENCIES = {
    "A2": 110.00,
    "C2": 65.406,
    "C3": 130.813,
    "E3": 164.814,
    "G3": 195.998,
    "A3": 220.000,
}


@dataclass(frozen=True)
class ProbeState:
    name: str
    notes: tuple[str, ...]
    bass: str
    preceding_context: str
    following_context: str
    relation_vector: dict[str, int]
    structural_pressure_to_am7: int
    c_center_resistance: int
    structural_prediction: str
    perceptual_hypothesis: str
    actual_listening_observation: str | None
    classification: str


def source_state() -> ProbeState:
    return ProbeState(
        name="source_C6_stable",
        notes=("C3", "E3", "G3", "A3"),
        bass="C",
        preceding_context="C-centered arrival",
        following_context="C-centered continuation expected",
        relation_vector={"bass_relation": 0, "register_gravity": 0, "context_support": 0},
        structural_pressure_to_am7=0,
        c_center_resistance=3,
        structural_prediction="C6 candidate is foregrounded by bass, register, and context",
        perceptual_hypothesis="listener may hear C as the most stable reference",
        actual_listening_observation=None,
        classification="C6_candidate",
    )


def classify(pressure: int, resistance: int) -> str:
    if pressure >= 5 and resistance <= 1:
        return "Am7_candidate_strong"
    if pressure >= 3:
        return "Am7_tilt_candidate"
    if pressure >= 1:
        return "C6_candidate_with_Am7_pressure"
    return "C6_candidate"


def make_state(
    name: str,
    notes: tuple[str, ...],
    bass: str,
    preceding_context: str,
    following_context: str,
    vector: dict[str, int],
    pressure: int,
    resistance: int,
    prediction: str,
    hypothesis: str,
) -> ProbeState:
    return ProbeState(
        name=name,
        notes=notes,
        bass=bass,
        preceding_context=preceding_context,
        following_context=following_context,
        relation_vector=vector,
        structural_pressure_to_am7=pressure,
        c_center_resistance=resistance,
        structural_prediction=prediction,
        perceptual_hypothesis=hypothesis,
        actual_listening_observation=None,
        classification=classify(pressure, resistance),
    )


def build_probe_states() -> list[ProbeState]:
    return [
        source_state(),
        make_state(
            name="context_only",
            notes=("C3", "E3", "G3", "A3"),
            bass="C",
            preceding_context="C-centered arrival retained",
            following_context="A-centered continuation becomes available",
            vector={"bass_relation": 0, "register_gravity": 0, "context_support": 1},
            pressure=1,
            resistance=3,
            prediction="context adds Am7 availability without rebasing the sounding sonority",
            hypothesis="listener may notice redirection while C remains grounded",
        ),
        make_state(
            name="register_only",
            notes=("C2", "E3", "G3", "A3"),
            bass="C",
            preceding_context="C-centered arrival",
            following_context="C-centered continuation expected",
            vector={"bass_relation": 0, "register_gravity": -1, "context_support": 0},
            pressure=0,
            resistance=4,
            prediction="lower C register reinforces C6 rather than tilting toward Am7",
            hypothesis="listener may hear stronger C grounding",
        ),
        make_state(
            name="bass_only",
            notes=("A2", "C3", "E3", "G3"),
            bass="A",
            preceding_context="C-centered arrival retained",
            following_context="C-centered continuation expected",
            vector={"bass_relation": 2, "register_gravity": 1, "context_support": 0},
            pressure=3,
            resistance=2,
            prediction="A bass creates Am7 tilt, while C-centered context remains as resistance",
            hypothesis="listener may hear a bass-driven Am7 possibility with C memory",
        ),
        make_state(
            name="bass_plus_context",
            notes=("A2", "C3", "E3", "G3"),
            bass="A",
            preceding_context="C-centered memory retained",
            following_context="A-centered continuation becomes available",
            vector={"bass_relation": 2, "register_gravity": 1, "context_support": 1},
            pressure=4,
            resistance=1,
            prediction="bass and following context support Am7, with some C memory retained",
            hypothesis="listener may hear Am7 more readily than in bass_only",
        ),
        make_state(
            name="bass_plus_register",
            notes=("A2", "C3", "E3", "G3"),
            bass="A",
            preceding_context="C-centered arrival retained",
            following_context="C-centered continuation expected",
            vector={"bass_relation": 2, "register_gravity": 1, "context_support": 0},
            pressure=3,
            resistance=2,
            prediction="bass and register act together, but C-centered continuation resists closure",
            hypothesis="listener may hear Am7 color without full contextual release",
        ),
        make_state(
            name="full_tilt",
            notes=("A2", "C3", "E3", "G3"),
            bass="A",
            preceding_context="C-centered memory retained",
            following_context="A-centered continuation becomes available",
            vector={"bass_relation": 2, "register_gravity": 1, "context_support": 2},
            pressure=5,
            resistance=1,
            prediction="bass, register, and context jointly make Am7 the strongest candidate",
            hypothesis="listener may hear the clearest Am7 tilt here",
        ),
    ]


def sine_sample(frequency: float, index: int, duration: float) -> float:
    t = index / SAMPLE_RATE
    attack = min(t / 0.035, 1.0)
    release = min((duration - t) / 0.08, 1.0)
    envelope = max(0.0, min(attack, release))
    return math.sin(2.0 * math.pi * frequency * t) * envelope


def render_state(state: ProbeState) -> list[int]:
    frames = int(SAMPLE_RATE * SECONDS_PER_STATE)
    samples: list[int] = []
    for i in range(frames):
        value = 0.0
        for note in state.notes:
            amp = 0.20 if note.startswith(state.bass) else 0.12
            value += amp * sine_sample(NOTE_FREQUENCIES[note], i, SECONDS_PER_STATE)
        samples.append(int(max(-0.95, min(0.95, value)) * 32767))
    samples.extend([0] * int(SAMPLE_RATE * SILENCE_SECONDS))
    return samples


def write_wave(states: list[ProbeState], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples: list[int] = []
    for state in states:
        samples.extend(render_state(state))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(sample.to_bytes(2, "little", signed=True) for sample in samples))


def write_manifest(states: list[ProbeState], audio_path: Path, manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "rdl_music_v02_c6_am7_relation_weight_probe_v0_1",
        "subject": "C6_Am7_relation_weight_probe",
        "preserved_pitch_class_set": ["C", "E", "G", "A"],
        "scale_note": "scores are structural probe values, not human listening measurements",
        "states": [asdict(state) for state in states],
        "device_audio_path": AUDIO_RELATIVE_PATH,
        "manifest_path": MANIFEST_RELATIVE_PATH,
        "stop_lines": [
            "structural_pressure_score_is_not_actual_hearing_strength",
            "classification_is_candidate_not_chord_truth",
            "relation_weight_is_contextual_not_universal_constant",
            "actual_listening_observation_remains_null_until_recorded",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    states = build_probe_states()
    assert states[0].classification == "C6_candidate"
    assert states[-1].classification == "Am7_candidate_strong"
    assert all(state.actual_listening_observation is None for state in states)
    audio_path = ROOT / AUDIO_RELATIVE_PATH
    manifest_path = ROOT / MANIFEST_RELATIVE_PATH
    write_wave(states, audio_path)
    write_manifest(states, audio_path, manifest_path)
    print("music_v02_c6_am7_relation_weight_probe_observed")
    for state in states:
        print(
            f"state={state.name}; pressure={state.structural_pressure_to_am7}; "
            f"resistance={state.c_center_resistance}; class={state.classification}; actual={state.actual_listening_observation}"
        )
    print(f"device_audio_file={audio_path.name}")
    print(f"manifest_file={manifest_path.name}")


if __name__ == "__main__":
    main()