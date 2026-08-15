"""音程Module state record候補とvalidation境界の最小検証。"""

from dataclasses import dataclass

from interval_module_state_record_boundary import (
    IntervalModuleStateRecordObservation,
    compare_state_record_creation,
)


@dataclass(frozen=True)
class IntervalRecordValidationEvidence:
    name: str
    target_record_label: str
    evidence_scope: str
    generated_by_state_record: bool


@dataclass(frozen=True)
class IntervalRecordValidationGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class ValidatedIntervalStateRecordCandidate:
    label: str
    source_state_record_label: str
    validation_scope: str
    mb_candidate_generated: bool
    core_promoted: bool


@dataclass(frozen=True)
class IntervalRecordValidationObservation:
    state_record_observation: IntervalModuleStateRecordObservation
    validation_evidence: IntervalRecordValidationEvidence | None
    gamma_validation: IntervalRecordValidationGamma | None
    validated_record: ValidatedIntervalStateRecordCandidate | None
    status: str
    validation_reason: str | None


def state_record_observation() -> IntervalModuleStateRecordObservation:
    return compare_state_record_creation().with_gamma


def validation_evidence_fixture() -> IntervalRecordValidationEvidence:
    return IntervalRecordValidationEvidence(
        name="interval_state_record_validation_evidence_fixture",
        target_record_label="interval_module_context_harmony_state_record_candidate",
        evidence_scope="fixture_replay_consistency",
        generated_by_state_record=False,
    )


def gamma_record_validation_fixture() -> IntervalRecordValidationGamma:
    return IntervalRecordValidationGamma(
        name="Gamma_interval_record_validation_fixture",
        reads=("state_record_candidate", "external_validation_evidence"),
        rule_scope="fixture_limited_record_validation_not_M_B_confirmation",
    )


def validate_record(
    state_record_obs: IntervalModuleStateRecordObservation,
    evidence: IntervalRecordValidationEvidence | None,
    gamma_validation: IntervalRecordValidationGamma | None,
) -> IntervalRecordValidationObservation:
    record = state_record_obs.state_record
    if record is None:
        return IntervalRecordValidationObservation(
            state_record_observation=state_record_obs,
            validation_evidence=evidence,
            gamma_validation=gamma_validation,
            validated_record=None,
            status="no_state_record_candidate",
            validation_reason=None,
        )
    if evidence is None:
        return IntervalRecordValidationObservation(
            state_record_observation=state_record_obs,
            validation_evidence=None,
            gamma_validation=gamma_validation,
            validated_record=None,
            status="record_not_validated_without_evidence",
            validation_reason=None,
        )
    if gamma_validation is None:
        return IntervalRecordValidationObservation(
            state_record_observation=state_record_obs,
            validation_evidence=evidence,
            gamma_validation=None,
            validated_record=None,
            status="record_not_validated_without_gamma",
            validation_reason=None,
        )
    if evidence.target_record_label != record.label:
        return IntervalRecordValidationObservation(
            state_record_observation=state_record_obs,
            validation_evidence=evidence,
            gamma_validation=gamma_validation,
            validated_record=None,
            status="validation_evidence_not_applicable",
            validation_reason="evidence_target_record_label_mismatch",
        )

    validated = ValidatedIntervalStateRecordCandidate(
        label="validated_interval_module_state_record_candidate",
        source_state_record_label=record.label,
        validation_scope=evidence.evidence_scope,
        mb_candidate_generated=False,
        core_promoted=False,
    )
    return IntervalRecordValidationObservation(
        state_record_observation=state_record_obs,
        validation_evidence=evidence,
        gamma_validation=gamma_validation,
        validated_record=validated,
        status="validated_state_record_candidate_observed_not_M_B",
        validation_reason="state_record_candidate_and_external_evidence_read_by_Gamma_validation",
    )


def compare_record_validation() -> tuple[
    IntervalRecordValidationObservation, IntervalRecordValidationObservation
]:
    record_obs = state_record_observation()
    evidence = validation_evidence_fixture()
    without_gamma = validate_record(record_obs, evidence, None)
    with_gamma = validate_record(record_obs, evidence, gamma_record_validation_fixture())
    return without_gamma, with_gamma


def run_checks() -> None:
    without_gamma, with_gamma = compare_record_validation()
    assert without_gamma.status == "record_not_validated_without_gamma"
    assert with_gamma.status == "validated_state_record_candidate_observed_not_M_B"
    assert without_gamma.state_record_observation.state_record == (
        with_gamma.state_record_observation.state_record
    )
    assert without_gamma.validation_evidence == with_gamma.validation_evidence
    assert without_gamma.gamma_validation != with_gamma.gamma_validation
    assert with_gamma.validated_record is not None
    assert with_gamma.validated_record.mb_candidate_generated is False
    assert with_gamma.validated_record.core_promoted is False
    assert with_gamma.validation_evidence is not None
    assert with_gamma.validation_evidence.generated_by_state_record is False


def main() -> None:
    run_checks()
    without_gamma, with_gamma = compare_record_validation()
    print("[pipeline]")
    print("  interval module state record candidate")
    print("  + external validation evidence")
    print("  + Gamma_interval_record_validation_fixture")
    print("  -> validated state record candidate")
    print(f"  without_gamma_status={without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(
        "  validated_record="
        + (with_gamma.validated_record.label if with_gamma.validated_record else "None")
    )
    print("  M_B candidate and Core promotion remain False")


if __name__ == "__main__":
    main()
