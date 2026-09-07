"""Two fixed voice IDs under an octave placement intervention.

Crossing denotes a discrete pitch-order reversal between note events,
not an interpolated pitch glide or an observed change of listener attribution.
"""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
import random
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "10_Music_Validation/Timbre_Attack"))
import music_v02_timbre_attack_identity_probe as synth
from music_v02_timbre_attack_listening_pairs import pcm_bytes, write_pcm

VOICE_A = (60, 62, 65, 69, 72, 69, 65, 62)
VOICE_B = (55, 55, 57, 55, 57, 55, 57, 55)
AUDIO_DIR = ROOT / "artifacts/audio/voice_placement"
MANIFEST = ROOT / "artifacts/json/music_voice_placement_crossing.json"
FRAME = synth.build_frames()[0]
NOTE_SAMPLES = int(synth.SAMPLE_RATE * synth.BEAT_SECONDS * synth.NOTE_DURATION_BEATS)
TOTAL_SAMPLES = int(synth.SAMPLE_RATE * (8 * synth.BEAT_SECONDS + 0.75))


def intervals(notes: tuple[int, ...]) -> list[int]:
    return [right - left for left, right in zip(notes, notes[1:])]


def render_voice(notes: tuple[int, ...]) -> list[float]:
    samples = [0.0] * TOTAL_SAMPLES
    rng = random.Random(0)
    for beat, midi in enumerate(notes):
        start = int(beat * synth.BEAT_SECONDS * synth.SAMPLE_RATE)
        frequency = 440.0 * 2 ** ((midi - 69) / 12)
        for index in range(NOTE_SAMPLES):
            samples[start + index] = synth.tone_sample(
                frequency, index / synth.SAMPLE_RATE, FRAME, rng
            )
    return samples


def quantize(samples: list[float]) -> list[int]:
    assert max(abs(value) for value in samples) < 0.95
    return [int(value * 32767) for value in samples]


def write_artifact(name: str, pcm: list[int]) -> dict:
    path = AUDIO_DIR / (name + ".wav")
    write_pcm(path, pcm)
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "pcm_sha256": hashlib.sha256(pcm_bytes(pcm)).hexdigest(),
        "duration_seconds": len(pcm) / synth.SAMPLE_RATE,
        "peak_full_scale": max(abs(value) for value in pcm) / 32767,
    }


def main() -> None:
    raised_b = tuple(note + 12 for note in VOICE_B)
    assert intervals(VOICE_B) == intervals(raised_b)
    assert [note % 12 for note in VOICE_B] == [note % 12 for note in raised_b]
    a_samples = render_voice(VOICE_A)
    a_pcm = quantize(a_samples)
    stems = {"voice_A": write_artifact("voice_A", a_pcm)}
    conditions = []
    mixes = {}
    for name, b_notes in (("separated", VOICE_B), ("crossing", raised_b)):
        b_samples = render_voice(b_notes)
        b_pcm = quantize(b_samples)
        stems[name + "_voice_B"] = write_artifact(name + "_voice_B", b_pcm)
        signed_intervals = [a - b for a, b in zip(VOICE_A, b_notes)]
        assert all(value != 0 for value in signed_intervals)
        reversals = [
            index for index in range(1, len(signed_intervals))
            if signed_intervals[index - 1] * signed_intervals[index] < 0
        ]
        assert reversals == ([] if name == "separated" else [3, 6])
        mix = quantize([a + b for a, b in zip(a_samples, b_samples)])
        assert all(abs(m - a - b) <= 1 for m, a, b in zip(mix, a_pcm, b_pcm))
        assert any(mix)
        mixes[name] = mix
        conditions.append({
            "name": name,
            "voice_midi": {"A": list(VOICE_A), "B": list(b_notes)},
            "melodic_intervals": {"A": intervals(VOICE_A), "B": intervals(b_notes)},
            "voice_ranges_midi": {"A": [min(VOICE_A), max(VOICE_A)], "B": [min(b_notes), max(b_notes)]},
            "signed_vertical_semitones_A_minus_B": signed_intervals,
            "upper_voice_id_per_event": ["A" if value > 0 else "B" for value in signed_intervals],
            "order_reversal_event_indices": reversals,
            "order_reversal_onsets_seconds": [index * synth.BEAT_SECONDS for index in reversals],
            "mix": write_artifact(name, mix),
            "structural_prediction": "stable A-above-B order" if name == "separated" else "pitch order reverses at events 3 and 6",
            "perceptual_hypothesis": "octave placement may affect following voice A or B across changes in pitch order",
            "actual_listening_observation": None,
        })
    assert [
        value % 12 for value in conditions[0]["signed_vertical_semitones_A_minus_B"]
    ] == [value % 12 for value in conditions[1]["signed_vertical_semitones_A_minus_B"]]
    presentations = []
    for order in (("separated", "crossing"), ("crossing", "separated")):
        artifact = write_artifact("_then_".join(order), mixes[order[0]] + mixes[order[1]])
        presentations.append({
            **artifact, "order": list(order),
            "segment_start_seconds": [0, TOTAL_SAMPLES / synth.SAMPLE_RATE],
            "actual_listening_observation": None,
        })
    manifest = {
        "schema": "rdl_music_voice_placement_crossing_v1",
        "material_origin": "authored eight-event fixture, not a transcription",
        "boundary": {
            "voice_ids": ["A", "B"], "tuning": "12TET, A4=440Hz",
            "sample_rate": synth.SAMPLE_RATE, "channels": 1,
            "onsets_beats": list(range(8)), "beat_seconds": synth.BEAT_SECONDS,
            "duration_beats": synth.NOTE_DURATION_BEATS,
            "synthesis": {key: asdict(FRAME)[key] for key in (
                "attack_seconds", "release_seconds", "harmonic_profile", "transient_noise_amount"
            )},
            "per_voice_amplitude": synth.BASE_AMPLITUDE,
            "gain_policy": "fixed per voice; no mix normalization",
            "trailing_silence_seconds": (TOTAL_SAMPLES - 7 * synth.BEAT_SECONDS * synth.SAMPLE_RATE - NOTE_SAMPLES) / synth.SAMPLE_RATE,
        },
        "primary_intervention": "voice B transposed +12 semitones for the entire phrase",
        "preserved": ["voice IDs", "per-voice melodic intervals", "pitch classes", "onset and duration schedules", "synthesis parameters", "voice A PCM"],
        "entailed_changes": ["B register", "signed vertical intervals", "pitch-order reversals", "absolute frequency distribution", "possible mix RMS change"],
        "stems": stems, "conditions": conditions, "presentations": presentations,
        "listening_question": "Can the listener follow voice A or B without switching identity when pitch order changes?",
        "actual_listening_observation": None,
        "stop_lines": [
            "voice_ID_is_not_upper_or_lower_pitch_rank",
            "octave_placement_is_not_crossing_only_intervention",
            "preserved_synthesis_parameters_are_not_preserved_perceived_timbre",
            "pitch_order_reversal_is_not_listener_identity_switch",
            "discrete_events_are_not_continuous_pitch_glides",
            "solo_stem_familiarization_changes_listening_history",
            "no_human_tracking_or_Core_update_inferred_from_PCM",
        ],
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Verified 7 WAVs: three stems, two mixtures and two ordered comparisons.")
    for condition in conditions:
        print(condition["name"], condition["signed_vertical_semitones_A_minus_B"],
              "reversals=", condition["order_reversal_event_indices"])
    print(MANIFEST.relative_to(ROOT))


if __name__ == "__main__":
    main()

