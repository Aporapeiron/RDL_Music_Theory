"""selected next xiと音程Module契約一般化target境界の最小検証。"""

from dataclasses import dataclass

from interval_module_handoff_summary_boundary import (
    HandoffSummaryObservation,
    compare_handoff_summary,
)


@dataclass(frozen=True)
class IntervalModulePlanReference:
    name: str
    target_document: str
    generated_by_selected_xi: bool


@dataclass(frozen=True)
class ContractGeneralizationTargetCandidate:
    label: str
    source_selected_xi: str
    target_document: str
    contract_clauses_generated: bool


@dataclass(frozen=True)
class ContractGeneralizationTargetObservation:
    handoff_observation: HandoffSummaryObservation
    module_plan_reference: IntervalModulePlanReference | None
    target_candidate: ContractGeneralizationTargetCandidate | None
    status: str


def handoff_observation() -> HandoffSummaryObservation:
    return compare_handoff_summary()[1]


def module_plan_reference_fixture() -> IntervalModulePlanReference:
    return IntervalModulePlanReference(
        name="interval_module_plan_reference_fixture",
        target_document="40_中核音楽理論/02_音程_Module計画.md",
        generated_by_selected_xi=False,
    )


def create_generalization_target(
    handoff: HandoffSummaryObservation,
    module_plan: IntervalModulePlanReference | None,
) -> ContractGeneralizationTargetObservation:
    selected = handoff.xi_selection_observation.selected_xi
    if selected is None:
        return ContractGeneralizationTargetObservation(
            handoff, module_plan, None, "no_selected_next_xi"
        )
    if module_plan is None:
        return ContractGeneralizationTargetObservation(
            handoff,
            None,
            None,
            "contract_generalization_target_not_created_without_module_plan",
        )
    target = ContractGeneralizationTargetCandidate(
        label="interval_module_contract_generalization_target_candidate",
        source_selected_xi=selected.selected_xi,
        target_document=module_plan.target_document,
        contract_clauses_generated=False,
    )
    return ContractGeneralizationTargetObservation(
        handoff,
        module_plan,
        target,
        "contract_generalization_target_candidate_observed_not_clauses",
    )


def compare_generalization_target() -> tuple[
    ContractGeneralizationTargetObservation, ContractGeneralizationTargetObservation
]:
    handoff = handoff_observation()
    return (
        create_generalization_target(handoff, None),
        create_generalization_target(handoff, module_plan_reference_fixture()),
    )


def run_checks() -> None:
    without_plan, with_plan = compare_generalization_target()
    assert (
        without_plan.status
        == "contract_generalization_target_not_created_without_module_plan"
    )
    assert (
        with_plan.status
        == "contract_generalization_target_candidate_observed_not_clauses"
    )
    assert with_plan.target_candidate is not None
    assert with_plan.target_candidate.source_selected_xi == (
        "xi_interval_module_contract_generalization"
    )
    assert with_plan.target_candidate.contract_clauses_generated is False
    assert with_plan.module_plan_reference is not None
    assert with_plan.module_plan_reference.generated_by_selected_xi is False


if __name__ == "__main__":
    run_checks()
    print(compare_generalization_target()[1].status)
