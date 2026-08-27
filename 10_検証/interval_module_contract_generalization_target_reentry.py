"""再入handoff summaryと契約一般化target境界の最小検証。"""

from dataclasses import dataclass

from interval_module_contract_generalization_target import ContractGeneralizationTargetCandidate, IntervalModulePlanReference, module_plan_reference_fixture
from interval_module_handoff_summary_reentry import ReenteredHandoffSummaryObservation, compare_handoff_summary_reentry


@dataclass(frozen=True)
class ReenteredContractGeneralizationTargetObservation:
    handoff_observation: ReenteredHandoffSummaryObservation
    module_plan_reference: IntervalModulePlanReference | None
    target_candidate: ContractGeneralizationTargetCandidate | None
    status: str


def create_reentered_generalization_target(handoff: ReenteredHandoffSummaryObservation, module_plan: IntervalModulePlanReference | None) -> ReenteredContractGeneralizationTargetObservation:
    selected = handoff.xi_selection_observation.selected_xi
    if selected is None:
        return ReenteredContractGeneralizationTargetObservation(handoff, module_plan, None, "no_reentered_selected_next_xi")
    if module_plan is None:
        return ReenteredContractGeneralizationTargetObservation(handoff, None, None, "reentered_contract_generalization_target_not_created_without_module_plan")
    target = ContractGeneralizationTargetCandidate("interval_module_contract_generalization_target_candidate", selected.selected_xi, module_plan.target_document, False)
    return ReenteredContractGeneralizationTargetObservation(handoff, module_plan, target, "contract_generalization_target_observed_from_reentered_handoff_not_clauses")


def compare_generalization_target_reentry() -> tuple[ReenteredContractGeneralizationTargetObservation, ReenteredContractGeneralizationTargetObservation]:
    handoff = compare_handoff_summary_reentry()[1]
    return create_reentered_generalization_target(handoff, None), create_reentered_generalization_target(handoff, module_plan_reference_fixture())


def run_checks() -> None:
    without_plan, with_plan = compare_generalization_target_reentry()
    assert without_plan.target_candidate is None
    assert with_plan.target_candidate is not None
    assert with_plan.target_candidate.contract_clauses_generated is False


if __name__ == "__main__":
    run_checks()
    print(compare_generalization_target_reentry()[1].status)
