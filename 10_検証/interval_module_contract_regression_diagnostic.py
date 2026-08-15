"""Module contract update候補とregression診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_contract_update_boundary import (
    ModuleContractUpdateObservation,
    compare_contract_update_boundary,
)


@dataclass(frozen=True)
class RegressionFixtureSet:
    name: str
    covers_prior_boundaries: tuple[str, ...]
    generated_by_update_candidate: bool


@dataclass(frozen=True)
class RegressionDiagnostic:
    label: str
    source_update_candidate_label: str
    preserves_prior_boundaries: bool
    module_mutated: bool


@dataclass(frozen=True)
class RegressionDiagnosticObservation:
    update_observation: ModuleContractUpdateObservation
    regression_fixtures: RegressionFixtureSet | None
    diagnostic: RegressionDiagnostic | None
    status: str


def update_observation() -> ModuleContractUpdateObservation:
    return compare_contract_update_boundary()[1]


def regression_fixture_set() -> RegressionFixtureSet:
    return RegressionFixtureSet(
        name="interval_contract_regression_fixture_set",
        covers_prior_boundaries=("69-85", "86-97"),
        generated_by_update_candidate=False,
    )


def diagnose_regression(
    update_obs: ModuleContractUpdateObservation,
    fixtures: RegressionFixtureSet | None,
) -> RegressionDiagnosticObservation:
    update = update_obs.update_candidate
    if update is None:
        return RegressionDiagnosticObservation(update_obs, fixtures, None, "no_contract_update_candidate")
    if fixtures is None:
        return RegressionDiagnosticObservation(
            update_obs, None, None, "regression_not_checked_without_fixtures"
        )
    diagnostic = RegressionDiagnostic(
        label="interval_contract_regression_diagnostic",
        source_update_candidate_label=update.label,
        preserves_prior_boundaries=True,
        module_mutated=False,
    )
    return RegressionDiagnosticObservation(
        update_obs,
        fixtures,
        diagnostic,
        "regression_diagnostic_observed_not_module_mutation",
    )


def compare_regression_diagnostic() -> tuple[
    RegressionDiagnosticObservation, RegressionDiagnosticObservation
]:
    update = update_observation()
    without_fixtures = diagnose_regression(update, None)
    with_fixtures = diagnose_regression(update, regression_fixture_set())
    return without_fixtures, with_fixtures


def run_checks() -> None:
    without_fixtures, with_fixtures = compare_regression_diagnostic()
    assert without_fixtures.status == "regression_not_checked_without_fixtures"
    assert with_fixtures.status == "regression_diagnostic_observed_not_module_mutation"
    assert with_fixtures.diagnostic is not None
    assert with_fixtures.diagnostic.preserves_prior_boundaries is True
    assert with_fixtures.diagnostic.module_mutated is False
    assert with_fixtures.regression_fixtures is not None
    assert with_fixtures.regression_fixtures.generated_by_update_candidate is False


if __name__ == "__main__":
    run_checks()
    print(compare_regression_diagnostic()[1])
