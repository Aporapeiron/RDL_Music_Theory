"""commitment record後のtrace update境界を検査する最小実験。"""

from dataclasses import dataclass

from commitment_record_boundary_stress_2449_2498 import (
    CommitmentRecord,
    CommitmentRecordBoundaryBundle,
    observe_commitment_record_boundary,
)


@dataclass(frozen=True)
class PostCommitmentTraceUpdateStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class PostCommitmentTraceUpdate:
    source_record: CommitmentRecord
    update_kind: str
    update_content: str
    preserves_record_trace: bool
    preserves_interpretation_trace: bool
    preserves_conflict_trace: bool
    appends_trace: bool
    rewrites_history: bool
    deletes_alternative: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class PostCommitmentTraceUpdateBundle:
    source_bundle: CommitmentRecordBoundaryBundle
    trace_updates: tuple[PostCommitmentTraceUpdate, ...]
    contextual_updates: tuple[PostCommitmentTraceUpdate, ...]
    hearing_shift_updates: tuple[PostCommitmentTraceUpdate, ...]
    reference_updates: tuple[PostCommitmentTraceUpdate, ...]
    stop_lines: tuple[str, ...]
    generated_trace_update: bool
    generated_history_rewrite: bool
    generated_alternative_deletion: bool
    generated_resolution: bool
    status: str


@dataclass(frozen=True)
class PostCommitmentTraceUpdateObservation:
    source_status: str
    steps: tuple[PostCommitmentTraceUpdateStep, ...]
    bundle: PostCommitmentTraceUpdateBundle
    every_record_gets_trace_update: bool
    update_variety_preserved: bool
    record_interpretation_conflict_traces_preserved: bool
    update_appended_without_history_rewrite: bool
    no_resolution_or_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2499, "source_reentry", "reuse_2449_2498_commitment_record_boundary", "commitment_record_boundary_preserved"),
    (2500, "source_reentry", "next_xi_received", "post_commitment_trace_update_stress_received"),
    (2501, "source_reentry", "commitment_records_recheck", "commitment_records_available"),
    (2502, "update_request", "post_commitment_trace_update_request", "post_commitment_trace_update_candidate"),
    (2503, "update_request", "trace_update_not_history_rewrite_guard", "history_rewrite_non_identity_preserved"),
    (2504, "update_request", "trace_update_not_alternative_deletion_guard", "alternative_deletion_blocked"),
    (2505, "update_request", "trace_update_not_resolution_guard", "resolution_non_identity_preserved"),
    (2506, "update_layer", "trace_update_generation", "trace_updates_recorded"),
    (2507, "update_layer", "contextual_record_trace_update", "contextual_record_trace_update_recorded"),
    (2508, "update_layer", "hearing_shift_record_trace_update", "hearing_shift_record_trace_update_recorded"),
    (2509, "update_layer", "reference_record_trace_update", "reference_record_trace_update_recorded"),
    (2510, "update_layer", "appends_trace_true", "appends_trace_true_recorded"),
    (2511, "update_layer", "rewrites_history_false", "rewrites_history_false_recorded"),
    (2512, "update_layer", "deletes_alternative_false", "deletes_alternative_false_recorded"),
    (2513, "update_content_layer", "contextual_trace_append_content", "contextual_trace_append_content_recorded"),
    (2514, "update_content_layer", "hearing_shift_trace_append_content", "hearing_shift_trace_append_content_recorded"),
    (2515, "update_content_layer", "reference_trace_append_content", "reference_trace_append_content_recorded"),
    (2516, "update_content_layer", "record_trace_carry", "record_trace_carried"),
    (2517, "update_content_layer", "interpretation_trace_carry", "interpretation_trace_carried"),
    (2518, "update_content_layer", "conflict_trace_carry", "conflict_trace_carried"),
    (2519, "partition_layer", "contextual_trace_update_partition", "contextual_trace_update_partition_recorded"),
    (2520, "partition_layer", "hearing_shift_trace_update_partition", "hearing_shift_trace_update_partition_recorded"),
    (2521, "partition_layer", "reference_trace_update_partition", "reference_trace_update_partition_recorded"),
    (2522, "partition_layer", "trace_update_partition_not_rewrite_guard", "partition_rewrite_non_identity"),
    (2523, "partition_layer", "trace_update_partition_not_solution_guard", "partition_solution_non_identity"),
    (2524, "update_view", "post_commitment_trace_update_view", "post_commitment_trace_update_view_created"),
    (2525, "update_view", "contextual_trace_update_view", "contextual_trace_update_view_created"),
    (2526, "update_view", "hearing_shift_trace_update_view", "hearing_shift_trace_update_view_created"),
    (2527, "update_view", "reference_trace_update_view", "reference_trace_update_view_created"),
    (2528, "bundle", "post_commitment_trace_update_bundle_creation", "post_commitment_trace_update_bundle_created"),
    (2529, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2530, "bundle", "stop_lines_carry", "post_commitment_trace_update_stop_lines_carried"),
    (2531, "bundle", "generated_trace_update_true", "generated_trace_update_true_recorded"),
    (2532, "bundle", "generated_history_rewrite_false", "generated_history_rewrite_false_recorded"),
    (2533, "bundle", "generated_alternative_deletion_false", "generated_alternative_deletion_false_recorded"),
    (2534, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (2535, "integrity", "every_record_gets_trace_update_check", "every_record_gets_trace_update_confirmed"),
    (2536, "integrity", "update_variety_preservation_check", "update_variety_preservation_confirmed"),
    (2537, "integrity", "record_interpretation_conflict_trace_check", "record_interpretation_conflict_trace_confirmed"),
    (2538, "integrity", "update_without_history_rewrite_check", "update_without_history_rewrite_confirmed"),
    (2539, "integrity", "no_alternative_deletion_check", "no_alternative_deletion_confirmed"),
    (2540, "integrity", "no_resolution_check", "no_resolution_confirmed"),
    (2541, "non_identity", "trace_update_vs_history_rewrite_split", "trace_update_history_rewrite_non_identity"),
    (2542, "non_identity", "trace_update_vs_deletion_split", "trace_update_deletion_non_identity"),
    (2543, "non_identity", "trace_update_vs_resolution_split", "trace_update_resolution_non_identity"),
    (2544, "music_subject", "trace_update_as_after_adoption_memory", "after_adoption_memory_preserved"),
    (2545, "music_subject", "contextual_update_as_phrase_memory_append", "phrase_memory_append_preserved"),
    (2546, "music_subject", "hearing_shift_update_as_weight_memory_append", "weight_memory_append_preserved"),
    (2547, "summary", "post_commitment_trace_update_summary", "post_commitment_trace_update_observed"),
    (2548, "next_plan", "next_xi_selection", "xi_post_commitment_alternative_retention_stress"),
)


def _build_steps() -> tuple[PostCommitmentTraceUpdateStep, ...]:
    previous = "commitment_record_boundary_2449_2498"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(PostCommitmentTraceUpdateStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _trace_update(record: CommitmentRecord) -> PostCommitmentTraceUpdate:
    if record.record_kind == "contextual_commitment_record":
        kind = "contextual_record_trace_update"
        content = "append_phrase_context_trace_without_rewriting_record"
    elif record.record_kind == "hearing_shift_commitment_record":
        kind = "hearing_shift_record_trace_update"
        content = "append_weighted_reading_trace_without_deleting_alternatives"
    else:
        kind = "reference_record_trace_update"
        content = "append_reference_axis_trace_without_resolving_conflict"

    return PostCommitmentTraceUpdate(
        source_record=record,
        update_kind=kind,
        update_content=content,
        preserves_record_trace=True,
        preserves_interpretation_trace=record.preserves_interpretation_trace,
        preserves_conflict_trace=record.preserves_conflict_trace,
        appends_trace=True,
        rewrites_history=False,
        deletes_alternative=False,
        resolves_conflict=False,
        status="post_commitment_trace_update_appended_without_history_rewrite",
    )


def build_post_commitment_trace_update_bundle(
    source: CommitmentRecordBoundaryBundle,
) -> PostCommitmentTraceUpdateBundle:
    updates = tuple(_trace_update(record) for record in source.records)
    contextual = tuple(update for update in updates if update.update_kind == "contextual_record_trace_update")
    hearing_shift = tuple(update for update in updates if update.update_kind == "hearing_shift_record_trace_update")
    reference = tuple(update for update in updates if update.update_kind == "reference_record_trace_update")
    return PostCommitmentTraceUpdateBundle(
        source_bundle=source,
        trace_updates=updates,
        contextual_updates=contextual,
        hearing_shift_updates=hearing_shift,
        reference_updates=reference,
        stop_lines=(
            "trace_update_not_history_rewrite",
            "trace_update_not_alternative_deletion",
            "trace_update_not_resolution",
            "trace_update_partition_not_solution",
            "trace_update_not_final_judgement",
        ),
        generated_trace_update=True,
        generated_history_rewrite=False,
        generated_alternative_deletion=False,
        generated_resolution=False,
        status="post_commitment_trace_update_bundle_2499_2548_built_without_history_rewrite",
    )


def observe_post_commitment_trace_update() -> PostCommitmentTraceUpdateObservation:
    source = observe_commitment_record_boundary()
    bundle = build_post_commitment_trace_update_bundle(source.bundle)
    steps = _build_steps()

    return PostCommitmentTraceUpdateObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_record_gets_trace_update=(len(bundle.trace_updates) == len(source.bundle.records)),
        update_variety_preserved=(
            len(bundle.contextual_updates) == 1
            and len(bundle.hearing_shift_updates) == 1
            and len(bundle.reference_updates) == 1
        ),
        record_interpretation_conflict_traces_preserved=all(
            update.preserves_record_trace
            and update.preserves_interpretation_trace
            and update.preserves_conflict_trace
            for update in bundle.trace_updates
        ),
        update_appended_without_history_rewrite=(
            bundle.generated_trace_update is True
            and bundle.generated_history_rewrite is False
            and all(update.appends_trace and not update.rewrites_history for update in bundle.trace_updates)
        ),
        no_resolution_or_deletion=(
            bundle.generated_resolution is False
            and bundle.generated_alternative_deletion is False
            and all(not update.resolves_conflict and not update.deletes_alternative for update in bundle.trace_updates)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="post_commitment_trace_update_2499_2548_observed_without_history_rewrite_or_deletion",
    )


def run_checks() -> None:
    observation = observe_post_commitment_trace_update()
    bundle = observation.bundle

    assert observation.source_status == (
        "commitment_record_boundary_2449_2498_observed_without_final_judgement_or_resolution"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2499
    assert observation.steps[-1].number == 2548
    assert observation.every_record_gets_trace_update is True
    assert observation.update_variety_preserved is True
    assert observation.record_interpretation_conflict_traces_preserved is True
    assert observation.update_appended_without_history_rewrite is True
    assert observation.no_resolution_or_deletion is True
    assert len(bundle.trace_updates) == 3
    assert len(bundle.contextual_updates) == 1
    assert len(bundle.hearing_shift_updates) == 1
    assert len(bundle.reference_updates) == 1
    assert bundle.generated_trace_update is True
    assert bundle.generated_history_rewrite is False
    assert bundle.generated_alternative_deletion is False
    assert bundle.generated_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_post_commitment_alternative_retention_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_post_commitment_trace_update().status)
