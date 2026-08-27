"""再入payload schema契約候補集合とinput contract adoption境界の最小検証。"""

from dataclasses import dataclass

from interval_module_input_contract_adoption import AdoptedInputReceptionContractCandidate, InputContractAdoptionController, adoption_controller_fixture
from interval_module_input_payload_schema_contract_reentry import ReenteredPayloadSchemaContractObservation, compare_payload_schema_contracts_reentry


@dataclass(frozen=True)
class ReenteredInputContractAdoptionObservation:
    schema_contract_observation: ReenteredPayloadSchemaContractObservation
    adoption_controller: InputContractAdoptionController | None
    adopted_contract: AdoptedInputReceptionContractCandidate | None
    status: str


def adopt_reentered_input_contract(schema_obs: ReenteredPayloadSchemaContractObservation, controller: InputContractAdoptionController | None) -> ReenteredInputContractAdoptionObservation:
    if not schema_obs.schema_contract_candidates:
        return ReenteredInputContractAdoptionObservation(schema_obs, controller, None, "no_reentered_payload_schema_contract_candidates")
    if controller is None:
        return ReenteredInputContractAdoptionObservation(schema_obs, None, None, "reentered_input_contract_not_adopted_without_controller")
    matches = tuple(c for c in schema_obs.schema_contract_candidates if c.payload_schema == controller.selected_payload_schema)
    adopted = AdoptedInputReceptionContractCandidate("adopted_interval_input_reception_contract_candidate", matches[0], False, False) if len(matches) == 1 else None
    status = "adopted_input_contract_observed_from_reentered_payload_schema_not_processed" if adopted else "reentered_input_contract_adoption_ambiguous"
    return ReenteredInputContractAdoptionObservation(schema_obs, controller, adopted, status)


def compare_input_contract_adoption_reentry() -> tuple[ReenteredInputContractAdoptionObservation, ReenteredInputContractAdoptionObservation]:
    schema = compare_payload_schema_contracts_reentry()[1]
    return adopt_reentered_input_contract(schema, None), adopt_reentered_input_contract(schema, adoption_controller_fixture())


def run_checks() -> None:
    without_controller, with_controller = compare_input_contract_adoption_reentry()
    assert without_controller.adopted_contract is None
    assert with_controller.adopted_contract is not None
    assert with_controller.adopted_contract.module_processing_started is False
    assert with_controller.adopted_contract.module_document_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_input_contract_adoption_reentry()[1].status)
