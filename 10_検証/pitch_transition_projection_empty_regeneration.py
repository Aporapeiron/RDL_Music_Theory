"""実差分を持つ同一音程fallback recordが、空の再生成へ接続する最小検証。

31で分離した通り、構造遷移recordからの再生成接続と、候補が非空になることは
別の事実である。ここではvoice B境界をF4からG4へ変える同一recordを投影と
再生成へ通し、操作がappliedでも三つの既存再探索枝が空のまま残ることを確認する。
"""

from dataclasses import dataclass

from degree_to_pitch_realization import RealizationBoundary, SpelledNote, VoiceRange
from dynamic_adapter_boundary import project_fallback
from fallback_state_adoption import (
    build_exhausted_state_without_import_side_effects,
)
from pitch_transition_projection_reconstruction import state_after_transition
from reexploration_after_empty import ChangeAxes
from state_rebased_reexploration import (
    ActionObservation,
    DynamicSearchState,
    FallbackStateTransition,
    observe_actions,
)


@dataclass(frozen=True)
class PitchEmptyRegenerationRun:
    transition: FallbackStateTransition
    observations: tuple[ActionObservation, ...]


def build_empty_regeneration_transition(
) -> tuple[DynamicSearchState, FallbackStateTransition]:
    source = build_exhausted_state_without_import_side_effects()
    resulting_boundary = RealizationBoundary(
        candidate_octaves=(4,),
        voice_range=VoiceRange(
            SpelledNote("G", octave=4),
            SpelledNote("G", octave=4),
        ),
    )
    transition = FallbackStateTransition(
        source_state_id=source.state_id,
        fallback_kind="shift_voice_B_boundary_to_G4",
        outcome_status="candidate_space_still_empty",
        operation_status="applied",
        resulting_state_id=f"{source.state_id}->voice_B_boundary_G4",
        change_axes=ChangeAxes(boundary_changed=True),
        source_voice_b_boundary=source.voice_b_boundary,
        resulting_voice_b_boundary=resulting_boundary,
        next_policy_reason="recorded boundary difference is applied before re-observation",
    )
    return source, transition


def run_empty_regeneration() -> PitchEmptyRegenerationRun:
    source, transition = build_empty_regeneration_transition()
    resulting = state_after_transition(source, transition)
    return PitchEmptyRegenerationRun(
        transition=transition,
        observations=tuple(observe_actions(resulting)),
    )


def run_checks() -> None:
    source, transition = build_empty_regeneration_transition()
    event = project_fallback(transition)
    resulting = state_after_transition(source, transition)
    run = run_empty_regeneration()
    observations = run.observations

    assert transition.source_voice_b_boundary != transition.resulting_voice_b_boundary
    assert transition.operation_status == "applied"
    assert event.event_kind == "structural_transition"
    assert event.operation_kind == transition.fallback_kind
    assert event.realization_status == "not_realized"
    assert resulting.voice_b_boundary == transition.resulting_voice_b_boundary
    assert len(observations) == 3
    assert all(item.observation.selected is None for item in observations)
    assert all(item.observation.status == "constraint_no_candidate" for item in observations)
    assert all(item.evaluation is None for item in observations)


def main() -> None:
    run_checks()
    run = run_empty_regeneration()
    transition = run.transition
    observations = run.observations
    print("[pitch transition projection with empty regeneration]")
    print(f"operation={transition.fallback_kind} event={project_fallback(transition).event_kind}")
    print(f"regeneration_status=executed regenerated_count=0")
    print(f"observation_statuses={tuple(item.observation.status for item in observations)}")


if __name__ == "__main__":
    main()
