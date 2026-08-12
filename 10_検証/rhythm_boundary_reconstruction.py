"""リズム境界変更が候補空間を実際に変えるかの最小検証。

25の第二標本で記録した ``reopen_grid_boundary`` を、候補生成器へ接続する。
境界変更前の空候補、構造遷移、変更後の再候補生成と再観測を分離して保持する。
"""

from dataclasses import dataclass

from rhythm_candidate_operations import BOUNDARY, candidate_space, constrain_candidates


@dataclass(frozen=True)
class BoundaryObservation:
    state_id: str
    operation_kind: str
    candidates: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class BoundaryTransition:
    source_state_id: str
    operation_kind: str
    source_grid_open: bool
    resulting_grid_open: bool


@dataclass(frozen=True)
class RhythmBoundaryRun:
    observations: tuple[BoundaryObservation, ...]
    structural_transitions: tuple[BoundaryTransition, ...]


def _boundary(*, grid_open: bool) -> dict[str, object]:
    return {**BOUNDARY, "grid_open": grid_open}


def dynamic_candidate_space(boundary: dict[str, object]) -> tuple[str, ...]:
    """26専用の境界依存候補生成器を返す。

    03の静的な ``candidate_space`` は変更せず、25で使った候補語彙と
    制約器を再利用して、26でのみ ``grid_open`` を候補生成条件へ接続する。
    """
    if boundary.get("meter") != BOUNDARY["meter"]:
        raise ValueError("この実験で定義していない拍子です")
    if boundary.get("grid") != BOUNDARY["grid"]:
        raise ValueError("この実験で定義していないグリッドです")
    if boundary.get("grid_open"):
        return ("表拍", "裏拍", "休符")
    return ("表拍", "裏拍")


def run_boundary_reconstruction() -> RhythmBoundaryRun:
    # 03の静的候補生成器は、元の境界定義どおり閉じた候補集合を確認する。
    assert candidate_space(BOUNDARY) == ("表拍", "裏拍")

    closed_candidates = dynamic_candidate_space(_boundary(grid_open=False))
    before = constrain_candidates(
        closed_candidates,
        current="裏拍",
        change_current=True,
        target="休符",
    )
    assert before["candidates"] == ()

    observations = (
        BoundaryObservation(
            state_id="R1",
            operation_kind="target_rest",
            candidates=before["candidates"],
            status=before["status"],
        ),
    )
    transition = BoundaryTransition(
        source_state_id="R1",
        operation_kind="reopen_grid_boundary",
        source_grid_open=False,
        resulting_grid_open=True,
    )

    open_candidates = dynamic_candidate_space(
        _boundary(grid_open=transition.resulting_grid_open)
    )
    after = constrain_candidates(
        open_candidates,
        current="裏拍",
        change_current=True,
        target="休符",
    )
    assert open_candidates == ("表拍", "裏拍", "休符")
    assert after["candidates"] == ("休符",)
    assert after["status"] == "locally_resolved"

    observations += (
        BoundaryObservation(
            state_id="R2",
            operation_kind="target_rest",
            candidates=after["candidates"],
            status=after["status"],
        ),
    )
    return RhythmBoundaryRun(
        observations=observations,
        structural_transitions=(transition,),
    )


def run_checks() -> None:
    run = run_boundary_reconstruction()
    assert len(run.observations) == 2
    assert run.observations[0].status == "no_candidate"
    assert run.observations[1].status == "locally_resolved"
    assert run.observations[0].candidates == ()
    assert run.observations[1].candidates == ("休符",)
    assert len(run.structural_transitions) == 1
    assert run.structural_transitions[0].resulting_grid_open is True


def main() -> None:
    run_checks()
    run = run_boundary_reconstruction()
    print("[rhythm boundary reconstruction]")
    print("before=", run.observations[0])
    print("transition=", run.structural_transitions[0])
    print("after=", run.observations[1])


if __name__ == "__main__":
    main()
