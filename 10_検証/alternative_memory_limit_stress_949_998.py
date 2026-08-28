"""alternative memoryの保持制限を削除へ変換しない最小検証。"""

from dataclasses import dataclass

from selection_record_update_alternative_memory_899_948 import (
    SelectionUpdateMemoryBundle,
    observe_selection_record_update_alternative_memory,
)


@dataclass(frozen=True)
class AlternativeMemoryLimitStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ExpandedAlternativeMemoryEntry:
    label: str
    source_role: str
    priority_reason: str
    retention_weight: float
    retained_for: tuple[str, ...]
    compressed: bool
    deleted: bool
    status: str


@dataclass(frozen=True)
class AlternativeMemoryLimitPolicy:
    max_active_entries: int
    active_selection_rule: str
    overflow_handling: str
    preserves_inactive_memory: bool
    permits_reactivation: bool
    deletes_overflow: bool
    asserts_final_ranking: bool
    status: str


@dataclass(frozen=True)
class AlternativeMemoryLimitBundle:
    source_bundle: SelectionUpdateMemoryBundle
    expanded_memory: tuple[ExpandedAlternativeMemoryEntry, ...]
    active_memory: tuple[ExpandedAlternativeMemoryEntry, ...]
    compressed_memory: tuple[ExpandedAlternativeMemoryEntry, ...]
    policy: AlternativeMemoryLimitPolicy
    stop_lines: tuple[str, ...]
    generated_resolution: bool
    generated_deletion: bool
    status: str


@dataclass(frozen=True)
class AlternativeMemoryLimitObservation:
    source_status: str
    steps: tuple[AlternativeMemoryLimitStep, ...]
    bundle: AlternativeMemoryLimitBundle
    limit_is_not_deletion: bool
    compression_preserves_reactivation: bool
    active_memory_bounded: bool
    inactive_memory_retained: bool
    ranking_not_final_truth: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (949, "source_reentry", "reuse_899_948_update_memory_bundle", "update_memory_bundle_preserved"),
    (950, "source_reentry", "next_xi_received", "alternative_memory_limit_stress_received"),
    (951, "source_reentry", "alternative_memory_recheck", "alternative_memory_available"),
    (952, "pressure_setup", "memory_expansion_request", "expanded_alternative_memory_candidate"),
    (953, "pressure_setup", "future_context_variant_memory", "future_context_variant_memory_added"),
    (954, "pressure_setup", "B_shift_variant_memory", "B_shift_variant_memory_added"),
    (955, "pressure_setup", "policy_comparison_variant_memory", "policy_comparison_variant_memory_added"),
    (956, "pressure_setup", "memory_pressure_observation", "memory_pressure_observed"),
    (957, "limit_request", "limit_policy_request", "alternative_memory_limit_policy_candidate"),
    (958, "limit_request", "limit_not_deletion_guard", "limit_deletion_non_identity"),
    (959, "limit_request", "limit_not_truth_guard", "limit_truth_non_identity"),
    (960, "limit_request", "limit_not_final_ranking_guard", "final_ranking_blocked"),
    (961, "policy_layer", "max_active_entries_record", "max_active_entries_recorded"),
    (962, "policy_layer", "active_selection_rule_record", "active_selection_rule_recorded"),
    (963, "policy_layer", "overflow_handling_record", "overflow_handling_recorded"),
    (964, "policy_layer", "inactive_memory_preservation_record", "inactive_memory_preservation_recorded"),
    (965, "policy_layer", "reactivation_permission_record", "reactivation_permission_recorded"),
    (966, "policy_layer", "delete_overflow_false_record", "delete_overflow_false_recorded"),
    (967, "policy_layer", "final_ranking_false_record", "final_ranking_false_recorded"),
    (968, "bounded_view", "active_memory_view_creation", "active_memory_view_created"),
    (969, "bounded_view", "active_memory_count_check", "active_memory_count_bounded"),
    (970, "bounded_view", "active_memory_reason_check", "active_memory_reason_recorded"),
    (971, "compressed_view", "compressed_memory_view_creation", "compressed_memory_view_created"),
    (972, "compressed_view", "compressed_memory_keeps_label", "compressed_memory_label_preserved"),
    (973, "compressed_view", "compressed_memory_keeps_reactivation_target", "compressed_memory_reactivation_preserved"),
    (974, "compressed_view", "compressed_memory_not_error_guard", "compressed_memory_error_non_identity"),
    (975, "compressed_view", "compressed_memory_not_deleted_guard", "compressed_memory_deletion_blocked"),
    (976, "bundle", "limit_bundle_creation", "limit_bundle_created"),
    (977, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (978, "bundle", "stop_lines_carry", "limit_stop_lines_carried"),
    (979, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (980, "bundle", "generated_deletion_false", "generated_deletion_false_recorded"),
    (981, "integrity", "limit_deletion_split_check", "limit_deletion_split_confirmed"),
    (982, "integrity", "compression_reactivation_check", "compression_reactivation_confirmed"),
    (983, "integrity", "bounded_active_check", "bounded_active_confirmed"),
    (984, "integrity", "inactive_retention_check", "inactive_retention_confirmed"),
    (985, "integrity", "ranking_truth_split_check", "ranking_truth_split_confirmed"),
    (986, "non_identity", "limit_vs_deletion_split", "limit_deletion_non_identity_preserved"),
    (987, "non_identity", "compression_vs_rejection_split", "compression_rejection_non_identity"),
    (988, "non_identity", "priority_vs_truth_split", "priority_truth_non_identity"),
    (989, "non_identity", "active_view_vs_memory_total_split", "active_view_memory_total_non_identity"),
    (990, "music_subject", "memory_pressure_as_musical_density", "memory_pressure_music_subject_preserved"),
    (991, "music_subject", "low_priority_as_latent_reading", "low_priority_latent_reading_preserved"),
    (992, "music_subject", "future_reentry_route", "future_reentry_route_preserved"),
    (993, "summary", "limit_policy_summary", "limit_policy_observed"),
    (994, "summary", "compression_summary", "compression_observed"),
    (995, "summary", "no_deletion_summary", "no_deletion_confirmed"),
    (996, "summary", "no_truth_summary", "no_truth_confirmed"),
    (997, "next_plan", "memory_reactivation_priority_next_candidate", "memory_reactivation_priority_next_candidate"),
    (998, "next_plan", "next_xi_selection", "xi_memory_reactivation_priority_stress"),
)


def _build_steps() -> tuple[AlternativeMemoryLimitStep, ...]:
    previous = "selection_record_update_alternative_memory_899_948"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            AlternativeMemoryLimitStep(
                number=number,
                phase=phase,
                name=name,
                source=previous,
                result=result,
                generated_mutation=False,
            )
        )
        previous = result
    return tuple(steps)


def _expanded_memory(source: SelectionUpdateMemoryBundle) -> tuple[ExpandedAlternativeMemoryEntry, ...]:
    base_label = source.alternative_memory[0].label
    return (
        ExpandedAlternativeMemoryEntry(
            label=base_label,
            source_role="source_retained_alternative",
            priority_reason="directly_retained_from_selection_update",
            retention_weight=0.91,
            retained_for=source.alternative_memory[0].retained_for,
            compressed=False,
            deleted=False,
            status="active_memory_retained",
        ),
        ExpandedAlternativeMemoryEntry(
            label="C major continuation frame under delayed cadence",
            source_role="future_context_variant",
            priority_reason="future_context_shift",
            retention_weight=0.63,
            retained_for=("future_context_shift",),
            compressed=False,
            deleted=False,
            status="active_memory_retained",
        ),
        ExpandedAlternativeMemoryEntry(
            label="C major continuation frame under altered B",
            source_role="B_shift_variant",
            priority_reason="B_shift_reentry",
            retention_weight=0.47,
            retained_for=("B_shift_reentry",),
            compressed=True,
            deleted=False,
            status="compressed_memory_retained",
        ),
        ExpandedAlternativeMemoryEntry(
            label="C major continuation frame for policy audit",
            source_role="policy_comparison_variant",
            priority_reason="policy_comparison",
            retention_weight=0.36,
            retained_for=("policy_comparison",),
            compressed=True,
            deleted=False,
            status="compressed_memory_retained",
        ),
    )


def build_alternative_memory_limit_bundle(
    source: SelectionUpdateMemoryBundle,
) -> AlternativeMemoryLimitBundle:
    expanded = _expanded_memory(source)
    policy = AlternativeMemoryLimitPolicy(
        max_active_entries=2,
        active_selection_rule="highest_retention_weight_with_music_reason",
        overflow_handling="compress_to_latent_reactivation_memory",
        preserves_inactive_memory=True,
        permits_reactivation=True,
        deletes_overflow=False,
        asserts_final_ranking=False,
        status="alternative_memory_limit_policy_recorded_without_deletion",
    )
    active = tuple(entry for entry in expanded if not entry.compressed)
    compressed = tuple(entry for entry in expanded if entry.compressed)
    return AlternativeMemoryLimitBundle(
        source_bundle=source,
        expanded_memory=expanded,
        active_memory=active,
        compressed_memory=compressed,
        policy=policy,
        stop_lines=(
            "limit_not_deletion",
            "compression_not_rejection",
            "priority_not_truth",
            "active_view_not_total_memory",
            "inactive_memory_reactivation_preserved",
        ),
        generated_resolution=False,
        generated_deletion=False,
        status="alternative_memory_limit_bundle_949_998_built_without_deleting_overflow_memory",
    )


def observe_alternative_memory_limit() -> AlternativeMemoryLimitObservation:
    source = observe_selection_record_update_alternative_memory()
    bundle = build_alternative_memory_limit_bundle(source.bundle)
    steps = _build_steps()

    return AlternativeMemoryLimitObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        limit_is_not_deletion=(
            bundle.policy.deletes_overflow is False
            and bundle.generated_deletion is False
            and all(entry.deleted is False for entry in bundle.expanded_memory)
        ),
        compression_preserves_reactivation=(
            bundle.policy.permits_reactivation is True
            and all(entry.retained_for for entry in bundle.compressed_memory)
        ),
        active_memory_bounded=len(bundle.active_memory) <= bundle.policy.max_active_entries,
        inactive_memory_retained=(
            len(bundle.compressed_memory) == 2
            and bundle.policy.preserves_inactive_memory is True
        ),
        ranking_not_final_truth=bundle.policy.asserts_final_ranking is False,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="alternative_memory_limit_949_998_observed_without_deleting_or_finalizing_memory",
    )


def run_checks() -> None:
    observation = observe_alternative_memory_limit()
    bundle = observation.bundle

    assert observation.source_status == (
        "selection_record_update_alternative_memory_899_948_observed_without_erasing_memory_or_history"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 949
    assert observation.steps[-1].number == 998
    assert len(bundle.expanded_memory) == 4
    assert len(bundle.active_memory) == 2
    assert len(bundle.compressed_memory) == 2
    assert observation.limit_is_not_deletion is True
    assert observation.compression_preserves_reactivation is True
    assert observation.active_memory_bounded is True
    assert observation.inactive_memory_retained is True
    assert observation.ranking_not_final_truth is True
    assert bundle.generated_resolution is False
    assert bundle.generated_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_memory_reactivation_priority_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_alternative_memory_limit().status)
