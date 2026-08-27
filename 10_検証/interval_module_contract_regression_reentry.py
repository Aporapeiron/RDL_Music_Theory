"""再入Module contract update候補とregression診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_contract_regression_diagnostic import RegressionDiagnostic, RegressionFixtureSet, regression_fixture_set
from interval_module_contract_update_reentry import ReenteredContractUpdateObservation, compare_contract_update_reentry


@dataclass(frozen=True)
class ReenteredRegressionDiagnosticObservation:
    update_observation: ReenteredContractUpdateObservation
    regression_fixtures: RegressionFixtureSet | None
    diagnostic: RegressionDiagnostic | None
    status: str


def diagnose_reentered_regression(
    update_obs: ReenteredContractUpdateObservation,
    fixtures: RegressionFixtureSet | None,
) -> ReenteredRegressionDiagnosticObservation:
    update = update_obs.update_candidate
    if update is None:
        return ReenteredRegressionDiagnosticObservation(update_obs, fixtures, None, "no_reentered_contract_update_candidate")
    if fixtures is None:
        return ReenteredRegressionDiagnosticObservation(update_obs, None, None, "reentered_regression_not_checked_without_fixtures")
    diagnostic = RegressionDiagnostic("interval_contract_regression_diagnostic", update.label, True, False)
    return ReenteredRegressionDiagnosticObservation(update_obs, fixtures, diagnostic, "regression_diagnostic_observed_from_reentered_update_not_module_mutation")


def compare_regression_reentry() -> tuple[ReenteredRegressionDiagnosticObservation, ReenteredRegressionDiagnosticObservation]:
    update = compare_contract_update_reentry()[1]
    return (
        diagnose_reentered_regression(update, None),
        diagnose_reentered_regression(update, regression_fixture_set()),
    )


def run_checks() -> None:
    without_fixtures, with_fixtures = compare_regression_reentry()
    assert without_fixtures.diagnostic is None
    assert with_fixtures.diagnostic is not None
    assert with_fixtures.diagnostic.preserves_prior_boundaries is True
    assert with_fixtures.diagnostic.module_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_regression_reentry()[1].status)
