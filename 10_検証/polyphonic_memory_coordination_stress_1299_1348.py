"""並行variation memory track同士の協調境界を検査する最小実験。"""

from dataclasses import dataclass

from parallel_variation_memory_stress_1249_1298 import (
    ParallelMemoryTrack,
    ParallelVariationMemoryBundle,
    observe_parallel_variation_memory,
)


@dataclass(frozen=True)
class PolyphonicMemoryCoordinationStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class CoordinationSignal:
    name: str
    source_track: str
    target_track: str
    signal_kind: str
    coordinates_without_sync: bool
    causes_interference: bool
    forces_merge: bool
    status: str


@dataclass(frozen=True)
class TrackCoordinationState:
    track: ParallelMemoryTrack
    receives_signals: tuple[str, ...]
    emits_signals: tuple[str, ...]
    synchronization_state: str
    interference_state: str
    remains_distinct_track: bool
    deleted: bool
    status: str


@dataclass(frozen=True)
class PolyphonicMemoryCoordinationBundle:
    source_bundle: ParallelVariationMemoryBundle
    signals: tuple[CoordinationSignal, ...]
    track_states: tuple[TrackCoordinationState, ...]
    coordination_mode: str
    stop_lines: tuple[str, ...]
    generated_sync_collapse: bool
    generated_track_merge: bool
    generated_interference_erasure: bool
    generated_deletion: bool
    status: str


@dataclass(frozen=True)
class PolyphonicMemoryCoordinationObservation:
    source_status: str
    steps: tuple[PolyphonicMemoryCoordinationStep, ...]
    bundle: PolyphonicMemoryCoordinationBundle
    coordination_preserves_tracks: bool
    coordination_is_not_sync_collapse: bool
    interference_is_retained_not_erased: bool
    latent_track_remains_background: bool
    signals_do_not_assert_equivalence: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1299, "source_reentry", "reuse_1249_1298_parallel_variation_memory", "parallel_variation_memory_preserved"),
    (1300, "source_reentry", "next_xi_received", "polyphonic_memory_coordination_stress_received"),
    (1301, "source_reentry", "parallel_tracks_recheck", "parallel_tracks_available"),
    (1302, "coordination_request", "polyphonic_coordination_request", "polyphonic_coordination_candidate"),
    (1303, "coordination_request", "coordination_not_merge_guard", "coordination_merge_non_identity"),
    (1304, "coordination_request", "coordination_not_sync_collapse_guard", "sync_collapse_blocked"),
    (1305, "coordination_request", "interference_not_erasure_guard", "interference_erasure_non_identity"),
    (1306, "signal_layer", "anchor_reference_signal", "anchor_reference_signal_recorded"),
    (1307, "signal_layer", "cadential_alignment_signal", "cadential_alignment_signal_recorded"),
    (1308, "signal_layer", "B_coloring_feedback_signal", "B_coloring_feedback_signal_recorded"),
    (1309, "signal_layer", "latent_echo_pressure_signal", "latent_echo_pressure_signal_recorded"),
    (1310, "signal_guard", "signal_not_equivalence_guard", "signal_equivalence_non_identity"),
    (1311, "signal_guard", "signal_not_truth_guard", "signal_truth_non_identity"),
    (1312, "signal_guard", "signal_not_track_merge_guard", "signal_track_merge_non_identity"),
    (1313, "track_state_layer", "primary_track_coordination_state", "primary_track_coordination_state_recorded"),
    (1314, "track_state_layer", "derivative_track_coordination_state", "derivative_track_coordination_state_recorded"),
    (1315, "track_state_layer", "latent_track_coordination_state", "latent_track_coordination_state_recorded"),
    (1316, "track_state_layer", "asynchronous_state_record", "asynchronous_state_recorded"),
    (1317, "track_state_layer", "interference_state_record", "interference_state_recorded"),
    (1318, "track_state_layer", "distinct_track_record", "distinct_track_recorded"),
    (1319, "track_guard", "track_distinction_check", "track_distinction_confirmed"),
    (1320, "track_guard", "latent_background_check", "latent_background_confirmed"),
    (1321, "track_guard", "track_deletion_false_check", "track_deletion_false_confirmed"),
    (1322, "coordination_view", "coordination_mode_record", "coordination_mode_recorded"),
    (1323, "coordination_view", "asynchronous_coordination_view", "asynchronous_coordination_view_created"),
    (1324, "coordination_view", "controlled_interference_view", "controlled_interference_view_created"),
    (1325, "coordination_view", "non_confluent_polyphony_view", "non_confluent_polyphony_view_created"),
    (1326, "bundle", "polyphonic_coordination_bundle_creation", "polyphonic_coordination_bundle_created"),
    (1327, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1328, "bundle", "stop_lines_carry", "polyphonic_coordination_stop_lines_carried"),
    (1329, "bundle", "generated_sync_collapse_false", "generated_sync_collapse_false_recorded"),
    (1330, "bundle", "generated_track_merge_false", "generated_track_merge_false_recorded"),
    (1331, "bundle", "generated_interference_erasure_false", "generated_interference_erasure_false_recorded"),
    (1332, "bundle", "generated_deletion_false", "generated_deletion_false_recorded"),
    (1333, "integrity", "track_preservation_check", "track_preservation_confirmed"),
    (1334, "integrity", "sync_collapse_split_check", "sync_collapse_split_confirmed"),
    (1335, "integrity", "interference_retention_check", "interference_retention_confirmed"),
    (1336, "integrity", "latent_background_retention_check", "latent_background_retention_confirmed"),
    (1337, "integrity", "signal_equivalence_split_check", "signal_equivalence_split_confirmed"),
    (1338, "non_identity", "coordination_vs_merge_split", "coordination_merge_non_identity_preserved"),
    (1339, "non_identity", "coordination_vs_sync_split", "coordination_sync_non_identity"),
    (1340, "non_identity", "interference_vs_erasure_split", "interference_erasure_non_identity_preserved"),
    (1341, "non_identity", "polyphony_vs_single_voice_split", "polyphony_single_voice_non_identity"),
    (1342, "music_subject", "polyphonic_memory_as_coordinated_difference", "polyphonic_memory_coordinated_difference_preserved"),
    (1343, "music_subject", "asynchronous_tracks_as_musical_tension", "asynchronous_tracks_musical_tension_preserved"),
    (1344, "music_subject", "latent_echo_as_background_pressure", "latent_echo_background_pressure_preserved"),
    (1345, "summary", "polyphonic_coordination_summary", "polyphonic_coordination_observed"),
    (1346, "summary", "no_merge_no_sync_collapse_summary", "no_merge_no_sync_collapse_confirmed"),
    (1347, "next_plan", "coordination_resolution_pressure_next_candidate", "coordination_resolution_pressure_next_candidate"),
    (1348, "next_plan", "next_xi_selection", "xi_coordination_resolution_pressure_stress"),
)


def _build_steps() -> tuple[PolyphonicMemoryCoordinationStep, ...]:
    previous = "parallel_variation_memory_1249_1298"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            PolyphonicMemoryCoordinationStep(
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


def build_polyphonic_memory_coordination_bundle(
    source: ParallelVariationMemoryBundle,
) -> PolyphonicMemoryCoordinationBundle:
    primary, derivative, latent = source.tracks
    signals = (
        CoordinationSignal(
            name="anchor_reference_signal",
            source_track=primary.name,
            target_track=derivative.name,
            signal_kind="shared_anchor_reference",
            coordinates_without_sync=True,
            causes_interference=False,
            forces_merge=False,
            status="anchor_signal_coordinates_without_merging_tracks",
        ),
        CoordinationSignal(
            name="cadential_alignment_signal",
            source_track=primary.name,
            target_track=derivative.name,
            signal_kind="loose_cadential_alignment",
            coordinates_without_sync=True,
            causes_interference=False,
            forces_merge=False,
            status="cadential_signal_aligns_without_sync_collapse",
        ),
        CoordinationSignal(
            name="B_coloring_feedback_signal",
            source_track=derivative.name,
            target_track=primary.name,
            signal_kind="coloring_feedback",
            coordinates_without_sync=True,
            causes_interference=True,
            forces_merge=False,
            status="feedback_signal_retains_controlled_interference",
        ),
        CoordinationSignal(
            name="latent_echo_pressure_signal",
            source_track=latent.name,
            target_track=primary.name,
            signal_kind="background_pressure",
            coordinates_without_sync=True,
            causes_interference=True,
            forces_merge=False,
            status="latent_signal_preserved_as_background_pressure",
        ),
    )
    states = (
        TrackCoordinationState(
            track=primary,
            receives_signals=("B_coloring_feedback_signal", "latent_echo_pressure_signal"),
            emits_signals=("anchor_reference_signal", "cadential_alignment_signal"),
            synchronization_state="loosely_aligned_not_synchronized",
            interference_state="receives_controlled_interference",
            remains_distinct_track=True,
            deleted=False,
            status="primary_track_coordinated_without_single_voice_collapse",
        ),
        TrackCoordinationState(
            track=derivative,
            receives_signals=("anchor_reference_signal", "cadential_alignment_signal"),
            emits_signals=("B_coloring_feedback_signal",),
            synchronization_state="asynchronous_derivative_alignment",
            interference_state="feeds_coloring_difference",
            remains_distinct_track=True,
            deleted=False,
            status="derivative_track_coordinated_without_primary_merge",
        ),
        TrackCoordinationState(
            track=latent,
            receives_signals=(),
            emits_signals=("latent_echo_pressure_signal",),
            synchronization_state="background_asynchronous",
            interference_state="latent_pressure_retained",
            remains_distinct_track=True,
            deleted=False,
            status="latent_track_coordinated_as_background_pressure",
        ),
    )
    return PolyphonicMemoryCoordinationBundle(
        source_bundle=source,
        signals=signals,
        track_states=states,
        coordination_mode="loose_coordination_with_controlled_interference",
        stop_lines=(
            "coordination_not_merge",
            "coordination_not_sync_collapse",
            "interference_not_erasure",
            "signal_not_equivalence",
            "polyphony_not_single_voice",
        ),
        generated_sync_collapse=False,
        generated_track_merge=False,
        generated_interference_erasure=False,
        generated_deletion=False,
        status="polyphonic_memory_coordination_bundle_1299_1348_built_without_sync_collapse_or_track_merge",
    )


def observe_polyphonic_memory_coordination() -> PolyphonicMemoryCoordinationObservation:
    source = observe_parallel_variation_memory()
    bundle = build_polyphonic_memory_coordination_bundle(source.bundle)
    steps = _build_steps()

    return PolyphonicMemoryCoordinationObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        coordination_preserves_tracks=(
            len(bundle.track_states) == 3
            and all(state.remains_distinct_track for state in bundle.track_states)
        ),
        coordination_is_not_sync_collapse=(
            bundle.generated_sync_collapse is False
            and all("not_synchronized" in state.synchronization_state or "asynchronous" in state.synchronization_state for state in bundle.track_states)
        ),
        interference_is_retained_not_erased=(
            bundle.generated_interference_erasure is False
            and any(signal.causes_interference for signal in bundle.signals)
        ),
        latent_track_remains_background=(
            bundle.track_states[2].track.track_kind == "latent"
            and bundle.track_states[2].deleted is False
        ),
        signals_do_not_assert_equivalence=all(signal.forces_merge is False for signal in bundle.signals),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="polyphonic_memory_coordination_1299_1348_observed_without_sync_collapse_or_track_merge",
    )


def run_checks() -> None:
    observation = observe_polyphonic_memory_coordination()
    bundle = observation.bundle

    assert observation.source_status == (
        "parallel_variation_memory_1249_1298_observed_without_track_merge_or_memory_erasure"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1299
    assert observation.steps[-1].number == 1348
    assert observation.coordination_preserves_tracks is True
    assert observation.coordination_is_not_sync_collapse is True
    assert observation.interference_is_retained_not_erased is True
    assert observation.latent_track_remains_background is True
    assert observation.signals_do_not_assert_equivalence is True
    assert len(bundle.signals) == 4
    assert len(bundle.track_states) == 3
    assert bundle.generated_sync_collapse is False
    assert bundle.generated_track_merge is False
    assert bundle.generated_interference_erasure is False
    assert bundle.generated_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_coordination_resolution_pressure_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_polyphonic_memory_coordination().status)
