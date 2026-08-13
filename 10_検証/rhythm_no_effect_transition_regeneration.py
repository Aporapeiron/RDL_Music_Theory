"""実差分のないリズム境界recordと再生成の関係を検証する。

既に開いたgridを再び開くBoundaryTransitionを同一recordとして投影と候補生成へ
渡す。再生成処理は実行できるが、source/resultの候補空間は同じであり、操作は
no_effectとして残ることを確認する。03の静的candidate_spaceは変更しない。
"""

from dataclasses import dataclass

from rhythm_boundary_reconstruction import BoundaryTransition, _boundary, dynamic_candidate_space
from rhythm_candidate_operations import constrain_candidates
from rhythm_transition_projection_reconstruction import project_boundary_transition


@dataclass(frozen=True)
class RhythmNoEffectRegenerationRun:
    transition: BoundaryTransition
    source_candidate_space: tuple[str, ...]
    resulting_candidate_space: tuple[str, ...]
    source_candidates: tuple[str, ...]
    resulting_candidates: tuple[str, ...]
    source_status: str
    resulting_status: str


def run_no_effect_regeneration() -> RhythmNoEffectRegenerationRun:
    transition = BoundaryTransition(
        source_state_id="R_open",
        operation_kind="reopen_grid_boundary",
        source_grid_open=True,
        resulting_grid_open=True,
    )
    source_candidate_space = dynamic_candidate_space(
        _boundary(grid_open=transition.source_grid_open)
    )
    resulting_candidate_space = dynamic_candidate_space(
        _boundary(grid_open=transition.resulting_grid_open)
    )
    source_result = constrain_candidates(
        source_candidate_space,
        current="裏拍",
        change_current=True,
        target="休符",
    )
    resulting_result = constrain_candidates(
        resulting_candidate_space,
        current="裏拍",
        change_current=True,
        target="休符",
    )
    return RhythmNoEffectRegenerationRun(
        transition=transition,
        source_candidate_space=source_candidate_space,
        resulting_candidate_space=resulting_candidate_space,
        source_candidates=source_result["candidates"],
        resulting_candidates=resulting_result["candidates"],
        source_status=source_result["status"],
        resulting_status=resulting_result["status"],
    )


def run_checks() -> None:
    run = run_no_effect_regeneration()
    event = project_boundary_transition(run.transition)

    assert run.transition.source_grid_open == run.transition.resulting_grid_open
    assert event.event_kind == "structural_transition"
    assert event.operation_kind == run.transition.operation_kind
    assert event.operation_status == "no_effect"
    assert event.change_axes == ()
    assert event.realization_status == "not_realized"
    assert run.source_candidate_space == run.resulting_candidate_space
    assert run.source_candidates == run.resulting_candidates == ("休符",)
    assert run.source_status == run.resulting_status == "locally_resolved"


def main() -> None:
    run_checks()
    run = run_no_effect_regeneration()
    event = project_boundary_transition(run.transition)
    print("[rhythm no-effect transition regeneration]")
    print(f"event_kind={event.event_kind} operation_status={event.operation_status}")
    print(f"source_candidate_space={run.source_candidate_space}")
    print(f"resulting_candidate_space={run.resulting_candidate_space}")
    print(f"source_candidates={run.source_candidates}")
    print(f"resulting_candidates={run.resulting_candidates}")


if __name__ == "__main__":
    main()
