"""payload schema契約候補集合とinput contract adoption境界の最小検証。"""

from dataclasses import dataclass

from interval_module_input_payload_schema_contract import (
    PayloadSchemaContractCandidate,
    PayloadSchemaContractObservation,
    compare_payload_schema_contracts,
)


@dataclass(frozen=True)
class InputContractAdoptionController:
    name: str
    selected_payload_schema: str
    generated_by_schema_candidates: bool


@dataclass(frozen=True)
class AdoptedInputReceptionContractCandidate:
    label: str
    selected_schema_contract: PayloadSchemaContractCandidate
    module_processing_started: bool
    module_document_mutated: bool


@dataclass(frozen=True)
class InputContractAdoptionObservation:
    schema_contract_observation: PayloadSchemaContractObservation
    adoption_controller: InputContractAdoptionController | None
    adopted_contract: AdoptedInputReceptionContractCandidate | None
    status: str


def schema_contract_observation() -> PayloadSchemaContractObservation:
    return compare_payload_schema_contracts()[1]


def adoption_controller_fixture() -> InputContractAdoptionController:
    return InputContractAdoptionController(
        name="interval_input_contract_adoption_controller_fixture",
        selected_payload_schema="pitch_relation_payload",
        generated_by_schema_candidates=False,
    )


def adopt_input_contract(
    schema_obs: PayloadSchemaContractObservation,
    controller: InputContractAdoptionController | None,
) -> InputContractAdoptionObservation:
    if not schema_obs.schema_contract_candidates:
        return InputContractAdoptionObservation(
            schema_obs, controller, None, "no_payload_schema_contract_candidates"
        )
    if controller is None:
        return InputContractAdoptionObservation(
            schema_obs, None, None, "input_contract_not_adopted_without_controller"
        )
    matches = [
        candidate
        for candidate in schema_obs.schema_contract_candidates
        if candidate.payload_schema == controller.selected_payload_schema
    ]
    if len(matches) != 1:
        return InputContractAdoptionObservation(
            schema_obs, controller, None, "input_contract_adoption_ambiguous"
        )
    adopted = AdoptedInputReceptionContractCandidate(
        label="adopted_interval_input_reception_contract_candidate",
        selected_schema_contract=matches[0],
        module_processing_started=False,
        module_document_mutated=False,
    )
    return InputContractAdoptionObservation(
        schema_obs,
        controller,
        adopted,
        "adopted_input_reception_contract_candidate_observed_not_processed",
    )


def compare_input_contract_adoption() -> tuple[
    InputContractAdoptionObservation, InputContractAdoptionObservation
]:
    schema_obs = schema_contract_observation()
    return (
        adopt_input_contract(schema_obs, None),
        adopt_input_contract(schema_obs, adoption_controller_fixture()),
    )


def run_checks() -> None:
    without_controller, with_controller = compare_input_contract_adoption()
    assert without_controller.status == "input_contract_not_adopted_without_controller"
    assert (
        with_controller.status
        == "adopted_input_reception_contract_candidate_observed_not_processed"
    )
    assert with_controller.adopted_contract is not None
    assert (
        with_controller.adopted_contract.selected_schema_contract.payload_schema
        == "pitch_relation_payload"
    )
    assert with_controller.adopted_contract.module_processing_started is False
    assert with_controller.adopted_contract.module_document_mutated is False
    assert with_controller.adoption_controller is not None
    assert with_controller.adoption_controller.generated_by_schema_candidates is False


if __name__ == "__main__":
    run_checks()
    print(compare_input_contract_adoption()[1].status)
