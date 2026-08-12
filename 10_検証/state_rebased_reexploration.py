"""現在状態から再探索操作を適用し、候補を再生成する最小検証。

18では、履歴から次のSearchPolicyを選ぶ接続を固定枝メニュー上で確認した。
19では、B・Γ・targetを現在状態として保持し、枝を結果テンプレートではなく
操作候補として毎回適用する。

    state_t
      -> action candidate
      -> apply to B / Γ / target
      -> regenerate candidates
      -> diff state_t and state_t+1
      -> actual change_axes

既に適用済みの操作は候補から消さず、no_effectとして観測する。
これは音楽一般の再探索規則ではなく、16〜18を接続する検証用Moduleである。
"""

from dataclasses import dataclass, replace

from degree_to_pitch_realization import (
    MajorContext,
    PairRealizationRequest,
    RealizationBoundary,
    SpelledNote,
    VoiceRealizationRequest,
    VoiceRange,
)
from history_aware_reexploration_cycle import (
    PolicySelection,
    select_policy,
)
from reexploration_after_empty import (
    ChangeAxes,
    ReexplorationObservation,
    build_seed_request,
    observe_request,
)
from reexploration_policy_comparison import (
    BranchEvaluation,
    PolicyDecision,
    SearchPolicy,
    apply_policy,
    evaluate_branch,
)


STRICT_ORDERING = "strict_voice_a_pitch_lt_voice_b_pitch"
RELAXED_ORDERING = "allow_crossed_voice_pitches"


@dataclass(frozen=True)
class ActionAttemptRecord:
    """候補選択とは別に、各操作の観測結果を履歴へ残す。"""

    source_state_id: str
    branch_kind: str
    operation_status: str
    observation_status: str
    change_axes: ChangeAxes
    selected_pair: tuple[str, str] | None
    failure_stage: str | None
    failure_reason: str | None


@dataclass(frozen=True)
class DynamicSearchState:
    """次状態へ影響する条件と、最後に実現した音高を保持する。"""

    state_id: str
    context: MajorContext
    last_realized_pair: tuple[SpelledNote, SpelledNote]
    voice_a_target_degree: int
    voice_b_target_degree: int
    voice_a_boundary: RealizationBoundary
    voice_b_boundary: RealizationBoundary
    pitch_ordering_rule: str
    last_policy_name: str | None
    last_branch_kind: str | None
    last_change_axes: ChangeAxes | None
    realized_transition_history: tuple["DynamicStateTransition", ...]
    observation_history: tuple[ActionAttemptRecord, ...] = ()
    fallback_transition_history: tuple["FallbackStateTransition", ...] = ()

    def to_request(self, name: str) -> PairRealizationRequest:
        """現在状態を16の候補生成器が読める入力へ戻す。"""

        return PairRealizationRequest(
            name=name,
            context=self.context,
            lower=VoiceRealizationRequest(
                voice="voice_A",
                start=self.last_realized_pair[0],
                target_degree=self.voice_a_target_degree,
                boundary=self.voice_a_boundary,
            ),
            upper=VoiceRealizationRequest(
                voice="voice_B",
                start=self.last_realized_pair[1],
                target_degree=self.voice_b_target_degree,
                boundary=self.voice_b_boundary,
            ),
        )


@dataclass(frozen=True)
class DynamicStateTransition:
    """操作適用後の実差分を履歴へ保存する。"""

    source_state_id: str
    policy_name: str
    selected_branch_kind: str
    operation_status: str
    resulting_pair: tuple[str, str]
    change_axes: ChangeAxes
    resulting_target_degrees: tuple[int, int]
    resulting_pitch_ordering_rule: str
    next_policy_reason: str


@dataclass(frozen=True)
class FallbackStateTransition:
    """fallbackが実状態へ与えた遷移を、具体音遷移とは別に保存する。"""

    source_state_id: str
    fallback_kind: str
    outcome_status: str
    operation_status: str
    resulting_state_id: str
    change_axes: ChangeAxes
    resulting_voice_b_boundary: str
    next_policy_reason: str


@dataclass(frozen=True)
class StateAction:
    """現在状態へ適用する操作候補。枝名は操作の表示名にすぎない。"""

    branch_kind: str
    change_layer: str
    description: str


@dataclass(frozen=True)
class ActionObservation:
    """一つの操作を現在状態へ適用した観測。"""

    action: StateAction
    source_state_id: str
    resulting_state: DynamicSearchState
    operation_status: str
    change_axes: ChangeAxes
    observation: ReexplorationObservation
    evaluation: BranchEvaluation | None


ACTIONS = (
    StateAction(
        branch_kind="B_change",
        change_layer="realization_layer",
        description="reopen voice A candidate octave and voice range",
    ),
    StateAction(
        branch_kind="Γ_change",
        change_layer="realization_layer",
        description="relax the voice A pitch < voice B pitch relation",
    ),
    StateAction(
        branch_kind="upstream_target_change",
        change_layer="upstream_target_layer",
        description="replace upstream target degree 3 -> 7",
    ),
)


def build_initial_state() -> DynamicSearchState:
    seed = build_seed_request()
    return DynamicSearchState(
        state_id="S0_empty",
        context=seed.context,
        last_realized_pair=(seed.lower.start, seed.upper.start),
        voice_a_target_degree=seed.lower.target_degree,
        voice_b_target_degree=seed.upper.target_degree,
        voice_a_boundary=seed.lower.boundary,
        voice_b_boundary=seed.upper.boundary,
        pitch_ordering_rule=STRICT_ORDERING,
        last_policy_name=None,
        last_branch_kind=None,
        last_change_axes=None,
        realized_transition_history=(),
    )


def apply_action(
    state: DynamicSearchState,
    action: StateAction,
) -> DynamicSearchState:
    """操作候補を現在状態へ適用する。適用前後の比較は別関数で行う。"""

    if action.branch_kind == "B_change":
        return replace(
            state,
            voice_a_boundary=RealizationBoundary(
                candidate_octaves=(3, 4),
                voice_range=VoiceRange(
                    SpelledNote("E", accidental=1, octave=3),
                    SpelledNote("A", accidental=1, octave=4),
                ),
            ),
        )
    if action.branch_kind == "Γ_change":
        return replace(state, pitch_ordering_rule=RELAXED_ORDERING)
    if action.branch_kind == "upstream_target_change":
        return replace(state, voice_a_target_degree=7)
    raise ValueError(f"unknown state action: {action.branch_kind}")


def diff_change_axes(
    source: DynamicSearchState,
    resulting: DynamicSearchState,
) -> ChangeAxes:
    """枝名ではなく、状態の実差分から変更軸を計算する。"""

    return ChangeAxes(
        boundary_changed=(
            source.voice_a_boundary != resulting.voice_a_boundary
            or source.voice_b_boundary != resulting.voice_b_boundary
        ),
        relation_changed=(
            source.pitch_ordering_rule != resulting.pitch_ordering_rule
        ),
        upstream_target_changed=(
            (
                source.voice_a_target_degree,
                source.voice_b_target_degree,
            )
            != (
                resulting.voice_a_target_degree,
                resulting.voice_b_target_degree,
            )
        ),
    )


def _pair_motion(
    source_pair: tuple[SpelledNote, SpelledNote],
    target_pair: tuple[SpelledNote, SpelledNote],
) -> int:
    return sum(
        abs(target.chromatic_index - source.chromatic_index)
        for source, target in zip(source_pair, target_pair)
    )


def observe_action(
    state: DynamicSearchState,
    action: StateAction,
) -> ActionObservation:
    """操作を適用し、現在状態から候補を再生成して実差分を記録する。"""

    resulting_state = apply_action(state, action)
    return observe_resulting_state(state, action, resulting_state)


def observe_resulting_state(
    state: DynamicSearchState,
    action: StateAction,
    resulting_state: DynamicSearchState,
) -> ActionObservation:
    """指定した次条件を観測する。候補が空でも観測を捨てない。"""

    change_axes = diff_change_axes(state, resulting_state)
    operation_status = "applied" if change_axes != ChangeAxes() else "no_effect"
    request = resulting_state.to_request(
        name=f"{state.state_id}: apply {action.branch_kind}"
    )
    observation = observe_request(
        request,
        branch_kind=action.branch_kind,
        change_layer=action.change_layer,
        change_axes=change_axes,
        action=action.description,
        pitch_ordering_rule=resulting_state.pitch_ordering_rule,
    )
    evaluation = None
    if observation.selected is not None:
        evaluation = evaluate_branch(observation)
        evaluation = replace(
            evaluation,
            motion_cost=_pair_motion(state.last_realized_pair, observation.selected),
        )
    return ActionObservation(
        action=action,
        source_state_id=state.state_id,
        resulting_state=resulting_state,
        operation_status=operation_status,
        change_axes=change_axes,
        observation=observation,
        evaluation=evaluation,
    )


def observe_actions(
    state: DynamicSearchState,
) -> tuple[ActionObservation, ...]:
    """固定枝を再利用せず、三つの操作を現在状態から再評価する。"""

    return tuple(observe_action(state, action) for action in ACTIONS)


def choose_action(
    selection: PolicySelection,
    observations: tuple[ActionObservation, ...],
) -> PolicyDecision:
    """no_effectを記録しつつ、採用比較からは除外する。"""

    actionable = tuple(
        item.evaluation
        for item in observations
        if item.operation_status == "applied" and item.evaluation is not None
    )
    if not actionable:
        raise ValueError("no effective state action remains")
    return apply_policy(selection.policy, actionable)


def _find_observation(
    observations: tuple[ActionObservation, ...],
    branch_kind: str,
) -> ActionObservation:
    for item in observations:
        if item.action.branch_kind == branch_kind:
            return item
    raise KeyError(f"unknown selected action: {branch_kind}")


def advance_state(
    state: DynamicSearchState,
    selection: PolicySelection,
    decision: PolicyDecision,
    observations: tuple[ActionObservation, ...],
) -> DynamicSearchState:
    selected = _find_observation(observations, decision.selected_branch_kind)
    resulting = selected.resulting_state
    selected_pair = selected.observation.selected
    if selected_pair is None:
        raise ValueError("cannot transition through an empty action observation")
    transition = DynamicStateTransition(
        source_state_id=state.state_id,
        policy_name=selection.policy.name,
        selected_branch_kind=decision.selected_branch_kind,
        operation_status=selected.operation_status,
        resulting_pair=(selected_pair[0].text, selected_pair[1].text),
        change_axes=selected.change_axes,
        resulting_target_degrees=(
            resulting.voice_a_target_degree,
            resulting.voice_b_target_degree,
        ),
        resulting_pitch_ordering_rule=resulting.pitch_ordering_rule,
        next_policy_reason=(
            "history is now available; next policy is selected from the actual "
            "state difference"
        ),
    )
    return replace(
        resulting,
        state_id=f"{state.state_id}->{decision.selected_branch_kind}",
        # 採用候補を最後に実現したペアへ記録し、次回Γ_selectの移動基準にする。
        last_realized_pair=selected_pair,
        last_policy_name=selection.policy.name,
        last_branch_kind=decision.selected_branch_kind,
        last_change_axes=selected.change_axes,
        realized_transition_history=state.realized_transition_history + (transition,),
        observation_history=state.observation_history
        + tuple(_record_observation(item) for item in observations),
    )


def _record_observation(item: ActionObservation) -> ActionAttemptRecord:
    selected_pair = item.observation.selected
    return ActionAttemptRecord(
        source_state_id=item.source_state_id,
        branch_kind=item.action.branch_kind,
        operation_status=item.operation_status,
        observation_status=item.observation.status,
        change_axes=item.change_axes,
        selected_pair=(selected_pair[0].text, selected_pair[1].text)
        if selected_pair is not None
        else None,
        failure_stage=item.observation.failure_stage,
        failure_reason=item.observation.failure_reason,
    )


def advance_empty_observation(
    state: DynamicSearchState,
    selection: PolicySelection,
    item: ActionObservation,
) -> DynamicSearchState:
    """選択候補がない操作を、遷移と混同せず観測状態として記録する。"""

    if item.observation.selected is not None:
        raise ValueError("expected an empty action observation")
    record = _record_observation(item)
    return replace(
        item.resulting_state,
        state_id=f"{state.state_id}->{item.action.branch_kind}[empty]",
        last_realized_pair=state.last_realized_pair,
        last_policy_name=selection.policy.name,
        last_branch_kind=item.action.branch_kind,
        last_change_axes=item.change_axes,
        realized_transition_history=state.realized_transition_history,
        observation_history=state.observation_history + (record,),
    )


def run_step(
    state: DynamicSearchState,
) -> tuple[
    PolicySelection,
    tuple[ActionObservation, ...],
    PolicyDecision,
    DynamicSearchState,
]:
    selection = select_policy(state)
    observations = observe_actions(state)
    decision = choose_action(selection, observations)
    next_state = advance_state(state, selection, decision, observations)
    return selection, observations, decision, next_state


def _by_kind(
    observations: tuple[ActionObservation, ...],
    branch_kind: str,
) -> ActionObservation:
    return _find_observation(observations, branch_kind)


def run_checks() -> None:
    initial = build_initial_state()

    selection_0, observations_0, decision_0, state_1 = run_step(initial)
    assert selection_0.policy.name == "target_continuity_then_relation"
    assert decision_0.selected_branch_kind == "B_change"
    b_0 = _by_kind(observations_0, "B_change")
    assert b_0.operation_status == "applied"
    assert b_0.change_axes == ChangeAxes(boundary_changed=True)
    assert tuple(note.text for note in state_1.last_realized_pair) == ("A♯3", "F♯4")
    assert state_1.voice_a_boundary.candidate_octaves == (3, 4)
    assert state_1.to_request("S1 rebased request").lower.start == SpelledNote(
        "A", accidental=1, octave=3
    )

    # S1では、target操作がS0と同じ固定結果を使わず、S1のBから候補を再生成する。
    target_0 = _by_kind(observations_0, "upstream_target_change")
    selection_1, observations_1, decision_1, state_2 = run_step(state_1)
    target_1 = _by_kind(observations_1, "upstream_target_change")
    assert target_0.observation.generated_voice_a_candidates == (SpelledNote("E", accidental=1, octave=4),)
    assert tuple(note.text for note in target_1.observation.generated_voice_a_candidates) == (
        "E♯3",
        "E♯4",
    )
    assert selection_1.policy.name == "strict_relation_then_boundary"
    assert decision_1.selected_branch_kind == "upstream_target_change"
    assert target_1.operation_status == "applied"
    assert target_1.change_axes == ChangeAxes(upstream_target_changed=True)
    assert tuple(note.text for note in state_2.last_realized_pair) == ("E♯3", "F♯4")
    assert state_2.voice_a_target_degree == 7

    # S2ではtargetが既に7度なので、同じ操作は実変化を起こさない。
    target_2 = _by_kind(observe_actions(state_2), "upstream_target_change")
    assert target_2.operation_status == "no_effect"
    assert target_2.change_axes == ChangeAxes()
    assert target_2.resulting_state.voice_a_target_degree == 7
    assert target_2.observation.selected == state_2.last_realized_pair

    # no_effectを除外すると、S2ではΓ変更だけが有効な操作として残る。
    selection_2, observations_2, decision_2, state_3 = run_step(state_2)
    assert selection_2.policy.name == "minimum_immediate_motion"
    assert decision_2.selected_branch_kind == "Γ_change"
    gamma_2 = _by_kind(observations_2, "Γ_change")
    assert gamma_2.operation_status == "applied"
    assert gamma_2.change_axes == ChangeAxes(relation_changed=True)
    assert state_3.pitch_ordering_rule == RELAXED_ORDERING
    assert len(state_3.realized_transition_history) == 3

    assert [item.change_axes for item in state_3.realized_transition_history] == [
        ChangeAxes(boundary_changed=True),
        ChangeAxes(upstream_target_changed=True),
        ChangeAxes(relation_changed=True),
    ]


def print_action(item: ActionObservation) -> None:
    if item.evaluation is None:
        print(
            f"[{item.action.branch_kind}] status={item.operation_status} "
            f"observation_status={item.observation.status} "
            f"failure_stage={item.observation.failure_stage}"
        )
        return
    evaluation = item.evaluation
    print(
        f"[{item.action.branch_kind}] status={item.operation_status} "
        f"change_axes={item.change_axes} pair={evaluation.selected_pair} "
        f"motion={evaluation.motion_cost}"
    )


def main() -> None:
    run_checks()
    state = build_initial_state()
    print("[state-rebased re-exploration]")
    for index in range(3):
        selection, observations, decision, next_state = run_step(state)
        print(
            f"step={index} state={state.state_id} "
            f"policy={selection.policy.name} selected={decision.selected_branch_kind}"
        )
        for item in observations:
            print_action(item)
        transition = next_state.realized_transition_history[-1]
        print(
            f"  next_state={next_state.state_id} "
            f"pair={transition.resulting_pair} "
            f"actual_change_axes={transition.change_axes}"
        )
        state = next_state


if __name__ == "__main__":
    main()
