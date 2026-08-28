"""threshold policyを通しても低weight候補を保持する最小検証。"""

from dataclasses import dataclass

from weighting_without_collapse_549_598 import (
    BWeightingView,
    InterpretationWeight,
    observe_weighting_without_collapse,
)


@dataclass(frozen=True)
class ThresholdRetentionStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ThresholdPolicy:
    name: str
    support_threshold: float
    low_weight_status: str
    threshold_source: str
    deletes_below_threshold: bool


@dataclass(frozen=True)
class ThresholdedWeightEntry:
    label: str
    support_weight: float
    retention_weight: float
    above_threshold: bool
    display_status: str
    retained: bool
    deletion_reason: str | None


@dataclass(frozen=True)
class ThresholdedBView:
    source_view: BWeightingView
    policy: ThresholdPolicy
    entries: tuple[ThresholdedWeightEntry, ...]
    retained_labels: tuple[str, ...]
    low_weight_labels: tuple[str, ...]
    status: str
    generated_selection: bool
    deleted_alternatives: bool


@dataclass(frozen=True)
class ThresholdLowWeightRetentionObservation:
    source_status: str
    steps: tuple[ThresholdRetentionStep, ...]
    threshold_policy: ThresholdPolicy
    thresholded_views: tuple[ThresholdedBView, ...]
    low_weight_candidates_exist: bool
    low_weight_candidates_retained: bool
    threshold_deletes_candidates: bool
    threshold_is_truth_boundary: bool
    threshold_is_selection_generator: bool
    all_candidates_retained: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (599, "source_reentry", "reuse_549_598_weighting_view", "weighting_without_collapse_result_preserved"),
    (600, "source_reentry", "next_xi_received", "threshold_policy_and_low_weight_retention_stress_received"),
    (601, "source_reentry", "weight_view_recheck", "weight_view_available_for_threshold"),
    (602, "threshold_request", "threshold_policy_request", "threshold_policy_candidate"),
    (603, "threshold_request", "threshold_not_truth_guard", "threshold_truth_non_identity"),
    (604, "threshold_request", "threshold_not_deletion_guard", "threshold_deletion_blocked"),
    (605, "threshold_request", "threshold_not_selection_generator_guard", "threshold_selection_generation_blocked"),
    (606, "threshold_request", "threshold_source_external_guard", "threshold_external_source_preserved"),
    (607, "threshold_policy", "support_threshold_set", "support_threshold_recorded"),
    (608, "threshold_policy", "low_weight_status_set", "low_weight_status_recorded"),
    (609, "threshold_policy", "delete_flag_false", "deletes_below_threshold_false"),
    (610, "threshold_policy", "threshold_as_view_policy", "threshold_view_policy_preserved"),
    (611, "threshold_policy", "threshold_not_probability_guard", "threshold_probability_non_identity"),
    (612, "threshold_application", "analysis_threshold_application", "analysis_threshold_view_recorded"),
    (613, "threshold_application", "performance_threshold_application", "performance_threshold_view_recorded"),
    (614, "threshold_application", "listener_threshold_application", "listener_threshold_view_recorded"),
    (615, "threshold_application", "composition_threshold_application", "composition_threshold_view_recorded"),
    (616, "threshold_application", "above_threshold_labels", "above_threshold_labels_recorded"),
    (617, "threshold_application", "below_threshold_labels", "below_threshold_labels_recorded"),
    (618, "threshold_application", "threshold_not_source_mutation_guard", "threshold_source_mutation_blocked"),
    (619, "low_weight_retention", "analysis_low_weight_retention", "analysis_low_weight_candidates_retained"),
    (620, "low_weight_retention", "performance_low_weight_retention", "performance_low_weight_candidates_retained"),
    (621, "low_weight_retention", "listener_low_weight_retention", "listener_low_weight_candidates_retained"),
    (622, "low_weight_retention", "composition_low_weight_retention", "composition_low_weight_candidates_retained"),
    (623, "low_weight_retention", "low_weight_not_error_guard", "low_weight_error_non_identity"),
    (624, "low_weight_retention", "low_weight_not_deleted_guard", "low_weight_deletion_blocked"),
    (625, "low_weight_retention", "low_weight_future_xi_record", "low_weight_future_xi_preserved"),
    (626, "classification", "primary_display_status", "primary_display_status_recorded"),
    (627, "classification", "secondary_retained_status", "secondary_retained_status_recorded"),
    (628, "classification", "status_not_truth_guard", "display_status_truth_non_identity"),
    (629, "classification", "status_not_error_guard", "display_status_error_non_identity"),
    (630, "record_view", "thresholded_record_schema", "thresholded_record_schema_observed"),
    (631, "record_view", "retention_reason_field", "retention_reason_field_recorded"),
    (632, "record_view", "deletion_reason_empty_check", "deletion_reason_absence_confirmed"),
    (633, "record_view", "threshold_policy_trace", "threshold_policy_trace_recorded"),
    (634, "non_identity", "threshold_vs_weight_split", "threshold_weight_non_identity"),
    (635, "non_identity", "threshold_vs_selection_split", "threshold_selection_non_identity"),
    (636, "non_identity", "threshold_vs_truth_split", "threshold_truth_split_preserved"),
    (637, "non_identity", "threshold_vs_deletion_split", "threshold_deletion_split_preserved"),
    (638, "music_subject", "low_salience_music_reading", "low_salience_music_reading_preserved"),
    (639, "music_subject", "secondary_interpretation_space", "secondary_interpretation_space_preserved"),
    (640, "music_subject", "ambiguity_survives_threshold", "ambiguity_survives_threshold"),
    (641, "summary", "threshold_boundary_summary", "threshold_boundary_observed"),
    (642, "summary", "low_weight_retention_summary", "low_weight_retention_confirmed"),
    (643, "summary", "no_deletion_summary", "threshold_deleted_no_candidates"),
    (644, "summary", "no_mutation_summary", "no_mutation_generated"),
    (645, "next_plan", "real_evidence_threshold_origin_open_xi", "real_evidence_threshold_origin_left_open"),
    (646, "next_plan", "secondary_candidate_reactivation_open_xi", "secondary_candidate_reactivation_left_open"),
    (647, "next_plan", "threshold_record_schema_next_candidate", "threshold_record_schema_next_candidate"),
    (648, "next_plan", "next_xi_selection", "xi_secondary_candidate_reactivation_stress"),
)


def _build_steps() -> tuple[ThresholdRetentionStep, ...]:
    previous = "weighting_without_collapse_549_598"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            ThresholdRetentionStep(
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


def fixture_threshold_policy() -> ThresholdPolicy:
    return ThresholdPolicy(
        name="support_threshold_with_low_weight_retention",
        support_threshold=0.60,
        low_weight_status="secondary_retained",
        threshold_source="external_display_policy_fixture",
        deletes_below_threshold=False,
    )


def _threshold_entry(
    weight: InterpretationWeight,
    policy: ThresholdPolicy,
) -> ThresholdedWeightEntry:
    above = weight.support_weight >= policy.support_threshold
    return ThresholdedWeightEntry(
        label=weight.candidate.label,
        support_weight=weight.support_weight,
        retention_weight=weight.retention_weight,
        above_threshold=above,
        display_status="primary_display" if above else policy.low_weight_status,
        retained=True,
        deletion_reason=None,
    )


def apply_threshold_policy(
    view: BWeightingView,
    policy: ThresholdPolicy,
) -> ThresholdedBView:
    entries = tuple(_threshold_entry(weight, policy) for weight in view.weights)
    return ThresholdedBView(
        source_view=view,
        policy=policy,
        entries=entries,
        retained_labels=tuple(entry.label for entry in entries if entry.retained),
        low_weight_labels=tuple(
            entry.label for entry in entries if not entry.above_threshold
        ),
        status="threshold_view_observed_with_low_weight_retention",
        generated_selection=False,
        deleted_alternatives=False,
    )


def observe_threshold_low_weight_retention() -> ThresholdLowWeightRetentionObservation:
    source = observe_weighting_without_collapse()
    policy = fixture_threshold_policy()
    views = tuple(
        apply_threshold_policy(view, policy)
        for view in source.weighting_views
    )
    steps = _build_steps()

    return ThresholdLowWeightRetentionObservation(
        source_status=source.status,
        steps=steps,
        threshold_policy=policy,
        thresholded_views=views,
        low_weight_candidates_exist=any(view.low_weight_labels for view in views),
        low_weight_candidates_retained=all(
            set(view.low_weight_labels).issubset(set(view.retained_labels))
            for view in views
        ),
        threshold_deletes_candidates=any(view.deleted_alternatives for view in views),
        threshold_is_truth_boundary=False,
        threshold_is_selection_generator=any(view.generated_selection for view in views),
        all_candidates_retained=all(
            set(view.retained_labels)
            == {"C major continuation frame", "A minor reinterpretation frame"}
            for view in views
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="threshold_low_weight_retention_599_648_observed_without_deleting_low_weight_candidates",
    )


def run_checks() -> None:
    observation = observe_threshold_low_weight_retention()

    assert observation.source_status == (
        "weighting_without_collapse_549_598_observed_without_turning_weight_into_probability_or_truth"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 599
    assert observation.steps[-1].number == 648
    assert observation.threshold_policy.support_threshold == 0.60
    assert observation.threshold_policy.deletes_below_threshold is False
    assert len(observation.thresholded_views) == 4
    assert observation.low_weight_candidates_exist is True
    assert observation.low_weight_candidates_retained is True
    assert observation.threshold_deletes_candidates is False
    assert observation.threshold_is_truth_boundary is False
    assert observation.threshold_is_selection_generator is False
    assert observation.all_candidates_retained is True
    assert observation.generated_mutation is False
    assert all(
        entry.deletion_reason is None
        for view in observation.thresholded_views
        for entry in view.entries
    )
    assert {
        entry.display_status
        for view in observation.thresholded_views
        for entry in view.entries
    } == {"primary_display", "secondary_retained"}
    assert observation.steps[-1].result == "xi_secondary_candidate_reactivation_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_threshold_low_weight_retention().status)
