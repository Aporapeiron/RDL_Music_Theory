"""Encoded melody transposition and chromatic inversion with preserved timing."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "10_Music_Validation/Voice_Placement"))
import music_voice_placement_crossing as audio

MELODY = (60, 62, 64, 67, 65, 64, 62, 60)
AXIS = 60
SHIFT = 5
OUT = ROOT / "artifacts/audio/melody_transformation"


def main():
    variants = {
        "source": MELODY,
        "transposed_up_five": tuple(n + SHIFT for n in MELODY),
        "inverted_about_C4": tuple(2 * AXIS - n for n in MELODY),
    }
    source_intervals = audio.intervals(MELODY)
    assert audio.intervals(variants["transposed_up_five"]) == source_intervals
    assert audio.intervals(variants["inverted_about_C4"]) == [-n for n in source_intervals]
    assert tuple(2 * AXIS - n for n in variants["inverted_about_C4"]) == MELODY
    assert tuple(n - SHIFT for n in variants["transposed_up_five"]) == MELODY
    records, sequence = [], []
    for name, notes in variants.items():
        pcm = audio.quantize(audio.render_voice(notes))
        assert len(pcm) == audio.TOTAL_SAMPLES and any(pcm)
        path = OUT / (name + ".wav")
        audio.write_pcm(path, pcm)
        steps = audio.intervals(notes)
        records.append({
            "name": name, "midi_notes": list(notes),
            "signed_intervals_semitones": steps,
            "absolute_intervals_semitones": [abs(n) for n in steps],
            "contour": [(n > 0) - (n < 0) for n in steps],
            "range_midi": [min(notes), max(notes)],
            "encoded_pitch_class_set": sorted({n % 12 for n in notes}),
            "path": path.relative_to(ROOT).as_posix(),
            "pcm_sha256": hashlib.sha256(audio.pcm_bytes(pcm)).hexdigest(),
            "peak_full_scale": max(abs(n) for n in pcm) / 32767,
            "actual_listening_observation": None,
        })
        sequence.extend(pcm)
    sequence_path = OUT / "source_transposition_inversion.wav"
    audio.write_pcm(sequence_path, sequence)
    manifest = {
        "schema": "rdl_music_melody_transformation_v1",
        "material_origin": "authored monophonic eight-note fixture",
        "boundary": {"tuning": "12TET, A4=440Hz", "sample_rate": audio.synth.SAMPLE_RATE,
                     "onsets_beats": list(range(8)), "beat_seconds": audio.synth.BEAT_SECONDS,
                     "duration_beats": audio.synth.NOTE_DURATION_BEATS,
                     "inversion_axis_midi": AXIS, "transposition_semitones": SHIFT},
        "preserved_all": ["onsets", "durations", "note order as event IDs",
                          "absolute melodic interval sizes", "synthesis settings"],
        "transposition_preserves": ["signed melodic intervals", "contour"],
        "inversion_changes": ["sign of nonzero melodic intervals", "contour"],
        "entailed_changes": ["register and absolute frequencies", "pitch-class content may change"],
        "interpretation": "chromatic semitone reflection, not diatonic inversion in a fixed key",
        "conditions": records,
        "presentation": {"path": sequence_path.relative_to(ROOT).as_posix(),
                         "order": list(variants),
                         "segment_start_seconds": [i * audio.TOTAL_SAMPLES / audio.synth.SAMPLE_RATE for i in range(3)]},
        "perceptual_hypothesis": "transformed versions may remain recognizably related; untested",
        "actual_listening_observation": None,
        "stop_lines": ["encoded_invariants_are_not_perceived_melody_identity",
                       "synthesis_settings_are_not_perceived_timbre_or_loudness",
                       "no_automatic_key_or_harmonic_function_assignment"],
    }
    path = ROOT / "artifacts/json/music_melody_transformation.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Verified interval invariants, inverse transforms, four WAV round trips.")
    for record in records:
        print(record["name"], record["signed_intervals_semitones"])


if __name__ == "__main__":
    main()

