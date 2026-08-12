"""リズム候補Moduleを共通動態イベントへ投影する第二標本。

音程Moduleとは異なる、表拍・裏拍だけの閉じた候補空間を使う。
リズム側の記録形式や状態意味は共通化せず、24で定義した
observation / structural_transition / realized_transition の境界へ
投影できるかだけを検証する。
"""

from dataclasses import dataclass

from dynamic_adapter_boundary import GenericDynamicEvent
from rhythm_candidate_operations import BOUNDARY, candidate_space, constrain_candidates


@dataclass(frozen=True)
class RhythmChangeAxes:
    """リズムModule固有の変更軸。共通名へ解釈しない。"""

    grid_boundary_changed: bool = False
    candidate_relation_changed: bool = False


@dataclass(frozen=True)
class RhythmActionAttemptRecord:
    source_state_id: str
    branch_kind: str
    operation_status: str
    observation_status: str
    change_axes: RhythmChangeAxes
    selected_candidate: str | None
    failure_reason: str | None


@dataclass(frozen=True)
class RhythmStructuralTransition:
    source_state_id: str
    fallback_kind: str
    operation_status: str
    resulting_state_id: str
    change_axes: RhythmChangeAxes


@dataclass(frozen=True)
class RhythmRealizedTransition:
    source_state_id: str
    selected_branch_kind: str
    operation_status: str
    resulting_candidate: str
    change_axes: RhythmChangeAxes


@dataclass(frozen=True)
class RhythmState:
    state_id: str
    current: str
    target: str | None
    grid_open: bool
    observation_history: tuple[RhythmActionAttemptRecord, ...] = ()
    fallback_transition_history: tuple[RhythmStructuralTransition, ...] = ()
    realized_transition_history: tuple[RhythmRealizedTransition, ...] = ()


def _axes(axes: RhythmChangeAxes) -> tuple[str, ...]:
    """Module固有の軸名を、そのまま共通イベントの軸列へ投影する。"""

    names = []
    if axes.grid_boundary_changed:
        names.append("grid_boundary_changed")
    if axes.candidate_relation_changed:
        names.append("candidate_relation_changed")
    return tuple(names)


def project_observation(record: RhythmActionAttemptRecord) -> GenericDynamicEvent:
    return GenericDynamicEvent(
        event_kind="observation",
        history_channel="observation_history",
        operation_kind=record.branch_kind,
        source_state_id=record.source_state_id,
        resulting_state_id=None,
        operation_status=record.operation_status,
        change_axes=_axes(record.change_axes),
        realization_status="not_realized",
    )


def project_fallback(transition: RhythmStructuralTransition) -> GenericDynamicEvent:
    return GenericDynamicEvent(
        event_kind="structural_transition",
        history_channel="fallback_transition_history",
        operation_kind=transition.fallback_kind,
        source_state_id=transition.source_state_id,
        resulting_state_id=transition.resulting_state_id,
        operation_status=transition.operation_status,
        change_axes=_axes(transition.change_axes),
        realization_status="not_realized",
    )


def project_realized(transition: RhythmRealizedTransition) -> GenericDynamicEvent:
    return GenericDynamicEvent(
        event_kind="realized_transition",
        history_channel="realized_transition_history",
        operation_kind=transition.selected_branch_kind,
        source_state_id=transition.source_state_id,
        resulting_state_id=None,
        operation_status=transition.operation_status,
        change_axes=_axes(transition.change_axes),
        realization_status="realized",
    )


def project_state(state: RhythmState) -> tuple[GenericDynamicEvent, ...]:
    """履歴チャンネル順へ投影する。出力順は因果・時系列順ではない。"""

    events = [project_observation(item) for item in state.observation_history]
    events.extend(project_fallback(item) for item in state.fallback_transition_history)
    events.extend(project_realized(item) for item in state.realized_transition_history)
    return tuple(events)


def _events_of_kind(
    events: tuple[GenericDynamicEvent, ...],
    event_kind: str,
) -> tuple[GenericDynamicEvent, ...]:
    return tuple(event for event in events if event.event_kind == event_kind)


def _build_state() -> RhythmState:
    candidates = candidate_space(BOUNDARY)
    initial = RhythmState(state_id="R0", current="表拍", target=None, grid_open=False)

    changed = constrain_candidates(candidates, current=initial.current, change_current=True)
    assert changed["candidates"] == ("裏拍",)
    observed = RhythmActionAttemptRecord(
        source_state_id=initial.state_id,
        branch_kind="change_current",
        operation_status="applied",
        observation_status=changed["status"],
        change_axes=RhythmChangeAxes(candidate_relation_changed=True),
        selected_candidate="裏拍",
        failure_reason=None,
    )
    realized = RhythmRealizedTransition(
        source_state_id=initial.state_id,
        selected_branch_kind="select_offbeat",
        operation_status="applied",
        resulting_candidate="裏拍",
        change_axes=RhythmChangeAxes(candidate_relation_changed=True),
    )

    exhausted = RhythmState(
        state_id="R1",
        current="裏拍",
        target="休符",
        grid_open=False,
        observation_history=(observed,),
        realized_transition_history=(realized,),
    )
    empty = constrain_candidates(
        candidates,
        current=exhausted.current,
        change_current=True,
        target=exhausted.target,
    )
    assert empty["candidates"] == ()
    empty_observation = RhythmActionAttemptRecord(
        source_state_id=exhausted.state_id,
        branch_kind="target_rest",
        operation_status="applied",
        observation_status=empty["status"],
        change_axes=RhythmChangeAxes(candidate_relation_changed=True),
        selected_candidate=None,
        failure_reason="no_candidate",
    )
    return RhythmState(
        state_id="R2",
        current="裏拍",
        target=None,
        grid_open=True,
        observation_history=exhausted.observation_history + (empty_observation,),
        fallback_transition_history=(
            RhythmStructuralTransition(
                source_state_id=exhausted.state_id,
                fallback_kind="reopen_grid_boundary",
                operation_status="applied",
                resulting_state_id="R2",
                change_axes=RhythmChangeAxes(grid_boundary_changed=True),
            ),
        ),
        realized_transition_history=exhausted.realized_transition_history,
    )


def run_checks() -> None:
    events = project_state(_build_state())
    assert len(_events_of_kind(events, "observation")) == 2
    assert len(_events_of_kind(events, "structural_transition")) == 1
    assert len(_events_of_kind(events, "realized_transition")) == 1
    assert {event.operation_kind for event in events} == {
        "change_current",
        "target_rest",
        "reopen_grid_boundary",
        "select_offbeat",
    }
    assert _events_of_kind(events, "observation")[-1].realization_status == "not_realized"
    fallback = _events_of_kind(events, "structural_transition")[0]
    assert fallback.resulting_state_id == "R2"
    assert fallback.realization_status == "not_realized"
    assert _events_of_kind(events, "realized_transition")[0].realization_status == "realized"
    assert "grid_boundary_changed" in fallback.change_axes


def main() -> None:
    run_checks()
    events = project_state(_build_state())
    print("[rhythm dynamic adapter]")
    print({
        kind: len(_events_of_kind(events, kind))
        for kind in ("observation", "structural_transition", "realized_transition")
    })
    print("operation_kinds=", tuple(event.operation_kind for event in events))


if __name__ == "__main__":
    main()

