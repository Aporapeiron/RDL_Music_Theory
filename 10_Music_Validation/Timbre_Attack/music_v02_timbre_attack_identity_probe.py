"""Timbre / attack identity probe for Music v0.2.

This fixture keeps pitch, onset, duration, and note order stable while changing
attack envelope, harmonic spectrum, and transient noise. The generated audio is
a device-side fixture, not a confirmation of human timbre perception.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import random
import wave

ROOT = Path(__file__).resolve().parents[2]
AUDIO_RELATIVE_PATH = "artifacts/audio/music_v02_timbre_attack_identity_probe.wav"
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_timbre_attack_identity_probe.json"
SAMPLE_RATE = 44_100
BEAT_SECONDS = 0.5
PHRASE_GAP_SECONDS = 0.75
MATERIAL = (("C4", 0), ("E4", 1), ("G4", 2), ("C5", 3))
NOTE_DURATION_BEATS = 0.82
BASE_AMPLITUDE = 0.24

NOTE_FREQUENCIES = {
    "C4": 261.626,
    "E4": 329.628,
    "G4": 391.995,
    "C5": 523.251,
}


@dataclass(frozen=True)
class TimbreAttackFrame:
    name: str
    preserved_pitches: tuple[str, ...]
    preserved_onsets_beats: tuple[int, ...]
    preserved_duration_beats: float
    attack_seconds: float
    release_seconds: float
    harmonic_profile: tuple[float, ...]
    transient_noise_amount: float
    primary_interventions: tuple[str, ...]
    derived_relations: tuple[str, ...]
    timbre_attack_candidate: str
    structural_prediction: str
    perceptual_hypothesis: str
    actual_listening_observation: str | None
    candidate_classification: str

    @property
    def harmonic_count(self) -> int:
        return len(self.harmonic_profile)

    @property
    def brightness_proxy(self) -> float:
        weighted_sum = sum((index + 1) * amp for index, amp in enumerate(self.harmonic_profile))
        total = sum(self.harmonic_profile)
        return round(weighted_sum / total, 3)

    @property
    def attack_slope_proxy(self) -> float:
        return round(1.0 / self.attack_seconds, 3)


def build_frames() -> list[TimbreAttackFrame]:
    pitches = tuple(note for note, _beat in MATERIAL)
    onsets = tuple(beat for _note, beat in MATERIAL)
    return [
        TimbreAttackFrame(
            name="soft_sine_reference",
            preserved_pitches=pitches,
            preserved_onsets_beats=onsets,
            preserved_duration_beats=NOTE_DURATION_BEATS,
            attack_seconds=0.09,
            release_seconds=0.08,
            harmonic_profile=(1.0,),
            transient_noise_amount=0.0,
            primary_interventions=("reference attack envelope", "reference harmonic spectrum"),
            derived_relations=("attack_slope_proxy = 11.111", "brightness_proxy = 1.0", "transient_noise_amount = 0.0"),
            timbre_attack_candidate="soft_sine_reference_candidate",
            structural_prediction="same pitch-onset material with soft attack and minimal spectrum",
            perceptual_hypothesis="listener may hear a rounded or vowel-like entry",
            actual_listening_observation=None,
            candidate_classification="soft_attack_low_brightness_candidate",
        ),
        TimbreAttackFrame(
            name="sharp_attack_same_spectrum",
            preserved_pitches=pitches,
            preserved_onsets_beats=onsets,
            preserved_duration_beats=NOTE_DURATION_BEATS,
            attack_seconds=0.008,
            release_seconds=0.08,
            harmonic_profile=(1.0,),
            transient_noise_amount=0.0,
            primary_interventions=("shorten attack envelope",),
            derived_relations=("attack_slope_proxy = 125.0", "brightness_proxy = 1.0", "transient_noise_amount = 0.0"),
            timbre_attack_candidate="sharp_attack_same_spectrum_candidate",
            structural_prediction="same spectrum with sharper onset edge",
            perceptual_hypothesis="listener may hear a more percussive entry without pitch/onset change",
            actual_listening_observation=None,
            candidate_classification="attack_changed_spectrum_preserved_candidate",
        ),
        TimbreAttackFrame(
            name="bright_spectrum_same_attack",
            preserved_pitches=pitches,
            preserved_onsets_beats=onsets,
            preserved_duration_beats=NOTE_DURATION_BEATS,
            attack_seconds=0.09,
            release_seconds=0.08,
            harmonic_profile=(1.0, 0.45, 0.22, 0.12),
            transient_noise_amount=0.0,
            primary_interventions=("add upper harmonics",),
            derived_relations=("attack_slope_proxy = 11.111", "brightness_proxy = 1.698", "transient_noise_amount = 0.0"),
            timbre_attack_candidate="bright_spectrum_same_attack_candidate",
            structural_prediction="same attack timing with brighter harmonic distribution",
            perceptual_hypothesis="listener may hear brighter color without changed onset placement",
            actual_listening_observation=None,
            candidate_classification="spectrum_changed_attack_preserved_candidate",
        ),
        TimbreAttackFrame(
            name="transient_noise_attack",
            preserved_pitches=pitches,
            preserved_onsets_beats=onsets,
            preserved_duration_beats=NOTE_DURATION_BEATS,
            attack_seconds=0.008,
            release_seconds=0.08,
            harmonic_profile=(1.0, 0.38, 0.16),
            transient_noise_amount=0.08,
            primary_interventions=("shorten attack envelope", "add attack transient noise", "add upper harmonics"),
            derived_relations=("attack_slope_proxy = 125.0", "brightness_proxy = 1.455", "transient_noise_amount = 0.08"),
            timbre_attack_candidate="transient_attack_color_candidate",
            structural_prediction="same pitch-onset material with sharper and noisier attack color",
            perceptual_hypothesis="listener may hear plucked or struck articulation",
            actual_listening_observation=None,
            candidate_classification="attack_and_spectrum_changed_candidate",
        ),
    ]


def envelope(t: float, duration: float, attack: float, release: float) -> float:
    attack_part = min(t / attack, 1.0) if attack > 0 else 1.0
    release_part = min((duration - t) / release, 1.0) if release > 0 else 1.0
    return max(0.0, min(attack_part, release_part))


def tone_sample(frequency: float, t: float, frame: TimbreAttackFrame, rng: random.Random) -> float:
    duration = frame.preserved_duration_beats * BEAT_SECONDS
    amp = envelope(t, duration, frame.attack_seconds, frame.release_seconds)
    value = 0.0
    for harmonic, harmonic_amp in enumerate(frame.harmonic_profile, start=1):
        value += harmonic_amp * math.sin(2.0 * math.pi * frequency * harmonic * t)
    value /= max(1.0, sum(frame.harmonic_profile))
    if t < 0.045 and frame.transient_noise_amount > 0.0:
        noise_decay = math.exp(-t * 85.0)
        value += frame.transient_noise_amount * noise_decay * rng.uniform(-1.0, 1.0)
    return BASE_AMPLITUDE * amp * value


def add_note(samples: list[float], note: str, start_beat: int, frame: TimbreAttackFrame, rng: random.Random) -> None:
    duration = frame.preserved_duration_beats * BEAT_SECONDS
    frames = int(SAMPLE_RATE * duration)
    start_frame = int(start_beat * BEAT_SECONDS * SAMPLE_RATE)
    frequency = NOTE_FREQUENCIES[note]
    for index in range(frames):
        pos = start_frame + index
        if pos < len(samples):
            samples[pos] += tone_sample(frequency, index / SAMPLE_RATE, frame, rng)


def render_frame(frame: TimbreAttackFrame) -> list[int]:
    total_beats = max(frame.preserved_onsets_beats) + 2
    total_frames = int(SAMPLE_RATE * (total_beats * BEAT_SECONDS + PHRASE_GAP_SECONDS))
    values = [0.0] * total_frames
    rng = random.Random(frame.name)
    for note, beat in MATERIAL:
        add_note(values, note, beat, frame, rng)
    return [int(max(-0.95, min(0.95, sample)) * 32767) for sample in values]


def frame_record(frame: TimbreAttackFrame) -> dict[str, object]:
    record = asdict(frame)
    record["harmonic_count"] = frame.harmonic_count
    record["brightness_proxy"] = frame.brightness_proxy
    record["attack_slope_proxy"] = frame.attack_slope_proxy
    return record


def write_wave(frames: list[TimbreAttackFrame], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples: list[int] = []
    for frame in frames:
        samples.extend(render_frame(frame))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(sample.to_bytes(2, "little", signed=True) for sample in samples))


def write_manifest(frames: list[TimbreAttackFrame], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "rdl_music_v02_timbre_attack_identity_probe_v0_1",
        "subject": "timbre_attack_identity_probe",
        "preserved_material": {
            "pitches": [note for note, _beat in MATERIAL],
            "onsets_beats": [beat for _note, beat in MATERIAL],
            "duration_beats": NOTE_DURATION_BEATS,
            "note_order": [note for note, _beat in MATERIAL],
        },
        "frames": [frame_record(frame) for frame in frames],
        "device_audio_path": AUDIO_RELATIVE_PATH,
        "manifest_path": MANIFEST_RELATIVE_PATH,
        "stop_lines": [
            "same_pitch_onset_duration_is_not_same_timbre_attack_candidate_state",
            "attack_envelope_is_not_identical_to_spectrum",
            "spectrum_change_is_not_pitch_change_in_this_fixture",
            "transient_noise_is_attack_color_fixture_not_listener_confirmation",
            "brightness_proxy_is_fixture_descriptor_not_universal_timbre_constant",
            "device_audio_generation_is_not_actual_listening_observation",
            "actual_listening_observation_remains_null_until_recorded",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    frames = build_frames()
    expected_pitches = tuple(note for note, _beat in MATERIAL)
    expected_onsets = tuple(beat for _note, beat in MATERIAL)
    assert all(frame.preserved_pitches == expected_pitches for frame in frames)
    assert all(frame.preserved_onsets_beats == expected_onsets for frame in frames)
    assert frames[0].harmonic_count == 1
    assert frames[1].harmonic_profile == frames[0].harmonic_profile
    assert frames[1].attack_seconds < frames[0].attack_seconds
    assert frames[2].attack_seconds == frames[0].attack_seconds
    assert frames[2].brightness_proxy > frames[0].brightness_proxy
    assert frames[3].transient_noise_amount > 0.0
    assert all(frame.actual_listening_observation is None for frame in frames)

    audio_path = ROOT / AUDIO_RELATIVE_PATH
    manifest_path = ROOT / MANIFEST_RELATIVE_PATH
    write_wave(frames, audio_path)
    write_manifest(frames, manifest_path)
    print("music_v02_timbre_attack_identity_probe_observed")
    for frame in frames:
        print(
            f"frame={frame.name}; attack={frame.attack_seconds}; brightness={frame.brightness_proxy}; "
            f"class={frame.candidate_classification}; actual={frame.actual_listening_observation}"
        )
    print(f"device_audio_file={audio_path.name}")
    print(f"manifest_file={manifest_path.name}")


if __name__ == "__main__":
    main()