"""C6 / Am7 temporal-context probe for Music v0.2.

The target sonority is physically identical in each phrase: C3 E3 G3 A3.
Only the preceding and following chords change. This turns context from a
manifest-only label into a time-realized relation that can be listened to later.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import wave

ROOT = Path(__file__).resolve().parents[2]
AUDIO_RELATIVE_PATH = "artifacts/audio/music_v02_c6_am7_temporal_context_probe.wav"
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_c6_am7_temporal_context_probe.json"
SAMPLE_RATE = 44_100
SECONDS_PER_CHORD = 0.95
SILENCE_SECONDS = 0.16
PHRASE_GAP_SECONDS = 0.42
TARGET_NOTES = ("C3", "E3", "G3", "A3")

NOTE_FREQUENCIES = {
    "A2": 110.000,
    "B2": 123.471,
    "C3": 130.813,
    "D3": 146.832,
    "E3": 164.814,
    "F3": 174.614,
    "G3": 195.998,
    "A3": 220.000,
    "B3": 246.942,
    "C4": 261.626,
}


@dataclass(frozen=True)
class ChordEvent:
    role: str
    notes: tuple[str, ...]
    label: str


@dataclass(frozen=True)
class ContextPhrase:
    name: str
    preceding: ChordEvent
    target: ChordEvent
    following: ChordEvent
    preserved_target_notes: tuple[str, ...]
    changed_relation: str
    structural_prediction: str
    perceptual_hypothesis: str
    actual_listening_observation: str | None
    candidate_classification: str


def chord(role: str, notes: tuple[str, ...], label: str) -> ChordEvent:
    return ChordEvent(role=role, notes=notes, label=label)


def build_phrases() -> list[ContextPhrase]:
    target = chord("target", TARGET_NOTES, "shared_C_E_G_A_sonority")
    return [
        ContextPhrase(
            name="c_centered_frame",
            preceding=chord("preceding_context", ("C3", "E3", "G3"), "C_major_arrival"),
            target=target,
            following=chord("following_context", ("C3", "E3", "G3", "C4"), "C_major_continuation"),
            preserved_target_notes=TARGET_NOTES,
            changed_relation="temporal_context:C-centered before and after target",
            structural_prediction="the identical target sonority is framed as C6-side stable",
            perceptual_hypothesis="listener may retain C as the local reference through the target",
            actual_listening_observation=None,
            candidate_classification="C6_candidate_by_temporal_context",
        ),
        ContextPhrase(
            name="a_centered_frame",
            preceding=chord("preceding_context", ("A2", "C3", "E3"), "A_minor_arrival"),
            target=target,
            following=chord("following_context", ("A2", "C3", "E3", "A3"), "A_minor_continuation"),
            preserved_target_notes=TARGET_NOTES,
            changed_relation="temporal_context:A-centered before and after target",
            structural_prediction="the identical target sonority is framed as Am7-side available",
            perceptual_hypothesis="listener may hear the target as belonging more readily to A minor",
            actual_listening_observation=None,
            candidate_classification="Am7_candidate_by_temporal_context",
        ),
        ContextPhrase(
            name="c_to_a_pivot_frame",
            preceding=chord("preceding_context", ("C3", "E3", "G3"), "C_major_arrival"),
            target=target,
            following=chord("following_context", ("A2", "C3", "E3", "A3"), "A_minor_continuation"),
            preserved_target_notes=TARGET_NOTES,
            changed_relation="temporal_context:C-centered before target, A-centered after target",
            structural_prediction="the identical target sonority acts as a pivot from C6 stability toward Am7 availability",
            perceptual_hypothesis="listener may hear a delayed reinterpretation at or after the following chord",
            actual_listening_observation=None,
            candidate_classification="C6_Am7_pivot_candidate",
        ),
        ContextPhrase(
            name="a_to_c_resistance_frame",
            preceding=chord("preceding_context", ("A2", "C3", "E3"), "A_minor_arrival"),
            target=target,
            following=chord("following_context", ("C3", "E3", "G3", "C4"), "C_major_continuation"),
            preserved_target_notes=TARGET_NOTES,
            changed_relation="temporal_context:A-centered before target, C-centered after target",
            structural_prediction="the identical target sonority opens Am7 expectation but is reabsorbed into C-centered continuation",
            perceptual_hypothesis="listener may hear A-minor color that fails to settle as the following C frame returns",
            actual_listening_observation=None,
            candidate_classification="Am7_pressure_with_C_reabsorption_candidate",
        ),
    ]


def sine_sample(frequency: float, index: int, duration: float) -> float:
    t = index / SAMPLE_RATE
    attack = min(t / 0.025, 1.0)
    release = min((duration - t) / 0.07, 1.0)
    envelope = max(0.0, min(attack, release))
    return math.sin(2.0 * math.pi * frequency * t) * envelope


def render_chord(event: ChordEvent) -> list[int]:
    frames = int(SAMPLE_RATE * SECONDS_PER_CHORD)
    samples: list[int] = []
    bass_note = min(event.notes, key=lambda note: NOTE_FREQUENCIES[note])
    for i in range(frames):
        value = 0.0
        for note in event.notes:
            amp = 0.20 if note == bass_note else 0.115
            value += amp * sine_sample(NOTE_FREQUENCIES[note], i, SECONDS_PER_CHORD)
        samples.append(int(max(-0.95, min(0.95, value)) * 32767))
    samples.extend([0] * int(SAMPLE_RATE * SILENCE_SECONDS))
    return samples


def render_phrase(phrase: ContextPhrase) -> list[int]:
    samples: list[int] = []
    for event in (phrase.preceding, phrase.target, phrase.following):
        samples.extend(render_chord(event))
    samples.extend([0] * int(SAMPLE_RATE * PHRASE_GAP_SECONDS))
    return samples


def write_wave(phrases: list[ContextPhrase], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples: list[int] = []
    for phrase in phrases:
        samples.extend(render_phrase(phrase))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(sample.to_bytes(2, "little", signed=True) for sample in samples))


def write_manifest(phrases: list[ContextPhrase], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "rdl_music_v02_c6_am7_temporal_context_probe_v0_1",
        "subject": "C6_Am7_temporal_context_probe",
        "target_invariance": {
            "target_notes": list(TARGET_NOTES),
            "target_is_identical_in_all_phrases": True,
        },
        "phrases": [asdict(phrase) for phrase in phrases],
        "device_audio_path": AUDIO_RELATIVE_PATH,
        "manifest_path": MANIFEST_RELATIVE_PATH,
        "stop_lines": [
            "target_sonority_identity_is_not_context_identity",
            "temporal_context_is_realized_in_audio_not_only_manifest_text",
            "structural_prediction_is_not_actual_human_listening",
            "candidate_classification_is_not_final_chord_truth",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    phrases = build_phrases()
    assert all(phrase.target.notes == TARGET_NOTES for phrase in phrases)
    assert all(phrase.preserved_target_notes == TARGET_NOTES for phrase in phrases)
    assert all(phrase.actual_listening_observation is None for phrase in phrases)
    audio_path = ROOT / AUDIO_RELATIVE_PATH
    manifest_path = ROOT / MANIFEST_RELATIVE_PATH
    write_wave(phrases, audio_path)
    write_manifest(phrases, manifest_path)
    print("music_v02_c6_am7_temporal_context_probe_observed")
    for phrase in phrases:
        print(
            f"phrase={phrase.name}; target={','.join(phrase.target.notes)}; "
            f"context={phrase.changed_relation}; class={phrase.candidate_classification}; "
            f"actual={phrase.actual_listening_observation}"
        )
    print(f"device_audio_file={audio_path.name}")
    print(f"manifest_file={manifest_path.name}")


if __name__ == "__main__":
    main()