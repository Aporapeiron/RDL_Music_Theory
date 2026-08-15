"""Core adoption proposalとcompatibility診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_core_adoption_proposal_boundary import (
    CoreAdoptionProposalObservation,
    compare_core_adoption_proposal,
)


@dataclass(frozen=True)
class CoreCompatibilityCheck:
    name: str
    accepted_surface: str
    generated_by_proposal: bool


@dataclass(frozen=True)
class CoreCompatibilityDiagnostic:
    label: str
    source_proposal_label: str
    compatible: bool
    core_mutated: bool


@dataclass(frozen=True)
class CoreCompatibilityObservation:
    proposal_observation: CoreAdoptionProposalObservation
    compatibility_check: CoreCompatibilityCheck | None
    diagnostic: CoreCompatibilityDiagnostic | None
    status: str


def proposal_observation() -> CoreAdoptionProposalObservation:
    return compare_core_adoption_proposal()[1]


def compatibility_check_fixture() -> CoreCompatibilityCheck:
    return CoreCompatibilityCheck(
        name="core_compatibility_check_fixture",
        accepted_surface="module_state_record_surface",
        generated_by_proposal=False,
    )


def check_core_compatibility(
    proposal_obs: CoreAdoptionProposalObservation,
    check: CoreCompatibilityCheck | None,
) -> CoreCompatibilityObservation:
    proposal = proposal_obs.proposal
    if proposal is None:
        return CoreCompatibilityObservation(proposal_obs, check, None, "no_core_adoption_proposal")
    if check is None:
        return CoreCompatibilityObservation(
            proposal_obs, None, None, "core_compatibility_not_checked"
        )
    compatible = proposal.proposed_surface == check.accepted_surface
    diagnostic = CoreCompatibilityDiagnostic(
        label="interval_core_compatibility_diagnostic",
        source_proposal_label=proposal.label,
        compatible=compatible,
        core_mutated=False,
    )
    return CoreCompatibilityObservation(
        proposal_obs,
        check,
        diagnostic,
        "core_compatibility_diagnostic_observed",
    )


def compare_core_compatibility() -> tuple[
    CoreCompatibilityObservation, CoreCompatibilityObservation
]:
    proposal = proposal_observation()
    without_check = check_core_compatibility(proposal, None)
    with_check = check_core_compatibility(proposal, compatibility_check_fixture())
    return without_check, with_check


def run_checks() -> None:
    without_check, with_check = compare_core_compatibility()
    assert without_check.status == "core_compatibility_not_checked"
    assert with_check.status == "core_compatibility_diagnostic_observed"
    assert with_check.diagnostic is not None
    assert with_check.diagnostic.compatible is True
    assert with_check.diagnostic.core_mutated is False
    assert with_check.compatibility_check is not None
    assert with_check.compatibility_check.generated_by_proposal is False


if __name__ == "__main__":
    run_checks()
    print(compare_core_compatibility()[1])
