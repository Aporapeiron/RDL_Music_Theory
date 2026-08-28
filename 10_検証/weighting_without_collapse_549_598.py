"""候補へweightを付けても単一解へ潰さないことを検査する最小実験。"""

from dataclasses import dataclass

from policy_origin_B_dependent_selection_499_548 import (
    BContext,
    fixture_B_contexts,
    observe_B_dependent_policy_selection,
)
from cross_module_prediction_split_349_398 import (
    PredictionFrameCandidate,
    observe_prediction_split,
)


@dataclass(frozen=True)
class WeightingStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class InterpretationWeight:
    b_context: BContext
    candidate: PredictionFrameCandidate
    support_weight: float
    retention_weight: float
    weight_source: str
    status: str


@dataclass(frozen=True)
class BWeightingView:
    b_context: BContext
    weights: tuple[InterpretationWeight, ...]
    highest_weight_label: str
    retained_labels: tuple[str, ...]
    status: str
    generated_selection: bool
    deleted_alternatives: bool


@dataclass(frozen=True)
class WeightingWithoutCollapseObservation:
    source_status: str
    steps: tuple[WeightingStep, ...]
    weighting_views: tuple[BWeightingView, ...]
    weight_varies_by_B: bool
    highest_weight_can_differ: bool
    all_candidates_retained: bool
    weight_is_probability: bool
    weight_is_truth: bool
    weight_generates_selection: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (549, "source_reentry", "reuse_499_548_B_policy_selection", "B_dependent_policy_selection_preserved"),
    (550, "source_reentry", "next_xi_received", "weighting_without_collapse_stress_received"),
    (551, "source_reentry", "same_candidate_set_recheck", "same_candidate_set_available_for_weighting"),
    (552, "weight_request", "weight_view_request", "interpretation_weight_view_candidate"),
    (553, "weight_request", "weight_not_probability_guard", "weight_probability_non_identity"),
    (554, "weight_request", "weight_not_truth_guard", "weight_truth_non_identity"),
    (555, "weight_request", "weight_not_deletion_guard", "weight_deletion_blocked"),
    (556, "weight_request", "weight_not_selection_generator_guard", "weight_selection_generation_blocked"),
    (557, "B_weighting", "analysis_weight_view", "analysis_weight_view_recorded"),
    (558, "B_weighting", "performance_weight_view", "performance_weight_view_recorded"),
    (559, "B_weighting", "listener_weight_view", "listener_weight_view_recorded"),
    (560, "B_weighting", "composition_weight_view", "composition_weight_view_recorded"),
    (561, "B_weighting", "weight_source_per_B", "weight_source_per_B_preserved"),
    (562, "B_weighting", "B_weight_non_universal_guard", "B_weight_universalization_blocked"),
    (563, "candidate_weights", "continuation_support_weight", "continuation_support_weight_recorded"),
    (564, "candidate_weights", "reinterpretation_support_weight", "reinterpretation_support_weight_recorded"),
    (565, "candidate_weights", "retention_weight_for_selected_path", "selected_path_retention_weight_recorded"),
    (566, "candidate_weights", "retention_weight_for_alternative_path", "alternative_path_retention_weight_recorded"),
    (567, "candidate_weights", "weight_not_confidence_guard", "weight_confidence_non_identity"),
    (568, "candidate_weights", "weight_not_certainty_guard", "weight_certainty_non_identity"),
    (569, "ranking_view", "analysis_highest_weight", "analysis_highest_weight_observed"),
    (570, "ranking_view", "performance_highest_weight", "performance_highest_weight_observed"),
    (571, "ranking_view", "listener_highest_weight", "listener_highest_weight_observed"),
    (572, "ranking_view", "composition_highest_weight", "composition_highest_weight_observed"),
    (573, "ranking_view", "highest_weight_differs_by_B", "highest_weight_B_difference_preserved"),
    (574, "ranking_view", "ranking_not_selection_guard", "ranking_selection_non_identity"),
    (575, "retention", "analysis_candidate_retention", "analysis_candidates_retained"),
    (576, "retention", "performance_candidate_retention", "performance_candidates_retained"),
    (577, "retention", "listener_candidate_retention", "listener_candidates_retained"),
    (578, "retention", "composition_candidate_retention", "composition_candidates_retained"),
    (579, "retention", "low_weight_not_error_guard", "low_weight_error_non_identity"),
    (580, "retention", "low_weight_not_deletion_guard", "low_weight_deletion_blocked"),
    (581, "record_view", "weight_record_schema", "weight_record_schema_observed"),
    (582, "record_view", "support_vs_retention_weight_split", "support_retention_weight_split_preserved"),
    (583, "record_view", "weight_source_trace", "weight_source_trace_recorded"),
    (584, "record_view", "weight_view_not_source_record_mutation", "weight_view_source_record_mutation_blocked"),
    (585, "non_identity", "weight_vs_policy_split", "weight_policy_non_identity"),
    (586, "non_identity", "weight_vs_score_split", "weight_score_non_identity"),
    (587, "non_identity", "weight_vs_probability_split", "weight_probability_split_preserved"),
    (588, "non_identity", "weight_vs_truth_split", "weight_truth_split_preserved"),
    (589, "music_subject", "music_preference_gradient", "music_preference_gradient_preserved"),
    (590, "music_subject", "ambiguity_not_flattened", "ambiguity_not_flattened_by_weight"),
    (591, "music_subject", "performance_listener_difference", "performance_listener_weight_difference_preserved"),
    (592, "summary", "weighting_surface_summary", "weighting_surface_observed"),
    (593, "summary", "no_collapse_summary", "weighting_without_collapse_confirmed"),
    (594, "summary", "alternative_retention_summary", "alternatives_retained_under_weighting"),
    (595, "summary", "no_mutation_summary", "no_mutation_generated"),
    (596, "next_plan", "threshold_policy_open_xi", "threshold_policy_left_open"),
    (597, "next_plan", "real_evidence_weight_origin_open_xi", "real_evidence_weight_origin_left_open"),
    (598, "next_plan", "next_xi_selection", "xi_threshold_policy_and_low_weight_retention_stress"),
)


def _build_steps() -> tuple[WeightingStep, ...]:
    previous = "policy_origin_B_dependent_selection_499_548"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            WeightingStep(
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


SUPPORT_BY_ROLE: dict[str, tuple[float, float]] = {
    "analysis": (0.72, 0.38),
    "performance": (0.41, 0.76),
    "listener": (0.66, 0.44),
    "composition": (0.45, 0.81),
}


def _support_for(context: BContext, candidate: PredictionFrameCandidate) -> float:
    continuation, reinterpretation = SUPPORT_BY_ROLE[context.role]
    if candidate.label == "C major continuation frame":
        return continuation
    if candidate.label == "A minor reinterpretation frame":
        return reinterpretation
    raise ValueError(f"unknown candidate: {candidate.label}")


def build_weighting_view(
    context: BContext,
    candidates: tuple[PredictionFrameCandidate, ...],
) -> BWeightingView:
    weights = tuple(
        InterpretationWeight(
            b_context=context,
            candidate=candidate,
            support_weight=_support_for(context, candidate),
            retention_weight=1.0 if context.retention_required else 0.0,
            weight_source=context.policy_origin,
            status="weighted_without_collapse",
        )
        for candidate in candidates
    )
    highest = max(weights, key=lambda item: item.support_weight)
    return BWeightingView(
        b_context=context,
        weights=weights,
        highest_weight_label=highest.candidate.label,
        retained_labels=tuple(weight.candidate.label for weight in weights),
        status="weighting_view_observed_without_selection_generation",
        generated_selection=False,
        deleted_alternatives=False,
    )


def observe_weighting_without_collapse() -> WeightingWithoutCollapseObservation:
    source = observe_B_dependent_policy_selection()
    split = observe_prediction_split()
    views = tuple(
        build_weighting_view(context, split.prediction_candidates)
        for context in fixture_B_contexts()
    )
    steps = _build_steps()
    labels_by_B = {view.highest_weight_label for view in views}
    weight_signatures = {
        tuple(weight.support_weight for weight in view.weights)
        for view in views
    }

    return WeightingWithoutCollapseObservation(
        source_status=source.status,
        steps=steps,
        weighting_views=views,
        weight_varies_by_B=len(weight_signatures) == len(views),
        highest_weight_can_differ=labels_by_B == {
            "C major continuation frame",
            "A minor reinterpretation frame",
        },
        all_candidates_retained=all(
            set(view.retained_labels)
            == {"C major continuation frame", "A minor reinterpretation frame"}
            and view.deleted_alternatives is False
            for view in views
        ),
        weight_is_probability=False,
        weight_is_truth=False,
        weight_generates_selection=any(view.generated_selection for view in views),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="weighting_without_collapse_549_598_observed_without_turning_weight_into_probability_or_truth",
    )


def run_checks() -> None:
    observation = observe_weighting_without_collapse()

    assert observation.source_status == (
        "policy_origin_B_dependent_selection_499_548_observed_without_treating_B_as_truth"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 549
    assert observation.steps[-1].number == 598
    assert len(observation.weighting_views) == 4
    assert observation.weight_varies_by_B is True
    assert observation.highest_weight_can_differ is True
    assert observation.all_candidates_retained is True
    assert observation.weight_is_probability is False
    assert observation.weight_is_truth is False
    assert observation.weight_generates_selection is False
    assert observation.generated_mutation is False
    assert all(
        view.status == "weighting_view_observed_without_selection_generation"
        for view in observation.weighting_views
    )
    assert all(len(view.weights) == 2 for view in observation.weighting_views)
    assert observation.steps[-1].result == "xi_threshold_policy_and_low_weight_retention_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_weighting_without_collapse().status)
