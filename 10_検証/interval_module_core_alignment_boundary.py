"""confirmed M_B候補とCore整合候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_confirmed_mb_boundary import (
    ConfirmedMBObservation,
    compare_confirmed_mb_boundary,
)


@dataclass(frozen=True)
class CoreSurfaceInventory:
    name: str
    target_core_surface: str
    generated_by_confirmed_mb: bool


@dataclass(frozen=True)
class CoreAlignmentGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class CoreAlignmentCandidate:
    label: str
    source_confirmed_mb_label: str
    target_core_surface: str
    core_mutated: bool


@dataclass(frozen=True)
class CoreAlignmentObservation:
    confirmed_mb_observation: ConfirmedMBObservation
    core_inventory: CoreSurfaceInventory | None
    gamma_alignment: CoreAlignmentGamma | None
    alignment_candidate: CoreAlignmentCandidate | None
    status: str


def confirmed_mb_observation() -> ConfirmedMBObservation:
    return compare_confirmed_mb_boundary()[1]


def core_inventory_fixture() -> CoreSurfaceInventory:
    return CoreSurfaceInventory(
        name="interval_core_surface_inventory_fixture",
        target_core_surface="module_state_record_surface",
        generated_by_confirmed_mb=False,
    )


def gamma_core_alignment_fixture() -> CoreAlignmentGamma:
    return CoreAlignmentGamma(
        name="Gamma_interval_core_alignment_fixture",
        reads=("confirmed_M_B_interval_candidate", "external_core_surface_inventory"),
        rule_scope="fixture_limited_alignment_not_adoption",
    )


def align_to_core_surface(
    confirmed_obs: ConfirmedMBObservation,
    inventory: CoreSurfaceInventory | None,
    gamma_alignment: CoreAlignmentGamma | None,
) -> CoreAlignmentObservation:
    confirmed = confirmed_obs.confirmed_candidate
    if confirmed is None:
        return CoreAlignmentObservation(confirmed_obs, inventory, gamma_alignment, None, "no_confirmed_M_B_candidate")
    if inventory is None:
        return CoreAlignmentObservation(confirmed_obs, None, gamma_alignment, None, "core_alignment_not_checked_without_inventory")
    if gamma_alignment is None:
        return CoreAlignmentObservation(confirmed_obs, inventory, None, None, "core_alignment_not_checked_without_gamma")
    candidate = CoreAlignmentCandidate(
        label="interval_core_alignment_candidate",
        source_confirmed_mb_label=confirmed.label,
        target_core_surface=inventory.target_core_surface,
        core_mutated=False,
    )
    return CoreAlignmentObservation(
        confirmed_obs,
        inventory,
        gamma_alignment,
        candidate,
        "core_alignment_candidate_observed_not_adopted",
    )


def compare_core_alignment() -> tuple[CoreAlignmentObservation, CoreAlignmentObservation]:
    confirmed = confirmed_mb_observation()
    inventory = core_inventory_fixture()
    without_gamma = align_to_core_surface(confirmed, inventory, None)
    with_gamma = align_to_core_surface(confirmed, inventory, gamma_core_alignment_fixture())
    return without_gamma, with_gamma


def run_checks() -> None:
    without_gamma, with_gamma = compare_core_alignment()
    assert without_gamma.status == "core_alignment_not_checked_without_gamma"
    assert with_gamma.status == "core_alignment_candidate_observed_not_adopted"
    assert with_gamma.alignment_candidate is not None
    assert with_gamma.alignment_candidate.core_mutated is False
    assert with_gamma.core_inventory is not None
    assert with_gamma.core_inventory.generated_by_confirmed_mb is False


if __name__ == "__main__":
    run_checks()
    print(compare_core_alignment()[1])
