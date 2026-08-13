"""DynamicSearchStateの用途別比較用projection。"""

from dataclasses import dataclass

from state_rebased_reexploration import DynamicSearchState


@dataclass(frozen=True)
class StateSignatures:
    candidate_generation: tuple[object, ...]
    controller: tuple[object, ...]
    history: tuple[object, ...]


def observe_signatures(state: DynamicSearchState) -> StateSignatures:
    """既存stateを変更せず、既存利用者ごとの入力断面を取り出す。"""

    return StateSignatures(
        candidate_generation=(
            state.context,
            state.last_realized_pair,
            state.voice_a_target_degree,
            state.voice_b_target_degree,
            state.voice_a_boundary,
            state.voice_b_boundary,
            state.pitch_ordering_rule,
        ),
        controller=(
            state.last_policy_name,
            state.last_branch_kind,
            state.last_change_axes,
            state.realized_transition_history,
        ),
        history=(
            state.realized_transition_history,
            state.observation_history,
            state.fallback_transition_history,
        ),
    )


def same_for_candidate_generation(left: DynamicSearchState, right: DynamicSearchState) -> bool:
    return observe_signatures(left).candidate_generation == observe_signatures(right).candidate_generation


def same_for_controller(left: DynamicSearchState, right: DynamicSearchState) -> bool:
    return observe_signatures(left).controller == observe_signatures(right).controller


def same_for_history(left: DynamicSearchState, right: DynamicSearchState) -> bool:
    return observe_signatures(left).history == observe_signatures(right).history
