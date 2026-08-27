"""再入selected input_reception clauseと入力source契約候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_contract_clause_selection_reentry import ReenteredContractClauseSelectionObservation, compare_contract_clause_selection_reentry
from interval_module_input_source_contract import InputSourceContractCandidate, InputSourceContractGamma, InputSourceInventory, gamma_source_contract_fixture, input_source_inventory_fixture


@dataclass(frozen=True)
class ReenteredInputSourceContractObservation:
    clause_selection_observation: ReenteredContractClauseSelectionObservation
    source_inventory: InputSourceInventory | None
    gamma_source_contract: InputSourceContractGamma | None
    source_contract_candidates: tuple[InputSourceContractCandidate, ...]
    status: str


def generate_reentered_input_source_contracts(selection: ReenteredContractClauseSelectionObservation, inventory: InputSourceInventory | None, gamma: InputSourceContractGamma | None) -> ReenteredInputSourceContractObservation:
    selected = selection.selected_clause
    if selected is None:
        return ReenteredInputSourceContractObservation(selection, inventory, gamma, (), "no_reentered_selected_contract_clause")
    if inventory is None:
        return ReenteredInputSourceContractObservation(selection, None, gamma, (), "reentered_input_source_contracts_not_generated_without_inventory")
    if gamma is None:
        return ReenteredInputSourceContractObservation(selection, inventory, None, (), "reentered_input_source_contracts_not_generated_without_gamma")
    contracts = tuple(InputSourceContractCandidate(f"interval_input_source_contract_{source}_candidate", source, False, False) for source in inventory.sources)
    return ReenteredInputSourceContractObservation(selection, inventory, gamma, contracts, "input_source_contract_candidates_observed_from_reentered_clause_not_payload_schema")


def compare_input_source_contracts_reentry() -> tuple[ReenteredInputSourceContractObservation, ReenteredInputSourceContractObservation]:
    selection = compare_contract_clause_selection_reentry()[1]
    inventory = input_source_inventory_fixture()
    return generate_reentered_input_source_contracts(selection, inventory, None), generate_reentered_input_source_contracts(selection, inventory, gamma_source_contract_fixture())


def run_checks() -> None:
    without_gamma, with_gamma = compare_input_source_contracts_reentry()
    assert without_gamma.source_contract_candidates == ()
    assert len(with_gamma.source_contract_candidates) == 3
    assert all(not c.payload_schema_generated for c in with_gamma.source_contract_candidates)


if __name__ == "__main__":
    run_checks()
    print(compare_input_source_contracts_reentry()[1].status)
