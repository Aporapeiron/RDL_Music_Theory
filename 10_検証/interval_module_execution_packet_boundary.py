"""committed plan候補とexecution packet境界の最小検証。"""

from dataclasses import dataclass

from interval_module_plan_commitment_boundary import (
    PlanCommitmentObservation,
    compare_plan_commitment,
)


@dataclass(frozen=True)
class ExecutionScopeBoundary:
    name: str
    includes_structural_compression: bool
    generated_by_committed_plan: bool


@dataclass(frozen=True)
class ExecutionPacketCandidate:
    label: str
    source_committed_plan_label: str
    includes_structural_compression: bool
    executed: bool


@dataclass(frozen=True)
class ExecutionPacketObservation:
    commitment_observation: PlanCommitmentObservation
    scope_boundary: ExecutionScopeBoundary | None
    execution_packet: ExecutionPacketCandidate | None
    status: str


def commitment_observation() -> PlanCommitmentObservation:
    return compare_plan_commitment()[1]


def execution_scope_boundary_fixture() -> ExecutionScopeBoundary:
    return ExecutionScopeBoundary(
        name="interval_execution_scope_boundary_fixture",
        includes_structural_compression=True,
        generated_by_committed_plan=False,
    )


def create_execution_packet(
    commitment: PlanCommitmentObservation,
    scope: ExecutionScopeBoundary | None,
) -> ExecutionPacketObservation:
    committed = commitment.committed_plan
    if committed is None:
        return ExecutionPacketObservation(commitment, scope, None, "no_committed_plan_candidate")
    if scope is None:
        return ExecutionPacketObservation(
            commitment, None, None, "execution_packet_not_created_without_scope_boundary"
        )
    packet = ExecutionPacketCandidate(
        label="interval_verification_execution_packet_candidate",
        source_committed_plan_label=committed.label,
        includes_structural_compression=scope.includes_structural_compression,
        executed=False,
    )
    return ExecutionPacketObservation(
        commitment, scope, packet, "execution_packet_candidate_observed_not_executed"
    )


def compare_execution_packet() -> tuple[ExecutionPacketObservation, ExecutionPacketObservation]:
    commitment = commitment_observation()
    return (
        create_execution_packet(commitment, None),
        create_execution_packet(commitment, execution_scope_boundary_fixture()),
    )


def run_checks() -> None:
    without_scope, with_scope = compare_execution_packet()
    assert without_scope.status == "execution_packet_not_created_without_scope_boundary"
    assert with_scope.status == "execution_packet_candidate_observed_not_executed"
    assert with_scope.execution_packet is not None
    assert with_scope.execution_packet.includes_structural_compression is True
    assert with_scope.execution_packet.executed is False
    assert with_scope.scope_boundary is not None
    assert with_scope.scope_boundary.generated_by_committed_plan is False


if __name__ == "__main__":
    run_checks()
    print(compare_execution_packet()[1].status)
