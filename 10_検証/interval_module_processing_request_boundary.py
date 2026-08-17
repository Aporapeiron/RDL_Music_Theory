"""payload validation診断とmodule processing request候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_input_payload_validation import (
    PayloadValidationObservation,
    compare_payload_validation,
)


@dataclass(frozen=True)
class ProcessingRequestController:
    name: str
    generated_by_validation: bool


@dataclass(frozen=True)
class IntervalModuleProcessingRequestCandidate:
    label: str
    source_validation_label: str
    requested_processing_stage: str
    module_processing_started: bool


@dataclass(frozen=True)
class ProcessingRequestObservation:
    validation_observation: PayloadValidationObservation
    request_controller: ProcessingRequestController | None
    processing_request: IntervalModuleProcessingRequestCandidate | None
    status: str


def validation_observation() -> PayloadValidationObservation:
    return compare_payload_validation()[1]


def processing_request_controller_fixture() -> ProcessingRequestController:
    return ProcessingRequestController(
        name="interval_processing_request_controller_fixture",
        generated_by_validation=False,
    )


def create_processing_request(
    validation_obs: PayloadValidationObservation,
    controller: ProcessingRequestController | None,
) -> ProcessingRequestObservation:
    diagnostic = validation_obs.validation_diagnostic
    if diagnostic is None:
        return ProcessingRequestObservation(
            validation_obs, controller, None, "no_payload_validation_diagnostic"
        )
    if controller is None:
        return ProcessingRequestObservation(
            validation_obs, None, None, "processing_request_not_created_without_controller"
        )
    if not diagnostic.valid:
        return ProcessingRequestObservation(
            validation_obs, controller, None, "processing_request_blocked_invalid_payload"
        )
    request = IntervalModuleProcessingRequestCandidate(
        label="interval_module_processing_request_candidate",
        source_validation_label=diagnostic.label,
        requested_processing_stage="processing_frame_activation",
        module_processing_started=False,
    )
    return ProcessingRequestObservation(
        validation_obs,
        controller,
        request,
        "processing_request_candidate_observed_not_started",
    )


def compare_processing_request() -> tuple[
    ProcessingRequestObservation, ProcessingRequestObservation
]:
    validation = validation_observation()
    return (
        create_processing_request(validation, None),
        create_processing_request(validation, processing_request_controller_fixture()),
    )


def run_checks() -> None:
    without_controller, with_controller = compare_processing_request()
    assert without_controller.status == "processing_request_not_created_without_controller"
    assert with_controller.status == "processing_request_candidate_observed_not_started"
    assert with_controller.processing_request is not None
    assert (
        with_controller.processing_request.requested_processing_stage
        == "processing_frame_activation"
    )
    assert with_controller.processing_request.module_processing_started is False
    assert with_controller.request_controller is not None
    assert with_controller.request_controller.generated_by_validation is False


if __name__ == "__main__":
    run_checks()
    print(compare_processing_request()[1].status)
