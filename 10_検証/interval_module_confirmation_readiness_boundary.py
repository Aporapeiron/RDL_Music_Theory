"""M_B^interval候補とconfirmation readiness診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_mb_candidate_boundary import (
    IntervalMBCandidateObservation,
    compare_mb_candidate_projection,
)


@dataclass(frozen=True)
class ConfirmationEvidenceBundle:
    name: str
    replication_scope: str
    supports_confirmation_readiness: bool
    generated_by_mb_candidate: bool


@dataclass(frozen=True)
class ConfirmationReadinessGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class ConfirmationReadinessDiagnostic:
    label: str
    source_mb_candidate_label: str
    ready_for_confirmation_controller: bool
    confirmed_mb: bool


@dataclass(frozen=True)
class ConfirmationReadinessObservation:
    mb_candidate_observation: IntervalMBCandidateObservation
    evidence_bundle: ConfirmationEvidenceBundle | None
    gamma_readiness: ConfirmationReadinessGamma | None
    diagnostic: ConfirmationReadinessDiagnostic | None
    status: str


def mb_candidate_observation() -> IntervalMBCandidateObservation:
    return compare_mb_candidate_projection()[1]


def confirmation_evidence_bundle_fixture() -> ConfirmationEvidenceBundle:
    return ConfirmationEvidenceBundle(
        name="interval_confirmation_evidence_bundle_fixture",
        replication_scope="fixture_cross_step_replay",
        supports_confirmation_readiness=True,
        generated_by_mb_candidate=False,
    )


def gamma_readiness_fixture() -> ConfirmationReadinessGamma:
    return ConfirmationReadinessGamma(
        name="Gamma_interval_confirmation_readiness_fixture",
        reads=("M_B_interval_candidate", "external_confirmation_evidence_bundle"),
        rule_scope="fixture_limited_readiness_not_confirmation",
    )


def diagnose_confirmation_readiness(
    mb_obs: IntervalMBCandidateObservation,
    evidence: ConfirmationEvidenceBundle | None,
    gamma_readiness: ConfirmationReadinessGamma | None,
) -> ConfirmationReadinessObservation:
    candidate = mb_obs.mb_candidate
    if candidate is None:
        return ConfirmationReadinessObservation(
            mb_candidate_observation=mb_obs,
            evidence_bundle=evidence,
            gamma_readiness=gamma_readiness,
            diagnostic=None,
            status="no_M_B_interval_candidate",
        )
    if evidence is None:
        return ConfirmationReadinessObservation(
            mb_candidate_observation=mb_obs,
            evidence_bundle=None,
            gamma_readiness=gamma_readiness,
            diagnostic=None,
            status="confirmation_readiness_not_checked_without_evidence",
        )
    if gamma_readiness is None:
        return ConfirmationReadinessObservation(
            mb_candidate_observation=mb_obs,
            evidence_bundle=evidence,
            gamma_readiness=None,
            diagnostic=None,
            status="confirmation_readiness_not_checked_without_gamma",
        )
    diagnostic = ConfirmationReadinessDiagnostic(
        label="interval_confirmation_readiness_diagnostic",
        source_mb_candidate_label=candidate.label,
        ready_for_confirmation_controller=evidence.supports_confirmation_readiness,
        confirmed_mb=False,
    )
    return ConfirmationReadinessObservation(
        mb_candidate_observation=mb_obs,
        evidence_bundle=evidence,
        gamma_readiness=gamma_readiness,
        diagnostic=diagnostic,
        status="confirmation_readiness_diagnostic_observed_not_confirmed_M_B",
    )


def compare_confirmation_readiness() -> tuple[
    ConfirmationReadinessObservation, ConfirmationReadinessObservation
]:
    mb_obs = mb_candidate_observation()
    evidence = confirmation_evidence_bundle_fixture()
    without_gamma = diagnose_confirmation_readiness(mb_obs, evidence, None)
    with_gamma = diagnose_confirmation_readiness(mb_obs, evidence, gamma_readiness_fixture())
    return without_gamma, with_gamma


def run_checks() -> None:
    without_gamma, with_gamma = compare_confirmation_readiness()
    assert without_gamma.status == "confirmation_readiness_not_checked_without_gamma"
    assert with_gamma.status == "confirmation_readiness_diagnostic_observed_not_confirmed_M_B"
    assert with_gamma.diagnostic is not None
    assert with_gamma.diagnostic.ready_for_confirmation_controller is True
    assert with_gamma.diagnostic.confirmed_mb is False
    assert with_gamma.evidence_bundle is not None
    assert with_gamma.evidence_bundle.generated_by_mb_candidate is False


if __name__ == "__main__":
    run_checks()
    print(compare_confirmation_readiness()[1])
