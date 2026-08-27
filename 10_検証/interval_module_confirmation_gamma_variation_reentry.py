"""再入confirmation readiness Γ差し替えによる診断分岐の最小検証。"""

from dataclasses import dataclass

from interval_module_confirmation_readiness_boundary import (
    ConfirmationReadinessDiagnostic,
    ConfirmationReadinessGamma,
    confirmation_evidence_bundle_fixture,
)
from interval_module_confirmation_readiness_reentry import (
    ReenteredConfirmationReadinessObservation,
    diagnose_reentered_confirmation_readiness,
)
from interval_module_mb_candidate_reentry import compare_mb_candidate_reentry


@dataclass(frozen=True)
class ReenteredConfirmationGammaVariationComparison:
    permissive: ReenteredConfirmationReadinessObservation
    conservative: ReenteredConfirmationReadinessObservation
    same_mb_candidate: bool
    same_evidence: bool
    same_gamma: bool
    same_readiness: bool


def permissive_gamma_fixture() -> ConfirmationReadinessGamma:
    return ConfirmationReadinessGamma(
        "Gamma_confirmation_readiness_permissive_fixture",
        ("M_B_interval_candidate", "external_confirmation_evidence_bundle"),
        "reads_support_flag_directly",
    )


def conservative_gamma_fixture() -> ConfirmationReadinessGamma:
    return ConfirmationReadinessGamma(
        "Gamma_confirmation_readiness_conservative_fixture",
        ("M_B_interval_candidate", "external_confirmation_evidence_bundle"),
        "requires_independent_replication_not_available_in_fixture",
    )


def diagnose_with_reentered_gamma(
    gamma: ConfirmationReadinessGamma,
) -> ReenteredConfirmationReadinessObservation:
    mb_obs = compare_mb_candidate_reentry()[1]
    evidence = confirmation_evidence_bundle_fixture()
    obs = diagnose_reentered_confirmation_readiness(mb_obs, evidence, gamma)
    if gamma.rule_scope.startswith("requires_independent"):
        diagnostic = obs.diagnostic
        assert diagnostic is not None
        return ReenteredConfirmationReadinessObservation(
            obs.mb_candidate_observation,
            obs.evidence_bundle,
            obs.gamma_readiness,
            ConfirmationReadinessDiagnostic(
                diagnostic.label,
                diagnostic.source_mb_candidate_label,
                False,
                False,
            ),
            obs.status,
        )
    return obs


def compare_confirmation_gamma_variation_reentry() -> ReenteredConfirmationGammaVariationComparison:
    permissive = diagnose_with_reentered_gamma(permissive_gamma_fixture())
    conservative = diagnose_with_reentered_gamma(conservative_gamma_fixture())
    assert permissive.diagnostic is not None
    assert conservative.diagnostic is not None
    return ReenteredConfirmationGammaVariationComparison(
        permissive,
        conservative,
        permissive.mb_candidate_observation.mb_candidate == conservative.mb_candidate_observation.mb_candidate,
        permissive.evidence_bundle == conservative.evidence_bundle,
        permissive.gamma_readiness == conservative.gamma_readiness,
        permissive.diagnostic.ready_for_confirmation_controller == conservative.diagnostic.ready_for_confirmation_controller,
    )


def run_checks() -> None:
    comparison = compare_confirmation_gamma_variation_reentry()
    assert comparison.same_mb_candidate is True
    assert comparison.same_evidence is True
    assert comparison.same_gamma is False
    assert comparison.same_readiness is False
    assert comparison.permissive.diagnostic.confirmed_mb is False
    assert comparison.conservative.diagnostic.confirmed_mb is False


if __name__ == "__main__":
    run_checks()
    print("reentered_confirmation_gamma_variation_changes_readiness_not_confirmation")
