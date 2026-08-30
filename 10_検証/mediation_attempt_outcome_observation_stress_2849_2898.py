"""mediation outcome attemptをoutcome observationへ渡す最小実験。"""

from dataclasses import dataclass

from mediation_outcome_attempt_boundary_stress_2799_2848 import (
    MediationOutcomeAttemptBundle,
    MediationOutcomeAttemptRoute,
    observe_mediation_outcome_attempt,
)


@dataclass(frozen=True)
class MediationAttemptOutcomeObservationStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class MediationAttemptOutcomeObservedRoute:
    source_attempt: MediationOutcomeAttemptRoute
    observation_kind: str
    observed_content: str
    preserves_attempt_trace: bool
    preserves_mediation_trace: bool
    preserves_commitment_trace: bool
    preserves_conflict_trace: bool
    creates_outcome_observation: bool
    records_outcome: bool
    selects_outcome: bool
    finalizes_judgement: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class MediationAttemptOutcomeObservationBundle:
    source_bundle: MediationOutcomeAttemptBundle
    observed_routes: tuple[MediationAttemptOutcomeObservedRoute, ...]
    contextual_observations: tuple[MediationAttemptOutcomeObservedRoute, ...]
    hearing_shift_observations: tuple[MediationAttemptOutcomeObservedRoute, ...]
    reference_observations: tuple[MediationAttemptOutcomeObservedRoute, ...]
    stop_lines: tuple[str, ...]
    generated_outcome_observation: bool
    generated_outcome_record: bool
    generated_outcome_selection: bool
    generated_final_judgement: bool
    generated_resolution: bool
    status: str


@dataclass(frozen=True)
class MediationAttemptOutcomeObservation:
    source_status: str
    steps: tuple[MediationAttemptOutcomeObservationStep, ...]
    bundle: MediationAttemptOutcomeObservationBundle
    every_attempt_gets_observation_route: bool
    observation_variety_preserved: bool
    attempt_mediation_conflict_traces_preserved: bool
    observation_generated_without_record: bool
    no_selection_judgement_or_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2849, "source_reentry", "reuse_2799_2848_mediation_outcome_attempt", "mediation_outcome_attempt_preserved"),
    (2850, "source_reentry", "next_xi_received", "mediation_attempt_outcome_observation_stress_received"),
    (2851, "source_reentry", "attempt_routes_recheck", "attempt_routes_available"),
    (2852, "observation_request", "mediation_attempt_outcome_observation_request", "mediation_attempt_outcome_observation_candidate"),
    (2853, "observation_request", "observation_not_outcome_record_guard", "outcome_record_non_identity_preserved"),
    (2854, "observation_request", "observation_not_outcome_selection_guard", "outcome_selection_blocked"),
    (2855, "observation_request", "observation_not_final_judgement_guard", "final_judgement_non_identity_preserved"),
    (2856, "observation_layer", "outcome_observation_generation", "outcome_observation_routes_recorded"),
    (2857, "observation_layer", "contextual_outcome_observation", "contextual_outcome_observation_recorded"),
    (2858, "observation_layer", "hearing_shift_outcome_observation", "hearing_shift_outcome_observation_recorded"),
    (2859, "observation_layer", "reference_outcome_observation", "reference_outcome_observation_recorded"),
    (2860, "observation_layer", "creates_outcome_observation_true", "creates_outcome_observation_true_recorded"),
    (2861, "observation_layer", "records_outcome_false", "records_outcome_false_recorded"),
    (2862, "observation_layer", "selects_outcome_false", "selects_outcome_false_recorded"),
    (2863, "observation_content_layer", "phrase_reentry_observed_content", "phrase_reentry_observed_content_recorded"),
    (2864, "observation_content_layer", "weight_rehearing_observed_content", "weight_rehearing_observed_content_recorded"),
    (2865, "observation_content_layer", "reference_scope_observed_content", "reference_scope_observed_content_recorded"),
    (2866, "observation_content_layer", "attempt_trace_carry", "attempt_trace_carried"),
    (2867, "observation_content_layer", "mediation_trace_carry", "mediation_trace_carried"),
    (2868, "observation_content_layer", "commitment_conflict_trace_carry", "commitment_conflict_trace_carried"),
    (2869, "partition_layer", "contextual_observation_partition", "contextual_observation_partition_recorded"),
    (2870, "partition_layer", "hearing_shift_observation_partition", "hearing_shift_observation_partition_recorded"),
    (2871, "partition_layer", "reference_observation_partition", "reference_observation_partition_recorded"),
    (2872, "partition_layer", "observation_partition_not_record_guard", "partition_record_non_identity"),
    (2873, "partition_layer", "observation_partition_not_solution_guard", "partition_solution_non_identity"),
    (2874, "observation_view", "mediation_attempt_outcome_observation_view", "mediation_attempt_outcome_observation_view_created"),
    (2875, "observation_view", "contextual_observation_view", "contextual_observation_view_created"),
    (2876, "observation_view", "hearing_shift_observation_view", "hearing_shift_observation_view_created"),
    (2877, "observation_view", "reference_observation_view", "reference_observation_view_created"),
    (2878, "bundle", "mediation_attempt_outcome_observation_bundle_creation", "mediation_attempt_outcome_observation_bundle_created"),
    (2879, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2880, "bundle", "stop_lines_carry", "mediation_attempt_outcome_observation_stop_lines_carried"),
    (2881, "bundle", "generated_outcome_observation_true", "generated_outcome_observation_true_recorded"),
    (2882, "bundle", "generated_outcome_record_false", "generated_outcome_record_false_recorded"),
    (2883, "bundle", "generated_outcome_selection_false", "generated_outcome_selection_false_recorded"),
    (2884, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (2885, "integrity", "every_attempt_gets_observation_route_check", "every_attempt_gets_observation_route_confirmed"),
    (2886, "integrity", "observation_variety_preservation_check", "observation_variety_preservation_confirmed"),
    (2887, "integrity", "attempt_mediation_conflict_trace_check", "attempt_mediation_conflict_trace_confirmed"),
    (2888, "integrity", "observation_without_record_check", "observation_without_record_confirmed"),
    (2889, "integrity", "no_outcome_selection_check", "no_outcome_selection_confirmed"),
    (2890, "integrity", "no_final_judgement_or_resolution_check", "no_final_judgement_or_resolution_confirmed"),
    (2891, "non_identity", "observation_vs_record_split", "observation_record_non_identity"),
    (2892, "non_identity", "observation_vs_selection_split", "observation_selection_non_identity"),
    (2893, "non_identity", "observation_vs_resolution_split", "observation_resolution_non_identity"),
    (2894, "music_subject", "observation_as_mediated_listening_result_seen", "mediated_listening_result_seen_preserved"),
    (2895, "music_subject", "contextual_observation_as_phrase_reentry_heard", "phrase_reentry_heard_preserved"),
    (2896, "music_subject", "hearing_shift_observation_as_weight_rehearing_heard", "weight_rehearing_heard_preserved"),
    (2897, "summary", "mediation_attempt_outcome_observation_summary", "mediation_attempt_outcome_observation_observed"),
    (2898, "next_plan", "next_xi_selection", "xi_mediation_outcome_observation_record_boundary_stress"),
)


def _build_steps() -> tuple[MediationAttemptOutcomeObservationStep, ...]:
    previous = "mediation_outcome_attempt_boundary_2799_2848"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(MediationAttemptOutcomeObservationStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _observed_route(attempt: MediationOutcomeAttemptRoute) -> MediationAttemptOutcomeObservedRoute:
    if attempt.attempt_kind == "contextual_outcome_attempt":
        kind = "contextual_outcome_observation"
        content = "later_phrase_context_reentry_observed_without_record"
    elif attempt.attempt_kind == "hearing_shift_outcome_attempt":
        kind = "hearing_shift_outcome_observation"
        content = "returned_weight_rehearing_observed_without_selection"
    else:
        kind = "reference_outcome_observation"
        content = "reference_scope_continuation_observed_without_resolution"

    return MediationAttemptOutcomeObservedRoute(
        source_attempt=attempt,
        observation_kind=kind,
        observed_content=content,
        preserves_attempt_trace=True,
        preserves_mediation_trace=attempt.preserves_mediation_trace,
        preserves_commitment_trace=attempt.preserves_commitment_trace,
        preserves_conflict_trace=attempt.preserves_conflict_trace,
        creates_outcome_observation=True,
        records_outcome=False,
        selects_outcome=False,
        finalizes_judgement=False,
        resolves_conflict=False,
        status="mediation_attempt_outcome_observation_recorded_without_record_or_resolution",
    )


def build_mediation_attempt_outcome_observation_bundle(
    source: MediationOutcomeAttemptBundle,
) -> MediationAttemptOutcomeObservationBundle:
    routes = tuple(_observed_route(attempt) for attempt in source.attempt_routes)
    contextual = tuple(route for route in routes if route.observation_kind == "contextual_outcome_observation")
    hearing_shift = tuple(route for route in routes if route.observation_kind == "hearing_shift_outcome_observation")
    reference = tuple(route for route in routes if route.observation_kind == "reference_outcome_observation")
    return MediationAttemptOutcomeObservationBundle(
        source_bundle=source,
        observed_routes=routes,
        contextual_observations=contextual,
        hearing_shift_observations=hearing_shift,
        reference_observations=reference,
        stop_lines=(
            "observation_not_outcome_record",
            "observation_not_outcome_selection",
            "observation_not_final_judgement",
            "observation_not_resolution",
            "observation_not_solution",
        ),
        generated_outcome_observation=True,
        generated_outcome_record=False,
        generated_outcome_selection=False,
        generated_final_judgement=False,
        generated_resolution=False,
        status="mediation_attempt_outcome_observation_bundle_2849_2898_built_without_record_or_resolution",
    )


def observe_mediation_attempt_outcome_observation() -> MediationAttemptOutcomeObservation:
    source = observe_mediation_outcome_attempt()
    bundle = build_mediation_attempt_outcome_observation_bundle(source.bundle)
    steps = _build_steps()

    return MediationAttemptOutcomeObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_attempt_gets_observation_route=(len(bundle.observed_routes) == len(source.bundle.attempt_routes)),
        observation_variety_preserved=(
            len(bundle.contextual_observations) == 1
            and len(bundle.hearing_shift_observations) == 1
            and len(bundle.reference_observations) == 1
        ),
        attempt_mediation_conflict_traces_preserved=all(
            route.preserves_attempt_trace
            and route.preserves_mediation_trace
            and route.preserves_commitment_trace
            and route.preserves_conflict_trace
            for route in bundle.observed_routes
        ),
        observation_generated_without_record=(
            bundle.generated_outcome_observation is True
            and bundle.generated_outcome_record is False
            and all(route.creates_outcome_observation and not route.records_outcome for route in bundle.observed_routes)
        ),
        no_selection_judgement_or_resolution=(
            bundle.generated_outcome_selection is False
            and bundle.generated_final_judgement is False
            and bundle.generated_resolution is False
            and all(
                not route.selects_outcome and not route.finalizes_judgement and not route.resolves_conflict
                for route in bundle.observed_routes
            )
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="mediation_attempt_outcome_observation_2849_2898_observed_without_record_or_resolution",
    )


def run_checks() -> None:
    observation = observe_mediation_attempt_outcome_observation()
    bundle = observation.bundle

    assert observation.source_status == (
        "mediation_outcome_attempt_boundary_2799_2848_observed_without_observation_or_resolution"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2849
    assert observation.steps[-1].number == 2898
    assert observation.every_attempt_gets_observation_route is True
    assert observation.observation_variety_preserved is True
    assert observation.attempt_mediation_conflict_traces_preserved is True
    assert observation.observation_generated_without_record is True
    assert observation.no_selection_judgement_or_resolution is True
    assert len(bundle.observed_routes) == 3
    assert len(bundle.contextual_observations) == 1
    assert len(bundle.hearing_shift_observations) == 1
    assert len(bundle.reference_observations) == 1
    assert bundle.generated_outcome_observation is True
    assert bundle.generated_outcome_record is False
    assert bundle.generated_outcome_selection is False
    assert bundle.generated_final_judgement is False
    assert bundle.generated_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_mediation_outcome_observation_record_boundary_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_mediation_attempt_outcome_observation().status)
