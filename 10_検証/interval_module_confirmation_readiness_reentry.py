"""再入M_B候補とconfirmation readiness診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_confirmation_readiness_boundary import (
    ConfirmationEvidenceBundle,
    ConfirmationReadinessDiagnostic,
    ConfirmationReadinessGamma,
    confirmation_evidence_bundle_fixture,
    gamma_readiness_fixture,
)
from interval_module_mb_candidate_reentry import (
    ReenteredMBCandidateObservation,
    compare_mb_candidate_reentry,
)


@dataclass(frozen=True)
class ReenteredConfirmationReadinessObservation:
    mb_candidate_observation: ReenteredMBCandidateObservation
    evidence_bundle: ConfirmationEvidenceBundle | None
    gamma_readiness: ConfirmationReadinessGamma | None
    diagnostic: ConfirmationReadinessDiagnostic | None
    status: str


def diagnose_reentered_confirmation_readiness(
    mb_obs: ReenteredMBCandidateObservation,
    evidence: ConfirmationEvidenceBundle | None,
    gamma: ConfirmationReadinessGamma | None,
) -> ReenteredConfirmationReadinessObservation:
    candidate = mb_obs.mb_candidate
    if candidate is None:
        return ReenteredConfirmationReadinessObservation(mb_obs, evidence, gamma, None, "no_reentered_M_B_interval_candidate")
    if evidence is None:
        return ReenteredConfirmationReadinessObservation(mb_obs, None, gamma, None, "reentered_confirmation_readiness_not_checked_without_evidence")
    if gamma is None:
        return ReenteredConfirmationReadinessObservation(mb_obs, evidence, None, None, "reentered_confirmation_readiness_not_checked_without_gamma")
    diagnostic = ConfirmationReadinessDiagnostic(
        "interval_confirmation_readiness_diagnostic",
        candidate.label,
        evidence.supports_confirmation_readiness,
        False,
    )
    return ReenteredConfirmationReadinessObservation(mb_obs, evidence, gamma, diagnostic, "confirmation_readiness_observed_from_reentered_M_B_not_confirmed")


def compare_confirmation_readiness_reentry() -> tuple[
    ReenteredConfirmationReadinessObservation,
    ReenteredConfirmationReadinessObservation,
]:
    mb_obs = compare_mb_candidate_reentry()[1]
    evidence = confirmation_evidence_bundle_fixture()
    return (
        diagnose_reentered_confirmation_readiness(mb_obs, evidence, None),
        diagnose_reentered_confirmation_readiness(mb_obs, evidence, gamma_readiness_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_confirmation_readiness_reentry()
    assert without_gamma.diagnostic is None
    assert with_gamma.diagnostic is not None
    assert with_gamma.diagnostic.ready_for_confirmation_controller is True
    assert with_gamma.diagnostic.confirmed_mb is False


if __name__ == "__main__":
    run_checks()
    print(compare_confirmation_readiness_reentry()[1].status)
