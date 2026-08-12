"""実差分を持つ同一リズム境界recordが、空の再生成へ接続する最小検証。

grid_openをFalseからTrueへ変えるBoundaryTransitionを一度だけ作り、同じrecordを
structural_transitionへ投影し、26専用の動的候補生成器へ渡す。候補空間は開くが、
現在値の除外とtarget条件の交差を取ると空になることを確認する。
"""

from dataclasses import dataclass

from rhythm_boundary_reconstruction import (
    BoundaryTransition,
    _boundary,
    dynamic_candidate_space,
)
from rhythm_candidate_operations import constrain_candidates
from rhythm_transition_projection_reconstruction import project_boundary_transition


@dataclass(frozen=True)
class RhythmEmptyRegenerationRun:
    transition: BoundaryTransition
    raw_candidate_space: tuple[str, ...]
    current: str
    change_current: bool
    target: str | None
    constrained_candidates: tuple[str, ...]
    status: str


def run_empty_regeneration() -> RhythmEmptyRegenerationRun:
    current = "休符"
    change_current = True
    target = "休符"
    transition = BoundaryTransition(
        source_state_id="R_empty_1",
        operation_kind="reopen_grid_boundary",
        source_grid_open=False,
        resulting_grid_open=True,
    )
    raw_candidate_space = dynamic_candidate_space(
        _boundary(grid_open=transition.resulting_grid_open)
    )
    result = constrain_candidates(
        raw_candidate_space,
        current=current,
        change_current=change_current,
        target=target,
    )
    return RhythmEmptyRegenerationRun(
        transition=transition,
        raw_candidate_space=raw_candidate_space,
        current=result["current"],
        change_current=change_current,
        target=target,
        constrained_candidates=result["candidates"],
        status=result["status"],
    )


def run_checks() -> None:
    run = run_empty_regeneration()
    event = project_boundary_transition(run.transition)

    assert run.transition.source_grid_open != run.transition.resulting_grid_open
    assert event.event_kind == "structural_transition"
    assert event.operation_kind == run.transition.operation_kind
    assert event.operation_status == "applied"
    assert event.realization_status == "not_realized"
    assert run.raw_candidate_space == ("表拍", "裏拍", "休符")
    assert run.current == "休符"
    assert run.change_current is True
    assert run.target == "休符"
    assert run.constrained_candidates == ()
    assert run.status == "no_candidate"


def main() -> None:
    run_checks()
    run = run_empty_regeneration()
    print("[rhythm transition projection with empty regeneration]")
    print(f"operation={run.transition.operation_kind} event=structural_transition")
    print(f"raw_candidate_space={run.raw_candidate_space}")
    print(f"raw_candidate_space_count={len(run.raw_candidate_space)}")
    print(f"constrained_candidate_count={len(run.constrained_candidates)}")
    print("regeneration_status=executed")
    print(f"status={run.status}")


if __name__ == "__main__":
    main()
