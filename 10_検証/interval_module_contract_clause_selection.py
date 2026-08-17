"""contract clause候補集合とselection境界の最小検証。"""

from dataclasses import dataclass

from interval_module_contract_clause_generation import (
    ContractClauseCandidate,
    ContractClauseGenerationObservation,
    compare_contract_clause_generation,
)


@dataclass(frozen=True)
class ContractClauseSelectionController:
    name: str
    selected_surface: str
    generated_by_clause_candidates: bool


@dataclass(frozen=True)
class SelectedContractClauseCandidate:
    clause: ContractClauseCandidate
    selected: bool
    module_document_mutated: bool


@dataclass(frozen=True)
class ContractClauseSelectionObservation:
    clause_generation_observation: ContractClauseGenerationObservation
    selection_controller: ContractClauseSelectionController | None
    selected_clause: SelectedContractClauseCandidate | None
    status: str


def clause_generation_observation() -> ContractClauseGenerationObservation:
    return compare_contract_clause_generation()[1]


def selection_controller_fixture() -> ContractClauseSelectionController:
    return ContractClauseSelectionController(
        name="interval_contract_clause_selection_controller_fixture",
        selected_surface="input_reception",
        generated_by_clause_candidates=False,
    )


def select_contract_clause(
    clause_obs: ContractClauseGenerationObservation,
    controller: ContractClauseSelectionController | None,
) -> ContractClauseSelectionObservation:
    if not clause_obs.clause_candidates:
        return ContractClauseSelectionObservation(
            clause_obs, controller, None, "no_contract_clause_candidates"
        )
    if controller is None:
        return ContractClauseSelectionObservation(
            clause_obs, None, None, "contract_clause_not_selected_without_controller"
        )
    matches = [
        clause
        for clause in clause_obs.clause_candidates
        if clause.surface == controller.selected_surface
    ]
    if len(matches) != 1:
        return ContractClauseSelectionObservation(
            clause_obs, controller, None, "contract_clause_selection_ambiguous"
        )
    selected = SelectedContractClauseCandidate(
        clause=matches[0],
        selected=True,
        module_document_mutated=False,
    )
    return ContractClauseSelectionObservation(
        clause_obs,
        controller,
        selected,
        "selected_contract_clause_candidate_observed_not_module_mutation",
    )


def compare_contract_clause_selection() -> tuple[
    ContractClauseSelectionObservation, ContractClauseSelectionObservation
]:
    clauses = clause_generation_observation()
    return (
        select_contract_clause(clauses, None),
        select_contract_clause(clauses, selection_controller_fixture()),
    )


def run_checks() -> None:
    without_controller, with_controller = compare_contract_clause_selection()
    assert (
        without_controller.status
        == "contract_clause_not_selected_without_controller"
    )
    assert (
        with_controller.status
        == "selected_contract_clause_candidate_observed_not_module_mutation"
    )
    assert with_controller.selected_clause is not None
    assert with_controller.selected_clause.selected is True
    assert with_controller.selected_clause.module_document_mutated is False
    assert with_controller.selection_controller is not None
    assert with_controller.selection_controller.generated_by_clause_candidates is False


if __name__ == "__main__":
    run_checks()
    print(compare_contract_clause_selection()[1].status)
