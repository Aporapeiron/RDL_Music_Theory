"""no_effect fallback recordの候補再構成とcontroller入力を分けて観測する。"""

from dataclasses import dataclass

from exhaustion_fallback_observation import observe_action_set_exhaustion
from fallback_state_adoption import (
    adopt_reopen_voice_B_boundary,
    build_exhausted_state_without_import_side_effects,
)
from history_aware_reexploration_cycle import select_policy
from pitch_no_effect_transition_regeneration import run_no_effect_regeneration
from pitch_transition_projection_reconstruction import state_after_transition
from reexploration_after_empty import ChangeAxes
from state_rebased_reexploration import DynamicSearchState
from state_signature_views import same_for_candidate_generation


@dataclass(frozen=True)
class NoEffectControllerBoundaryRun:
    source_state: DynamicSearchState
    resulting_state: DynamicSearchState
    source_policy_name: str
    resulting_policy_name: str


def run_controller_boundary() -> NoEffectControllerBoundaryRun:
    """候補再構成用stateがcontroller入力まで再構成しないことを確認する。"""

    no_effect = run_no_effect_regeneration()
    source_state = no_effect.source_state
    resulting_state = state_after_transition(source_state, no_effect.transition)
    return NoEffectControllerBoundaryRun(
        source_state=source_state,
        resulting_state=resulting_state,
        source_policy_name=select_policy(source_state).policy.name,
        resulting_policy_name=select_policy(resulting_state).policy.name,
    )


def _candidate_generation_inputs(
    state: DynamicSearchState,
) -> tuple[object, ...]:
    """19のobserve_actionsへ渡る入力だけを明示して比較する。"""

    return (
        state.context,
        state.last_realized_pair,
        state.voice_a_target_degree,
        state.voice_b_target_degree,
        state.voice_a_boundary,
        state.voice_b_boundary,
        state.pitch_ordering_rule,
    )


def run_checks() -> None:
    run = run_controller_boundary()
    no_effect = run_no_effect_regeneration()

    # no_effect recordの前後で候補生成入力は同じである。
    assert run.source_state.state_id == run.resulting_state.state_id
    assert same_for_candidate_generation(run.source_state, run.resulting_state)

    # 用途別同一性は比較用であり、record由来の再生成処理は省略しない。
    assert no_effect.source_regenerated_pairs == no_effect.resulting_regenerated_pairs
    assert no_effect.transition.source_state_id == run.source_state.state_id

    # しかしrecord由来のlast_change_axesはcontrollerが読む別入力である。
    assert run.source_state.last_change_axes == ChangeAxes(boundary_changed=True)
    assert run.resulting_state.last_change_axes == ChangeAxes()
    assert run.source_policy_name == "strict_relation_then_boundary"
    assert run.resulting_policy_name == "target_continuity_then_relation"

    # state_after_transitionは候補再構成用であり、record採用履歴を追加しない。
    assert run.source_state.fallback_transition_history == (
        run.resulting_state.fallback_transition_history
    )
    assert len(run.resulting_state.fallback_transition_history) == 1

    # この比較のsourceは実際に22で採用済みの境界再開状態である。
    exhausted = build_exhausted_state_without_import_side_effects()
    reopened = adopt_reopen_voice_B_boundary(
        exhausted,
        observe_action_set_exhaustion(exhausted),
    )
    assert reopened.state_id == run.source_state.state_id


def main() -> None:
    run_checks()
    run = run_controller_boundary()
    print("[pitch no-effect controller boundary]")
    print(f"candidate_generation_inputs_same=True state_id={run.source_state.state_id}")
    print(
        "controller_policy="
        f"{run.source_policy_name} -> {run.resulting_policy_name}"
    )
    print(
        "fallback_history_length="
        f"{len(run.source_state.fallback_transition_history)}"
    )


if __name__ == "__main__":
    main()
