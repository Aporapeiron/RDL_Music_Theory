"""再入execution packet候補とexecution readiness診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_execution_packet_reentry import ReenteredExecutionPacketObservation, compare_execution_packet_reentry
from interval_module_execution_readiness_boundary import ExecutionReadinessDiagnostic, ExecutionResourceCheck, resource_check_fixture


@dataclass(frozen=True)
class ReenteredExecutionReadinessObservation:
    packet_observation: ReenteredExecutionPacketObservation
    resource_check: ExecutionResourceCheck | None
    diagnostic: ExecutionReadinessDiagnostic | None
    status: str


def diagnose_reentered_execution_readiness(packet_obs: ReenteredExecutionPacketObservation, check: ExecutionResourceCheck | None) -> ReenteredExecutionReadinessObservation:
    packet = packet_obs.execution_packet
    if packet is None:
        return ReenteredExecutionReadinessObservation(packet_obs, check, None, "no_reentered_execution_packet")
    if check is None:
        return ReenteredExecutionReadinessObservation(packet_obs, None, None, "reentered_execution_readiness_not_checked")
    diagnostic = ExecutionReadinessDiagnostic("interval_execution_readiness_diagnostic", packet.label, check.resources_available, False)
    return ReenteredExecutionReadinessObservation(packet_obs, check, diagnostic, "execution_readiness_observed_from_reentered_packet_not_executed")


def compare_execution_readiness_reentry() -> tuple[ReenteredExecutionReadinessObservation, ReenteredExecutionReadinessObservation]:
    packet = compare_execution_packet_reentry()[1]
    return diagnose_reentered_execution_readiness(packet, None), diagnose_reentered_execution_readiness(packet, resource_check_fixture())


def run_checks() -> None:
    without_check, with_check = compare_execution_readiness_reentry()
    assert without_check.diagnostic is None
    assert with_check.diagnostic is not None
    assert with_check.diagnostic.ready_to_execute is True
    assert with_check.diagnostic.executed is False


if __name__ == "__main__":
    run_checks()
    print(compare_execution_readiness_reentry()[1].status)
