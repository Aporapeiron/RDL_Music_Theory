"""再入regression診断から次検証計画候補へ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_contract_regression_reentry import ReenteredRegressionDiagnosticObservation, compare_regression_reentry
from interval_module_next_verification_plan_boundary import NextVerificationPlanCandidate, VerificationPlanningController, planning_controller_fixture


@dataclass(frozen=True)
class ReenteredNextVerificationPlanObservation:
    regression_observation: ReenteredRegressionDiagnosticObservation
    planning_controller: VerificationPlanningController | None
    next_plan: NextVerificationPlanCandidate | None
    status: str


def create_reentered_next_plan(
    regression_obs: ReenteredRegressionDiagnosticObservation,
    controller: VerificationPlanningController | None,
) -> ReenteredNextVerificationPlanObservation:
    diagnostic = regression_obs.diagnostic
    if diagnostic is None:
        return ReenteredNextVerificationPlanObservation(regression_obs, controller, None, "no_reentered_regression_diagnostic")
    if controller is None:
        return ReenteredNextVerificationPlanObservation(regression_obs, None, None, "reentered_next_verification_plan_not_created_without_controller")
    plan = NextVerificationPlanCandidate("interval_next_verification_plan_candidate", diagnostic.label, "xi_interval_module_execution_readiness", False)
    return ReenteredNextVerificationPlanObservation(regression_obs, controller, plan, "next_verification_plan_observed_from_reentered_regression_not_committed")


def compare_next_verification_plan_reentry() -> tuple[ReenteredNextVerificationPlanObservation, ReenteredNextVerificationPlanObservation]:
    regression = compare_regression_reentry()[1]
    return (
        create_reentered_next_plan(regression, None),
        create_reentered_next_plan(regression, planning_controller_fixture()),
    )


def run_checks() -> None:
    without_controller, with_controller = compare_next_verification_plan_reentry()
    assert without_controller.next_plan is None
    assert with_controller.next_plan is not None
    assert with_controller.next_plan.plan_committed is False


if __name__ == "__main__":
    run_checks()
    print(compare_next_verification_plan_reentry()[1].status)
