"""reactivated alternativeと既存commitmentのconflict境界を検査する最小実験。"""

from dataclasses import dataclass

from alternative_reactivation_after_commitment_stress_2599_2648 import (
    AlternativeReactivationAfterCommitment,
    AlternativeReactivationAfterCommitmentBundle,
    observe_alternative_reactivation_after_commitment,
)


@dataclass(frozen=True)
class ReactivationConflictWithCommitmentStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ReactivationCommitmentConflict:
    source_reactivation: AlternativeReactivationAfterCommitment
    conflict_kind: str
    conflict_content: str
    preserves_reactivation_trace: bool
    preserves_commitment_trace: bool
    preserves_conflict_trace: bool
    detects_conflict: bool
    cancels_commitment: bool
    replaces_commitment: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class ReactivationConflictWithCommitmentBundle:
    source_bundle: AlternativeReactivationAfterCommitmentBundle
    conflicts: tuple[ReactivationCommitmentConflict, ...]
    contextual_conflicts: tuple[ReactivationCommitmentConflict, ...]
    hearing_shift_conflicts: tuple[ReactivationCommitmentConflict, ...]
    reference_conflicts: tuple[ReactivationCommitmentConflict, ...]
    stop_lines: tuple[str, ...]
    generated_conflict_detection: bool
    generated_commitment_cancellation: bool
    generated_commitment_replacement: bool
    generated_resolution: bool
    status: str


@dataclass(frozen=True)
class ReactivationConflictWithCommitmentObservation:
    source_status: str
    steps: tuple[ReactivationConflictWithCommitmentStep, ...]
    bundle: ReactivationConflictWithCommitmentBundle
    every_reactivation_gets_conflict_check: bool
    conflict_variety_preserved: bool
    reactivation_commitment_conflict_traces_preserved: bool
    conflict_detected_without_cancellation: bool
    no_replacement_or_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2649, "source_reentry", "reuse_2599_2648_alternative_reactivation_after_commitment", "alternative_reactivation_after_commitment_preserved"),
    (2650, "source_reentry", "next_xi_received", "reactivation_conflict_with_commitment_stress_received"),
    (2651, "source_reentry", "reactivations_recheck", "reactivations_available"),
    (2652, "conflict_request", "reactivation_conflict_with_commitment_request", "reactivation_conflict_with_commitment_candidate"),
    (2653, "conflict_request", "conflict_not_commitment_cancellation_guard", "commitment_cancellation_non_identity_preserved"),
    (2654, "conflict_request", "conflict_not_commitment_replacement_guard", "commitment_replacement_blocked"),
    (2655, "conflict_request", "conflict_not_resolution_guard", "resolution_non_identity_preserved"),
    (2656, "conflict_layer", "reactivation_commitment_conflict_generation", "reactivation_commitment_conflicts_recorded"),
    (2657, "conflict_layer", "contextual_reactivation_commitment_conflict", "contextual_reactivation_commitment_conflict_recorded"),
    (2658, "conflict_layer", "hearing_shift_reactivation_commitment_conflict", "hearing_shift_reactivation_commitment_conflict_recorded"),
    (2659, "conflict_layer", "reference_reactivation_commitment_conflict", "reference_reactivation_commitment_conflict_recorded"),
    (2660, "conflict_layer", "detects_conflict_true", "detects_conflict_true_recorded"),
    (2661, "conflict_layer", "cancels_commitment_false", "cancels_commitment_false_recorded"),
    (2662, "conflict_layer", "replaces_commitment_false", "replaces_commitment_false_recorded"),
    (2663, "conflict_content_layer", "phrase_pressure_conflict_content", "phrase_pressure_conflict_content_recorded"),
    (2664, "conflict_content_layer", "hearing_weight_conflict_content", "hearing_weight_conflict_content_recorded"),
    (2665, "conflict_content_layer", "reference_axis_conflict_content", "reference_axis_conflict_content_recorded"),
    (2666, "conflict_content_layer", "reactivation_trace_carry", "reactivation_trace_carried"),
    (2667, "conflict_content_layer", "commitment_trace_carry", "commitment_trace_carried"),
    (2668, "conflict_content_layer", "conflict_trace_carry", "conflict_trace_carried"),
    (2669, "partition_layer", "contextual_conflict_partition", "contextual_conflict_partition_recorded"),
    (2670, "partition_layer", "hearing_shift_conflict_partition", "hearing_shift_conflict_partition_recorded"),
    (2671, "partition_layer", "reference_conflict_partition", "reference_conflict_partition_recorded"),
    (2672, "partition_layer", "conflict_partition_not_cancellation_guard", "partition_cancellation_non_identity"),
    (2673, "partition_layer", "conflict_partition_not_solution_guard", "partition_solution_non_identity"),
    (2674, "conflict_view", "reactivation_conflict_with_commitment_view", "reactivation_conflict_with_commitment_view_created"),
    (2675, "conflict_view", "contextual_conflict_view", "contextual_conflict_view_created"),
    (2676, "conflict_view", "hearing_shift_conflict_view", "hearing_shift_conflict_view_created"),
    (2677, "conflict_view", "reference_conflict_view", "reference_conflict_view_created"),
    (2678, "bundle", "reactivation_conflict_with_commitment_bundle_creation", "reactivation_conflict_with_commitment_bundle_created"),
    (2679, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2680, "bundle", "stop_lines_carry", "reactivation_conflict_with_commitment_stop_lines_carried"),
    (2681, "bundle", "generated_conflict_detection_true", "generated_conflict_detection_true_recorded"),
    (2682, "bundle", "generated_commitment_cancellation_false", "generated_commitment_cancellation_false_recorded"),
    (2683, "bundle", "generated_commitment_replacement_false", "generated_commitment_replacement_false_recorded"),
    (2684, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (2685, "integrity", "every_reactivation_gets_conflict_check", "every_reactivation_gets_conflict_check_confirmed"),
    (2686, "integrity", "conflict_variety_preservation_check", "conflict_variety_preservation_confirmed"),
    (2687, "integrity", "reactivation_commitment_conflict_trace_check", "reactivation_commitment_conflict_trace_confirmed"),
    (2688, "integrity", "conflict_without_commitment_cancellation_check", "conflict_without_commitment_cancellation_confirmed"),
    (2689, "integrity", "no_commitment_replacement_check", "no_commitment_replacement_confirmed"),
    (2690, "integrity", "no_resolution_check", "no_resolution_confirmed"),
    (2691, "non_identity", "conflict_vs_cancellation_split", "conflict_cancellation_non_identity"),
    (2692, "non_identity", "conflict_vs_replacement_split", "conflict_replacement_non_identity"),
    (2693, "non_identity", "conflict_vs_resolution_split", "conflict_resolution_non_identity"),
    (2694, "music_subject", "conflict_as_after_adoption_tension_return", "after_adoption_tension_return_preserved"),
    (2695, "music_subject", "contextual_conflict_as_phrase_pressure_against_record", "phrase_pressure_against_record_preserved"),
    (2696, "music_subject", "hearing_shift_conflict_as_weight_pressure_against_record", "weight_pressure_against_record_preserved"),
    (2697, "summary", "reactivation_conflict_with_commitment_summary", "reactivation_conflict_with_commitment_observed"),
    (2698, "next_plan", "next_xi_selection", "xi_conflict_mediation_after_reactivation_stress"),
)


def _build_steps() -> tuple[ReactivationConflictWithCommitmentStep, ...]:
    previous = "alternative_reactivation_after_commitment_2599_2648"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(ReactivationConflictWithCommitmentStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _conflict(
    reactivation: AlternativeReactivationAfterCommitment,
) -> ReactivationCommitmentConflict:
    if reactivation.reactivation_kind == "contextual_alternative_reactivation":
        kind = "contextual_reactivation_commitment_conflict"
        content = "later_phrase_pressure_conflicts_with_existing_record"
    elif reactivation.reactivation_kind == "hearing_shift_alternative_reactivation":
        kind = "hearing_shift_reactivation_commitment_conflict"
        content = "returned_weight_pressure_conflicts_with_committed_reading"
    else:
        kind = "reference_reactivation_commitment_conflict"
        content = "reference_axis_check_conflicts_with_record_scope"

    return ReactivationCommitmentConflict(
        source_reactivation=reactivation,
        conflict_kind=kind,
        conflict_content=content,
        preserves_reactivation_trace=True,
        preserves_commitment_trace=reactivation.preserves_commitment_trace,
        preserves_conflict_trace=reactivation.preserves_conflict_trace,
        detects_conflict=True,
        cancels_commitment=False,
        replaces_commitment=False,
        resolves_conflict=False,
        status="reactivation_commitment_conflict_recorded_without_cancellation",
    )


def build_reactivation_conflict_with_commitment_bundle(
    source: AlternativeReactivationAfterCommitmentBundle,
) -> ReactivationConflictWithCommitmentBundle:
    conflicts = tuple(_conflict(item) for item in source.reactivations)
    contextual = tuple(item for item in conflicts if item.conflict_kind == "contextual_reactivation_commitment_conflict")
    hearing_shift = tuple(item for item in conflicts if item.conflict_kind == "hearing_shift_reactivation_commitment_conflict")
    reference = tuple(item for item in conflicts if item.conflict_kind == "reference_reactivation_commitment_conflict")
    return ReactivationConflictWithCommitmentBundle(
        source_bundle=source,
        conflicts=conflicts,
        contextual_conflicts=contextual,
        hearing_shift_conflicts=hearing_shift,
        reference_conflicts=reference,
        stop_lines=(
            "conflict_not_commitment_cancellation",
            "conflict_not_commitment_replacement",
            "conflict_not_resolution",
            "conflict_partition_not_solution",
            "conflict_not_history_rewrite",
        ),
        generated_conflict_detection=True,
        generated_commitment_cancellation=False,
        generated_commitment_replacement=False,
        generated_resolution=False,
        status="reactivation_conflict_with_commitment_bundle_2649_2698_built_without_cancellation",
    )


def observe_reactivation_conflict_with_commitment() -> ReactivationConflictWithCommitmentObservation:
    source = observe_alternative_reactivation_after_commitment()
    bundle = build_reactivation_conflict_with_commitment_bundle(source.bundle)
    steps = _build_steps()

    return ReactivationConflictWithCommitmentObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_reactivation_gets_conflict_check=(len(bundle.conflicts) == len(source.bundle.reactivations)),
        conflict_variety_preserved=(
            len(bundle.contextual_conflicts) == 1
            and len(bundle.hearing_shift_conflicts) == 1
            and len(bundle.reference_conflicts) == 1
        ),
        reactivation_commitment_conflict_traces_preserved=all(
            item.preserves_reactivation_trace and item.preserves_commitment_trace and item.preserves_conflict_trace
            for item in bundle.conflicts
        ),
        conflict_detected_without_cancellation=(
            bundle.generated_conflict_detection is True
            and bundle.generated_commitment_cancellation is False
            and all(item.detects_conflict and not item.cancels_commitment for item in bundle.conflicts)
        ),
        no_replacement_or_resolution=(
            bundle.generated_commitment_replacement is False
            and bundle.generated_resolution is False
            and all(not item.replaces_commitment and not item.resolves_conflict for item in bundle.conflicts)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="reactivation_conflict_with_commitment_2649_2698_observed_without_cancellation_or_replacement",
    )


def run_checks() -> None:
    observation = observe_reactivation_conflict_with_commitment()
    bundle = observation.bundle

    assert observation.source_status == (
        "alternative_reactivation_after_commitment_2599_2648_observed_without_cancellation_or_verdict"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2649
    assert observation.steps[-1].number == 2698
    assert observation.every_reactivation_gets_conflict_check is True
    assert observation.conflict_variety_preserved is True
    assert observation.reactivation_commitment_conflict_traces_preserved is True
    assert observation.conflict_detected_without_cancellation is True
    assert observation.no_replacement_or_resolution is True
    assert len(bundle.conflicts) == 3
    assert len(bundle.contextual_conflicts) == 1
    assert len(bundle.hearing_shift_conflicts) == 1
    assert len(bundle.reference_conflicts) == 1
    assert bundle.generated_conflict_detection is True
    assert bundle.generated_commitment_cancellation is False
    assert bundle.generated_commitment_replacement is False
    assert bundle.generated_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_conflict_mediation_after_reactivation_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_reactivation_conflict_with_commitment().status)
