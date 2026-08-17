"""adopted input reception contractとpayload instance候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_input_contract_adoption import (
    InputContractAdoptionObservation,
    compare_input_contract_adoption,
)


@dataclass(frozen=True)
class InputPayloadInstanceFixture:
    name: str
    payload_schema: str
    lower_note: str
    upper_note: str
    chromatic_distance: int
    spelling_pair: tuple[str, str]
    generated_by_adopted_contract: bool


@dataclass(frozen=True)
class PayloadInstanceBindingGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class BoundPayloadInstanceCandidate:
    label: str
    source_contract_label: str
    payload_schema: str
    validation_generated: bool
    module_processing_started: bool


@dataclass(frozen=True)
class PayloadInstanceBindingObservation:
    contract_observation: InputContractAdoptionObservation
    payload_instance: InputPayloadInstanceFixture | None
    binding_gamma: PayloadInstanceBindingGamma | None
    bound_payload: BoundPayloadInstanceCandidate | None
    status: str


def contract_observation() -> InputContractAdoptionObservation:
    return compare_input_contract_adoption()[1]


def payload_instance_fixture() -> InputPayloadInstanceFixture:
    return InputPayloadInstanceFixture(
        name="pitch_relation_payload_C4_G4_instance_fixture",
        payload_schema="pitch_relation_payload",
        lower_note="C4",
        upper_note="G4",
        chromatic_distance=7,
        spelling_pair=("C", "G"),
        generated_by_adopted_contract=False,
    )


def binding_gamma_fixture() -> PayloadInstanceBindingGamma:
    return PayloadInstanceBindingGamma(
        name="Gamma_interval_payload_instance_binding_fixture",
        reads=("adopted_input_reception_contract", "external_payload_instance"),
        rule_scope="fixture_limited_not_payload_validation_rule",
    )


def bind_payload_instance(
    contract_obs: InputContractAdoptionObservation,
    payload: InputPayloadInstanceFixture | None,
    gamma: PayloadInstanceBindingGamma | None,
) -> PayloadInstanceBindingObservation:
    contract = contract_obs.adopted_contract
    if contract is None:
        return PayloadInstanceBindingObservation(
            contract_obs, payload, gamma, None, "no_adopted_input_reception_contract"
        )
    if payload is None:
        return PayloadInstanceBindingObservation(
            contract_obs, None, gamma, None, "payload_instance_not_bound_without_payload"
        )
    if gamma is None:
        return PayloadInstanceBindingObservation(
            contract_obs, payload, None, None, "payload_instance_not_bound_without_gamma"
        )
    expected_schema = contract.selected_schema_contract.payload_schema
    if payload.payload_schema != expected_schema:
        return PayloadInstanceBindingObservation(
            contract_obs,
            payload,
            gamma,
            None,
            "payload_instance_schema_mismatch",
        )
    bound = BoundPayloadInstanceCandidate(
        label="bound_pitch_relation_payload_C4_G4_candidate",
        source_contract_label=contract.label,
        payload_schema=payload.payload_schema,
        validation_generated=False,
        module_processing_started=False,
    )
    return PayloadInstanceBindingObservation(
        contract_obs,
        payload,
        gamma,
        bound,
        "bound_payload_instance_candidate_observed_not_validated",
    )


def compare_payload_instance_binding() -> tuple[
    PayloadInstanceBindingObservation, PayloadInstanceBindingObservation
]:
    contract = contract_observation()
    payload = payload_instance_fixture()
    return (
        bind_payload_instance(contract, payload, None),
        bind_payload_instance(contract, payload, binding_gamma_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_payload_instance_binding()
    assert without_gamma.status == "payload_instance_not_bound_without_gamma"
    assert with_gamma.status == "bound_payload_instance_candidate_observed_not_validated"
    assert with_gamma.bound_payload is not None
    assert with_gamma.bound_payload.validation_generated is False
    assert with_gamma.bound_payload.module_processing_started is False
    assert with_gamma.payload_instance is not None
    assert with_gamma.payload_instance.generated_by_adopted_contract is False


if __name__ == "__main__":
    run_checks()
    print(compare_payload_instance_binding()[1].status)
