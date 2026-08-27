"""再入verification result候補と構造破断診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_break_diagnostic_boundary import BreakDiagnosticGamma, StructuralBreakDiagnosticCandidate, break_gamma_fixture
from interval_module_result_classification_reentry import ReenteredResultClassificationObservation, compare_result_classification_reentry


@dataclass(frozen=True)
class ReenteredBreakDiagnosticObservation:
    result_observation: ReenteredResultClassificationObservation
    break_gamma: BreakDiagnosticGamma | None
    break_diagnostic: StructuralBreakDiagnosticCandidate | None
    status: str


def diagnose_reentered_structural_break(result_obs: ReenteredResultClassificationObservation, gamma: BreakDiagnosticGamma | None) -> ReenteredBreakDiagnosticObservation:
    result = result_obs.result_candidate
    if result is None:
        return ReenteredBreakDiagnosticObservation(result_obs, gamma, None, "no_reentered_result_candidate")
    if gamma is None:
        return ReenteredBreakDiagnosticObservation(result_obs, None, None, "reentered_break_diagnostic_not_created_without_gamma")
    diagnostic = StructuralBreakDiagnosticCandidate("interval_structural_break_diagnostic_candidate", result.label, False, False)
    return ReenteredBreakDiagnosticObservation(result_obs, gamma, diagnostic, "break_diagnostic_observed_from_reentered_result_not_integrated")


def compare_break_diagnostic_reentry() -> tuple[ReenteredBreakDiagnosticObservation, ReenteredBreakDiagnosticObservation]:
    result = compare_result_classification_reentry()[1]
    return diagnose_reentered_structural_break(result, None), diagnose_reentered_structural_break(result, break_gamma_fixture())


def run_checks() -> None:
    without_gamma, with_gamma = compare_break_diagnostic_reentry()
    assert without_gamma.break_diagnostic is None
    assert with_gamma.break_diagnostic is not None
    assert with_gamma.break_diagnostic.break_detected is False
    assert with_gamma.break_diagnostic.integration_generated is False


if __name__ == "__main__":
    run_checks()
    print(compare_break_diagnostic_reentry()[1].status)
