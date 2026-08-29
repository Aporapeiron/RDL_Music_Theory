"""commitment後に保持されたalternative memoryのreactivation境界を検査する最小実験。"""

from dataclasses import dataclass

from post_commitment_alternative_retention_stress_2549_2598 import (
    PostCommitmentAlternativeRetentionBundle,
    PostCommitmentAlternativeState,
    observe_post_commitment_alternative_retention,
)


@dataclass(frozen=True)
class AlternativeReactivationAfterCommitmentStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class AlternativeReactivationAfterCommitment:
    source_alternative: PostCommitmentAlternativeState
    reactivation_kind: str
    reactivation_trigger: str
    preserves_alternative_trace: bool
    preserves_commitment_trace: bool
    preserves_conflict_trace: bool
    reactivates_alternative: bool
    cancels_commitment: bool
    commits_new_verdict: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class AlternativeReactivationAfterCommitmentBundle:
    source_bundle: PostCommitmentAlternativeRetentionBundle
    reactivations: tuple[AlternativeReactivationAfterCommitment, ...]
    contextual_reactivations: tuple[AlternativeReactivationAfterCommitment, ...]
    hearing_shift_reactivations: tuple[AlternativeReactivationAfterCommitment, ...]
    reference_reactivations: tuple[AlternativeReactivationAfterCommitment, ...]
    stop_lines: tuple[str, ...]
    generated_reactivation: bool
    generated_commitment_cancellation: bool
    generated_new_verdict: bool
    generated_resolution: bool
    status: str


@dataclass(frozen=True)
class AlternativeReactivationAfterCommitmentObservation:
    source_status: str
    steps: tuple[AlternativeReactivationAfterCommitmentStep, ...]
    bundle: AlternativeReactivationAfterCommitmentBundle
    every_retained_alternative_gets_reactivation: bool
    reactivation_variety_preserved: bool
    alternative_commitment_conflict_traces_preserved: bool
    alternatives_reactivated_without_cancelling_commitment: bool
    no_verdict_or_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2599, "source_reentry", "reuse_2549_2598_post_commitment_alternative_retention", "post_commitment_alternative_retention_preserved"),
    (2600, "source_reentry", "next_xi_received", "alternative_reactivation_after_commitment_stress_received"),
    (2601, "source_reentry", "retained_alternatives_recheck", "retained_alternatives_available"),
    (2602, "reactivation_request", "alternative_reactivation_after_commitment_request", "alternative_reactivation_after_commitment_candidate"),
    (2603, "reactivation_request", "reactivation_not_commitment_cancellation_guard", "commitment_cancellation_non_identity_preserved"),
    (2604, "reactivation_request", "reactivation_not_new_verdict_guard", "new_verdict_blocked"),
    (2605, "reactivation_request", "reactivation_not_resolution_guard", "resolution_non_identity_preserved"),
    (2606, "reactivation_layer", "alternative_reactivation_generation", "alternative_reactivations_recorded"),
    (2607, "reactivation_layer", "contextual_alternative_reactivation", "contextual_alternative_reactivation_recorded"),
    (2608, "reactivation_layer", "hearing_shift_alternative_reactivation", "hearing_shift_alternative_reactivation_recorded"),
    (2609, "reactivation_layer", "reference_alternative_reactivation", "reference_alternative_reactivation_recorded"),
    (2610, "reactivation_layer", "reactivates_alternative_true", "reactivates_alternative_true_recorded"),
    (2611, "reactivation_layer", "cancels_commitment_false", "cancels_commitment_false_recorded"),
    (2612, "reactivation_layer", "commits_new_verdict_false", "commits_new_verdict_false_recorded"),
    (2613, "reactivation_trigger_layer", "later_phrase_context_trigger", "later_phrase_context_trigger_recorded"),
    (2614, "reactivation_trigger_layer", "hearing_weight_shift_trigger", "hearing_weight_shift_trigger_recorded"),
    (2615, "reactivation_trigger_layer", "reference_axis_check_trigger", "reference_axis_check_trigger_recorded"),
    (2616, "reactivation_trigger_layer", "alternative_trace_carry", "alternative_trace_carried"),
    (2617, "reactivation_trigger_layer", "commitment_trace_carry", "commitment_trace_carried"),
    (2618, "reactivation_trigger_layer", "conflict_trace_carry", "conflict_trace_carried"),
    (2619, "partition_layer", "contextual_reactivation_partition", "contextual_reactivation_partition_recorded"),
    (2620, "partition_layer", "hearing_shift_reactivation_partition", "hearing_shift_reactivation_partition_recorded"),
    (2621, "partition_layer", "reference_reactivation_partition", "reference_reactivation_partition_recorded"),
    (2622, "partition_layer", "reactivation_partition_not_cancellation_guard", "partition_cancellation_non_identity"),
    (2623, "partition_layer", "reactivation_partition_not_solution_guard", "partition_solution_non_identity"),
    (2624, "reactivation_view", "alternative_reactivation_after_commitment_view", "alternative_reactivation_after_commitment_view_created"),
    (2625, "reactivation_view", "contextual_reactivation_view", "contextual_reactivation_view_created"),
    (2626, "reactivation_view", "hearing_shift_reactivation_view", "hearing_shift_reactivation_view_created"),
    (2627, "reactivation_view", "reference_reactivation_view", "reference_reactivation_view_created"),
    (2628, "bundle", "alternative_reactivation_after_commitment_bundle_creation", "alternative_reactivation_after_commitment_bundle_created"),
    (2629, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2630, "bundle", "stop_lines_carry", "alternative_reactivation_after_commitment_stop_lines_carried"),
    (2631, "bundle", "generated_reactivation_true", "generated_reactivation_true_recorded"),
    (2632, "bundle", "generated_commitment_cancellation_false", "generated_commitment_cancellation_false_recorded"),
    (2633, "bundle", "generated_new_verdict_false", "generated_new_verdict_false_recorded"),
    (2634, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (2635, "integrity", "every_retained_alternative_gets_reactivation_check", "every_retained_alternative_gets_reactivation_confirmed"),
    (2636, "integrity", "reactivation_variety_preservation_check", "reactivation_variety_preservation_confirmed"),
    (2637, "integrity", "alternative_commitment_conflict_trace_check", "alternative_commitment_conflict_trace_confirmed"),
    (2638, "integrity", "reactivation_without_commitment_cancellation_check", "reactivation_without_commitment_cancellation_confirmed"),
    (2639, "integrity", "no_new_verdict_check", "no_new_verdict_confirmed"),
    (2640, "integrity", "no_resolution_check", "no_resolution_confirmed"),
    (2641, "non_identity", "reactivation_vs_commitment_cancellation_split", "reactivation_commitment_cancellation_non_identity"),
    (2642, "non_identity", "reactivation_vs_new_verdict_split", "reactivation_new_verdict_non_identity"),
    (2643, "non_identity", "reactivation_vs_resolution_split", "reactivation_resolution_non_identity"),
    (2644, "music_subject", "reactivation_as_after_adoption_rehearing", "after_adoption_rehearing_preserved"),
    (2645, "music_subject", "contextual_reactivation_as_later_phrase_pressure", "later_phrase_pressure_preserved"),
    (2646, "music_subject", "hearing_shift_reactivation_as_weight_pressure_return", "weight_pressure_return_preserved"),
    (2647, "summary", "alternative_reactivation_after_commitment_summary", "alternative_reactivation_after_commitment_observed"),
    (2648, "next_plan", "next_xi_selection", "xi_reactivation_conflict_with_commitment_stress"),
)


def _build_steps() -> tuple[AlternativeReactivationAfterCommitmentStep, ...]:
    previous = "post_commitment_alternative_retention_2549_2598"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(AlternativeReactivationAfterCommitmentStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _reactivation(
    alternative: PostCommitmentAlternativeState,
) -> AlternativeReactivationAfterCommitment:
    if alternative.retention_kind == "contextual_alternative_retention":
        kind = "contextual_alternative_reactivation"
        trigger = "later_phrase_context_reopens_latent_reading"
    elif alternative.retention_kind == "hearing_shift_alternative_retention":
        kind = "hearing_shift_alternative_reactivation"
        trigger = "hearing_weight_shift_returns_latent_reading"
    else:
        kind = "reference_alternative_reactivation"
        trigger = "reference_axis_check_reactivates_active_alternative"

    return AlternativeReactivationAfterCommitment(
        source_alternative=alternative,
        reactivation_kind=kind,
        reactivation_trigger=trigger,
        preserves_alternative_trace=True,
        preserves_commitment_trace=alternative.preserves_record_trace,
        preserves_conflict_trace=alternative.preserves_conflict_trace,
        reactivates_alternative=True,
        cancels_commitment=False,
        commits_new_verdict=False,
        resolves_conflict=False,
        status="alternative_reactivated_after_commitment_without_cancellation",
    )


def build_alternative_reactivation_after_commitment_bundle(
    source: PostCommitmentAlternativeRetentionBundle,
) -> AlternativeReactivationAfterCommitmentBundle:
    reactivations = tuple(_reactivation(item) for item in source.retained_alternatives)
    contextual = tuple(item for item in reactivations if item.reactivation_kind == "contextual_alternative_reactivation")
    hearing_shift = tuple(item for item in reactivations if item.reactivation_kind == "hearing_shift_alternative_reactivation")
    reference = tuple(item for item in reactivations if item.reactivation_kind == "reference_alternative_reactivation")
    return AlternativeReactivationAfterCommitmentBundle(
        source_bundle=source,
        reactivations=reactivations,
        contextual_reactivations=contextual,
        hearing_shift_reactivations=hearing_shift,
        reference_reactivations=reference,
        stop_lines=(
            "reactivation_not_commitment_cancellation",
            "reactivation_not_new_verdict",
            "reactivation_not_resolution",
            "reactivation_partition_not_solution",
            "reactivation_not_history_rewrite",
        ),
        generated_reactivation=True,
        generated_commitment_cancellation=False,
        generated_new_verdict=False,
        generated_resolution=False,
        status="alternative_reactivation_after_commitment_bundle_2599_2648_built_without_cancellation",
    )


def observe_alternative_reactivation_after_commitment() -> AlternativeReactivationAfterCommitmentObservation:
    source = observe_post_commitment_alternative_retention()
    bundle = build_alternative_reactivation_after_commitment_bundle(source.bundle)
    steps = _build_steps()

    return AlternativeReactivationAfterCommitmentObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_retained_alternative_gets_reactivation=(
            len(bundle.reactivations) == len(source.bundle.retained_alternatives)
        ),
        reactivation_variety_preserved=(
            len(bundle.contextual_reactivations) == 1
            and len(bundle.hearing_shift_reactivations) == 1
            and len(bundle.reference_reactivations) == 1
        ),
        alternative_commitment_conflict_traces_preserved=all(
            item.preserves_alternative_trace
            and item.preserves_commitment_trace
            and item.preserves_conflict_trace
            for item in bundle.reactivations
        ),
        alternatives_reactivated_without_cancelling_commitment=(
            bundle.generated_reactivation is True
            and bundle.generated_commitment_cancellation is False
            and all(item.reactivates_alternative and not item.cancels_commitment for item in bundle.reactivations)
        ),
        no_verdict_or_resolution=(
            bundle.generated_new_verdict is False
            and bundle.generated_resolution is False
            and all(not item.commits_new_verdict and not item.resolves_conflict for item in bundle.reactivations)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="alternative_reactivation_after_commitment_2599_2648_observed_without_cancellation_or_verdict",
    )


def run_checks() -> None:
    observation = observe_alternative_reactivation_after_commitment()
    bundle = observation.bundle

    assert observation.source_status == (
        "post_commitment_alternative_retention_2549_2598_observed_without_deletion_or_rewrite"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2599
    assert observation.steps[-1].number == 2648
    assert observation.every_retained_alternative_gets_reactivation is True
    assert observation.reactivation_variety_preserved is True
    assert observation.alternative_commitment_conflict_traces_preserved is True
    assert observation.alternatives_reactivated_without_cancelling_commitment is True
    assert observation.no_verdict_or_resolution is True
    assert len(bundle.reactivations) == 3
    assert len(bundle.contextual_reactivations) == 1
    assert len(bundle.hearing_shift_reactivations) == 1
    assert len(bundle.reference_reactivations) == 1
    assert bundle.generated_reactivation is True
    assert bundle.generated_commitment_cancellation is False
    assert bundle.generated_new_verdict is False
    assert bundle.generated_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_reactivation_conflict_with_commitment_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_alternative_reactivation_after_commitment().status)
