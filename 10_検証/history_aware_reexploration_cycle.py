"""採用枝から次状態へ進み、履歴で方針を更新する最小検証。

17では、同じ再探索枝へ異なるSearchPolicyを適用し、採用枝が方針に
依存することを確認した。
18では、採用枝をStateTransitionとして次状態へ記録し、その履歴を
次回の方針選択へ入力する。候補生成そのものは16から再利用し、
履歴依存の方針更新と状態遷移の接続だけを検証する。

したがって18は、現在状態から枝を再生成する完全な動態ではなく、
固定した枝メニュー上のcontroller接続として閉じる。状態内のB・Γ・
targetを比較し、実際の変更軸を再計算する検証は19へ送る。

この履歴→方針写像は音楽一般の法則ではなく、この実験に注入した
暫定controllerである。
"""

from dataclasses import dataclass, replace

from degree_to_pitch_realization import SpelledNote
from reexploration_after_empty import (
    ChangeAxes,
    ReexplorationObservation,
    build_reexploration_observations,
)
from reexploration_policy_comparison import (
    BranchEvaluation,
    POLICIES,
    PolicyDecision,
    SearchPolicy,
    apply_policy,
    evaluate_branch,
)


@dataclass(frozen=True)
class CycleBranch:
    """17の評価軸と16の候補観測を同じ枝として保持する。"""

    observation: ReexplorationObservation
    evaluation: BranchEvaluation


@dataclass(frozen=True)
class StateTransition:
    """採用枝が状態へ与えた変化を、枝名と分離して記録する。"""

    source_state_id: str
    policy_name: str
    selected_branch_kind: str
    resulting_pair: tuple[str, str]
    change_axes: ChangeAxes
    next_policy_reason: str


@dataclass(frozen=True)
class SearchState:
    """再探索controllerが保持する最小の次状態。"""

    state_id: str
    selected_pair: tuple[SpelledNote, SpelledNote] | None
    last_policy_name: str | None
    last_branch_kind: str | None
    last_change_axes: ChangeAxes | None
    realized_transition_history: tuple[StateTransition, ...]


@dataclass(frozen=True)
class PolicySelection:
    """履歴から次の方針を選んだ結果。"""

    policy: SearchPolicy
    reason: str


POLICY_BY_NAME = {policy.name: policy for policy in POLICIES}


def build_cycle_branches() -> tuple[CycleBranch, ...]:
    """16の初期seedから、17と同じ三枝を構成する。"""

    _, b_branch, gamma_branch, upstream_branch = (
        build_reexploration_observations()
    )
    observations = (b_branch, gamma_branch, upstream_branch)
    return tuple(
        CycleBranch(observation, evaluate_branch(observation))
        for observation in observations
    )


def _pair_motion(
    source_pair: tuple[SpelledNote, SpelledNote],
    target_pair: tuple[SpelledNote, SpelledNote],
) -> int:
    return sum(
        abs(target.chromatic_index - source.chromatic_index)
        for source, target in zip(source_pair, target_pair)
    )


def rebase_branches(
    state: SearchState,
    branches: tuple[CycleBranch, ...],
) -> tuple[BranchEvaluation, ...]:
    """候補枝の移動量だけを、現在状態からの距離へ再基準化する。

    17の枝・変更軸・保存条件は維持し、状態によって変化しうる
    即時移動量だけを再計算する。
    """

    if state.selected_pair is None:
        return tuple(branch.evaluation for branch in branches)

    return tuple(
        replace(
            branch.evaluation,
            motion_cost=_pair_motion(
                state.selected_pair,
                branch.observation.selected,
            ),
        )
        for branch in branches
    )


def select_policy(state: SearchState) -> PolicySelection:
    """直前の実変更と履歴から次の方針を選ぶ実験用controller。

    方針の起源を音楽一般から導出せず、履歴に対する暫定的な分岐表を
    明示する。選択遷移が存在しない空状態でも、直前の操作で実際に
    生じたchange_axesは方針入力として保持する。未定義の履歴条件は
    最小移動方針へ固定せず、例外として検出する。
    """

    if state.last_change_axes == ChangeAxes(boundary_changed=True):
        return PolicySelection(
            POLICY_BY_NAME["strict_relation_then_boundary"],
            "previous observed change changed B: preserve strict relation next",
        )
    if state.last_change_axes == ChangeAxes(upstream_target_changed=True):
        return PolicySelection(
            POLICY_BY_NAME["minimum_immediate_motion"],
            "previous observed change changed upstream target: reduce immediate motion next",
        )
    if not state.realized_transition_history:
        return PolicySelection(
            POLICY_BY_NAME["target_continuity_then_relation"],
            "no prior transition or effective change: preserve the upstream target first",
        )
    raise ValueError(
        "history-dependent policy is undefined for the previous branch: "
        f"{state.last_change_axes}"
    )


def _find_branch(
    branches: tuple[CycleBranch, ...],
    branch_kind: str,
) -> CycleBranch:
    for branch in branches:
        if branch.evaluation.branch_kind == branch_kind:
            return branch
    raise KeyError(f"unknown selected branch: {branch_kind}")


def advance_state(
    state: SearchState,
    selection: PolicySelection,
    decision: PolicyDecision,
    branches: tuple[CycleBranch, ...],
) -> SearchState:
    """採用枝を次状態へ反映し、履歴を一件追加する。"""

    branch = _find_branch(branches, decision.selected_branch_kind)
    if branch.observation.selected is None:
        raise ValueError("cannot transition through an empty branch")

    selected_a, selected_b = branch.observation.selected
    next_reason = (
        "history is now available; next policy is selected from the last "
        "branch change"
    )
    transition = StateTransition(
        source_state_id=state.state_id,
        policy_name=selection.policy.name,
        selected_branch_kind=decision.selected_branch_kind,
        resulting_pair=(selected_a.text, selected_b.text),
        change_axes=branch.evaluation.change_axes,
        next_policy_reason=next_reason,
    )
    return SearchState(
        state_id=f"{state.state_id}->{decision.selected_branch_kind}",
        selected_pair=(selected_a, selected_b),
        last_policy_name=selection.policy.name,
        last_branch_kind=decision.selected_branch_kind,
        last_change_axes=branch.evaluation.change_axes,
        realized_transition_history=state.realized_transition_history + (transition,),
    )


def run_cycle(
    state: SearchState,
    branches: tuple[CycleBranch, ...],
) -> tuple[PolicySelection, PolicyDecision, SearchState]:
    selection = select_policy(state)
    evaluations = rebase_branches(state, branches)
    decision = apply_policy(selection.policy, evaluations)
    next_state = advance_state(state, selection, decision, branches)
    return selection, decision, next_state


def run_checks() -> None:
    branches = build_cycle_branches()
    initial = SearchState(
        state_id="S0_empty",
        selected_pair=None,
        last_policy_name=None,
        last_branch_kind=None,
        last_change_axes=None,
        realized_transition_history=(),
    )

    selection_0, decision_0, state_1 = run_cycle(initial, branches)
    assert selection_0.policy.name == "target_continuity_then_relation"
    assert decision_0.selected_branch_kind == "B_change"
    assert state_1.selected_pair is not None
    assert tuple(note.text for note in state_1.selected_pair) == ("A♯3", "F♯4")
    assert len(state_1.realized_transition_history) == 1

    selection_1, decision_1, state_2 = run_cycle(state_1, branches)
    assert selection_1.policy.name == "strict_relation_then_boundary"
    assert decision_1.selected_branch_kind == "upstream_target_change"
    assert tuple(note.text for note in state_2.selected_pair) == ("E♯4", "F♯4")
    assert len(state_2.realized_transition_history) == 2

    # ここで停止する。S2から同じ固定枝を再適用すると、枝テンプレートの
    # change_axesと現在状態から実際に起きた変化がずれるため、完全な動態は19へ送る。
    next_selection = select_policy(state_2)
    assert next_selection.policy.name == "minimum_immediate_motion"
    assert len(state_2.realized_transition_history) == 2

    assert [item.policy_name for item in state_2.realized_transition_history] == [
        "target_continuity_then_relation",
        "strict_relation_then_boundary",
    ]
    assert [item.selected_branch_kind for item in state_2.realized_transition_history] == [
        "B_change",
        "upstream_target_change",
    ]

    # 状態由来の移動量再基準化が実際に行われている。
    rebased = rebase_branches(state_1, branches)
    by_kind = {branch.branch_kind: branch for branch in rebased}
    assert by_kind["B_change"].motion_cost == 0
    assert by_kind["Γ_change"].motion_cost == 12
    assert by_kind["upstream_target_change"].motion_cost == 7


def main() -> None:
    run_checks()
    branches = build_cycle_branches()
    state = SearchState(
        state_id="S0_empty",
        selected_pair=None,
        last_policy_name=None,
        last_branch_kind=None,
        last_change_axes=None,
        realized_transition_history=(),
    )
    print("[history-aware cycle]")
    for index in range(2):
        selection, decision, next_state = run_cycle(state, branches)
        print(
            f"step={index} state={state.state_id} "
            f"policy={selection.policy.name}"
        )
        print(
            f"  reason={selection.reason} "
            f"selected={decision.selected_branch_kind}"
        )
        print(
            f"  next_state={next_state.state_id} "
            f"pair={next_state.realized_transition_history[-1].resulting_pair}"
        )
        state = next_state
    next_selection = select_policy(state)
    print(
        f"next_policy_after_stop={next_selection.policy.name} "
        f"reason={next_selection.reason}"
    )


if __name__ == "__main__":
    main()
