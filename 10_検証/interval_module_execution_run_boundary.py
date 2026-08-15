"""execution readiness診断とverification run観測境界の最小検証。"""

from dataclasses import dataclass

from interval_module_execution_readiness_boundary import (
    ExecutionReadinessObservation,
    compare_execution_readiness,
)


@dataclass(frozen=True)
class ExecutionController:
    name: str
    generated_by_readiness: bool


@dataclass(frozen=True)
class VerificationRunObservationCandidate:
    label: str
    source_readiness_label: str
    completed: bool
    classified: bool


@dataclass(frozen=True)
class VerificationRunBoundaryObservation:
    readiness_observation: ExecutionReadinessObservation
    execution_controller: ExecutionController | None
    run_observation: VerificationRunObservationCandidate | None
    status: str


def readiness_observation() -> ExecutionReadinessObservation:
    return compare_execution_readiness()[1]


def execution_controller_fixture() -> ExecutionController:
    return ExecutionController(
        name="interval_verification_execution_controller_fixture",
        generated_by_readiness=False,
    )


def execute_verification_packet(
    readiness: ExecutionReadinessObservation,
    controller: ExecutionController | None,
) -> VerificationRunBoundaryObservation:
    diagnostic = readiness.diagnostic
    if diagnostic is None:
        return VerificationRunBoundaryObservation(readiness, controller, None, "no_readiness_diagnostic")
    if controller is None:
        return VerificationRunBoundaryObservation(
            readiness, None, None, "verification_run_not_observed_without_controller"
        )
    if not diagnostic.ready_to_execute:
        return VerificationRunBoundaryObservation(
            readiness, controller, None, "verification_run_blocked_not_ready"
        )
    run = VerificationRunObservationCandidate(
        label="interval_verification_run_observation_candidate",
        source_readiness_label=diagnostic.label,
        completed=True,
        classified=False,
    )
    return VerificationRunBoundaryObservation(
        readiness, controller, run, "verification_run_observed_not_classified"
    )


def compare_verification_run() -> tuple[
    VerificationRunBoundaryObservation, VerificationRunBoundaryObservation
]:
    readiness = readiness_observation()
    return (
        execute_verification_packet(readiness, None),
        execute_verification_packet(readiness, execution_controller_fixture()),
    )


def run_checks() -> None:
    without_controller, with_controller = compare_verification_run()
    assert without_controller.status == "verification_run_not_observed_without_controller"
    assert with_controller.status == "verification_run_observed_not_classified"
    assert with_controller.run_observation is not None
    assert with_controller.run_observation.completed is True
    assert with_controller.run_observation.classified is False
    assert with_controller.execution_controller is not None
    assert with_controller.execution_controller.generated_by_readiness is False


if __name__ == "__main__":
    run_checks()
    print(compare_verification_run()[1].status)
