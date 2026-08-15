"""verification run観測とresult classification境界の最小検証。"""

from dataclasses import dataclass

from interval_module_execution_run_boundary import (
    VerificationRunBoundaryObservation,
    compare_verification_run,
)


@dataclass(frozen=True)
class ResultClassifierGamma:
    name: str
    generated_by_run: bool


@dataclass(frozen=True)
class VerificationResultCandidate:
    label: str
    source_run_label: str
    result_kind: str
    break_diagnostic_generated: bool


@dataclass(frozen=True)
class ResultClassificationObservation:
    run_observation: VerificationRunBoundaryObservation
    classifier_gamma: ResultClassifierGamma | None
    result_candidate: VerificationResultCandidate | None
    status: str


def run_observation() -> VerificationRunBoundaryObservation:
    return compare_verification_run()[1]


def result_classifier_gamma_fixture() -> ResultClassifierGamma:
    return ResultClassifierGamma(
        name="Gamma_interval_result_classifier_fixture",
        generated_by_run=False,
    )


def classify_result(
    run_obs: VerificationRunBoundaryObservation,
    classifier: ResultClassifierGamma | None,
) -> ResultClassificationObservation:
    run = run_obs.run_observation
    if run is None:
        return ResultClassificationObservation(run_obs, classifier, None, "no_run_observation")
    if classifier is None:
        return ResultClassificationObservation(
            run_obs, None, None, "result_not_classified_without_gamma"
        )
    result = VerificationResultCandidate(
        label="interval_verification_result_candidate",
        source_run_label=run.label,
        result_kind="boundary_preserved_fixture",
        break_diagnostic_generated=False,
    )
    return ResultClassificationObservation(
        run_obs, classifier, result, "verification_result_candidate_observed_not_diagnosed"
    )


def compare_result_classification() -> tuple[
    ResultClassificationObservation, ResultClassificationObservation
]:
    run = run_observation()
    return (
        classify_result(run, None),
        classify_result(run, result_classifier_gamma_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_result_classification()
    assert without_gamma.status == "result_not_classified_without_gamma"
    assert with_gamma.status == "verification_result_candidate_observed_not_diagnosed"
    assert with_gamma.result_candidate is not None
    assert with_gamma.result_candidate.break_diagnostic_generated is False
    assert with_gamma.classifier_gamma is not None
    assert with_gamma.classifier_gamma.generated_by_run is False


if __name__ == "__main__":
    run_checks()
    print(compare_result_classification()[1].status)
