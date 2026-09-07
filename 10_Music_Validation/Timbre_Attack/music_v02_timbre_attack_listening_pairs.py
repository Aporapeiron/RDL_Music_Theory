"""Export existing timbre controls as listening pairs and verify PCM differences."""
from __future__ import annotations

from array import array
import hashlib
import json
import math
from pathlib import Path
import sys
import wave

import music_v02_timbre_attack_identity_probe as source

AUDIO_DIR = source.ROOT / "artifacts/audio/timbre_attack_pairs"
MANIFEST = source.ROOT / "artifacts/json/music_v02_timbre_attack_listening_pairs.json"
AXES = ("attack", "harmonic_profile", "transient_noise")


def pcm_bytes(samples: list[int]) -> bytes:
    data = array("h", samples)
    if sys.byteorder != "little":
        data.byteswap()
    return data.tobytes()


def write_pcm(path: Path, samples: list[int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = pcm_bytes(samples)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(source.SAMPLE_RATE)
        wav.writeframes(payload)
    with wave.open(str(path), "rb") as wav:
        assert wav.getparams()[:3] == (1, 2, source.SAMPLE_RATE)
        assert wav.readframes(wav.getnframes()) == payload


def rms(samples: list[int]) -> float:
    return math.sqrt(sum(value * value for value in samples) / len(samples)) / 32767


def main() -> None:
    frames = source.build_frames()[:4]
    reference = frames[0]
    controls = dict(zip(AXES, frames[1:]))
    rendered = {frame.name: source.render_frame(frame) for frame in frames}
    reference_pcm = rendered[reference.name]
    duration = int(source.NOTE_DURATION_BEATS * source.BEAT_SECONDS * source.SAMPLE_RATE)
    starts = [int(beat * source.BEAT_SECONDS * source.SAMPLE_RATE) for _, beat in source.MATERIAL]
    comparisons = []
    artifacts = []
    for frame in frames:
        samples = rendered[frame.name]
        assert len(samples) == len(reference_pcm)
        assert any(samples)
        assert max(abs(value) for value in samples) < int(0.95 * 32767)
        assert frame.preserved_pitches == reference.preserved_pitches
        assert frame.preserved_onsets_beats == reference.preserved_onsets_beats
        assert frame.preserved_duration_beats == reference.preserved_duration_beats
        assert frame.release_seconds == reference.release_seconds
        path = AUDIO_DIR / (frame.name + ".wav")
        write_pcm(path, samples)
        artifacts.append({
            "condition": frame.name,
            "path": path.relative_to(source.ROOT).as_posix(),
            "pcm_sha256": hashlib.sha256(pcm_bytes(samples)).hexdigest(),
            "first_note_rms_full_scale": rms(samples[:duration]),
            "peak_full_scale": max(abs(value) for value in samples) / 32767,
            "actual_listening_observation": None,
        })

    for axis, frame in controls.items():
        changed = [
            name for name in ("attack_seconds", "harmonic_profile", "transient_noise_amount")
            if getattr(frame, name) != getattr(reference, name)
        ]
        expected = dict(attack="attack_seconds", harmonic_profile="harmonic_profile",
                        transient_noise="transient_noise_amount")[axis]
        assert changed == [expected]
        samples = rendered[frame.name]
        changed_indices = [i for i, (a, b) in enumerate(zip(reference_pcm, samples)) if a != b]
        assert changed_indices
        # Verify that changed PCM samples stay inside the intervention's support.
        window_seconds = {
            "attack": reference.attack_seconds,
            "harmonic_profile": source.NOTE_DURATION_BEATS * source.BEAT_SECONDS,
            "transient_noise": 0.045,
        }[axis]
        assert all(
            any(0 <= i - start < window_seconds * source.SAMPLE_RATE for start in starts)
            for i in changed_indices
        )
        pairs = []
        for order, sequence in (
            ("reference_then_variant", (reference.name, frame.name)),
            ("variant_then_reference", (frame.name, reference.name)),
        ):
            combined = rendered[sequence[0]] + rendered[sequence[1]]
            path = AUDIO_DIR / (axis + "_" + order + ".wav")
            write_pcm(path, combined)
            pairs.append({
                "order": list(sequence),
                "path": path.relative_to(source.ROOT).as_posix(),
                "segment_start_seconds": [0, len(reference_pcm) / source.SAMPLE_RATE],
                "actual_listening_observation": None,
            })
        comparisons.append({
            "primary_intervention": axis,
            "reference": reference.name,
            "variant": frame.name,
            "structural_prediction": "PCM differences occur only within the declared per-note window",
            "device_observation": {
                "changed_pcm_samples": len(changed_indices),
                "per_note_difference_window_seconds": window_seconds,
                "outside_window_pcm_identical": True,
                "first_note_difference_rms_full_scale": rms([
                    b - a for a, b in zip(reference_pcm[:duration], samples[:duration])
                ]),
            },
            "perceptual_hypothesis": frame.perceptual_hypothesis,
            "actual_listening_observation": None,
            "presentations": pairs,
        })
    manifest = {
        "schema": "rdl_music_timbre_attack_listening_pairs_v1",
        "source": str(Path(source.__file__).relative_to(source.ROOT).as_posix()),
        "sample_rate": source.SAMPLE_RATE,
        "gain_policy": "existing renderer gain; no added peak/RMS/loudness normalization",
        "trailing_silence_seconds": (len(reference_pcm) - starts[-1] - duration) / source.SAMPLE_RATE,
        "measurement_scope": "16-bit rendered PCM; first-note RMS includes attack, plateau and release",
        "individual_artifacts": artifacts,
        "comparisons": comparisons,
        "stop_lines": [
            "PCM_difference_is_not_perceptual_discrimination",
            "RMS_is_not_perceived_loudness",
            "reverse_order_does_not_remove_memory_or_expectation",
            "harmonic_profile_normalization_can_change_fundamental_amplitude_and_RMS",
            "noise_difference_is_window_limited_and_may_not_be_audible",
            "no_E_H_theta_or_Core_update_without_specified_model_and_observation",
        ],
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Verified 4 individual WAVs, 6 ordered pairs and intervention-local PCM differences.")
    for artifact in artifacts:
        print(artifact["condition"], "first_note_rms=", round(artifact["first_note_rms_full_scale"], 6))
    print(MANIFEST.relative_to(source.ROOT))


if __name__ == "__main__":
    main()

