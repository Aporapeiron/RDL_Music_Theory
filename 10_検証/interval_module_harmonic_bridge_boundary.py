"""音程Module selected targetと和声機能bridge境界の最小検証。"""

from dataclasses import dataclass

from interval_module_target_selection_boundary import (
    IntervalTargetSelectionObservation,
    compare_interval_target_selection,
)


@dataclass(frozen=True)
class HarmonicBridgeCandidate:
    label: str
    source: str
    bridge_tag: str
    generated_by_selected_target: bool


@dataclass(frozen=True)
class HarmonicBridgeInventory:
    name: str
    candidates: tuple[HarmonicBridgeCandidate, ...]
    generated_by_selected_target: bool


@dataclass(frozen=True)
class IntervalHarmonicBridgeGamma:
    name: str
    reads: tuple[str, str]
    accepted_bridge_tag: str
    rule_scope: str


@dataclass(frozen=True)
class IntervalHarmonicBridgeObservation:
    target_selection_observation: IntervalTargetSelectionObservation
    harmonic_bridge_inventory: HarmonicBridgeInventory | None
    gamma_harmonic_bridge: IntervalHarmonicBridgeGamma | None
    harmonic_bridge: HarmonicBridgeCandidate | None
    harmonic_function_annotation_generated: bool
    target_generated: bool
    core_promoted: bool
    status: str
    bridge_reason: str | None


@dataclass(frozen=True)
class IntervalHarmonicBridgeComparison:
    without_gamma: IntervalHarmonicBridgeObservation
    with_gamma: IntervalHarmonicBridgeObservation
    same_selected_target: bool
    same_harmonic_bridge_inventory: bool
    same_gamma_harmonic_bridge: bool
    harmonic_bridge_observed: bool
    harmonic_function_annotation_generated: bool
    target_generated: bool
    core_promoted: bool


def target_selection_observation() -> IntervalTargetSelectionObservation:
    return compare_interval_target_selection().with_controller


def harmonic_bridge_inventory_fixture() -> HarmonicBridgeInventory:
    return HarmonicBridgeInventory(
        name="external_harmonic_bridge_inventory_fixture",
        candidates=(
            HarmonicBridgeCandidate(
                label="consonant_span_bridge_candidate",
                source="external_fixture",
                bridge_tag="consonance_description",
                generated_by_selected_target=False,
            ),
            HarmonicBridgeCandidate(
                label="tonic_support_bridge_candidate",
                source="external_fixture",
                bridge_tag="tonic_support",
                generated_by_selected_target=False,
            ),
            HarmonicBridgeCandidate(
                label="dominant_resolution_bridge_candidate",
                source="external_fixture",
                bridge_tag="dominant_resolution",
                generated_by_selected_target=False,
            ),
        ),
        generated_by_selected_target=False,
    )


def gamma_harmonic_bridge_fixture() -> IntervalHarmonicBridgeGamma:
    return IntervalHarmonicBridgeGamma(
        name="Gamma_interval_harmonic_bridge_fixture",
        reads=("selected_interval_target", "external_harmonic_bridge_inventory"),
        accepted_bridge_tag="tonic_support",
        rule_scope="fixture_limited_not_harmonic_function_annotation_rule",
    )


def observe_harmonic_bridge(
    target_selection: IntervalTargetSelectionObservation,
    inventory: HarmonicBridgeInventory | None,
    gamma_harmonic_bridge: IntervalHarmonicBridgeGamma | None,
) -> IntervalHarmonicBridgeObservation:
    if target_selection.selected_target is None:
        return IntervalHarmonicBridgeObservation(
            target_selection_observation=target_selection,
            harmonic_bridge_inventory=inventory,
            gamma_harmonic_bridge=gamma_harmonic_bridge,
            harmonic_bridge=None,
            harmonic_function_annotation_generated=False,
            target_generated=False,
            core_promoted=False,
            status="no_selected_interval_target",
            bridge_reason=None,
        )
    if inventory is None:
        return IntervalHarmonicBridgeObservation(
            target_selection_observation=target_selection,
            harmonic_bridge_inventory=None,
            gamma_harmonic_bridge=gamma_harmonic_bridge,
            harmonic_bridge=None,
            harmonic_function_annotation_generated=False,
            target_generated=False,
            core_promoted=False,
            status="harmonic_bridge_not_observed_without_inventory",
            bridge_reason=None,
        )
    if gamma_harmonic_bridge is None:
        return IntervalHarmonicBridgeObservation(
            target_selection_observation=target_selection,
            harmonic_bridge_inventory=inventory,
            gamma_harmonic_bridge=None,
            harmonic_bridge=None,
            harmonic_function_annotation_generated=False,
            target_generated=False,
            core_promoted=False,
            status="harmonic_bridge_not_observed_without_gamma",
            bridge_reason=None,
        )

    matches = tuple(
        candidate
        for candidate in inventory.candidates
        if candidate.bridge_tag == gamma_harmonic_bridge.accepted_bridge_tag
    )
    if len(matches) != 1:
        return IntervalHarmonicBridgeObservation(
            target_selection_observation=target_selection,
            harmonic_bridge_inventory=inventory,
            gamma_harmonic_bridge=gamma_harmonic_bridge,
            harmonic_bridge=None,
            harmonic_function_annotation_generated=False,
            target_generated=False,
            core_promoted=False,
            status="harmonic_bridge_ambiguous_or_absent",
            bridge_reason=None,
        )

    return IntervalHarmonicBridgeObservation(
        target_selection_observation=target_selection,
        harmonic_bridge_inventory=inventory,
        gamma_harmonic_bridge=gamma_harmonic_bridge,
        harmonic_bridge=matches[0],
        harmonic_function_annotation_generated=False,
        target_generated=False,
        core_promoted=False,
        status="harmonic_bridge_candidate_observed_not_annotated",
        bridge_reason="selected_target_and_external_inventory_read_by_Gamma_interval_harmonic_bridge",
    )


def compare_interval_harmonic_bridge() -> IntervalHarmonicBridgeComparison:
    target_selection = target_selection_observation()
    inventory = harmonic_bridge_inventory_fixture()
    without_gamma = observe_harmonic_bridge(target_selection, inventory, None)
    with_gamma = observe_harmonic_bridge(
        target_selection, inventory, gamma_harmonic_bridge_fixture()
    )
    return IntervalHarmonicBridgeComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_selected_target=(
            without_gamma.target_selection_observation.selected_target
            == with_gamma.target_selection_observation.selected_target
        ),
        same_harmonic_bridge_inventory=(
            without_gamma.harmonic_bridge_inventory
            == with_gamma.harmonic_bridge_inventory
        ),
        same_gamma_harmonic_bridge=(
            without_gamma.gamma_harmonic_bridge == with_gamma.gamma_harmonic_bridge
        ),
        harmonic_bridge_observed=(
            with_gamma.status == "harmonic_bridge_candidate_observed_not_annotated"
        ),
        harmonic_function_annotation_generated=(
            with_gamma.harmonic_function_annotation_generated
        ),
        target_generated=with_gamma.target_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_interval_harmonic_bridge()
    assert comparison.same_selected_target is True
    assert comparison.same_harmonic_bridge_inventory is True
    assert comparison.same_gamma_harmonic_bridge is False
    assert comparison.harmonic_bridge_observed is True
    assert comparison.harmonic_function_annotation_generated is False
    assert comparison.target_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_gamma.status
        == "harmonic_bridge_not_observed_without_gamma"
    )
    assert comparison.without_gamma.harmonic_bridge is None
    assert comparison.with_gamma.harmonic_bridge is not None
    assert comparison.with_gamma.harmonic_bridge.label == "tonic_support_bridge_candidate"
    assert comparison.with_gamma.harmonic_bridge.generated_by_selected_target is False
    assert comparison.with_gamma.harmonic_bridge_inventory is not None
    assert comparison.with_gamma.harmonic_bridge_inventory.generated_by_selected_target is False


def main() -> None:
    run_checks()
    comparison = compare_interval_harmonic_bridge()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  selected interval target candidate")
    print("  + external harmonic bridge inventory")
    print("  + Gamma_interval_harmonic_bridge_fixture")
    print("  -> harmonic function bridge candidate")
    print("  -> harmonic function annotation remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_selected_target={comparison.same_selected_target}")
    print(f"  same_harmonic_bridge_inventory={comparison.same_harmonic_bridge_inventory}")
    print(f"  same_gamma_harmonic_bridge={comparison.same_gamma_harmonic_bridge}")
    print(f"  harmonic_bridge_observed={comparison.harmonic_bridge_observed}")
    print(
        "  harmonic_bridge="
        + (with_gamma.harmonic_bridge.label if with_gamma.harmonic_bridge else "None")
    )
    print(
        "  harmonic_function_annotation_generated="
        f"{comparison.harmonic_function_annotation_generated}"
    )
    print(f"  target_generated={comparison.target_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
