"""音程Moduleの三履歴を共通イベントへ投影する最小検証。

24では、音程固有の状態意味やcontrollerを一般化せず、既存の
observation_history / fallback_transition_history /
realized_transition_historyを、動態観測用の最小イベントへ写像する。

    observation record
      -> observation event
    fallback transition
      -> structural transition event
    realized transition
      -> realized transition event

Adapterは状態を再構成せず、イベントの分類と履歴層の分離だけを担う。
"""

from dataclasses import dataclass

from fallback_state_adoption import (
    adopt_reopen_voice_B_boundary,
    build_exhausted_state_without_import_side_effects,
)
from state_rebased_reexploration import (
    ActionAttemptRecord,
    DynamicSearchState,
    DynamicStateTransition,
    FallbackStateTransition,
    build_initial_state,
    run_step,
)


@dataclass(frozen=True)
class GenericDynamicEvent:
    """Module記録を読むための、音楽語彙を含まない最小イベント。"""

    event_kind: str
    history_channel: str
    # Module側の識別子を解釈せず、そのまま不透明な値として保持する。
    operation_kind: str
    source_state_id: str
    resulting_state_id: str | None
    operation_status: str
    change_axes: tuple[str, ...]
    realization_status: str


def _axis_names(change_axes: object) -> tuple[str, ...]:
    """Module側の変更軸を、存在する軸名だけへ投影する。"""

    axis_projection = (
        ("boundary_changed", "boundary_changed"),
        ("relation_changed", "relation_changed"),
        ("upstream_target_changed", "upstream_changed"),
    )
    return tuple(
        generic_name
        for module_name, generic_name in axis_projection
        if getattr(change_axes, module_name)
    )


def project_observation(record: ActionAttemptRecord) -> GenericDynamicEvent:
    """emptyを含む操作観測を、実現とは別のイベントへ投影する。"""

    return GenericDynamicEvent(
        event_kind="observation",
        history_channel="observation_history",
        operation_kind=record.branch_kind,
        source_state_id=record.source_state_id,
        resulting_state_id=None,
        operation_status=record.operation_status,
        change_axes=_axis_names(record.change_axes),
        realization_status="not_realized",
    )


def project_fallback(
    transition: FallbackStateTransition,
) -> GenericDynamicEvent:
    """fallbackの構造遷移を、具体実現とは別のイベントへ投影する。"""

    return GenericDynamicEvent(
        event_kind="structural_transition",
        history_channel="fallback_transition_history",
        operation_kind=transition.fallback_kind,
        source_state_id=transition.source_state_id,
        resulting_state_id=transition.resulting_state_id,
        operation_status=transition.operation_status,
        change_axes=_axis_names(transition.change_axes),
        realization_status="not_realized",
    )


def project_realized(
    transition: DynamicStateTransition,
) -> GenericDynamicEvent:
    """具体音を実現した通常遷移を、実現イベントへ投影する。"""

    return GenericDynamicEvent(
        event_kind="realized_transition",
        history_channel="realized_transition_history",
        operation_kind=transition.selected_branch_kind,
        source_state_id=transition.source_state_id,
        # DynamicStateTransitionはresulting_state_idを保持しないため、推測しない。
        resulting_state_id=None,
        operation_status=transition.operation_status,
        change_axes=_axis_names(transition.change_axes),
        realization_status="realized",
    )


def project_state(state: DynamicSearchState) -> tuple[GenericDynamicEvent, ...]:
    """三履歴をチャンネル順へ投影する（因果・時系列順ではない）。"""

    events = [project_observation(record) for record in state.observation_history]
    events.extend(project_fallback(item) for item in state.fallback_transition_history)

    events.extend(
        project_realized(transition)
        for transition in state.realized_transition_history
    )
    return tuple(events)


def _events_of_kind(
    events: tuple[GenericDynamicEvent, ...],
    event_kind: str,
) -> tuple[GenericDynamicEvent, ...]:
    return tuple(event for event in events if event.event_kind == event_kind)


def run_checks() -> None:
    # 通常探索：観測と具体実現は出るが、fallbackは出ない。
    initial = build_initial_state()
    _, _, _, ordinary_state = run_step(initial)
    ordinary_events = project_state(ordinary_state)
    ordinary_observations = _events_of_kind(ordinary_events, "observation")
    assert ordinary_observations
    assert {event.operation_kind for event in ordinary_observations} == {
        "B_change",
        "Γ_change",
        "upstream_target_change",
    }
    assert len(_events_of_kind(ordinary_events, "structural_transition")) == 0
    ordinary_realized = _events_of_kind(ordinary_events, "realized_transition")
    assert len(ordinary_realized) == 1
    assert ordinary_realized[0].realization_status == "realized"
    assert ordinary_realized[0].history_channel == "realized_transition_history"
    assert ordinary_realized[0].operation_kind == "B_change"

    # fallback復帰：構造遷移はfallbackイベントへ入り、直後の具体実現とは分離される。
    exhausted = build_exhausted_state_without_import_side_effects()
    from exhaustion_fallback_observation import observe_action_set_exhaustion

    exhaustion = observe_action_set_exhaustion(exhausted)
    reopened = adopt_reopen_voice_B_boundary(exhausted, exhaustion)
    fallback_events = project_state(reopened)
    fallback_transitions = _events_of_kind(fallback_events, "structural_transition")
    assert len(fallback_transitions) == 1
    assert fallback_transitions[0].realization_status == "not_realized"
    assert fallback_transitions[0].history_channel == "fallback_transition_history"
    assert fallback_transitions[0].operation_kind == "reopen_voice_B_boundary"
    assert len(_events_of_kind(fallback_events, "realized_transition")) == 0

    _, _, _, continued = run_step(reopened)
    continued_events = project_state(continued)
    assert len(_events_of_kind(continued_events, "structural_transition")) == 1
    assert len(_events_of_kind(continued_events, "realized_transition")) == 1
    continued_realized = _events_of_kind(continued_events, "realized_transition")[0]
    assert continued_realized.operation_kind == "upstream_target_change"
    assert "upstream_changed" in continued_realized.change_axes
    assert all(
        "upstream_target_changed" not in event.change_axes
        for event in continued_events
    )
    assert all(
        event.event_kind != "realized_transition"
        or event.realization_status == "realized"
        for event in continued_events
    )

    # empty観測は、候補がない場合でも観測イベントとして残る。
    empty_events = tuple(
        project_observation(record)
        for record in continued.observation_history
        if record.selected_pair is None
    )
    assert empty_events
    assert all(event.event_kind == "observation" for event in empty_events)
    assert all(event.realization_status == "not_realized" for event in empty_events)


def main() -> None:
    run_checks()
    initial = build_initial_state()
    _, _, _, ordinary_state = run_step(initial)
    ordinary_events = project_state(ordinary_state)
    print("[dynamic adapter boundary]")
    print(
        "ordinary=",
        {kind: len(_events_of_kind(ordinary_events, kind)) for kind in (
            "observation",
            "structural_transition",
            "realized_transition",
        )},
    )

    exhausted = build_exhausted_state_without_import_side_effects()
    from exhaustion_fallback_observation import observe_action_set_exhaustion

    reopened = adopt_reopen_voice_B_boundary(
        exhausted,
        observe_action_set_exhaustion(exhausted),
    )
    _, _, _, continued = run_step(reopened)
    continued_events = project_state(continued)
    print(
        "fallback_continued=",
        {kind: len(_events_of_kind(continued_events, kind)) for kind in (
            "observation",
            "structural_transition",
            "realized_transition",
        )},
    )


if __name__ == "__main__":
    main()
