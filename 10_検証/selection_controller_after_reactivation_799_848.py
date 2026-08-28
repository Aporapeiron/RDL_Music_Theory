"""再活性化後のselection controllerを50工程でstress testする最小検証。"""

from dataclasses import dataclass

from reactivated_to_selection_boundary_749_798 import (
    ReactivatedSelectionReadiness,
    observe_reactivated_to_selection_boundary,
)


@dataclass(frozen=True)
class SelectionControllerStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class SelectionController:
    name: str
    origin: str
    required_source_state: str
    selection_reason: str
    generated_candidate: bool
    asserts_truth: bool


@dataclass(frozen=True)
class ControlledSelectionRecord:
    readiness: ReactivatedSelectionReadiness
    controller: SelectionController
    selected_label: str
    retained_alternatives: tuple[str, ...]
    post_selection_state: str
    lifecycle_still_open: bool
    generated_candidate: bool
    deleted_alternatives: bool
    asserted_truth: bool
    status: str


@dataclass(frozen=True)
class SelectionControllerAfterReactivationObservation:
    source_status: str
    steps: tuple[SelectionControllerStep, ...]
    controller: SelectionController
    selection_record: ControlledSelectionRecord
    reactivated_candidate_selected: bool
    selection_requires_controller: bool
    controller_generates_candidate: bool
    selection_asserts_truth: bool
    alternatives_retained_after_selection: bool
    post_selection_lifecycle_open: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (799, "source_reentry", "reuse_749_798_selection_readiness", "reactivated_selection_readiness_preserved"),
    (800, "source_reentry", "next_xi_received", "selection_controller_after_reactivation_stress_received"),
    (801, "source_reentry", "readiness_recheck", "reactivated_candidate_readiness_available"),
    (802, "controller_request", "selection_controller_request", "selection_controller_candidate"),
    (803, "controller_request", "controller_not_candidate_generator_guard", "controller_candidate_generation_blocked"),
    (804, "controller_request", "controller_not_truth_guard", "controller_truth_non_identity"),
    (805, "controller_request", "controller_not_Core_guard", "controller_Core_promotion_blocked"),
    (806, "controller_request", "controller_origin_record", "controller_origin_recorded"),
    (807, "controller_conditions", "required_source_state_check", "required_source_state_recorded"),
    (808, "controller_conditions", "readiness_status_check", "readiness_status_recorded"),
    (809, "controller_conditions", "candidate_label_check", "reactivated_candidate_label_recorded"),
    (810, "controller_conditions", "alternative_presence_check", "alternative_presence_recorded"),
    (811, "controller_conditions", "condition_not_truth_guard", "condition_truth_non_identity"),
    (812, "selection_application", "controller_application", "selection_controller_applied"),
    (813, "selection_application", "reactivated_candidate_selection", "A_minor_reinterpretation_selected_by_controller"),
    (814, "selection_application", "selection_record_creation", "controlled_selection_record_created"),
    (815, "selection_application", "selection_not_generation_guard", "selection_generation_blocked"),
    (816, "selection_application", "selection_not_truth_guard", "selection_truth_non_identity"),
    (817, "alternative_retention", "previous_continuation_retained", "C_major_continuation_retained_after_selection"),
    (818, "alternative_retention", "selected_candidate_retained", "selected_candidate_retained_in_lifecycle"),
    (819, "alternative_retention", "alternative_not_deleted_guard", "alternative_deletion_blocked"),
    (820, "alternative_retention", "alternative_not_error_guard", "alternative_error_non_identity"),
    (821, "post_selection", "post_selection_state_assignment", "selected_after_reactivation_state_recorded"),
    (822, "post_selection", "post_selection_lifecycle_open", "post_selection_lifecycle_open_recorded"),
    (823, "post_selection", "post_selection_not_final_guard", "post_selection_finalization_blocked"),
    (824, "post_selection", "post_selection_not_truth_guard", "post_selection_truth_non_identity"),
    (825, "record_schema", "controller_name_field", "controller_name_field_recorded"),
    (826, "record_schema", "controller_origin_field", "controller_origin_field_recorded"),
    (827, "record_schema", "selection_reason_field", "selection_reason_field_recorded"),
    (828, "record_schema", "post_selection_state_field", "post_selection_state_field_recorded"),
    (829, "record_schema", "lifecycle_open_field", "lifecycle_open_field_recorded"),
    (830, "record_schema", "retained_alternatives_field", "retained_alternatives_field_recorded"),
    (831, "non_identity", "controller_vs_policy_split", "controller_policy_non_identity"),
    (832, "non_identity", "controller_vs_selection_split", "controller_selection_non_identity"),
    (833, "non_identity", "selection_vs_truth_split", "selection_truth_split_preserved"),
    (834, "non_identity", "selection_vs_lifecycle_close_split", "selection_lifecycle_close_split_preserved"),
    (835, "non_identity", "post_selection_vs_final_resolution_split", "post_selection_final_resolution_split_preserved"),
    (836, "music_subject", "delayed_reinterpretation_selection", "delayed_reinterpretation_selection_preserved"),
    (837, "music_subject", "continuation_as_retained_alternative", "continuation_retained_as_music_information"),
    (838, "music_subject", "post_selection_ambiguity_memory", "post_selection_ambiguity_memory_preserved"),
    (839, "summary", "controller_boundary_summary", "selection_controller_boundary_observed"),
    (840, "summary", "reactivated_selection_summary", "reactivated_candidate_selected_by_controller"),
    (841, "summary", "alternative_retention_summary", "alternatives_retained_after_controller_selection"),
    (842, "summary", "post_selection_open_summary", "post_selection_lifecycle_remains_open"),
    (843, "summary", "no_truth_summary", "selection_asserted_no_truth"),
    (844, "summary", "no_mutation_summary", "no_mutation_generated"),
    (845, "next_plan", "post_selection_lifecycle_next_candidate", "post_selection_lifecycle_next_candidate"),
    (846, "next_plan", "controller_origin_open_xi", "controller_origin_left_open"),
    (847, "next_plan", "selection_record_update_open_xi", "selection_record_update_left_open"),
    (848, "next_plan", "next_xi_selection", "xi_post_selection_lifecycle_stress"),
)


def _build_steps() -> tuple[SelectionControllerStep, ...]:
    previous = "reactivated_to_selection_boundary_749_798"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            SelectionControllerStep(
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


def fixture_selection_controller() -> SelectionController:
    return SelectionController(
        name="reactivated_selection_controller_fixture",
        origin="external_context_shift_selection_controller",
        required_source_state="reactivated",
        selection_reason="context_shift_prioritizes_relative_minor_reinterpretation",
        generated_candidate=False,
        asserts_truth=False,
    )


def apply_selection_controller(
    readiness: ReactivatedSelectionReadiness,
    controller: SelectionController,
) -> ControlledSelectionRecord:
    if readiness.request.source_state != controller.required_source_state:
        raise ValueError("readiness source state does not match controller")
    if not readiness.eligible:
        raise ValueError("readiness must be eligible before controller selection")
    return ControlledSelectionRecord(
        readiness=readiness,
        controller=controller,
        selected_label=readiness.request.candidate_label,
        retained_alternatives=readiness.retained_alternatives,
        post_selection_state="selected_after_reactivation",
        lifecycle_still_open=True,
        generated_candidate=False,
        deleted_alternatives=False,
        asserted_truth=False,
        status="reactivated_candidate_selected_by_controller_without_closing_lifecycle",
    )


def observe_selection_controller_after_reactivation() -> SelectionControllerAfterReactivationObservation:
    source = observe_reactivated_to_selection_boundary()
    controller = fixture_selection_controller()
    selection_record = apply_selection_controller(source.readiness, controller)
    steps = _build_steps()

    return SelectionControllerAfterReactivationObservation(
        source_status=source.status,
        steps=steps,
        controller=controller,
        selection_record=selection_record,
        reactivated_candidate_selected=(
            selection_record.selected_label == "A minor reinterpretation frame"
            and source.reactivated_is_selected is False
        ),
        selection_requires_controller=(
            source.readiness.selected is False
            and selection_record.controller.name == "reactivated_selection_controller_fixture"
        ),
        controller_generates_candidate=controller.generated_candidate,
        selection_asserts_truth=selection_record.asserted_truth,
        alternatives_retained_after_selection=(
            selection_record.retained_alternatives == ("C major continuation frame",)
            and selection_record.deleted_alternatives is False
        ),
        post_selection_lifecycle_open=selection_record.lifecycle_still_open,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="selection_controller_after_reactivation_799_848_observed_without_closing_post_selection_lifecycle",
    )


def run_checks() -> None:
    observation = observe_selection_controller_after_reactivation()

    assert observation.source_status == (
        "reactivated_to_selection_boundary_749_798_observed_without_treating_reactivation_as_selection"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 799
    assert observation.steps[-1].number == 848
    assert observation.reactivated_candidate_selected is True
    assert observation.selection_requires_controller is True
    assert observation.controller_generates_candidate is False
    assert observation.selection_asserts_truth is False
    assert observation.alternatives_retained_after_selection is True
    assert observation.post_selection_lifecycle_open is True
    assert observation.selection_record.status == (
        "reactivated_candidate_selected_by_controller_without_closing_lifecycle"
    )
    assert observation.selection_record.generated_candidate is False
    assert observation.selection_record.deleted_alternatives is False
    assert observation.selection_record.asserted_truth is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_post_selection_lifecycle_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_selection_controller_after_reactivation().status)
