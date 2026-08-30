"""reactivation conflictをmediationへ渡す境界を検査する最小実験。"""

from dataclasses import dataclass

from reactivation_conflict_with_commitment_stress_2649_2698 import (
    ReactivationCommitmentConflict,
    ReactivationConflictWithCommitmentBundle,
    observe_reactivation_conflict_with_commitment,
)


@dataclass(frozen=True)
class ConflictMediationAfterReactivationStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ConflictMediationRoute:
    source_conflict: ReactivationCommitmentConflict
    mediation_kind: str
    mediation_content: str
    preserves_reactivation_trace: bool
    preserves_commitment_trace: bool
    preserves_conflict_trace: bool
    creates_mediation: bool
    cancels_commitment: bool
    replaces_commitment: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class ConflictMediationAfterReactivationBundle:
    source_bundle: ReactivationConflictWithCommitmentBundle
    mediation_routes: tuple[ConflictMediationRoute, ...]
    contextual_mediations: tuple[ConflictMediationRoute, ...]
    hearing_shift_mediations: tuple[ConflictMediationRoute, ...]
    reference_mediations: tuple[ConflictMediationRoute, ...]
    stop_lines: tuple[str, ...]
    generated_mediation: bool
    generated_commitment_cancellation: bool
    generated_commitment_replacement: bool
    generated_resolution: bool
    status: str


@dataclass(frozen=True)
class ConflictMediationAfterReactivationObservation:
    source_status: str
    steps: tuple[ConflictMediationAfterReactivationStep, ...]
    bundle: ConflictMediationAfterReactivationBundle
    every_conflict_gets_mediation_route: bool
    mediation_variety_preserved: bool
    reactivation_commitment_conflict_traces_preserved: bool
    mediation_generated_without_cancellation: bool
    no_replacement_or_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2699, "source_reentry", "reuse_2649_2698_reactivation_conflict_with_commitment", "reactivation_conflict_with_commitment_preserved"),
    (2700, "source_reentry", "next_xi_received", "conflict_mediation_after_reactivation_stress_received"),
    (2701, "source_reentry", "reactivation_conflicts_recheck", "reactivation_conflicts_available"),
    (2702, "mediation_request", "conflict_mediation_after_reactivation_request", "conflict_mediation_after_reactivation_candidate"),
    (2703, "mediation_request", "mediation_not_commitment_cancellation_guard", "commitment_cancellation_non_identity_preserved"),
    (2704, "mediation_request", "mediation_not_commitment_replacement_guard", "commitment_replacement_blocked"),
    (2705, "mediation_request", "mediation_not_resolution_guard", "resolution_non_identity_preserved"),
    (2706, "mediation_layer", "conflict_mediation_generation", "conflict_mediations_recorded"),
    (2707, "mediation_layer", "contextual_conflict_mediation", "contextual_conflict_mediation_recorded"),
    (2708, "mediation_layer", "hearing_shift_conflict_mediation", "hearing_shift_conflict_mediation_recorded"),
    (2709, "mediation_layer", "reference_conflict_mediation", "reference_conflict_mediation_recorded"),
    (2710, "mediation_layer", "creates_mediation_true", "creates_mediation_true_recorded"),
    (2711, "mediation_layer", "cancels_commitment_false", "cancels_commitment_false_recorded"),
    (2712, "mediation_layer", "replaces_commitment_false", "replaces_commitment_false_recorded"),
    (2713, "mediation_content_layer", "phrase_pressure_mediation_content", "phrase_pressure_mediation_content_recorded"),
    (2714, "mediation_content_layer", "weight_pressure_mediation_content", "weight_pressure_mediation_content_recorded"),
    (2715, "mediation_content_layer", "reference_scope_mediation_content", "reference_scope_mediation_content_recorded"),
    (2716, "mediation_content_layer", "reactivation_trace_carry", "reactivation_trace_carried"),
    (2717, "mediation_content_layer", "commitment_trace_carry", "commitment_trace_carried"),
    (2718, "mediation_content_layer", "conflict_trace_carry", "conflict_trace_carried"),
    (2719, "partition_layer", "contextual_mediation_partition", "contextual_mediation_partition_recorded"),
    (2720, "partition_layer", "hearing_shift_mediation_partition", "hearing_shift_mediation_partition_recorded"),
    (2721, "partition_layer", "reference_mediation_partition", "reference_mediation_partition_recorded"),
    (2722, "partition_layer", "mediation_partition_not_cancellation_guard", "partition_cancellation_non_identity"),
    (2723, "partition_layer", "mediation_partition_not_solution_guard", "partition_solution_non_identity"),
    (2724, "mediation_view", "conflict_mediation_after_reactivation_view", "conflict_mediation_after_reactivation_view_created"),
    (2725, "mediation_view", "contextual_mediation_view", "contextual_mediation_view_created"),
    (2726, "mediation_view", "hearing_shift_mediation_view", "hearing_shift_mediation_view_created"),
    (2727, "mediation_view", "reference_mediation_view", "reference_mediation_view_created"),
    (2728, "bundle", "conflict_mediation_after_reactivation_bundle_creation", "conflict_mediation_after_reactivation_bundle_created"),
    (2729, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2730, "bundle", "stop_lines_carry", "conflict_mediation_after_reactivation_stop_lines_carried"),
    (2731, "bundle", "generated_mediation_true", "generated_mediation_true_recorded"),
    (2732, "bundle", "generated_commitment_cancellation_false", "generated_commitment_cancellation_false_recorded"),
    (2733, "bundle", "generated_commitment_replacement_false", "generated_commitment_replacement_false_recorded"),
    (2734, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (2735, "integrity", "every_conflict_gets_mediation_route_check", "every_conflict_gets_mediation_route_confirmed"),
    (2736, "integrity", "mediation_variety_preservation_check", "mediation_variety_preservation_confirmed"),
    (2737, "integrity", "reactivation_commitment_conflict_trace_check", "reactivation_commitment_conflict_trace_confirmed"),
    (2738, "integrity", "mediation_without_commitment_cancellation_check", "mediation_without_commitment_cancellation_confirmed"),
    (2739, "integrity", "no_commitment_replacement_check", "no_commitment_replacement_confirmed"),
    (2740, "integrity", "no_resolution_check", "no_resolution_confirmed"),
    (2741, "non_identity", "mediation_vs_cancellation_split", "mediation_cancellation_non_identity"),
    (2742, "non_identity", "mediation_vs_replacement_split", "mediation_replacement_non_identity"),
    (2743, "non_identity", "mediation_vs_resolution_split", "mediation_resolution_non_identity"),
    (2744, "music_subject", "mediation_as_after_adoption_tension_handling", "after_adoption_tension_handling_preserved"),
    (2745, "music_subject", "contextual_mediation_as_phrase_pressure_balancing", "phrase_pressure_balancing_preserved"),
    (2746, "music_subject", "hearing_shift_mediation_as_weight_pressure_balancing", "weight_pressure_balancing_preserved"),
    (2747, "summary", "conflict_mediation_after_reactivation_summary", "conflict_mediation_after_reactivation_observed"),
    (2748, "next_plan", "next_xi_selection", "xi_mediation_outcome_readiness_stress"),
)


def _build_steps() -> tuple[ConflictMediationAfterReactivationStep, ...]:
    previous = "reactivation_conflict_with_commitment_2649_2698"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(ConflictMediationAfterReactivationStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _mediation_route(conflict: ReactivationCommitmentConflict) -> ConflictMediationRoute:
    if conflict.conflict_kind == "contextual_reactivation_commitment_conflict":
        kind = "contextual_conflict_mediation"
        content = "balance_later_phrase_pressure_without_cancelling_record"
    elif conflict.conflict_kind == "hearing_shift_reactivation_commitment_conflict":
        kind = "hearing_shift_conflict_mediation"
        content = "balance_returned_weight_pressure_without_replacing_record"
    else:
        kind = "reference_conflict_mediation"
        content = "mediate_reference_scope_without_resolving_conflict"

    return ConflictMediationRoute(
        source_conflict=conflict,
        mediation_kind=kind,
        mediation_content=content,
        preserves_reactivation_trace=True,
        preserves_commitment_trace=conflict.preserves_commitment_trace,
        preserves_conflict_trace=conflict.preserves_conflict_trace,
        creates_mediation=True,
        cancels_commitment=False,
        replaces_commitment=False,
        resolves_conflict=False,
        status="conflict_mediation_after_reactivation_recorded_without_resolution",
    )


def build_conflict_mediation_after_reactivation_bundle(
    source: ReactivationConflictWithCommitmentBundle,
) -> ConflictMediationAfterReactivationBundle:
    routes = tuple(_mediation_route(conflict) for conflict in source.conflicts)
    contextual = tuple(route for route in routes if route.mediation_kind == "contextual_conflict_mediation")
    hearing_shift = tuple(route for route in routes if route.mediation_kind == "hearing_shift_conflict_mediation")
    reference = tuple(route for route in routes if route.mediation_kind == "reference_conflict_mediation")
    return ConflictMediationAfterReactivationBundle(
        source_bundle=source,
        mediation_routes=routes,
        contextual_mediations=contextual,
        hearing_shift_mediations=hearing_shift,
        reference_mediations=reference,
        stop_lines=(
            "mediation_not_commitment_cancellation",
            "mediation_not_commitment_replacement",
            "mediation_not_resolution",
            "mediation_partition_not_solution",
            "mediation_not_final_judgement",
        ),
        generated_mediation=True,
        generated_commitment_cancellation=False,
        generated_commitment_replacement=False,
        generated_resolution=False,
        status="conflict_mediation_after_reactivation_bundle_2699_2748_built_without_resolution",
    )


def observe_conflict_mediation_after_reactivation() -> ConflictMediationAfterReactivationObservation:
    source = observe_reactivation_conflict_with_commitment()
    bundle = build_conflict_mediation_after_reactivation_bundle(source.bundle)
    steps = _build_steps()

    return ConflictMediationAfterReactivationObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_conflict_gets_mediation_route=(len(bundle.mediation_routes) == len(source.bundle.conflicts)),
        mediation_variety_preserved=(
            len(bundle.contextual_mediations) == 1
            and len(bundle.hearing_shift_mediations) == 1
            and len(bundle.reference_mediations) == 1
        ),
        reactivation_commitment_conflict_traces_preserved=all(
            route.preserves_reactivation_trace and route.preserves_commitment_trace and route.preserves_conflict_trace
            for route in bundle.mediation_routes
        ),
        mediation_generated_without_cancellation=(
            bundle.generated_mediation is True
            and bundle.generated_commitment_cancellation is False
            and all(route.creates_mediation and not route.cancels_commitment for route in bundle.mediation_routes)
        ),
        no_replacement_or_resolution=(
            bundle.generated_commitment_replacement is False
            and bundle.generated_resolution is False
            and all(not route.replaces_commitment and not route.resolves_conflict for route in bundle.mediation_routes)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="conflict_mediation_after_reactivation_2699_2748_observed_without_cancellation_or_resolution",
    )


def run_checks() -> None:
    observation = observe_conflict_mediation_after_reactivation()
    bundle = observation.bundle

    assert observation.source_status == (
        "reactivation_conflict_with_commitment_2649_2698_observed_without_cancellation_or_replacement"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2699
    assert observation.steps[-1].number == 2748
    assert observation.every_conflict_gets_mediation_route is True
    assert observation.mediation_variety_preserved is True
    assert observation.reactivation_commitment_conflict_traces_preserved is True
    assert observation.mediation_generated_without_cancellation is True
    assert observation.no_replacement_or_resolution is True
    assert len(bundle.mediation_routes) == 3
    assert len(bundle.contextual_mediations) == 1
    assert len(bundle.hearing_shift_mediations) == 1
    assert len(bundle.reference_mediations) == 1
    assert bundle.generated_mediation is True
    assert bundle.generated_commitment_cancellation is False
    assert bundle.generated_commitment_replacement is False
    assert bundle.generated_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_mediation_outcome_readiness_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_conflict_mediation_after_reactivation().status)
