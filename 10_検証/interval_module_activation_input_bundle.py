"""adopted processing requestとactivation input bundle境界の最小検証。"""

from dataclasses import dataclass

from interval_module_input_payload_instance import InputPayloadInstanceFixture
from interval_module_processing_request_adoption import (
    ProcessingRequestAdoptionObservation,
    compare_processing_request_adoption,
)


@dataclass(frozen=True)
class ActivationBoundaryInventory:
    name: str
    includes_b_chromatic: bool
    includes_b_spelling: bool
    includes_processing_gamma: bool
    generated_by_adopted_request: bool


@dataclass(frozen=True)
class ActivationInputBundleCandidate:
    label: str
    source_adopted_request_label: str
    payload: InputPayloadInstanceFixture
    has_b_chromatic: bool
    has_b_spelling: bool
    has_processing_gamma: bool
    processing_frame_generated: bool


@dataclass(frozen=True)
class ActivationInputBundleObservation:
    adoption_observation: ProcessingRequestAdoptionObservation
    boundary_inventory: ActivationBoundaryInventory | None
    activation_bundle: ActivationInputBundleCandidate | None
    status: str


def adoption_observation() -> ProcessingRequestAdoptionObservation:
    return compare_processing_request_adoption()[1]


def boundary_inventory_fixture() -> ActivationBoundaryInventory:
    return ActivationBoundaryInventory(
        name="interval_activation_boundary_inventory_fixture",
        includes_b_chromatic=True,
        includes_b_spelling=True,
        includes_processing_gamma=True,
        generated_by_adopted_request=False,
    )


def create_activation_input_bundle(
    adoption_obs: ProcessingRequestAdoptionObservation,
    inventory: ActivationBoundaryInventory | None,
) -> ActivationInputBundleObservation:
    adopted = adoption_obs.adopted_request
    payload = (
        adoption_obs.request_observation.validation_observation.binding_observation.payload_instance
    )
    if adopted is None:
        return ActivationInputBundleObservation(
            adoption_obs, inventory, None, "no_adopted_processing_request_candidate"
        )
    if payload is None:
        return ActivationInputBundleObservation(
            adoption_obs, inventory, None, "no_bound_payload_instance_for_activation"
        )
    if inventory is None:
        return ActivationInputBundleObservation(
            adoption_obs, None, None, "activation_input_bundle_not_created_without_inventory"
        )
    bundle = ActivationInputBundleCandidate(
        label="interval_activation_input_bundle_candidate",
        source_adopted_request_label=adopted.label,
        payload=payload,
        has_b_chromatic=inventory.includes_b_chromatic,
        has_b_spelling=inventory.includes_b_spelling,
        has_processing_gamma=inventory.includes_processing_gamma,
        processing_frame_generated=False,
    )
    return ActivationInputBundleObservation(
        adoption_obs,
        inventory,
        bundle,
        "activation_input_bundle_candidate_observed_not_frame",
    )


def compare_activation_input_bundle() -> tuple[
    ActivationInputBundleObservation, ActivationInputBundleObservation
]:
    adoption = adoption_observation()
    return (
        create_activation_input_bundle(adoption, None),
        create_activation_input_bundle(adoption, boundary_inventory_fixture()),
    )


def run_checks() -> None:
    without_inventory, with_inventory = compare_activation_input_bundle()
    assert without_inventory.status == "activation_input_bundle_not_created_without_inventory"
    assert with_inventory.status == "activation_input_bundle_candidate_observed_not_frame"
    assert with_inventory.activation_bundle is not None
    assert with_inventory.activation_bundle.has_b_chromatic is True
    assert with_inventory.activation_bundle.has_b_spelling is True
    assert with_inventory.activation_bundle.has_processing_gamma is True
    assert with_inventory.activation_bundle.processing_frame_generated is False
    assert with_inventory.boundary_inventory is not None
    assert with_inventory.boundary_inventory.generated_by_adopted_request is False


if __name__ == "__main__":
    run_checks()
    print(compare_activation_input_bundle()[1].status)
