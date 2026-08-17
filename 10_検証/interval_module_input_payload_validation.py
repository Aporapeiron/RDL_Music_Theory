"""bound payload instance候補とinput validation診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_input_payload_instance import (
    PayloadInstanceBindingObservation,
    compare_payload_instance_binding,
)


@dataclass(frozen=True)
class PayloadValidationGamma:
    name: str
    required_fields: tuple[str, ...]
    generated_by_bound_payload: bool


@dataclass(frozen=True)
class PayloadValidationDiagnosticCandidate:
    label: str
    source_bound_payload_label: str
    valid: bool
    processing_request_generated: bool


@dataclass(frozen=True)
class PayloadValidationObservation:
    binding_observation: PayloadInstanceBindingObservation
    validation_gamma: PayloadValidationGamma | None
    validation_diagnostic: PayloadValidationDiagnosticCandidate | None
    status: str


def binding_observation() -> PayloadInstanceBindingObservation:
    return compare_payload_instance_binding()[1]


def validation_gamma_fixture() -> PayloadValidationGamma:
    return PayloadValidationGamma(
        name="Gamma_interval_payload_validation_fixture",
        required_fields=("lower_note", "upper_note", "chromatic_distance", "spelling_pair"),
        generated_by_bound_payload=False,
    )


def validate_payload(
    binding_obs: PayloadInstanceBindingObservation,
    gamma: PayloadValidationGamma | None,
) -> PayloadValidationObservation:
    bound = binding_obs.bound_payload
    payload = binding_obs.payload_instance
    if bound is None or payload is None:
        return PayloadValidationObservation(
            binding_obs, gamma, None, "no_bound_payload_instance_candidate"
        )
    if gamma is None:
        return PayloadValidationObservation(
            binding_obs, None, None, "payload_validation_not_created_without_gamma"
        )
    valid = all(
        getattr(payload, field, None) is not None for field in gamma.required_fields
    )
    diagnostic = PayloadValidationDiagnosticCandidate(
        label="pitch_relation_payload_validation_diagnostic_candidate",
        source_bound_payload_label=bound.label,
        valid=valid,
        processing_request_generated=False,
    )
    return PayloadValidationObservation(
        binding_obs,
        gamma,
        diagnostic,
        "payload_validation_diagnostic_observed_not_processing_request",
    )


def compare_payload_validation() -> tuple[
    PayloadValidationObservation, PayloadValidationObservation
]:
    binding = binding_observation()
    return (
        validate_payload(binding, None),
        validate_payload(binding, validation_gamma_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_payload_validation()
    assert without_gamma.status == "payload_validation_not_created_without_gamma"
    assert (
        with_gamma.status
        == "payload_validation_diagnostic_observed_not_processing_request"
    )
    assert with_gamma.validation_diagnostic is not None
    assert with_gamma.validation_diagnostic.valid is True
    assert with_gamma.validation_diagnostic.processing_request_generated is False
    assert with_gamma.validation_gamma is not None
    assert with_gamma.validation_gamma.generated_by_bound_payload is False


if __name__ == "__main__":
    run_checks()
    print(compare_payload_validation()[1].status)
