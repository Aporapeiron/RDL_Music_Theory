"""入力source契約候補とpayload schema契約候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_input_source_contract import (
    InputSourceContractCandidate,
    InputSourceContractObservation,
    compare_input_source_contracts,
)


@dataclass(frozen=True)
class PayloadSchemaInventory:
    name: str
    schemas: tuple[str, ...]
    generated_by_source_contracts: bool


@dataclass(frozen=True)
class PayloadSchemaContractGamma:
    name: str
    reads: tuple[str, str]
    accepted_source_kind: str
    rule_scope: str


@dataclass(frozen=True)
class PayloadSchemaContractCandidate:
    label: str
    source_contract: InputSourceContractCandidate
    payload_schema: str
    adopted: bool
    module_document_mutated: bool


@dataclass(frozen=True)
class PayloadSchemaContractObservation:
    source_contract_observation: InputSourceContractObservation
    schema_inventory: PayloadSchemaInventory | None
    gamma_schema_contract: PayloadSchemaContractGamma | None
    schema_contract_candidates: tuple[PayloadSchemaContractCandidate, ...]
    status: str


def source_contract_observation() -> InputSourceContractObservation:
    return compare_input_source_contracts()[1]


def payload_schema_inventory_fixture() -> PayloadSchemaInventory:
    return PayloadSchemaInventory(
        name="interval_payload_schema_inventory_fixture",
        schemas=(
            "pitch_relation_payload",
            "spelled_interval_payload",
            "contextual_role_payload",
        ),
        generated_by_source_contracts=False,
    )


def gamma_payload_schema_contract_fixture() -> PayloadSchemaContractGamma:
    return PayloadSchemaContractGamma(
        name="Gamma_interval_payload_schema_contract_fixture",
        reads=("input_source_contract_candidates", "external_payload_schema_inventory"),
        accepted_source_kind="base_learned_core_input",
        rule_scope="fixture_limited_not_input_adoption_rule",
    )


def generate_payload_schema_contracts(
    source_obs: InputSourceContractObservation,
    inventory: PayloadSchemaInventory | None,
    gamma: PayloadSchemaContractGamma | None,
) -> PayloadSchemaContractObservation:
    if not source_obs.source_contract_candidates:
        return PayloadSchemaContractObservation(
            source_obs, inventory, gamma, (), "no_input_source_contract_candidates"
        )
    if inventory is None:
        return PayloadSchemaContractObservation(
            source_obs,
            None,
            gamma,
            (),
            "payload_schema_contracts_not_generated_without_inventory",
        )
    if gamma is None:
        return PayloadSchemaContractObservation(
            source_obs,
            inventory,
            None,
            (),
            "payload_schema_contracts_not_generated_without_gamma",
        )
    accepted_sources = tuple(
        source
        for source in source_obs.source_contract_candidates
        if source.source_kind == gamma.accepted_source_kind
    )
    candidates = tuple(
        PayloadSchemaContractCandidate(
            label=f"interval_payload_schema_contract_{schema}_candidate",
            source_contract=source,
            payload_schema=schema,
            adopted=False,
            module_document_mutated=False,
        )
        for source in accepted_sources
        for schema in inventory.schemas
    )
    return PayloadSchemaContractObservation(
        source_obs,
        inventory,
        gamma,
        candidates,
        "payload_schema_contract_candidates_observed_not_adopted",
    )


def compare_payload_schema_contracts() -> tuple[
    PayloadSchemaContractObservation, PayloadSchemaContractObservation
]:
    source_obs = source_contract_observation()
    inventory = payload_schema_inventory_fixture()
    return (
        generate_payload_schema_contracts(source_obs, inventory, None),
        generate_payload_schema_contracts(
            source_obs, inventory, gamma_payload_schema_contract_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_payload_schema_contracts()
    assert without_gamma.status == "payload_schema_contracts_not_generated_without_gamma"
    assert with_gamma.status == "payload_schema_contract_candidates_observed_not_adopted"
    assert len(with_gamma.schema_contract_candidates) == 3
    assert all(
        candidate.source_contract.source_kind == "base_learned_core_input"
        for candidate in with_gamma.schema_contract_candidates
    )
    assert all(not candidate.adopted for candidate in with_gamma.schema_contract_candidates)
    assert all(
        not candidate.module_document_mutated
        for candidate in with_gamma.schema_contract_candidates
    )
    assert with_gamma.schema_inventory is not None
    assert with_gamma.schema_inventory.generated_by_source_contracts is False


if __name__ == "__main__":
    run_checks()
    print(compare_payload_schema_contracts()[1].status)
