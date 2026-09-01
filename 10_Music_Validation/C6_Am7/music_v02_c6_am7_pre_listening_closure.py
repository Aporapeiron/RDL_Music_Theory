"""Pre-listening closure summary for the C6 / Am7 Music v0.2 loop.

This gathers the existing C6 / Am7 manifests and writes a compact closure
manifest. The closure separates what can be returned to Music Core before human
listening from what must remain pending until actual listening observations are
recorded.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INPUT_MANIFESTS = [
    "artifacts/json/music_v02_c6_am7_rehearing_observation.json",
    "artifacts/json/music_v02_c6_am7_intervention_separation.json",
    "artifacts/json/music_v02_c6_am7_relation_weight_probe.json",
    "artifacts/json/music_v02_c6_am7_temporal_context_probe.json",
    "artifacts/json/music_v02_c6_am7_temporal_context_order_split.json",
]
OUTPUT_MANIFEST = "artifacts/json/music_v02_c6_am7_pre_listening_closure.json"


def load_manifest(relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    return json.loads(path.read_text(encoding="utf-8"))


def collect_actual_slots(manifests: list[dict[str, Any]]) -> list[dict[str, Any]]:
    slots: list[dict[str, Any]] = []
    for manifest in manifests:
        subject = manifest.get("subject", "unknown_subject")
        if "actual_listening_observation" in manifest:
            slots.append(
                {
                    "subject": subject,
                    "path": "actual_listening_observation",
                    "value": manifest["actual_listening_observation"],
                }
            )
        for key in ("cases", "states", "phrases", "single_phrase_files", "order_variants"):
            for index, item in enumerate(manifest.get(key, [])):
                if isinstance(item, dict) and "actual_listening_observation" in item:
                    slots.append(
                        {
                            "subject": subject,
                            "path": f"{key}[{index}].actual_listening_observation",
                            "name": item.get("name"),
                            "value": item["actual_listening_observation"],
                        }
                    )
    return slots


def main() -> None:
    manifests = [load_manifest(path) for path in INPUT_MANIFESTS]
    actual_slots = collect_actual_slots(manifests)
    assert actual_slots, "expected actual listening slots"
    assert all(slot["value"] is None for slot in actual_slots)

    closure = {
        "schema": "rdl_music_v02_c6_am7_pre_listening_closure_v0_1",
        "subject": "C6_Am7_pre_listening_closure",
        "source_manifests": INPUT_MANIFESTS,
        "actual_listening_slots": actual_slots,
        "returnable_to_music_core_before_listening": [
            "pitch_class_set_preservation_does_not_preserve_harmonic_state",
            "bass_relation_can_rebase_the_same_material_toward_Am7",
            "register_gravity_depends_on_which_pitch_receives_low_support",
            "context_must_be_distinguished_as_score_fixture_and_temporal_audio_relation",
            "identical_target_sonority_can_have_different_candidate_states_under_different_temporal_frames",
            "presentation_order_memory_is_a_separate_listening_condition_from_phrase_internal_context",
        ],
        "pending_until_actual_listening": [
            "whether_listener_hears_C6_or_Am7_in_each_fixture",
            "whether_pivot_reinterpretation_occurs_at_target_or_after_following_chord",
            "whether_order_variants_change perceived candidate strength",
            "whether_structural_prediction_discrepancies_are_absorbed_by_current_M_B_or_remain_as_H",
            "whether_any_residual_relation_after_finite_B_should_be_held_as_xi",
        ],
        "not_returned_as_core_claims": [
            "relation_weight_numbers_as_universal_constants",
            "candidate_classification_as_final_chord_truth",
            "device_audio_generation_as_human_listening_confirmation",
            "C6_Am7_problem_as_resolved_binary_label_choice",
        ],
        "next_music_target_after_listening_or_deferral": "melody_meter_identity_preservation_probe",
        "manifest_path": OUTPUT_MANIFEST,
    }

    output_path = ROOT / OUTPUT_MANIFEST
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(closure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("music_v02_c6_am7_pre_listening_closure_observed")
    print(f"source_manifest_count={len(INPUT_MANIFESTS)}")
    print(f"actual_listening_slot_count={len(actual_slots)}")
    print("all_actual_listening_slots_null=True")
    for claim in closure["returnable_to_music_core_before_listening"]:
        print(f"returnable={claim}")
    print(f"manifest_file={output_path.name}")


if __name__ == "__main__":
    main()