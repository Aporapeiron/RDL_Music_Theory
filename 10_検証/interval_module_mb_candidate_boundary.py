"""validated state record候補とM_B候補投影境界の最小検証。"""

from dataclasses import dataclass

from interval_module_record_validation_boundary import (
    IntervalRecordValidationObservation,
    compare_record_validation,
)


@dataclass(frozen=True)
class IntervalMBCandidateCriteria:
    name: str
    required_validation_scope: str
    criteria_scope: str
    generated_by_validated_record: bool


@dataclass(frozen=True)
class IntervalMBCandidateGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class IntervalMBCandidate:
    label: str
    source_validated_record_label: str
    criteria_scope: str
    confirmed_mb: bool
    core_promoted: bool


@dataclass(frozen=True)
class IntervalMBCandidateObservation:
    validation_observation: IntervalRecordValidationObservation
    mb_criteria: IntervalMBCandidateCriteria | None
    gamma_mb_candidate: IntervalMBCandidateGamma | None
    mb_candidate: IntervalMBCandidate | None
    status: str
    mb_candidate_reason: str | None


def validation_observation() -> IntervalRecordValidationObservation:
    return compare_record_validation()[1]


def mb_candidate_criteria_fixture() -> IntervalMBCandidateCriteria:
    return IntervalMBCandidateCriteria(
        name="interval_M_B_candidate_criteria_fixture",
        required_validation_scope="fixture_replay_consistency",
        criteria_scope="interval_module_candidate_only",
        generated_by_validated_record=False,
    )


def gamma_mb_candidate_fixture() -> IntervalMBCandidateGamma:
    return IntervalMBCandidateGamma(
        name="Gamma_interval_M_B_candidate_projection_fixture",
        reads=("validated_state_record_candidate", "external_M_B_candidate_criteria"),
        rule_scope="fixture_limited_M_B_candidate_not_confirmed_M_B",
    )


def project_mb_candidate(
    validation_obs: IntervalRecordValidationObservation,
    criteria: IntervalMBCandidateCriteria | None,
    gamma_mb_candidate: IntervalMBCandidateGamma | None,
) -> IntervalMBCandidateObservation:
    validated = validation_obs.validated_record
    if validated is None:
        return IntervalMBCandidateObservation(
            validation_observation=validation_obs,
            mb_criteria=criteria,
            gamma_mb_candidate=gamma_mb_candidate,
            mb_candidate=None,
            status="no_validated_state_record_candidate",
            mb_candidate_reason=None,
        )
    if criteria is None:
        return IntervalMBCandidateObservation(
            validation_observation=validation_obs,
            mb_criteria=None,
            gamma_mb_candidate=gamma_mb_candidate,
            mb_candidate=None,
            status="M_B_candidate_not_projected_without_criteria",
            mb_candidate_reason=None,
        )
    if gamma_mb_candidate is None:
        return IntervalMBCandidateObservation(
            validation_observation=validation_obs,
            mb_criteria=criteria,
            gamma_mb_candidate=None,
            mb_candidate=None,
            status="M_B_candidate_not_projected_without_gamma",
            mb_candidate_reason=None,
        )
    if validated.validation_scope != criteria.required_validation_scope:
        return IntervalMBCandidateObservation(
            validation_observation=validation_obs,
            mb_criteria=criteria,
            gamma_mb_candidate=gamma_mb_candidate,
            mb_candidate=None,
            status="M_B_candidate_criteria_not_applicable",
            mb_candidate_reason="validation_scope_mismatch",
        )

    candidate = IntervalMBCandidate(
        label="M_B_interval_context_harmony_candidate",
        source_validated_record_label=validated.label,
        criteria_scope=criteria.criteria_scope,
        confirmed_mb=False,
        core_promoted=False,
    )
    return IntervalMBCandidateObservation(
        validation_observation=validation_obs,
        mb_criteria=criteria,
        gamma_mb_candidate=gamma_mb_candidate,
        mb_candidate=candidate,
        status="interval_M_B_candidate_observed_not_confirmed",
        mb_candidate_reason="validated_record_and_external_M_B_criteria_read_by_Gamma_projection",
    )


def compare_mb_candidate_projection() -> tuple[
    IntervalMBCandidateObservation, IntervalMBCandidateObservation
]:
    validation_obs = validation_observation()
    criteria = mb_candidate_criteria_fixture()
    without_gamma = project_mb_candidate(validation_obs, criteria, None)
    with_gamma = project_mb_candidate(
        validation_obs, criteria, gamma_mb_candidate_fixture()
    )
    return without_gamma, with_gamma


def run_checks() -> None:
    without_gamma, with_gamma = compare_mb_candidate_projection()
    assert without_gamma.status == "M_B_candidate_not_projected_without_gamma"
    assert with_gamma.status == "interval_M_B_candidate_observed_not_confirmed"
    assert without_gamma.validation_observation.validated_record == (
        with_gamma.validation_observation.validated_record
    )
    assert without_gamma.mb_criteria == with_gamma.mb_criteria
    assert without_gamma.gamma_mb_candidate != with_gamma.gamma_mb_candidate
    assert with_gamma.mb_candidate is not None
    assert with_gamma.mb_candidate.confirmed_mb is False
    assert with_gamma.mb_candidate.core_promoted is False
    assert with_gamma.mb_criteria is not None
    assert with_gamma.mb_criteria.generated_by_validated_record is False


def main() -> None:
    run_checks()
    without_gamma, with_gamma = compare_mb_candidate_projection()
    print("[pipeline]")
    print("  validated state record candidate")
    print("  + external M_B candidate criteria")
    print("  + Gamma_interval_M_B_candidate_projection_fixture")
    print("  -> M_B^interval candidate")
    print(f"  without_gamma_status={without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(
        "  mb_candidate="
        + (with_gamma.mb_candidate.label if with_gamma.mb_candidate else "None")
    )
    print("  confirmed M_B and Core promotion remain False")


if __name__ == "__main__":
    main()
