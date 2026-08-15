"""M_B^interval候補とCore昇格診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_mb_candidate_boundary import (
    IntervalMBCandidateObservation,
    compare_mb_candidate_projection,
)


@dataclass(frozen=True)
class CorePromotionCriteria:
    name: str
    requires_confirmed_mb: bool
    allows_candidate_only: bool
    generated_by_mb_candidate: bool


@dataclass(frozen=True)
class CorePromotionDiagnosticGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class CorePromotionDiagnostic:
    label: str
    source_mb_candidate_label: str
    promotable: bool
    blocked_reason: str | None
    core_promoted: bool


@dataclass(frozen=True)
class CorePromotionDiagnosticObservation:
    mb_candidate_observation: IntervalMBCandidateObservation
    core_promotion_criteria: CorePromotionCriteria | None
    gamma_core_diagnostic: CorePromotionDiagnosticGamma | None
    diagnostic: CorePromotionDiagnostic | None
    status: str


def mb_candidate_observation() -> IntervalMBCandidateObservation:
    return compare_mb_candidate_projection()[1]


def core_promotion_criteria_fixture() -> CorePromotionCriteria:
    return CorePromotionCriteria(
        name="interval_core_promotion_criteria_fixture",
        requires_confirmed_mb=True,
        allows_candidate_only=False,
        generated_by_mb_candidate=False,
    )


def gamma_core_promotion_diagnostic_fixture() -> CorePromotionDiagnosticGamma:
    return CorePromotionDiagnosticGamma(
        name="Gamma_interval_core_promotion_diagnostic_fixture",
        reads=("M_B_interval_candidate", "external_core_promotion_criteria"),
        rule_scope="fixture_limited_diagnostic_not_core_mutation",
    )


def diagnose_core_promotion(
    mb_obs: IntervalMBCandidateObservation,
    criteria: CorePromotionCriteria | None,
    gamma_core_diagnostic: CorePromotionDiagnosticGamma | None,
) -> CorePromotionDiagnosticObservation:
    candidate = mb_obs.mb_candidate
    if candidate is None:
        return CorePromotionDiagnosticObservation(
            mb_candidate_observation=mb_obs,
            core_promotion_criteria=criteria,
            gamma_core_diagnostic=gamma_core_diagnostic,
            diagnostic=None,
            status="no_M_B_interval_candidate",
        )
    if criteria is None:
        return CorePromotionDiagnosticObservation(
            mb_candidate_observation=mb_obs,
            core_promotion_criteria=None,
            gamma_core_diagnostic=gamma_core_diagnostic,
            diagnostic=None,
            status="core_promotion_not_checked_without_criteria",
        )
    if gamma_core_diagnostic is None:
        return CorePromotionDiagnosticObservation(
            mb_candidate_observation=mb_obs,
            core_promotion_criteria=criteria,
            gamma_core_diagnostic=None,
            diagnostic=None,
            status="core_promotion_not_checked_without_gamma",
        )

    if criteria.requires_confirmed_mb and not candidate.confirmed_mb:
        diagnostic = CorePromotionDiagnostic(
            label="interval_core_promotion_blocked_diagnostic",
            source_mb_candidate_label=candidate.label,
            promotable=False,
            blocked_reason="M_B_candidate_is_not_confirmed",
            core_promoted=False,
        )
        return CorePromotionDiagnosticObservation(
            mb_candidate_observation=mb_obs,
            core_promotion_criteria=criteria,
            gamma_core_diagnostic=gamma_core_diagnostic,
            diagnostic=diagnostic,
            status="core_promotion_blocked_unconfirmed_M_B",
        )

    diagnostic = CorePromotionDiagnostic(
        label="interval_core_promotion_possible_diagnostic",
        source_mb_candidate_label=candidate.label,
        promotable=True,
        blocked_reason=None,
        core_promoted=False,
    )
    return CorePromotionDiagnosticObservation(
        mb_candidate_observation=mb_obs,
        core_promotion_criteria=criteria,
        gamma_core_diagnostic=gamma_core_diagnostic,
        diagnostic=diagnostic,
        status="core_promotion_diagnostic_observed_not_core_mutation",
    )


def compare_core_promotion_diagnostic() -> tuple[
    CorePromotionDiagnosticObservation, CorePromotionDiagnosticObservation
]:
    mb_obs = mb_candidate_observation()
    criteria = core_promotion_criteria_fixture()
    without_gamma = diagnose_core_promotion(mb_obs, criteria, None)
    with_gamma = diagnose_core_promotion(
        mb_obs, criteria, gamma_core_promotion_diagnostic_fixture()
    )
    return without_gamma, with_gamma


def run_checks() -> None:
    without_gamma, with_gamma = compare_core_promotion_diagnostic()
    assert without_gamma.status == "core_promotion_not_checked_without_gamma"
    assert with_gamma.status == "core_promotion_blocked_unconfirmed_M_B"
    assert without_gamma.mb_candidate_observation.mb_candidate == (
        with_gamma.mb_candidate_observation.mb_candidate
    )
    assert without_gamma.core_promotion_criteria == with_gamma.core_promotion_criteria
    assert without_gamma.gamma_core_diagnostic != with_gamma.gamma_core_diagnostic
    assert with_gamma.diagnostic is not None
    assert with_gamma.diagnostic.promotable is False
    assert with_gamma.diagnostic.core_promoted is False
    assert with_gamma.core_promotion_criteria is not None
    assert with_gamma.core_promotion_criteria.generated_by_mb_candidate is False


def main() -> None:
    run_checks()
    without_gamma, with_gamma = compare_core_promotion_diagnostic()
    print("[pipeline]")
    print("  M_B^interval candidate")
    print("  + external Core promotion criteria")
    print("  + Gamma_interval_core_promotion_diagnostic_fixture")
    print("  -> Core promotion diagnostic")
    print(f"  without_gamma_status={without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(
        "  diagnostic="
        + (with_gamma.diagnostic.label if with_gamma.diagnostic else "None")
    )
    print("  Core is not mutated")


if __name__ == "__main__":
    main()
