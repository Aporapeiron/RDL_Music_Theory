"""activation input bundleと既存70 processing frame activation接続の最小検証。"""

from dataclasses import dataclass

from interval_module_activation_input_bundle import (
    ActivationInputBundleObservation,
    compare_activation_input_bundle,
)
from interval_module_internal_boundary_activation import (
    PitchRelationPayload,
    activate_interval_internal_frame,
    b_chromatic_fixture,
    b_spelling_fixture,
    interval_processing_frame_gamma,
    interval_reception_observation,
)


@dataclass(frozen=True)
class Existing70ActivationBridgeGamma:
    name: str
    reads: tuple[str, str]
    generated_by_activation_bundle: bool


@dataclass(frozen=True)
class Existing70ActivationBridgeObservation:
    bundle_observation: ActivationInputBundleObservation
    bridge_gamma: Existing70ActivationBridgeGamma | None
    existing70_status: str | None
    processing_frame_label: str | None
    generic_interval_generated: bool
    quality_generated: bool
    interval_label_generated: bool
    status: str


def bundle_observation() -> ActivationInputBundleObservation:
    return compare_activation_input_bundle()[1]


def bridge_gamma_fixture() -> Existing70ActivationBridgeGamma:
    return Existing70ActivationBridgeGamma(
        name="Gamma_existing_70_activation_bridge_fixture",
        reads=("activation_input_bundle", "existing_70_activation_pipeline"),
        generated_by_activation_bundle=False,
    )


def run_existing_70_activation(
    bundle_obs: ActivationInputBundleObservation,
    gamma: Existing70ActivationBridgeGamma | None,
) -> Existing70ActivationBridgeObservation:
    bundle = bundle_obs.activation_bundle
    if bundle is None:
        return Existing70ActivationBridgeObservation(
            bundle_obs, gamma, None, None, False, False, False, "no_activation_input_bundle"
        )
    if gamma is None:
        return Existing70ActivationBridgeObservation(
            bundle_obs,
            None,
            None,
            None,
            False,
            False,
            False,
            "existing_70_activation_not_run_without_bridge_gamma",
        )

    payload = PitchRelationPayload(
        name=bundle.payload.name.replace("_instance", ""),
        lower_note=bundle.payload.lower_note,
        upper_note=bundle.payload.upper_note,
        chromatic_distance=bundle.payload.chromatic_distance,
        spelling_pair=bundle.payload.spelling_pair,
        generated_by_boundary_input=False,
    )
    result = activate_interval_internal_frame(
        reception_observation=interval_reception_observation(),
        pitch_payload=payload,
        b_chromatic=b_chromatic_fixture() if bundle.has_b_chromatic else None,
        b_spelling=b_spelling_fixture() if bundle.has_b_spelling else None,
        processing_gamma=(
            interval_processing_frame_gamma()
            if bundle.has_processing_gamma
            else None
        ),
    )
    return Existing70ActivationBridgeObservation(
        bundle_observation=bundle_obs,
        bridge_gamma=gamma,
        existing70_status=result.status,
        processing_frame_label=(
            result.processing_frame.label if result.processing_frame else None
        ),
        generic_interval_generated=result.generic_interval_generated,
        quality_generated=result.quality_generated,
        interval_label_generated=result.interval_label_generated,
        status="existing_70_activation_observed_not_generic_quality_label",
    )


def compare_existing_70_activation_bridge() -> tuple[
    Existing70ActivationBridgeObservation, Existing70ActivationBridgeObservation
]:
    bundle = bundle_observation()
    return (
        run_existing_70_activation(bundle, None),
        run_existing_70_activation(bundle, bridge_gamma_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_existing_70_activation_bridge()
    assert without_gamma.status == "existing_70_activation_not_run_without_bridge_gamma"
    assert (
        with_gamma.status
        == "existing_70_activation_observed_not_generic_quality_label"
    )
    assert with_gamma.existing70_status == "interval_processing_frame_observed_not_labeled"
    assert with_gamma.processing_frame_label == "interval_processing_frame_C4_G4_candidate"
    assert with_gamma.generic_interval_generated is False
    assert with_gamma.quality_generated is False
    assert with_gamma.interval_label_generated is False
    assert with_gamma.bridge_gamma is not None
    assert with_gamma.bridge_gamma.generated_by_activation_bundle is False


if __name__ == "__main__":
    run_checks()
    print(compare_existing_70_activation_bridge()[1].status)
