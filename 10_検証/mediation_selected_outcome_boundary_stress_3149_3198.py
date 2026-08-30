"""mediation outcome selection candidateをselected outcome boundaryへ渡す最小実験。"""

from dataclasses import dataclass

from mediation_outcome_selection_candidate_stress_3099_3148 import (
    MediationOutcomeSelectionCandidateBundle,
    MediationOutcomeSelectionCandidateRoute,
    observe_mediation_outcome_selection_candidate,
)


@dataclass(frozen=True)
class MediationSelectedOutcomeStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class MediationSelectedOutcomeRoute:
    source_candidate: MediationOutcomeSelectionCandidateRoute
    selected_kind: str
    selected_basis: str
    preserves_candidate_trace: bool
    preserves_result_trace: bool
    preserves_record_trace: bool
    preserves_commitment_trace: bool
    preserves_conflict_trace: bool
    creates_selected_outcome: bool
    commits_outcome: bool
    rewrites_record: bool
    cancels_alternatives: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class MediationSelectedOutcomeBundle:
    source_bundle: MediationOutcomeSelectionCandidateBundle
    selected_routes: tuple[MediationSelectedOutcomeRoute, ...]
    contextual_selected: tuple[MediationSelectedOutcomeRoute, ...]
    hearing_shift_selected: tuple[MediationSelectedOutcomeRoute, ...]
    reference_selected: tuple[MediationSelectedOutcomeRoute, ...]
    stop_lines: tuple[str, ...]
    generated_selected_outcome: bool
    generated_outcome_commitment: bool
    generated_record_rewrite: bool
    generated_alternative_cancellation: bool
    generated_resolution: bool
    status: str


@dataclass(frozen=True)
class MediationSelectedOutcomeObservation:
    source_status: str
    steps: tuple[MediationSelectedOutcomeStep, ...]
    bundle: MediationSelectedOutcomeBundle
    every_candidate_gets_selected_route: bool
    selected_variety_preserved: bool
    candidate_result_record_traces_preserved: bool
    selected_generated_without_commitment: bool
    no_rewrite_cancellation_or_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (3149, "source_reentry", "reuse_3099_3148_mediation_outcome_selection_candidate", "mediation_outcome_selection_candidate_preserved"),
    (3150, "source_reentry", "next_xi_received", "mediation_selected_outcome_boundary_stress_received"),
    (3151, "source_reentry", "selection_candidate_routes_recheck", "selection_candidate_routes_available"),
    (3152, "selected_request", "mediation_selected_outcome_boundary_request", "mediation_selected_outcome_boundary_candidate"),
    (3153, "selected_request", "selected_outcome_not_commitment_guard", "outcome_commitment_non_identity_preserved"),
    (3154, "selected_request", "selected_outcome_not_record_rewrite_guard", "record_rewrite_blocked"),
    (3155, "selected_request", "selected_outcome_not_resolution_guard", "resolution_non_identity_preserved"),
    (3156, "selected_layer", "selected_outcome_generation", "selected_outcome_routes_recorded"),
    (3157, "selected_layer", "contextual_selected_outcome", "contextual_selected_outcome_recorded"),
    (3158, "selected_layer", "hearing_shift_selected_outcome", "hearing_shift_selected_outcome_recorded"),
    (3159, "selected_layer", "reference_selected_outcome", "reference_selected_outcome_recorded"),
    (3160, "selected_layer", "creates_selected_outcome_true", "creates_selected_outcome_true_recorded"),
    (3161, "selected_layer", "commits_outcome_false", "commits_outcome_false_recorded"),
    (3162, "selected_layer", "rewrites_record_false", "rewrites_record_false_recorded"),
    (3163, "selected_basis_layer", "phrase_trace_selected_basis", "phrase_trace_selected_basis_recorded"),
    (3164, "selected_basis_layer", "weight_trace_selected_basis", "weight_trace_selected_basis_recorded"),
    (3165, "selected_basis_layer", "reference_trace_selected_basis", "reference_trace_selected_basis_recorded"),
    (3166, "selected_basis_layer", "candidate_trace_carry", "candidate_trace_carried"),
    (3167, "selected_basis_layer", "result_trace_carry", "result_trace_carried"),
    (3168, "selected_basis_layer", "record_commitment_conflict_trace_carry", "record_commitment_conflict_trace_carried"),
    (3169, "partition_layer", "contextual_selected_partition", "contextual_selected_partition_recorded"),
    (3170, "partition_layer", "hearing_shift_selected_partition", "hearing_shift_selected_partition_recorded"),
    (3171, "partition_layer", "reference_selected_partition", "reference_selected_partition_recorded"),
    (3172, "partition_layer", "selected_partition_not_commitment_guard", "partition_commitment_non_identity"),
    (3173, "partition_layer", "selected_partition_not_solution_guard", "partition_solution_non_identity"),
    (3174, "selected_view", "mediation_selected_outcome_view", "mediation_selected_outcome_view_created"),
    (3175, "selected_view", "contextual_selected_view", "contextual_selected_view_created"),
    (3176, "selected_view", "hearing_shift_selected_view", "hearing_shift_selected_view_created"),
    (3177, "selected_view", "reference_selected_view", "reference_selected_view_created"),
    (3178, "bundle", "mediation_selected_outcome_bundle_creation", "mediation_selected_outcome_bundle_created"),
    (3179, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (3180, "bundle", "stop_lines_carry", "mediation_selected_outcome_stop_lines_carried"),
    (3181, "bundle", "generated_selected_outcome_true", "generated_selected_outcome_true_recorded"),
    (3182, "bundle", "generated_outcome_commitment_false", "generated_outcome_commitment_false_recorded"),
    (3183, "bundle", "generated_alternative_cancellation_false", "generated_alternative_cancellation_false_recorded"),
    (3184, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (3185, "integrity", "every_candidate_gets_selected_route_check", "every_candidate_gets_selected_route_confirmed"),
    (3186, "integrity", "selected_variety_preservation_check", "selected_variety_preservation_confirmed"),
    (3187, "integrity", "candidate_result_record_trace_check", "candidate_result_record_trace_confirmed"),
    (3188, "integrity", "selected_without_commitment_check", "selected_without_commitment_confirmed"),
    (3189, "integrity", "no_record_rewrite_check", "no_record_rewrite_confirmed"),
    (3190, "integrity", "no_cancellation_or_resolution_check", "no_cancellation_or_resolution_confirmed"),
    (3191, "non_identity", "selected_vs_commitment_split", "selected_commitment_non_identity"),
    (3192, "non_identity", "selected_vs_record_rewrite_split", "selected_record_rewrite_non_identity"),
    (3193, "non_identity", "selected_vs_resolution_split", "selected_resolution_non_identity"),
    (3194, "music_subject", "selected_as_provisional_mediated_hearing", "provisional_mediated_hearing_preserved"),
    (3195, "music_subject", "contextual_selected_as_phrase_trace_precommitment", "phrase_trace_precommitment_preserved"),
    (3196, "music_subject", "hearing_shift_selected_as_weight_trace_precommitment", "weight_trace_precommitment_preserved"),
    (3197, "summary", "mediation_selected_outcome_summary", "mediation_selected_outcome_observed"),
    (3198, "next_plan", "next_xi_selection", "xi_mediation_selected_outcome_commitment_readiness_stress"),
)


def _build_steps() -> tuple[MediationSelectedOutcomeStep, ...]:
    previous = "mediation_outcome_selection_candidate_3099_3148"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(MediationSelectedOutcomeStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _selected_route(candidate: MediationOutcomeSelectionCandidateRoute) -> MediationSelectedOutcomeRoute:
    if candidate.candidate_kind == "contextual_selection_candidate":
        kind = "contextual_selected_outcome"
        basis = "phrase_trace_candidate_selected_without_commitment"
    elif candidate.candidate_kind == "hearing_shift_selection_candidate":
        kind = "hearing_shift_selected_outcome"
        basis = "weight_trace_candidate_selected_without_record_rewrite"
    else:
        kind = "reference_selected_outcome"
        basis = "reference_trace_candidate_selected_without_resolution"

    return MediationSelectedOutcomeRoute(
        source_candidate=candidate,
        selected_kind=kind,
        selected_basis=basis,
        preserves_candidate_trace=True,
        preserves_result_trace=candidate.preserves_result_trace,
        preserves_record_trace=candidate.preserves_record_trace,
        preserves_commitment_trace=candidate.preserves_commitment_trace,
        preserves_conflict_trace=candidate.preserves_conflict_trace,
        creates_selected_outcome=True,
        commits_outcome=False,
        rewrites_record=False,
        cancels_alternatives=False,
        resolves_conflict=False,
        status="mediation_selected_outcome_recorded_without_commitment_or_resolution",
    )


def build_mediation_selected_outcome_bundle(
    source: MediationOutcomeSelectionCandidateBundle,
) -> MediationSelectedOutcomeBundle:
    routes = tuple(_selected_route(candidate) for candidate in source.candidate_routes)
    contextual = tuple(route for route in routes if route.selected_kind == "contextual_selected_outcome")
    hearing_shift = tuple(route for route in routes if route.selected_kind == "hearing_shift_selected_outcome")
    reference = tuple(route for route in routes if route.selected_kind == "reference_selected_outcome")
    return MediationSelectedOutcomeBundle(
        source_bundle=source,
        selected_routes=routes,
        contextual_selected=contextual,
        hearing_shift_selected=hearing_shift,
        reference_selected=reference,
        stop_lines=(
            "selected_outcome_not_outcome_commitment",
            "selected_outcome_not_record_rewrite",
            "selected_outcome_not_alternative_cancellation",
            "selected_outcome_not_resolution",
            "selected_outcome_not_solution",
        ),
        generated_selected_outcome=True,
        generated_outcome_commitment=False,
        generated_record_rewrite=False,
        generated_alternative_cancellation=False,
        generated_resolution=False,
        status="mediation_selected_outcome_bundle_3149_3198_built_without_commitment_or_resolution",
    )


def observe_mediation_selected_outcome() -> MediationSelectedOutcomeObservation:
    source = observe_mediation_outcome_selection_candidate()
    bundle = build_mediation_selected_outcome_bundle(source.bundle)
    steps = _build_steps()

    return MediationSelectedOutcomeObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_candidate_gets_selected_route=(len(bundle.selected_routes) == len(source.bundle.candidate_routes)),
        selected_variety_preserved=(
            len(bundle.contextual_selected) == 1
            and len(bundle.hearing_shift_selected) == 1
            and len(bundle.reference_selected) == 1
        ),
        candidate_result_record_traces_preserved=all(
            route.preserves_candidate_trace
            and route.preserves_result_trace
            and route.preserves_record_trace
            and route.preserves_commitment_trace
            and route.preserves_conflict_trace
            for route in bundle.selected_routes
        ),
        selected_generated_without_commitment=(
            bundle.generated_selected_outcome is True
            and bundle.generated_outcome_commitment is False
            and all(route.creates_selected_outcome and not route.commits_outcome for route in bundle.selected_routes)
        ),
        no_rewrite_cancellation_or_resolution=(
            bundle.generated_record_rewrite is False
            and bundle.generated_alternative_cancellation is False
            and bundle.generated_resolution is False
            and all(
                not route.rewrites_record and not route.cancels_alternatives and not route.resolves_conflict
                for route in bundle.selected_routes
            )
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="mediation_selected_outcome_boundary_3149_3198_observed_without_commitment_or_resolution",
    )


def run_checks() -> None:
    observation = observe_mediation_selected_outcome()
    bundle = observation.bundle

    assert observation.source_status == "mediation_outcome_selection_candidate_3099_3148_observed_without_selection_or_resolution"
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 3149
    assert observation.steps[-1].number == 3198
    assert observation.every_candidate_gets_selected_route is True
    assert observation.selected_variety_preserved is True
    assert observation.candidate_result_record_traces_preserved is True
    assert observation.selected_generated_without_commitment is True
    assert observation.no_rewrite_cancellation_or_resolution is True
    assert len(bundle.selected_routes) == 3
    assert len(bundle.contextual_selected) == 1
    assert len(bundle.hearing_shift_selected) == 1
    assert len(bundle.reference_selected) == 1
    assert bundle.generated_selected_outcome is True
    assert bundle.generated_outcome_commitment is False
    assert bundle.generated_record_rewrite is False
    assert bundle.generated_alternative_cancellation is False
    assert bundle.generated_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_mediation_selected_outcome_commitment_readiness_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_mediation_selected_outcome().status)
