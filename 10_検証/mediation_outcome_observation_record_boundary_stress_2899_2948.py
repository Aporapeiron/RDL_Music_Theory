"""mediation outcome observationをrecord boundaryへ渡す最小実験。"""

from dataclasses import dataclass

from mediation_attempt_outcome_observation_stress_2849_2898 import (
    MediationAttemptOutcomeObservationBundle,
    MediationAttemptOutcomeObservedRoute,
    observe_mediation_attempt_outcome_observation,
)


@dataclass(frozen=True)
class MediationOutcomeObservationRecordStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class MediationOutcomeObservationRecordRoute:
    source_observation: MediationAttemptOutcomeObservedRoute
    record_kind: str
    record_content: str
    preserves_observation_trace: bool
    preserves_attempt_trace: bool
    preserves_mediation_trace: bool
    preserves_commitment_trace: bool
    preserves_conflict_trace: bool
    creates_observation_record: bool
    selects_outcome: bool
    commits_outcome: bool
    finalizes_judgement: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class MediationOutcomeObservationRecordBundle:
    source_bundle: MediationAttemptOutcomeObservationBundle
    record_routes: tuple[MediationOutcomeObservationRecordRoute, ...]
    contextual_records: tuple[MediationOutcomeObservationRecordRoute, ...]
    hearing_shift_records: tuple[MediationOutcomeObservationRecordRoute, ...]
    reference_records: tuple[MediationOutcomeObservationRecordRoute, ...]
    stop_lines: tuple[str, ...]
    generated_observation_record: bool
    generated_outcome_selection: bool
    generated_outcome_commitment: bool
    generated_final_judgement: bool
    generated_resolution: bool
    status: str


@dataclass(frozen=True)
class MediationOutcomeObservationRecordObservation:
    source_status: str
    steps: tuple[MediationOutcomeObservationRecordStep, ...]
    bundle: MediationOutcomeObservationRecordBundle
    every_observation_gets_record_route: bool
    record_variety_preserved: bool
    observation_attempt_mediation_traces_preserved: bool
    record_generated_without_selection: bool
    no_commitment_judgement_or_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2899, "source_reentry", "reuse_2849_2898_mediation_attempt_outcome_observation", "mediation_attempt_outcome_observation_preserved"),
    (2900, "source_reentry", "next_xi_received", "mediation_outcome_observation_record_boundary_stress_received"),
    (2901, "source_reentry", "observation_routes_recheck", "observation_routes_available"),
    (2902, "record_request", "mediation_outcome_observation_record_request", "mediation_outcome_observation_record_candidate"),
    (2903, "record_request", "record_not_outcome_selection_guard", "outcome_selection_non_identity_preserved"),
    (2904, "record_request", "record_not_outcome_commitment_guard", "outcome_commitment_blocked"),
    (2905, "record_request", "record_not_final_judgement_guard", "final_judgement_non_identity_preserved"),
    (2906, "record_layer", "observation_record_generation", "observation_record_routes_recorded"),
    (2907, "record_layer", "contextual_observation_record", "contextual_observation_recorded"),
    (2908, "record_layer", "hearing_shift_observation_record", "hearing_shift_observation_recorded"),
    (2909, "record_layer", "reference_observation_record", "reference_observation_recorded"),
    (2910, "record_layer", "creates_observation_record_true", "creates_observation_record_true_recorded"),
    (2911, "record_layer", "selects_outcome_false", "selects_outcome_false_recorded"),
    (2912, "record_layer", "commits_outcome_false", "commits_outcome_false_recorded"),
    (2913, "record_content_layer", "phrase_reentry_record_content", "phrase_reentry_record_content_recorded"),
    (2914, "record_content_layer", "weight_rehearing_record_content", "weight_rehearing_record_content_recorded"),
    (2915, "record_content_layer", "reference_scope_record_content", "reference_scope_record_content_recorded"),
    (2916, "record_content_layer", "observation_trace_carry", "observation_trace_carried"),
    (2917, "record_content_layer", "attempt_trace_carry", "attempt_trace_carried"),
    (2918, "record_content_layer", "mediation_commitment_conflict_trace_carry", "mediation_commitment_conflict_trace_carried"),
    (2919, "partition_layer", "contextual_record_partition", "contextual_record_partition_recorded"),
    (2920, "partition_layer", "hearing_shift_record_partition", "hearing_shift_record_partition_recorded"),
    (2921, "partition_layer", "reference_record_partition", "reference_record_partition_recorded"),
    (2922, "partition_layer", "record_partition_not_selection_guard", "partition_selection_non_identity"),
    (2923, "partition_layer", "record_partition_not_solution_guard", "partition_solution_non_identity"),
    (2924, "record_view", "mediation_outcome_observation_record_view", "mediation_outcome_observation_record_view_created"),
    (2925, "record_view", "contextual_record_view", "contextual_record_view_created"),
    (2926, "record_view", "hearing_shift_record_view", "hearing_shift_record_view_created"),
    (2927, "record_view", "reference_record_view", "reference_record_view_created"),
    (2928, "bundle", "mediation_outcome_observation_record_bundle_creation", "mediation_outcome_observation_record_bundle_created"),
    (2929, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2930, "bundle", "stop_lines_carry", "mediation_outcome_observation_record_stop_lines_carried"),
    (2931, "bundle", "generated_observation_record_true", "generated_observation_record_true_recorded"),
    (2932, "bundle", "generated_outcome_selection_false", "generated_outcome_selection_false_recorded"),
    (2933, "bundle", "generated_outcome_commitment_false", "generated_outcome_commitment_false_recorded"),
    (2934, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (2935, "integrity", "every_observation_gets_record_route_check", "every_observation_gets_record_route_confirmed"),
    (2936, "integrity", "record_variety_preservation_check", "record_variety_preservation_confirmed"),
    (2937, "integrity", "observation_attempt_mediation_trace_check", "observation_attempt_mediation_trace_confirmed"),
    (2938, "integrity", "record_without_selection_check", "record_without_selection_confirmed"),
    (2939, "integrity", "no_outcome_commitment_check", "no_outcome_commitment_confirmed"),
    (2940, "integrity", "no_final_judgement_or_resolution_check", "no_final_judgement_or_resolution_confirmed"),
    (2941, "non_identity", "record_vs_selection_split", "record_selection_non_identity"),
    (2942, "non_identity", "record_vs_commitment_split", "record_commitment_non_identity"),
    (2943, "non_identity", "record_vs_resolution_split", "record_resolution_non_identity"),
    (2944, "music_subject", "record_as_mediated_listening_trace", "mediated_listening_trace_preserved"),
    (2945, "music_subject", "contextual_record_as_phrase_reentry_trace", "phrase_reentry_trace_preserved"),
    (2946, "music_subject", "hearing_shift_record_as_weight_rehearing_trace", "weight_rehearing_trace_preserved"),
    (2947, "summary", "mediation_outcome_observation_record_summary", "mediation_outcome_observation_record_observed"),
    (2948, "next_plan", "next_xi_selection", "xi_mediation_record_selection_readiness_stress"),
)


def _build_steps() -> tuple[MediationOutcomeObservationRecordStep, ...]:
    previous = "mediation_attempt_outcome_observation_2849_2898"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(MediationOutcomeObservationRecordStep(number, phase, name, previous, result, False))
        previous = result
    return tuple(steps)


def _record_route(observation: MediationAttemptOutcomeObservedRoute) -> MediationOutcomeObservationRecordRoute:
    if observation.observation_kind == "contextual_outcome_observation":
        kind = "contextual_observation_record"
        content = "later_phrase_context_reentry_recorded_without_selection"
    elif observation.observation_kind == "hearing_shift_outcome_observation":
        kind = "hearing_shift_observation_record"
        content = "returned_weight_rehearing_recorded_without_commitment"
    else:
        kind = "reference_observation_record"
        content = "reference_scope_continuation_recorded_without_resolution"

    return MediationOutcomeObservationRecordRoute(
        source_observation=observation,
        record_kind=kind,
        record_content=content,
        preserves_observation_trace=True,
        preserves_attempt_trace=observation.preserves_attempt_trace,
        preserves_mediation_trace=observation.preserves_mediation_trace,
        preserves_commitment_trace=observation.preserves_commitment_trace,
        preserves_conflict_trace=observation.preserves_conflict_trace,
        creates_observation_record=True,
        selects_outcome=False,
        commits_outcome=False,
        finalizes_judgement=False,
        resolves_conflict=False,
        status="mediation_outcome_observation_recorded_without_selection_or_resolution",
    )


def build_mediation_outcome_observation_record_bundle(
    source: MediationAttemptOutcomeObservationBundle,
) -> MediationOutcomeObservationRecordBundle:
    routes = tuple(_record_route(observation) for observation in source.observed_routes)
    contextual = tuple(route for route in routes if route.record_kind == "contextual_observation_record")
    hearing_shift = tuple(route for route in routes if route.record_kind == "hearing_shift_observation_record")
    reference = tuple(route for route in routes if route.record_kind == "reference_observation_record")
    return MediationOutcomeObservationRecordBundle(
        source_bundle=source,
        record_routes=routes,
        contextual_records=contextual,
        hearing_shift_records=hearing_shift,
        reference_records=reference,
        stop_lines=(
            "record_not_outcome_selection",
            "record_not_outcome_commitment",
            "record_not_final_judgement",
            "record_not_resolution",
            "record_not_solution",
        ),
        generated_observation_record=True,
        generated_outcome_selection=False,
        generated_outcome_commitment=False,
        generated_final_judgement=False,
        generated_resolution=False,
        status="mediation_outcome_observation_record_bundle_2899_2948_built_without_selection_or_resolution",
    )


def observe_mediation_outcome_observation_record() -> MediationOutcomeObservationRecordObservation:
    source = observe_mediation_attempt_outcome_observation()
    bundle = build_mediation_outcome_observation_record_bundle(source.bundle)
    steps = _build_steps()

    return MediationOutcomeObservationRecordObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_observation_gets_record_route=(len(bundle.record_routes) == len(source.bundle.observed_routes)),
        record_variety_preserved=(
            len(bundle.contextual_records) == 1
            and len(bundle.hearing_shift_records) == 1
            and len(bundle.reference_records) == 1
        ),
        observation_attempt_mediation_traces_preserved=all(
            route.preserves_observation_trace
            and route.preserves_attempt_trace
            and route.preserves_mediation_trace
            and route.preserves_commitment_trace
            and route.preserves_conflict_trace
            for route in bundle.record_routes
        ),
        record_generated_without_selection=(
            bundle.generated_observation_record is True
            and bundle.generated_outcome_selection is False
            and all(route.creates_observation_record and not route.selects_outcome for route in bundle.record_routes)
        ),
        no_commitment_judgement_or_resolution=(
            bundle.generated_outcome_commitment is False
            and bundle.generated_final_judgement is False
            and bundle.generated_resolution is False
            and all(
                not route.commits_outcome and not route.finalizes_judgement and not route.resolves_conflict
                for route in bundle.record_routes
            )
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="mediation_outcome_observation_record_boundary_2899_2948_observed_without_selection_or_resolution",
    )


def run_checks() -> None:
    observation = observe_mediation_outcome_observation_record()
    bundle = observation.bundle

    assert observation.source_status == "mediation_attempt_outcome_observation_2849_2898_observed_without_record_or_resolution"
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2899
    assert observation.steps[-1].number == 2948
    assert observation.every_observation_gets_record_route is True
    assert observation.record_variety_preserved is True
    assert observation.observation_attempt_mediation_traces_preserved is True
    assert observation.record_generated_without_selection is True
    assert observation.no_commitment_judgement_or_resolution is True
    assert len(bundle.record_routes) == 3
    assert len(bundle.contextual_records) == 1
    assert len(bundle.hearing_shift_records) == 1
    assert len(bundle.reference_records) == 1
    assert bundle.generated_observation_record is True
    assert bundle.generated_outcome_selection is False
    assert bundle.generated_outcome_commitment is False
    assert bundle.generated_final_judgement is False
    assert bundle.generated_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_mediation_record_selection_readiness_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_mediation_outcome_observation_record().status)
