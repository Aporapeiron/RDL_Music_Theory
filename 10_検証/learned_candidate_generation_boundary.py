"""learned category候補集合の供給境界を観測する最小検証。

57〜59で外部入力だったlearned category candidatesについて、
human-side response differenceから直生成せず、sourceとΓ_generationを分けて候補集合を観測する。

    human-side response difference
      + learned candidate generation source
      + Gamma_learned_candidate_generation_fixture
      -> learned category candidates observed
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
    source: LearnedCandidateGenerationSource | None
    gamma: LearnedCandidateGenerationGamma | None
    learned_candidates: tuple[LearnedCategoryCandidate, ...]
    generated_learned_category: str | None
    bridge_candidate: str | None
    selected_musical_interpretation: str | None
    status: str


@dataclass(frozen=True)
class LearnedCandidateGenerationComparison:
    without_gamma: LearnedCandidateSetObservation
    with_gamma: LearnedCandidateSetObservation
    same_response_difference: bool
    same_source: bool
    same_gamma: bool
    candidate_set_observed: bool
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


def learned_pitch_relation_source() -> LearnedCandidateGenerationSource:
    return LearnedCandidateGenerationSource(
        label="learned_pitch_relation_label_inventory_fixture",
        source_kind="external_learned_inventory_fixture",
        category_family="learned_pitch_relation_label",
        generated_by_response_difference=False,
    )


def learned_candidate_generation_gamma() -> LearnedCandidateGenerationGamma:
    return LearnedCandidateGenerationGamma(
        name="Gamma_learned_candidate_generation_fixture",
        reads=("learned_candidate_generation_source", "category_family"),
        rule_scope="fixture_limited_not_general_learned_category_generation_rule",
    )


def observe_learned_candidate_set(
    response_difference: HumanSideResponseDifference,
    source: LearnedCandidateGenerationSource | None,
    gamma: LearnedCandidateGenerationGamma | None,
) -> LearnedCandidateSetObservation:
    if source is None:
        return LearnedCandidateSetObservation(
            response_difference=response_difference,
            source=None,
            gamma=gamma,
            learned_candidates=(),
            generated_learned_category=None,
            bridge_candidate=None,
            selected_musical_interpretation=None,
            status="no_learned_candidate_generation_source",
        )

    if gamma is None:
        return LearnedCandidateSetObservation(
            response_difference=response_difference,
            source=source,
            gamma=None,
            learned_candidates=(),
            generated_learned_category=None,
            bridge_candidate=None,
            selected_musical_interpretation=None,
            status="no_learned_candidate_generation_gamma",
        )

    candidates = (
        LearnedCategoryCandidate(
            label="same_pitch_relation_label_candidate",
            category_family=source.category_family,
            supplied_by=source.label,
            generated_by_response_difference=False,
        ),
        LearnedCategoryCandidate(
            label="different_pitch_relation_label_candidate",
            category_family=source.category_family,
            supplied_by=source.label,
            generated_by_response_difference=False,
        ),
        LearnedCategoryCandidate(
            label="uncertain_pitch_relation_label_candidate",
            category_family=source.category_family,
            supplied_by=source.label,
            generated_by_response_difference=False,
        ),
    )
    return LearnedCandidateSetObservation(
        response_difference=response_difference,
        source=source,
        gamma=gamma,
        learned_candidates=candidates,
        generated_learned_category=None,
        bridge_candidate=None,
        selected_musical_interpretation=None,
        status="learned_candidate_set_observed_not_bridged",
    )


def compare_learned_candidate_generation() -> LearnedCandidateGenerationComparison:
    response_difference = a2_human_side_response_difference()
    source = learned_pitch_relation_source()
    gamma = learned_candidate_generation_gamma()
    without_gamma = observe_learned_candidate_set(
        response_difference=response_difference,
        source=source,
        gamma=None,
    )
    with_gamma = observe_learned_candidate_set(
        response_difference=response_difference,
        source=source,
        gamma=gamma,
    )
    return LearnedCandidateGenerationComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_response_difference=(
            without_gamma.response_difference == with_gamma.response_difference
        ),
        same_source=without_gamma.source == with_gamma.source,
        same_gamma=without_gamma.gamma == with_gamma.gamma,
        candidate_set_observed=(
            with_gamma.status == "learned_candidate_set_observed_not_bridged"
        ),
        generated_learned_category=with_gamma.generated_learned_category,
        bridge_candidate=with_gamma.bridge_candidate,
        selected_musical_interpretation=with_gamma.selected_musical_interpretation,
    )


def run_checks() -> None:
    comparison = compare_learned_candidate_generation()
    assert comparison.same_response_difference is True
    assert comparison.same_source is True
    assert comparison.same_gamma is False
    assert comparison.candidate_set_observed is True
    assert comparison.generated_learned_category is None
    assert comparison.bridge_candidate is None
    assert comparison.selected_musical_interpretation is None

    assert comparison.without_gamma.status == "no_learned_candidate_generation_gamma"
    assert comparison.with_gamma.status == "learned_candidate_set_observed_not_bridged"
    assert len(comparison.with_gamma.learned_candidates) == 3
    assert comparison.with_gamma.response_difference.generated_learned_category is None
    assert comparison.with_gamma.source is not None
    assert comparison.with_gamma.source.generated_by_response_difference is False
    assert all(
        candidate.generated_by_response_difference is False
        for candidate in comparison.with_gamma.learned_candidates
    )


def main() -> None:
    run_checks()
    comparison = compare_learned_candidate_generation()
    observation = comparison.with_gamma

    print("[pipeline]")
    print("  human-side response difference")
    print("  + learned candidate generation source")
    print("  + Gamma_learned_candidate_generation_fixture")
    print("  -> learned category candidates observed")
    print("  -> bridge candidate remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={observation.status}")
    print(f"  same_response_difference={comparison.same_response_difference}")
    print(f"  same_source={comparison.same_source}")
    print(f"  candidate_set_observed={comparison.candidate_set_observed}")
    print(f"  generated_learned_category={comparison.generated_learned_category}")
    print(f"  bridge_candidate={comparison.bridge_candidate}")
    print(
        "  selected_musical_interpretation="
        f"{comparison.selected_musical_interpretation}"
    )
    print(
        "  learned_candidates="
        + ", ".join(candidate.label for candidate in observation.learned_candidates)
    )


if __name__ == "__main__":
    main()
