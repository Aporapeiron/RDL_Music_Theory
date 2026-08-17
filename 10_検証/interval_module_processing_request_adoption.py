"""processing request候補とactivation adoption境界の最小検証。"""

from dataclasses import dataclass

from interval_module_processing_request_boundary import (
    ProcessingRequestObservation,
    compare_processing_request,
)


@dataclass(frozen=True)
class ProcessingRequestAdoptionController:
    name: str
    accepted_stage: str
    generated_by_processing_request: bool


@dataclass(frozen=True)
class AdoptedProcessingRequestCandidate:
    label: str
    source_request_label: str
    activation_input_bundle_generated: bool
    module_processing_started: bool


@dataclass(frozen=True)
class ProcessingRequestAdoptionObservation:
    request_observation: ProcessingRequestObservation
    adoption_controller: ProcessingRequestAdoptionController | None
    adopted_request: AdoptedProcessingRequestCandidate | None
    status: str


def request_observation() -> ProcessingRequestObservation:
    return compare_processing_request()[1]


def adoption_controller_fixture() -> ProcessingRequestAdoptionController:
    return ProcessingRequestAdoptionController(
        name="interval_processing_request_adoption_controller_fixture",
        accepted_stage="processing_frame_activation",
        generated_by_processing_request=False,
    )


def adopt_processing_request(
    request_obs: ProcessingRequestObservation,
    controller: ProcessingRequestAdoptionController | None,
) -> ProcessingRequestAdoptionObservation:
    request = request_obs.processing_request
    if request is None:
        return ProcessingRequestAdoptionObservation(
            request_obs, controller, None, "no_processing_request_candidate"
        )
    if controller is None:
        return ProcessingRequestAdoptionObservation(
            request_obs, None, None, "processing_request_not_adopted_without_controller"
        )
    if request.requested_processing_stage != controller.accepted_stage:
        return ProcessingRequestAdoptionObservation(
            request_obs, controller, None, "processing_request_stage_not_accepted"
        )
    adopted = AdoptedProcessingRequestCandidate(
        label="adopted_interval_processing_request_candidate",
        source_request_label=request.label,
        activation_input_bundle_generated=False,
        module_processing_started=False,
    )
    return ProcessingRequestAdoptionObservation(
        request_obs,
        controller,
        adopted,
        "adopted_processing_request_candidate_observed_not_started",
    )


def compare_processing_request_adoption() -> tuple[
    ProcessingRequestAdoptionObservation, ProcessingRequestAdoptionObservation
]:
    request = request_observation()
    return (
        adopt_processing_request(request, None),
        adopt_processing_request(request, adoption_controller_fixture()),
    )


def run_checks() -> None:
    without_controller, with_controller = compare_processing_request_adoption()
    assert without_controller.status == "processing_request_not_adopted_without_controller"
    assert (
        with_controller.status
        == "adopted_processing_request_candidate_observed_not_started"
    )
    assert with_controller.adopted_request is not None
    assert with_controller.adopted_request.activation_input_bundle_generated is False
    assert with_controller.adopted_request.module_processing_started is False
    assert with_controller.adoption_controller is not None
    assert with_controller.adoption_controller.generated_by_processing_request is False


if __name__ == "__main__":
    run_checks()
    print(compare_processing_request_adoption()[1].status)
