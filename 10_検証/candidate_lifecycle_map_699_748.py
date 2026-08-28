"""候補ライフサイクル地図を50工程でstress testする最小検証。"""

from dataclasses import dataclass

from secondary_candidate_reactivation_649_698 import (
    SecondaryReactivationView,
    observe_secondary_candidate_reactivation,
)


@dataclass(frozen=True)
class CandidateLifecycleStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class CandidateLifecycleTransition:
    label: str
    from_state: str
    to_state: str
    trigger: str
    reversible: bool
    deletes_candidate: bool
    asserts_truth: bool


@dataclass(frozen=True)
class CandidateLifecycleEntry:
    label: str
    states: tuple[str, ...]
    transitions: tuple[CandidateLifecycleTransition, ...]
    retained: bool
    status: str


@dataclass(frozen=True)
class CandidateLifecycleMap:
    source_status: str
    entries: tuple[CandidateLifecycleEntry, ...]
    global_stop_lines: tuple[str, ...]
    next_xi_candidates: tuple[str, ...]
    generated_final_resolution: bool
    deleted_candidates: bool
    status: str


@dataclass(frozen=True)
class CandidateLifecycleMapObservation:
    source_status: str
    steps: tuple[CandidateLifecycleStep, ...]
    lifecycle_map: CandidateLifecycleMap
    selected_lifecycle_preserved: bool
    secondary_reactivated_lifecycle_preserved: bool
    transitions_do_not_delete_candidates: bool
    transitions_do_not_assert_truth: bool
    map_is_not_final_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (699, "source_reentry", "reuse_649_698_reactivation", "secondary_reactivation_result_preserved"),
    (700, "source_reentry", "next_xi_received", "candidate_lifecycle_map_stress_received"),
    (701, "source_reentry", "reactivation_view_recheck", "reactivation_views_available"),
    (702, "lifecycle_request", "candidate_lifecycle_map_request", "candidate_lifecycle_map_candidate"),
    (703, "lifecycle_request", "lifecycle_not_generation_guard", "lifecycle_generation_blocked"),
    (704, "lifecycle_request", "lifecycle_not_deletion_guard", "lifecycle_deletion_blocked"),
    (705, "lifecycle_request", "lifecycle_not_truth_guard", "lifecycle_truth_non_identity"),
    (706, "state_inventory", "candidate_state_inventory", "candidate_state_recorded"),
    (707, "state_inventory", "selected_state_inventory", "selected_state_recorded"),
    (708, "state_inventory", "secondary_retained_state_inventory", "secondary_retained_state_recorded"),
    (709, "state_inventory", "reactivated_state_inventory", "reactivated_state_recorded"),
    (710, "state_inventory", "retained_alternative_state_inventory", "retained_alternative_state_recorded"),
    (711, "state_inventory", "state_not_truth_guard", "state_truth_non_identity"),
    (712, "transition_inventory", "candidate_to_selected_transition", "candidate_selected_transition_recorded"),
    (713, "transition_inventory", "candidate_to_secondary_transition", "candidate_secondary_transition_recorded"),
    (714, "transition_inventory", "secondary_to_reactivated_transition", "secondary_reactivated_transition_recorded"),
    (715, "transition_inventory", "selected_to_retained_alternative_transition", "selected_retained_alternative_transition_recorded"),
    (716, "transition_inventory", "reactivated_to_selection_boundary_open", "reactivated_selection_boundary_left_open"),
    (717, "transition_inventory", "transition_not_mutation_guard", "transition_mutation_blocked"),
    (718, "transition_inventory", "transition_not_finalization_guard", "transition_finalization_blocked"),
    (719, "entry_map", "continuation_lifecycle_entry", "continuation_lifecycle_entry_recorded"),
    (720, "entry_map", "reinterpretation_lifecycle_entry", "reinterpretation_lifecycle_entry_recorded"),
    (721, "entry_map", "entry_retention_check", "entries_retained"),
    (722, "entry_map", "entry_state_history_check", "state_histories_preserved"),
    (723, "entry_map", "entry_transition_history_check", "transition_histories_preserved"),
    (724, "entry_map", "entry_not_error_guard", "entry_error_non_identity"),
    (725, "global_map", "global_stop_lines", "global_stop_lines_recorded"),
    (726, "global_map", "next_xi_candidates", "next_xi_candidates_recorded"),
    (727, "global_map", "map_status_assignment", "lifecycle_map_status_recorded"),
    (728, "global_map", "map_not_Core_guard", "map_Core_promotion_blocked"),
    (729, "global_map", "map_not_T2_final_guard", "map_T2_finalization_blocked"),
    (730, "non_identity", "selected_vs_true_split", "selected_true_split_preserved"),
    (731, "non_identity", "secondary_vs_rejected_split", "secondary_rejected_split_preserved"),
    (732, "non_identity", "reactivated_vs_selected_split", "reactivated_selected_split_preserved"),
    (733, "non_identity", "retained_vs_deleted_split", "retained_deleted_split_preserved"),
    (734, "non_identity", "lifecycle_vs_processing_pipeline_split", "lifecycle_pipeline_non_identity"),
    (735, "music_subject", "musical_memory_of_candidates", "musical_candidate_memory_preserved"),
    (736, "music_subject", "interpretation_history_as_music_information", "interpretation_history_preserved_as_music_information"),
    (737, "music_subject", "B_context_sensitive_lifecycle", "B_context_sensitive_lifecycle_preserved"),
    (738, "music_subject", "context_shift_sensitive_lifecycle", "context_shift_sensitive_lifecycle_preserved"),
    (739, "summary", "lifecycle_map_summary", "candidate_lifecycle_map_observed"),
    (740, "summary", "no_candidate_deletion_summary", "no_candidate_deletion_confirmed"),
    (741, "summary", "no_truth_assignment_summary", "no_truth_assignment_confirmed"),
    (742, "summary", "no_final_resolution_summary", "no_final_resolution_generated"),
    (743, "summary", "no_mutation_summary", "no_mutation_generated"),
    (744, "next_plan", "reactivated_to_selection_boundary_candidate", "reactivated_to_selection_boundary_candidate"),
    (745, "next_plan", "lifecycle_memory_limit_open_xi", "lifecycle_memory_limit_left_open"),
    (746, "next_plan", "Core_side_path_record", "Core_side_path_recorded_but_not_taken"),
    (747, "next_plan", "module_generalization_limit_record", "module_generalization_limit_recorded"),
    (748, "next_plan", "next_xi_selection", "xi_reactivated_to_selection_boundary_stress"),
)


def _build_steps() -> tuple[CandidateLifecycleStep, ...]:
    previous = "secondary_candidate_reactivation_649_698"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            CandidateLifecycleStep(
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


def _transitions_for_label(
    label: str,
    reactivation_views: tuple[SecondaryReactivationView, ...],
) -> tuple[CandidateLifecycleTransition, ...]:
    transitions = [
        CandidateLifecycleTransition(
            label=label,
            from_state="candidate",
            to_state="selected" if label == "C major continuation frame" else "secondary_retained",
            trigger="policy_or_threshold_view",
            reversible=True,
            deletes_candidate=False,
            asserts_truth=False,
        )
    ]
    if label == "A minor reinterpretation frame" and any(
        label in view.reactivated_labels for view in reactivation_views
    ):
        transitions.append(
            CandidateLifecycleTransition(
                label=label,
                from_state="secondary_retained",
                to_state="reactivated",
                trigger="context_B_or_policy_shift",
                reversible=True,
                deletes_candidate=False,
                asserts_truth=False,
            )
        )
    if label == "C major continuation frame":
        transitions.append(
            CandidateLifecycleTransition(
                label=label,
                from_state="selected",
                to_state="retained_alternative",
                trigger="B_or_policy_view_change",
                reversible=True,
                deletes_candidate=False,
                asserts_truth=False,
            )
        )
    return tuple(transitions)


def build_candidate_lifecycle_map(
    reactivation_views: tuple[SecondaryReactivationView, ...],
    source_status: str,
) -> CandidateLifecycleMap:
    labels = ("C major continuation frame", "A minor reinterpretation frame")
    entries = []
    for label in labels:
        transitions = _transitions_for_label(label, reactivation_views)
        states = ("candidate",) + tuple(transition.to_state for transition in transitions)
        entries.append(
            CandidateLifecycleEntry(
                label=label,
                states=states,
                transitions=transitions,
                retained=True,
                status="lifecycle_recorded_without_final_resolution",
            )
        )
    return CandidateLifecycleMap(
        source_status=source_status,
        entries=tuple(entries),
        global_stop_lines=(
            "state_not_truth",
            "transition_not_deletion",
            "reactivated_not_selected",
            "selected_not_true",
            "lifecycle_map_not_Core_primitive",
        ),
        next_xi_candidates=(
            "reactivated_to_selection_boundary",
            "candidate_memory_limit",
            "lifecycle_record_schema_view",
        ),
        generated_final_resolution=False,
        deleted_candidates=False,
        status="candidate_lifecycle_map_699_748_built_without_deleting_or_finalizing_candidates",
    )


def observe_candidate_lifecycle_map() -> CandidateLifecycleMapObservation:
    source = observe_secondary_candidate_reactivation()
    lifecycle_map = build_candidate_lifecycle_map(
        source.reactivation_views,
        source.status,
    )
    steps = _build_steps()
    all_transitions = tuple(
        transition
        for entry in lifecycle_map.entries
        for transition in entry.transitions
    )
    entry_by_label = {entry.label: entry for entry in lifecycle_map.entries}

    return CandidateLifecycleMapObservation(
        source_status=source.status,
        steps=steps,
        lifecycle_map=lifecycle_map,
        selected_lifecycle_preserved=(
            "selected" in entry_by_label["C major continuation frame"].states
            and "retained_alternative" in entry_by_label["C major continuation frame"].states
        ),
        secondary_reactivated_lifecycle_preserved=(
            "secondary_retained" in entry_by_label["A minor reinterpretation frame"].states
            and "reactivated" in entry_by_label["A minor reinterpretation frame"].states
        ),
        transitions_do_not_delete_candidates=all(
            transition.deletes_candidate is False for transition in all_transitions
        ),
        transitions_do_not_assert_truth=all(
            transition.asserts_truth is False for transition in all_transitions
        ),
        map_is_not_final_resolution=lifecycle_map.generated_final_resolution is False,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="candidate_lifecycle_map_699_748_observed_without_finalizing_candidate_states",
    )


def run_checks() -> None:
    observation = observe_candidate_lifecycle_map()
    lifecycle_map = observation.lifecycle_map

    assert observation.source_status == (
        "secondary_candidate_reactivation_649_698_observed_without_generating_new_candidates"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 699
    assert observation.steps[-1].number == 748
    assert lifecycle_map.status == (
        "candidate_lifecycle_map_699_748_built_without_deleting_or_finalizing_candidates"
    )
    assert len(lifecycle_map.entries) == 2
    assert observation.selected_lifecycle_preserved is True
    assert observation.secondary_reactivated_lifecycle_preserved is True
    assert observation.transitions_do_not_delete_candidates is True
    assert observation.transitions_do_not_assert_truth is True
    assert observation.map_is_not_final_resolution is True
    assert lifecycle_map.deleted_candidates is False
    assert lifecycle_map.generated_final_resolution is False
    assert observation.generated_mutation is False
    assert "reactivated_to_selection_boundary" in lifecycle_map.next_xi_candidates
    assert observation.steps[-1].result == "xi_reactivated_to_selection_boundary_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_candidate_lifecycle_map().status)
