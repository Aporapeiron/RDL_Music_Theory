"""update review診断とaccepted update record境界の最小検証。"""

from dataclasses import dataclass

from interval_module_update_review_boundary import (
    UpdateReviewObservation,
    compare_update_review,
)


@dataclass(frozen=True)
class UpdateAcceptanceController:
    name: str
    generated_by_review: bool


@dataclass(frozen=True)
class AcceptedUpdateRecordCandidate:
    label: str
    source_review_label: str
    accepted: bool
    document_mutated: bool


@dataclass(frozen=True)
class UpdateAcceptanceObservation:
    review_observation: UpdateReviewObservation
    acceptance_controller: UpdateAcceptanceController | None
    accepted_update: AcceptedUpdateRecordCandidate | None
    status: str


def review_observation() -> UpdateReviewObservation:
    return compare_update_review()[1]


def acceptance_controller_fixture() -> UpdateAcceptanceController:
    return UpdateAcceptanceController(
        name="interval_update_acceptance_controller_fixture",
        generated_by_review=False,
    )


def accept_update_record(
    review_obs: UpdateReviewObservation,
    controller: UpdateAcceptanceController | None,
) -> UpdateAcceptanceObservation:
    diagnostic = review_obs.review_diagnostic
    if diagnostic is None:
        return UpdateAcceptanceObservation(review_obs, controller, None, "no_review_diagnostic")
    if controller is None:
        return UpdateAcceptanceObservation(
            review_obs, None, None, "update_not_accepted_without_controller"
        )
    record = AcceptedUpdateRecordCandidate(
        label="accepted_interval_update_record_candidate",
        source_review_label=diagnostic.label,
        accepted=diagnostic.passes_review,
        document_mutated=False,
    )
    return UpdateAcceptanceObservation(
        review_obs, controller, record, "accepted_update_record_candidate_observed"
    )


def compare_update_acceptance() -> tuple[
    UpdateAcceptanceObservation, UpdateAcceptanceObservation
]:
    review = review_observation()
    return (
        accept_update_record(review, None),
        accept_update_record(review, acceptance_controller_fixture()),
    )


def run_checks() -> None:
    without_controller, with_controller = compare_update_acceptance()
    assert without_controller.status == "update_not_accepted_without_controller"
    assert with_controller.status == "accepted_update_record_candidate_observed"
    assert with_controller.accepted_update is not None
    assert with_controller.accepted_update.accepted is True
    assert with_controller.accepted_update.document_mutated is False
    assert with_controller.acceptance_controller is not None
    assert with_controller.acceptance_controller.generated_by_review is False


if __name__ == "__main__":
    run_checks()
    print(compare_update_acceptance()[1].status)
