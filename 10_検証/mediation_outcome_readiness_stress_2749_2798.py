"""mediationをoutcome readinessへ渡す境界を検査する最小実験。"""

from dataclasses import dataclass

from conflict_mediation_after_reactivation_stress_2699_2748 import (
    ConflictMediationAfterReactivationBundle,
    ConflictMediationRoute,
    observe_conflict_mediation_after_reactivation,
)


@dataclass(frozen=True)
class MediationOutcomeReadinessStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class MediationOutcomeReadinessRoute:
    source_mediation: ConflictMediationRoute
    readiness_kind: str
    readiness_condition: str
    preserves_mediation_trace: bool
    preserves_reactivation_trace: bool
    preserves_commitment_trace: bool
    preserves_conflict_trace: bool
    creates_outcome_readiness: bool
    selects_outcome: bool
    executes_outcome: bool
    finalizes_judgement: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class MediationOutcomeReadinessBundle:
    source_bundle: ConflictMediationAfterReactivationBundle
    readiness_routes: tuple[MediationOutcomeReadinessRoute, ...]
    contextual_readiness: tuple[MediationOutcomeReadinessRoute, ...]
    hearing_shift_readiness: tuple[MediationOutcomeReadinessRoute, ...]
    reference_readiness: tuple[MediationOutcomeReadinessRoute, ...]
    stop_lines: tuple[str, ...]
    generated_outcome_readiness: bool
    generated_outcome_selection: bool
    generated_outcome_execution: bool
    generated_final_judgement: bool
    generated_resolution: bool
    status: str


@dataclass(frozen=True)
class MediationOutcomeReadinessObservation:
    source_status: str
    steps: tuple[MediationOutcomeReadinessStep, ...]
    bundle: MediationOutcomeReadinessBundle
    every_mediation_gets_readiness_route: bool
    readiness_variety_preserved: bool
    mediation_conflict_commitment_traces_preserved: bool
    readiness_generated_without_selection: bool
    no_execution_judgement_or_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2749, "source_reentry", "reuse_2699_2748_conflict_mediation_after_reactivation", "conflict_mediation_after_reactivation_preserved"),
    (2750, "source_reentry", "next_xi_received", "mediation_outcome_readiness_stress_received"),
    (2751, "source_reentry", "mediation_routes_recheck", "mediation_routes_available"),
    (2752, "readiness_request", "mediation_outcome_readiness_request", "mediation_outcome_readiness_candidate"),
    (2753, "readiness_request", "readiness_not_outcome_selection_guard", "outcome_selection_non_identity_preserved"),
    (2754, "readiness_request", "readiness_not_outcome_execution_guard", "outcome_execution_blocked"),
    (2755, "readiness_request", "readiness_not_final_judgement_guard", "final_judgement_non_identity_preserved"),
    (2756, "readiness_layer", "outcome_readiness_generation", "outcome_readiness_routes_recorded"),
    (2757, "readiness_layer", "contextual_outcome_readiness", "contextual_outcome_readiness_recorded"),
    (2758, "readiness_layer", "hearing_shift_outcome_readiness", "hearing_shift_outcome_readiness_recorded"),
    (2759, "readiness_layer", "reference_outcome_readiness", "reference_outcome_readiness_recorded"),
    (2760, "readiness_layer", "creates_outcome_readiness_true", "creates_outcome_readiness_true_recorded"),
    (2761, "readiness_layer", "selects_outcome_false", "selects_outcome_false_recorded"),
    (2762, "readiness_layer", "executes_outcome_false", "executes_outcome_false_recorded"),
    (2763, "readiness_condition_layer", "phrase_context_readiness_condition", "phrase_context_readiness_condition_recorded"),
    (2764, "readiness_condition_layer", "hearing_weight_readiness_condition", "hearing_weight_readiness_condition_recorded"),
    (2765, "readiness_condition_layer", "reference_scope_readiness_condition", "reference_scope_readiness_condition_recorded"),
    (2766, "readiness_condition_layer", "mediation_trace_carry", "mediation_trace_carried"),
    (2767, "readiness_condition_layer", "reactivation_trace_carry", "reactivation_trace_carried"),
    (2768, "readiness_condition_layer", "commitment_conflict_trace_carry", "commitment_conflict_trace_carried"),
    (2769, "partition_layer", "contextual_readiness_partition", "contextual_readiness_partition_recorded"),
    (2770, "partition_layer", "hearing_shift_readiness_partition", "hearing_shift_readiness_partition_recorded"),
    (2771, "partition_layer", "reference_readiness_partition", "reference_readiness_partition_recorded"),
    (2772, "partition_layer", "readiness_partition_not_selection_guard", "partition_selection_non_identity"),
    (2773, "partition_layer", "readiness_partition_not_solution_guard", "partition_solution_non_identity"),
    (2774, "readiness_view", "mediation_outcome_readiness_view", "mediation_outcome_readiness_view_created"),
    (2775, "readiness_view", "contextual_readiness_view", "contextual_readiness_view_created"),
    (2776, "readiness_view", "hearing_shift_readiness_view", "hearing_shift_readiness_view_created"),
    (2777, "readiness_view", "reference_readiness_view", "reference_readiness_view_created"),
    (2778, "bundle", "mediation_outcome_readiness_bundle_creation", "mediation_outcome_readiness_bundle_created"),
    (2779, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2780, "bundle", "stop_lines_carry", "mediation_outcome_readiness_stop_lines_carried"),
    (2781, "bundle", "generated_outcome_readiness_true", "generated_outcome_readiness_true_recorded"),
    (2782, "bundle", "generated_outcome_selection_false", "generated_outcome_selection_false_recorded"),
    (2783, "bundle", "generated_outcome_execution_false", "generated_outcome_execution_false_recorded"),
    (2784, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (2785, "integrity", "every_mediation_gets_readiness_route_check", "every_mediation_gets_readiness_route_confirmed"),
    (2786, "integrity", "readiness_variety_preservation_check", "readiness_variety_preservation_confirmed"),
    (2787, "integrity", "mediation_conflict_commitment_trace_check", "mediation_conflict_commitment_trace_confirmed"),
    (2788, "integrity", "readiness_without_selection_check", "readiness_without_selection_confirmed"),
    (2789, "integrity", "no_outcome_execution_check", "no_outcome_execution_confirmed"),
    (2790, "integrity", "no_final_judgement_or_resolution_check", "no_final_judgement_or_resolution_confirmed"),
    (2791, "non_identity", "readiness_vs_selection_split", "readiness_selection_non_identity"),
    (2792, "non_identity", "readiness_vs_execution_split", "readiness_execution_non_identity"),
    (2793, "non_identity", "readiness_vs_resolution_split", "readiness_resolution_non_identity"),
    (2794, "music_subject", "readiness_as_mediated_listening_preparation", "mediated_listening_preparation_preserved"),
    (2795, "music_subject", "contextual_readiness_as_phrase_reentry_preparation", "phrase_reentry_preparation_preserved"),
    (2796, "music_subject", "hearing_shift_readiness_as_weight_rehearing_preparation", "weight_rehearing_preparation_preserved"),
    (2797, "summary", "mediation_outcome_readiness_summary", "mediation_outcome_readiness_observed"),
    (2798, "next_plan", "next_xi_selection", "xi_mediation_outcome_attempt_boundary_stress"),
)


def _build_steps() -> tuple[MediationOutcomeReadinessStep, ...]:
    previous = "conflict_mediation_after_reactivation_2699_2748"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(MediationOutcomeReadinessStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _readiness_route(mediation: ConflictMediationRoute) -> MediationOutcomeReadinessRoute:
    if mediation.mediation_kind == "contextual_conflict_mediation":
        kind = "contextual_outcome_readiness"
        condition = "later_phrase_context_can_receive_mediation"
    elif mediation.mediation_kind == "hearing_shift_conflict_mediation":
        kind = "hearing_shift_outcome_readiness"
        condition = "returned_weight_can_be_reheard_without_replacement"
    else:
        kind = "reference_outcome_readiness"
        condition = "reference_scope_can_remain_open_without_resolution"

    return MediationOutcomeReadinessRoute(
        source_mediation=mediation,
        readiness_kind=kind,
        readiness_condition=condition,
        preserves_mediation_trace=True,
        preserves_reactivation_trace=mediation.preserves_reactivation_trace,
        preserves_commitment_trace=mediation.preserves_commitment_trace,
        preserves_conflict_trace=mediation.preserves_conflict_trace,
        creates_outcome_readiness=True,
        selects_outcome=False,
        executes_outcome=False,
        finalizes_judgement=False,
        resolves_conflict=False,
        status="mediation_outcome_readiness_recorded_without_selection_or_resolution",
    )


def build_mediation_outcome_readiness_bundle(
    source: ConflictMediationAfterReactivationBundle,
) -> MediationOutcomeReadinessBundle:
    routes = tuple(_readiness_route(mediation) for mediation in source.mediation_routes)
    contextual = tuple(route for route in routes if route.readiness_kind == "contextual_outcome_readiness")
    hearing_shift = tuple(route for route in routes if route.readiness_kind == "hearing_shift_outcome_readiness")
    reference = tuple(route for route in routes if route.readiness_kind == "reference_outcome_readiness")
    return MediationOutcomeReadinessBundle(
        source_bundle=source,
        readiness_routes=routes,
        contextual_readiness=contextual,
        hearing_shift_readiness=hearing_shift,
        reference_readiness=reference,
        stop_lines=(
            "readiness_not_outcome_selection",
            "readiness_not_outcome_execution",
            "readiness_not_final_judgement",
            "readiness_not_resolution",
            "readiness_not_solution",
        ),
        generated_outcome_readiness=True,
        generated_outcome_selection=False,
        generated_outcome_execution=False,
        generated_final_judgement=False,
        generated_resolution=False,
        status="mediation_outcome_readiness_bundle_2749_2798_built_without_selection_or_resolution",
    )


def observe_mediation_outcome_readiness() -> MediationOutcomeReadinessObservation:
    source = observe_conflict_mediation_after_reactivation()
    bundle = build_mediation_outcome_readiness_bundle(source.bundle)
    steps = _build_steps()

    return MediationOutcomeReadinessObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_mediation_gets_readiness_route=(len(bundle.readiness_routes) == len(source.bundle.mediation_routes)),
        readiness_variety_preserved=(
            len(bundle.contextual_readiness) == 1
            and len(bundle.hearing_shift_readiness) == 1
            and len(bundle.reference_readiness) == 1
        ),
        mediation_conflict_commitment_traces_preserved=all(
            route.preserves_mediation_trace
            and route.preserves_reactivation_trace
            and route.preserves_commitment_trace
            and route.preserves_conflict_trace
            for route in bundle.readiness_routes
        ),
        readiness_generated_without_selection=(
            bundle.generated_outcome_readiness is True
            and bundle.generated_outcome_selection is False
            and all(route.creates_outcome_readiness and not route.selects_outcome for route in bundle.readiness_routes)
        ),
        no_execution_judgement_or_resolution=(
            bundle.generated_outcome_execution is False
            and bundle.generated_final_judgement is False
            and bundle.generated_resolution is False
            and all(
                not route.executes_outcome and not route.finalizes_judgement and not route.resolves_conflict
                for route in bundle.readiness_routes
            )
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="mediation_outcome_readiness_2749_2798_observed_without_selection_or_resolution",
    )


def run_checks() -> None:
    observation = observe_mediation_outcome_readiness()
    bundle = observation.bundle

    assert observation.source_status == (
        "conflict_mediation_after_reactivation_2699_2748_observed_without_cancellation_or_resolution"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2749
    assert observation.steps[-1].number == 2798
    assert observation.every_mediation_gets_readiness_route is True
    assert observation.readiness_variety_preserved is True
    assert observation.mediation_conflict_commitment_traces_preserved is True
    assert observation.readiness_generated_without_selection is True
    assert observation.no_execution_judgement_or_resolution is True
    assert len(bundle.readiness_routes) == 3
    assert len(bundle.contextual_readiness) == 1
    assert len(bundle.hearing_shift_readiness) == 1
    assert len(bundle.reference_readiness) == 1
    assert bundle.generated_outcome_readiness is True
    assert bundle.generated_outcome_selection is False
    assert bundle.generated_outcome_execution is False
    assert bundle.generated_final_judgement is False
    assert bundle.generated_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_mediation_outcome_attempt_boundary_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_mediation_outcome_readiness().status)
