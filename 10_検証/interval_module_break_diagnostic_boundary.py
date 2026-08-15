"""verification result候補と構造破断診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_result_classification_boundary import (
    ResultClassificationObservation,
    compare_result_classification,
)


@dataclass(frozen=True)
class BreakDiagnosticGamma:
    name: str
    generated_by_result: bool


@dataclass(frozen=True)
class StructuralBreakDiagnosticCandidate:
    label: str
    source_result_label: str
    break_detected: bool
    integration_generated: bool


@dataclass(frozen=True)
class BreakDiagnosticObservation:
    result_observation: ResultClassificationObservation
    break_gamma: BreakDiagnosticGamma | None
    break_diagnostic: StructuralBreakDiagnosticCandidate | None
    status: str


def result_observation() -> ResultClassificationObservation:
    return compare_result_classification()[1]


def break_gamma_fixture() -> BreakDiagnosticGamma:
    return BreakDiagnosticGamma(
        name="Gamma_interval_structural_break_diagnostic_fixture",
        generated_by_result=False,
    )


def diagnose_structural_break(
    result_obs: ResultClassificationObservation,
    gamma: BreakDiagnosticGamma | None,
) -> BreakDiagnosticObservation:
    result = result_obs.result_candidate
    if result is None:
        return BreakDiagnosticObservation(result_obs, gamma, None, "no_result_candidate")
    if gamma is None:
        return BreakDiagnosticObservation(
            result_obs, None, None, "break_diagnostic_not_created_without_gamma"
        )
    diagnostic = StructuralBreakDiagnosticCandidate(
        label="interval_structural_break_diagnostic_candidate",
        source_result_label=result.label,
        break_detected=False,
        integration_generated=False,
    )
    return BreakDiagnosticObservation(
        result_obs, gamma, diagnostic, "break_diagnostic_candidate_observed_not_integrated"
    )


def compare_break_diagnostic() -> tuple[BreakDiagnosticObservation, BreakDiagnosticObservation]:
    result = result_observation()
    return (
        diagnose_structural_break(result, None),
        diagnose_structural_break(result, break_gamma_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_break_diagnostic()
    assert without_gamma.status == "break_diagnostic_not_created_without_gamma"
    assert with_gamma.status == "break_diagnostic_candidate_observed_not_integrated"
    assert with_gamma.break_diagnostic is not None
    assert with_gamma.break_diagnostic.break_detected is False
    assert with_gamma.break_diagnostic.integration_generated is False
    assert with_gamma.break_gamma is not None
    assert with_gamma.break_gamma.generated_by_result is False


if __name__ == "__main__":
    run_checks()
    print(compare_break_diagnostic()[1].status)
