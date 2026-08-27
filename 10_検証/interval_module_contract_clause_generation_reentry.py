"""再入契約一般化targetとcontract clause候補生成境界の最小検証。"""

from dataclasses import dataclass

from interval_module_contract_clause_generation import ContractClauseCandidate, ContractClauseGenerationGamma, ContractSurfaceInventory, contract_surface_inventory_fixture, gamma_clause_generation_fixture
from interval_module_contract_generalization_target_reentry import ReenteredContractGeneralizationTargetObservation, compare_generalization_target_reentry


@dataclass(frozen=True)
class ReenteredContractClauseGenerationObservation:
    target_observation: ReenteredContractGeneralizationTargetObservation
    surface_inventory: ContractSurfaceInventory | None
    gamma_clause_generation: ContractClauseGenerationGamma | None
    clause_candidates: tuple[ContractClauseCandidate, ...]
    status: str


def generate_reentered_contract_clauses(target_obs: ReenteredContractGeneralizationTargetObservation, inventory: ContractSurfaceInventory | None, gamma: ContractClauseGenerationGamma | None) -> ReenteredContractClauseGenerationObservation:
    target = target_obs.target_candidate
    if target is None:
        return ReenteredContractClauseGenerationObservation(target_obs, inventory, gamma, (), "no_reentered_contract_generalization_target")
    if inventory is None:
        return ReenteredContractClauseGenerationObservation(target_obs, None, gamma, (), "reentered_contract_clauses_not_generated_without_inventory")
    if gamma is None:
        return ReenteredContractClauseGenerationObservation(target_obs, inventory, None, (), "reentered_contract_clauses_not_generated_without_gamma")
    clauses = tuple(ContractClauseCandidate(f"interval_contract_clause_{surface}_candidate", surface, False) for surface in inventory.surfaces)
    return ReenteredContractClauseGenerationObservation(target_obs, inventory, gamma, clauses, "contract_clause_candidates_observed_from_reentered_target_not_module_mutation")


def compare_contract_clause_generation_reentry() -> tuple[ReenteredContractClauseGenerationObservation, ReenteredContractClauseGenerationObservation]:
    target = compare_generalization_target_reentry()[1]
    inventory = contract_surface_inventory_fixture()
    return generate_reentered_contract_clauses(target, inventory, None), generate_reentered_contract_clauses(target, inventory, gamma_clause_generation_fixture())


def run_checks() -> None:
    without_gamma, with_gamma = compare_contract_clause_generation_reentry()
    assert without_gamma.clause_candidates == ()
    assert len(with_gamma.clause_candidates) == 3
    assert all(not clause.module_document_mutated for clause in with_gamma.clause_candidates)


if __name__ == "__main__":
    run_checks()
    print(compare_contract_clause_generation_reentry()[1].status)
