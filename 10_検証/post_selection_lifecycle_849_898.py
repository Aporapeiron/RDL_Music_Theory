"""選択後もcandidate lifecycleを閉じないことを検査する最小実験。"""

from dataclasses import dataclass

from selection_controller_after_reactivation_799_848 import (
    ControlledSelectionRecord,
    observe_selection_controller_after_reactivation,
)


@dataclass(frozen=True)
class PostSelectionLifecycleStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class PostSelectionLifecycleRecord:
    selected_label: str
    previous_state: str
    current_state: str
    retained_alternatives: tuple[str, ...]
    controller_trace: str
    update_reason: str
    next_open_states: tuple[str, ...]
    lifecycle_closed: bool
    asserted_truth: bool
    deleted_alternatives: bool
    status: str


@dataclass(frozen=True)
class PostSelectionLifecycleObservation:
    source_status: str
    steps: tuple[PostSelectionLifecycleStep, ...]
    source_selection: ControlledSelectionRecord
    lifecycle_record: PostSelectionLifecycleRecord
    selection_record_updated: bool
    alternatives_retained: bool
    controller_trace_preserved: bool
    post_selection_keeps_open_states: bool
    lifecycle_closed: bool
    selection_asserts_truth: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (849, "source_reentry", "reuse_799_848_controlled_selection", "controlled_selection_result_preserved"),
    (850, "source_reentry", "next_xi_received", "post_selection_lifecycle_stress_received"),
    (851, "source_reentry", "selected_after_reactivation_recheck", "selected_after_reactivation_available"),
    (852, "post_selection_request", "post_selection_lifecycle_request", "post_selection_lifecycle_candidate"),
    (853, "post_selection_request", "post_selection_not_final_guard", "post_selection_finalization_blocked"),
    (854, "post_selection_request", "post_selection_not_truth_guard", "post_selection_truth_non_identity"),
    (855, "post_selection_request", "post_selection_not_deletion_guard", "post_selection_deletion_blocked"),
    (856, "record_update", "selected_label_carry", "selected_label_carried"),
    (857, "record_update", "previous_state_record", "previous_state_recorded"),
    (858, "record_update", "current_state_record", "current_state_recorded"),
    (859, "record_update", "controller_trace_carry", "controller_trace_carried"),
    (860, "record_update", "update_reason_record", "update_reason_recorded"),
    (861, "record_update", "record_update_not_mutation_guard", "source_record_mutation_blocked"),
    (862, "alternative_retention", "retained_alternatives_carry", "retained_alternatives_carried"),
    (863, "alternative_retention", "alternative_status_after_selection", "alternative_status_after_selection_recorded"),
    (864, "alternative_retention", "alternative_not_deleted_guard", "alternative_deletion_blocked"),
    (865, "alternative_retention", "alternative_not_error_guard", "alternative_error_non_identity"),
    (866, "open_states", "future_reinterpretation_open_state", "future_reinterpretation_open_state_recorded"),
    (867, "open_states", "B_shift_reentry_open_state", "B_shift_reentry_open_state_recorded"),
    (868, "open_states", "policy_shift_reentry_open_state", "policy_shift_reentry_open_state_recorded"),
    (869, "open_states", "context_shift_reentry_open_state", "context_shift_reentry_open_state_recorded"),
    (870, "open_states", "open_state_not_selection_guard", "open_state_selection_non_identity"),
    (871, "open_states", "open_state_not_generation_guard", "open_state_generation_blocked"),
    (872, "lifecycle_record", "post_selection_lifecycle_record_schema", "post_selection_lifecycle_record_schema_observed"),
    (873, "lifecycle_record", "lifecycle_closed_false_field", "lifecycle_closed_false_recorded"),
    (874, "lifecycle_record", "asserted_truth_false_field", "asserted_truth_false_recorded"),
    (875, "lifecycle_record", "deleted_alternatives_false_field", "deleted_alternatives_false_recorded"),
    (876, "lifecycle_record", "status_assignment", "post_selection_lifecycle_status_recorded"),
    (877, "non_identity", "selected_after_reactivation_vs_final_split", "selected_after_reactivation_final_non_identity"),
    (878, "non_identity", "post_selection_vs_truth_split", "post_selection_truth_split_preserved"),
    (879, "non_identity", "record_update_vs_candidate_mutation_split", "record_update_candidate_mutation_split_preserved"),
    (880, "non_identity", "alternative_retention_vs_rejection_split", "alternative_retention_rejection_split_preserved"),
    (881, "non_identity", "open_state_vs_generated_candidate_split", "open_state_generation_split_preserved"),
    (882, "music_subject", "selection_as_musical_event", "selection_as_musical_event_preserved"),
    (883, "music_subject", "post_selection_ambiguity_memory", "post_selection_ambiguity_memory_preserved"),
    (884, "music_subject", "continuation_memory_after_reinterpretation", "continuation_memory_after_reinterpretation_preserved"),
    (885, "music_subject", "future_context_sensitivity", "future_context_sensitivity_preserved"),
    (886, "summary", "post_selection_lifecycle_summary", "post_selection_lifecycle_observed"),
    (887, "summary", "alternative_retention_summary", "alternatives_retained_after_post_selection"),
    (888, "summary", "open_states_summary", "open_states_preserved"),
    (889, "summary", "no_truth_summary", "no_truth_asserted"),
    (890, "summary", "no_deletion_summary", "no_alternative_deleted"),
    (891, "summary", "no_mutation_summary", "no_mutation_generated"),
    (892, "next_plan", "selection_record_update_next_candidate", "selection_record_update_next_candidate"),
    (893, "next_plan", "alternative_memory_limit_open_xi", "alternative_memory_limit_left_open"),
    (894, "next_plan", "post_selection_reentry_open_xi", "post_selection_reentry_left_open"),
    (895, "next_plan", "Core_side_path_record", "Core_side_path_recorded_but_not_taken"),
    (896, "next_plan", "T2_candidate_limit_record", "T2_candidate_limit_recorded"),
    (897, "next_plan", "music_specific_lifecycle_continuation", "music_specific_lifecycle_continuation_recorded"),
    (898, "next_plan", "next_xi_selection", "xi_selection_record_update_and_alternative_memory_stress"),
)


def _build_steps() -> tuple[PostSelectionLifecycleStep, ...]:
    previous = "selection_controller_after_reactivation_799_848"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            PostSelectionLifecycleStep(
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


def build_post_selection_lifecycle_record(
    selection: ControlledSelectionRecord,
) -> PostSelectionLifecycleRecord:
    return PostSelectionLifecycleRecord(
        selected_label=selection.selected_label,
        previous_state="reactivated",
        current_state=selection.post_selection_state,
        retained_alternatives=selection.retained_alternatives,
        controller_trace=selection.controller.name,
        update_reason=selection.controller.selection_reason,
        next_open_states=(
            "future_reinterpretation",
            "B_shift_reentry",
            "policy_shift_reentry",
            "context_shift_reentry",
        ),
        lifecycle_closed=False,
        asserted_truth=False,
        deleted_alternatives=False,
        status="post_selection_lifecycle_849_898_recorded_without_final_resolution",
    )


def observe_post_selection_lifecycle() -> PostSelectionLifecycleObservation:
    source = observe_selection_controller_after_reactivation()
    lifecycle_record = build_post_selection_lifecycle_record(source.selection_record)
    steps = _build_steps()

    return PostSelectionLifecycleObservation(
        source_status=source.status,
        steps=steps,
        source_selection=source.selection_record,
        lifecycle_record=lifecycle_record,
        selection_record_updated=(
            lifecycle_record.selected_label == "A minor reinterpretation frame"
            and lifecycle_record.previous_state == "reactivated"
            and lifecycle_record.current_state == "selected_after_reactivation"
        ),
        alternatives_retained=(
            lifecycle_record.retained_alternatives == ("C major continuation frame",)
            and lifecycle_record.deleted_alternatives is False
        ),
        controller_trace_preserved=(
            lifecycle_record.controller_trace == "reactivated_selection_controller_fixture"
        ),
        post_selection_keeps_open_states=(
            "future_reinterpretation" in lifecycle_record.next_open_states
            and "context_shift_reentry" in lifecycle_record.next_open_states
        ),
        lifecycle_closed=lifecycle_record.lifecycle_closed,
        selection_asserts_truth=lifecycle_record.asserted_truth,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="post_selection_lifecycle_849_898_observed_without_closing_selection_history",
    )


def run_checks() -> None:
    observation = observe_post_selection_lifecycle()
    lifecycle_record = observation.lifecycle_record

    assert observation.source_status == (
        "selection_controller_after_reactivation_799_848_observed_without_closing_post_selection_lifecycle"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 849
    assert observation.steps[-1].number == 898
    assert observation.selection_record_updated is True
    assert observation.alternatives_retained is True
    assert observation.controller_trace_preserved is True
    assert observation.post_selection_keeps_open_states is True
    assert observation.lifecycle_closed is False
    assert observation.selection_asserts_truth is False
    assert lifecycle_record.deleted_alternatives is False
    assert lifecycle_record.status == (
        "post_selection_lifecycle_849_898_recorded_without_final_resolution"
    )
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_selection_record_update_and_alternative_memory_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_post_selection_lifecycle().status)
