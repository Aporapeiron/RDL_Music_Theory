"""再入document update proposalとreview診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_document_update_proposal_reentry import ReenteredDocumentUpdateProposalObservation, compare_document_update_proposal_reentry
from interval_module_update_review_boundary import UpdateReviewChecklist, UpdateReviewDiagnostic, review_checklist_fixture


@dataclass(frozen=True)
class ReenteredUpdateReviewObservation:
    proposal_observation: ReenteredDocumentUpdateProposalObservation
    review_checklist: UpdateReviewChecklist | None
    review_diagnostic: UpdateReviewDiagnostic | None
    status: str


def review_reentered_update_proposal(proposal_obs: ReenteredDocumentUpdateProposalObservation, checklist: UpdateReviewChecklist | None) -> ReenteredUpdateReviewObservation:
    proposal = proposal_obs.update_proposal
    if proposal is None:
        return ReenteredUpdateReviewObservation(proposal_obs, checklist, None, "no_reentered_update_proposal")
    if checklist is None:
        return ReenteredUpdateReviewObservation(proposal_obs, None, None, "reentered_update_review_not_checked")
    diagnostic = UpdateReviewDiagnostic("interval_update_review_diagnostic", proposal.label, checklist.checks_boundary_separation, False)
    return ReenteredUpdateReviewObservation(proposal_obs, checklist, diagnostic, "update_review_diagnostic_observed_from_reentered_proposal")


def compare_update_review_reentry() -> tuple[ReenteredUpdateReviewObservation, ReenteredUpdateReviewObservation]:
    proposal = compare_document_update_proposal_reentry()[1]
    return review_reentered_update_proposal(proposal, None), review_reentered_update_proposal(proposal, review_checklist_fixture())


def run_checks() -> None:
    without_checklist, with_checklist = compare_update_review_reentry()
    assert without_checklist.review_diagnostic is None
    assert with_checklist.review_diagnostic is not None
    assert with_checklist.review_diagnostic.passes_review is True
    assert with_checklist.review_diagnostic.document_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_update_review_reentry()[1].status)
