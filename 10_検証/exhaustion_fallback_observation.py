"""列挙済みaction setがemptyになった後のfallback outcomeを観測する最小検証。

20では、操作後のemptyを観測履歴へ保持し、別操作による再探索を続けた。
21では、同一source stateから独立に評価した
B_change・Γ_change・upstream_target_changeの全てがemptyになる候補枯渇状態を作り、
その後のfallback outcomeを同じ採用結果へ潰さずに記録する。

    current action set exhausted
      ├─ stop_search
      ├─ reopen_voice_B_boundary -> candidate space reopens
      └─ discard_target          -> target is abandoned without fabricating a pair

これは探索方針の一般則を決める実験ではなく、候補枯渇後に異なる層を
操作したときの帰結を、検証Module内で比較可能にするための構造である。
"""

from dataclasses import dataclass, replace

from degree_to_pitch_realization import RealizationBoundary, SpelledNote, VoiceRange
from empty_action_observation import EMPTY_ACTION, apply_empty_action
from history_aware_reexploration_cycle import select_policy
from state_rebased_reexploration import (
    ACTIONS,
    ActionAttemptRecord,
    ActionObservation,
    DynamicSearchState,
    StateAction,
    advance_empty_observation,
    build_initial_state,
    observe_actions,
    observe_resulting_state,
)


VOICE_B_BOUNDARY_TIGHTEN = StateAction(
    branch_kind="voice_B_boundary_tighten",
    change_layer="realization_layer",
    description="close voice B range so every voice B candidate is removed",
)


UNRESOLVED_XI = (
    "which fallback should be selected after the enumerated action set is exhausted",
    "whether voice-B boundary reopening is allowed by the surrounding boundary",
    "what concrete successor state exists after discarding the target",
)


@dataclass(frozen=True)
class ExhaustionObservation:
    """列挙済みaction setの独立評価結果を、単一の失敗値へ潰さずに保持する。"""

    source_state_id: str
    enumerated_branch_kinds: tuple[str, ...]
    empty_branch_kinds: tuple[str, ...]
    observations: tuple[ActionObservation, ...]

    @property
    def all_enumerated_actions_empty(self) -> bool:
        return bool(self.enumerated_branch_kinds) and (
            self.enumerated_branch_kinds == self.empty_branch_kinds
        )


@dataclass(frozen=True)
class FallbackOutcomeObservation:
    """枯渇後のfallback outcomeを観測する。

    これは`DynamicSearchState`の次状態ではない。各fallbackを同じsource
    stateから見たときに、何が変わり、何が未観測のまま残るかを記録する。
    """

    fallback_kind: str
    outcome_status: str
    source_state_id: str
    outcome_reference_id: str
    target_status: str
    reopened_candidate_branch_kinds: tuple[str, ...]
    selected_branch_kind: str | None
    realized_transition_count: int
    observation_history_count: int
    unresolved_xi: tuple[str, ...]


def close_voice_B_boundary(state: DynamicSearchState) -> DynamicSearchState:
    """voice B側の境界を閉じ、三つの既存操作でも候補を戻せなくする。"""

    return replace(
        state,
        voice_b_boundary=RealizationBoundary(
            candidate_octaves=(4,),
            voice_range=VoiceRange(
                SpelledNote("F", octave=4),
                SpelledNote("F", octave=4),
            ),
        ),
    )


def reopen_voice_B_boundary_state(state: DynamicSearchState) -> DynamicSearchState:
    """voice Bの候補境界を再開する。上位B層への退避はまだ扱わない。"""

    return replace(
        state,
        voice_b_boundary=RealizationBoundary(
            candidate_octaves=(4,),
            voice_range=VoiceRange(
                SpelledNote("F", accidental=1, octave=4),
                SpelledNote("F", accidental=1, octave=4),
            ),
        ),
    )


def _record_observation(item: ActionObservation) -> ActionAttemptRecord:
    selected = item.observation.selected
    return ActionAttemptRecord(
        source_state_id=item.source_state_id,
        branch_kind=item.action.branch_kind,
        operation_status=item.operation_status,
        observation_status=item.observation.status,
        change_axes=item.change_axes,
        selected_pair=(selected[0].text, selected[1].text)
        if selected is not None
        else None,
        failure_stage=item.observation.failure_stage,
        failure_reason=item.observation.failure_reason,
    )


def build_exhausted_state() -> DynamicSearchState:
    """20のemptyから、voice B境界も閉じたaction-set枯渇状態へ進める。"""

    initial = build_initial_state()
    first_selection = select_policy(initial)
    first_observation = observe_resulting_state(
        initial,
        EMPTY_ACTION,
        apply_empty_action(initial),
    )
    state_1 = advance_empty_observation(
        initial,
        first_selection,
        first_observation,
    )

    upper_observation = observe_resulting_state(
        state_1,
        VOICE_B_BOUNDARY_TIGHTEN,
        close_voice_B_boundary(state_1),
    )
    state_2 = advance_empty_observation(
        state_1,
        select_policy(state_1),
        upper_observation,
    )

    observations = observe_actions(state_2)
    assert all(item.observation.selected is None for item in observations)
    assert all(item.evaluation is None for item in observations)
    return replace(
        state_2,
        state_id=f"{state_2.state_id}->action_set_exhausted",
        observation_history=state_2.observation_history
        + tuple(_record_observation(item) for item in observations),
    )


def observe_action_set_exhaustion(state: DynamicSearchState) -> ExhaustionObservation:
    """同一source stateから列挙した各再探索枝を独立に評価する。"""

    observations = observe_actions(state)
    enumerated = tuple(action.branch_kind for action in ACTIONS)
    empty = tuple(
        item.action.branch_kind
        for item in observations
        if item.observation.selected is None
    )
    result = ExhaustionObservation(
        source_state_id=state.state_id,
        enumerated_branch_kinds=enumerated,
        empty_branch_kinds=empty,
        observations=observations,
    )
    assert result.all_enumerated_actions_empty
    return result


def stop_search(
    state: DynamicSearchState,
    exhaustion: ExhaustionObservation,
) -> FallbackOutcomeObservation:
    return FallbackOutcomeObservation(
        fallback_kind="stop_search",
        outcome_status="stopped",
        source_state_id=exhaustion.source_state_id,
        outcome_reference_id=f"{state.state_id}->stop_search_outcome",
        target_status="active",
        reopened_candidate_branch_kinds=(),
        selected_branch_kind=None,
        realized_transition_count=len(state.realized_transition_history),
        observation_history_count=len(state.observation_history),
        unresolved_xi=UNRESOLVED_XI,
    )


def reopen_voice_B_boundary(
    state: DynamicSearchState,
    exhaustion: ExhaustionObservation,
) -> FallbackOutcomeObservation:
    reopened = reopen_voice_B_boundary_state(state)
    observations = observe_actions(reopened)
    recovered = tuple(
        item.action.branch_kind
        for item in observations
        if item.observation.selected is not None
    )
    assert recovered == ("B_change", "upstream_target_change")
    return FallbackOutcomeObservation(
        fallback_kind="reopen_voice_B_boundary",
        outcome_status="candidate_space_reopened",
        source_state_id=exhaustion.source_state_id,
        outcome_reference_id=f"{state.state_id}->voice_B_boundary_reopened_outcome",
        target_status="active",
        reopened_candidate_branch_kinds=recovered,
        selected_branch_kind=None,
        realized_transition_count=len(state.realized_transition_history),
        observation_history_count=len(state.observation_history),
        unresolved_xi=UNRESOLVED_XI,
    )


def discard_target(
    state: DynamicSearchState,
    exhaustion: ExhaustionObservation,
) -> FallbackOutcomeObservation:
    """targetを捨てるが、代替targetや具体音を自動生成しない。"""

    return FallbackOutcomeObservation(
        fallback_kind="discard_target",
        outcome_status="target_discarded",
        source_state_id=exhaustion.source_state_id,
        outcome_reference_id=f"{state.state_id}->target_discarded_outcome",
        target_status="discarded",
        reopened_candidate_branch_kinds=(),
        selected_branch_kind=None,
        realized_transition_count=len(state.realized_transition_history),
        observation_history_count=len(state.observation_history),
        unresolved_xi=UNRESOLVED_XI,
    )


def run_checks() -> None:
    exhausted = build_exhausted_state()
    exhaustion = observe_action_set_exhaustion(exhausted)

    assert exhaustion.enumerated_branch_kinds == (
        "B_change",
        "Γ_change",
        "upstream_target_change",
    )
    assert exhaustion.empty_branch_kinds == exhaustion.enumerated_branch_kinds
    assert exhaustion.all_enumerated_actions_empty
    assert all(
        item.observation.failure_stage == "B_range_projection"
        for item in exhaustion.observations
    )
    assert len(exhausted.realized_transition_history) == 0
    assert len(exhausted.observation_history) == 5

    stopped = stop_search(exhausted, exhaustion)
    assert stopped.outcome_status == "stopped"
    assert stopped.selected_branch_kind is None
    assert stopped.realized_transition_count == 0

    reopened = reopen_voice_B_boundary(exhausted, exhaustion)
    assert reopened.outcome_status == "candidate_space_reopened"
    assert reopened.fallback_kind == "reopen_voice_B_boundary"
    assert reopened.reopened_candidate_branch_kinds == (
        "B_change",
        "upstream_target_change",
    )
    assert reopened.selected_branch_kind is None
    assert reopened.realized_transition_count == 0

    discarded = discard_target(exhausted, exhaustion)
    assert discarded.outcome_status == "target_discarded"
    assert discarded.target_status == "discarded"
    assert discarded.reopened_candidate_branch_kinds == ()
    assert discarded.realized_transition_count == 0
    assert "what concrete successor state exists after discarding the target" in discarded.unresolved_xi


def main() -> None:
    run_checks()
    state = build_exhausted_state()
    exhaustion = observe_action_set_exhaustion(state)
    print("[enumerated action-set exhaustion fallback observation]")
    print(
        f"state={state.state_id} enumerated={exhaustion.enumerated_branch_kinds} "
        f"empty={exhaustion.empty_branch_kinds}"
    )
    for result in (
        stop_search(state, exhaustion),
        reopen_voice_B_boundary(state, exhaustion),
        discard_target(state, exhaustion),
    ):
        print(
            f"fallback={result.fallback_kind} status={result.outcome_status} "
            f"reopened={result.reopened_candidate_branch_kinds} "
            f"target={result.target_status}"
        )


if __name__ == "__main__":
    main()
