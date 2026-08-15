"""document update proposalとreview診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_document_update_proposal_boundary import (
    DocumentUpdateProposalObservation,
    compare_document_update_proposal,
)


@dataclass(frozen=True)
class UpdateReviewChecklist:
    name: str
    checks_boundary_separation: bool
    generated_by_proposal: bool


@dataclass(frozen=True)
class UpdateReviewDiagnostic:
    label: str
    source_proposal_label: str
    passes_review: bool
    document_mutated: bool


@dataclass(frozen=True)
class UpdateReviewObservation:
    proposal_observation: DocumentUpdateProposalObservation
    review_checklist: UpdateReviewChecklist | None
    review_diagnostic: UpdateReviewDiagnostic | None
    status: str


def proposal_observation() -> DocumentUpdateProposalObservation:
    return compare_document_update_proposal()[1]


def review_checklist_fixture() -> UpdateReviewChecklist:
    return UpdateReviewChecklist(
        name="interval_update_review_checklist_fixture",
        checks_boundary_separation=True,
        generated_by_proposal=False,
    )


def review_update_proposal(
    proposal_obs: DocumentUpdateProposalObservation,
    checklist: UpdateReviewChecklist | None,
) -> UpdateReviewObservation:
    proposal = proposal_obs.update_proposal
    if proposal is None:
        return UpdateReviewObservation(proposal_obs, checklist, None, "no_update_proposal")
    if checklist is None:
        return UpdateReviewObservation(
            proposal_obs, None, None, "update_review_not_checked"
        )
    diagnostic = UpdateReviewDiagnostic(
        label="interval_update_review_diagnostic",
        source_proposal_label=proposal.label,
        passes_review=checklist.checks_boundary_separation,
        document_mutated=False,
    )
    return UpdateReviewObservation(
        proposal_obs, checklist, diagnostic, "update_review_diagnostic_observed"
    )


def compare_update_review() -> tuple[UpdateReviewObservation, UpdateReviewObservation]:
    proposal = proposal_observation()
    return (
        review_update_proposal(proposal, None),
        review_update_proposal(proposal, review_checklist_fixture()),
    )


def run_checks() -> None:
    without_checklist, with_checklist = compare_update_review()
    assert without_checklist.status == "update_review_not_checked"
    assert with_checklist.status == "update_review_diagnostic_observed"
    assert with_checklist.review_diagnostic is not None
    assert with_checklist.review_diagnostic.passes_review is True
    assert with_checklist.review_diagnostic.document_mutated is False
    assert with_checklist.review_checklist is not None
    assert with_checklist.review_checklist.generated_by_proposal is False


if __name__ == "__main__":
    run_checks()
    print(compare_update_review()[1].status)
