"""同じhuman-side response differenceとΓ_generationでsourceだけを差し替える最小検証。

60で観測したlearned category candidatesについて、候補集合が
sourceの属性ではなく、sourceとΓ_generationの関係として分岐することを確認する。

    same human-side response difference
      + same Gamma_learned_candidate_generation_fixture
      + different learned candidate generation sources
      -> different learned category candidate sets
      -> bridge candidate remains None
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class HumanSideResponseDifference:
    label: str
    source_base_candidate: str
    response_axis: str
    lower_response: str
    higher_response: str
    generated_learned_category: str | None


@dataclass(frozen=True)
class LearnedCandidateGenerationSource:
    label: str
    source_kind: str
    category_family: str
    inventory_profile: str
    generated_by_response_difference: bool


@dataclass(frozen=True)
class LearnedCandidateGenerationGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class LearnedCategoryCandidate:
    label: str
    category_family: str
    supplied_by: str
    generated_by_response_difference: bool


@dataclass(frozen=True)
class LearnedCandidateSetObservation:
    response_difference: HumanSideResponseDifference
    source: LearnedCandidateGenerationSource
    gamma: LearnedCandidateGenerationGamma
    learned_candidates: tuple[LearnedCategoryCandidate, ...]
    generated_learned_category: str | None
    bridge_candidate: str | None
    selected_musical_interpretation: str | None
    status: str


@dataclass(frozen=True)
class LearnedCandidateSourceVariationComparison:
    pitch_relation_observation: LearnedCandidateSetObservation
    coarse_binary_observation: LearnedCandidateSetObservation
    same_response_difference: bool
    same_gamma: bool
    same_source: bool
    same_candidate_set: bool
    generated_learned_category: str | None
    bridge_candidate: str | None
    selected_musical_interpretation: str | None


def a2_human_side_response_difference() -> HumanSideResponseDifference:
    return HumanSideResponseDifference(
        label="A2 behavioral discriminability difference",
        source_base_candidate="frequency_difference_to_behavioral_discriminability_candidate",
        response_axis="behavioral_discriminability",
        lower_response="low_discriminability",
        higher_response="high_discriminability",
        generated_learned_category=None,
    )


def pitch_relation_source() -> LearnedCandidateGenerationSource:
    return LearnedCandidateGenerationSource(
        label="learned_pitch_relation_label_inventory_fixture",
        source_kind="external_learned_inventory_fixture",
        category_family="learned_pitch_relation_label",
        inventory_profile="same_different_uncertain_profile",
        generated_by_response_difference=False,
    )


def coarse_binary_source() -> LearnedCandidateGenerationSource:
    return LearnedCandidateGenerationSource(
        label="learned_pitch_binary_label_inventory_fixture",
        source_kind="external_learned_inventory_fixture",
        category_family="learned_pitch_relation_label",
        inventory_profile="same_different_only_profile",
        generated_by_response_difference=False,
    )


def learned_candidate_generation_gamma() -> LearnedCandidateGenerationGamma:
    return LearnedCandidateGenerationGamma(
        name="Gamma_learned_candidate_generation_fixture",
        reads=("learned_candidate_generation_source", "inventory_profile"),
        rule_scope="fixture_limited_not_general_learned_category_generation_rule",
    )


def observe_learned_candidate_set(
    response_difference: HumanSideResponseDifference,
    source: LearnedCandidateGenerationSource,
    gamma: LearnedCandidateGenerationGamma,
) -> LearnedCandidateSetObservation:
    if source.inventory_profile == "same_different_uncertain_profile":
        labels = (
            "same_pitch_relation_label_candidate",
            "different_pitch_relation_label_candidate",
            "uncertain_pitch_relation_label_candidate",
        )
    elif source.inventory_profile == "same_different_only_profile":
        labels = (
            "same_pitch_relation_label_candidate",
            "different_pitch_relation_label_candidate",
        )
    else:
        labels = ()

    candidates = tuple(
        LearnedCategoryCandidate(
            label=label,
            category_family=source.category_family,
            supplied_by=source.label,
            generated_by_response_difference=False,
        )
        for label in labels
    )
    status = (
        "learned_candidate_set_observed_not_bridged"
        if candidates
        else "no_learned_candidate_observed"
    )
    return LearnedCandidateSetObservation(
        response_difference=response_difference,
        source=source,
        gamma=gamma,
        learned_candidates=candidates,
        generated_learned_category=None,
        bridge_candidate=None,
        selected_musical_interpretation=None,
        status=status,
    )


def compare_learned_candidate_source_variation() -> LearnedCandidateSourceVariationComparison:
    response_difference = a2_human_side_response_difference()
    gamma = learned_candidate_generation_gamma()
    pitch_relation_observation = observe_learned_candidate_set(
        response_difference=response_difference,
        source=pitch_relation_source(),
        gamma=gamma,
    )
    coarse_binary_observation = observe_learned_candidate_set(
        response_difference=response_difference,
        source=coarse_binary_source(),
        gamma=gamma,
    )
    pitch_labels = tuple(
        candidate.label for candidate in pitch_relation_observation.learned_candidates
    )
    coarse_labels = tuple(
        candidate.label for candidate in coarse_binary_observation.learned_candidates
    )
    return LearnedCandidateSourceVariationComparison(
        pitch_relation_observation=pitch_relation_observation,
        coarse_binary_observation=coarse_binary_observation,
        same_response_difference=(
            pitch_relation_observation.response_difference
            == coarse_binary_observation.response_difference
        ),
        same_gamma=pitch_relation_observation.gamma == coarse_binary_observation.gamma,
        same_source=pitch_relation_observation.source == coarse_binary_observation.source,
        same_candidate_set=pitch_labels == coarse_labels,
        generated_learned_category=pitch_relation_observation.generated_learned_category,
        bridge_candidate=pitch_relation_observation.bridge_candidate,
        selected_musical_interpretation=(
            pitch_relation_observation.selected_musical_interpretation
        ),
    )


def run_checks() -> None:
    comparison = compare_learned_candidate_source_variation()
    assert comparison.same_response_difference is True
    assert comparison.same_gamma is True
    assert comparison.same_source is False
    assert comparison.same_candidate_set is False
    assert comparison.generated_learned_category is None
    assert comparison.bridge_candidate is None
    assert comparison.selected_musical_interpretation is None

    first = comparison.pitch_relation_observation
    second = comparison.coarse_binary_observation
    assert first.status == "learned_candidate_set_observed_not_bridged"
    assert second.status == "learned_candidate_set_observed_not_bridged"
    assert len(first.learned_candidates) == 3
    assert len(second.learned_candidates) == 2
    assert first.response_difference.generated_learned_category is None
    assert first.source.generated_by_response_difference is False
    assert second.source.generated_by_response_difference is False
    assert all(
        candidate.generated_by_response_difference is False
        for candidate in first.learned_candidates + second.learned_candidates
    )


def main() -> None:
    run_checks()
    comparison = compare_learned_candidate_source_variation()
    first = comparison.pitch_relation_observation
    second = comparison.coarse_binary_observation

    print("[pipeline]")
    print("  same human-side response difference")
    print("  + same Gamma_learned_candidate_generation_fixture")
    print("  + different learned candidate generation sources")
    print("  -> different learned category candidate sets")
    print("  -> bridge candidate remains None")
    print(f"  same_response_difference={comparison.same_response_difference}")
    print(f"  same_gamma={comparison.same_gamma}")
    print(f"  same_source={comparison.same_source}")
    print(f"  same_candidate_set={comparison.same_candidate_set}")
    print(f"  generated_learned_category={comparison.generated_learned_category}")
    print(f"  bridge_candidate={comparison.bridge_candidate}")
    print(
        "  selected_musical_interpretation="
        f"{comparison.selected_musical_interpretation}"
    )
    print(
        "  pitch_relation_candidates="
        + ", ".join(candidate.label for candidate in first.learned_candidates)
    )
    print(
        "  coarse_binary_candidates="
        + ", ".join(candidate.label for candidate in second.learned_candidates)
    )


if __name__ == "__main__":
    main()
