"""Core alignment候補とCore採用proposal境界の最小検証。"""

from dataclasses import dataclass

from interval_module_core_alignment_boundary import (
    CoreAlignmentObservation,
    compare_core_alignment,
)


@dataclass(frozen=True)
class CoreAdoptionPolicy:
    name: str
    reads: tuple[str, str]
    generated_by_alignment: bool


@dataclass(frozen=True)
class CoreAdoptionProposal:
    label: str
    source_alignment_label: str
    proposed_surface: str
    core_mutated: bool


@dataclass(frozen=True)
class CoreAdoptionProposalObservation:
    alignment_observation: CoreAlignmentObservation
    adoption_policy: CoreAdoptionPolicy | None
    proposal: CoreAdoptionProposal | None
    status: str


def alignment_observation() -> CoreAlignmentObservation:
    return compare_core_alignment()[1]


def adoption_policy_fixture() -> CoreAdoptionPolicy:
    return CoreAdoptionPolicy(
        name="Gamma_core_adoption_proposal_fixture",
        reads=("core_alignment_candidate", "external_adoption_policy"),
        generated_by_alignment=False,
    )


def propose_core_adoption(
    alignment: CoreAlignmentObservation,
    policy: CoreAdoptionPolicy | None,
) -> CoreAdoptionProposalObservation:
    candidate = alignment.alignment_candidate
    if candidate is None:
        return CoreAdoptionProposalObservation(alignment, policy, None, "no_core_alignment_candidate")
    if policy is None:
        return CoreAdoptionProposalObservation(
            alignment, None, None, "core_adoption_not_proposed_without_policy"
        )
    proposal = CoreAdoptionProposal(
        label="interval_core_adoption_proposal_candidate",
        source_alignment_label=candidate.label,
        proposed_surface=candidate.target_core_surface,
        core_mutated=False,
    )
    return CoreAdoptionProposalObservation(
        alignment,
        policy,
        proposal,
        "core_adoption_proposal_observed_not_core_mutation",
    )


def compare_core_adoption_proposal() -> tuple[
    CoreAdoptionProposalObservation, CoreAdoptionProposalObservation
]:
    alignment = alignment_observation()
    without_policy = propose_core_adoption(alignment, None)
    with_policy = propose_core_adoption(alignment, adoption_policy_fixture())
    return without_policy, with_policy


def run_checks() -> None:
    without_policy, with_policy = compare_core_adoption_proposal()
    assert without_policy.status == "core_adoption_not_proposed_without_policy"
    assert with_policy.status == "core_adoption_proposal_observed_not_core_mutation"
    assert with_policy.proposal is not None
    assert with_policy.proposal.core_mutated is False
    assert with_policy.adoption_policy is not None
    assert with_policy.adoption_policy.generated_by_alignment is False


if __name__ == "__main__":
    run_checks()
    print(compare_core_adoption_proposal()[1])
