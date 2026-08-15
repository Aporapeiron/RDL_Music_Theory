"""同じhuman-side response differenceとlearned候補集合でΓ_bridgeだけを差し替える最小検証。

57で開いたbase-to-learned bridge境界について、bridge候補が
response differenceやlearned候補集合の属性ではなく、Γ_bridgeを含む関係から生じることを確認する。

    same human-side response difference
      + same external learned category candidates
      + different Gamma_bridge fixtures
      -> different bridge candidates
      -> generated learned category remains None
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
class LearnedCategoryCandidate:
    label: str
    category_family: str
    supplied_by: str
    generated_by_response_difference: bool


@dataclass(frozen=True)
class BridgeGamma:
    name: str
    target_candidate_label: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class BridgeCandidate:
    response_difference: HumanSideResponseDifference
    learned_candidate: LearnedCategoryCandidate
    bridge_relation: str
    confirmed_learned_category: bool


@dataclass(frozen=True)
class BridgeObservation:
    response_difference: HumanSideResponseDifference
    external_learned_candidates: tuple[LearnedCategoryCandidate, ...]
    gamma: BridgeGamma
    bridge_candidates: tuple[BridgeCandidate, ...]
    generated_learned_category: str | None
    selected_musical_interpretation: str | None
    status: str


@dataclass(frozen=True)
class BridgeGammaVariationComparison:
    difference_label_observation: BridgeObservation
    uncertain_label_observation: BridgeObservation
    same_response_difference: bool
    same_external_candidates: bool
    same_gamma: bool
    same_bridge_candidate_set: bool
    generated_learned_category: str | None
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


def external_learned_category_candidates() -> tuple[
    LearnedCategoryCandidate,
    LearnedCategoryCandidate,
    LearnedCategoryCandidate,
]:
    return (
        LearnedCategoryCandidate(
            label="same_pitch_relation_label_candidate",
            category_family="learned_pitch_relation_label",
            supplied_by="external_learned_candidate_fixture",
            generated_by_response_difference=False,
        ),
        LearnedCategoryCandidate(
            label="different_pitch_relation_label_candidate",
            category_family="learned_pitch_relation_label",
            supplied_by="external_learned_candidate_fixture",
            generated_by_response_difference=False,
        ),
        LearnedCategoryCandidate(
            label="uncertain_pitch_relation_label_candidate",
            category_family="learned_pitch_relation_label",
            supplied_by="external_learned_candidate_fixture",
            generated_by_response_difference=False,
        ),
    )


def bridge_gamma_to_difference_label() -> BridgeGamma:
    return BridgeGamma(
        name="Gamma_bridge_discriminability_to_difference_label_fixture",
        target_candidate_label="different_pitch_relation_label_candidate",
        reads=("human_side_response_difference", "external_learned_category_candidate"),
        rule_scope="fixture_limited_not_general_category_generation_rule",
    )


def bridge_gamma_to_uncertain_label() -> BridgeGamma:
    return BridgeGamma(
        name="Gamma_bridge_discriminability_to_uncertain_label_fixture",
        target_candidate_label="uncertain_pitch_relation_label_candidate",
        reads=("human_side_response_difference", "external_learned_category_candidate"),
        rule_scope="fixture_limited_not_general_category_generation_rule",
    )


def observe_bridge_with_gamma(
    response_difference: HumanSideResponseDifference,
    learned_candidates: tuple[LearnedCategoryCandidate, ...],
    gamma: BridgeGamma,
) -> BridgeObservation:
    compatible = tuple(
        BridgeCandidate(
            response_difference=response_difference,
            learned_candidate=candidate,
            bridge_relation="compatible_bridge_candidate",
            confirmed_learned_category=False,
        )
        for candidate in learned_candidates
        if candidate.label == gamma.target_candidate_label
    )
    if not compatible:
        return BridgeObservation(
            response_difference=response_difference,
            external_learned_candidates=learned_candidates,
            gamma=gamma,
            bridge_candidates=(),
            generated_learned_category=None,
            selected_musical_interpretation=None,
            status="no_bridge_candidate_observed",
        )

    return BridgeObservation(
        response_difference=response_difference,
        external_learned_candidates=learned_candidates,
        gamma=gamma,
        bridge_candidates=compatible,
        generated_learned_category=None,
        selected_musical_interpretation=None,
        status="bridge_candidate_observed_not_selected",
    )


def compare_bridge_gamma_variation() -> BridgeGammaVariationComparison:
    response_difference = a2_human_side_response_difference()
    learned_candidates = external_learned_category_candidates()
    difference_label_observation = observe_bridge_with_gamma(
        response_difference=response_difference,
        learned_candidates=learned_candidates,
        gamma=bridge_gamma_to_difference_label(),
    )
    uncertain_label_observation = observe_bridge_with_gamma(
        response_difference=response_difference,
        learned_candidates=learned_candidates,
        gamma=bridge_gamma_to_uncertain_label(),
    )
    difference_labels = tuple(
        candidate.learned_candidate.label
        for candidate in difference_label_observation.bridge_candidates
    )
    uncertain_labels = tuple(
        candidate.learned_candidate.label
        for candidate in uncertain_label_observation.bridge_candidates
    )
    return BridgeGammaVariationComparison(
        difference_label_observation=difference_label_observation,
        uncertain_label_observation=uncertain_label_observation,
        same_response_difference=(
            difference_label_observation.response_difference
            == uncertain_label_observation.response_difference
        ),
        same_external_candidates=(
            difference_label_observation.external_learned_candidates
            == uncertain_label_observation.external_learned_candidates
        ),
        same_gamma=(difference_label_observation.gamma == uncertain_label_observation.gamma),
        same_bridge_candidate_set=(difference_labels == uncertain_labels),
        generated_learned_category=difference_label_observation.generated_learned_category,
        selected_musical_interpretation=(
            difference_label_observation.selected_musical_interpretation
        ),
    )


def run_checks() -> None:
    comparison = compare_bridge_gamma_variation()
    assert comparison.same_response_difference is True
    assert comparison.same_external_candidates is True
    assert comparison.same_gamma is False
    assert comparison.same_bridge_candidate_set is False
    assert comparison.generated_learned_category is None
    assert comparison.selected_musical_interpretation is None

    first = comparison.difference_label_observation
    second = comparison.uncertain_label_observation
    assert first.status == "bridge_candidate_observed_not_selected"
    assert second.status == "bridge_candidate_observed_not_selected"
    assert first.bridge_candidates[0].learned_candidate.label == (
        "different_pitch_relation_label_candidate"
    )
    assert second.bridge_candidates[0].learned_candidate.label == (
        "uncertain_pitch_relation_label_candidate"
    )
    assert first.bridge_candidates[0].confirmed_learned_category is False
    assert second.bridge_candidates[0].confirmed_learned_category is False
    assert all(
        candidate.generated_by_response_difference is False
        for candidate in first.external_learned_candidates
    )


def main() -> None:
    run_checks()
    comparison = compare_bridge_gamma_variation()
    first = comparison.difference_label_observation
    second = comparison.uncertain_label_observation

    print("[pipeline]")
    print("  same human-side response difference")
    print("  + same external learned category candidates")
    print("  + different Gamma_bridge fixtures")
    print("  -> different bridge candidates")
    print("  -> generated learned category remains None")
    print(f"  same_response_difference={comparison.same_response_difference}")
    print(f"  same_external_candidates={comparison.same_external_candidates}")
    print(f"  same_gamma={comparison.same_gamma}")
    print(f"  same_bridge_candidate_set={comparison.same_bridge_candidate_set}")
    print(f"  generated_learned_category={comparison.generated_learned_category}")
    print(
        "  selected_musical_interpretation="
        f"{comparison.selected_musical_interpretation}"
    )
    print(
        "  bridge_candidates="
        + ", ".join(
            [
                first.bridge_candidates[0].learned_candidate.label,
                second.bridge_candidates[0].learned_candidate.label,
            ]
        )
    )


if __name__ == "__main__":
    main()
