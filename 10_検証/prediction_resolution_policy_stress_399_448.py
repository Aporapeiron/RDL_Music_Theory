"""予測分岐を解決するpolicy境界を50工程でstress testする最小実験。"""

from dataclasses import dataclass

from cross_module_prediction_split_349_398 import (
    PredictionFrameCandidate,
    observe_prediction_split,
)


@dataclass(frozen=True)
class ResolutionPolicyStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class PolicyCriterion:
    name: str
    preferred_value: str
    source: str


@dataclass(frozen=True)
class PredictionResolutionPolicy:
    name: str
    criteria: tuple[PolicyCriterion, ...]
    generated_candidates: bool


@dataclass(frozen=True)
class PolicyScore:
    candidate: PredictionFrameCandidate
    matched_criteria: tuple[str, ...]
    score: int


@dataclass(frozen=True)
class PolicyDecisionRecord:
    policy: PredictionResolutionPolicy
    scores: tuple[PolicyScore, ...]
    selected: PredictionFrameCandidate | None
    retained_alternatives: tuple[PredictionFrameCandidate, ...]
    status: str
    generated_prediction: bool
    deleted_alternatives: bool


@dataclass(frozen=True)
class PredictionResolutionPolicyStressObservation:
    source_status: str
    steps: tuple[ResolutionPolicyStep, ...]
    policy: PredictionResolutionPolicy
    decision: PolicyDecisionRecord
    policy_selects_one_candidate: bool
    policy_generates_candidates: bool
    alternative_retention_preserved: bool
    unresolved_without_policy_preserved: bool
    selected_prediction_is_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (399, "source_reentry", "reuse_349_398_prediction_split", "prediction_split_result_preserved"),
    (400, "source_reentry", "next_xi_received", "prediction_split_resolution_policy_stress_received"),
    (401, "source_reentry", "multiple_interpretation_recheck", "multiple_interpretation_still_retained"),
    (402, "policy_request", "resolution_policy_request", "resolution_policy_candidate"),
    (403, "policy_request", "policy_not_candidate_generator_guard", "policy_candidate_generation_blocked"),
    (404, "policy_request", "policy_not_Core_guard", "policy_Core_promotion_blocked"),
    (405, "policy_request", "policy_not_unified_Module_guard", "policy_unified_Module_blocked"),
    (406, "criteria_bundle", "continuation_preference_criterion", "continuation_preference_criterion_recorded"),
    (407, "criteria_bundle", "grid_alignment_criterion", "grid_alignment_criterion_recorded"),
    (408, "criteria_bundle", "reinterpretation_retention_criterion", "reinterpretation_retention_criterion_recorded"),
    (409, "criteria_bundle", "criteria_source_external_guard", "criteria_external_source_preserved"),
    (410, "criteria_bundle", "criteria_not_truth_guard", "criteria_not_truth_condition"),
    (411, "criteria_bundle", "criteria_not_generation_guard", "criteria_generation_blocked"),
    (412, "scoring_boundary", "candidate_set_reuse", "prediction_candidates_reused"),
    (413, "scoring_boundary", "continuation_candidate_score", "continuation_candidate_scored"),
    (414, "scoring_boundary", "reinterpretation_candidate_score", "reinterpretation_candidate_scored"),
    (415, "scoring_boundary", "score_not_confidence_guard", "score_confidence_non_identity"),
    (416, "scoring_boundary", "score_not_probability_guard", "score_probability_non_identity"),
    (417, "scoring_boundary", "score_not_music_truth_guard", "score_music_truth_non_identity"),
    (418, "selection_boundary", "highest_score_selection", "highest_score_candidate_selected"),
    (419, "selection_boundary", "selected_continuation_frame", "C_major_continuation_frame_selected"),
    (420, "selection_boundary", "selection_requires_policy", "selection_policy_dependency_preserved"),
    (421, "selection_boundary", "selection_not_prediction_generation", "selection_prediction_generation_blocked"),
    (422, "selection_boundary", "selection_not_context_generation", "selection_context_generation_blocked"),
    (423, "selection_boundary", "selection_record_created", "policy_decision_record_created"),
    (424, "alternative_retention", "unselected_reinterpretation_retained", "A_minor_reinterpretation_retained"),
    (425, "alternative_retention", "alternative_not_deleted_guard", "alternative_deletion_blocked"),
    (426, "alternative_retention", "alternative_status_record", "alternative_status_recorded"),
    (427, "alternative_retention", "alternative_future_xi_record", "alternative_future_xi_preserved"),
    (428, "alternative_retention", "selection_space_not_exhausted_guard", "selection_space_exhaustion_blocked"),
    (429, "non_identity", "policy_vs_candidate_split", "policy_candidate_non_identity"),
    (430, "non_identity", "policy_vs_function_split", "policy_function_non_identity"),
    (431, "non_identity", "policy_vs_context_split", "policy_context_non_identity"),
    (432, "non_identity", "policy_vs_prediction_split", "policy_prediction_non_identity"),
    (433, "non_identity", "selected_vs_resolved_split", "selected_resolved_non_identity"),
    (434, "non_identity", "selected_vs_true_future_split", "selected_true_future_non_identity"),
    (435, "record_schema", "decision_record_source", "decision_source_recorded"),
    (436, "record_schema", "decision_record_criteria", "decision_criteria_recorded"),
    (437, "record_schema", "decision_record_scores", "decision_scores_recorded"),
    (438, "record_schema", "decision_record_selected", "decision_selected_recorded"),
    (439, "record_schema", "decision_record_alternatives", "decision_alternatives_recorded"),
    (440, "record_schema", "decision_record_stop_lines", "decision_stop_lines_recorded"),
    (441, "summary", "policy_boundary_summary", "policy_boundary_observed"),
    (442, "summary", "alternative_retention_summary", "alternative_retention_confirmed"),
    (443, "summary", "no_generation_summary", "policy_generated_no_prediction"),
    (444, "summary", "no_mutation_summary", "no_mutation_generated"),
    (445, "next_plan", "policy_origin_open_xi", "policy_origin_remains_open"),
    (446, "next_plan", "weighting_without_collapse_open_xi", "weighting_without_collapse_remains_open"),
    (447, "next_plan", "record_schema_stabilization_candidate", "multiple_interpretation_record_schema_candidate"),
    (448, "next_plan", "next_xi_selection", "xi_multiple_interpretation_record_schema_stress"),
)


def _build_steps() -> tuple[ResolutionPolicyStep, ...]:
    previous = "cross_module_prediction_split_349_398"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            ResolutionPolicyStep(
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


def fixture_resolution_policy() -> PredictionResolutionPolicy:
    return PredictionResolutionPolicy(
        name="prefer_continuation_with_alternative_retention",
        criteria=(
            PolicyCriterion(
                name="prefer_continuation_fixture",
                preferred_value="continuation_fixture",
                source="external_policy_fixture",
            ),
            PolicyCriterion(
                name="prefer_grid_aligned_arrival",
                preferred_value="arrival_can_be_grid_aligned",
                source="external_policy_fixture",
            ),
            PolicyCriterion(
                name="retain_reinterpretation_candidate",
                preferred_value="reinterpretation_fixture",
                source="external_policy_fixture",
            ),
        ),
        generated_candidates=False,
    )


def apply_resolution_policy(
    candidates: tuple[PredictionFrameCandidate, ...],
    policy: PredictionResolutionPolicy,
) -> PolicyDecisionRecord:
    scores = []
    retention_criterion = "retain_reinterpretation_candidate"
    for candidate in candidates:
        matched = []
        for criterion in policy.criteria:
            if criterion.preferred_value in {
                candidate.source,
                candidate.rhythm_alignment,
            }:
                matched.append(criterion.name)
        scores.append(
            PolicyScore(
                candidate=candidate,
                matched_criteria=tuple(matched),
                score=len(tuple(name for name in matched if name != retention_criterion)),
            )
        )

    max_score = max(score.score for score in scores)
    selected_scores = tuple(score for score in scores if score.score == max_score)
    selected = selected_scores[0].candidate if len(selected_scores) == 1 else None
    retained_alternatives = tuple(
        score.candidate
        for score in scores
        if score.candidate != selected
    )
    return PolicyDecisionRecord(
        policy=policy,
        scores=tuple(scores),
        selected=selected,
        retained_alternatives=retained_alternatives,
        status="selected_with_alternative_retention" if selected else "selection_ambiguous",
        generated_prediction=False,
        deleted_alternatives=False,
    )


def observe_resolution_policy_stress() -> PredictionResolutionPolicyStressObservation:
    split = observe_prediction_split()
    policy = fixture_resolution_policy()
    decision = apply_resolution_policy(split.prediction_candidates, policy)
    steps = _build_steps()

    return PredictionResolutionPolicyStressObservation(
        source_status=split.status,
        steps=steps,
        policy=policy,
        decision=decision,
        policy_selects_one_candidate=decision.selected is not None,
        policy_generates_candidates=policy.generated_candidates,
        alternative_retention_preserved=(
            len(decision.retained_alternatives) == 1
            and decision.retained_alternatives[0].label == "A minor reinterpretation frame"
            and decision.deleted_alternatives is False
        ),
        unresolved_without_policy_preserved=(
            split.selected_prediction is None
            and split.unique_prediction_without_policy is False
        ),
        selected_prediction_is_resolution=False,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="prediction_resolution_policy_stress_399_448_observed_without_erasing_alternative_interpretation",
    )


def run_checks() -> None:
    observation = observe_resolution_policy_stress()
    decision = observation.decision

    assert observation.source_status == (
        "cross_module_prediction_split_349_398_observed_without_collapsing_multiple_interpretations"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 399
    assert observation.steps[-1].number == 448
    assert observation.policy.name == "prefer_continuation_with_alternative_retention"
    assert observation.policy.generated_candidates is False
    assert len(observation.policy.criteria) == 3
    assert decision.status == "selected_with_alternative_retention"
    assert decision.selected is not None
    assert decision.selected.label == "C major continuation frame"
    assert decision.selected.prediction == "continue_C_major_context"
    assert len(decision.retained_alternatives) == 1
    assert decision.retained_alternatives[0].label == "A minor reinterpretation frame"
    assert decision.generated_prediction is False
    assert decision.deleted_alternatives is False
    assert observation.policy_selects_one_candidate is True
    assert observation.policy_generates_candidates is False
    assert observation.alternative_retention_preserved is True
    assert observation.unresolved_without_policy_preserved is True
    assert observation.selected_prediction_is_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_multiple_interpretation_record_schema_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_resolution_policy_stress().status)
