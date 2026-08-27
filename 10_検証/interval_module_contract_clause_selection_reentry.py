"""再入contract clause候補集合とselection境界の最小検証。"""

from dataclasses import dataclass

from interval_module_contract_clause_generation import ContractClauseCandidate
from interval_module_contract_clause_generation_reentry import ReenteredContractClauseGenerationObservation, compare_contract_clause_generation_reentry
from interval_module_contract_clause_selection import ContractClauseSelectionController, SelectedContractClauseCandidate, selection_controller_fixture


@dataclass(frozen=True)
class ReenteredContractClauseSelectionObservation:
    clause_generation_observation: ReenteredContractClauseGenerationObservation
    selection_controller: ContractClauseSelectionController | None
    selected_clause: SelectedContractClauseCandidate | None
    status: str


def select_reentered_contract_clause(clause_obs: ReenteredContractClauseGenerationObservation, controller: ContractClauseSelectionController | None) -> ReenteredContractClauseSelectionObservation:
    if not clause_obs.clause_candidates:
        return ReenteredContractClauseSelectionObservation(clause_obs, controller, None, "no_reentered_contract_clause_candidates")
    if controller is None:
        return ReenteredContractClauseSelectionObservation(clause_obs, None, None, "reentered_contract_clause_not_selected_without_controller")
    matches = tuple(clause for clause in clause_obs.clause_candidates if clause.surface == controller.selected_surface)
    selected = SelectedContractClauseCandidate(matches[0], True, False) if len(matches) == 1 else None
    status = "selected_contract_clause_observed_from_reentered_candidates_not_module_mutation" if selected else "reentered_contract_clause_selection_ambiguous"
    return ReenteredContractClauseSelectionObservation(clause_obs, controller, selected, status)


def compare_contract_clause_selection_reentry() -> tuple[ReenteredContractClauseSelectionObservation, ReenteredContractClauseSelectionObservation]:
    clauses = compare_contract_clause_generation_reentry()[1]
    return select_reentered_contract_clause(clauses, None), select_reentered_contract_clause(clauses, selection_controller_fixture())


def run_checks() -> None:
    without_controller, with_controller = compare_contract_clause_selection_reentry()
    assert without_controller.selected_clause is None
    assert with_controller.selected_clause is not None
    assert with_controller.selected_clause.selected is True
    assert with_controller.selected_clause.module_document_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_contract_clause_selection_reentry()[1].status)
