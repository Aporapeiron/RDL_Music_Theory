"""同じhuman-side response differenceとsourceでΓ_generationだけを差し替える最小検証。

61で確認したsource差による候補集合分岐に対し、今回はsourceを固定して
Γ_learned_candidate_generationの読み方だけで候補集合が分岐することを確認する。

    same human-side response difference
      + same learned candidate generation source
      + different Gamma_learned_candidate_generation fixtures
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
    generation_profile: str
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
class LearnedCandidateGammaVariationComparison:
    full_inventory_observation: LearnedCandidateSetObservation
    binary_only_observation: LearnedCandidateSetObservation
    same_response_difference: bool
    same_source: bool
    same_gamma: bool
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


def gamma_full_inventory() -> LearnedCandidateGenerationGamma:
    return LearnedCandidateGenerationGamma(
        name="Gamma_learned_candidate_generation_full_inventory_fixture",
        generation_profile="read_full_inventory_profile",
        reads=("learned_candidate_generation_source", "inventory_profile"),
        rule_scope="fixture_limited_not_general_learned_category_generation_rule",
    )


def gamma_binary_only() -> LearnedCandidateGenerationGamma:
    return LearnedCandidateGenerationGamma(
        name="Gamma_learned_candidate_generation_binary_only_fixture",
        generation_profile="read_binary_only_profile",
        reads=("learned_candidate_generation_source", "inventory_profile"),
        rule_scope="fixture_limited_not_general_learned_category_generation_rule",
    )


def observe_learned_candidate_set(
    response_difference: HumanSideResponseDifference,
    source: LearnedCandidateGenerationSource,
    gamma: LearnedCandidateGenerationGamma,
) -> LearnedCandidateSetObservation:
    if gamma.generation_profile == "read_full_inventory_profile":
        labels = (
            "same_pitch_relation_label_candidate",
            "different_pitch_relation_label_candidate",
            "uncertain_pitch_relation_label_candidate",
        )
    elif gamma.generation_profile == "read_binary_only_profile":
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


def compare_learned_candidate_gamma_variation() -> LearnedCandidateGammaVariationComparison:
    response_difference = a2_human_side_response_difference()
    source = pitch_relation_source()
    full_inventory_observation = observe_learned_candidate_set(
        response_difference=response_difference,
        source=source,
        gamma=gamma_full_inventory(),
    )
    binary_only_observation = observe_learned_candidate_set(
        response_difference=response_difference,
        source=source,
        gamma=gamma_binary_only(),
    )
    full_labels = tuple(
        candidate.label for candidate in full_inventory_observation.learned_candidates
    )
    binary_labels = tuple(
        candidate.label for candidate in binary_only_observation.learned_candidates
    )
    return LearnedCandidateGammaVariationComparison(
        full_inventory_observation=full_inventory_observation,
        binary_only_observation=binary_only_observation,
        same_response_difference=(
            full_inventory_observation.response_difference
            == binary_only_observation.response_difference
        ),
        same_source=full_inventory_observation.source == binary_only_observation.source,
        same_gamma=full_inventory_observation.gamma == binary_only_observation.gamma,
        same_candidate_set=full_labels == binary_labels,
        generated_learned_category=full_inventory_observation.generated_learned_category,
        bridge_candidate=full_inventory_observation.bridge_candidate,
        selected_musical_interpretation=(
            full_inventory_observation.selected_musical_interpretation
        ),
    )


def run_checks() -> None:
    comparison = compare_learned_candidate_gamma_variation()
    assert comparison.same_response_difference is True
    assert comparison.same_source is True
    assert comparison.same_gamma is False
    assert comparison.same_candidate_set is False
    assert comparison.generated_learned_category is None
    assert comparison.bridge_candidate is None
    assert comparison.selected_musical_interpretation is None

    first = comparison.full_inventory_observation
    second = comparison.binary_only_observation
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
    comparison = compare_learned_candidate_gamma_variation()
    first = comparison.full_inventory_observation
    second = comparison.binary_only_observation

    print("[pipeline]")
    print("  same human-side response difference")
    print("  + same learned candidate generation source")
    print("  + different Gamma_learned_candidate_generation fixtures")
    print("  -> different learned category candidate sets")
    print("  -> bridge candidate remains None")
    print(f"  same_response_difference={comparison.same_response_difference}")
    print(f"  same_source={comparison.same_source}")
    print(f"  same_gamma={comparison.same_gamma}")
    print(f"  same_candidate_set={comparison.same_candidate_set}")
    print(f"  generated_learned_category={comparison.generated_learned_category}")
    print(f"  bridge_candidate={comparison.bridge_candidate}")
    print(
        "  selected_musical_interpretation="
        f"{comparison.selected_musical_interpretation}"
    )
    print(
        "  full_inventory_candidates="
        + ", ".join(candidate.label for candidate in first.learned_candidates)
    )
    print(
        "  binary_only_candidates="
        + ", ".join(candidate.label for candidate in second.learned_candidates)
    )


if __name__ == "__main__":
    main()
