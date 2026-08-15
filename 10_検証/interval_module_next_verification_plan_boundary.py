"""regression診断と次検証計画候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_contract_regression_diagnostic import (
    RegressionDiagnosticObservation,
    compare_regression_diagnostic,
)


@dataclass(frozen=True)
class VerificationPlanningController:
    name: str
    generated_by_regression: bool


@dataclass(frozen=True)
class NextVerificationPlanCandidate:
    label: str
    source_regression_diagnostic_label: str
    next_xi: str
    plan_committed: bool


@dataclass(frozen=True)
class NextVerificationPlanObservation:
    regression_observation: RegressionDiagnosticObservation
    planning_controller: VerificationPlanningController | None
    next_plan: NextVerificationPlanCandidate | None
    status: str


def regression_observation() -> RegressionDiagnosticObservation:
    return compare_regression_diagnostic()[1]


def planning_controller_fixture() -> VerificationPlanningController:
    return VerificationPlanningController(
        name="interval_next_verification_planning_controller_fixture",
        generated_by_regression=False,
    )


def create_next_plan(
    regression_obs: RegressionDiagnosticObservation,
    controller: VerificationPlanningController | None,
) -> NextVerificationPlanObservation:
    diagnostic = regression_obs.diagnostic
    if diagnostic is None:
        return NextVerificationPlanObservation(regression_obs, controller, None, "no_regression_diagnostic")
    if controller is None:
        return NextVerificationPlanObservation(
            regression_obs, None, None, "next_verification_plan_not_created_without_controller"
        )
    plan = NextVerificationPlanCandidate(
        label="interval_next_verification_plan_candidate",
        source_regression_diagnostic_label=diagnostic.label,
        next_xi="xi_interval_module_contract_generalization",
        plan_committed=False,
    )
    return NextVerificationPlanObservation(
        regression_obs,
        controller,
        plan,
        "next_verification_plan_candidate_observed_not_committed_plan",
    )


def compare_next_verification_plan() -> tuple[
    NextVerificationPlanObservation, NextVerificationPlanObservation
]:
    regression = regression_observation()
    without_controller = create_next_plan(regression, None)
    with_controller = create_next_plan(regression, planning_controller_fixture())
    return without_controller, with_controller


def run_checks() -> None:
    without_controller, with_controller = compare_next_verification_plan()
    assert without_controller.status == "next_verification_plan_not_created_without_controller"
    assert with_controller.status == "next_verification_plan_candidate_observed_not_committed_plan"
    assert with_controller.next_plan is not None
    assert with_controller.next_plan.plan_committed is False
    assert with_controller.planning_controller is not None
    assert with_controller.planning_controller.generated_by_regression is False


if __name__ == "__main__":
    run_checks()
    print(compare_next_verification_plan()[1])
