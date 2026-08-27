"""再入verification run観測とresult classification境界の最小検証。"""

from dataclasses import dataclass

from interval_module_execution_run_reentry import ReenteredVerificationRunObservation, compare_verification_run_reentry
from interval_module_result_classification_boundary import ResultClassifierGamma, VerificationResultCandidate, result_classifier_gamma_fixture


@dataclass(frozen=True)
class ReenteredResultClassificationObservation:
    run_observation: ReenteredVerificationRunObservation
    classifier_gamma: ResultClassifierGamma | None
    result_candidate: VerificationResultCandidate | None
    status: str


def classify_reentered_result(run_obs: ReenteredVerificationRunObservation, classifier: ResultClassifierGamma | None) -> ReenteredResultClassificationObservation:
    run = run_obs.run_observation
    if run is None:
        return ReenteredResultClassificationObservation(run_obs, classifier, None, "no_reentered_run_observation")
    if classifier is None:
        return ReenteredResultClassificationObservation(run_obs, None, None, "reentered_result_not_classified_without_gamma")
    result = VerificationResultCandidate("interval_verification_result_candidate", run.label, "boundary_preserved_fixture", False)
    return ReenteredResultClassificationObservation(run_obs, classifier, result, "verification_result_observed_from_reentered_run_not_diagnosed")


def compare_result_classification_reentry() -> tuple[ReenteredResultClassificationObservation, ReenteredResultClassificationObservation]:
    run = compare_verification_run_reentry()[1]
    return classify_reentered_result(run, None), classify_reentered_result(run, result_classifier_gamma_fixture())


def run_checks() -> None:
    without_gamma, with_gamma = compare_result_classification_reentry()
    assert without_gamma.result_candidate is None
    assert with_gamma.result_candidate is not None
    assert with_gamma.result_candidate.break_diagnostic_generated is False


if __name__ == "__main__":
    run_checks()
    print(compare_result_classification_reentry()[1].status)
