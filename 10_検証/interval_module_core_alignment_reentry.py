"""再入confirmed M_B候補からCore整合候補へ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_confirmed_mb_reentry import (
    ReenteredConfirmedMBObservation,
    compare_confirmed_mb_reentry,
)
from interval_module_core_alignment_boundary import (
    CoreAlignmentCandidate,
    CoreAlignmentGamma,
    CoreSurfaceInventory,
    core_inventory_fixture,
    gamma_core_alignment_fixture,
)


@dataclass(frozen=True)
class ReenteredCoreAlignmentObservation:
    confirmed_mb_observation: ReenteredConfirmedMBObservation
    core_inventory: CoreSurfaceInventory | None
    gamma_alignment: CoreAlignmentGamma | None
    alignment_candidate: CoreAlignmentCandidate | None
    status: str


def align_reentered_to_core_surface(
    confirmed_obs: ReenteredConfirmedMBObservation,
    inventory: CoreSurfaceInventory | None,
    gamma: CoreAlignmentGamma | None,
) -> ReenteredCoreAlignmentObservation:
    confirmed = confirmed_obs.confirmed_candidate
    if confirmed is None:
        return ReenteredCoreAlignmentObservation(confirmed_obs, inventory, gamma, None, "no_reentered_confirmed_M_B_candidate")
    if inventory is None:
        return ReenteredCoreAlignmentObservation(confirmed_obs, None, gamma, None, "reentered_core_alignment_not_checked_without_inventory")
    if gamma is None:
        return ReenteredCoreAlignmentObservation(confirmed_obs, inventory, None, None, "reentered_core_alignment_not_checked_without_gamma")
    candidate = CoreAlignmentCandidate(
        "interval_core_alignment_candidate",
        confirmed.label,
        inventory.target_core_surface,
        False,
    )
    return ReenteredCoreAlignmentObservation(confirmed_obs, inventory, gamma, candidate, "core_alignment_candidate_observed_from_reentered_confirmed_M_B_not_adopted")


def compare_core_alignment_reentry() -> tuple[ReenteredCoreAlignmentObservation, ReenteredCoreAlignmentObservation]:
    confirmed = compare_confirmed_mb_reentry()[1]
    inventory = core_inventory_fixture()
    return (
        align_reentered_to_core_surface(confirmed, inventory, None),
        align_reentered_to_core_surface(confirmed, inventory, gamma_core_alignment_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_core_alignment_reentry()
    assert without_gamma.alignment_candidate is None
    assert with_gamma.alignment_candidate is not None
    assert with_gamma.alignment_candidate.core_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_core_alignment_reentry()[1].status)
