"""再入integration候補とdocument update proposal境界の最小検証。"""

from dataclasses import dataclass

from interval_module_document_update_proposal_boundary import DocumentTargetBoundary, DocumentUpdateProposal, document_target_fixture
from interval_module_integration_candidate_reentry import ReenteredIntegrationObservation, compare_integration_candidate_reentry


@dataclass(frozen=True)
class ReenteredDocumentUpdateProposalObservation:
    integration_observation: ReenteredIntegrationObservation
    document_target: DocumentTargetBoundary | None
    update_proposal: DocumentUpdateProposal | None
    status: str


def propose_reentered_document_update(integration_obs: ReenteredIntegrationObservation, target: DocumentTargetBoundary | None) -> ReenteredDocumentUpdateProposalObservation:
    integration = integration_obs.integration_candidate
    if integration is None:
        return ReenteredDocumentUpdateProposalObservation(integration_obs, target, None, "no_reentered_integration_candidate")
    if target is None:
        return ReenteredDocumentUpdateProposalObservation(integration_obs, None, None, "reentered_document_update_not_proposed_without_target")
    proposal = DocumentUpdateProposal("interval_structure_map_update_proposal_candidate", integration.label, target.target_document, False)
    return ReenteredDocumentUpdateProposalObservation(integration_obs, target, proposal, "document_update_proposal_observed_from_reentered_integration_not_document_mutation")


def compare_document_update_proposal_reentry() -> tuple[ReenteredDocumentUpdateProposalObservation, ReenteredDocumentUpdateProposalObservation]:
    integration = compare_integration_candidate_reentry()[1]
    return propose_reentered_document_update(integration, None), propose_reentered_document_update(integration, document_target_fixture())


def run_checks() -> None:
    without_target, with_target = compare_document_update_proposal_reentry()
    assert without_target.update_proposal is None
    assert with_target.update_proposal is not None
    assert with_target.update_proposal.document_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_document_update_proposal_reentry()[1].status)
