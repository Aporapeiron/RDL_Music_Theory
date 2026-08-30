"""mediation selection controller boundaryをcontroller resultへ渡す最小実験。"""

from dataclasses import dataclass

from mediation_selection_controller_boundary_stress_2999_3048 import (
    MediationSelectionControllerBundle,
    MediationSelectionControllerRoute,
    observe_mediation_selection_controller_boundary,
)


@dataclass(frozen=True)
class MediationSelectionControllerResultStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class MediationSelectionControllerResultRoute:
    source_controller: MediationSelectionControllerRoute
    result_kind: str
    result_content: str
    preserves_controller_trace: bool
    preserves_record_trace: bool
    preserves_mediation_trace: bool
    preserves_commitment_trace: bool
    preserves_conflict_trace: bool
    creates_controller_result: bool
    selects_outcome: bool
    commits_outcome: bool
    rewrites_record: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class MediationSelectionControllerResultBundle:
    source_bundle: MediationSelectionControllerBundle
    result_routes: tuple[MediationSelectionControllerResultRoute, ...]
    contextual_results: tuple[MediationSelectionControllerResultRoute, ...]
    hearing_shift_results: tuple[MediationSelectionControllerResultRoute, ...]
    reference_results: tuple[MediationSelectionControllerResultRoute, ...]
    stop_lines: tuple[str, ...]
    generated_controller_result: bool
    generated_outcome_selection: bool
    generated_outcome_commitment: bool
    generated_record_rewrite: bool
    generated_resolution: bool
    status: str


@dataclass(frozen=True)
class MediationSelectionControllerResultObservation:
    source_status: str
    steps: tuple[MediationSelectionControllerResultStep, ...]
    bundle: MediationSelectionControllerResultBundle
    every_controller_gets_result_route: bool
    result_variety_preserved: bool
    controller_record_mediation_traces_preserved: bool
    result_generated_without_selection: bool
    no_commitment_rewrite_or_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (3049, "source_reentry", "reuse_2999_3048_mediation_selection_controller_boundary", "mediation_selection_controller_boundary_preserved"),
    (3050, "source_reentry", "next_xi_received", "mediation_selection_controller_result_stress_received"),
    (3051, "source_reentry", "controller_routes_recheck", "controller_routes_available"),
    (3052, "result_request", "mediation_selection_controller_result_request", "mediation_selection_controller_result_candidate"),
    (3053, "result_request", "result_not_outcome_selection_guard", "outcome_selection_non_identity_preserved"),
    (3054, "result_request", "result_not_outcome_commitment_guard", "outcome_commitment_blocked"),
    (3055, "result_request", "result_not_record_rewrite_guard", "record_rewrite_non_identity_preserved"),
    (3056, "result_layer", "selection_controller_result_generation", "selection_controller_results_recorded"),
    (3057, "result_layer", "contextual_controller_result", "contextual_controller_result_recorded"),
    (3058, "result_layer", "hearing_shift_controller_result", "hearing_shift_controller_result_recorded"),
    (3059, "result_layer", "reference_controller_result", "reference_controller_result_recorded"),
    (3060, "result_layer", "creates_controller_result_true", "creates_controller_result_true_recorded"),
    (3061, "result_layer", "selects_outcome_false", "selects_outcome_false_recorded"),
    (3062, "result_layer", "commits_outcome_false", "commits_outcome_false_recorded"),
    (3063, "result_content_layer", "phrase_trace_comparison_result", "phrase_trace_comparison_result_recorded"),
    (3064, "result_content_layer", "weight_trace_comparison_result", "weight_trace_comparison_result_recorded"),
    (3065, "result_content_layer", "reference_trace_comparison_result", "reference_trace_comparison_result_recorded"),
    (3066, "result_content_layer", "controller_trace_carry", "controller_trace_carried"),
    (3067, "result_content_layer", "record_trace_carry", "record_trace_carried"),
    (3068, "result_content_layer", "mediation_commitment_conflict_trace_carry", "mediation_commitment_conflict_trace_carried"),
    (3069, "partition_layer", "contextual_result_partition", "contextual_result_partition_recorded"),
    (3070, "partition_layer", "hearing_shift_result_partition", "hearing_shift_result_partition_recorded"),
    (3071, "partition_layer", "reference_result_partition", "reference_result_partition_recorded"),
    (3072, "partition_layer", "result_partition_not_selection_guard", "partition_selection_non_identity"),
    (3073, "partition_layer", "result_partition_not_solution_guard", "partition_solution_non_identity"),
    (3074, "result_view", "mediation_selection_controller_result_view", "mediation_selection_controller_result_view_created"),
    (3075, "result_view", "contextual_result_view", "contextual_result_view_created"),
    (3076, "result_view", "hearing_shift_result_view", "hearing_shift_result_view_created"),
    (3077, "result_view", "reference_result_view", "reference_result_view_created"),
    (3078, "bundle", "mediation_selection_controller_result_bundle_creation", "mediation_selection_controller_result_bundle_created"),
    (3079, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (3080, "bundle", "stop_lines_carry", "mediation_selection_controller_result_stop_lines_carried"),
    (3081, "bundle", "generated_controller_result_true", "generated_controller_result_true_recorded"),
    (3082, "bundle", "generated_outcome_selection_false", "generated_outcome_selection_false_recorded"),
    (3083, "bundle", "generated_record_rewrite_false", "generated_record_rewrite_false_recorded"),
    (3084, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (3085, "integrity", "every_controller_gets_result_route_check", "every_controller_gets_result_route_confirmed"),
    (3086, "integrity", "result_variety_preservation_check", "result_variety_preservation_confirmed"),
    (3087, "integrity", "controller_record_mediation_trace_check", "controller_record_mediation_trace_confirmed"),
    (3088, "integrity", "result_without_selection_check", "result_without_selection_confirmed"),
    (3089, "integrity", "no_outcome_commitment_check", "no_outcome_commitment_confirmed"),
    (3090, "integrity", "no_rewrite_or_resolution_check", "no_rewrite_or_resolution_confirmed"),
    (3091, "non_identity", "result_vs_selection_split", "result_selection_non_identity"),
    (3092, "non_identity", "result_vs_commitment_split", "result_commitment_non_identity"),
    (3093, "non_identity", "result_vs_resolution_split", "result_resolution_non_identity"),
    (3094, "music_subject", "result_as_mediated_comparison_result", "mediated_comparison_result_preserved"),
    (3095, "music_subject", "contextual_result_as_phrase_trace_comparison_seen", "phrase_trace_comparison_seen_preserved"),
    (3096, "music_subject", "hearing_shift_result_as_weight_trace_comparison_seen", "weight_trace_comparison_seen_preserved"),
    (3097, "summary", "mediation_selection_controller_result_summary", "mediation_selection_controller_result_observed"),
    (3098, "next_plan", "next_xi_selection", "xi_mediation_outcome_selection_candidate_stress"),
)


def _build_steps() -> tuple[MediationSelectionControllerResultStep, ...]:
    previous = "mediation_selection_controller_boundary_2999_3048"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(MediationSelectionControllerResultStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _result_route(controller: MediationSelectionControllerRoute) -> MediationSelectionControllerResultRoute:
    if controller.controller_kind == "contextual_selection_controller_boundary":
        kind = "contextual_controller_result"
        content = "phrase_trace_comparison_result_without_selection"
    elif controller.controller_kind == "hearing_shift_selection_controller_boundary":
        kind = "hearing_shift_controller_result"
        content = "weight_trace_comparison_result_without_commitment"
    else:
        kind = "reference_controller_result"
        content = "reference_trace_comparison_result_without_resolution"

    return MediationSelectionControllerResultRoute(
        source_controller=controller,
        result_kind=kind,
        result_content=content,
        preserves_controller_trace=True,
        preserves_record_trace=controller.preserves_record_trace,
        preserves_mediation_trace=controller.preserves_mediation_trace,
        preserves_commitment_trace=controller.preserves_commitment_trace,
        preserves_conflict_trace=controller.preserves_conflict_trace,
        creates_controller_result=True,
        selects_outcome=False,
        commits_outcome=False,
        rewrites_record=False,
        resolves_conflict=False,
        status="mediation_selection_controller_result_recorded_without_selection_or_resolution",
    )


def build_mediation_selection_controller_result_bundle(
    source: MediationSelectionControllerBundle,
) -> MediationSelectionControllerResultBundle:
    routes = tuple(_result_route(controller) for controller in source.controller_routes)
    contextual = tuple(route for route in routes if route.result_kind == "contextual_controller_result")
    hearing_shift = tuple(route for route in routes if route.result_kind == "hearing_shift_controller_result")
    reference = tuple(route for route in routes if route.result_kind == "reference_controller_result")
    return MediationSelectionControllerResultBundle(
        source_bundle=source,
        result_routes=routes,
        contextual_results=contextual,
        hearing_shift_results=hearing_shift,
        reference_results=reference,
        stop_lines=(
            "result_not_outcome_selection",
            "result_not_outcome_commitment",
            "result_not_record_rewrite",
            "result_not_resolution",
            "result_not_solution",
        ),
        generated_controller_result=True,
        generated_outcome_selection=False,
        generated_outcome_commitment=False,
        generated_record_rewrite=False,
        generated_resolution=False,
        status="mediation_selection_controller_result_bundle_3049_3098_built_without_selection_or_resolution",
    )


def observe_mediation_selection_controller_result() -> MediationSelectionControllerResultObservation:
    source = observe_mediation_selection_controller_boundary()
    bundle = build_mediation_selection_controller_result_bundle(source.bundle)
    steps = _build_steps()

    return MediationSelectionControllerResultObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_controller_gets_result_route=(len(bundle.result_routes) == len(source.bundle.controller_routes)),
        result_variety_preserved=(
            len(bundle.contextual_results) == 1
            and len(bundle.hearing_shift_results) == 1
            and len(bundle.reference_results) == 1
        ),
        controller_record_mediation_traces_preserved=all(
            route.preserves_controller_trace
            and route.preserves_record_trace
            and route.preserves_mediation_trace
            and route.preserves_commitment_trace
            and route.preserves_conflict_trace
            for route in bundle.result_routes
        ),
        result_generated_without_selection=(
            bundle.generated_controller_result is True
            and bundle.generated_outcome_selection is False
            and all(route.creates_controller_result and not route.selects_outcome for route in bundle.result_routes)
        ),
        no_commitment_rewrite_or_resolution=(
            bundle.generated_outcome_commitment is False
            and bundle.generated_record_rewrite is False
            and bundle.generated_resolution is False
            and all(
                not route.commits_outcome and not route.rewrites_record and not route.resolves_conflict
                for route in bundle.result_routes
            )
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="mediation_selection_controller_result_3049_3098_observed_without_selection_or_resolution",
    )


def run_checks() -> None:
    observation = observe_mediation_selection_controller_result()
    bundle = observation.bundle

    assert observation.source_status == "mediation_selection_controller_boundary_2999_3048_observed_without_result_or_selection"
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 3049
    assert observation.steps[-1].number == 3098
    assert observation.every_controller_gets_result_route is True
    assert observation.result_variety_preserved is True
    assert observation.controller_record_mediation_traces_preserved is True
    assert observation.result_generated_without_selection is True
    assert observation.no_commitment_rewrite_or_resolution is True
    assert len(bundle.result_routes) == 3
    assert len(bundle.contextual_results) == 1
    assert len(bundle.hearing_shift_results) == 1
    assert len(bundle.reference_results) == 1
    assert bundle.generated_controller_result is True
    assert bundle.generated_outcome_selection is False
    assert bundle.generated_outcome_commitment is False
    assert bundle.generated_record_rewrite is False
    assert bundle.generated_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_mediation_outcome_selection_candidate_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_mediation_selection_controller_result().status)
