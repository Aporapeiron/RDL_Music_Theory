"""mediation selection controller resultをoutcome selection candidateへ渡す最小実験。"""

from dataclasses import dataclass

from mediation_selection_controller_result_stress_3049_3098 import (
    MediationSelectionControllerResultBundle,
    MediationSelectionControllerResultRoute,
    observe_mediation_selection_controller_result,
)


@dataclass(frozen=True)
class MediationOutcomeSelectionCandidateStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class MediationOutcomeSelectionCandidateRoute:
    source_result: MediationSelectionControllerResultRoute
    candidate_kind: str
    candidate_basis: str
    preserves_result_trace: bool
    preserves_controller_trace: bool
    preserves_record_trace: bool
    preserves_commitment_trace: bool
    preserves_conflict_trace: bool
    creates_selection_candidate: bool
    selects_outcome: bool
    commits_outcome: bool
    rewrites_record: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class MediationOutcomeSelectionCandidateBundle:
    source_bundle: MediationSelectionControllerResultBundle
    candidate_routes: tuple[MediationOutcomeSelectionCandidateRoute, ...]
    contextual_candidates: tuple[MediationOutcomeSelectionCandidateRoute, ...]
    hearing_shift_candidates: tuple[MediationOutcomeSelectionCandidateRoute, ...]
    reference_candidates: tuple[MediationOutcomeSelectionCandidateRoute, ...]
    stop_lines: tuple[str, ...]
    generated_selection_candidate: bool
    generated_outcome_selection: bool
    generated_outcome_commitment: bool
    generated_record_rewrite: bool
    generated_resolution: bool
    status: str


@dataclass(frozen=True)
class MediationOutcomeSelectionCandidateObservation:
    source_status: str
    steps: tuple[MediationOutcomeSelectionCandidateStep, ...]
    bundle: MediationOutcomeSelectionCandidateBundle
    every_result_gets_candidate_route: bool
    candidate_variety_preserved: bool
    result_controller_record_traces_preserved: bool
    candidate_generated_without_selection: bool
    no_commitment_rewrite_or_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (3099, "source_reentry", "reuse_3049_3098_mediation_selection_controller_result", "mediation_selection_controller_result_preserved"),
    (3100, "source_reentry", "next_xi_received", "mediation_outcome_selection_candidate_stress_received"),
    (3101, "source_reentry", "controller_result_routes_recheck", "controller_result_routes_available"),
    (3102, "candidate_request", "mediation_outcome_selection_candidate_request", "mediation_outcome_selection_candidate"),
    (3103, "candidate_request", "candidate_not_selected_outcome_guard", "selected_outcome_non_identity_preserved"),
    (3104, "candidate_request", "candidate_not_outcome_commitment_guard", "outcome_commitment_blocked"),
    (3105, "candidate_request", "candidate_not_record_rewrite_guard", "record_rewrite_non_identity_preserved"),
    (3106, "candidate_layer", "selection_candidate_generation", "selection_candidate_routes_recorded"),
    (3107, "candidate_layer", "contextual_selection_candidate", "contextual_selection_candidate_recorded"),
    (3108, "candidate_layer", "hearing_shift_selection_candidate", "hearing_shift_selection_candidate_recorded"),
    (3109, "candidate_layer", "reference_selection_candidate", "reference_selection_candidate_recorded"),
    (3110, "candidate_layer", "creates_selection_candidate_true", "creates_selection_candidate_true_recorded"),
    (3111, "candidate_layer", "selects_outcome_false", "selects_outcome_false_recorded"),
    (3112, "candidate_layer", "commits_outcome_false", "commits_outcome_false_recorded"),
    (3113, "candidate_basis_layer", "phrase_trace_candidate_basis", "phrase_trace_candidate_basis_recorded"),
    (3114, "candidate_basis_layer", "weight_trace_candidate_basis", "weight_trace_candidate_basis_recorded"),
    (3115, "candidate_basis_layer", "reference_trace_candidate_basis", "reference_trace_candidate_basis_recorded"),
    (3116, "candidate_basis_layer", "result_trace_carry", "result_trace_carried"),
    (3117, "candidate_basis_layer", "controller_trace_carry", "controller_trace_carried"),
    (3118, "candidate_basis_layer", "record_commitment_conflict_trace_carry", "record_commitment_conflict_trace_carried"),
    (3119, "partition_layer", "contextual_candidate_partition", "contextual_candidate_partition_recorded"),
    (3120, "partition_layer", "hearing_shift_candidate_partition", "hearing_shift_candidate_partition_recorded"),
    (3121, "partition_layer", "reference_candidate_partition", "reference_candidate_partition_recorded"),
    (3122, "partition_layer", "candidate_partition_not_selection_guard", "partition_selection_non_identity"),
    (3123, "partition_layer", "candidate_partition_not_solution_guard", "partition_solution_non_identity"),
    (3124, "candidate_view", "mediation_outcome_selection_candidate_view", "mediation_outcome_selection_candidate_view_created"),
    (3125, "candidate_view", "contextual_candidate_view", "contextual_candidate_view_created"),
    (3126, "candidate_view", "hearing_shift_candidate_view", "hearing_shift_candidate_view_created"),
    (3127, "candidate_view", "reference_candidate_view", "reference_candidate_view_created"),
    (3128, "bundle", "mediation_outcome_selection_candidate_bundle_creation", "mediation_outcome_selection_candidate_bundle_created"),
    (3129, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (3130, "bundle", "stop_lines_carry", "mediation_outcome_selection_candidate_stop_lines_carried"),
    (3131, "bundle", "generated_selection_candidate_true", "generated_selection_candidate_true_recorded"),
    (3132, "bundle", "generated_outcome_selection_false", "generated_outcome_selection_false_recorded"),
    (3133, "bundle", "generated_record_rewrite_false", "generated_record_rewrite_false_recorded"),
    (3134, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (3135, "integrity", "every_result_gets_candidate_route_check", "every_result_gets_candidate_route_confirmed"),
    (3136, "integrity", "candidate_variety_preservation_check", "candidate_variety_preservation_confirmed"),
    (3137, "integrity", "result_controller_record_trace_check", "result_controller_record_trace_confirmed"),
    (3138, "integrity", "candidate_without_selection_check", "candidate_without_selection_confirmed"),
    (3139, "integrity", "no_outcome_commitment_check", "no_outcome_commitment_confirmed"),
    (3140, "integrity", "no_rewrite_or_resolution_check", "no_rewrite_or_resolution_confirmed"),
    (3141, "non_identity", "candidate_vs_selection_split", "candidate_selection_non_identity"),
    (3142, "non_identity", "candidate_vs_commitment_split", "candidate_commitment_non_identity"),
    (3143, "non_identity", "candidate_vs_resolution_split", "candidate_resolution_non_identity"),
    (3144, "music_subject", "candidate_as_possible_selection_from_mediated_result", "possible_mediated_selection_preserved"),
    (3145, "music_subject", "contextual_candidate_as_phrase_trace_selection_possibility", "phrase_trace_selection_possibility_preserved"),
    (3146, "music_subject", "hearing_shift_candidate_as_weight_trace_selection_possibility", "weight_trace_selection_possibility_preserved"),
    (3147, "summary", "mediation_outcome_selection_candidate_summary", "mediation_outcome_selection_candidate_observed"),
    (3148, "next_plan", "next_xi_selection", "xi_mediation_selected_outcome_boundary_stress"),
)


def _build_steps() -> tuple[MediationOutcomeSelectionCandidateStep, ...]:
    previous = "mediation_selection_controller_result_3049_3098"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(MediationOutcomeSelectionCandidateStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _candidate_route(result: MediationSelectionControllerResultRoute) -> MediationOutcomeSelectionCandidateRoute:
    if result.result_kind == "contextual_controller_result":
        kind = "contextual_selection_candidate"
        basis = "phrase_trace_result_can_become_candidate_without_selection"
    elif result.result_kind == "hearing_shift_controller_result":
        kind = "hearing_shift_selection_candidate"
        basis = "weight_trace_result_can_become_candidate_without_commitment"
    else:
        kind = "reference_selection_candidate"
        basis = "reference_trace_result_can_become_candidate_without_resolution"

    return MediationOutcomeSelectionCandidateRoute(
        source_result=result,
        candidate_kind=kind,
        candidate_basis=basis,
        preserves_result_trace=True,
        preserves_controller_trace=result.preserves_controller_trace,
        preserves_record_trace=result.preserves_record_trace,
        preserves_commitment_trace=result.preserves_commitment_trace,
        preserves_conflict_trace=result.preserves_conflict_trace,
        creates_selection_candidate=True,
        selects_outcome=False,
        commits_outcome=False,
        rewrites_record=False,
        resolves_conflict=False,
        status="mediation_outcome_selection_candidate_recorded_without_selection_or_resolution",
    )


def build_mediation_outcome_selection_candidate_bundle(
    source: MediationSelectionControllerResultBundle,
) -> MediationOutcomeSelectionCandidateBundle:
    routes = tuple(_candidate_route(result) for result in source.result_routes)
    contextual = tuple(route for route in routes if route.candidate_kind == "contextual_selection_candidate")
    hearing_shift = tuple(route for route in routes if route.candidate_kind == "hearing_shift_selection_candidate")
    reference = tuple(route for route in routes if route.candidate_kind == "reference_selection_candidate")
    return MediationOutcomeSelectionCandidateBundle(
        source_bundle=source,
        candidate_routes=routes,
        contextual_candidates=contextual,
        hearing_shift_candidates=hearing_shift,
        reference_candidates=reference,
        stop_lines=(
            "candidate_not_selected_outcome",
            "candidate_not_outcome_commitment",
            "candidate_not_record_rewrite",
            "candidate_not_resolution",
            "candidate_not_solution",
        ),
        generated_selection_candidate=True,
        generated_outcome_selection=False,
        generated_outcome_commitment=False,
        generated_record_rewrite=False,
        generated_resolution=False,
        status="mediation_outcome_selection_candidate_bundle_3099_3148_built_without_selection_or_resolution",
    )


def observe_mediation_outcome_selection_candidate() -> MediationOutcomeSelectionCandidateObservation:
    source = observe_mediation_selection_controller_result()
    bundle = build_mediation_outcome_selection_candidate_bundle(source.bundle)
    steps = _build_steps()

    return MediationOutcomeSelectionCandidateObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_result_gets_candidate_route=(len(bundle.candidate_routes) == len(source.bundle.result_routes)),
        candidate_variety_preserved=(
            len(bundle.contextual_candidates) == 1
            and len(bundle.hearing_shift_candidates) == 1
            and len(bundle.reference_candidates) == 1
        ),
        result_controller_record_traces_preserved=all(
            route.preserves_result_trace
            and route.preserves_controller_trace
            and route.preserves_record_trace
            and route.preserves_commitment_trace
            and route.preserves_conflict_trace
            for route in bundle.candidate_routes
        ),
        candidate_generated_without_selection=(
            bundle.generated_selection_candidate is True
            and bundle.generated_outcome_selection is False
            and all(route.creates_selection_candidate and not route.selects_outcome for route in bundle.candidate_routes)
        ),
        no_commitment_rewrite_or_resolution=(
            bundle.generated_outcome_commitment is False
            and bundle.generated_record_rewrite is False
            and bundle.generated_resolution is False
            and all(
                not route.commits_outcome and not route.rewrites_record and not route.resolves_conflict
                for route in bundle.candidate_routes
            )
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="mediation_outcome_selection_candidate_3099_3148_observed_without_selection_or_resolution",
    )


def run_checks() -> None:
    observation = observe_mediation_outcome_selection_candidate()
    bundle = observation.bundle

    assert observation.source_status == "mediation_selection_controller_result_3049_3098_observed_without_selection_or_resolution"
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 3099
    assert observation.steps[-1].number == 3148
    assert observation.every_result_gets_candidate_route is True
    assert observation.candidate_variety_preserved is True
    assert observation.result_controller_record_traces_preserved is True
    assert observation.candidate_generated_without_selection is True
    assert observation.no_commitment_rewrite_or_resolution is True
    assert len(bundle.candidate_routes) == 3
    assert len(bundle.contextual_candidates) == 1
    assert len(bundle.hearing_shift_candidates) == 1
    assert len(bundle.reference_candidates) == 1
    assert bundle.generated_selection_candidate is True
    assert bundle.generated_outcome_selection is False
    assert bundle.generated_outcome_commitment is False
    assert bundle.generated_record_rewrite is False
    assert bundle.generated_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_mediation_selected_outcome_boundary_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_mediation_outcome_selection_candidate().status)
