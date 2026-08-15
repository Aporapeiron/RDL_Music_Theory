"""prioritized bridge orderingとselection controller境界の最小検証。

63で得た同じprioritized bridge orderingを固定し、selection controllerの
有無・種類だけを差し替える。selected bridge candidateは生成するが、
confirmed learned category / selected musical interpretationへは昇格しない。

    same prioritized bridge ordering
      + no selection controller -> unselected
      + select_top_rank fixture -> different label bridge
      + select_uncertain_label fixture -> uncertain label bridge
"""

from dataclasses import dataclass

from base_to_learned_bridge_candidate_prioritization_boundary import (
    BridgePrioritizationObservation,
    PrioritizedBridgeCandidate,
    compare_bridge_prioritization,
)


@dataclass(frozen=True)
class BridgeSelectionController:
    name: str
    rule_scope: str


@dataclass(frozen=True)
class BridgeSelectionObservation:
    prioritization_observation: BridgePrioritizationObservation
    selection_controller: BridgeSelectionController | None
    selected_bridge_candidate: PrioritizedBridgeCandidate | None
    selected_musical_interpretation: str | None
    confirmed_learned_category: bool
    status: str
    selection_reason: str | None


@dataclass(frozen=True)
class BridgeSelectionComparison:
    without_controller: BridgeSelectionObservation
    top_rank_selection: BridgeSelectionObservation
    uncertain_label_selection: BridgeSelectionObservation
    same_prioritized_ordering: bool
    same_selection_controller: bool
    same_selected_bridge_candidate: bool
    top_rank_always_selected: bool
    selected_musical_interpretation: str | None
    confirmed_learned_category: bool


def primary_prioritization_observation() -> BridgePrioritizationObservation:
    return compare_bridge_prioritization().with_prioritization


def bridge_selection_controllers() -> tuple[
    BridgeSelectionController,
    BridgeSelectionController,
]:
    return (
        BridgeSelectionController(
            name="select_top_rank_bridge_fixture",
            rule_scope="fixture_limited_not_general_bridge_selection",
        ),
        BridgeSelectionController(
            name="select_uncertain_label_bridge_fixture",
            rule_scope="fixture_limited_not_general_bridge_selection",
        ),
    )


def select_from_prioritized_bridge_candidates(
    prioritization_observation: BridgePrioritizationObservation,
    selection_controller: BridgeSelectionController | None,
) -> BridgeSelectionObservation:
    prioritized = prioritization_observation.prioritized_bridge_candidates
    if not prioritized:
        return BridgeSelectionObservation(
            prioritization_observation=prioritization_observation,
            selection_controller=selection_controller,
            selected_bridge_candidate=None,
            selected_musical_interpretation=None,
            confirmed_learned_category=False,
            status="no_prioritized_bridge_candidates",
            selection_reason=None,
        )

    if selection_controller is None:
        return BridgeSelectionObservation(
            prioritization_observation=prioritization_observation,
            selection_controller=None,
            selected_bridge_candidate=None,
            selected_musical_interpretation=None,
            confirmed_learned_category=False,
            status="prioritized_bridge_ordering_unselected",
            selection_reason=None,
        )

    if selection_controller.name == "select_top_rank_bridge_fixture":
        selected = next(
            candidate for candidate in prioritized if candidate.priority_rank == 1
        )
        return BridgeSelectionObservation(
            prioritization_observation=prioritization_observation,
            selection_controller=selection_controller,
            selected_bridge_candidate=selected,
            selected_musical_interpretation=None,
            confirmed_learned_category=False,
            status="selected_bridge_candidate_not_confirmed",
            selection_reason="selected_priority_rank_1",
        )

    if selection_controller.name == "select_uncertain_label_bridge_fixture":
        selected = next(
            candidate
            for candidate in prioritized
            if candidate.bridge_candidate.learned_candidate.label
            == "uncertain_pitch_relation_label_candidate"
        )
        return BridgeSelectionObservation(
            prioritization_observation=prioritization_observation,
            selection_controller=selection_controller,
            selected_bridge_candidate=selected,
            selected_musical_interpretation=None,
            confirmed_learned_category=False,
            status="selected_bridge_candidate_not_confirmed",
            selection_reason="selected_uncertain_label",
        )

    raise ValueError(f"unknown selection controller: {selection_controller.name}")


def prioritized_ordering(
    observation: BridgeSelectionObservation,
) -> tuple[PrioritizedBridgeCandidate, ...]:
    return observation.prioritization_observation.prioritized_bridge_candidates


def selected_label(observation: BridgeSelectionObservation) -> str | None:
    if observation.selected_bridge_candidate is None:
        return None
    return (
        observation.selected_bridge_candidate.bridge_candidate.learned_candidate.label
    )


def compare_bridge_selection_controllers() -> BridgeSelectionComparison:
    prioritization = primary_prioritization_observation()
    top_rank_controller, uncertain_controller = bridge_selection_controllers()
    without_controller = select_from_prioritized_bridge_candidates(
        prioritization,
        None,
    )
    top_rank_selection = select_from_prioritized_bridge_candidates(
        prioritization,
        top_rank_controller,
    )
    uncertain_label_selection = select_from_prioritized_bridge_candidates(
        prioritization,
        uncertain_controller,
    )
    first_order = prioritized_ordering(top_rank_selection)
    second_order = prioritized_ordering(uncertain_label_selection)
    rank_one = next(item for item in first_order if item.priority_rank == 1)
    return BridgeSelectionComparison(
        without_controller=without_controller,
        top_rank_selection=top_rank_selection,
        uncertain_label_selection=uncertain_label_selection,
        same_prioritized_ordering=(first_order == second_order),
        same_selection_controller=(
            top_rank_selection.selection_controller
            == uncertain_label_selection.selection_controller
        ),
        same_selected_bridge_candidate=(
            top_rank_selection.selected_bridge_candidate
            == uncertain_label_selection.selected_bridge_candidate
        ),
        top_rank_always_selected=(
            uncertain_label_selection.selected_bridge_candidate == rank_one
        ),
        selected_musical_interpretation=(
            top_rank_selection.selected_musical_interpretation
        ),
        confirmed_learned_category=top_rank_selection.confirmed_learned_category,
    )


def run_checks() -> None:
    comparison = compare_bridge_selection_controllers()
    assert comparison.same_prioritized_ordering is True
    assert comparison.same_selection_controller is False
    assert comparison.same_selected_bridge_candidate is False
    assert comparison.top_rank_always_selected is False
    assert comparison.selected_musical_interpretation is None
    assert comparison.confirmed_learned_category is False

    assert comparison.without_controller.status == "prioritized_bridge_ordering_unselected"
    assert comparison.without_controller.selected_bridge_candidate is None

    assert comparison.top_rank_selection.status == "selected_bridge_candidate_not_confirmed"
    assert selected_label(comparison.top_rank_selection) == (
        "different_pitch_relation_label_candidate"
    )
    assert comparison.top_rank_selection.selection_reason == "selected_priority_rank_1"

    assert (
        comparison.uncertain_label_selection.status
        == "selected_bridge_candidate_not_confirmed"
    )
    assert selected_label(comparison.uncertain_label_selection) == (
        "uncertain_pitch_relation_label_candidate"
    )
    assert (
        comparison.uncertain_label_selection.selection_reason
        == "selected_uncertain_label"
    )

    assert comparison.top_rank_selection.confirmed_learned_category is False
    assert comparison.uncertain_label_selection.confirmed_learned_category is False
    assert comparison.top_rank_selection.selected_musical_interpretation is None
    assert comparison.uncertain_label_selection.selected_musical_interpretation is None


def main() -> None:
    run_checks()
    comparison = compare_bridge_selection_controllers()

    print("[pipeline]")
    print("  same prioritized bridge ordering")
    print("  + different Gamma_bridge_selection_fixture")
    print("  -> different selected bridge candidate")
    print("  -> selected musical interpretation remains None")
    print(f"  same_prioritized_ordering={comparison.same_prioritized_ordering}")
    print(f"  same_selection_controller={comparison.same_selection_controller}")
    print(
        "  same_selected_bridge_candidate="
        f"{comparison.same_selected_bridge_candidate}"
    )
    print(f"  without_controller_status={comparison.without_controller.status}")
    print(
        "  prioritized_ordering="
        + ", ".join(
            f"{item.priority_rank}:{item.bridge_candidate.learned_candidate.label}"
            for item in comparison.top_rank_selection.prioritization_observation.prioritized_bridge_candidates
        )
    )
    print(
        "  top_rank_controller_selected="
        + (selected_label(comparison.top_rank_selection) or "None")
    )
    print(
        "  uncertain_label_controller_selected="
        + (selected_label(comparison.uncertain_label_selection) or "None")
    )
    print(f"  top_rank_always_selected={comparison.top_rank_always_selected}")
    print(
        "  selected_musical_interpretation="
        f"{comparison.selected_musical_interpretation}"
    )
    print(f"  confirmed_learned_category={comparison.confirmed_learned_category}")


if __name__ == "__main__":
    main()
