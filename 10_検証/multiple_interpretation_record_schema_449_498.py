"""複数解釈を保持するrecord schemaを50工程でstress testする最小実験。"""

from dataclasses import dataclass

from prediction_resolution_policy_stress_399_448 import (
    PolicyDecisionRecord,
    PolicyScore,
    observe_resolution_policy_stress,
)


@dataclass(frozen=True)
class InterpretationRecordStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class InterpretationRecordEntry:
    label: str
    role: str
    prediction: str
    harmonic_reading: str
    rhythm_alignment: str
    score: int
    matched_criteria: tuple[str, ...]
    retained_for: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class MultipleInterpretationRecord:
    source_status: str
    policy_name: str
    entries: tuple[InterpretationRecordEntry, ...]
    selected_label: str | None
    retained_labels: tuple[str, ...]
    stop_lines: tuple[str, ...]
    next_xi_candidates: tuple[str, ...]
    generated_resolution: bool
    deleted_alternatives: bool
    status: str


@dataclass(frozen=True)
class MultipleInterpretationRecordSchemaObservation:
    source_status: str
    steps: tuple[InterpretationRecordStep, ...]
    record: MultipleInterpretationRecord
    selected_entry_preserved: bool
    alternative_entry_preserved: bool
    schema_keeps_policy_trace: bool
    schema_keeps_stop_lines: bool
    schema_generates_resolution: bool
    schema_deletes_alternatives: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (449, "source_reentry", "reuse_399_448_policy_decision", "policy_decision_result_preserved"),
    (450, "source_reentry", "next_xi_received", "multiple_interpretation_record_schema_stress_received"),
    (451, "source_reentry", "decision_record_recheck", "decision_record_available"),
    (452, "schema_request", "record_schema_request", "multiple_interpretation_record_schema_candidate"),
    (453, "schema_request", "schema_not_resolution_guard", "schema_resolution_generation_blocked"),
    (454, "schema_request", "schema_not_prediction_generator_guard", "schema_prediction_generation_blocked"),
    (455, "schema_request", "schema_not_Core_guard", "schema_Core_promotion_blocked"),
    (456, "required_fields", "source_status_field", "source_status_field_recorded"),
    (457, "required_fields", "policy_name_field", "policy_name_field_recorded"),
    (458, "required_fields", "entry_collection_field", "entry_collection_field_recorded"),
    (459, "required_fields", "selected_label_field", "selected_label_field_recorded"),
    (460, "required_fields", "retained_labels_field", "retained_labels_field_recorded"),
    (461, "required_fields", "stop_lines_field", "stop_lines_field_recorded"),
    (462, "required_fields", "next_xi_candidates_field", "next_xi_candidates_field_recorded"),
    (463, "selected_entry", "selected_entry_creation", "selected_entry_created"),
    (464, "selected_entry", "selected_entry_role_marking", "selected_role_marked_without_resolution"),
    (465, "selected_entry", "selected_entry_score_trace", "selected_score_trace_recorded"),
    (466, "selected_entry", "selected_entry_criteria_trace", "selected_criteria_trace_recorded"),
    (467, "selected_entry", "selected_entry_not_truth_guard", "selected_truth_non_identity"),
    (468, "alternative_entry", "alternative_entry_creation", "alternative_entry_created"),
    (469, "alternative_entry", "alternative_entry_role_marking", "alternative_role_marked_as_retained"),
    (470, "alternative_entry", "alternative_entry_score_trace", "alternative_score_trace_recorded"),
    (471, "alternative_entry", "alternative_entry_criteria_trace", "alternative_criteria_trace_recorded"),
    (472, "alternative_entry", "alternative_not_error_guard", "alternative_error_non_identity"),
    (473, "retention_purpose", "reinterpretation_future_xi", "reinterpretation_future_xi_recorded"),
    (474, "retention_purpose", "policy_comparison_future_xi", "policy_comparison_future_xi_recorded"),
    (475, "retention_purpose", "context_shift_future_xi", "context_shift_future_xi_recorded"),
    (476, "retention_purpose", "retention_not_deletion_guard", "retention_deletion_blocked"),
    (477, "stop_lines", "selected_not_resolved_future_stop", "selected_resolved_future_stop_recorded"),
    (478, "stop_lines", "score_not_probability_stop", "score_probability_stop_recorded"),
    (479, "stop_lines", "policy_not_generator_stop", "policy_generator_stop_recorded"),
    (480, "stop_lines", "alternative_not_error_stop", "alternative_error_stop_recorded"),
    (481, "stop_lines", "record_not_Core_stop", "record_Core_stop_recorded"),
    (482, "schema_integrity", "entry_count_check", "two_entries_preserved"),
    (483, "schema_integrity", "selected_label_check", "selected_label_matches_entry"),
    (484, "schema_integrity", "retained_label_check", "retained_label_matches_entry"),
    (485, "schema_integrity", "policy_trace_check", "policy_trace_preserved"),
    (486, "schema_integrity", "no_resolution_generation_check", "no_resolution_generated"),
    (487, "schema_integrity", "no_alternative_deletion_check", "no_alternative_deleted"),
    (488, "music_subject", "music_ambiguity_preservation", "music_ambiguity_preserved"),
    (489, "music_subject", "analysis_generation_split", "analysis_generation_split_preserved"),
    (490, "music_subject", "performance_policy_opening", "performance_policy_left_open"),
    (491, "music_subject", "listener_B_policy_opening", "listener_B_policy_left_open"),
    (492, "summary", "record_schema_summary", "record_schema_observed"),
    (493, "summary", "selection_trace_summary", "selection_trace_observed"),
    (494, "summary", "alternative_trace_summary", "alternative_trace_observed"),
    (495, "summary", "no_mutation_summary", "no_mutation_generated"),
    (496, "next_plan", "record_schema_stabilization_limit", "record_schema_not_finalized"),
    (497, "next_plan", "policy_origin_next_candidate", "policy_origin_next_candidate_preserved"),
    (498, "next_plan", "next_xi_selection", "xi_policy_origin_and_B_dependent_selection_stress"),
)


def _build_steps() -> tuple[InterpretationRecordStep, ...]:
    previous = "prediction_resolution_policy_stress_399_448"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            InterpretationRecordStep(
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


def _entry_from_score(
    score: PolicyScore,
    decision: PolicyDecisionRecord,
) -> InterpretationRecordEntry:
    candidate = score.candidate
    selected = decision.selected == candidate
    if selected:
        role = "selected"
        retained_for = ("current_policy_path",)
        status = "selected_without_resolving_future"
    else:
        role = "retained_alternative"
        retained_for = (
            "future_reinterpretation",
            "policy_comparison",
            "context_shift_test",
        )
        status = "retained_without_error_classification"

    return InterpretationRecordEntry(
        label=candidate.label,
        role=role,
        prediction=candidate.prediction,
        harmonic_reading=candidate.harmonic_reading,
        rhythm_alignment=candidate.rhythm_alignment,
        score=score.score,
        matched_criteria=score.matched_criteria,
        retained_for=retained_for,
        status=status,
    )


def build_multiple_interpretation_record(
    decision: PolicyDecisionRecord,
    source_status: str,
) -> MultipleInterpretationRecord:
    entries = tuple(_entry_from_score(score, decision) for score in decision.scores)
    selected_label = decision.selected.label if decision.selected is not None else None
    retained_labels = tuple(candidate.label for candidate in decision.retained_alternatives)
    return MultipleInterpretationRecord(
        source_status=source_status,
        policy_name=decision.policy.name,
        entries=entries,
        selected_label=selected_label,
        retained_labels=retained_labels,
        stop_lines=(
            "selected_prediction_not_resolved_future",
            "score_not_probability",
            "policy_not_generator",
            "alternative_not_error",
            "record_not_Core_primitive",
        ),
        next_xi_candidates=(
            "policy_origin_for_prediction_selection",
            "weighting_without_collapse",
            "listener_B_dependent_policy",
            "performer_B_dependent_policy",
        ),
        generated_resolution=False,
        deleted_alternatives=False,
        status="multiple_interpretation_record_schema_449_498_built_without_closing_interpretation_space",
    )


def observe_multiple_interpretation_record_schema() -> MultipleInterpretationRecordSchemaObservation:
    policy_observation = observe_resolution_policy_stress()
    record = build_multiple_interpretation_record(
        policy_observation.decision,
        policy_observation.status,
    )
    steps = _build_steps()
    selected_entries = tuple(entry for entry in record.entries if entry.role == "selected")
    alternative_entries = tuple(
        entry for entry in record.entries if entry.role == "retained_alternative"
    )

    return MultipleInterpretationRecordSchemaObservation(
        source_status=policy_observation.status,
        steps=steps,
        record=record,
        selected_entry_preserved=(
            len(selected_entries) == 1
            and selected_entries[0].label == "C major continuation frame"
            and selected_entries[0].status == "selected_without_resolving_future"
        ),
        alternative_entry_preserved=(
            len(alternative_entries) == 1
            and alternative_entries[0].label == "A minor reinterpretation frame"
            and "future_reinterpretation" in alternative_entries[0].retained_for
        ),
        schema_keeps_policy_trace=(
            record.policy_name == "prefer_continuation_with_alternative_retention"
            and all(entry.matched_criteria for entry in record.entries)
        ),
        schema_keeps_stop_lines=(
            "selected_prediction_not_resolved_future" in record.stop_lines
            and "alternative_not_error" in record.stop_lines
            and "record_not_Core_primitive" in record.stop_lines
        ),
        schema_generates_resolution=record.generated_resolution,
        schema_deletes_alternatives=record.deleted_alternatives,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="multiple_interpretation_record_schema_449_498_observed_without_closing_interpretation_space",
    )


def run_checks() -> None:
    observation = observe_multiple_interpretation_record_schema()
    record = observation.record

    assert observation.source_status == (
        "prediction_resolution_policy_stress_399_448_observed_without_erasing_alternative_interpretation"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 449
    assert observation.steps[-1].number == 498
    assert record.status == (
        "multiple_interpretation_record_schema_449_498_built_without_closing_interpretation_space"
    )
    assert len(record.entries) == 2
    assert record.selected_label == "C major continuation frame"
    assert record.retained_labels == ("A minor reinterpretation frame",)
    assert observation.selected_entry_preserved is True
    assert observation.alternative_entry_preserved is True
    assert observation.schema_keeps_policy_trace is True
    assert observation.schema_keeps_stop_lines is True
    assert observation.schema_generates_resolution is False
    assert observation.schema_deletes_alternatives is False
    assert record.generated_resolution is False
    assert record.deleted_alternatives is False
    assert "policy_origin_for_prediction_selection" in record.next_xi_candidates
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_policy_origin_and_B_dependent_selection_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_multiple_interpretation_record_schema().status)
