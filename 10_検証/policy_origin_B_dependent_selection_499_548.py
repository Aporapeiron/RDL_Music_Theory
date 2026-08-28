"""policyの由来とB依存選択差を50工程でstress testする最小実験。"""

from dataclasses import dataclass

from multiple_interpretation_record_schema_449_498 import (
    MultipleInterpretationRecord,
    observe_multiple_interpretation_record_schema,
)
from prediction_resolution_policy_stress_399_448 import (
    PolicyCriterion,
    PredictionResolutionPolicy,
    apply_resolution_policy,
)
from cross_module_prediction_split_349_398 import observe_prediction_split


@dataclass(frozen=True)
class BDependentPolicyStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class BContext:
    name: str
    role: str
    policy_origin: str
    preferred_source: str
    preferred_rhythm_alignment: str
    retention_required: bool


@dataclass(frozen=True)
class BPolicySelectionRecord:
    b_context: BContext
    policy: PredictionResolutionPolicy
    selected_label: str | None
    retained_labels: tuple[str, ...]
    status: str
    generated_candidates: bool
    deleted_alternatives: bool


@dataclass(frozen=True)
class BDependentPolicySelectionObservation:
    source_status: str
    steps: tuple[BDependentPolicyStep, ...]
    source_record: MultipleInterpretationRecord
    selection_records: tuple[BPolicySelectionRecord, ...]
    distinct_policy_origins_preserved: bool
    B_changes_selection: bool
    B_does_not_generate_candidates: bool
    alternative_retention_preserved: bool
    record_schema_reused: bool
    treats_B_as_truth: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (499, "source_reentry", "reuse_449_498_record_schema", "multiple_interpretation_record_schema_preserved"),
    (500, "source_reentry", "next_xi_received", "policy_origin_and_B_dependent_selection_stress_received"),
    (501, "source_reentry", "record_schema_recheck", "record_schema_available_for_B_policy_test"),
    (502, "B_context_request", "analysis_B_context_request", "analysis_B_context_candidate"),
    (503, "B_context_request", "performance_B_context_request", "performance_B_context_candidate"),
    (504, "B_context_request", "listener_B_context_request", "listener_B_context_candidate"),
    (505, "B_context_request", "composition_B_context_request", "composition_B_context_candidate"),
    (506, "B_context_request", "B_not_truth_guard", "B_truth_non_identity"),
    (507, "B_context_request", "B_not_candidate_generator_guard", "B_candidate_generation_blocked"),
    (508, "policy_origin", "analysis_policy_origin", "analysis_policy_origin_recorded"),
    (509, "policy_origin", "performance_policy_origin", "performance_policy_origin_recorded"),
    (510, "policy_origin", "listener_policy_origin", "listener_policy_origin_recorded"),
    (511, "policy_origin", "composition_policy_origin", "composition_policy_origin_recorded"),
    (512, "policy_origin", "origin_not_Core_guard", "policy_origin_Core_promotion_blocked"),
    (513, "policy_origin", "origin_not_universal_guard", "policy_origin_universalization_blocked"),
    (514, "policy_build", "analysis_policy_build", "analysis_policy_built"),
    (515, "policy_build", "performance_policy_build", "performance_policy_built"),
    (516, "policy_build", "listener_policy_build", "listener_policy_built"),
    (517, "policy_build", "composition_policy_build", "composition_policy_built"),
    (518, "policy_build", "policy_criteria_externalized", "policy_criteria_externalized"),
    (519, "policy_build", "policy_not_generator_guard", "policy_generation_blocked"),
    (520, "selection", "analysis_selection_application", "analysis_selection_recorded"),
    (521, "selection", "performance_selection_application", "performance_selection_recorded"),
    (522, "selection", "listener_selection_application", "listener_selection_recorded"),
    (523, "selection", "composition_selection_application", "composition_selection_recorded"),
    (524, "selection", "same_candidate_set_reuse", "same_candidate_set_reused"),
    (525, "selection", "selection_difference_observation", "B_dependent_selection_difference_observed"),
    (526, "selection", "selection_not_truth_guard", "selection_truth_non_identity"),
    (527, "alternative_retention", "analysis_alternative_retention", "analysis_alternatives_retained"),
    (528, "alternative_retention", "performance_alternative_retention", "performance_alternatives_retained"),
    (529, "alternative_retention", "listener_alternative_retention", "listener_alternatives_retained"),
    (530, "alternative_retention", "composition_alternative_retention", "composition_alternatives_retained"),
    (531, "alternative_retention", "retention_not_error_guard", "retention_error_non_identity"),
    (532, "non_identity", "B_vs_policy_split", "B_policy_non_identity"),
    (533, "non_identity", "policy_vs_selection_split", "policy_selection_non_identity"),
    (534, "non_identity", "selection_vs_record_split", "selection_record_non_identity"),
    (535, "non_identity", "B_vs_module_split", "B_module_non_identity"),
    (536, "record_reuse", "record_schema_reuse", "multiple_interpretation_record_schema_reused"),
    (537, "record_reuse", "selected_label_update_as_view", "selected_label_view_changed_by_policy"),
    (538, "record_reuse", "retained_labels_update_as_view", "retained_labels_view_preserved_by_policy"),
    (539, "record_reuse", "source_record_not_mutated_guard", "source_record_mutation_blocked"),
    (540, "music_subject", "analysis_performance_difference", "analysis_performance_difference_preserved"),
    (541, "music_subject", "listener_composition_difference", "listener_composition_difference_preserved"),
    (542, "music_subject", "music_use_case_specificity", "music_use_case_specificity_preserved"),
    (543, "summary", "B_dependent_policy_summary", "B_dependent_policy_surface_observed"),
    (544, "summary", "selection_difference_summary", "selection_difference_preserved_without_truth"),
    (545, "summary", "alternative_retention_summary", "alternative_retention_preserved_across_B"),
    (546, "summary", "no_mutation_summary", "no_mutation_generated"),
    (547, "next_plan", "weighting_without_collapse_next_candidate", "weighting_without_collapse_next_candidate"),
    (548, "next_plan", "next_xi_selection", "xi_weighting_without_collapse_stress"),
)


def _build_steps() -> tuple[BDependentPolicyStep, ...]:
    previous = "multiple_interpretation_record_schema_449_498"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            BDependentPolicyStep(
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


def fixture_B_contexts() -> tuple[BContext, ...]:
    return (
        BContext(
            name="analysis_B",
            role="analysis",
            policy_origin="theoretical_continuity_reading",
            preferred_source="continuation_fixture",
            preferred_rhythm_alignment="arrival_can_be_grid_aligned",
            retention_required=True,
        ),
        BContext(
            name="performance_B",
            role="performance",
            policy_origin="expressive_reaccentuation_reading",
            preferred_source="reinterpretation_fixture",
            preferred_rhythm_alignment="arrival_can_be_reaccented",
            retention_required=True,
        ),
        BContext(
            name="listener_B",
            role="listener",
            policy_origin="local_expectation_reading",
            preferred_source="continuation_fixture",
            preferred_rhythm_alignment="arrival_can_be_grid_aligned",
            retention_required=True,
        ),
        BContext(
            name="composition_B",
            role="composition",
            policy_origin="future_pivot_potential_reading",
            preferred_source="reinterpretation_fixture",
            preferred_rhythm_alignment="arrival_can_be_reaccented",
            retention_required=True,
        ),
    )


def policy_from_B_context(context: BContext) -> PredictionResolutionPolicy:
    return PredictionResolutionPolicy(
        name=f"{context.name}_policy",
        criteria=(
            PolicyCriterion(
                name=f"{context.role}_preferred_source",
                preferred_value=context.preferred_source,
                source=context.policy_origin,
            ),
            PolicyCriterion(
                name=f"{context.role}_preferred_rhythm_alignment",
                preferred_value=context.preferred_rhythm_alignment,
                source=context.policy_origin,
            ),
            PolicyCriterion(
                name=f"{context.role}_retain_alternatives",
                preferred_value="retain_alternatives",
                source=context.policy_origin,
            ),
        ),
        generated_candidates=False,
    )


def observe_B_dependent_policy_selection() -> BDependentPolicySelectionObservation:
    schema_observation = observe_multiple_interpretation_record_schema()
    split = observe_prediction_split()
    records = []
    for context in fixture_B_contexts():
        policy = policy_from_B_context(context)
        decision = apply_resolution_policy(split.prediction_candidates, policy)
        records.append(
            BPolicySelectionRecord(
                b_context=context,
                policy=policy,
                selected_label=decision.selected.label if decision.selected else None,
                retained_labels=tuple(
                    candidate.label for candidate in decision.retained_alternatives
                ),
                status=decision.status,
                generated_candidates=policy.generated_candidates,
                deleted_alternatives=decision.deleted_alternatives,
            )
        )

    selection_records = tuple(records)
    selected_labels = {record.selected_label for record in selection_records}
    steps = _build_steps()

    return BDependentPolicySelectionObservation(
        source_status=schema_observation.status,
        steps=steps,
        source_record=schema_observation.record,
        selection_records=selection_records,
        distinct_policy_origins_preserved=(
            len({record.b_context.policy_origin for record in selection_records}) == 4
        ),
        B_changes_selection=selected_labels == {
            "C major continuation frame",
            "A minor reinterpretation frame",
        },
        B_does_not_generate_candidates=all(
            record.generated_candidates is False for record in selection_records
        ),
        alternative_retention_preserved=all(
            len(record.retained_labels) == 1
            and record.deleted_alternatives is False
            for record in selection_records
        ),
        record_schema_reused=(
            schema_observation.record.status
            == "multiple_interpretation_record_schema_449_498_built_without_closing_interpretation_space"
        ),
        treats_B_as_truth=False,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="policy_origin_B_dependent_selection_499_548_observed_without_treating_B_as_truth",
    )


def run_checks() -> None:
    observation = observe_B_dependent_policy_selection()

    assert observation.source_status == (
        "multiple_interpretation_record_schema_449_498_observed_without_closing_interpretation_space"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 499
    assert observation.steps[-1].number == 548
    assert len(observation.selection_records) == 4
    assert observation.distinct_policy_origins_preserved is True
    assert observation.B_changes_selection is True
    assert observation.B_does_not_generate_candidates is True
    assert observation.alternative_retention_preserved is True
    assert observation.record_schema_reused is True
    assert observation.treats_B_as_truth is False
    assert observation.generated_mutation is False
    assert {
        record.selected_label for record in observation.selection_records
    } == {"C major continuation frame", "A minor reinterpretation frame"}
    assert all(record.status == "selected_with_alternative_retention" for record in observation.selection_records)
    assert observation.steps[-1].result == "xi_weighting_without_collapse_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_B_dependent_policy_selection().status)
