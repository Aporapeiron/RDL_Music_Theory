"""再入Core adoption recordからModule contract update候補へ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_contract_update_boundary import ModuleContractUpdateBoundary, ModuleContractUpdateCandidate, contract_update_boundary_fixture
from interval_module_core_adoption_record_reentry import ReenteredCoreAdoptionRecordObservation, compare_core_adoption_record_reentry


@dataclass(frozen=True)
class ReenteredContractUpdateObservation:
    adoption_record_observation: ReenteredCoreAdoptionRecordObservation
    update_boundary: ModuleContractUpdateBoundary | None
    update_candidate: ModuleContractUpdateCandidate | None
    status: str


def create_reentered_contract_update(
    adoption_record: ReenteredCoreAdoptionRecordObservation,
    boundary: ModuleContractUpdateBoundary | None,
) -> ReenteredContractUpdateObservation:
    record = adoption_record.adoption_record
    if record is None:
        return ReenteredContractUpdateObservation(adoption_record, boundary, None, "no_reentered_adoption_record_candidate")
    if boundary is None:
        return ReenteredContractUpdateObservation(adoption_record, None, None, "reentered_module_contract_update_not_created_without_boundary")
    update = ModuleContractUpdateCandidate("interval_module_contract_update_candidate", record.label, boundary.target_module, False)
    return ReenteredContractUpdateObservation(adoption_record, boundary, update, "module_contract_update_observed_from_reentered_adoption_record_not_mutation")


def compare_contract_update_reentry() -> tuple[ReenteredContractUpdateObservation, ReenteredContractUpdateObservation]:
    record = compare_core_adoption_record_reentry()[1]
    return (
        create_reentered_contract_update(record, None),
        create_reentered_contract_update(record, contract_update_boundary_fixture()),
    )


def run_checks() -> None:
    without_boundary, with_boundary = compare_contract_update_reentry()
    assert without_boundary.update_candidate is None
    assert with_boundary.update_candidate is not None
    assert with_boundary.update_candidate.module_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_contract_update_reentry()[1].status)
