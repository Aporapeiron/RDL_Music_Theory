"""Pre-listening closure summary for the melody-meter motif memory loop.

This gathers the motif memory probe manifest and writes a compact closure
manifest. The closure separates device-side structural claims from claims that
must remain pending until actual listening observations are recorded.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INPUT_MANIFESTS = [
    "artifacts/json/music_v02_melody_meter_motif_memory_probe.json",
]
OUTPUT_MANIFEST = "artifacts/json/music_v02_melody_meter_motif_memory_pre_listening_closure.json"


def load_manifest(relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    return json.loads(path.read_text(encoding="utf-8"))


def collect_actual_slots(manifests: list[dict[str, Any]]) -> list[dict[str, Any]]:
    slots: list[dict[str, Any]] = []
    for manifest in manifests:
        subject = manifest.get("subject", "unknown_subject")
        for key in ("frames", "cases", "states", "phrases"):
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

    motif_manifest = manifests[0]
    frames = motif_manifest["frames"]
    names = {frame["name"] for frame in frames}
    assert "delayed_return_after_filler" in names
    assert "delayed_return_after_silence" in names

    filler = next(frame for frame in frames if frame["name"] == "delayed_return_after_filler")
    silence = next(frame for frame in frames if frame["name"] == "delayed_return_after_silence")
    assert filler["return_motif_start_beat"] == silence["return_motif_start_beat"]
    assert filler["return_gap_beats"] == silence["return_gap_beats"]
    assert filler["return_phase"] == silence["return_phase"]
    assert filler["intervening_duration_beats"] != silence["intervening_duration_beats"]

    closure = {
        "schema": "rdl_music_v02_melody_meter_motif_memory_pre_listening_closure_v0_1",
        "subject": "melody_meter_motif_memory_pre_listening_closure",
        "source_manifests": INPUT_MANIFESTS,
        "actual_listening_slots": actual_slots,
        "returnable_to_music_core_before_listening": [
            "same_motif_material_does_not_preserve_motif_memory_candidate_state",
            "return_start_time_derives_return_gap_and_return_phase_under_fixed_meter",
            "absence_interval_is_not_identical_to_sounding_intervening_material",
            "melodic_material_silence_is_not_total_acoustic_silence_when_meter_reference_continues",
            "intervening_material_identity_can_change_while_return_start_gap_and_phase_are_held",
            "motif_memory_fixture_extends_local_timing_relations_to_mid_range_absence_retention_return",
        ],
        "pending_until_actual_listening": [
            "whether_direct_repetition_is_heard_as_confirmation_or_simple_echo",
            "whether_delayed_return_is_heard_as_refrain_answer_or_recollection",
            "whether_silent_gap_or_sounding_filler_better_supports_motif_retention",
            "whether_offphase_return_is_heard_as_interruption_compression_or_syncopated_return",
            "whether_contrast_before_return_increases_perceived_return_strength",
            "which_discrepancies_are_absorbed_by_current_M_B_or_remain_as_H",
            "which_unrecovered_relation_due_to_the_chosen_finite_B_is_described_as_xi_in_this_observation",
        ],
        "not_returned_as_core_claims": [
            "device_candidate_classification_as_actual_listener_memory_state",
            "melodic_material_silence_as_total_acoustic_silence",
            "return_phase_as_independent_intervention_under_fixed_meter",
            "motif_return_candidate_as_confirmed_refrain_perception",
        ],
        "next_music_target_after_listening_or_deferral": "timbre_attack_identity_probe",
        "manifest_path": OUTPUT_MANIFEST,
    }

    output_path = ROOT / OUTPUT_MANIFEST
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(closure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("music_v02_melody_meter_motif_memory_pre_listening_closure_observed")
    print(f"source_manifest_count={len(INPUT_MANIFESTS)}")
    print(f"actual_listening_slot_count={len(actual_slots)}")
    print("all_actual_listening_slots_null=True")
    for claim in closure["returnable_to_music_core_before_listening"]:
        print(f"returnable={claim}")
    print(f"manifest_file={output_path.name}")


if __name__ == "__main__":
    main()