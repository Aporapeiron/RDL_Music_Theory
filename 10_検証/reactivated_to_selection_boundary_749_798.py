"""reactivated候補をselection境界へ戻す最小検証。"""

from dataclasses import dataclass

from candidate_lifecycle_map_699_748 import (
    CandidateLifecycleEntry,
    observe_candidate_lifecycle_map,
)
from prediction_resolution_policy_stress_399_448 import (
    PolicyCriterion,
    PredictionResolutionPolicy,
)


@dataclass(frozen=True)
class ReactivatedSelectionStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ReactivatedSelectionRequest:
    candidate_label: str
    source_state: str
    request_reason: str
    source_lifecycle_status: str
    generated_candidate: bool


@dataclass(frozen=True)
class ReactivatedSelectionReadiness:
    request: ReactivatedSelectionRequest
    policy: PredictionResolutionPolicy
    eligible: bool
    selected: bool
    retained_alternatives: tuple[str, ...]
    status: str
    generated_selection: bool
    deleted_alternatives: bool


@dataclass(frozen=True)
class ReactivatedToSelectionBoundaryObservation:
    source_status: str
    steps: tuple[ReactivatedSelectionStep, ...]
    request: ReactivatedSelectionRequest
    readiness: ReactivatedSelectionReadiness
    reactivated_candidate_found: bool
    request_created_from_lifecycle: bool
    reactivated_is_selected: bool
    selection_requires_policy: bool
    alternatives_retained: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (749, "source_reentry", "reuse_699_748_lifecycle_map", "candidate_lifecycle_map_preserved"),
    (750, "source_reentry", "next_xi_received", "reactivated_to_selection_boundary_stress_received"),
    (751, "source_reentry", "reactivated_state_recheck", "reactivated_candidate_available"),
    (752, "selection_request", "reactivated_selection_request", "reactivated_selection_request_candidate"),
    (753, "selection_request", "request_not_selection_guard", "request_selection_non_identity"),
    (754, "selection_request", "request_not_generation_guard", "request_generation_blocked"),
    (755, "selection_request", "request_not_truth_guard", "request_truth_non_identity"),
    (756, "selection_request", "request_source_lifecycle_trace", "request_source_lifecycle_trace_recorded"),
    (757, "eligibility", "reactivated_state_eligibility", "reactivated_state_eligible_for_selection_boundary"),
    (758, "eligibility", "candidate_retention_eligibility", "retained_candidate_eligible_for_selection_boundary"),
    (759, "eligibility", "lifecycle_status_eligibility", "lifecycle_status_eligibility_recorded"),
    (760, "eligibility", "eligibility_not_selection_guard", "eligibility_selection_non_identity"),
    (761, "eligibility", "eligibility_not_truth_guard", "eligibility_truth_non_identity"),
    (762, "policy_boundary", "selection_policy_request", "selection_policy_required"),
    (763, "policy_boundary", "reactivation_policy_fixture", "reactivation_policy_fixture_recorded"),
    (764, "policy_boundary", "policy_not_candidate_generator_guard", "policy_candidate_generation_blocked"),
    (765, "policy_boundary", "policy_not_lifecycle_mutation_guard", "policy_lifecycle_mutation_blocked"),
    (766, "readiness", "readiness_record_creation", "selection_readiness_record_created"),
    (767, "readiness", "eligible_true_record", "eligible_true_recorded"),
    (768, "readiness", "selected_false_record", "selected_false_recorded"),
    (769, "readiness", "retained_alternatives_record", "retained_alternatives_recorded"),
    (770, "readiness", "generated_selection_false_record", "generated_selection_false_recorded"),
    (771, "readiness", "deleted_alternatives_false_record", "deleted_alternatives_false_recorded"),
    (772, "boundary_stop", "reactivated_not_selected_stop", "reactivated_selected_stop_recorded"),
    (773, "boundary_stop", "request_not_selection_stop", "request_selection_stop_recorded"),
    (774, "boundary_stop", "eligible_not_selected_stop", "eligible_selected_stop_recorded"),
    (775, "boundary_stop", "selection_requires_controller_stop", "selection_controller_stop_recorded"),
    (776, "boundary_stop", "reactivated_not_true_stop", "reactivated_truth_stop_recorded"),
    (777, "alternative_retention", "continuation_alternative_retained", "continuation_alternative_retained"),
    (778, "alternative_retention", "reactivated_candidate_retained", "reactivated_candidate_retained"),
    (779, "alternative_retention", "no_candidate_deletion", "candidate_deletion_blocked"),
    (780, "alternative_retention", "alternative_not_error_guard", "alternative_error_non_identity"),
    (781, "record_schema", "selection_request_schema", "selection_request_schema_observed"),
    (782, "record_schema", "selection_readiness_schema", "selection_readiness_schema_observed"),
    (783, "record_schema", "policy_trace_field", "policy_trace_field_recorded"),
    (784, "record_schema", "lifecycle_trace_field", "lifecycle_trace_field_recorded"),
    (785, "non_identity", "reactivation_vs_selection_request_split", "reactivation_request_non_identity"),
    (786, "non_identity", "selection_request_vs_selection_split", "request_selection_split_preserved"),
    (787, "non_identity", "selection_readiness_vs_selection_split", "readiness_selection_split_preserved"),
    (788, "non_identity", "selection_boundary_vs_truth_split", "selection_truth_split_preserved"),
    (789, "music_subject", "returning_interpretation_to_choice", "returning_interpretation_choice_preserved"),
    (790, "music_subject", "delayed_choice_without_erasure", "delayed_choice_without_erasure_preserved"),
    (791, "music_subject", "music_context_memory", "music_context_memory_preserved"),
    (792, "summary", "reactivated_selection_boundary_summary", "reactivated_selection_boundary_observed"),
    (793, "summary", "policy_required_summary", "policy_required_for_selection"),
    (794, "summary", "alternatives_retained_summary", "alternatives_retained"),
    (795, "summary", "no_mutation_summary", "no_mutation_generated"),
    (796, "next_plan", "selection_controller_next_candidate", "selection_controller_next_candidate"),
    (797, "next_plan", "post_selection_lifecycle_open_xi", "post_selection_lifecycle_left_open"),
    (798, "next_plan", "next_xi_selection", "xi_selection_controller_after_reactivation_stress"),
)


def _build_steps() -> tuple[ReactivatedSelectionStep, ...]:
    previous = "candidate_lifecycle_map_699_748"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            ReactivatedSelectionStep(
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


def _reactivated_entry(entries: tuple[CandidateLifecycleEntry, ...]) -> CandidateLifecycleEntry:
    for entry in entries:
        if "reactivated" in entry.states:
            return entry
    raise ValueError("no reactivated candidate in lifecycle map")


def fixture_reactivation_selection_policy() -> PredictionResolutionPolicy:
    return PredictionResolutionPolicy(
        name="reactivated_candidate_selection_readiness_policy",
        criteria=(
            PolicyCriterion(
                name="requires_reactivated_state",
                preferred_value="reactivated",
                source="external_selection_readiness_fixture",
            ),
            PolicyCriterion(
                name="requires_controller",
                preferred_value="selection_controller_pending",
                source="external_selection_readiness_fixture",
            ),
        ),
        generated_candidates=False,
    )


def build_selection_request(
    entry: CandidateLifecycleEntry,
) -> ReactivatedSelectionRequest:
    return ReactivatedSelectionRequest(
        candidate_label=entry.label,
        source_state="reactivated",
        request_reason="reactivated_candidate_can_reenter_selection_boundary",
        source_lifecycle_status=entry.status,
        generated_candidate=False,
    )


def observe_reactivated_to_selection_boundary() -> ReactivatedToSelectionBoundaryObservation:
    source = observe_candidate_lifecycle_map()
    entry = _reactivated_entry(source.lifecycle_map.entries)
    request = build_selection_request(entry)
    policy = fixture_reactivation_selection_policy()
    alternatives = tuple(
        candidate.label
        for candidate in source.lifecycle_map.entries
        if candidate.label != request.candidate_label
    )
    readiness = ReactivatedSelectionReadiness(
        request=request,
        policy=policy,
        eligible=True,
        selected=False,
        retained_alternatives=alternatives,
        status="reactivated_candidate_ready_for_selection_controller",
        generated_selection=False,
        deleted_alternatives=False,
    )
    steps = _build_steps()

    return ReactivatedToSelectionBoundaryObservation(
        source_status=source.status,
        steps=steps,
        request=request,
        readiness=readiness,
        reactivated_candidate_found=True,
        request_created_from_lifecycle=(
            request.source_lifecycle_status
            == "lifecycle_recorded_without_final_resolution"
        ),
        reactivated_is_selected=readiness.selected,
        selection_requires_policy=(
            policy.name == "reactivated_candidate_selection_readiness_policy"
            and readiness.generated_selection is False
        ),
        alternatives_retained=(
            readiness.retained_alternatives == ("C major continuation frame",)
            and readiness.deleted_alternatives is False
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="reactivated_to_selection_boundary_749_798_observed_without_treating_reactivation_as_selection",
    )


def run_checks() -> None:
    observation = observe_reactivated_to_selection_boundary()

    assert observation.source_status == (
        "candidate_lifecycle_map_699_748_observed_without_finalizing_candidate_states"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 749
    assert observation.steps[-1].number == 798
    assert observation.reactivated_candidate_found is True
    assert observation.request.candidate_label == "A minor reinterpretation frame"
    assert observation.request.generated_candidate is False
    assert observation.request_created_from_lifecycle is True
    assert observation.readiness.eligible is True
    assert observation.reactivated_is_selected is False
    assert observation.selection_requires_policy is True
    assert observation.alternatives_retained is True
    assert observation.readiness.generated_selection is False
    assert observation.readiness.deleted_alternatives is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_selection_controller_after_reactivation_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_reactivated_to_selection_boundary().status)
