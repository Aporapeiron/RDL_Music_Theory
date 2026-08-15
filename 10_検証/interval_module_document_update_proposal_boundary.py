"""integration候補とdocument update proposal境界の最小検証。"""

from dataclasses import dataclass

from interval_module_integration_candidate_boundary import (
    IntegrationObservation,
    compare_integration_candidate,
)


@dataclass(frozen=True)
class DocumentTargetBoundary:
    name: str
    target_document: str
    generated_by_integration: bool


@dataclass(frozen=True)
class DocumentUpdateProposal:
    label: str
    source_integration_label: str
    target_document: str
    document_mutated: bool


@dataclass(frozen=True)
class DocumentUpdateProposalObservation:
    integration_observation: IntegrationObservation
    document_target: DocumentTargetBoundary | None
    update_proposal: DocumentUpdateProposal | None
    status: str


def integration_observation() -> IntegrationObservation:
    return compare_integration_candidate()[1]


def document_target_fixture() -> DocumentTargetBoundary:
    return DocumentTargetBoundary(
        name="interval_document_target_boundary_fixture",
        target_document="20_構造抽出/音程Module構造地図.md",
        generated_by_integration=False,
    )


def propose_document_update(
    integration_obs: IntegrationObservation,
    target: DocumentTargetBoundary | None,
) -> DocumentUpdateProposalObservation:
    integration = integration_obs.integration_candidate
    if integration is None:
        return DocumentUpdateProposalObservation(integration_obs, target, None, "no_integration_candidate")
    if target is None:
        return DocumentUpdateProposalObservation(
            integration_obs, None, None, "document_update_not_proposed_without_target"
        )
    proposal = DocumentUpdateProposal(
        label="interval_structure_map_update_proposal_candidate",
        source_integration_label=integration.label,
        target_document=target.target_document,
        document_mutated=False,
    )
    return DocumentUpdateProposalObservation(
        integration_obs,
        target,
        proposal,
        "document_update_proposal_observed_not_document_mutation",
    )


def compare_document_update_proposal() -> tuple[
    DocumentUpdateProposalObservation, DocumentUpdateProposalObservation
]:
    integration = integration_observation()
    return (
        propose_document_update(integration, None),
        propose_document_update(integration, document_target_fixture()),
    )


def run_checks() -> None:
    without_target, with_target = compare_document_update_proposal()
    assert without_target.status == "document_update_not_proposed_without_target"
    assert with_target.status == "document_update_proposal_observed_not_document_mutation"
    assert with_target.update_proposal is not None
    assert with_target.update_proposal.document_mutated is False
    assert with_target.document_target is not None
    assert with_target.document_target.generated_by_integration is False


if __name__ == "__main__":
    run_checks()
    print(compare_document_update_proposal()[1].status)
