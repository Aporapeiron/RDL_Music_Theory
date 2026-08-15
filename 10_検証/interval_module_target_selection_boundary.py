"""音程Module target候補集合とselection controller境界の最小検証。"""

from dataclasses import dataclass

from interval_module_target_candidate_boundary import (
    IntervalTargetCandidate,
    IntervalTargetCandidateSetObservation,
    compare_target_candidate_set_observation,
)


@dataclass(frozen=True)
class IntervalTargetSelectionGamma:
    name: str
    reads: tuple[str, str]
    selected_policy_tag: str
    rule_scope: str


@dataclass(frozen=True)
class IntervalTargetSelectionObservation:
    target_set_observation: IntervalTargetCandidateSetObservation
    gamma_target_selection: IntervalTargetSelectionGamma | None
    selected_target: IntervalTargetCandidate | None
    voice_leading_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    selection_reason: str | None


@dataclass(frozen=True)
class IntervalTargetSelectionComparison:
    without_controller: IntervalTargetSelectionObservation
    with_controller: IntervalTargetSelectionObservation
    same_target_candidate_set: bool
    same_selection_controller: bool
    selected_target_observed: bool
    voice_leading_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool


def target_set_observation() -> IntervalTargetCandidateSetObservation:
    return compare_target_candidate_set_observation().with_gamma


def gamma_target_selection_fixture() -> IntervalTargetSelectionGamma:
    return IntervalTargetSelectionGamma(
        name="Gamma_interval_target_selection_fixture",
        reads=("target_candidate_set", "selected_policy_tag"),
        selected_policy_tag="preserve_span",
        rule_scope="fixture_limited_not_voice_leading_or_harmonic_function_rule",
    )


def select_interval_target(
    target_set: IntervalTargetCandidateSetObservation,
    gamma_target_selection: IntervalTargetSelectionGamma | None,
) -> IntervalTargetSelectionObservation:
    if not target_set.target_candidates:
        return IntervalTargetSelectionObservation(
            target_set_observation=target_set,
            gamma_target_selection=gamma_target_selection,
            selected_target=None,
            voice_leading_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="no_target_candidate_set",
            selection_reason=None,
        )
    if gamma_target_selection is None:
        return IntervalTargetSelectionObservation(
            target_set_observation=target_set,
            gamma_target_selection=None,
            selected_target=None,
            voice_leading_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="target_candidate_set_unselected_without_controller",
            selection_reason=None,
        )

    matches = tuple(
        candidate
        for candidate in target_set.target_candidates
        if candidate.policy_tag == gamma_target_selection.selected_policy_tag
    )
    if len(matches) != 1:
        return IntervalTargetSelectionObservation(
            target_set_observation=target_set,
            gamma_target_selection=gamma_target_selection,
            selected_target=None,
            voice_leading_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="target_selection_ambiguous_or_absent",
            selection_reason=None,
        )

    return IntervalTargetSelectionObservation(
        target_set_observation=target_set,
        gamma_target_selection=gamma_target_selection,
        selected_target=matches[0],
        voice_leading_generated=False,
        harmonic_function_generated=False,
        core_promoted=False,
        status="selected_interval_target_observed_not_realized",
        selection_reason="target_candidate_matched_selected_policy_tag",
    )


def compare_interval_target_selection() -> IntervalTargetSelectionComparison:
    target_set = target_set_observation()
    without_controller = select_interval_target(target_set, None)
    with_controller = select_interval_target(
        target_set, gamma_target_selection_fixture()
    )
    return IntervalTargetSelectionComparison(
        without_controller=without_controller,
        with_controller=with_controller,
        same_target_candidate_set=(
            without_controller.target_set_observation.target_candidates
            == with_controller.target_set_observation.target_candidates
        ),
        same_selection_controller=(
            without_controller.gamma_target_selection
            == with_controller.gamma_target_selection
        ),
        selected_target_observed=(
            with_controller.status == "selected_interval_target_observed_not_realized"
        ),
        voice_leading_generated=with_controller.voice_leading_generated,
        harmonic_function_generated=with_controller.harmonic_function_generated,
        core_promoted=with_controller.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_interval_target_selection()
    assert comparison.same_target_candidate_set is True
    assert comparison.same_selection_controller is False
    assert comparison.selected_target_observed is True
    assert comparison.voice_leading_generated is False
    assert comparison.harmonic_function_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_controller.status
        == "target_candidate_set_unselected_without_controller"
    )
    assert comparison.without_controller.selected_target is None
    assert comparison.with_controller.selected_target is not None
    assert comparison.with_controller.selected_target.label == "maintain_C_G_span"
    assert comparison.with_controller.selected_target.policy_tag == "preserve_span"
    assert comparison.with_controller.selection_reason == (
        "target_candidate_matched_selected_policy_tag"
    )


def main() -> None:
    run_checks()
    comparison = compare_interval_target_selection()
    with_controller = comparison.with_controller
    print("[pipeline]")
    print("  target candidate set observed")
    print("  + Gamma_interval_target_selection_fixture")
    print("  -> selected interval target candidate")
    print("  -> voice leading and harmonic function remain None")
    print(f"  without_controller_status={comparison.without_controller.status}")
    print(f"  with_controller_status={with_controller.status}")
    print(f"  same_target_candidate_set={comparison.same_target_candidate_set}")
    print(f"  same_selection_controller={comparison.same_selection_controller}")
    print(f"  selected_target_observed={comparison.selected_target_observed}")
    print(
        "  selected_target="
        + (with_controller.selected_target.label if with_controller.selected_target else "None")
    )
    print(f"  voice_leading_generated={comparison.voice_leading_generated}")
    print(f"  harmonic_function_generated={comparison.harmonic_function_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
