"""post commitment後のalternative retention境界を検査する最小実験。"""

from dataclasses import dataclass

from post_commitment_trace_update_stress_2499_2548 import (
    PostCommitmentTraceUpdate,
    PostCommitmentTraceUpdateBundle,
    observe_post_commitment_trace_update,
)


@dataclass(frozen=True)
class PostCommitmentAlternativeRetentionStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class PostCommitmentAlternativeState:
    source_update: PostCommitmentTraceUpdate
    retention_kind: str
    retained_as: str
    preserves_update_trace: bool
    preserves_record_trace: bool
    preserves_conflict_trace: bool
    keeps_alternative_available: bool
    deletes_alternative: bool
    rewrites_commitment: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class PostCommitmentAlternativeRetentionBundle:
    source_bundle: PostCommitmentTraceUpdateBundle
    retained_alternatives: tuple[PostCommitmentAlternativeState, ...]
    contextual_alternatives: tuple[PostCommitmentAlternativeState, ...]
    hearing_shift_alternatives: tuple[PostCommitmentAlternativeState, ...]
    reference_alternatives: tuple[PostCommitmentAlternativeState, ...]
    stop_lines: tuple[str, ...]
    generated_retention: bool
    generated_alternative_deletion: bool
    generated_commitment_rewrite: bool
    generated_resolution: bool
    status: str


@dataclass(frozen=True)
class PostCommitmentAlternativeRetentionObservation:
    source_status: str
    steps: tuple[PostCommitmentAlternativeRetentionStep, ...]
    bundle: PostCommitmentAlternativeRetentionBundle
    every_update_gets_retention_state: bool
    retention_variety_preserved: bool
    update_record_conflict_traces_preserved: bool
    alternatives_retained_without_deletion: bool
    no_rewrite_or_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2549, "source_reentry", "reuse_2499_2548_post_commitment_trace_update", "post_commitment_trace_update_preserved"),
    (2550, "source_reentry", "next_xi_received", "post_commitment_alternative_retention_stress_received"),
    (2551, "source_reentry", "trace_updates_recheck", "trace_updates_available"),
    (2552, "retention_request", "post_commitment_alternative_retention_request", "post_commitment_alternative_retention_candidate"),
    (2553, "retention_request", "retention_not_deletion_guard", "alternative_deletion_non_identity_preserved"),
    (2554, "retention_request", "retention_not_commitment_rewrite_guard", "commitment_rewrite_blocked"),
    (2555, "retention_request", "retention_not_resolution_guard", "resolution_non_identity_preserved"),
    (2556, "retention_layer", "alternative_retention_state_generation", "alternative_retention_states_recorded"),
    (2557, "retention_layer", "contextual_alternative_retention", "contextual_alternative_retention_recorded"),
    (2558, "retention_layer", "hearing_shift_alternative_retention", "hearing_shift_alternative_retention_recorded"),
    (2559, "retention_layer", "reference_alternative_retention", "reference_alternative_retention_recorded"),
    (2560, "retention_layer", "keeps_alternative_available_true", "keeps_alternative_available_true_recorded"),
    (2561, "retention_layer", "deletes_alternative_false", "deletes_alternative_false_recorded"),
    (2562, "retention_layer", "rewrites_commitment_false", "rewrites_commitment_false_recorded"),
    (2563, "retention_content_layer", "latent_contextual_alternative_content", "latent_contextual_alternative_content_recorded"),
    (2564, "retention_content_layer", "latent_hearing_shift_alternative_content", "latent_hearing_shift_alternative_content_recorded"),
    (2565, "retention_content_layer", "active_reference_alternative_content", "active_reference_alternative_content_recorded"),
    (2566, "retention_content_layer", "update_trace_carry", "update_trace_carried"),
    (2567, "retention_content_layer", "record_trace_carry", "record_trace_carried"),
    (2568, "retention_content_layer", "conflict_trace_carry", "conflict_trace_carried"),
    (2569, "partition_layer", "contextual_alternative_partition", "contextual_alternative_partition_recorded"),
    (2570, "partition_layer", "hearing_shift_alternative_partition", "hearing_shift_alternative_partition_recorded"),
    (2571, "partition_layer", "reference_alternative_partition", "reference_alternative_partition_recorded"),
    (2572, "partition_layer", "retention_partition_not_deletion_guard", "partition_deletion_non_identity"),
    (2573, "partition_layer", "retention_partition_not_solution_guard", "partition_solution_non_identity"),
    (2574, "retention_view", "post_commitment_alternative_retention_view", "post_commitment_alternative_retention_view_created"),
    (2575, "retention_view", "contextual_alternative_view", "contextual_alternative_view_created"),
    (2576, "retention_view", "hearing_shift_alternative_view", "hearing_shift_alternative_view_created"),
    (2577, "retention_view", "reference_alternative_view", "reference_alternative_view_created"),
    (2578, "bundle", "post_commitment_alternative_retention_bundle_creation", "post_commitment_alternative_retention_bundle_created"),
    (2579, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2580, "bundle", "stop_lines_carry", "post_commitment_alternative_retention_stop_lines_carried"),
    (2581, "bundle", "generated_retention_true", "generated_retention_true_recorded"),
    (2582, "bundle", "generated_alternative_deletion_false", "generated_alternative_deletion_false_recorded"),
    (2583, "bundle", "generated_commitment_rewrite_false", "generated_commitment_rewrite_false_recorded"),
    (2584, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (2585, "integrity", "every_update_gets_retention_state_check", "every_update_gets_retention_state_confirmed"),
    (2586, "integrity", "retention_variety_preservation_check", "retention_variety_preservation_confirmed"),
    (2587, "integrity", "update_record_conflict_trace_check", "update_record_conflict_trace_confirmed"),
    (2588, "integrity", "alternatives_retained_without_deletion_check", "alternatives_retained_without_deletion_confirmed"),
    (2589, "integrity", "no_commitment_rewrite_check", "no_commitment_rewrite_confirmed"),
    (2590, "integrity", "no_resolution_check", "no_resolution_confirmed"),
    (2591, "non_identity", "retention_vs_deletion_split", "retention_deletion_non_identity"),
    (2592, "non_identity", "retention_vs_rewrite_split", "retention_rewrite_non_identity"),
    (2593, "non_identity", "retention_vs_resolution_split", "retention_resolution_non_identity"),
    (2594, "music_subject", "retention_as_after_adoption_alternative_memory", "after_adoption_alternative_memory_preserved"),
    (2595, "music_subject", "contextual_alternative_as_latent_phrase_reading", "latent_phrase_reading_preserved"),
    (2596, "music_subject", "hearing_shift_alternative_as_latent_weight_reading", "latent_weight_reading_preserved"),
    (2597, "summary", "post_commitment_alternative_retention_summary", "post_commitment_alternative_retention_observed"),
    (2598, "next_plan", "next_xi_selection", "xi_alternative_reactivation_after_commitment_stress"),
)


def _build_steps() -> tuple[PostCommitmentAlternativeRetentionStep, ...]:
    previous = "post_commitment_trace_update_2499_2548"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(PostCommitmentAlternativeRetentionStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _retention_state(update: PostCommitmentTraceUpdate) -> PostCommitmentAlternativeState:
    if update.update_kind == "contextual_record_trace_update":
        kind = "contextual_alternative_retention"
        retained_as = "latent_phrase_context_alternative"
    elif update.update_kind == "hearing_shift_record_trace_update":
        kind = "hearing_shift_alternative_retention"
        retained_as = "latent_weighted_hearing_alternative"
    else:
        kind = "reference_alternative_retention"
        retained_as = "active_reference_axis_alternative"

    return PostCommitmentAlternativeState(
        source_update=update,
        retention_kind=kind,
        retained_as=retained_as,
        preserves_update_trace=True,
        preserves_record_trace=update.preserves_record_trace,
        preserves_conflict_trace=update.preserves_conflict_trace,
        keeps_alternative_available=True,
        deletes_alternative=False,
        rewrites_commitment=False,
        resolves_conflict=False,
        status="post_commitment_alternative_retained_without_deletion",
    )


def build_post_commitment_alternative_retention_bundle(
    source: PostCommitmentTraceUpdateBundle,
) -> PostCommitmentAlternativeRetentionBundle:
    alternatives = tuple(_retention_state(update) for update in source.trace_updates)
    contextual = tuple(item for item in alternatives if item.retention_kind == "contextual_alternative_retention")
    hearing_shift = tuple(item for item in alternatives if item.retention_kind == "hearing_shift_alternative_retention")
    reference = tuple(item for item in alternatives if item.retention_kind == "reference_alternative_retention")
    return PostCommitmentAlternativeRetentionBundle(
        source_bundle=source,
        retained_alternatives=alternatives,
        contextual_alternatives=contextual,
        hearing_shift_alternatives=hearing_shift,
        reference_alternatives=reference,
        stop_lines=(
            "retention_not_deletion",
            "retention_not_commitment_rewrite",
            "retention_not_resolution",
            "retention_partition_not_solution",
            "retention_not_final_judgement",
        ),
        generated_retention=True,
        generated_alternative_deletion=False,
        generated_commitment_rewrite=False,
        generated_resolution=False,
        status="post_commitment_alternative_retention_bundle_2549_2598_built_without_deletion",
    )


def observe_post_commitment_alternative_retention() -> PostCommitmentAlternativeRetentionObservation:
    source = observe_post_commitment_trace_update()
    bundle = build_post_commitment_alternative_retention_bundle(source.bundle)
    steps = _build_steps()

    return PostCommitmentAlternativeRetentionObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_update_gets_retention_state=(len(bundle.retained_alternatives) == len(source.bundle.trace_updates)),
        retention_variety_preserved=(
            len(bundle.contextual_alternatives) == 1
            and len(bundle.hearing_shift_alternatives) == 1
            and len(bundle.reference_alternatives) == 1
        ),
        update_record_conflict_traces_preserved=all(
            item.preserves_update_trace and item.preserves_record_trace and item.preserves_conflict_trace
            for item in bundle.retained_alternatives
        ),
        alternatives_retained_without_deletion=(
            bundle.generated_retention is True
            and bundle.generated_alternative_deletion is False
            and all(item.keeps_alternative_available and not item.deletes_alternative for item in bundle.retained_alternatives)
        ),
        no_rewrite_or_resolution=(
            bundle.generated_commitment_rewrite is False
            and bundle.generated_resolution is False
            and all(not item.rewrites_commitment and not item.resolves_conflict for item in bundle.retained_alternatives)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="post_commitment_alternative_retention_2549_2598_observed_without_deletion_or_rewrite",
    )


def run_checks() -> None:
    observation = observe_post_commitment_alternative_retention()
    bundle = observation.bundle

    assert observation.source_status == (
        "post_commitment_trace_update_2499_2548_observed_without_history_rewrite_or_deletion"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2549
    assert observation.steps[-1].number == 2598
    assert observation.every_update_gets_retention_state is True
    assert observation.retention_variety_preserved is True
    assert observation.update_record_conflict_traces_preserved is True
    assert observation.alternatives_retained_without_deletion is True
    assert observation.no_rewrite_or_resolution is True
    assert len(bundle.retained_alternatives) == 3
    assert len(bundle.contextual_alternatives) == 1
    assert len(bundle.hearing_shift_alternatives) == 1
    assert len(bundle.reference_alternatives) == 1
    assert bundle.generated_retention is True
    assert bundle.generated_alternative_deletion is False
    assert bundle.generated_commitment_rewrite is False
    assert bundle.generated_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_alternative_reactivation_after_commitment_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_post_commitment_alternative_retention().status)
