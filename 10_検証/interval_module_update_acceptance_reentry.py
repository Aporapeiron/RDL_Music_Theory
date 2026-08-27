"""再入update review診断とaccepted update record境界の最小検証。"""

from dataclasses import dataclass

from interval_module_update_acceptance_boundary import AcceptedUpdateRecordCandidate, UpdateAcceptanceController, acceptance_controller_fixture
from interval_module_update_review_reentry import ReenteredUpdateReviewObservation, compare_update_review_reentry


@dataclass(frozen=True)
class ReenteredUpdateAcceptanceObservation:
    review_observation: ReenteredUpdateReviewObservation
    acceptance_controller: UpdateAcceptanceController | None
    accepted_update: AcceptedUpdateRecordCandidate | None
    status: str


def accept_reentered_update_record(review_obs: ReenteredUpdateReviewObservation, controller: UpdateAcceptanceController | None) -> ReenteredUpdateAcceptanceObservation:
    diagnostic = review_obs.review_diagnostic
    if diagnostic is None:
        return ReenteredUpdateAcceptanceObservation(review_obs, controller, None, "no_reentered_review_diagnostic")
    if controller is None:
        return ReenteredUpdateAcceptanceObservation(review_obs, None, None, "reentered_update_not_accepted_without_controller")
    record = AcceptedUpdateRecordCandidate("accepted_interval_update_record_candidate", diagnostic.label, diagnostic.passes_review, False)
    return ReenteredUpdateAcceptanceObservation(review_obs, controller, record, "accepted_update_record_observed_from_reentered_review")


def compare_update_acceptance_reentry() -> tuple[ReenteredUpdateAcceptanceObservation, ReenteredUpdateAcceptanceObservation]:
    review = compare_update_review_reentry()[1]
    return accept_reentered_update_record(review, None), accept_reentered_update_record(review, acceptance_controller_fixture())


def run_checks() -> None:
    without_controller, with_controller = compare_update_acceptance_reentry()
    assert without_controller.accepted_update is None
    assert with_controller.accepted_update is not None
    assert with_controller.accepted_update.accepted is True
    assert with_controller.accepted_update.document_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_update_acceptance_reentry()[1].status)
