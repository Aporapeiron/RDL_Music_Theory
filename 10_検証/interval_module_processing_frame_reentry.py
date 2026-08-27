"""既存70 activation経由processing frameからgeneric intervalへ再入する最小検証。"""

from dataclasses import dataclass

from interval_module_existing_70_activation_bridge import (
    Existing70ActivationBridgeObservation,
    bridge_gamma_fixture,
    bundle_observation,
    run_existing_70_activation,
)
from interval_module_generic_interval_boundary import (
    GenericIntervalCandidate,
    GenericIntervalGamma,
    gamma_generic_fixture,
)
from interval_module_internal_boundary_activation import (
    IntervalModuleProcessingFrameCandidate,
    PitchRelationPayload,
)

LETTER_INDEX = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}


@dataclass(frozen=True)
class ProcessingFrameReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_existing70_bridge: bool


@dataclass(frozen=True)
class ProcessingFramePayloadView:
    processing_frame: IntervalModuleProcessingFrameCandidate
    pitch_payload: PitchRelationPayload


@dataclass(frozen=True)
class ReenteredGenericIntervalObservation:
    frame_payload_view: ProcessingFramePayloadView
    gamma_generic: GenericIntervalGamma | None
    generic_interval: GenericIntervalCandidate | None
    quality_generated: bool
    interval_label_generated: bool
    contextual_role_generated: bool
    core_promoted: bool
    status: str
    generation_reason: str | None


@dataclass(frozen=True)
class ProcessingFrameReentryObservation:
    bridge_observation: Existing70ActivationBridgeObservation
    reentry_gamma: ProcessingFrameReentryGamma | None
    generic_observation: ReenteredGenericIntervalObservation | None
    same_processing_frame_label: bool
    same_spelling_pair: bool
    generic_interval_generated: bool
    quality_generated: bool
    interval_label_generated: bool
    status: str


def existing70_bridge_observation() -> Existing70ActivationBridgeObservation:
    return run_existing_70_activation(bundle_observation(), bridge_gamma_fixture())


def reentry_gamma_fixture() -> ProcessingFrameReentryGamma:
    return ProcessingFrameReentryGamma(
        name="Gamma_processing_frame_to_generic_reentry_fixture",
        reads=("existing70_processing_frame", "payload_spelling_pair"),
        generated_by_existing70_bridge=False,
    )


def frame_payload_view_from_bridge(
    bridge_obs: Existing70ActivationBridgeObservation,
) -> ProcessingFramePayloadView | None:
    bundle = bridge_obs.bundle_observation.activation_bundle
    if bundle is None or bridge_obs.processing_frame_label is None:
        return None

    payload = PitchRelationPayload(
        name=bundle.payload.name.replace("_instance", ""),
        lower_note=bundle.payload.lower_note,
        upper_note=bundle.payload.upper_note,
        chromatic_distance=bundle.payload.chromatic_distance,
        spelling_pair=bundle.payload.spelling_pair,
        generated_by_boundary_input=False,
    )
    frame = IntervalModuleProcessingFrameCandidate(
        label=bridge_obs.processing_frame_label,
        source_boundary_input_label=bundle.source_adopted_request_label,
        payload_name=payload.name,
        chromatic_distance_available=True,
        spelling_pair_available=True,
        generic_interval_generated=False,
        quality_generated=False,
        interval_label_generated=False,
        contextual_role_generated=False,
    )
    return ProcessingFramePayloadView(processing_frame=frame, pitch_payload=payload)


def generate_reentered_generic_interval(
    view: ProcessingFramePayloadView,
    gamma_generic: GenericIntervalGamma | None,
) -> ReenteredGenericIntervalObservation:
    if gamma_generic is None:
        return ReenteredGenericIntervalObservation(
            frame_payload_view=view,
            gamma_generic=None,
            generic_interval=None,
            quality_generated=False,
            interval_label_generated=False,
            contextual_role_generated=False,
            core_promoted=False,
            status="generic_interval_not_generated_without_gamma",
            generation_reason=None,
        )

    lower, upper = view.pitch_payload.spelling_pair
    generic = GenericIntervalCandidate(
        label="generic_interval_fifth_candidate",
        source_processing_frame_label=view.processing_frame.label,
        spelling_pair=view.pitch_payload.spelling_pair,
        generic_number=LETTER_INDEX[upper] - LETTER_INDEX[lower] + 1,
        quality_generated=False,
        interval_label_generated=False,
        contextual_role_generated=False,
    )
    return ReenteredGenericIntervalObservation(
        frame_payload_view=view,
        gamma_generic=gamma_generic,
        generic_interval=generic,
        quality_generated=False,
        interval_label_generated=False,
        contextual_role_generated=False,
        core_promoted=False,
        status="generic_interval_candidate_observed_not_qualified",
        generation_reason="reentered_processing_frame_read_by_Gamma_generic",
    )


def reenter_processing_frame_to_generic(
    bridge_obs: Existing70ActivationBridgeObservation,
    reentry_gamma: ProcessingFrameReentryGamma | None,
) -> ProcessingFrameReentryObservation:
    view = frame_payload_view_from_bridge(bridge_obs)
    if view is None:
        return ProcessingFrameReentryObservation(
            bridge_obs,
            reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            False,
            "no_existing70_processing_frame",
        )
    if reentry_gamma is None:
        return ProcessingFrameReentryObservation(
            bridge_obs,
            None,
            None,
            True,
            True,
            False,
            False,
            False,
            "processing_frame_not_reentered_without_reentry_gamma",
        )

    generic_obs = generate_reentered_generic_interval(view, gamma_generic_fixture())
    generic = generic_obs.generic_interval
    bundle = bridge_obs.bundle_observation.activation_bundle
    return ProcessingFrameReentryObservation(
        bridge_observation=bridge_obs,
        reentry_gamma=reentry_gamma,
        generic_observation=generic_obs,
        same_processing_frame_label=(
            generic is not None
            and generic.source_processing_frame_label == bridge_obs.processing_frame_label
        ),
        same_spelling_pair=(
            bundle is not None
            and generic is not None
            and generic.spelling_pair == bundle.payload.spelling_pair
        ),
        generic_interval_generated=generic is not None,
        quality_generated=generic_obs.quality_generated,
        interval_label_generated=generic_obs.interval_label_generated,
        status="processing_frame_reentered_to_generic_not_quality_label",
    )


def compare_processing_frame_reentry() -> tuple[
    ProcessingFrameReentryObservation, ProcessingFrameReentryObservation
]:
    bridge_obs = existing70_bridge_observation()
    return (
        reenter_processing_frame_to_generic(bridge_obs, None),
        reenter_processing_frame_to_generic(bridge_obs, reentry_gamma_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_processing_frame_reentry()
    assert without_gamma.status == "processing_frame_not_reentered_without_reentry_gamma"
    assert without_gamma.generic_interval_generated is False
    assert with_gamma.status == "processing_frame_reentered_to_generic_not_quality_label"
    assert with_gamma.same_processing_frame_label is True
    assert with_gamma.same_spelling_pair is True
    assert with_gamma.generic_interval_generated is True
    assert with_gamma.quality_generated is False
    assert with_gamma.interval_label_generated is False
    assert with_gamma.generic_observation is not None
    assert with_gamma.generic_observation.generic_interval is not None
    assert with_gamma.generic_observation.generic_interval.generic_number == 5
    assert with_gamma.reentry_gamma is not None
    assert with_gamma.reentry_gamma.generated_by_existing70_bridge is False


if __name__ == "__main__":
    run_checks()
    print(compare_processing_frame_reentry()[1].status)
