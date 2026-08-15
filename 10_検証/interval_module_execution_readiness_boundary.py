"""execution packet候補とexecution readiness診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_execution_packet_boundary import (
    ExecutionPacketObservation,
    compare_execution_packet,
)


@dataclass(frozen=True)
class ExecutionResourceCheck:
    name: str
    resources_available: bool
    generated_by_packet: bool


@dataclass(frozen=True)
class ExecutionReadinessDiagnostic:
    label: str
    source_packet_label: str
    ready_to_execute: bool
    executed: bool


@dataclass(frozen=True)
class ExecutionReadinessObservation:
    packet_observation: ExecutionPacketObservation
    resource_check: ExecutionResourceCheck | None
    diagnostic: ExecutionReadinessDiagnostic | None
    status: str


def packet_observation() -> ExecutionPacketObservation:
    return compare_execution_packet()[1]


def resource_check_fixture() -> ExecutionResourceCheck:
    return ExecutionResourceCheck(
        name="interval_execution_resource_check_fixture",
        resources_available=True,
        generated_by_packet=False,
    )


def diagnose_execution_readiness(
    packet_obs: ExecutionPacketObservation,
    resource_check: ExecutionResourceCheck | None,
) -> ExecutionReadinessObservation:
    packet = packet_obs.execution_packet
    if packet is None:
        return ExecutionReadinessObservation(packet_obs, resource_check, None, "no_execution_packet")
    if resource_check is None:
        return ExecutionReadinessObservation(
            packet_obs, None, None, "execution_readiness_not_checked"
        )
    diagnostic = ExecutionReadinessDiagnostic(
        label="interval_execution_readiness_diagnostic",
        source_packet_label=packet.label,
        ready_to_execute=resource_check.resources_available,
        executed=False,
    )
    return ExecutionReadinessObservation(
        packet_obs, resource_check, diagnostic, "execution_readiness_diagnostic_observed"
    )


def compare_execution_readiness() -> tuple[
    ExecutionReadinessObservation, ExecutionReadinessObservation
]:
    packet = packet_observation()
    return (
        diagnose_execution_readiness(packet, None),
        diagnose_execution_readiness(packet, resource_check_fixture()),
    )


def run_checks() -> None:
    without_check, with_check = compare_execution_readiness()
    assert without_check.status == "execution_readiness_not_checked"
    assert with_check.status == "execution_readiness_diagnostic_observed"
    assert with_check.diagnostic is not None
    assert with_check.diagnostic.ready_to_execute is True
    assert with_check.diagnostic.executed is False
    assert with_check.resource_check is not None
    assert with_check.resource_check.generated_by_packet is False


if __name__ == "__main__":
    run_checks()
    print(compare_execution_readiness()[1].status)
