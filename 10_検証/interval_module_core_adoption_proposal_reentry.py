"""再入Core alignment候補からCore採用proposalへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_core_adoption_proposal_boundary import CoreAdoptionPolicy, CoreAdoptionProposal, adoption_policy_fixture
from interval_module_core_alignment_reentry import ReenteredCoreAlignmentObservation, compare_core_alignment_reentry


@dataclass(frozen=True)
class ReenteredCoreAdoptionProposalObservation:
    alignment_observation: ReenteredCoreAlignmentObservation
    adoption_policy: CoreAdoptionPolicy | None
    proposal: CoreAdoptionProposal | None
    status: str


def propose_reentered_core_adoption(
    alignment: ReenteredCoreAlignmentObservation,
    policy: CoreAdoptionPolicy | None,
) -> ReenteredCoreAdoptionProposalObservation:
    candidate = alignment.alignment_candidate
    if candidate is None:
        return ReenteredCoreAdoptionProposalObservation(alignment, policy, None, "no_reentered_core_alignment_candidate")
    if policy is None:
        return ReenteredCoreAdoptionProposalObservation(alignment, None, None, "reentered_core_adoption_not_proposed_without_policy")
    proposal = CoreAdoptionProposal("interval_core_adoption_proposal_candidate", candidate.label, candidate.target_core_surface, False)
    return ReenteredCoreAdoptionProposalObservation(alignment, policy, proposal, "core_adoption_proposal_observed_from_reentered_alignment_not_core_mutation")


def compare_core_adoption_proposal_reentry() -> tuple[ReenteredCoreAdoptionProposalObservation, ReenteredCoreAdoptionProposalObservation]:
    alignment = compare_core_alignment_reentry()[1]
    return (
        propose_reentered_core_adoption(alignment, None),
        propose_reentered_core_adoption(alignment, adoption_policy_fixture()),
    )


def run_checks() -> None:
    without_policy, with_policy = compare_core_adoption_proposal_reentry()
    assert without_policy.proposal is None
    assert with_policy.proposal is not None
    assert with_policy.proposal.core_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_core_adoption_proposal_reentry()[1].status)
