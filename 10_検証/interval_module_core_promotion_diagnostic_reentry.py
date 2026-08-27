"""再入M_B候補とCore昇格診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_core_promotion_diagnostic import (
    CorePromotionCriteria,
    CorePromotionDiagnostic,
    CorePromotionDiagnosticGamma,
    core_promotion_criteria_fixture,
    gamma_core_promotion_diagnostic_fixture,
)
from interval_module_mb_candidate_reentry import (
    ReenteredMBCandidateObservation,
    compare_mb_candidate_reentry,
)


@dataclass(frozen=True)
class ReenteredCorePromotionDiagnosticObservation:
    mb_candidate_observation: ReenteredMBCandidateObservation
    core_promotion_criteria: CorePromotionCriteria | None
    gamma_core_diagnostic: CorePromotionDiagnosticGamma | None
    diagnostic: CorePromotionDiagnostic | None
    status: str


def diagnose_reentered_core_promotion(
    mb_obs: ReenteredMBCandidateObservation,
    criteria: CorePromotionCriteria | None,
    gamma: CorePromotionDiagnosticGamma | None,
) -> ReenteredCorePromotionDiagnosticObservation:
    candidate = mb_obs.mb_candidate
    if candidate is None:
        return ReenteredCorePromotionDiagnosticObservation(mb_obs, criteria, gamma, None, "no_reentered_M_B_interval_candidate")
    if criteria is None:
        return ReenteredCorePromotionDiagnosticObservation(mb_obs, None, gamma, None, "reentered_core_promotion_not_checked_without_criteria")
    if gamma is None:
        return ReenteredCorePromotionDiagnosticObservation(mb_obs, criteria, None, None, "reentered_core_promotion_not_checked_without_gamma")
    diagnostic = CorePromotionDiagnostic(
        "interval_core_promotion_blocked_diagnostic",
        candidate.label,
        False,
        "M_B_candidate_is_not_confirmed",
        False,
    )
    return ReenteredCorePromotionDiagnosticObservation(mb_obs, criteria, gamma, diagnostic, "core_promotion_blocked_reentered_unconfirmed_M_B")


def compare_core_promotion_diagnostic_reentry() -> tuple[
    ReenteredCorePromotionDiagnosticObservation,
    ReenteredCorePromotionDiagnosticObservation,
]:
    mb_obs = compare_mb_candidate_reentry()[1]
    criteria = core_promotion_criteria_fixture()
    return (
        diagnose_reentered_core_promotion(mb_obs, criteria, None),
        diagnose_reentered_core_promotion(
            mb_obs, criteria, gamma_core_promotion_diagnostic_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_core_promotion_diagnostic_reentry()
    assert without_gamma.diagnostic is None
    assert with_gamma.diagnostic is not None
    assert with_gamma.diagnostic.promotable is False
    assert with_gamma.diagnostic.core_promoted is False


if __name__ == "__main__":
    run_checks()
    print(compare_core_promotion_diagnostic_reentry()[1].status)
