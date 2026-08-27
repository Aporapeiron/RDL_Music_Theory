"""再入next verification plan候補とplan commitment境界の最小検証。"""

from dataclasses import dataclass

from interval_module_next_verification_plan_reentry import ReenteredNextVerificationPlanObservation, compare_next_verification_plan_reentry
from interval_module_plan_commitment_boundary import CommittedPlanCandidate, PlanCommitmentController, commitment_controller_fixture


@dataclass(frozen=True)
class ReenteredPlanCommitmentObservation:
    plan_observation: ReenteredNextVerificationPlanObservation
    controller: PlanCommitmentController | None
    committed_plan: CommittedPlanCandidate | None
    status: str


def commit_reentered_plan(
    plan_obs: ReenteredNextVerificationPlanObservation,
    controller: PlanCommitmentController | None,
) -> ReenteredPlanCommitmentObservation:
    plan = plan_obs.next_plan
    if plan is None:
        return ReenteredPlanCommitmentObservation(plan_obs, controller, None, "no_reentered_next_plan_candidate")
    if controller is None:
        return ReenteredPlanCommitmentObservation(plan_obs, None, None, "reentered_plan_not_committed_without_controller")
    committed = CommittedPlanCandidate("committed_interval_verification_plan_candidate", plan.label, plan.next_xi, False)
    return ReenteredPlanCommitmentObservation(plan_obs, controller, committed, "committed_plan_observed_from_reentered_next_plan_not_executed")


def compare_plan_commitment_reentry() -> tuple[ReenteredPlanCommitmentObservation, ReenteredPlanCommitmentObservation]:
    plan = compare_next_verification_plan_reentry()[1]
    return (
        commit_reentered_plan(plan, None),
        commit_reentered_plan(plan, commitment_controller_fixture()),
    )


def run_checks() -> None:
    without_controller, with_controller = compare_plan_commitment_reentry()
    assert without_controller.committed_plan is None
    assert with_controller.committed_plan is not None
    assert with_controller.committed_plan.executed is False


if __name__ == "__main__":
    run_checks()
    print(compare_plan_commitment_reentry()[1].status)
