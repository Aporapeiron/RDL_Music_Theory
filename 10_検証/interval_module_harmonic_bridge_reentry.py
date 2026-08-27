"""再入selected targetからharmonic bridge candidateへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_harmonic_bridge_boundary import (
    HarmonicBridgeCandidate,
    HarmonicBridgeInventory,
    IntervalHarmonicBridgeGamma,
    gamma_harmonic_bridge_fixture,
    harmonic_bridge_inventory_fixture,
)
from interval_module_target_selection_reentry import (
    TargetSelectionReentryObservation,
    ReenteredTargetSelectionObservation,
    compare_target_selection_reentry,
)


@dataclass(frozen=True)
class HarmonicBridgeReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_target_selection_reentry: bool


@dataclass(frozen=True)
class ReenteredHarmonicBridgeObservation:
    target_selection_observation: ReenteredTargetSelectionObservation
    harmonic_bridge_inventory: HarmonicBridgeInventory | None
    gamma_harmonic_bridge: IntervalHarmonicBridgeGamma | None
    harmonic_bridge: HarmonicBridgeCandidate | None
    harmonic_function_annotation_generated: bool
    target_generated: bool
    core_promoted: bool
    status: str
    bridge_reason: str | None


@dataclass(frozen=True)
class HarmonicBridgeReentryObservation:
    target_selection_reentry: TargetSelectionReentryObservation
    harmonic_bridge_reentry_gamma: HarmonicBridgeReentryGamma | None
    harmonic_bridge_observation: ReenteredHarmonicBridgeObservation | None
    same_selected_target: bool
    same_harmonic_bridge_inventory: bool
    harmonic_bridge_observed: bool
    harmonic_function_annotation_generated: bool
    target_generated: bool
    status: str


def target_selection_reentry_observation() -> TargetSelectionReentryObservation:
    return compare_target_selection_reentry()[1]


def harmonic_bridge_reentry_gamma_fixture() -> HarmonicBridgeReentryGamma:
    return HarmonicBridgeReentryGamma(
        name="Gamma_reentered_selected_target_to_harmonic_bridge_fixture",
        reads=("reentered_selected_target", "external_harmonic_bridge_inventory"),
        generated_by_target_selection_reentry=False,
    )


def observe_reentered_harmonic_bridge(
    target_selection: ReenteredTargetSelectionObservation,
    inventory: HarmonicBridgeInventory | None,
    gamma_harmonic_bridge: IntervalHarmonicBridgeGamma | None,
) -> ReenteredHarmonicBridgeObservation:
    if target_selection.selected_target is None:
        return ReenteredHarmonicBridgeObservation(
            target_selection,
            inventory,
            gamma_harmonic_bridge,
            None,
            False,
            False,
            False,
            "no_reentered_selected_interval_target",
            None,
        )
    if inventory is None:
        return ReenteredHarmonicBridgeObservation(
            target_selection,
            None,
            gamma_harmonic_bridge,
            None,
            False,
            False,
            False,
            "reentered_harmonic_bridge_not_observed_without_inventory",
            None,
        )
    if gamma_harmonic_bridge is None:
        return ReenteredHarmonicBridgeObservation(
            target_selection,
            inventory,
            None,
            None,
            False,
            False,
            False,
            "reentered_harmonic_bridge_not_observed_without_gamma",
            None,
        )

    matches = tuple(
        candidate
        for candidate in inventory.candidates
        if candidate.bridge_tag == gamma_harmonic_bridge.accepted_bridge_tag
    )
    if len(matches) != 1:
        return ReenteredHarmonicBridgeObservation(
            target_selection,
            inventory,
            gamma_harmonic_bridge,
            None,
            False,
            False,
            False,
            "reentered_harmonic_bridge_ambiguous_or_absent",
            None,
        )

    return ReenteredHarmonicBridgeObservation(
        target_selection_observation=target_selection,
        harmonic_bridge_inventory=inventory,
        gamma_harmonic_bridge=gamma_harmonic_bridge,
        harmonic_bridge=matches[0],
        harmonic_function_annotation_generated=False,
        target_generated=False,
        core_promoted=False,
        status="harmonic_bridge_candidate_observed_from_reentered_target_not_annotated",
        bridge_reason="reentered_selected_target_and_external_inventory_read_by_Gamma_interval_harmonic_bridge",
    )


def reenter_selected_target_to_harmonic_bridge(
    target_selection_reentry: TargetSelectionReentryObservation,
    reentry_gamma: HarmonicBridgeReentryGamma | None,
) -> HarmonicBridgeReentryObservation:
    target_selection = target_selection_reentry.target_selection_observation
    if target_selection is None or target_selection.selected_target is None:
        return HarmonicBridgeReentryObservation(
            target_selection_reentry,
            reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            False,
            "no_reentered_selected_interval_target",
        )
    if reentry_gamma is None:
        return HarmonicBridgeReentryObservation(
            target_selection_reentry,
            None,
            None,
            True,
            False,
            False,
            False,
            False,
            "reentered_selected_target_not_connected_to_harmonic_bridge_without_reentry_gamma",
        )

    inventory = harmonic_bridge_inventory_fixture()
    bridge_obs = observe_reentered_harmonic_bridge(
        target_selection, inventory, gamma_harmonic_bridge_fixture()
    )
    return HarmonicBridgeReentryObservation(
        target_selection_reentry=target_selection_reentry,
        harmonic_bridge_reentry_gamma=reentry_gamma,
        harmonic_bridge_observation=bridge_obs,
        same_selected_target=(
            bridge_obs.target_selection_observation.selected_target
            == target_selection.selected_target
        ),
        same_harmonic_bridge_inventory=bridge_obs.harmonic_bridge_inventory == inventory,
        harmonic_bridge_observed=bridge_obs.harmonic_bridge is not None,
        harmonic_function_annotation_generated=(
            bridge_obs.harmonic_function_annotation_generated
        ),
        target_generated=bridge_obs.target_generated,
        status="reentered_selected_target_connected_to_harmonic_bridge_not_annotation",
    )


def compare_harmonic_bridge_reentry() -> tuple[
    HarmonicBridgeReentryObservation,
    HarmonicBridgeReentryObservation,
]:
    selected = target_selection_reentry_observation()
    return (
        reenter_selected_target_to_harmonic_bridge(selected, None),
        reenter_selected_target_to_harmonic_bridge(
            selected, harmonic_bridge_reentry_gamma_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_harmonic_bridge_reentry()
    assert (
        without_gamma.status
        == "reentered_selected_target_not_connected_to_harmonic_bridge_without_reentry_gamma"
    )
    assert without_gamma.harmonic_bridge_observed is False
    assert (
        with_gamma.status
        == "reentered_selected_target_connected_to_harmonic_bridge_not_annotation"
    )
    assert with_gamma.same_selected_target is True
    assert with_gamma.same_harmonic_bridge_inventory is True
    assert with_gamma.harmonic_bridge_observed is True
    assert with_gamma.harmonic_function_annotation_generated is False
    assert with_gamma.target_generated is False
    assert with_gamma.harmonic_bridge_observation is not None
    assert with_gamma.harmonic_bridge_observation.harmonic_bridge is not None
    assert (
        with_gamma.harmonic_bridge_observation.harmonic_bridge.label
        == "tonic_support_bridge_candidate"
    )


if __name__ == "__main__":
    run_checks()
    print(compare_harmonic_bridge_reentry()[1].status)
