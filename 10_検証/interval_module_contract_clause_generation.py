"""契約一般化targetとcontract clause候補生成境界の最小検証。"""

from dataclasses import dataclass

from interval_module_contract_generalization_target import (
    ContractGeneralizationTargetObservation,
    compare_generalization_target,
)


@dataclass(frozen=True)
class ContractSurfaceInventory:
    name: str
    surfaces: tuple[str, ...]
    generated_by_target: bool


@dataclass(frozen=True)
class ContractClauseGenerationGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class ContractClauseCandidate:
    label: str
    surface: str
    module_document_mutated: bool


@dataclass(frozen=True)
class ContractClauseGenerationObservation:
    target_observation: ContractGeneralizationTargetObservation
    surface_inventory: ContractSurfaceInventory | None
    gamma_clause_generation: ContractClauseGenerationGamma | None
    clause_candidates: tuple[ContractClauseCandidate, ...]
    status: str


def target_observation() -> ContractGeneralizationTargetObservation:
    return compare_generalization_target()[1]


def contract_surface_inventory_fixture() -> ContractSurfaceInventory:
    return ContractSurfaceInventory(
        name="interval_contract_surface_inventory_fixture",
        surfaces=("input_reception", "internal_processing", "post_context_connection"),
        generated_by_target=False,
    )


def gamma_clause_generation_fixture() -> ContractClauseGenerationGamma:
    return ContractClauseGenerationGamma(
        name="Gamma_interval_contract_clause_generation_fixture",
        reads=("contract_generalization_target", "external_contract_surface_inventory"),
        rule_scope="fixture_limited_not_module_document_mutation",
    )


def generate_contract_clauses(
    target_obs: ContractGeneralizationTargetObservation,
    inventory: ContractSurfaceInventory | None,
    gamma: ContractClauseGenerationGamma | None,
) -> ContractClauseGenerationObservation:
    target = target_obs.target_candidate
    if target is None:
        return ContractClauseGenerationObservation(
            target_obs, inventory, gamma, (), "no_contract_generalization_target"
        )
    if inventory is None:
        return ContractClauseGenerationObservation(
            target_obs,
            None,
            gamma,
            (),
            "contract_clauses_not_generated_without_inventory",
        )
    if gamma is None:
        return ContractClauseGenerationObservation(
            target_obs,
            inventory,
            None,
            (),
            "contract_clauses_not_generated_without_gamma",
        )
    clauses = tuple(
        ContractClauseCandidate(
            label=f"interval_contract_clause_{surface}_candidate",
            surface=surface,
            module_document_mutated=False,
        )
        for surface in inventory.surfaces
    )
    return ContractClauseGenerationObservation(
        target_obs,
        inventory,
        gamma,
        clauses,
        "contract_clause_candidates_observed_not_module_mutation",
    )


def compare_contract_clause_generation() -> tuple[
    ContractClauseGenerationObservation, ContractClauseGenerationObservation
]:
    target = target_observation()
    inventory = contract_surface_inventory_fixture()
    return (
        generate_contract_clauses(target, inventory, None),
        generate_contract_clauses(target, inventory, gamma_clause_generation_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_contract_clause_generation()
    assert without_gamma.status == "contract_clauses_not_generated_without_gamma"
    assert with_gamma.status == "contract_clause_candidates_observed_not_module_mutation"
    assert len(with_gamma.clause_candidates) == 3
    assert all(not clause.module_document_mutated for clause in with_gamma.clause_candidates)
    assert with_gamma.surface_inventory is not None
    assert with_gamma.surface_inventory.generated_by_target is False


if __name__ == "__main__":
    run_checks()
    print(compare_contract_clause_generation()[1].status)
