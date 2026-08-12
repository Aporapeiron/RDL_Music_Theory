"""同一BoundaryTransitionを投影と候補再構成へ通す最小検証。

26のBoundaryTransitionを一度だけ生成し、その同じrecordを
structural_transitionへ投影する。その後、recordが持つresulting_grid_openを
26専用のdynamic_candidate_spaceへ渡し、同一の境界変更が候補空間の再構成にも
使われることを確認する。共通Adapterや03の静的candidate_spaceは変更しない。
"""

from dataclasses import dataclass

from dynamic_adapter_boundary import GenericDynamicEvent
from rhythm_boundary_reconstruction import (
    BoundaryTransition,
    _boundary,
    dynamic_candidate_space,
    run_boundary_reconstruction,
)
from rhythm_candidate_operations import constrain_candidates


@dataclass(frozen=True)
class RhythmTransitionProjectionRun:
    transition: BoundaryTransition
    event: GenericDynamicEvent
    candidates: tuple[str, ...]
    status: str


def project_boundary_transition(
    transition: BoundaryTransition,
) -> GenericDynamicEvent:
    """26の同一transition recordを実差分からGenericDynamicEventへ投影する。"""

    grid_boundary_changed = (
        transition.source_grid_open != transition.resulting_grid_open
    )
    change_axes = (
        ("grid_boundary_changed",) if grid_boundary_changed else ()
    )
    operation_status = "applied" if grid_boundary_changed else "no_effect"

    return GenericDynamicEvent(
        event_kind="structural_transition",
        history_channel="fallback_transition_history",
        operation_kind=transition.operation_kind,
        source_state_id=transition.source_state_id,
        resulting_state_id=None,
        operation_status=operation_status,
        change_axes=change_axes,
        realization_status="not_realized",
    )


def run_same_transition() -> RhythmTransitionProjectionRun:
    boundary_run = run_boundary_reconstruction()
    transition = boundary_run.structural_transitions[0]
    event = project_boundary_transition(transition)

    candidates = dynamic_candidate_space(
        _boundary(grid_open=transition.resulting_grid_open)
    )
    result = constrain_candidates(
        candidates,
        current="裏拍",
        change_current=True,
        target="休符",
    )
    return RhythmTransitionProjectionRun(
        transition=transition,
        event=event,
        candidates=result["candidates"],
        status=result["status"],
    )


def run_checks() -> None:
    run = run_same_transition()
    assert run.transition.operation_kind == "reopen_grid_boundary"
    assert run.event.event_kind == "structural_transition"
    assert run.event.operation_kind == run.transition.operation_kind
    assert run.event.realization_status == "not_realized"
    assert run.event.operation_status == "applied"
    assert run.event.change_axes == ("grid_boundary_changed",)
    assert run.candidates == ("休符",)
    assert run.status == "locally_resolved"
    assert run.transition.resulting_grid_open is True

    no_effect_transition = BoundaryTransition(
        source_state_id="R2",
        operation_kind="reopen_grid_boundary",
        source_grid_open=True,
        resulting_grid_open=True,
    )
    no_effect_event = project_boundary_transition(no_effect_transition)
    assert no_effect_event.operation_status == "no_effect"
    assert no_effect_event.change_axes == ()


def main() -> None:
    run_checks()
    run = run_same_transition()
    print("[same rhythm transition projection and reconstruction]")
    print("transition=", run.transition)
    print("event=", run.event)
    print("reconstructed_candidates=", run.candidates)
    print("status=", run.status)


if __name__ == "__main__":
    main()
