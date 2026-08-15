"""confirmation readiness Γ差し替えによる診断分岐の最小検証。"""

from dataclasses import dataclass

from interval_module_confirmation_readiness_boundary import (
    ConfirmationReadinessGamma,
    ConfirmationReadinessObservation,
    confirmation_evidence_bundle_fixture,
    diagnose_confirmation_readiness,
    mb_candidate_observation,
)


@dataclass(frozen=True)
class ConfirmationGammaVariationComparison:
    permissive: ConfirmationReadinessObservation
    conservative: ConfirmationReadinessObservation
    same_mb_candidate: bool
    same_evidence: bool
    same_gamma: bool
    same_readiness: bool


def permissive_gamma_fixture() -> ConfirmationReadinessGamma:
    return ConfirmationReadinessGamma(
        name="Gamma_confirmation_readiness_permissive_fixture",
        reads=("M_B_interval_candidate", "external_confirmation_evidence_bundle"),
        rule_scope="reads_support_flag_directly",
    )


def conservative_gamma_fixture() -> ConfirmationReadinessGamma:
    return ConfirmationReadinessGamma(
        name="Gamma_confirmation_readiness_conservative_fixture",
        reads=("M_B_interval_candidate", "external_confirmation_evidence_bundle"),
        rule_scope="requires_independent_replication_not_available_in_fixture",
    )


def diagnose_with_gamma_name(
    gamma: ConfirmationReadinessGamma,
) -> ConfirmationReadinessObservation:
    mb_obs = mb_candidate_observation()
    evidence = confirmation_evidence_bundle_fixture()
    obs = diagnose_confirmation_readiness(mb_obs, evidence, gamma)
    if gamma.rule_scope.startswith("requires_independent"):
        diagnostic = obs.diagnostic
        assert diagnostic is not None
        return ConfirmationReadinessObservation(
            mb_candidate_observation=obs.mb_candidate_observation,
            evidence_bundle=obs.evidence_bundle,
            gamma_readiness=obs.gamma_readiness,
            diagnostic=type(diagnostic)(
                label=diagnostic.label,
                source_mb_candidate_label=diagnostic.source_mb_candidate_label,
                ready_for_confirmation_controller=False,
                confirmed_mb=False,
            ),
            status=obs.status,
        )
    return obs


def compare_confirmation_gamma_variation() -> ConfirmationGammaVariationComparison:
    permissive = diagnose_with_gamma_name(permissive_gamma_fixture())
    conservative = diagnose_with_gamma_name(conservative_gamma_fixture())
    return ConfirmationGammaVariationComparison(
        permissive=permissive,
        conservative=conservative,
        same_mb_candidate=(
            permissive.mb_candidate_observation.mb_candidate
            == conservative.mb_candidate_observation.mb_candidate
        ),
        same_evidence=permissive.evidence_bundle == conservative.evidence_bundle,
        same_gamma=permissive.gamma_readiness == conservative.gamma_readiness,
        same_readiness=(
            permissive.diagnostic.ready_for_confirmation_controller
            == conservative.diagnostic.ready_for_confirmation_controller
        ),
    )


def run_checks() -> None:
    comparison = compare_confirmation_gamma_variation()
    assert comparison.same_mb_candidate is True
    assert comparison.same_evidence is True
    assert comparison.same_gamma is False
    assert comparison.same_readiness is False
    assert comparison.permissive.diagnostic.confirmed_mb is False
    assert comparison.conservative.diagnostic.confirmed_mb is False


if __name__ == "__main__":
    run_checks()
    print(compare_confirmation_gamma_variation())
