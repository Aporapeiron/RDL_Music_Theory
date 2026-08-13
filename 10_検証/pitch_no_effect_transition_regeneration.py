"""実差分のない音程fallback recordと候補再生成の関係を検証する。"""

from dataclasses import dataclass

from dynamic_adapter_boundary import project_fallback
from exhaustion_fallback_observation import observe_action_set_exhaustion
from fallback_state_adoption import (
    adopt_reopen_voice_B_boundary,
    build_exhausted_state_without_import_side_effects,
)
from pitch_transition_projection_reconstruction import (
    regenerate_candidate_branches,
    state_after_transition,
)
from reexploration_after_empty import ChangeAxes
from state_rebased_reexploration import (
    DynamicSearchState,
    FallbackStateTransition,
    observe_actions,
)


@dataclass(frozen=True)
class PitchNoEffectRegenerationRun:
    source_state: DynamicSearchState
    transition: FallbackStateTransition
    source_regenerated_pairs: tuple[tuple[str, tuple[str, str]], ...]
    resulting_regenerated_pairs: tuple[tuple[str, tuple[str, str]], ...]


def run_no_effect_regeneration() -> PitchNoEffectRegenerationRun:
    exhausted = build_exhausted_state_without_import_side_effects()
    source_state = adopt_reopen_voice_B_boundary(
        exhausted,
        observe_action_set_exhaustion(exhausted),
    )
    transition = FallbackStateTransition(
        source_state_id=source_state.state_id,
        fallback_kind="reopen_voice_B_boundary",
        outcome_status="candidate_space_unchanged",
        operation_status="no_effect",
        resulting_state_id=source_state.state_id,
        change_axes=ChangeAxes(),
        source_voice_b_boundary=source_state.voice_b_boundary,
        resulting_voice_b_boundary=source_state.voice_b_boundary,
        next_policy_reason="record has no boundary difference; no new policy input",
    )
    source_pairs = tuple(
        (
            item.action.branch_kind,
            (item.observation.selected[0].text, item.observation.selected[1].text),
        )
        for item in observe_actions(source_state)
        if item.observation.selected is not None
    )
    return PitchNoEffectRegenerationRun(
        source_state=source_state,
        transition=transition,
        source_regenerated_pairs=source_pairs,
        resulting_regenerated_pairs=regenerate_candidate_branches(
            source_state,
            transition,
        ),
    )


def run_checks() -> None:
    run = run_no_effect_regeneration()
    event = project_fallback(run.transition)
    resulting = state_after_transition(run.source_state, run.transition)

    assert run.transition.source_voice_b_boundary == run.transition.resulting_voice_b_boundary
    assert run.transition.source_state_id == run.transition.resulting_state_id
    assert event.event_kind == "structural_transition"
    assert event.operation_kind == run.transition.fallback_kind
    assert event.operation_status == "no_effect"
    assert event.change_axes == ()
    assert event.realization_status == "not_realized"
    assert resulting.voice_b_boundary == run.source_state.voice_b_boundary
    assert run.source_regenerated_pairs == run.resulting_regenerated_pairs
    assert run.resulting_regenerated_pairs == (
        ("B_change", ("A♯3", "F♯4")),
        ("upstream_target_change", ("E♯4", "F♯4")),
    )


def main() -> None:
    run_checks()
    run = run_no_effect_regeneration()
    event = project_fallback(run.transition)
    print("[pitch no-effect transition regeneration]")
    print(f"event_kind={event.event_kind} operation_status={event.operation_status}")
    print(f"source_regenerated={run.source_regenerated_pairs}")
    print(f"resulting_regenerated={run.resulting_regenerated_pairs}")


if __name__ == "__main__":
    main()
