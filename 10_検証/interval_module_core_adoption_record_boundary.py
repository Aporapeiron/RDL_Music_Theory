"""Core compatibility診断とCore adoption record境界の最小検証。"""

from dataclasses import dataclass

from interval_module_core_compatibility_boundary import (
    CoreCompatibilityObservation,
    compare_core_compatibility,
)


@dataclass(frozen=True)
class CoreAdoptionGovernance:
    name: str
    requires_compatibility: bool
    generated_by_diagnostic: bool


@dataclass(frozen=True)
class CoreAdoptionRecordCandidate:
    label: str
    source_diagnostic_label: str
    core_mutated: bool


@dataclass(frozen=True)
class CoreAdoptionRecordObservation:
    compatibility_observation: CoreCompatibilityObservation
    governance: CoreAdoptionGovernance | None
    adoption_record: CoreAdoptionRecordCandidate | None
    status: str


def compatibility_observation() -> CoreCompatibilityObservation:
    return compare_core_compatibility()[1]


def governance_fixture() -> CoreAdoptionGovernance:
    return CoreAdoptionGovernance(
        name="core_adoption_governance_fixture",
        requires_compatibility=True,
        generated_by_diagnostic=False,
    )


def create_core_adoption_record(
    compatibility: CoreCompatibilityObservation,
    governance: CoreAdoptionGovernance | None,
) -> CoreAdoptionRecordObservation:
    diagnostic = compatibility.diagnostic
    if diagnostic is None:
        return CoreAdoptionRecordObservation(compatibility, governance, None, "no_compatibility_diagnostic")
    if governance is None:
        return CoreAdoptionRecordObservation(
            compatibility, None, None, "core_adoption_record_not_created_without_governance"
        )
    if governance.requires_compatibility and not diagnostic.compatible:
        return CoreAdoptionRecordObservation(
            compatibility, governance, None, "core_adoption_record_blocked_incompatible"
        )
    record = CoreAdoptionRecordCandidate(
        label="interval_core_adoption_record_candidate",
        source_diagnostic_label=diagnostic.label,
        core_mutated=False,
    )
    return CoreAdoptionRecordObservation(
        compatibility,
        governance,
        record,
        "core_adoption_record_candidate_observed_not_core_mutation",
    )


def compare_core_adoption_record() -> tuple[
    CoreAdoptionRecordObservation, CoreAdoptionRecordObservation
]:
    compatibility = compatibility_observation()
    without_governance = create_core_adoption_record(compatibility, None)
    with_governance = create_core_adoption_record(compatibility, governance_fixture())
    return without_governance, with_governance


def run_checks() -> None:
    without_governance, with_governance = compare_core_adoption_record()
    assert without_governance.status == "core_adoption_record_not_created_without_governance"
    assert with_governance.status == "core_adoption_record_candidate_observed_not_core_mutation"
    assert with_governance.adoption_record is not None
    assert with_governance.adoption_record.core_mutated is False
    assert with_governance.governance is not None
    assert with_governance.governance.generated_by_diagnostic is False


if __name__ == "__main__":
    run_checks()
    print(compare_core_adoption_record()[1])
