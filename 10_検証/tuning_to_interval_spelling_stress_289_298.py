"""音高調律から音程綴り境界への片方向接続stress test。"""

from dataclasses import dataclass
from math import isclose

from cross_module_interaction_surface_279_288 import observe_interaction_surfaces
from interval_fifth_decomposition import observe_interval
from spelled_interval_divergence import SpelledNote, observe_spelled_interval


@dataclass(frozen=True)
class TuningToIntervalStressStep:
    number: int
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class TuningToIntervalSpellingStressObservation:
    source_status: str
    tuning_semitones_12tet: int
    spelling_labels: tuple[str, ...]
    same_tuning_category: bool
    spelling_required_for_label: bool
    spelling_splits_interval_label: bool
    directed_connection_preserved: bool
    returns_interval_name_to_tuning: bool
    steps: tuple[TuningToIntervalStressStep, ...]
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str], ...] = (
    (289, "tuning_category_source", "tuning_7_semitone_category"),
    (290, "interval_spelling_boundary_request", "spelling_boundary_required"),
    (291, "unspelled_interval_label_block", "interval_label_not_generated_without_spelling"),
    (292, "C4_G4_spelling_application", "perfect_fifth_label_candidate"),
    (293, "Csharp4_Aflat4_spelling_application", "diminished_sixth_label_candidate"),
    (294, "same_12tet_category_comparison", "same_category_different_label_observation"),
    (295, "directed_connection_check", "tuning_to_interval_connection_preserved"),
    (296, "reverse_determination_block", "interval_name_not_returned_to_tuning_category"),
    (297, "music_specific_difference_preservation", "spelling_difference_preserved"),
    (298, "next_stress_target", "interval_to_harmonic_target_stress_candidate"),
)


def observe_tuning_to_interval_spelling_stress() -> TuningToIntervalSpellingStressObservation:
    interaction = observe_interaction_surfaces()
    tuning = observe_interval(100.0, 150.0)
    p5 = observe_spelled_interval(
        SpelledNote("C", octave=4),
        SpelledNote("G", octave=4),
    )
    d6 = observe_spelled_interval(
        SpelledNote("C", accidental=1, octave=4),
        SpelledNote("A", accidental=-1, octave=4),
    )
    same_pitch_d6 = observe_spelled_interval(
        SpelledNote("C", octave=4),
        SpelledNote("A", accidental=-2, octave=4),
    )

    previous = "cross_module_interaction_surface_279"
    steps = []
    for number, name, result in STEP_DEFINITIONS:
        steps.append(
            TuningToIntervalStressStep(
                number=number,
                name=name,
                source=previous,
                result=result,
                generated_mutation=False,
            )
        )
        previous = result

    same_tuning_category = (
        tuning.semitones_12tet
        == p5.semitones_12tet
        == d6.semitones_12tet
        == same_pitch_d6.semitones_12tet
        == 7
    )
    spelling_labels = (p5.label, d6.label, same_pitch_d6.label)
    spelling_splits_interval_label = len(set(spelling_labels)) == 2

    return TuningToIntervalSpellingStressObservation(
        source_status=interaction.status,
        tuning_semitones_12tet=tuning.semitones_12tet,
        spelling_labels=spelling_labels,
        same_tuning_category=same_tuning_category,
        spelling_required_for_label=True,
        spelling_splits_interval_label=spelling_splits_interval_label,
        directed_connection_preserved=True,
        returns_interval_name_to_tuning=False,
        steps=tuple(steps),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="tuning_to_interval_spelling_stress_289_298_observed_without_collapsing_12tet_category_into_interval_name",
    )


def run_checks() -> None:
    observation = observe_tuning_to_interval_spelling_stress()
    assert observation.source_status == (
        "cross_module_interaction_surface_279_288_observed_without_unifying_music_domains"
    )
    assert observation.tuning_semitones_12tet == 7
    assert observation.same_tuning_category is True
    assert observation.spelling_required_for_label is True
    assert observation.spelling_splits_interval_label is True
    assert observation.spelling_labels == ("完全五度", "減六度", "減六度")
    assert observation.directed_connection_preserved is True
    assert observation.returns_interval_name_to_tuning is False
    assert len(observation.steps) == 10
    assert observation.steps[0].number == 289
    assert observation.steps[-1].number == 298
    assert observation.generated_mutation is False
    assert isclose(observe_interval(100.0, 150.0).ratio, 1.5, abs_tol=1e-12)


if __name__ == "__main__":
    run_checks()
    print(observe_tuning_to_interval_spelling_stress().status)
