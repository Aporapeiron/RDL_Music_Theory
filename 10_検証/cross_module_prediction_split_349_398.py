"""四Module相互作用面で予測分岐と複数解釈保持を検査する最小実験。"""

from dataclasses import dataclass

from cross_module_interaction_stress_299_348 import (
    observe_cross_module_interaction_stress,
)
from next_key_context_after_voice_leading_boundary import (
    NextContextCandidate,
    VoiceLeadingResult,
    fixture_next_context_candidates,
    observe_next_context,
    voice_leading_result_from_44,
)
from rhythm_spiral_transfer_239_248 import observe_rhythm_spiral_transfer


@dataclass(frozen=True)
class PredictionSplitStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class PredictionFrameCandidate:
    label: str
    next_context: NextContextCandidate
    harmonic_reading: str
    rhythm_alignment: str
    prediction: str
    source: str


@dataclass(frozen=True)
class PredictionSplitObservation:
    source_status: str
    steps: tuple[PredictionSplitStep, ...]
    voice_leading_result: VoiceLeadingResult
    prediction_candidates: tuple[PredictionFrameCandidate, ...]
    selected_prediction: PredictionFrameCandidate | None
    retained_alternatives: tuple[PredictionFrameCandidate, ...]
    split_point: str
    prediction_split_preserved: bool
    multiple_interpretation_retained: bool
    unique_prediction_without_policy: bool
    external_policy_required: bool
    treats_prediction_as_resolution: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (349, "source_reentry", "reuse_299_348_interaction_stress", "interaction_stress_result_preserved"),
    (350, "source_reentry", "next_xi_received", "interval_to_harmonic_target_context_stress_received"),
    (351, "source_reentry", "music_interaction_not_unified_guard", "interaction_unification_still_blocked"),
    (352, "prediction_request", "prediction_surface_request", "prediction_surface_candidate"),
    (353, "prediction_request", "same_evidence_bundle_projection", "shared_evidence_bundle_observed"),
    (354, "prediction_request", "voice_leading_result_reuse", "E4_C5_result_reused_without_context_generation"),
    (355, "prediction_request", "rhythm_regeneration_reuse", "rhythm_candidate_regeneration_reused_as_timing_evidence"),
    (356, "candidate_set", "next_context_fixture_reuse", "next_context_candidate_set_reused"),
    (357, "candidate_set", "continuation_frame_candidate", "C_major_continuation_prediction_candidate"),
    (358, "candidate_set", "reinterpretation_frame_candidate", "A_minor_reinterpretation_prediction_candidate"),
    (359, "candidate_set", "same_concrete_pair_supports_two_frames", "same_pair_multiple_context_support_observed"),
    (360, "candidate_set", "rhythm_alignment_does_not_remove_split", "rhythm_alignment_split_preserved"),
    (361, "split_point", "harmonic_target_context_split", "target_context_prediction_split_observed"),
    (362, "split_point", "spelling_context_memory_split", "spelling_context_memory_difference_preserved"),
    (363, "split_point", "voice_context_branching", "voice_context_branching_preserved"),
    (364, "split_point", "rhythm_harmonic_timing_branching", "rhythm_harmonic_branching_preserved"),
    (365, "split_point", "prediction_not_function_generation_guard", "prediction_function_generation_blocked"),
    (366, "underdetermination", "observe_without_policy", "prediction_underdetermined_without_policy"),
    (367, "underdetermination", "multiple_prediction_count_check", "multiple_predictions_retained"),
    (368, "underdetermination", "no_unique_forecast_guard", "unique_forecast_not_available"),
    (369, "underdetermination", "no_auto_resolution_guard", "auto_resolution_blocked"),
    (370, "policy_boundary", "external_policy_boundary_request", "external_prediction_policy_required"),
    (371, "policy_boundary", "continuation_policy_application", "continuation_prediction_selected"),
    (372, "policy_boundary", "alternative_retention_after_selection", "unselected_alternative_retained"),
    (373, "policy_boundary", "selection_not_generation_guard", "selection_generation_non_identity"),
    (374, "prediction_content", "continuation_prediction_reading", "tonic_continuation_prediction_read"),
    (375, "prediction_content", "reinterpretation_prediction_reading", "relative_minor_reinterpretation_prediction_read"),
    (376, "prediction_content", "same_evidence_different_future_reading", "future_reading_divergence_preserved"),
    (377, "prediction_content", "same_target_different_context_guard", "target_context_non_identity_preserved"),
    (378, "non_confluent", "prediction_split_not_error_guard", "prediction_split_not_classified_as_failure"),
    (379, "non_confluent", "prediction_split_not_Core_guard", "prediction_split_not_promoted_to_Core"),
    (380, "non_confluent", "prediction_split_not_unified_Module_guard", "prediction_split_not_unified_Module"),
    (381, "non_confluent", "music_specific_ambiguity_record", "music_specific_ambiguity_preserved"),
    (382, "relation_grid", "tuning_interval_prediction_edge", "tuning_interval_prediction_edge_recorded"),
    (383, "relation_grid", "interval_harmonic_prediction_edge", "interval_harmonic_prediction_edge_recorded"),
    (384, "relation_grid", "harmonic_context_prediction_edge", "harmonic_context_prediction_edge_recorded"),
    (385, "relation_grid", "rhythm_harmonic_prediction_edge", "rhythm_harmonic_prediction_edge_recorded"),
    (386, "relation_grid", "non_edge_direct_rhythm_interval_prediction", "direct_rhythm_interval_prediction_blocked"),
    (387, "relation_grid", "non_edge_tuning_harmonic_prediction", "direct_tuning_harmonic_prediction_blocked"),
    (388, "difference_retention", "contextual_difference_retention", "contextual_difference_retained"),
    (389, "difference_retention", "harmonic_reading_difference_retention", "harmonic_reading_difference_retained"),
    (390, "difference_retention", "rhythm_alignment_difference_retention", "rhythm_alignment_difference_retained"),
    (391, "difference_retention", "future_prediction_difference_retention", "future_prediction_difference_retained"),
    (392, "summary", "prediction_surface_summary", "prediction_surface_observed"),
    (393, "summary", "multiple_interpretation_summary", "multiple_interpretation_retained"),
    (394, "summary", "external_policy_summary", "external_policy_required_for_selection"),
    (395, "summary", "no_mutation_summary", "no_mutation_generated"),
    (396, "next_plan", "single_pair_deeper_stress_readiness", "single_pair_deeper_stress_ready"),
    (397, "next_plan", "Core_side_path_record", "Core_side_path_recorded_but_not_taken"),
    (398, "next_plan", "next_xi_selection", "xi_prediction_split_resolution_policy_stress"),
)


def _build_steps() -> tuple[PredictionSplitStep, ...]:
    previous = "cross_module_interaction_stress_299_348"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            PredictionSplitStep(
                number=number,
                phase=phase,
                name=name,
                source=previous,
                result=result,
                generated_mutation=False,
            )
        )
        previous = result
    return tuple(steps)


def build_prediction_candidates(
    voice_leading_result: VoiceLeadingResult,
    next_context_candidates: tuple[NextContextCandidate, ...],
) -> tuple[PredictionFrameCandidate, ...]:
    if voice_leading_result.concrete_target_pair != ("E4", "C5"):
        raise ValueError("this fixture only covers the E4-C5 realization")

    by_label = {candidate.label: candidate for candidate in next_context_candidates}
    return (
        PredictionFrameCandidate(
            label="C major continuation frame",
            next_context=by_label["C major continuation"],
            harmonic_reading="tonic_continuation",
            rhythm_alignment="arrival_can_be_grid_aligned",
            prediction="continue_C_major_context",
            source="continuation_fixture",
        ),
        PredictionFrameCandidate(
            label="A minor reinterpretation frame",
            next_context=by_label["A minor reinterpretation"],
            harmonic_reading="relative_minor_reinterpretation",
            rhythm_alignment="arrival_can_be_reaccented",
            prediction="reinterpret_as_A_minor_context",
            source="reinterpretation_fixture",
        ),
    )


def observe_prediction_split(
    selection_policy: str | None = None,
) -> PredictionSplitObservation:
    interaction = observe_cross_module_interaction_stress()
    voice_leading_result = voice_leading_result_from_44()
    next_context_candidates = fixture_next_context_candidates()
    prediction_candidates = build_prediction_candidates(
        voice_leading_result,
        next_context_candidates,
    )
    rhythm = observe_rhythm_spiral_transfer()
    next_context = observe_next_context(
        voice_leading_result,
        next_context_candidates,
        selection_policy=selection_policy,
    )

    selected_prediction = None
    if next_context.selected is not None:
        selected_prediction = next(
            candidate
            for candidate in prediction_candidates
            if candidate.next_context.label == next_context.selected.label
        )

    retained_alternatives = tuple(
        candidate
        for candidate in prediction_candidates
        if candidate != selected_prediction
    )
    steps = _build_steps()
    generated_mutation = any(step.generated_mutation for step in steps)

    return PredictionSplitObservation(
        source_status=interaction.status,
        steps=steps,
        voice_leading_result=voice_leading_result,
        prediction_candidates=prediction_candidates,
        selected_prediction=selected_prediction,
        retained_alternatives=retained_alternatives,
        split_point="target_context_prediction_surface",
        prediction_split_preserved=(
            len(prediction_candidates) == 2
            and {candidate.prediction for candidate in prediction_candidates}
            == {"continue_C_major_context", "reinterpret_as_A_minor_context"}
        ),
        multiple_interpretation_retained=(
            selected_prediction is None and len(retained_alternatives) == 2
        )
        or (selected_prediction is not None and len(retained_alternatives) == 1),
        unique_prediction_without_policy=(selection_policy is None and len(prediction_candidates) == 1),
        external_policy_required=(next_context.status == "underdetermined")
        if selection_policy is None
        else (next_context.status == "selected_next_context"),
        treats_prediction_as_resolution=False,
        generated_mutation=generated_mutation or rhythm.generated_mutation,
        status="cross_module_prediction_split_349_398_observed_without_collapsing_multiple_interpretations",
    )


def run_checks() -> None:
    observation = observe_prediction_split()
    selected = observe_prediction_split(selection_policy="prefer_continuation_fixture")

    assert observation.source_status == (
        "cross_module_interaction_stress_299_348_observed_without_unifying_interaction_surfaces"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 349
    assert observation.steps[-1].number == 398
    assert observation.voice_leading_result.concrete_target_pair == ("E4", "C5")
    assert observation.prediction_split_preserved is True
    assert observation.multiple_interpretation_retained is True
    assert observation.unique_prediction_without_policy is False
    assert observation.external_policy_required is True
    assert observation.selected_prediction is None
    assert len(observation.retained_alternatives) == 2
    assert selected.selected_prediction is not None
    assert selected.selected_prediction.label == "C major continuation frame"
    assert len(selected.retained_alternatives) == 1
    assert selected.retained_alternatives[0].label == "A minor reinterpretation frame"
    assert selected.multiple_interpretation_retained is True
    assert selected.treats_prediction_as_resolution is False
    assert observation.generated_mutation is False
    assert selected.generated_mutation is False
    assert observation.steps[-1].result == "xi_prediction_split_resolution_policy_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_prediction_split().status)
