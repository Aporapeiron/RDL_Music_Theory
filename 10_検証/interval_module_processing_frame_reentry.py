"""既存70 activation経由processing frameからgeneric intervalへ再入する最小検証。"""

from dataclasses import dataclass

from interval_module_existing_70_activation_bridge import (
    Existing70ActivationBridgeObservation,
    bridge_gamma_fixture,
    bundle_observation,
    run_existing_70_activation,
)
from interval_module_generic_interval_boundary import (
    GenericIntervalObservation,
    gamma_generic_fixture,
    generate_generic_interval,
)
from interval_module_internal_boundary_activation import (
    IntervalInternalActivationObservation,
    IntervalModuleProcessingFrameCandidate,
    PitchRelationPayload,
)


@dataclass(frozen=True)
class ProcessingFrameReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_existing70_bridge: bool


@dataclass(frozen=True)
class ProcessingFrameReentryObservation:
    bridge_observation: Existing70ActivationBridgeObservation
    reentry_gamma: ProcessingFrameReentryGamma | None
    generic_observation: GenericIntervalObservation | None
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


def activation_view_from_bridge(
    bridge_obs: Existing70ActivationBridgeObservation,
) -> IntervalInternalActivationObservation | None:
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
    return IntervalInternalActivationObservation(
        reception_observation=bridge_obs.bundle_observation,
        pitch_payload=payload,
        b_chromatic=None,
        b_spelling=None,
        processing_gamma=None,
        processing_frame=frame,
        generic_interval_generated=False,
        quality_generated=False,
        interval_label_generated=False,
        contextual_role_generated=False,
        core_promoted=False,
        status=bridge_obs.existing70_status or "existing70_activation_status_missing",
        activation_reason="reentered_from_existing70_bridge_observation",
    )


def reenter_processing_frame_to_generic(
    bridge_obs: Existing70ActivationBridgeObservation,
    reentry_gamma: ProcessingFrameReentryGamma | None,
) -> ProcessingFrameReentryObservation:
    if bridge_obs.processing_frame_label is None:
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

    activation_view = activation_view_from_bridge(bridge_obs)
    if activation_view is None:
        return ProcessingFrameReentryObservation(
            bridge_obs,
            reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            False,
            "activation_view_not_constructed",
        )

    generic_obs = generate_generic_interval(activation_view, gamma_generic_fixture())
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
