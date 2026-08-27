"""再入Core compatibility診断からCore adoption recordへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_core_adoption_record_boundary import CoreAdoptionGovernance, CoreAdoptionRecordCandidate, governance_fixture
from interval_module_core_compatibility_reentry import ReenteredCoreCompatibilityObservation, compare_core_compatibility_reentry


@dataclass(frozen=True)
class ReenteredCoreAdoptionRecordObservation:
    compatibility_observation: ReenteredCoreCompatibilityObservation
    governance: CoreAdoptionGovernance | None
    adoption_record: CoreAdoptionRecordCandidate | None
    status: str


def create_reentered_core_adoption_record(
    compatibility: ReenteredCoreCompatibilityObservation,
    governance: CoreAdoptionGovernance | None,
) -> ReenteredCoreAdoptionRecordObservation:
    diagnostic = compatibility.diagnostic
    if diagnostic is None:
        return ReenteredCoreAdoptionRecordObservation(compatibility, governance, None, "no_reentered_compatibility_diagnostic")
    if governance is None:
        return ReenteredCoreAdoptionRecordObservation(compatibility, None, None, "reentered_core_adoption_record_not_created_without_governance")
    if governance.requires_compatibility and not diagnostic.compatible:
        return ReenteredCoreAdoptionRecordObservation(compatibility, governance, None, "reentered_core_adoption_record_blocked_incompatible")
    record = CoreAdoptionRecordCandidate("interval_core_adoption_record_candidate", diagnostic.label, False)
    return ReenteredCoreAdoptionRecordObservation(compatibility, governance, record, "core_adoption_record_observed_from_reentered_compatibility_not_core_mutation")


def compare_core_adoption_record_reentry() -> tuple[ReenteredCoreAdoptionRecordObservation, ReenteredCoreAdoptionRecordObservation]:
    compatibility = compare_core_compatibility_reentry()[1]
    return (
        create_reentered_core_adoption_record(compatibility, None),
        create_reentered_core_adoption_record(compatibility, governance_fixture()),
    )


def run_checks() -> None:
    without_governance, with_governance = compare_core_adoption_record_reentry()
    assert without_governance.adoption_record is None
    assert with_governance.adoption_record is not None
    assert with_governance.adoption_record.core_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_core_adoption_record_reentry()[1].status)
