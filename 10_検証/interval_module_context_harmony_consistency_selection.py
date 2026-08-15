"""音程Module context-harmony整合候補とselection境界の最小検証。"""

from dataclasses import dataclass

from interval_module_context_harmony_consistency_boundary import (
    ContextHarmonyConsistencyCandidate,
    ContextHarmonyConsistencyObservation,
    compare_context_harmony_consistency,
)


@dataclass(frozen=True)
class ContextHarmonyConsistencySelectionGamma:
    name: str
    reads: tuple[str, str]
    selected_label: str
    rule_scope: str


@dataclass(frozen=True)
class ContextHarmonyConsistencySelectionObservation:
    consistency_observation: ContextHarmonyConsistencyObservation
    gamma_consistency_selection: ContextHarmonyConsistencySelectionGamma | None
    selected_consistency: ContextHarmonyConsistencyCandidate | None
    module_state_record_generated: bool
    core_promoted: bool
    status: str
    selection_reason: str | None


@dataclass(frozen=True)
class ContextHarmonyConsistencySelectionComparison:
    without_controller: ContextHarmonyConsistencySelectionObservation
    with_controller: ContextHarmonyConsistencySelectionObservation
    same_consistency_candidates: bool
    same_selection_controller: bool
    selected_consistency_observed: bool
    module_state_record_generated: bool
    core_promoted: bool


def consistency_observation() -> ContextHarmonyConsistencyObservation:
    return compare_context_harmony_consistency().with_gamma


def gamma_consistency_selection_fixture() -> ContextHarmonyConsistencySelectionGamma:
    return ContextHarmonyConsistencySelectionGamma(
        name="Gamma_context_harmony_consistency_selection_fixture",
        reads=("context_harmony_consistency_candidates", "selected_label"),
        selected_label="C_major_tonic_support_consistency_candidate",
        rule_scope="fixture_limited_not_module_state_record_rule",
    )


def select_consistency(
    consistency: ContextHarmonyConsistencyObservation,
    gamma_selection: ContextHarmonyConsistencySelectionGamma | None,
) -> ContextHarmonyConsistencySelectionObservation:
    if not consistency.consistency_candidates:
        return ContextHarmonyConsistencySelectionObservation(
            consistency_observation=consistency,
            gamma_consistency_selection=gamma_selection,
            selected_consistency=None,
            module_state_record_generated=False,
            core_promoted=False,
            status="no_context_harmony_consistency_candidates",
            selection_reason=None,
        )
    if gamma_selection is None:
        return ContextHarmonyConsistencySelectionObservation(
            consistency_observation=consistency,
            gamma_consistency_selection=None,
            selected_consistency=None,
            module_state_record_generated=False,
            core_promoted=False,
            status="consistency_candidates_unselected_without_controller",
            selection_reason=None,
        )

    matches = tuple(
        candidate
        for candidate in consistency.consistency_candidates
        if candidate.label == gamma_selection.selected_label
    )
    if len(matches) != 1:
        return ContextHarmonyConsistencySelectionObservation(
            consistency_observation=consistency,
            gamma_consistency_selection=gamma_selection,
            selected_consistency=None,
            module_state_record_generated=False,
            core_promoted=False,
            status="consistency_selection_ambiguous_or_absent",
            selection_reason=None,
        )

    selected = ContextHarmonyConsistencyCandidate(
        label=matches[0].label,
        selected_context_label=matches[0].selected_context_label,
        harmonic_function_label=matches[0].harmonic_function_label,
        selected=True,
        module_state_record_generated=False,
    )
    return ContextHarmonyConsistencySelectionObservation(
        consistency_observation=consistency,
        gamma_consistency_selection=gamma_selection,
        selected_consistency=selected,
        module_state_record_generated=False,
        core_promoted=False,
        status="selected_context_harmony_consistency_observed_not_recorded",
        selection_reason="consistency_candidate_matched_selected_label",
    )


def compare_consistency_selection() -> ContextHarmonyConsistencySelectionComparison:
    consistency = consistency_observation()
    without_controller = select_consistency(consistency, None)
    with_controller = select_consistency(
        consistency, gamma_consistency_selection_fixture()
    )
    return ContextHarmonyConsistencySelectionComparison(
        without_controller=without_controller,
        with_controller=with_controller,
        same_consistency_candidates=(
            without_controller.consistency_observation.consistency_candidates
            == with_controller.consistency_observation.consistency_candidates
        ),
        same_selection_controller=(
            without_controller.gamma_consistency_selection
            == with_controller.gamma_consistency_selection
        ),
        selected_consistency_observed=(
            with_controller.status
            == "selected_context_harmony_consistency_observed_not_recorded"
        ),
        module_state_record_generated=with_controller.module_state_record_generated,
        core_promoted=with_controller.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_consistency_selection()
    assert comparison.same_consistency_candidates is True
    assert comparison.same_selection_controller is False
    assert comparison.selected_consistency_observed is True
    assert comparison.module_state_record_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_controller.status
        == "consistency_candidates_unselected_without_controller"
    )
    assert comparison.without_controller.selected_consistency is None
    assert comparison.with_controller.selected_consistency is not None
    assert comparison.with_controller.selected_consistency.selected is True
    assert comparison.with_controller.selected_consistency.module_state_record_generated is False


def main() -> None:
    run_checks()
    comparison = compare_consistency_selection()
    with_controller = comparison.with_controller
    print("[pipeline]")
    print("  context-harmony consistency candidates")
    print("  + Gamma_context_harmony_consistency_selection_fixture")
    print("  -> selected consistency candidate")
    print("  -> module state record remains None")
    print(f"  without_controller_status={comparison.without_controller.status}")
    print(f"  with_controller_status={with_controller.status}")
    print(f"  same_consistency_candidates={comparison.same_consistency_candidates}")
    print(f"  same_selection_controller={comparison.same_selection_controller}")
    print(f"  selected_consistency_observed={comparison.selected_consistency_observed}")
    print(
        "  selected_consistency="
        + (
            with_controller.selected_consistency.label
            if with_controller.selected_consistency
            else "None"
        )
    )
    print(
        "  module_state_record_generated="
        f"{comparison.module_state_record_generated}"
    )
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
