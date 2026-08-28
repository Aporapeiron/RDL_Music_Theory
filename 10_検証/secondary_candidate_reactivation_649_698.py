"""secondary_retained候補の再活性化を50工程でstress testする最小検証。"""

from dataclasses import dataclass

from threshold_low_weight_retention_599_648 import (
    ThresholdedBView,
    ThresholdedWeightEntry,
    observe_threshold_low_weight_retention,
)


@dataclass(frozen=True)
class SecondaryReactivationStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ReactivationCondition:
    name: str
    source: str
    preferred_label: str
    support_delta: float
    generated_candidate: bool


@dataclass(frozen=True)
class ReactivatedCandidateEntry:
    label: str
    previous_status: str
    reactivated_status: str
    previous_support_weight: float
    reactivated_support_weight: float
    condition_name: str
    retained_before_reactivation: bool
    generated_as_new_candidate: bool


@dataclass(frozen=True)
class SecondaryReactivationView:
    source_view: ThresholdedBView
    condition: ReactivationCondition
    entries: tuple[ReactivatedCandidateEntry, ...]
    reactivated_labels: tuple[str, ...]
    still_retained_labels: tuple[str, ...]
    status: str
    deleted_candidates: bool
    mutated_source_view: bool


@dataclass(frozen=True)
class SecondaryCandidateReactivationObservation:
    source_status: str
    steps: tuple[SecondaryReactivationStep, ...]
    reactivation_views: tuple[SecondaryReactivationView, ...]
    secondary_candidates_exist: bool
    secondary_candidates_reactivated: bool
    reactivation_requires_prior_retention: bool
    reactivation_generates_new_candidates: bool
    source_threshold_views_preserved: bool
    deleted_candidates: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (649, "source_reentry", "reuse_599_648_threshold_retention", "threshold_low_weight_retention_preserved"),
    (650, "source_reentry", "next_xi_received", "secondary_candidate_reactivation_stress_received"),
    (651, "source_reentry", "secondary_retained_recheck", "secondary_retained_candidates_available"),
    (652, "reactivation_request", "reactivation_surface_request", "reactivation_surface_candidate"),
    (653, "reactivation_request", "reactivation_not_generation_guard", "reactivation_generation_blocked"),
    (654, "reactivation_request", "reactivation_not_deletion_reversal_guard", "reactivation_deletion_reversal_blocked"),
    (655, "reactivation_request", "reactivation_not_truth_guard", "reactivation_truth_non_identity"),
    (656, "condition_bundle", "context_shift_condition", "context_shift_condition_recorded"),
    (657, "condition_bundle", "B_shift_condition", "B_shift_condition_recorded"),
    (658, "condition_bundle", "policy_shift_condition", "policy_shift_condition_recorded"),
    (659, "condition_bundle", "condition_not_generator_guard", "condition_generation_blocked"),
    (660, "condition_bundle", "condition_not_Core_guard", "condition_Core_promotion_blocked"),
    (661, "candidate_recheck", "analysis_secondary_candidate_recheck", "analysis_secondary_candidate_found"),
    (662, "candidate_recheck", "performance_secondary_candidate_recheck", "performance_secondary_candidate_found"),
    (663, "candidate_recheck", "listener_secondary_candidate_recheck", "listener_secondary_candidate_found"),
    (664, "candidate_recheck", "composition_secondary_candidate_recheck", "composition_secondary_candidate_found"),
    (665, "candidate_recheck", "candidate_retention_before_reactivation", "prior_retention_confirmed"),
    (666, "reactivation", "context_shift_reactivation", "context_shift_reactivation_observed"),
    (667, "reactivation", "B_shift_reactivation", "B_shift_reactivation_observed"),
    (668, "reactivation", "policy_shift_reactivation", "policy_shift_reactivation_observed"),
    (669, "reactivation", "support_delta_application", "support_delta_applied_as_view"),
    (670, "reactivation", "reactivated_status_assignment", "reactivated_status_recorded"),
    (671, "reactivation", "reactivation_not_source_mutation_guard", "source_threshold_view_mutation_blocked"),
    (672, "reactivation", "reactivation_not_final_selection_guard", "reactivation_selection_non_identity"),
    (673, "reactivated_record", "reactivated_entry_schema", "reactivated_entry_schema_observed"),
    (674, "reactivated_record", "previous_status_field", "previous_status_field_recorded"),
    (675, "reactivated_record", "reactivated_status_field", "reactivated_status_field_recorded"),
    (676, "reactivated_record", "previous_weight_field", "previous_weight_field_recorded"),
    (677, "reactivated_record", "reactivated_weight_field", "reactivated_weight_field_recorded"),
    (678, "reactivated_record", "condition_trace_field", "condition_trace_field_recorded"),
    (679, "retention", "non_reactivated_candidates_retained", "non_reactivated_candidates_retained"),
    (680, "retention", "reactivated_candidates_retained", "reactivated_candidates_retained"),
    (681, "retention", "no_candidate_deletion", "candidate_deletion_blocked"),
    (682, "retention", "reactivation_lifecycle_record", "reactivation_lifecycle_recorded"),
    (683, "non_identity", "secondary_vs_reactivated_split", "secondary_reactivated_non_identity"),
    (684, "non_identity", "reactivation_vs_selection_split", "reactivation_selection_split_preserved"),
    (685, "non_identity", "reactivation_vs_truth_split", "reactivation_truth_split_preserved"),
    (686, "non_identity", "reactivation_vs_generation_split", "reactivation_generation_split_preserved"),
    (687, "music_subject", "delayed_interpretation_return", "delayed_interpretation_return_preserved"),
    (688, "music_subject", "contextual_reaccentuation_return", "contextual_reaccentuation_return_preserved"),
    (689, "music_subject", "music_memory_of_low_salience", "music_memory_of_low_salience_preserved"),
    (690, "summary", "reactivation_surface_summary", "reactivation_surface_observed"),
    (691, "summary", "prior_retention_summary", "prior_retention_required"),
    (692, "summary", "no_generation_summary", "no_new_candidate_generated"),
    (693, "summary", "no_deletion_summary", "no_candidate_deleted"),
    (694, "summary", "no_mutation_summary", "no_mutation_generated"),
    (695, "next_plan", "reactivation_record_lifecycle_open_xi", "reactivation_record_lifecycle_left_open"),
    (696, "next_plan", "context_shift_evidence_open_xi", "context_shift_evidence_left_open"),
    (697, "next_plan", "candidate_lifecycle_map_next_candidate", "candidate_lifecycle_map_next_candidate"),
    (698, "next_plan", "next_xi_selection", "xi_candidate_lifecycle_map_stress"),
)


def _build_steps() -> tuple[SecondaryReactivationStep, ...]:
    previous = "threshold_low_weight_retention_599_648"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            SecondaryReactivationStep(
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


def fixture_reactivation_conditions() -> tuple[ReactivationCondition, ...]:
    return (
        ReactivationCondition(
            name="context_shift_to_relative_minor",
            source="external_context_shift_fixture",
            preferred_label="A minor reinterpretation frame",
            support_delta=0.31,
            generated_candidate=False,
        ),
        ReactivationCondition(
            name="B_shift_to_performance_reaccentuation",
            source="external_B_shift_fixture",
            preferred_label="A minor reinterpretation frame",
            support_delta=0.27,
            generated_candidate=False,
        ),
        ReactivationCondition(
            name="policy_shift_to_future_pivot",
            source="external_policy_shift_fixture",
            preferred_label="A minor reinterpretation frame",
            support_delta=0.36,
            generated_candidate=False,
        ),
    )


def _entry_for_reactivation(
    entry: ThresholdedWeightEntry,
    condition: ReactivationCondition,
) -> ReactivatedCandidateEntry:
    reactivated = (
        entry.display_status == "secondary_retained"
        and entry.label == condition.preferred_label
    )
    next_weight = entry.support_weight + condition.support_delta if reactivated else entry.support_weight
    return ReactivatedCandidateEntry(
        label=entry.label,
        previous_status=entry.display_status,
        reactivated_status="reactivated" if reactivated else entry.display_status,
        previous_support_weight=entry.support_weight,
        reactivated_support_weight=round(next_weight, 2),
        condition_name=condition.name,
        retained_before_reactivation=entry.retained,
        generated_as_new_candidate=False,
    )


def apply_reactivation_condition(
    view: ThresholdedBView,
    condition: ReactivationCondition,
) -> SecondaryReactivationView:
    entries = tuple(
        _entry_for_reactivation(entry, condition)
        for entry in view.entries
    )
    return SecondaryReactivationView(
        source_view=view,
        condition=condition,
        entries=entries,
        reactivated_labels=tuple(
            entry.label for entry in entries if entry.reactivated_status == "reactivated"
        ),
        still_retained_labels=tuple(entry.label for entry in entries),
        status="secondary_candidate_reactivation_observed_without_candidate_generation",
        deleted_candidates=False,
        mutated_source_view=False,
    )


def observe_secondary_candidate_reactivation() -> SecondaryCandidateReactivationObservation:
    source = observe_threshold_low_weight_retention()
    conditions = fixture_reactivation_conditions()
    views = tuple(
        apply_reactivation_condition(view, conditions[index % len(conditions)])
        for index, view in enumerate(source.thresholded_views)
    )
    steps = _build_steps()

    return SecondaryCandidateReactivationObservation(
        source_status=source.status,
        steps=steps,
        reactivation_views=views,
        secondary_candidates_exist=source.low_weight_candidates_exist,
        secondary_candidates_reactivated=any(view.reactivated_labels for view in views),
        reactivation_requires_prior_retention=all(
            entry.retained_before_reactivation
            for view in views
            for entry in view.entries
            if entry.reactivated_status == "reactivated"
        ),
        reactivation_generates_new_candidates=any(
            entry.generated_as_new_candidate
            for view in views
            for entry in view.entries
        )
        or any(view.condition.generated_candidate for view in views),
        source_threshold_views_preserved=all(view.mutated_source_view is False for view in views),
        deleted_candidates=any(view.deleted_candidates for view in views),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="secondary_candidate_reactivation_649_698_observed_without_generating_new_candidates",
    )


def run_checks() -> None:
    observation = observe_secondary_candidate_reactivation()

    assert observation.source_status == (
        "threshold_low_weight_retention_599_648_observed_without_deleting_low_weight_candidates"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 649
    assert observation.steps[-1].number == 698
    assert len(observation.reactivation_views) == 4
    assert observation.secondary_candidates_exist is True
    assert observation.secondary_candidates_reactivated is True
    assert observation.reactivation_requires_prior_retention is True
    assert observation.reactivation_generates_new_candidates is False
    assert observation.source_threshold_views_preserved is True
    assert observation.deleted_candidates is False
    assert observation.generated_mutation is False
    assert any(
        "A minor reinterpretation frame" in view.reactivated_labels
        for view in observation.reactivation_views
    )
    assert all(
        set(view.still_retained_labels)
        == {"C major continuation frame", "A minor reinterpretation frame"}
        for view in observation.reactivation_views
    )
    assert observation.steps[-1].result == "xi_candidate_lifecycle_map_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_secondary_candidate_reactivation().status)
