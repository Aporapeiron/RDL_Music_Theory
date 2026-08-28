"""compressed latent memoryの再活性化優先度を検査する最小実験。"""

from dataclasses import dataclass

from alternative_memory_limit_stress_949_998 import (
    AlternativeMemoryLimitBundle,
    ExpandedAlternativeMemoryEntry,
    observe_alternative_memory_limit,
)


@dataclass(frozen=True)
class MemoryReactivationPriorityStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ReactivationTrigger:
    name: str
    trigger_source: str
    raises_priority_for: str
    musical_reason: str
    asserts_repetition: bool
    asserts_truth: bool
    status: str


@dataclass(frozen=True)
class ReactivationPriorityEvaluation:
    label: str
    previous_memory_state: str
    new_memory_state: str
    trigger: ReactivationTrigger
    priority_delta: float
    reactivation_score: float
    returns_to_active_view: bool
    reinterpreted: bool
    selected: bool
    deleted: bool
    status: str


@dataclass(frozen=True)
class MemoryReactivationPriorityBundle:
    source_bundle: AlternativeMemoryLimitBundle
    trigger: ReactivationTrigger
    evaluations: tuple[ReactivationPriorityEvaluation, ...]
    promoted_memory: tuple[ReactivationPriorityEvaluation, ...]
    remaining_latent_memory: tuple[ReactivationPriorityEvaluation, ...]
    stop_lines: tuple[str, ...]
    generated_selection: bool
    generated_repetition_identity: bool
    generated_deletion: bool
    status: str


@dataclass(frozen=True)
class MemoryReactivationPriorityObservation:
    source_status: str
    steps: tuple[MemoryReactivationPriorityStep, ...]
    bundle: MemoryReactivationPriorityBundle
    compressed_memory_was_reconsidered: bool
    reactivation_is_not_selection: bool
    refrain_is_not_repetition: bool
    reactivation_preserves_reinterpretation: bool
    latent_remainder_preserved: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (999, "source_reentry", "reuse_949_998_memory_limit_bundle", "memory_limit_bundle_preserved"),
    (1000, "source_reentry", "next_xi_received", "memory_reactivation_priority_stress_received"),
    (1001, "source_reentry", "compressed_memory_recheck", "compressed_memory_available"),
    (1002, "trigger_setup", "context_shift_trigger_request", "context_shift_trigger_candidate"),
    (1003, "trigger_setup", "B_shift_trigger_request", "B_shift_trigger_candidate"),
    (1004, "trigger_setup", "cadential_return_trigger_request", "cadential_return_trigger_candidate"),
    (1005, "trigger_setup", "trigger_music_reason_record", "trigger_music_reason_recorded"),
    (1006, "trigger_guard", "trigger_not_truth_guard", "trigger_truth_non_identity"),
    (1007, "trigger_guard", "trigger_not_repetition_guard", "trigger_repetition_non_identity"),
    (1008, "trigger_guard", "trigger_not_selection_guard", "trigger_selection_non_identity"),
    (1009, "priority_request", "reactivation_priority_request", "reactivation_priority_candidate"),
    (1010, "priority_request", "priority_delta_request", "priority_delta_candidate"),
    (1011, "priority_request", "compressed_memory_evaluation_request", "compressed_memory_evaluation_candidate"),
    (1012, "evaluation_layer", "altered_B_memory_evaluation", "altered_B_memory_evaluated"),
    (1013, "evaluation_layer", "policy_audit_memory_evaluation", "policy_audit_memory_evaluated"),
    (1014, "evaluation_layer", "priority_score_record", "priority_score_recorded"),
    (1015, "evaluation_layer", "reactivation_target_record", "reactivation_target_recorded"),
    (1016, "evaluation_layer", "reinterpretation_flag_record", "reinterpretation_flag_recorded"),
    (1017, "evaluation_layer", "selection_false_record", "selection_false_recorded"),
    (1018, "evaluation_layer", "deletion_false_record", "deletion_false_recorded"),
    (1019, "promotion_view", "promoted_memory_view_creation", "promoted_memory_view_created"),
    (1020, "promotion_view", "active_return_without_selection", "active_return_without_selection_recorded"),
    (1021, "promotion_view", "refrain_return_check", "refrain_return_observed"),
    (1022, "promotion_view", "refrain_not_repetition_check", "refrain_repetition_split_confirmed"),
    (1023, "latent_remainder", "remaining_latent_memory_view", "remaining_latent_memory_preserved"),
    (1024, "latent_remainder", "latent_remainder_not_rejection", "latent_remainder_rejection_non_identity"),
    (1025, "latent_remainder", "latent_remainder_not_deletion", "latent_remainder_deletion_blocked"),
    (1026, "bundle", "reactivation_priority_bundle_creation", "reactivation_priority_bundle_created"),
    (1027, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1028, "bundle", "stop_lines_carry", "reactivation_stop_lines_carried"),
    (1029, "bundle", "generated_selection_false", "generated_selection_false_recorded"),
    (1030, "bundle", "generated_repetition_identity_false", "generated_repetition_identity_false_recorded"),
    (1031, "bundle", "generated_deletion_false", "generated_deletion_false_recorded"),
    (1032, "integrity", "compressed_reconsideration_check", "compressed_reconsideration_confirmed"),
    (1033, "integrity", "reactivation_selection_split_check", "reactivation_selection_split_confirmed"),
    (1034, "integrity", "refrain_repetition_split_check", "refrain_repetition_split_confirmed"),
    (1035, "integrity", "reinterpretation_preservation_check", "reinterpretation_preserved"),
    (1036, "integrity", "latent_remainder_check", "latent_remainder_confirmed"),
    (1037, "non_identity", "reactivation_vs_selection_split", "reactivation_selection_non_identity"),
    (1038, "non_identity", "refrain_vs_repetition_split", "refrain_repetition_non_identity"),
    (1039, "non_identity", "priority_vs_truth_split", "priority_truth_non_identity"),
    (1040, "non_identity", "promotion_vs_deletion_split", "promotion_deletion_non_identity"),
    (1041, "music_subject", "return_as_refrain", "return_as_refrain_preserved"),
    (1042, "music_subject", "latent_memory_as_heard_absence", "heard_absence_preserved"),
    (1043, "music_subject", "contextual_return_difference", "contextual_return_difference_preserved"),
    (1044, "summary", "reactivation_priority_summary", "reactivation_priority_observed"),
    (1045, "summary", "refrain_non_repetition_summary", "refrain_non_repetition_confirmed"),
    (1046, "summary", "no_selection_no_deletion_summary", "no_selection_no_deletion_confirmed"),
    (1047, "next_plan", "refrain_identity_boundary_next_candidate", "refrain_identity_boundary_next_candidate"),
    (1048, "next_plan", "next_xi_selection", "xi_refrain_identity_boundary_stress"),
)


def _build_steps() -> tuple[MemoryReactivationPriorityStep, ...]:
    previous = "alternative_memory_limit_949_998"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            MemoryReactivationPriorityStep(
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


def _target_compressed_entries(
    bundle: AlternativeMemoryLimitBundle,
) -> tuple[ExpandedAlternativeMemoryEntry, ExpandedAlternativeMemoryEntry]:
    return bundle.compressed_memory[0], bundle.compressed_memory[1]


def build_memory_reactivation_priority_bundle(
    source: AlternativeMemoryLimitBundle,
) -> MemoryReactivationPriorityBundle:
    altered_b, policy_audit = _target_compressed_entries(source)
    trigger = ReactivationTrigger(
        name="altered_B_with_cadential_return",
        trigger_source="B_shift_reentry_and_cadential_context",
        raises_priority_for=altered_b.label,
        musical_reason="previously_latent_reading_now_matches_returning_harmonic_context",
        asserts_repetition=False,
        asserts_truth=False,
        status="reactivation_trigger_recorded_without_truth_or_repetition_identity",
    )
    evaluations = (
        ReactivationPriorityEvaluation(
            label=altered_b.label,
            previous_memory_state="compressed_latent_memory",
            new_memory_state="reactivation_priority_candidate",
            trigger=trigger,
            priority_delta=0.35,
            reactivation_score=altered_b.retention_weight + 0.35,
            returns_to_active_view=True,
            reinterpreted=True,
            selected=False,
            deleted=False,
            status="compressed_memory_promoted_to_active_view_candidate",
        ),
        ReactivationPriorityEvaluation(
            label=policy_audit.label,
            previous_memory_state="compressed_latent_memory",
            new_memory_state="latent_memory_retained",
            trigger=trigger,
            priority_delta=0.05,
            reactivation_score=policy_audit.retention_weight + 0.05,
            returns_to_active_view=False,
            reinterpreted=False,
            selected=False,
            deleted=False,
            status="compressed_memory_remains_latent_reactivation_memory",
        ),
    )
    promoted = tuple(item for item in evaluations if item.returns_to_active_view)
    remaining = tuple(item for item in evaluations if not item.returns_to_active_view)
    return MemoryReactivationPriorityBundle(
        source_bundle=source,
        trigger=trigger,
        evaluations=evaluations,
        promoted_memory=promoted,
        remaining_latent_memory=remaining,
        stop_lines=(
            "reactivation_not_selection",
            "refrain_not_repetition",
            "priority_not_truth",
            "promotion_not_deletion",
            "latent_remainder_not_rejection",
        ),
        generated_selection=False,
        generated_repetition_identity=False,
        generated_deletion=False,
        status="memory_reactivation_priority_bundle_999_1048_built_without_selection_or_repetition_identity",
    )


def observe_memory_reactivation_priority() -> MemoryReactivationPriorityObservation:
    source = observe_alternative_memory_limit()
    bundle = build_memory_reactivation_priority_bundle(source.bundle)
    steps = _build_steps()

    return MemoryReactivationPriorityObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        compressed_memory_was_reconsidered=len(bundle.evaluations) == 2,
        reactivation_is_not_selection=(
            bundle.generated_selection is False
            and all(item.selected is False for item in bundle.evaluations)
        ),
        refrain_is_not_repetition=(
            bundle.generated_repetition_identity is False
            and bundle.trigger.asserts_repetition is False
        ),
        reactivation_preserves_reinterpretation=(
            len(bundle.promoted_memory) == 1
            and bundle.promoted_memory[0].reinterpreted is True
        ),
        latent_remainder_preserved=(
            len(bundle.remaining_latent_memory) == 1
            and bundle.remaining_latent_memory[0].deleted is False
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="memory_reactivation_priority_999_1048_observed_without_selection_or_repetition_collapse",
    )


def run_checks() -> None:
    observation = observe_memory_reactivation_priority()
    bundle = observation.bundle

    assert observation.source_status == (
        "alternative_memory_limit_949_998_observed_without_deleting_or_finalizing_memory"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 999
    assert observation.steps[-1].number == 1048
    assert len(bundle.evaluations) == 2
    assert len(bundle.promoted_memory) == 1
    assert len(bundle.remaining_latent_memory) == 1
    assert observation.compressed_memory_was_reconsidered is True
    assert observation.reactivation_is_not_selection is True
    assert observation.refrain_is_not_repetition is True
    assert observation.reactivation_preserves_reinterpretation is True
    assert observation.latent_remainder_preserved is True
    assert bundle.generated_selection is False
    assert bundle.generated_repetition_identity is False
    assert bundle.generated_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_refrain_identity_boundary_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_memory_reactivation_priority().status)
