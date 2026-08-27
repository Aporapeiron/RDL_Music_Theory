"""再入Core adoption proposalとcompatibility診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_core_adoption_proposal_reentry import ReenteredCoreAdoptionProposalObservation, compare_core_adoption_proposal_reentry
from interval_module_core_compatibility_boundary import CoreCompatibilityCheck, CoreCompatibilityDiagnostic, compatibility_check_fixture


@dataclass(frozen=True)
class ReenteredCoreCompatibilityObservation:
    proposal_observation: ReenteredCoreAdoptionProposalObservation
    compatibility_check: CoreCompatibilityCheck | None
    diagnostic: CoreCompatibilityDiagnostic | None
    status: str


def check_reentered_core_compatibility(
    proposal_obs: ReenteredCoreAdoptionProposalObservation,
    check: CoreCompatibilityCheck | None,
) -> ReenteredCoreCompatibilityObservation:
    proposal = proposal_obs.proposal
    if proposal is None:
        return ReenteredCoreCompatibilityObservation(proposal_obs, check, None, "no_reentered_core_adoption_proposal")
    if check is None:
        return ReenteredCoreCompatibilityObservation(proposal_obs, None, None, "reentered_core_compatibility_not_checked")
    diagnostic = CoreCompatibilityDiagnostic(
        "interval_core_compatibility_diagnostic",
        proposal.label,
        proposal.proposed_surface == check.accepted_surface,
        False,
    )
    return ReenteredCoreCompatibilityObservation(proposal_obs, check, diagnostic, "core_compatibility_diagnostic_observed_from_reentered_proposal")


def compare_core_compatibility_reentry() -> tuple[ReenteredCoreCompatibilityObservation, ReenteredCoreCompatibilityObservation]:
    proposal = compare_core_adoption_proposal_reentry()[1]
    return (
        check_reentered_core_compatibility(proposal, None),
        check_reentered_core_compatibility(proposal, compatibility_check_fixture()),
    )


def run_checks() -> None:
    without_check, with_check = compare_core_compatibility_reentry()
    assert without_check.diagnostic is None
    assert with_check.diagnostic is not None
    assert with_check.diagnostic.compatible is True
    assert with_check.diagnostic.core_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_core_compatibility_reentry()[1].status)
