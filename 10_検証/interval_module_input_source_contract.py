"""selected input_reception clauseと入力source契約候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_contract_clause_selection import (
    ContractClauseSelectionObservation,
    compare_contract_clause_selection,
)


@dataclass(frozen=True)
class InputSourceInventory:
    name: str
    sources: tuple[str, ...]
    generated_by_selected_clause: bool


@dataclass(frozen=True)
class InputSourceContractGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class InputSourceContractCandidate:
    label: str
    source_kind: str
    payload_schema_generated: bool
    module_document_mutated: bool


@dataclass(frozen=True)
class InputSourceContractObservation:
    clause_selection_observation: ContractClauseSelectionObservation
    source_inventory: InputSourceInventory | None
    gamma_source_contract: InputSourceContractGamma | None
    source_contract_candidates: tuple[InputSourceContractCandidate, ...]
    status: str


def clause_selection_observation() -> ContractClauseSelectionObservation:
    return compare_contract_clause_selection()[1]


def input_source_inventory_fixture() -> InputSourceInventory:
    return InputSourceInventory(
        name="interval_input_source_inventory_fixture",
        sources=(
            "base_learned_core_input",
            "known_interval_theory_reference",
            "manual_payload_fixture",
        ),
        generated_by_selected_clause=False,
    )


def gamma_source_contract_fixture() -> InputSourceContractGamma:
    return InputSourceContractGamma(
        name="Gamma_interval_input_source_contract_fixture",
        reads=("selected_input_reception_clause", "external_input_source_inventory"),
        rule_scope="fixture_limited_not_payload_schema_generation",
    )


def generate_input_source_contracts(
    clause_selection: ContractClauseSelectionObservation,
    inventory: InputSourceInventory | None,
    gamma: InputSourceContractGamma | None,
) -> InputSourceContractObservation:
    selected = clause_selection.selected_clause
    if selected is None:
        return InputSourceContractObservation(
            clause_selection, inventory, gamma, (), "no_selected_contract_clause"
        )
    if selected.clause.surface != "input_reception":
        return InputSourceContractObservation(
            clause_selection,
            inventory,
            gamma,
            (),
            "selected_clause_is_not_input_reception",
        )
    if inventory is None:
        return InputSourceContractObservation(
            clause_selection,
            None,
            gamma,
            (),
            "input_source_contracts_not_generated_without_inventory",
        )
    if gamma is None:
        return InputSourceContractObservation(
            clause_selection,
            inventory,
            None,
            (),
            "input_source_contracts_not_generated_without_gamma",
        )
    contracts = tuple(
        InputSourceContractCandidate(
            label=f"interval_input_source_contract_{source}_candidate",
            source_kind=source,
            payload_schema_generated=False,
            module_document_mutated=False,
        )
        for source in inventory.sources
    )
    return InputSourceContractObservation(
        clause_selection,
        inventory,
        gamma,
        contracts,
        "input_source_contract_candidates_observed_not_payload_schema",
    )


def compare_input_source_contracts() -> tuple[
    InputSourceContractObservation, InputSourceContractObservation
]:
    clause_selection = clause_selection_observation()
    inventory = input_source_inventory_fixture()
    return (
        generate_input_source_contracts(clause_selection, inventory, None),
        generate_input_source_contracts(
            clause_selection, inventory, gamma_source_contract_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_input_source_contracts()
    assert without_gamma.status == "input_source_contracts_not_generated_without_gamma"
    assert (
        with_gamma.status
        == "input_source_contract_candidates_observed_not_payload_schema"
    )
    assert len(with_gamma.source_contract_candidates) == 3
    assert all(
        not candidate.payload_schema_generated
        for candidate in with_gamma.source_contract_candidates
    )
    assert all(
        not candidate.module_document_mutated
        for candidate in with_gamma.source_contract_candidates
    )
    assert with_gamma.source_inventory is not None
    assert with_gamma.source_inventory.generated_by_selected_clause is False


if __name__ == "__main__":
    run_checks()
    print(compare_input_source_contracts()[1].status)
