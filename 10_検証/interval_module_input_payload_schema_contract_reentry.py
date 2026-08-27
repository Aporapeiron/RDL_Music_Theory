"""再入入力source契約候補とpayload schema契約候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_input_payload_schema_contract import PayloadSchemaContractCandidate, PayloadSchemaContractGamma, PayloadSchemaInventory, gamma_payload_schema_contract_fixture, payload_schema_inventory_fixture
from interval_module_input_source_contract_reentry import ReenteredInputSourceContractObservation, compare_input_source_contracts_reentry


@dataclass(frozen=True)
class ReenteredPayloadSchemaContractObservation:
    source_contract_observation: ReenteredInputSourceContractObservation
    schema_inventory: PayloadSchemaInventory | None
    gamma_schema_contract: PayloadSchemaContractGamma | None
    schema_contract_candidates: tuple[PayloadSchemaContractCandidate, ...]
    status: str


def generate_reentered_payload_schema_contracts(source_obs: ReenteredInputSourceContractObservation, inventory: PayloadSchemaInventory | None, gamma: PayloadSchemaContractGamma | None) -> ReenteredPayloadSchemaContractObservation:
    if not source_obs.source_contract_candidates:
        return ReenteredPayloadSchemaContractObservation(source_obs, inventory, gamma, (), "no_reentered_input_source_contract_candidates")
    if inventory is None:
        return ReenteredPayloadSchemaContractObservation(source_obs, None, gamma, (), "reentered_payload_schema_contracts_not_generated_without_inventory")
    if gamma is None:
        return ReenteredPayloadSchemaContractObservation(source_obs, inventory, None, (), "reentered_payload_schema_contracts_not_generated_without_gamma")
    sources = tuple(source for source in source_obs.source_contract_candidates if source.source_kind == gamma.accepted_source_kind)
    candidates = tuple(PayloadSchemaContractCandidate(f"interval_payload_schema_contract_{schema}_candidate", source, schema, False, False) for source in sources for schema in inventory.schemas)
    return ReenteredPayloadSchemaContractObservation(source_obs, inventory, gamma, candidates, "payload_schema_contract_candidates_observed_from_reentered_sources_not_adopted")


def compare_payload_schema_contracts_reentry() -> tuple[ReenteredPayloadSchemaContractObservation, ReenteredPayloadSchemaContractObservation]:
    sources = compare_input_source_contracts_reentry()[1]
    inventory = payload_schema_inventory_fixture()
    return generate_reentered_payload_schema_contracts(sources, inventory, None), generate_reentered_payload_schema_contracts(sources, inventory, gamma_payload_schema_contract_fixture())


def run_checks() -> None:
    without_gamma, with_gamma = compare_payload_schema_contracts_reentry()
    assert without_gamma.schema_contract_candidates == ()
    assert len(with_gamma.schema_contract_candidates) == 3
    assert all(not c.adopted for c in with_gamma.schema_contract_candidates)


if __name__ == "__main__":
    run_checks()
    print(compare_payload_schema_contracts_reentry()[1].status)
