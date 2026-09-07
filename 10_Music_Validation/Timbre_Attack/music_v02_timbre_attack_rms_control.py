"""First-note RMS-matched auxiliary control for the existing harmonic pair."""
from __future__ import annotations

import hashlib
import json

import music_v02_timbre_attack_identity_probe as source
from music_v02_timbre_attack_listening_pairs import pcm_bytes, rms, write_pcm

AUDIO_DIR = source.ROOT / "artifacts/audio/timbre_attack_rms_control"
MANIFEST = source.ROOT / "artifacts/json/music_v02_timbre_attack_rms_control.json"


def main() -> None:
    frames = {frame.name: frame for frame in source.build_frames()}
    reference = frames["soft_sine_reference"]
    variant = frames["bright_harmonic_profile_same_attack"]
    assert reference.attack_seconds == variant.attack_seconds
    assert reference.release_seconds == variant.release_seconds
    assert reference.preserved_pitches == variant.preserved_pitches
    assert reference.preserved_onsets_beats == variant.preserved_onsets_beats
    assert reference.preserved_duration_beats == variant.preserved_duration_beats
    assert reference.transient_noise_amount == variant.transient_noise_amount == 0
    baseline = source.render_frame(reference)
    original = source.render_frame(variant)
    duration = int(source.NOTE_DURATION_BEATS * source.BEAT_SECONDS * source.SAMPLE_RATE)
    target = rms(baseline[:duration])
    gain = target / rms(original[:duration])
    matched = [round(value * gain) for value in original]
    assert len(matched) == len(baseline)
    assert max(abs(value) for value in matched) < 32767
    assert abs(rms(matched[:duration]) - target) <= 1 / 32767
    assert all(abs(after - before * gain) <= 0.5 for before, after in zip(original, matched))
    assert all(after == 0 for before, after in zip(original, matched) if before == 0)
    note_measurements = []
    for note, beat in source.MATERIAL:
        start = int(beat * source.BEAT_SECONDS * source.SAMPLE_RATE)
        end = start + duration
        note_measurements.append({
            "note": note,
            "window_samples": [start, end],
            "reference_rms": rms(baseline[start:end]),
            "original_variant_rms": rms(original[start:end]),
            "matched_variant_rms": rms(matched[start:end]),
        })
    single_path = AUDIO_DIR / "bright_harmonic_profile_first_note_rms_matched.wav"
    write_pcm(single_path, matched)
    presentations = []
    for order, first, second in (
        ("reference_then_matched", baseline, matched),
        ("matched_then_reference", matched, baseline),
    ):
        path = AUDIO_DIR / (order + ".wav")
        write_pcm(path, first + second)
        presentations.append({
            "order": order,
            "path": path.relative_to(source.ROOT).as_posix(),
            "segment_start_seconds": [0, len(baseline) / source.SAMPLE_RATE],
            "actual_listening_observation": None,
        })
    manifest = {
        "schema": "rdl_music_timbre_attack_rms_control_v1",
        "source": "10_Music_Validation/Timbre_Attack/music_v02_timbre_attack_identity_probe.py",
        "fixed_gain_comparison_manifest": "artifacts/json/music_v02_timbre_attack_listening_pairs.json",
        "reference": reference.name,
        "variant": variant.name,
        "primary_intervention": "harmonic_profile",
        "auxiliary_intervention": "uniform_gain_on_variant",
        "match_window": "first note, including attack, plateau and release; no trailing silence",
        "sample_rate": source.SAMPLE_RATE,
        "gain": gain,
        "quantization": "round scaled source PCM to nearest integer; no clipping or limiter",
        "structural_prediction": "first-note RMS agrees within one 16-bit quantization step",
        "device_observation": {
            "note_measurements": note_measurements,
            "reference_peak": max(abs(value) for value in baseline) / 32767,
            "matched_peak": max(abs(value) for value in matched) / 32767,
            "reference_pcm_sha256": hashlib.sha256(pcm_bytes(baseline)).hexdigest(),
            "original_variant_pcm_sha256": hashlib.sha256(pcm_bytes(original)).hexdigest(),
            "matched_pcm_sha256": hashlib.sha256(pcm_bytes(matched)).hexdigest(),
            "first_note_rms_error": rms(matched[:duration]) - target,
        },
        "individual_path": single_path.relative_to(source.ROOT).as_posix(),
        "presentations": presentations,
        "perceptual_hypothesis": "harmonic-color distinction may remain when first-note RMS is matched",
        "actual_listening_observation": None,
        "stop_lines": [
            "first_note_RMS_match_is_not_perceptual_loudness_match",
            "other_notes_are_measured_not_individually_normalized",
            "uniform_gain_changes_absolute_partial_amplitudes",
            "matching_RMS_does_not_hold_fundamental_amplitude",
            "original_fixed_gain_fixture_is_preserved",
            "no_human_discrimination_or_Core_update_inferred_from_PCM",
        ],
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"gain={gain:.9f}; first_note_RMS_error={rms(matched[:duration]) - target:.9g}")
    print(f"matched_peak={manifest['device_observation']['matched_peak']:.6f}")
    print("Verified unclipped uniform gain, RMS tolerance, PCM round trips: 3 WAVs.")


if __name__ == "__main__":
    main()

