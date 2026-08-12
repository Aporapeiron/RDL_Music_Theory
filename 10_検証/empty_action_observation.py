"""操作後も空集合となる候補を捨てずに記録する最小検証。

19では、現在状態から候補を再生成し、実際のchange_axesを計算した。
20では、再生成後もselected=Noneとなる場合を例外にせず、
操作観測履歴へ残す。空観測はBranchEvaluationへ入れず、
選択された遷移履歴と分離する。

    state_t
      -> action
      -> observation(status=empty)
      -> observation history
      -> later re-exploration

これは音楽一般の復旧規則ではなく、19の状態・操作・観測接続を
空候補へ拡張する検証用Moduleである。
"""

from dataclasses import replace

from degree_to_pitch_realization import RealizationBoundary, SpelledNote, VoiceRange
from history_aware_reexploration_cycle import select_policy
from state_rebased_reexploration import (
    ActionObservation,
    DynamicSearchState,
    StateAction,
    advance_empty_observation,
    build_initial_state,
    observe_actions,
    observe_resulting_state,
    run_step,
)


EMPTY_ACTION = StateAction(
    branch_kind="B_tighten",
    change_layer="realization_layer",
    description="tighten voice A range so every generated candidate is removed",
)


UNRESOLVED_XI = (
    "which recovery action should be selected after empty",
    "when repeated empty exploration should stop",
)


def apply_empty_action(state: DynamicSearchState) -> DynamicSearchState:
    """候補を残さない境界変更を、検証用に一つだけ注入する。"""

    return replace(
        state,
        voice_a_boundary=RealizationBoundary(
            candidate_octaves=(4,),
            voice_range=VoiceRange(
                SpelledNote("E", accidental=1, octave=4),
                SpelledNote("G", accidental=1, octave=4),
            ),
        ),
    )


def run_checks() -> None:
    initial = build_initial_state()
    selection_0 = select_policy(initial)
    empty_observation = observe_resulting_state(
        initial,
        EMPTY_ACTION,
        apply_empty_action(initial),
    )

    # 操作は実行されたが、範囲投影で候補が消える。
    assert empty_observation.operation_status == "applied"
    assert empty_observation.change_axes.boundary_changed is True
    assert empty_observation.observation.selected is None
    assert empty_observation.observation.status == "constraint_no_candidate"
    assert empty_observation.observation.failure_stage == "B_range_projection"
    assert empty_observation.evaluation is None

    empty_state = advance_empty_observation(
        initial,
        selection_0,
        empty_observation,
    )
    assert empty_state.state_id == "S0_empty->B_tighten[empty]"
    assert empty_state.last_realized_pair == initial.last_realized_pair
    assert empty_state.realized_transition_history == ()
    assert len(empty_state.observation_history) == 1
    empty_record = empty_state.observation_history[-1]
    assert empty_record.branch_kind == "B_tighten"
    assert empty_record.observation_status == "constraint_no_candidate"
    assert empty_record.selected_pair is None
    assert empty_record.failure_stage == "B_range_projection"

    # 空状態から三操作を再評価する。Γ_changeも空のままだが、観測は消えない。
    selection_1, observations_1, decision_1, state_2 = run_step(empty_state)
    by_kind = {item.action.branch_kind: item for item in observations_1}
    gamma_observation = by_kind["Γ_change"]
    assert gamma_observation.operation_status == "applied"
    assert gamma_observation.observation.selected is None
    assert gamma_observation.observation.status == "constraint_no_candidate"
    assert gamma_observation.evaluation is None

    # 空観測は比較対象から除外されるが、有効候補による遷移は続行できる。
    assert selection_1.policy.name == "strict_relation_then_boundary"
    assert decision_1.selected_branch_kind == "upstream_target_change"
    assert tuple(note.text for note in state_2.last_realized_pair) == ("E♯4", "F♯4")
    assert len(state_2.realized_transition_history) == 1
    assert len(state_2.observation_history) == 4
    assert state_2.observation_history[-1].branch_kind == "upstream_target_change"
    assert any(
        record.observation_status == "constraint_no_candidate"
        for record in state_2.observation_history
    )

    # emptyの診断と、復旧方針の未定義部分は別に保持する。
    assert "which recovery action should be selected after empty" in UNRESOLVED_XI
    assert empty_record.observation_status != "unresolved_xi"


def print_observation(item: ActionObservation) -> None:
    if item.evaluation is None:
        print(
            f"[{item.action.branch_kind}] operation={item.operation_status} "
            f"status={item.observation.status} "
            f"failure_stage={item.observation.failure_stage}"
        )
        return
    print(
        f"[{item.action.branch_kind}] operation={item.operation_status} "
        f"status={item.observation.status} selected={item.evaluation.selected_pair}"
    )


def main() -> None:
    run_checks()
    initial = build_initial_state()
    selection = select_policy(initial)
    empty_observation = observe_resulting_state(
        initial,
        EMPTY_ACTION,
        apply_empty_action(initial),
    )
    empty_state = advance_empty_observation(initial, selection, empty_observation)
    print("[empty action observation]")
    print_observation(empty_observation)
    print(
        f"next_state={empty_state.state_id} "
        f"realized_transition_history={len(empty_state.realized_transition_history)}"
    )
    _, observations, decision, next_state = run_step(empty_state)
    print(f"selected_recovery={decision.selected_branch_kind}")
    for item in observations:
        print_observation(item)
    print(
        f"next_state={next_state.state_id} "
        f"realized_transition_history={len(next_state.realized_transition_history)} "
        f"observation_history={len(next_state.observation_history)}"
    )


if __name__ == "__main__":
    main()
