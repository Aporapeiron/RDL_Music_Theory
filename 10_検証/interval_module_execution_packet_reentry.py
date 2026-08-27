"""再入committed planからexecution packet候補へ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_execution_packet_boundary import ExecutionPacketCandidate, ExecutionScopeBoundary, execution_scope_boundary_fixture
from interval_module_plan_commitment_reentry import ReenteredPlanCommitmentObservation, compare_plan_commitment_reentry


@dataclass(frozen=True)
class ReenteredExecutionPacketObservation:
    commitment_observation: ReenteredPlanCommitmentObservation
    scope_boundary: ExecutionScopeBoundary | None
    execution_packet: ExecutionPacketCandidate | None
    status: str


def create_reentered_execution_packet(commitment: ReenteredPlanCommitmentObservation, scope: ExecutionScopeBoundary | None) -> ReenteredExecutionPacketObservation:
    committed = commitment.committed_plan
    if committed is None:
        return ReenteredExecutionPacketObservation(commitment, scope, None, "no_reentered_committed_plan_candidate")
    if scope is None:
        return ReenteredExecutionPacketObservation(commitment, None, None, "reentered_execution_packet_not_created_without_scope_boundary")
    packet = ExecutionPacketCandidate("interval_verification_execution_packet_candidate", committed.label, scope.includes_structural_compression, False)
    return ReenteredExecutionPacketObservation(commitment, scope, packet, "execution_packet_observed_from_reentered_committed_plan_not_executed")


def compare_execution_packet_reentry() -> tuple[ReenteredExecutionPacketObservation, ReenteredExecutionPacketObservation]:
    commitment = compare_plan_commitment_reentry()[1]
    return create_reentered_execution_packet(commitment, None), create_reentered_execution_packet(commitment, execution_scope_boundary_fixture())


def run_checks() -> None:
    without_scope, with_scope = compare_execution_packet_reentry()
    assert without_scope.execution_packet is None
    assert with_scope.execution_packet is not None
    assert with_scope.execution_packet.executed is False
    assert with_scope.execution_packet.includes_structural_compression is True


if __name__ == "__main__":
    run_checks()
    print(compare_execution_packet_reentry()[1].status)
