"""interpretation commitment attemptからcommitment recordを生成する境界を検査する最小実験。"""

from dataclasses import dataclass

from interpretation_commitment_attempt_stress_2399_2448 import (
    InterpretationCommitmentAttempt,
    InterpretationCommitmentAttemptBundle,
    observe_interpretation_commitment_attempt,
)


@dataclass(frozen=True)
class CommitmentRecordBoundaryStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class CommitmentRecord:
    source_attempt: InterpretationCommitmentAttempt
    record_kind: str
    record_content: str
    preserves_attempt_trace: bool
    preserves_interpretation_trace: bool
    preserves_conflict_trace: bool
    commits_record: bool
    commits_final_judgement: bool
    resolves_conflict: bool
    deletes_alternative: bool
    status: str


@dataclass(frozen=True)
class CommitmentRecordBoundaryBundle:
    source_bundle: InterpretationCommitmentAttemptBundle
    records: tuple[CommitmentRecord, ...]
    contextual_records: tuple[CommitmentRecord, ...]
    hearing_shift_records: tuple[CommitmentRecord, ...]
    reference_records: tuple[CommitmentRecord, ...]
    stop_lines: tuple[str, ...]
    generated_commitment_record: bool
    generated_final_judgement: bool
    generated_resolution: bool
    generated_alternative_deletion: bool
    status: str


@dataclass(frozen=True)
class CommitmentRecordBoundaryObservation:
    source_status: str
    steps: tuple[CommitmentRecordBoundaryStep, ...]
    bundle: CommitmentRecordBoundaryBundle
    every_attempt_gets_record: bool
    record_variety_preserved: bool
    attempt_interpretation_conflict_traces_preserved: bool
    record_generated_without_final_judgement: bool
    no_resolution_or_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2449, "source_reentry", "reuse_2399_2448_interpretation_commitment_attempt", "interpretation_commitment_attempt_preserved"),
    (2450, "source_reentry", "next_xi_received", "commitment_record_boundary_stress_received"),
    (2451, "source_reentry", "commitment_attempts_recheck", "commitment_attempts_available"),
    (2452, "record_request", "commitment_record_request", "commitment_record_candidate"),
    (2453, "record_request", "record_not_final_judgement_guard", "record_final_judgement_non_identity_preserved"),
    (2454, "record_request", "record_not_resolution_guard", "record_resolution_non_identity_preserved"),
    (2455, "record_request", "record_not_alternative_deletion_guard", "alternative_deletion_blocked"),
    (2456, "record_layer", "commitment_record_generation", "commitment_records_recorded"),
    (2457, "record_layer", "contextual_commitment_record", "contextual_commitment_record_recorded"),
    (2458, "record_layer", "hearing_shift_commitment_record", "hearing_shift_commitment_record_recorded"),
    (2459, "record_layer", "reference_commitment_record", "reference_commitment_record_recorded"),
    (2460, "record_layer", "commits_record_true", "commits_record_true_recorded"),
    (2461, "record_layer", "commits_final_judgement_false", "commits_final_judgement_false_recorded"),
    (2462, "record_layer", "resolves_conflict_false", "resolves_conflict_false_recorded"),
    (2463, "record_content_layer", "contextual_adoption_record_content", "contextual_adoption_record_content_recorded"),
    (2464, "record_content_layer", "weighted_reading_record_content", "weighted_reading_record_content_recorded"),
    (2465, "record_content_layer", "reference_axis_record_content", "reference_axis_record_content_recorded"),
    (2466, "record_content_layer", "attempt_trace_carry", "attempt_trace_carried"),
    (2467, "record_content_layer", "interpretation_trace_carry", "interpretation_trace_carried"),
    (2468, "record_content_layer", "conflict_trace_carry", "conflict_trace_carried"),
    (2469, "partition_layer", "contextual_record_partition", "contextual_record_partition_recorded"),
    (2470, "partition_layer", "hearing_shift_record_partition", "hearing_shift_record_partition_recorded"),
    (2471, "partition_layer", "reference_record_partition", "reference_record_partition_recorded"),
    (2472, "partition_layer", "record_partition_not_judgement_guard", "partition_judgement_non_identity"),
    (2473, "partition_layer", "record_partition_not_solution_guard", "partition_solution_non_identity"),
    (2474, "record_view", "commitment_record_view", "commitment_record_view_created"),
    (2475, "record_view", "contextual_record_view", "contextual_record_view_created"),
    (2476, "record_view", "hearing_shift_record_view", "hearing_shift_record_view_created"),
    (2477, "record_view", "reference_record_view", "reference_record_view_created"),
    (2478, "bundle", "commitment_record_boundary_bundle_creation", "commitment_record_boundary_bundle_created"),
    (2479, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2480, "bundle", "stop_lines_carry", "commitment_record_boundary_stop_lines_carried"),
    (2481, "bundle", "generated_commitment_record_true", "generated_commitment_record_true_recorded"),
    (2482, "bundle", "generated_final_judgement_false", "generated_final_judgement_false_recorded"),
    (2483, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (2484, "bundle", "generated_alternative_deletion_false", "generated_alternative_deletion_false_recorded"),
    (2485, "integrity", "every_attempt_gets_record_check", "every_attempt_gets_record_confirmed"),
    (2486, "integrity", "record_variety_preservation_check", "record_variety_preservation_confirmed"),
    (2487, "integrity", "attempt_interpretation_conflict_trace_check", "attempt_interpretation_conflict_trace_confirmed"),
    (2488, "integrity", "record_without_final_judgement_check", "record_without_final_judgement_confirmed"),
    (2489, "integrity", "no_resolution_check", "no_resolution_confirmed"),
    (2490, "integrity", "no_alternative_deletion_check", "no_alternative_deletion_confirmed"),
    (2491, "non_identity", "record_vs_final_judgement_split", "record_final_judgement_non_identity"),
    (2492, "non_identity", "record_vs_resolution_split", "record_resolution_non_identity"),
    (2493, "non_identity", "record_vs_solution_split", "record_solution_non_identity"),
    (2494, "music_subject", "record_as_adopted_heard_meaning_trace", "adopted_heard_meaning_trace_preserved"),
    (2495, "music_subject", "contextual_record_as_phrase_level_trace", "phrase_level_trace_preserved"),
    (2496, "music_subject", "hearing_shift_record_as_weighted_reading_trace", "weighted_reading_trace_preserved"),
    (2497, "summary", "commitment_record_boundary_summary", "commitment_record_boundary_observed"),
    (2498, "next_plan", "next_xi_selection", "xi_post_commitment_trace_update_stress"),
)


def _build_steps() -> tuple[CommitmentRecordBoundaryStep, ...]:
    previous = "interpretation_commitment_attempt_2399_2448"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(CommitmentRecordBoundaryStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _record(attempt: InterpretationCommitmentAttempt) -> CommitmentRecord:
    if attempt.attempt_kind == "contextual_commitment_attempt":
        kind = "contextual_commitment_record"
        content = "phrase_context_adoption_recorded_without_final_judgement"
    elif attempt.attempt_kind == "hearing_shift_commitment_attempt":
        kind = "hearing_shift_commitment_record"
        content = "weighted_reading_adoption_recorded_without_resolution"
    else:
        kind = "reference_commitment_record"
        content = "reference_axis_adoption_recorded_without_deleting_alternatives"

    return CommitmentRecord(
        source_attempt=attempt,
        record_kind=kind,
        record_content=content,
        preserves_attempt_trace=True,
        preserves_interpretation_trace=attempt.preserves_interpretation_trace,
        preserves_conflict_trace=attempt.preserves_conflict_trace,
        commits_record=True,
        commits_final_judgement=False,
        resolves_conflict=False,
        deletes_alternative=False,
        status="commitment_record_recorded_without_final_judgement",
    )


def build_commitment_record_boundary_bundle(
    source: InterpretationCommitmentAttemptBundle,
) -> CommitmentRecordBoundaryBundle:
    records = tuple(_record(attempt) for attempt in source.attempts)
    contextual = tuple(record for record in records if record.record_kind == "contextual_commitment_record")
    hearing_shift = tuple(record for record in records if record.record_kind == "hearing_shift_commitment_record")
    reference = tuple(record for record in records if record.record_kind == "reference_commitment_record")
    return CommitmentRecordBoundaryBundle(
        source_bundle=source,
        records=records,
        contextual_records=contextual,
        hearing_shift_records=hearing_shift,
        reference_records=reference,
        stop_lines=(
            "record_not_final_judgement",
            "record_not_resolution",
            "record_not_alternative_deletion",
            "record_partition_not_solution",
            "record_not_final_truth",
        ),
        generated_commitment_record=True,
        generated_final_judgement=False,
        generated_resolution=False,
        generated_alternative_deletion=False,
        status="commitment_record_boundary_bundle_2449_2498_built_without_final_judgement",
    )


def observe_commitment_record_boundary() -> CommitmentRecordBoundaryObservation:
    source = observe_interpretation_commitment_attempt()
    bundle = build_commitment_record_boundary_bundle(source.bundle)
    steps = _build_steps()

    return CommitmentRecordBoundaryObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_attempt_gets_record=(len(bundle.records) == len(source.bundle.attempts)),
        record_variety_preserved=(
            len(bundle.contextual_records) == 1
            and len(bundle.hearing_shift_records) == 1
            and len(bundle.reference_records) == 1
        ),
        attempt_interpretation_conflict_traces_preserved=all(
            record.preserves_attempt_trace
            and record.preserves_interpretation_trace
            and record.preserves_conflict_trace
            for record in bundle.records
        ),
        record_generated_without_final_judgement=(
            bundle.generated_commitment_record is True
            and bundle.generated_final_judgement is False
            and all(record.commits_record and not record.commits_final_judgement for record in bundle.records)
        ),
        no_resolution_or_deletion=(
            bundle.generated_resolution is False
            and bundle.generated_alternative_deletion is False
            and all(not record.resolves_conflict and not record.deletes_alternative for record in bundle.records)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="commitment_record_boundary_2449_2498_observed_without_final_judgement_or_resolution",
    )


def run_checks() -> None:
    observation = observe_commitment_record_boundary()
    bundle = observation.bundle

    assert observation.source_status == (
        "interpretation_commitment_attempt_2399_2448_observed_without_record_or_verdict"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2449
    assert observation.steps[-1].number == 2498
    assert observation.every_attempt_gets_record is True
    assert observation.record_variety_preserved is True
    assert observation.attempt_interpretation_conflict_traces_preserved is True
    assert observation.record_generated_without_final_judgement is True
    assert observation.no_resolution_or_deletion is True
    assert len(bundle.records) == 3
    assert len(bundle.contextual_records) == 1
    assert len(bundle.hearing_shift_records) == 1
    assert len(bundle.reference_records) == 1
    assert bundle.generated_commitment_record is True
    assert bundle.generated_final_judgement is False
    assert bundle.generated_resolution is False
    assert bundle.generated_alternative_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_post_commitment_trace_update_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_commitment_record_boundary().status)
