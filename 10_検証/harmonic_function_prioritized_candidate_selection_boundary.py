"""prioritized候補列とselection controller境界の最小検証。

52で得た同じprimary-prioritized orderingを固定し、
selection controllerの有無・種類だけを差し替える。

    same prioritized target candidate ordering
      + no selection controller -> unselected
      + select_top_rank fixture -> C major
      + select_deceptive_source fixture -> A minor

prioritized orderingはselected targetではない。
"""

from dataclasses import dataclass

from harmonic_function_target_candidate_boundary import TargetCandidate
from harmonic_function_target_candidate_prioritization_boundary import (
    PrioritizationObservation,
    PrioritizedTargetCandidate,
    compare_prioritization_policies,
)


@dataclass(frozen=True)
class SelectionController:
    name: str
    rule_scope: str


@dataclass(frozen=True)
class SelectionObservation:
    prioritization_observation: PrioritizationObservation
    selection_controller: SelectionController | None
    selected_target: TargetCandidate | None
    status: str
    selection_reason: str | None


@dataclass(frozen=True)
class SelectionComparison:
    without_controller: SelectionObservation
    top_rank_selection: SelectionObservation
    deceptive_source_selection: SelectionObservation
    same_prioritized_order: bool
    same_selection_controller: bool
    same_selected_target: bool
    top_rank_always_selected: bool


def primary_prioritization_observation() -> PrioritizationObservation:
    return compare_prioritization_policies().first


def selection_controllers() -> tuple[SelectionController, SelectionController]:
    return (
        SelectionController(
            name="select_top_rank_fixture",
            rule_scope="fixture_limited_not_general_harmony",
        ),
        SelectionController(
            name="select_deceptive_source_fixture",
            rule_scope="fixture_limited_not_general_harmony",
        ),
    )


def select_from_prioritized_candidates(
    prioritization_observation: PrioritizationObservation,
    selection_controller: SelectionController | None,
) -> SelectionObservation:
    prioritized = prioritization_observation.prioritized_candidates
    if selection_controller is None:
        return SelectionObservation(
            prioritization_observation=prioritization_observation,
            selection_controller=None,
            selected_target=None,
            status="prioritized_but_unselected",
            selection_reason=None,
        )

    if selection_controller.name == "select_top_rank_fixture":
        selected = next(
            item for item in prioritized if item.priority_rank == 1
        ).candidate
        return SelectionObservation(
            prioritization_observation=prioritization_observation,
            selection_controller=selection_controller,
            selected_target=selected,
            status="selected_target",
            selection_reason="selected_priority_rank_1",
        )

    if selection_controller.name == "select_deceptive_source_fixture":
        selected = next(
            item for item in prioritized
            if item.candidate.source == "history_boundary_fixture_deceptive"
        ).candidate
        return SelectionObservation(
            prioritization_observation=prioritization_observation,
            selection_controller=selection_controller,
            selected_target=selected,
            status="selected_target",
            selection_reason="selected_deceptive_source",
        )

    raise ValueError(f"unknown selection controller: {selection_controller.name}")


def prioritized_order(
    observation: SelectionObservation,
) -> tuple[PrioritizedTargetCandidate, ...]:
    return observation.prioritization_observation.prioritized_candidates


def compare_selection_controllers() -> SelectionComparison:
    prioritization = primary_prioritization_observation()
    top_rank_controller, deceptive_controller = selection_controllers()
    without_controller = select_from_prioritized_candidates(prioritization, None)
    top_rank_selection = select_from_prioritized_candidates(
        prioritization,
        top_rank_controller,
    )
    deceptive_source_selection = select_from_prioritized_candidates(
        prioritization,
        deceptive_controller,
    )
    first_order = prioritized_order(top_rank_selection)
    second_order = prioritized_order(deceptive_source_selection)
    return SelectionComparison(
        without_controller=without_controller,
        top_rank_selection=top_rank_selection,
        deceptive_source_selection=deceptive_source_selection,
        same_prioritized_order=first_order == second_order,
        same_selection_controller=(
            top_rank_selection.selection_controller
            == deceptive_source_selection.selection_controller
        ),
        same_selected_target=(
            top_rank_selection.selected_target
            == deceptive_source_selection.selected_target
        ),
        top_rank_always_selected=(
            deceptive_source_selection.selected_target
            == next(item for item in first_order if item.priority_rank == 1).candidate
        ),
    )


def run_checks() -> None:
    comparison = compare_selection_controllers()
    assert comparison.same_prioritized_order is True
    assert comparison.same_selection_controller is False
    assert comparison.same_selected_target is False
    assert comparison.top_rank_always_selected is False

    assert comparison.without_controller.status == "prioritized_but_unselected"
    assert comparison.without_controller.selected_target is None

    assert comparison.top_rank_selection.status == "selected_target"
    assert comparison.top_rank_selection.selected_target is not None
    assert comparison.top_rank_selection.selected_target.target_chord == "C major"
    assert comparison.top_rank_selection.selection_reason == "selected_priority_rank_1"

    assert comparison.deceptive_source_selection.status == "selected_target"
    assert comparison.deceptive_source_selection.selected_target is not None
    assert comparison.deceptive_source_selection.selected_target.target_chord == "A minor"
    assert comparison.deceptive_source_selection.selection_reason == "selected_deceptive_source"

    assert tuple(
        item.candidate.target_chord
        for item in comparison.top_rank_selection.prioritization_observation.prioritized_candidates
    ) == ("C major", "A minor")


def main() -> None:
    run_checks()
    comparison = compare_selection_controllers()

    print("[pipeline]")
    print("  same prioritized target candidate ordering")
    print("  + different Gamma_selection_fixture")
    print("  -> different selected target")
    print("  -> target degree plan remains ungenerated")
    print(f"  same_prioritized_order={comparison.same_prioritized_order}")
    print(f"  same_selection_controller={comparison.same_selection_controller}")
    print(f"  same_selected_target={comparison.same_selected_target}")
    print(f"  without_controller_status={comparison.without_controller.status}")
    print(
        "  prioritized_order="
        + ", ".join(
            item.candidate.target_chord
            for item in comparison.top_rank_selection.prioritization_observation.prioritized_candidates
        )
    )
    print(
        "  top_rank_controller_selected="
        + (comparison.top_rank_selection.selected_target.target_chord if comparison.top_rank_selection.selected_target else "None")
    )
    print(
        "  deceptive_source_controller_selected="
        + (
            comparison.deceptive_source_selection.selected_target.target_chord
            if comparison.deceptive_source_selection.selected_target
            else "None"
        )
    )
    print(f"  top_rank_always_selected={comparison.top_rank_always_selected}")


if __name__ == "__main__":
    main()