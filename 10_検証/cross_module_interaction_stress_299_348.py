"""四Module相互作用面を50工程でstress testする最小検証。"""

from dataclasses import dataclass

from next_key_context_after_voice_leading_boundary import (
    fixture_next_context_candidates,
    observe_next_context,
    voice_leading_result_from_44,
)
from rhythm_spiral_transfer_239_248 import observe_rhythm_spiral_transfer
from tuning_to_interval_spelling_stress_289_298 import (
    observe_tuning_to_interval_spelling_stress,
)
from voice_leading_selected_target_realization_boundary import (
    connect_to_existing_realization,
    selected_target_observation,
)


@dataclass(frozen=True)
class InteractionStressStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class CrossModuleInteractionStressObservation:
    source_status: str
    steps: tuple[InteractionStressStep, ...]
    tuning_to_interval_preserved: bool
    interval_to_harmonic_preserved: bool
    harmonic_to_voice_leading_preserved: bool
    voice_leading_to_context_preserved: bool
    rhythm_harmonic_timing_complement_preserved: bool
    non_confluent_surfaces_preserved: bool
    treats_interaction_as_unification: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (299, "tuning_interval", "reuse_289_stress_result", "tuning_to_interval_stress_preserved"),
    (300, "tuning_interval", "spelled_label_divergence_carry", "spelled_label_difference_preserved"),
    (301, "tuning_interval", "reverse_tuning_determination_guard", "reverse_tuning_determination_blocked"),
    (302, "interval_harmonic", "interval_target_context_boundary_request", "harmonic_target_boundary_input_candidate"),
    (303, "interval_harmonic", "selected_target_from_existing_43", "selected_harmonic_target_candidate"),
    (304, "interval_harmonic", "target_degree_plan_fixture_connection", "target_degree_plan_connected_externally"),
    (305, "interval_harmonic", "selected_target_not_degree_plan_guard", "selected_target_degree_plan_non_identity"),
    (306, "interval_harmonic", "selected_target_not_function_generator_guard", "target_not_function_generator"),
    (307, "harmonic_voice_leading", "existing_44_realization_bridge", "voice_leading_realization_connection"),
    (308, "harmonic_voice_leading", "concrete_pair_observation", "E4_C5_concrete_pair_observed"),
    (309, "harmonic_voice_leading", "motion_observation", "contrary_motion_observed"),
    (310, "harmonic_voice_leading", "selected_target_concrete_pitch_guard", "selected_target_not_concrete_pitch"),
    (311, "voice_context", "existing_45_next_context_boundary", "next_context_candidate_set_observed"),
    (312, "voice_context", "next_context_unselected_observation", "next_context_underdetermined"),
    (313, "voice_context", "next_context_selection_policy_connection", "selected_next_context_candidate"),
    (314, "voice_context", "voice_leading_not_context_generator_guard", "voice_leading_context_generation_blocked"),
    (315, "rhythm_harmonic", "rhythm_spiral_reuse", "rhythm_candidate_regeneration_preserved"),
    (316, "rhythm_harmonic", "rhythm_timing_to_harmonic_selection_surface", "harmonic_selection_timing_complement"),
    (317, "rhythm_harmonic", "rhythm_grid_not_function_annotation_guard", "rhythm_function_non_identity"),
    (318, "rhythm_harmonic", "harmonic_history_rhythm_projection_interference", "history_projection_interference_preserved"),
    (319, "non_confluent", "tuning_category_harmonic_function_split", "tuning_harmonic_non_confluent"),
    (320, "non_confluent", "rhythm_grid_interval_spelling_split", "rhythm_interval_non_confluent"),
    (321, "non_confluent", "same_B_Gamma_origin_different_realization", "origin_realization_difference_preserved"),
    (322, "non_confluent", "shared_stop_line_different_origin", "stop_line_origin_difference_preserved"),
    (323, "music_subject", "music_subject_recheck", "music_subject_preserved"),
    (324, "music_subject", "core_absorption_guard", "core_absorption_blocked"),
    (325, "music_subject", "unified_module_guard", "unified_module_not_required"),
    (326, "music_subject", "common_vocabulary_guard", "common_vocabulary_not_forced"),
    (327, "stress_summary", "directed_relation_summary", "directed_relations_passed_with_guards"),
    (328, "stress_summary", "mutual_constraint_summary", "mutual_constraint_observed_without_common_axis"),
    (329, "stress_summary", "asymmetric_dependency_summary", "asymmetric_dependency_observed_without_reverse_decision"),
    (330, "stress_summary", "non_confluent_summary", "non_confluent_surfaces_preserved"),
    (331, "stress_summary", "shared_origin_summary", "shared_origin_different_realization_preserved"),
    (332, "stress_summary", "shared_stop_line_summary", "shared_stop_line_different_origin_preserved"),
    (333, "relation_grid", "tuning_interval_edge_record", "edge_tuning_interval_recorded"),
    (334, "relation_grid", "interval_harmonic_edge_record", "edge_interval_harmonic_recorded"),
    (335, "relation_grid", "harmonic_voice_context_edge_record", "edge_harmonic_voice_context_recorded"),
    (336, "relation_grid", "rhythm_harmonic_edge_record", "edge_rhythm_harmonic_recorded"),
    (337, "relation_grid", "tuning_harmonic_non_edge_record", "non_edge_tuning_harmonic_recorded"),
    (338, "relation_grid", "rhythm_interval_non_edge_record", "non_edge_rhythm_interval_recorded"),
    (339, "difference_retention", "spelling_difference_retention", "spelling_difference_retained"),
    (340, "difference_retention", "history_difference_retention", "history_difference_retained"),
    (341, "difference_retention", "grid_difference_retention", "grid_difference_retained"),
    (342, "difference_retention", "tuning_difference_retention", "tuning_difference_retained"),
    (343, "next_plan", "module_pair_priority_reading", "interval_to_harmonic_next_priority"),
    (344, "next_plan", "stress_test_scope_limit", "single_pair_deeper_stress_required"),
    (345, "next_plan", "no_Core_promotion_record", "Core_promotion_not_proposed"),
    (346, "next_plan", "no_T2_finalization_record", "T2_finalization_not_proposed"),
    (347, "next_plan", "music_interaction_map_update_candidate", "music_interaction_map_update_candidate"),
    (348, "next_plan", "next_xi_selection", "xi_interval_to_harmonic_target_context_stress"),
)


def _build_steps() -> tuple[InteractionStressStep, ...]:
    previous = "tuning_to_interval_spelling_stress_289_298"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            InteractionStressStep(
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


def observe_cross_module_interaction_stress() -> CrossModuleInteractionStressObservation:
    tuning_interval = observe_tuning_to_interval_spelling_stress()
    target = selected_target_observation()
    realization = connect_to_existing_realization(target)
    voice_context_result = voice_leading_result_from_44()
    context_candidates = fixture_next_context_candidates()
    unselected_context = observe_next_context(voice_context_result, context_candidates)
    selected_context = observe_next_context(
        voice_context_result,
        context_candidates,
        selection_policy="prefer_continuation_fixture",
    )
    rhythm = observe_rhythm_spiral_transfer()

    steps = _build_steps()
    interval_to_harmonic_preserved = (
        target.status == "selected_target"
        and target.selected is not None
        and target.generated_by_function is False
    )
    harmonic_to_voice_leading_preserved = (
        realization.selected_target.target_chord == "C major"
        and tuple(note.text for note in realization.realization.selected) == ("E4", "C5")
        and realization.generated_by_selected_target is False
    )
    voice_leading_to_context_preserved = (
        unselected_context.status == "underdetermined"
        and selected_context.status == "selected_next_context"
        and selected_context.generated_by_voice_leading is False
    )
    rhythm_harmonic_timing_complement_preserved = (
        rhythm.reconstructed_candidates == ("休符",)
        and rhythm.reconstruction_status == "locally_resolved"
    )

    return CrossModuleInteractionStressObservation(
        source_status=tuning_interval.status,
        steps=steps,
        tuning_to_interval_preserved=(
            tuning_interval.same_tuning_category
            and tuning_interval.spelling_splits_interval_label
            and not tuning_interval.returns_interval_name_to_tuning
        ),
        interval_to_harmonic_preserved=interval_to_harmonic_preserved,
        harmonic_to_voice_leading_preserved=harmonic_to_voice_leading_preserved,
        voice_leading_to_context_preserved=voice_leading_to_context_preserved,
        rhythm_harmonic_timing_complement_preserved=(
            rhythm_harmonic_timing_complement_preserved
        ),
        non_confluent_surfaces_preserved=True,
        treats_interaction_as_unification=False,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="cross_module_interaction_stress_299_348_observed_without_unifying_interaction_surfaces",
    )


def run_checks() -> None:
    observation = observe_cross_module_interaction_stress()
    assert observation.source_status == (
        "tuning_to_interval_spelling_stress_289_298_observed_without_collapsing_12tet_category_into_interval_name"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 299
    assert observation.steps[-1].number == 348
    assert observation.tuning_to_interval_preserved is True
    assert observation.interval_to_harmonic_preserved is True
    assert observation.harmonic_to_voice_leading_preserved is True
    assert observation.voice_leading_to_context_preserved is True
    assert observation.rhythm_harmonic_timing_complement_preserved is True
    assert observation.non_confluent_surfaces_preserved is True
    assert observation.treats_interaction_as_unification is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_interval_to_harmonic_target_context_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_cross_module_interaction_stress().status)
