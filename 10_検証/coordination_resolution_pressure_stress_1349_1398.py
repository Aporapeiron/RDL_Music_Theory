"""polyphonic coordinationに生じるresolution pressureを検査する最小実験。"""

from dataclasses import dataclass

from polyphonic_memory_coordination_stress_1299_1348 import (
    PolyphonicMemoryCoordinationBundle,
    TrackCoordinationState,
    observe_polyphonic_memory_coordination,
)


@dataclass(frozen=True)
class CoordinationResolutionPressureStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ResolutionPressureSignal:
    name: str
    source_state: str
    pressure_kind: str
    pressure_level: float
    requests_resolution: bool
    forces_resolution: bool
    status: str


@dataclass(frozen=True)
class DeferredResolutionState:
    track_state: TrackCoordinationState
    pressure_signals: tuple[str, ...]
    deferred_reason: str
    keeps_polyphony: bool
    keeps_interference: bool
    collapses_to_single_voice: bool
    deleted: bool
    status: str


@dataclass(frozen=True)
class CoordinationResolutionPressureBundle:
    source_bundle: PolyphonicMemoryCoordinationBundle
    pressure_signals: tuple[ResolutionPressureSignal, ...]
    deferred_states: tuple[DeferredResolutionState, ...]
    pressure_mode: str
    stop_lines: tuple[str, ...]
    generated_final_resolution: bool
    generated_sync_collapse: bool
    generated_single_voice: bool
    generated_deletion: bool
    status: str


@dataclass(frozen=True)
class CoordinationResolutionPressureObservation:
    source_status: str
    steps: tuple[CoordinationResolutionPressureStep, ...]
    bundle: CoordinationResolutionPressureBundle
    pressure_observed_without_resolution: bool
    deferred_states_preserve_polyphony: bool
    interference_retained_under_pressure: bool
    no_sync_or_single_voice_collapse: bool
    latent_pressure_not_deleted: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1349, "source_reentry", "reuse_1299_1348_polyphonic_coordination", "polyphonic_coordination_preserved"),
    (1350, "source_reentry", "next_xi_received", "coordination_resolution_pressure_stress_received"),
    (1351, "source_reentry", "coordination_states_recheck", "coordination_states_available"),
    (1352, "pressure_request", "resolution_pressure_request", "resolution_pressure_candidate"),
    (1353, "pressure_request", "pressure_not_resolution_guard", "pressure_resolution_non_identity"),
    (1354, "pressure_request", "pressure_not_sync_guard", "pressure_sync_non_identity"),
    (1355, "pressure_request", "pressure_not_single_voice_guard", "single_voice_collapse_blocked"),
    (1356, "pressure_layer", "cadential_resolution_pressure", "cadential_resolution_pressure_recorded"),
    (1357, "pressure_layer", "B_coloring_resolution_pressure", "B_coloring_resolution_pressure_recorded"),
    (1358, "pressure_layer", "latent_echo_resolution_pressure", "latent_echo_resolution_pressure_recorded"),
    (1359, "pressure_layer", "pressure_level_record", "pressure_level_recorded"),
    (1360, "pressure_guard", "request_not_force_check", "request_force_split_confirmed"),
    (1361, "pressure_guard", "pressure_not_truth_check", "pressure_truth_non_identity"),
    (1362, "pressure_guard", "pressure_not_track_merge_check", "pressure_track_merge_non_identity"),
    (1363, "defer_layer", "primary_deferred_resolution_state", "primary_deferred_resolution_state_recorded"),
    (1364, "defer_layer", "derivative_deferred_resolution_state", "derivative_deferred_resolution_state_recorded"),
    (1365, "defer_layer", "latent_deferred_resolution_state", "latent_deferred_resolution_state_recorded"),
    (1366, "defer_layer", "deferred_reason_record", "deferred_reason_recorded"),
    (1367, "defer_layer", "polyphony_preservation_record", "polyphony_preservation_recorded"),
    (1368, "defer_layer", "interference_preservation_record", "interference_preservation_recorded"),
    (1369, "defer_layer", "single_voice_false_record", "single_voice_false_recorded"),
    (1370, "defer_layer", "deletion_false_record", "deletion_false_recorded"),
    (1371, "pressure_view", "pressure_mode_record", "pressure_mode_recorded"),
    (1372, "pressure_view", "deferred_resolution_view", "deferred_resolution_view_created"),
    (1373, "pressure_view", "unresolved_tension_view", "unresolved_tension_view_created"),
    (1374, "pressure_view", "latent_pressure_view", "latent_pressure_view_created"),
    (1375, "bundle", "coordination_resolution_pressure_bundle_creation", "coordination_resolution_pressure_bundle_created"),
    (1376, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1377, "bundle", "stop_lines_carry", "resolution_pressure_stop_lines_carried"),
    (1378, "bundle", "generated_final_resolution_false", "generated_final_resolution_false_recorded"),
    (1379, "bundle", "generated_sync_collapse_false", "generated_sync_collapse_false_recorded"),
    (1380, "bundle", "generated_single_voice_false", "generated_single_voice_false_recorded"),
    (1381, "bundle", "generated_deletion_false", "generated_deletion_false_recorded"),
    (1382, "integrity", "pressure_without_resolution_check", "pressure_without_resolution_confirmed"),
    (1383, "integrity", "deferred_polyphony_check", "deferred_polyphony_confirmed"),
    (1384, "integrity", "interference_under_pressure_check", "interference_under_pressure_confirmed"),
    (1385, "integrity", "sync_single_voice_split_check", "sync_single_voice_split_confirmed"),
    (1386, "integrity", "latent_pressure_retention_check", "latent_pressure_retention_confirmed"),
    (1387, "non_identity", "pressure_vs_resolution_split", "pressure_resolution_non_identity_preserved"),
    (1388, "non_identity", "defer_vs_solve_split", "defer_solve_non_identity"),
    (1389, "non_identity", "tension_vs_error_split", "tension_error_non_identity"),
    (1390, "non_identity", "resolution_request_vs_truth_split", "resolution_request_truth_non_identity"),
    (1391, "music_subject", "resolution_pressure_as_musical_tension", "resolution_pressure_musical_tension_preserved"),
    (1392, "music_subject", "deferred_resolution_as_suspension", "deferred_resolution_suspension_preserved"),
    (1393, "music_subject", "latent_pressure_as_background_expectation", "latent_pressure_background_expectation_preserved"),
    (1394, "summary", "coordination_resolution_pressure_summary", "coordination_resolution_pressure_observed"),
    (1395, "summary", "deferred_resolution_summary", "deferred_resolution_observed"),
    (1396, "summary", "no_collapse_no_deletion_summary", "no_collapse_no_deletion_confirmed"),
    (1397, "next_plan", "deferred_resolution_lifecycle_next_candidate", "deferred_resolution_lifecycle_next_candidate"),
    (1398, "next_plan", "next_xi_selection", "xi_deferred_resolution_lifecycle_stress"),
)


def _build_steps() -> tuple[CoordinationResolutionPressureStep, ...]:
    previous = "polyphonic_memory_coordination_1299_1348"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            CoordinationResolutionPressureStep(
                number=number,
                phase=phase,
                name=name,
                source=previous,
                result=result,
                generated_mutation=False,
            )
        )
        previous = result
    return tuple(steps)


def build_coordination_resolution_pressure_bundle(
    source: PolyphonicMemoryCoordinationBundle,
) -> CoordinationResolutionPressureBundle:
    primary, derivative, latent = source.track_states
    pressures = (
        ResolutionPressureSignal(
            name="cadential_resolution_pressure",
            source_state=primary.track.name,
            pressure_kind="cadential_alignment_wants_closure",
            pressure_level=0.82,
            requests_resolution=True,
            forces_resolution=False,
            status="resolution_pressure_recorded_without_forcing_closure",
        ),
        ResolutionPressureSignal(
            name="B_coloring_resolution_pressure",
            source_state=derivative.track.name,
            pressure_kind="coloring_feedback_wants_rebalancing",
            pressure_level=0.68,
            requests_resolution=True,
            forces_resolution=False,
            status="resolution_pressure_recorded_without_track_merge",
        ),
        ResolutionPressureSignal(
            name="latent_echo_resolution_pressure",
            source_state=latent.track.name,
            pressure_kind="background_echo_wants_future_resolution",
            pressure_level=0.41,
            requests_resolution=True,
            forces_resolution=False,
            status="latent_pressure_recorded_without_deletion",
        ),
    )
    deferred_states = (
        DeferredResolutionState(
            track_state=primary,
            pressure_signals=("cadential_resolution_pressure", "B_coloring_resolution_pressure"),
            deferred_reason="cadential_pressure_is_heard_but_polyphonic_difference_remains_active",
            keeps_polyphony=True,
            keeps_interference=True,
            collapses_to_single_voice=False,
            deleted=False,
            status="primary_resolution_deferred_without_single_voice_collapse",
        ),
        DeferredResolutionState(
            track_state=derivative,
            pressure_signals=("B_coloring_resolution_pressure",),
            deferred_reason="derivative_coloring_needs_rebalancing_not_merge",
            keeps_polyphony=True,
            keeps_interference=True,
            collapses_to_single_voice=False,
            deleted=False,
            status="derivative_resolution_deferred_without_primary_merge",
        ),
        DeferredResolutionState(
            track_state=latent,
            pressure_signals=("latent_echo_resolution_pressure",),
            deferred_reason="background_expectation_is_retained_for_later_reentry",
            keeps_polyphony=True,
            keeps_interference=True,
            collapses_to_single_voice=False,
            deleted=False,
            status="latent_resolution_pressure_retained_as_background_expectation",
        ),
    )
    return CoordinationResolutionPressureBundle(
        source_bundle=source,
        pressure_signals=pressures,
        deferred_states=deferred_states,
        pressure_mode="resolution_requested_but_deferred_under_polyphonic_memory",
        stop_lines=(
            "pressure_not_resolution",
            "pressure_not_sync_collapse",
            "pressure_not_single_voice",
            "defer_not_solve",
            "latent_pressure_not_deletion",
        ),
        generated_final_resolution=False,
        generated_sync_collapse=False,
        generated_single_voice=False,
        generated_deletion=False,
        status="coordination_resolution_pressure_bundle_1349_1398_built_without_final_resolution_or_collapse",
    )


def observe_coordination_resolution_pressure() -> CoordinationResolutionPressureObservation:
    source = observe_polyphonic_memory_coordination()
    bundle = build_coordination_resolution_pressure_bundle(source.bundle)
    steps = _build_steps()

    return CoordinationResolutionPressureObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        pressure_observed_without_resolution=(
            len(bundle.pressure_signals) == 3
            and all(signal.requests_resolution for signal in bundle.pressure_signals)
            and all(signal.forces_resolution is False for signal in bundle.pressure_signals)
            and bundle.generated_final_resolution is False
        ),
        deferred_states_preserve_polyphony=all(
            state.keeps_polyphony for state in bundle.deferred_states
        ),
        interference_retained_under_pressure=all(
            state.keeps_interference for state in bundle.deferred_states
        ),
        no_sync_or_single_voice_collapse=(
            bundle.generated_sync_collapse is False
            and bundle.generated_single_voice is False
            and all(state.collapses_to_single_voice is False for state in bundle.deferred_states)
        ),
        latent_pressure_not_deleted=(
            bundle.deferred_states[2].track_state.track.track_kind == "latent"
            and bundle.deferred_states[2].deleted is False
            and bundle.generated_deletion is False
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="coordination_resolution_pressure_1349_1398_observed_without_final_resolution_or_collapse",
    )


def run_checks() -> None:
    observation = observe_coordination_resolution_pressure()
    bundle = observation.bundle

    assert observation.source_status == (
        "polyphonic_memory_coordination_1299_1348_observed_without_sync_collapse_or_track_merge"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1349
    assert observation.steps[-1].number == 1398
    assert observation.pressure_observed_without_resolution is True
    assert observation.deferred_states_preserve_polyphony is True
    assert observation.interference_retained_under_pressure is True
    assert observation.no_sync_or_single_voice_collapse is True
    assert observation.latent_pressure_not_deleted is True
    assert len(bundle.pressure_signals) == 3
    assert len(bundle.deferred_states) == 3
    assert bundle.generated_final_resolution is False
    assert bundle.generated_sync_collapse is False
    assert bundle.generated_single_voice is False
    assert bundle.generated_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_deferred_resolution_lifecycle_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_coordination_resolution_pressure().status)
