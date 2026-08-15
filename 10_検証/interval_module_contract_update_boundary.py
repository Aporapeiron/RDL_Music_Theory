"""Core adoption record候補とModule contract update候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_core_adoption_record_boundary import (
    CoreAdoptionRecordObservation,
    compare_core_adoption_record,
)


@dataclass(frozen=True)
class ModuleContractUpdateBoundary:
    name: str
    target_module: str
    generated_by_adoption_record: bool


@dataclass(frozen=True)
class ModuleContractUpdateCandidate:
    label: str
    source_adoption_record_label: str
    target_module: str
    module_mutated: bool


@dataclass(frozen=True)
class ModuleContractUpdateObservation:
    adoption_record_observation: CoreAdoptionRecordObservation
    update_boundary: ModuleContractUpdateBoundary | None
    update_candidate: ModuleContractUpdateCandidate | None
    status: str


def adoption_record_observation() -> CoreAdoptionRecordObservation:
    return compare_core_adoption_record()[1]


def contract_update_boundary_fixture() -> ModuleContractUpdateBoundary:
    return ModuleContractUpdateBoundary(
        name="interval_module_contract_update_boundary_fixture",
        target_module="40_中核音楽理論/02_音程_Module計画.md",
        generated_by_adoption_record=False,
    )


def create_contract_update_candidate(
    adoption_record: CoreAdoptionRecordObservation,
    update_boundary: ModuleContractUpdateBoundary | None,
) -> ModuleContractUpdateObservation:
    record = adoption_record.adoption_record
    if record is None:
        return ModuleContractUpdateObservation(adoption_record, update_boundary, None, "no_adoption_record_candidate")
    if update_boundary is None:
        return ModuleContractUpdateObservation(
            adoption_record, None, None, "module_contract_update_not_created_without_boundary"
        )
    update = ModuleContractUpdateCandidate(
        label="interval_module_contract_update_candidate",
        source_adoption_record_label=record.label,
        target_module=update_boundary.target_module,
        module_mutated=False,
    )
    return ModuleContractUpdateObservation(
        adoption_record,
        update_boundary,
        update,
        "module_contract_update_candidate_observed_not_module_mutation",
    )


def compare_contract_update_boundary() -> tuple[
    ModuleContractUpdateObservation, ModuleContractUpdateObservation
]:
    record = adoption_record_observation()
    without_boundary = create_contract_update_candidate(record, None)
    with_boundary = create_contract_update_candidate(
        record, contract_update_boundary_fixture()
    )
    return without_boundary, with_boundary


def run_checks() -> None:
    without_boundary, with_boundary = compare_contract_update_boundary()
    assert without_boundary.status == "module_contract_update_not_created_without_boundary"
    assert with_boundary.status == "module_contract_update_candidate_observed_not_module_mutation"
    assert with_boundary.update_candidate is not None
    assert with_boundary.update_candidate.module_mutated is False
    assert with_boundary.update_boundary is not None
    assert with_boundary.update_boundary.generated_by_adoption_record is False


if __name__ == "__main__":
    run_checks()
    print(compare_contract_update_boundary()[1])
