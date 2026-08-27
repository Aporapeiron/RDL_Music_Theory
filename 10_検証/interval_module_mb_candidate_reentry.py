"""再入validated state recordからM_B候補へ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_mb_candidate_boundary import (
    IntervalMBCandidate,
    IntervalMBCandidateCriteria,
    IntervalMBCandidateGamma,
    gamma_mb_candidate_fixture,
    mb_candidate_criteria_fixture,
)
from interval_module_record_validation_reentry import (
    ReenteredRecordValidationObservation,
    compare_record_validation_reentry,
)


@dataclass(frozen=True)
class ReenteredMBCandidateObservation:
    validation_observation: ReenteredRecordValidationObservation
    mb_criteria: IntervalMBCandidateCriteria | None
    gamma_mb_candidate: IntervalMBCandidateGamma | None
    mb_candidate: IntervalMBCandidate | None
    status: str


def project_reentered_mb_candidate(
    validation_obs: ReenteredRecordValidationObservation,
    criteria: IntervalMBCandidateCriteria | None,
    gamma: IntervalMBCandidateGamma | None,
) -> ReenteredMBCandidateObservation:
    validated = validation_obs.validated_record
    if validated is None:
        return ReenteredMBCandidateObservation(validation_obs, criteria, gamma, None, "no_reentered_validated_state_record")
    if criteria is None:
        return ReenteredMBCandidateObservation(validation_obs, None, gamma, None, "reentered_M_B_candidate_not_projected_without_criteria")
    if gamma is None:
        return ReenteredMBCandidateObservation(validation_obs, criteria, None, None, "reentered_M_B_candidate_not_projected_without_gamma")
    if validated.validation_scope != criteria.required_validation_scope:
        return ReenteredMBCandidateObservation(validation_obs, criteria, gamma, None, "reentered_M_B_candidate_criteria_not_applicable")
    candidate = IntervalMBCandidate(
        "M_B_interval_context_harmony_candidate",
        validated.label,
        criteria.criteria_scope,
        False,
        False,
    )
    return ReenteredMBCandidateObservation(validation_obs, criteria, gamma, candidate, "interval_M_B_candidate_observed_from_reentered_record_not_confirmed")


def compare_mb_candidate_reentry() -> tuple[
    ReenteredMBCandidateObservation, ReenteredMBCandidateObservation
]:
    validation = compare_record_validation_reentry()[1]
    criteria = mb_candidate_criteria_fixture()
    return (
        project_reentered_mb_candidate(validation, criteria, None),
        project_reentered_mb_candidate(validation, criteria, gamma_mb_candidate_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_mb_candidate_reentry()
    assert without_gamma.mb_candidate is None
    assert with_gamma.mb_candidate is not None
    assert with_gamma.mb_candidate.confirmed_mb is False
    assert with_gamma.mb_candidate.core_promoted is False


if __name__ == "__main__":
    run_checks()
    print(compare_mb_candidate_reentry()[1].status)
