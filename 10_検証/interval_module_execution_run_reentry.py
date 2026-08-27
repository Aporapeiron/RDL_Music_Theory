"""再入execution readiness診断とverification run観測境界の最小検証。"""

from dataclasses import dataclass

from interval_module_execution_readiness_reentry import ReenteredExecutionReadinessObservation, compare_execution_readiness_reentry
from interval_module_execution_run_boundary import ExecutionController, VerificationRunObservationCandidate, execution_controller_fixture


@dataclass(frozen=True)
class ReenteredVerificationRunObservation:
    readiness_observation: ReenteredExecutionReadinessObservation
    execution_controller: ExecutionController | None
    run_observation: VerificationRunObservationCandidate | None
    status: str


def execute_reentered_verification_packet(readiness: ReenteredExecutionReadinessObservation, controller: ExecutionController | None) -> ReenteredVerificationRunObservation:
    diagnostic = readiness.diagnostic
    if diagnostic is None:
        return ReenteredVerificationRunObservation(readiness, controller, None, "no_reentered_readiness_diagnostic")
    if controller is None:
        return ReenteredVerificationRunObservation(readiness, None, None, "reentered_verification_run_not_observed_without_controller")
    if not diagnostic.ready_to_execute:
        return ReenteredVerificationRunObservation(readiness, controller, None, "reentered_verification_run_blocked_not_ready")
    run = VerificationRunObservationCandidate("interval_verification_run_observation_candidate", diagnostic.label, True, False)
    return ReenteredVerificationRunObservation(readiness, controller, run, "verification_run_observed_from_reentered_readiness_not_classified")


def compare_verification_run_reentry() -> tuple[ReenteredVerificationRunObservation, ReenteredVerificationRunObservation]:
    readiness = compare_execution_readiness_reentry()[1]
    return execute_reentered_verification_packet(readiness, None), execute_reentered_verification_packet(readiness, execution_controller_fixture())


def run_checks() -> None:
    without_controller, with_controller = compare_verification_run_reentry()
    assert without_controller.run_observation is None
    assert with_controller.run_observation is not None
    assert with_controller.run_observation.completed is True
    assert with_controller.run_observation.classified is False


if __name__ == "__main__":
    run_checks()
    print(compare_verification_run_reentry()[1].status)
