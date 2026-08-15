"""next verification plan候補とplan commitment境界の最小検証。"""

from dataclasses import dataclass

from interval_module_next_verification_plan_boundary import (
    NextVerificationPlanObservation,
    compare_next_verification_plan,
)


@dataclass(frozen=True)
class PlanCommitmentController:
    name: str
    generated_by_plan_candidate: bool


@dataclass(frozen=True)
class CommittedPlanCandidate:
    label: str
    source_plan_label: str
    target_xi: str
    executed: bool


@dataclass(frozen=True)
class PlanCommitmentObservation:
    plan_observation: NextVerificationPlanObservation
    controller: PlanCommitmentController | None
    committed_plan: CommittedPlanCandidate | None
    status: str


def plan_observation() -> NextVerificationPlanObservation:
    return compare_next_verification_plan()[1]


def commitment_controller_fixture() -> PlanCommitmentController:
    return PlanCommitmentController(
        name="interval_plan_commitment_controller_fixture",
        generated_by_plan_candidate=False,
    )


def commit_plan_candidate(
    plan_obs: NextVerificationPlanObservation,
    controller: PlanCommitmentController | None,
) -> PlanCommitmentObservation:
    plan = plan_obs.next_plan
    if plan is None:
        return PlanCommitmentObservation(plan_obs, controller, None, "no_next_plan_candidate")
    if controller is None:
        return PlanCommitmentObservation(
            plan_obs, None, None, "plan_not_committed_without_controller"
        )
    committed = CommittedPlanCandidate(
        label="committed_interval_verification_plan_candidate",
        source_plan_label=plan.label,
        target_xi=plan.next_xi,
        executed=False,
    )
    return PlanCommitmentObservation(
        plan_obs, controller, committed, "committed_plan_candidate_observed_not_executed"
    )


def compare_plan_commitment() -> tuple[PlanCommitmentObservation, PlanCommitmentObservation]:
    plan = plan_observation()
    return (
        commit_plan_candidate(plan, None),
        commit_plan_candidate(plan, commitment_controller_fixture()),
    )


def run_checks() -> None:
    without_controller, with_controller = compare_plan_commitment()
    assert without_controller.status == "plan_not_committed_without_controller"
    assert with_controller.status == "committed_plan_candidate_observed_not_executed"
    assert with_controller.committed_plan is not None
    assert with_controller.committed_plan.executed is False
    assert with_controller.controller is not None
    assert with_controller.controller.generated_by_plan_candidate is False


if __name__ == "__main__":
    run_checks()
    print(compare_plan_commitment()[1].status)
