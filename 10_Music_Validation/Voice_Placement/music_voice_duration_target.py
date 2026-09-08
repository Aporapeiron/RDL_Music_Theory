"""Duration-target pilot; presentation IDs and answer key are stored separately."""
from dataclasses import replace
import hashlib
import json
import random

import music_voice_placement_crossing as base

ROOT = base.ROOT
OUT = ROOT / "artifacts/audio/voice_duration_target"
PUBLIC = ROOT / "artifacts/json/voice_duration_target_presentations.json"
KEY = ROOT / "artifacts/json/voice_duration_target_answer_key.json"
SHORT_BEATS = 0.36


def shorten(notes, original, event):
    samples = original.copy()
    start = int(event * base.synth.BEAT_SECONDS * base.synth.SAMPLE_RATE)
    samples[start:start + base.NOTE_SAMPLES] = [0.0] * base.NOTE_SAMPLES
    frame = replace(base.FRAME, preserved_duration_beats=SHORT_BEATS)
    count = int(SHORT_BEATS * base.synth.BEAT_SECONDS * base.synth.SAMPLE_RATE)
    frequency = 440 * 2 ** ((notes[event] - 69) / 12)
    rng = random.Random(0)
    for index in range(count):
        samples[start + index] = base.synth.tone_sample(
            frequency, index / base.synth.SAMPLE_RATE, frame, rng
        )
    assert samples[:start] == original[:start]
    assert samples[start + base.NOTE_SAMPLES:] == original[start + base.NOTE_SAMPLES:]
    assert samples[start + count:start + base.NOTE_SAMPLES] == [0.0] * (base.NOTE_SAMPLES - count)
    return samples


def outcome(target_present, response):
    if response is None or response == "uncertain":
        return "unscored"
    if response not in ("yes", "no"):
        raise ValueError("response must be yes, no, uncertain or null")
    return {
        (True, "yes"): "hit", (True, "no"): "miss",
        (False, "yes"): "false_alarm", (False, "no"): "correct_rejection",
    }[(target_present, response)]


def save_audio(name, pcm):
    path = OUT / (name + ".wav")
    base.write_pcm(path, pcm)
    return {"path": path.relative_to(ROOT).as_posix(),
            "pcm_sha256": hashlib.sha256(base.pcm_bytes(pcm)).hexdigest()}


def main():
    notes_a = base.VOICE_A
    notes_b = tuple(note + 12 for note in base.VOICE_B)
    a = base.render_voice(notes_a)
    b = base.render_voice(notes_b)
    baseline = base.quantize([x + y for x, y in zip(a, b)])
    # Short pilot: changed events avoid the two pitch-order reversal onsets.
    plan = [(voice, event) for voice in ("B", "A") for event in (2, 5)]
    plan += [(None, None), (None, None)]
    random.Random(20260908).shuffle(plan)
    presentations, answers = [], []
    for index, (voice, event) in enumerate(plan, 1):
        trial_id = f"T{index:02d}"
        trial_a = shorten(notes_a, a, event) if voice == "A" else a
        trial_b = shorten(notes_b, b, event) if voice == "B" else b
        pcm = base.quantize([x + y for x, y in zip(trial_a, trial_b)])
        if voice is None:
            assert pcm == baseline
        else:
            start = int(event * base.synth.BEAT_SECONDS * base.synth.SAMPLE_RATE)
            assert pcm[:start] == baseline[:start]
            assert pcm[start + base.NOTE_SAMPLES:] == baseline[start + base.NOTE_SAMPLES:]
            assert pcm != baseline
        presentations.append({"trial_id": trial_id, **save_audio(trial_id, pcm)})
        answers.append({
            "trial_id": trial_id, "changed_voice": voice, "event_index": event,
            "target_in_B": voice == "B",
            "condition": "target" if voice == "B" else "other_voice" if voice else "unchanged",
        })
    examples = {
        "B_normal": save_audio("B_normal", base.quantize(b)),
        "B_short_example": save_audio("B_short_example", base.quantize(shorten(notes_b, b, 4))),
    }
    common = {
        "schema": "rdl_voice_duration_target_v1",
        "basis": "existing crossing placement, A fixed; B raised one octave",
        "sample_rate": base.synth.SAMPLE_RATE,
        "normal_duration_beats": base.synth.NOTE_DURATION_BEATS,
        "short_duration_beats": SHORT_BEATS,
        "gain_policy": "fixed per voice; no normalization",
        "primary_intervention": "shorten one note in A or B, or no change",
        "entailed_changes": ["earlier release", "longer local silence in changed voice",
                            "reduced two-voice simultaneity", "local energy change"],
        "response_options": ["yes", "no", "uncertain"],
        "actual_listening_observation": None,
        "limitations": [
            "target_detection_is_not_whole_voice_tracking",
            "temporal_pattern_is_changed_by_target",
            "local_acoustic_cues_can_support_detection",
            "fixed_order_small_pilot_not_population_estimate",
            "answer_key_separation_is_not_double_blinding",
            "training_example_changes_listening_history",
        ],
    }
    PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC.write_text(json.dumps({**common, "examples": examples, "presentations": presentations},
                                indent=2) + "\n", encoding="utf-8")
    KEY.write_text(json.dumps({"schema": "rdl_voice_duration_target_key_v1", "trials": answers},
                             indent=2) + "\n", encoding="utf-8")
    assert outcome(True, "yes") == "hit"
    assert outcome(True, "no") == "miss"
    assert outcome(False, "yes") == "false_alarm"
    assert outcome(False, "no") == "correct_rejection"
    assert outcome(True, "uncertain") == outcome(False, None) == "unscored"
    print("Verified 6 coded trials and 2 solo examples; unchanged controls, local PCM differences and scoring rules.")


if __name__ == "__main__":
    main()

