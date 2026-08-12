"""同一音程fallback recordを投影と候補再構成へ通す最小検証。

22で採用された ``FallbackStateTransition`` を一度だけ取得し、そのrecordを
24の ``project_fallback`` へ渡す。同時に、recordが保存するvoice B境界の実差分を
同じsource stateへ適用して、19の既存候補生成器から次の有効枝を再生成する。

この検証は共通Adapterや共通状態を作らない。source stateのうち、recordが変更して
いない条件はそのまま保持し、操作名から候補生成条件を推測しない。
"""

from dataclasses import dataclass, replace

from dynamic_adapter_boundary import GenericDynamicEvent, project_fallback
from exhaustion_fallback_observation import observe_action_set_exhaustion
from fallback_state_adoption import (
    adopt_reopen_voice_B_boundary,
    build_exhausted_state_without_import_side_effects,
)
from state_rebased_reexploration import (
    DynamicSearchState,
    FallbackStateTransition,
    observe_actions,
)


@dataclass(frozen=True)
class PitchTransitionProjectionRun:
    transition: FallbackStateTransition
    event: GenericDynamicEvent
    regenerated_branch_kinds: tuple[str, ...]
    regenerated_pairs: tuple[tuple[str, tuple[str, str]], ...]


def state_after_transition(
    source_state: DynamicSearchState,
    transition: FallbackStateTransition,
) -> DynamicSearchState:
    """recordの実差分だけをsource stateへ反映して候補生成条件を復元する。"""

    if source_state.state_id != transition.source_state_id:
        raise ValueError("source state does not match the transition record")
    if source_state.voice_b_boundary != transition.source_voice_b_boundary:
        raise ValueError("source boundary does not match the transition record")

    return replace(
        source_state,
        state_id=transition.resulting_state_id,
        voice_b_boundary=transition.resulting_voice_b_boundary,
        last_change_axes=transition.change_axes,
    )


def regenerate_candidate_branches(
    source_state: DynamicSearchState,
    transition: FallbackStateTransition,
) -> tuple[tuple[str, tuple[str, str]], ...]:
    """同一recordのresulting boundaryで、次の有効な候補枝だけを再観測する。"""

    resulting_state = state_after_transition(source_state, transition)
    return tuple(
        (
            item.action.branch_kind,
            (item.observation.selected[0].text, item.observation.selected[1].text),
        )
        for item in observe_actions(resulting_state)
        if item.observation.selected is not None
    )


def run_same_transition() -> PitchTransitionProjectionRun:
    exhausted = build_exhausted_state_without_import_side_effects()
    reopened = adopt_reopen_voice_B_boundary(
        exhausted,
        observe_action_set_exhaustion(exhausted),
    )
    transition = reopened.fallback_transition_history[-1]
    event = project_fallback(transition)
    regenerated_pairs = regenerate_candidate_branches(exhausted, transition)
    return PitchTransitionProjectionRun(
        transition=transition,
        event=event,
        regenerated_branch_kinds=tuple(kind for kind, _ in regenerated_pairs),
        regenerated_pairs=regenerated_pairs,
    )


def run_checks() -> None:
    run = run_same_transition()

    assert run.transition.fallback_kind == "reopen_voice_B_boundary"
    assert run.transition.operation_status == "applied"
    assert run.transition.change_axes.boundary_changed is True
    assert run.transition.source_voice_b_boundary != run.transition.resulting_voice_b_boundary

    assert run.event.event_kind == "structural_transition"
    assert run.event.operation_kind == run.transition.fallback_kind
    assert run.event.operation_status == run.transition.operation_status
    assert run.event.change_axes == ("boundary_changed",)
    assert run.event.realization_status == "not_realized"

    assert run.regenerated_branch_kinds == (
        "B_change",
        "upstream_target_change",
    )
    assert run.regenerated_pairs == (
        ("B_change", ("A♯3", "F♯4")),
        ("upstream_target_change", ("E♯4", "F♯4")),
    )


def main() -> None:
    run_checks()
    run = run_same_transition()
    print("[pitch transition projection reconstruction]")
    print(
        f"operation={run.transition.fallback_kind} "
        f"event={run.event.event_kind} "
        f"axes={run.event.change_axes}"
    )
    print(f"regenerated={run.regenerated_pairs}")


if __name__ == "__main__":
    main()
