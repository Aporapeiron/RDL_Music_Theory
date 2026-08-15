"""音程Module next context候補集合とselection境界の最小検証。"""

from dataclasses import dataclass

from interval_module_next_context_candidate_boundary import (
    NextContextCandidate,
    NextContextCandidateSetObservation,
    compare_next_context_candidate_set,
)


@dataclass(frozen=True)
class NextContextSelectionGamma:
    name: str
    reads: tuple[str, str]
    selected_source: str
    rule_scope: str


@dataclass(frozen=True)
class NextContextSelectionObservation:
    candidate_set_observation: NextContextCandidateSetObservation
    gamma_next_context_selection: NextContextSelectionGamma | None
    selected_next_context: NextContextCandidate | None
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    selection_reason: str | None


@dataclass(frozen=True)
class NextContextSelectionComparison:
    without_controller: NextContextSelectionObservation
    with_controller: NextContextSelectionObservation
    same_next_context_candidate_set: bool
    same_selection_controller: bool
    selected_next_context_observed: bool
    harmonic_function_generated: bool
    core_promoted: bool


def candidate_set_observation() -> NextContextCandidateSetObservation:
    return compare_next_context_candidate_set().with_gamma


def gamma_next_context_selection_fixture() -> NextContextSelectionGamma:
    return NextContextSelectionGamma(
        name="Gamma_next_context_selection_fixture",
        reads=("next_context_candidate_set", "selected_source"),
        selected_source="continuation_fixture",
        rule_scope="fixture_limited_not_harmonic_function_rule",
    )


def select_next_context(
    candidate_set: NextContextCandidateSetObservation,
    gamma_next_context_selection: NextContextSelectionGamma | None,
) -> NextContextSelectionObservation:
    if not candidate_set.next_context_candidates:
        return NextContextSelectionObservation(
            candidate_set_observation=candidate_set,
            gamma_next_context_selection=gamma_next_context_selection,
            selected_next_context=None,
            harmonic_function_generated=False,
            core_promoted=False,
            status="no_next_context_candidate_set",
            selection_reason=None,
        )
    if gamma_next_context_selection is None:
        return NextContextSelectionObservation(
            candidate_set_observation=candidate_set,
            gamma_next_context_selection=None,
            selected_next_context=None,
            harmonic_function_generated=False,
            core_promoted=False,
            status="next_context_candidate_set_unselected_without_controller",
            selection_reason=None,
        )

    matches = tuple(
        candidate
        for candidate in candidate_set.next_context_candidates
        if candidate.source == gamma_next_context_selection.selected_source
    )
    if len(matches) != 1:
        return NextContextSelectionObservation(
            candidate_set_observation=candidate_set,
            gamma_next_context_selection=gamma_next_context_selection,
            selected_next_context=None,
            harmonic_function_generated=False,
            core_promoted=False,
            status="next_context_selection_ambiguous_or_absent",
            selection_reason=None,
        )

    return NextContextSelectionObservation(
        candidate_set_observation=candidate_set,
        gamma_next_context_selection=gamma_next_context_selection,
        selected_next_context=matches[0],
        harmonic_function_generated=False,
        core_promoted=False,
        status="selected_next_context_observed_not_harmonized",
        selection_reason="next_context_candidate_matched_selected_source",
    )


def compare_next_context_selection() -> NextContextSelectionComparison:
    candidate_set = candidate_set_observation()
    without_controller = select_next_context(candidate_set, None)
    with_controller = select_next_context(
        candidate_set, gamma_next_context_selection_fixture()
    )
    return NextContextSelectionComparison(
        without_controller=without_controller,
        with_controller=with_controller,
        same_next_context_candidate_set=(
            without_controller.candidate_set_observation.next_context_candidates
            == with_controller.candidate_set_observation.next_context_candidates
        ),
        same_selection_controller=(
            without_controller.gamma_next_context_selection
            == with_controller.gamma_next_context_selection
        ),
        selected_next_context_observed=(
            with_controller.status == "selected_next_context_observed_not_harmonized"
        ),
        harmonic_function_generated=with_controller.harmonic_function_generated,
        core_promoted=with_controller.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_next_context_selection()
    assert comparison.same_next_context_candidate_set is True
    assert comparison.same_selection_controller is False
    assert comparison.selected_next_context_observed is True
    assert comparison.harmonic_function_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_controller.status
        == "next_context_candidate_set_unselected_without_controller"
    )
    assert comparison.without_controller.selected_next_context is None
    assert comparison.with_controller.selected_next_context is not None
    assert comparison.with_controller.selected_next_context.label == "C major continuation"
    assert comparison.with_controller.selected_next_context.generated_by_voice_leading is False


def main() -> None:
    run_checks()
    comparison = compare_next_context_selection()
    with_controller = comparison.with_controller
    print("[pipeline]")
    print("  next context candidate set observed")
    print("  + Gamma_next_context_selection_fixture")
    print("  -> selected next context candidate")
    print("  -> harmonic function remains None")
    print(f"  without_controller_status={comparison.without_controller.status}")
    print(f"  with_controller_status={with_controller.status}")
    print(
        "  same_next_context_candidate_set="
        f"{comparison.same_next_context_candidate_set}"
    )
    print(f"  same_selection_controller={comparison.same_selection_controller}")
    print(f"  selected_next_context_observed={comparison.selected_next_context_observed}")
    print(
        "  selected_next_context="
        + (
            with_controller.selected_next_context.label
            if with_controller.selected_next_context
            else "None"
        )
    )
    print(f"  harmonic_function_generated={comparison.harmonic_function_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
