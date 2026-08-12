"""fallback outcomeを実状態へ採用する最小検証。

21では、列挙済みaction set枯渇後のfallbackを outcome observation として
比較した。22では、そのうち ``reopen_voice_B_boundary`` を一つ採用し、
実際の ``DynamicSearchState`` を構成する。

    S2_action_set_exhausted
      -> reopen_voice_B_boundary
      -> S3_boundary_reopened
      -> ordinary action selection
      -> S4_realized

境界再開は具体音の実現ではない。そのため、fallback自体は
``realized_transition_history``へ入れず、``fallback_transition_history``へ
記録する。S3から通常操作を採用した時点で、初めて具体音遷移が
``realized_transition_history``へ追加される。
"""

from dataclasses import replace

from exhaustion_fallback_observation import (
    UNRESOLVED_XI,
    ExhaustionObservation,
    build_exhausted_state,
    observe_action_set_exhaustion,
    reopen_voice_B_boundary,
    reopen_voice_B_boundary_state,
)
from state_rebased_reexploration import (
    FallbackStateTransition,
    DynamicSearchState,
    diff_change_axes,
    run_step,
)


def adopt_reopen_voice_B_boundary(
    state: DynamicSearchState,
    exhaustion: ExhaustionObservation,
) -> DynamicSearchState:
    """境界再開fallbackを実状態へ適用し、fallback履歴へ記録する。"""

    outcome = reopen_voice_B_boundary(state, exhaustion)
    reopened = reopen_voice_B_boundary_state(state)
    next_state_id = f"{state.state_id}->reopen_voice_B_boundary"
    change_axes = diff_change_axes(state, reopened)
    assert change_axes.boundary_changed is True
    operation_status = "applied" if change_axes != type(change_axes)() else "no_effect"
    transition = FallbackStateTransition(
        source_state_id=state.state_id,
        fallback_kind=outcome.fallback_kind,
        outcome_status=outcome.outcome_status,
        operation_status=operation_status,
        resulting_state_id=next_state_id,
        change_axes=change_axes,
        source_voice_b_boundary=state.voice_b_boundary,
        resulting_voice_b_boundary=reopened.voice_b_boundary,
        next_policy_reason=(
            "fallback changed voice B boundary; ordinary action policy reads "
            "the actual boundary change next"
        ),
    )
    return replace(
        reopened,
        state_id=next_state_id,
        last_policy_name=None,
        last_branch_kind=outcome.fallback_kind,
        last_change_axes=transition.change_axes,
        fallback_transition_history=state.fallback_transition_history + (transition,),
    )


def build_exhausted_state_without_import_side_effects() -> DynamicSearchState:
    """21の枯渇状態をそのまま再構成する入口。"""

    return build_exhausted_state()


def run_checks() -> None:
    exhausted = build_exhausted_state_without_import_side_effects()
    exhaustion = observe_action_set_exhaustion(exhausted)
    reopened = adopt_reopen_voice_B_boundary(exhausted, exhaustion)

    assert reopened.state_id.endswith("->reopen_voice_B_boundary")
    assert reopened.voice_b_boundary.voice_range.low.text == "F♯4"
    assert reopened.voice_b_boundary.voice_range.high.text == "F♯4"
    assert len(reopened.fallback_transition_history) == 1
    fallback_record = reopened.fallback_transition_history[-1]
    assert fallback_record.source_state_id == exhausted.state_id
    assert fallback_record.fallback_kind == "reopen_voice_B_boundary"
    assert fallback_record.outcome_status == "candidate_space_reopened"
    assert fallback_record.operation_status == "applied"
    assert fallback_record.resulting_state_id == reopened.state_id
    assert fallback_record.change_axes.boundary_changed is True
    assert fallback_record.source_voice_b_boundary == exhausted.voice_b_boundary
    assert fallback_record.resulting_voice_b_boundary == reopened.voice_b_boundary
    assert reopened.realized_transition_history == ()

    # fallback後は、同じsource stateからの観測ではなく、実際のS3から再探索する。
    selection, observations, decision, realized = run_step(reopened)
    assert selection.policy.name == "strict_relation_then_boundary"
    assert decision.selected_branch_kind == "upstream_target_change"
    assert len(realized.fallback_transition_history) == 1
    assert len(realized.realized_transition_history) == 1
    assert realized.realized_transition_history[-1].selected_branch_kind == (
        "upstream_target_change"
    )
    assert tuple(note.text for note in realized.last_realized_pair) == (
        "E♯4",
        "F♯4",
    )
    assert any(item.action.branch_kind == "B_change" for item in observations)

    # さらに通常探索が続き、target変更後の方針へ接続する。
    next_selection, _, next_decision, continued = run_step(realized)
    assert next_selection.policy.name == "minimum_immediate_motion"
    assert next_decision.selected_branch_kind == "B_change"
    assert len(continued.fallback_transition_history) == 1
    assert len(continued.realized_transition_history) == 2
    assert continued.realized_transition_history[-1].selected_branch_kind == (
        "B_change"
    )

    # fallback観測の未解決部分は、実状態を作った後も自動解消しない。
    assert any("fallback" in item and "selected" in item for item in UNRESOLVED_XI)


def main() -> None:
    run_checks()
    exhausted = build_exhausted_state_without_import_side_effects()
    exhaustion = observe_action_set_exhaustion(exhausted)
    reopened = adopt_reopen_voice_B_boundary(exhausted, exhaustion)
    selection, _, decision, realized = run_step(reopened)
    next_selection, _, next_decision, continued = run_step(realized)
    print("[fallback state adoption]")
    print(
        f"source={exhausted.state_id} fallback={reopened.state_id} "
        f"fallback_history={len(reopened.fallback_transition_history)} "
        f"realized_history={len(reopened.realized_transition_history)}"
    )
    print(
        f"step=1 policy={selection.policy.name} selected={decision.selected_branch_kind} "
        f"state={realized.state_id}"
    )
    print(
        f"step=2 policy={next_selection.policy.name} "
        f"selected={next_decision.selected_branch_kind} state={continued.state_id}"
    )


if __name__ == "__main__":
    main()
