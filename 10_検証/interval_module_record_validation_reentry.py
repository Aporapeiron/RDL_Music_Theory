"""再入module state record候補とvalidation境界の最小検証。"""

from dataclasses import dataclass

from interval_module_record_validation_boundary import (
    IntervalRecordValidationEvidence,
    ValidatedIntervalStateRecordCandidate,
    gamma_record_validation_fixture,
    validation_evidence_fixture,
)
from interval_module_state_record_reentry import (
    ReenteredStateRecordObservation,
    compare_state_record_reentry,
)


@dataclass(frozen=True)
class ReenteredRecordValidationObservation:
    state_record_observation: ReenteredStateRecordObservation
    validation_evidence: IntervalRecordValidationEvidence | None
    gamma_validation: object | None
    validated_record: ValidatedIntervalStateRecordCandidate | None
    status: str


def validate_reentered_record(
    record_obs: ReenteredStateRecordObservation,
    evidence: IntervalRecordValidationEvidence | None,
    gamma: object | None,
) -> ReenteredRecordValidationObservation:
    record = record_obs.state_record
    if record is None:
        return ReenteredRecordValidationObservation(record_obs, evidence, gamma, None, "no_reentered_state_record_candidate")
    if evidence is None:
        return ReenteredRecordValidationObservation(record_obs, None, gamma, None, "reentered_record_not_validated_without_evidence")
    if gamma is None:
        return ReenteredRecordValidationObservation(record_obs, evidence, None, None, "reentered_record_not_validated_without_gamma")
    if evidence.target_record_label != record.label:
        return ReenteredRecordValidationObservation(record_obs, evidence, gamma, None, "reentered_validation_evidence_not_applicable")
    validated = ValidatedIntervalStateRecordCandidate(
        "validated_interval_module_state_record_candidate",
        record.label,
        evidence.evidence_scope,
        False,
        False,
    )
    return ReenteredRecordValidationObservation(record_obs, evidence, gamma, validated, "validated_state_record_observed_from_reentered_record_not_M_B")


def compare_record_validation_reentry() -> tuple[
    ReenteredRecordValidationObservation, ReenteredRecordValidationObservation
]:
    record = compare_state_record_reentry()[1]
    evidence = validation_evidence_fixture()
    return (
        validate_reentered_record(record, evidence, None),
        validate_reentered_record(record, evidence, gamma_record_validation_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_record_validation_reentry()
    assert without_gamma.validated_record is None
    assert with_gamma.validated_record is not None
    assert with_gamma.validated_record.mb_candidate_generated is False


if __name__ == "__main__":
    run_checks()
    print(compare_record_validation_reentry()[1].status)
