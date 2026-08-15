"""同じhuman-side response differenceとΓ_bridgeでlearned候補集合だけを差し替える最小検証。

58で確認したbridge候補の関係性を、今度はexternal learned category candidatesの
有無・構成差として観測する。

    same human-side response difference
      + same Gamma_bridge fixture
      + different external learned category candidates
      -> bridge candidate observed / no bridge candidate observed
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
class BridgeCandidateSetVariationComparison:
    with_target_candidate: BridgeObservation
    without_target_candidate: BridgeObservation
    same_response_difference: bool
    same_gamma: bool
    same_external_candidates: bool
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


def bridge_gamma_to_difference_label() -> BridgeGamma:
    return BridgeGamma(
        name="Gamma_bridge_discriminability_to_difference_label_fixture",
        target_candidate_label="different_pitch_relation_label_candidate",
        reads=("human_side_response_difference", "external_learned_category_candidate"),
        rule_scope="fixture_limited_not_general_category_generation_rule",
    )


def candidates_with_target() -> tuple[
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
    )


def candidates_without_target() -> tuple[
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
            label="uncertain_pitch_relation_label_candidate",
            category_family="learned_pitch_relation_label",
            supplied_by="external_learned_candidate_fixture",
            generated_by_response_difference=False,
        ),
    )


def observe_bridge_with_candidates(
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


def compare_bridge_candidate_set_variation() -> BridgeCandidateSetVariationComparison:
    response_difference = a2_human_side_response_difference()
    gamma = bridge_gamma_to_difference_label()
    with_target = observe_bridge_with_candidates(
        response_difference=response_difference,
        learned_candidates=candidates_with_target(),
        gamma=gamma,
    )
    without_target = observe_bridge_with_candidates(
        response_difference=response_difference,
        learned_candidates=candidates_without_target(),
        gamma=gamma,
    )
    with_labels = tuple(
        candidate.learned_candidate.label for candidate in with_target.bridge_candidates
    )
    without_labels = tuple(
        candidate.learned_candidate.label for candidate in without_target.bridge_candidates
    )
    return BridgeCandidateSetVariationComparison(
        with_target_candidate=with_target,
        without_target_candidate=without_target,
        same_response_difference=(
            with_target.response_difference == without_target.response_difference
        ),
        same_gamma=with_target.gamma == without_target.gamma,
        same_external_candidates=(
            with_target.external_learned_candidates
            == without_target.external_learned_candidates
        ),
        same_bridge_candidate_set=(with_labels == without_labels),
        generated_learned_category=with_target.generated_learned_category,
        selected_musical_interpretation=with_target.selected_musical_interpretation,
    )


def run_checks() -> None:
    comparison = compare_bridge_candidate_set_variation()
    assert comparison.same_response_difference is True
    assert comparison.same_gamma is True
    assert comparison.same_external_candidates is False
    assert comparison.same_bridge_candidate_set is False
    assert comparison.generated_learned_category is None
    assert comparison.selected_musical_interpretation is None

    with_target = comparison.with_target_candidate
    without_target = comparison.without_target_candidate
    assert with_target.status == "bridge_candidate_observed_not_selected"
    assert without_target.status == "no_bridge_candidate_observed"
    assert with_target.bridge_candidates[0].learned_candidate.label == (
        "different_pitch_relation_label_candidate"
    )
    assert without_target.bridge_candidates == ()
    assert with_target.bridge_candidates[0].confirmed_learned_category is False
    assert all(
        candidate.generated_by_response_difference is False
        for candidate in with_target.external_learned_candidates
    )
    assert all(
        candidate.generated_by_response_difference is False
        for candidate in without_target.external_learned_candidates
    )


def main() -> None:
    run_checks()
    comparison = compare_bridge_candidate_set_variation()
    with_target = comparison.with_target_candidate
    without_target = comparison.without_target_candidate

    print("[pipeline]")
    print("  same human-side response difference")
    print("  + same Gamma_bridge fixture")
    print("  + different external learned category candidates")
    print("  -> bridge candidate observed / no bridge candidate observed")
    print("  -> generated learned category remains None")
    print(f"  same_response_difference={comparison.same_response_difference}")
    print(f"  same_gamma={comparison.same_gamma}")
    print(f"  same_external_candidates={comparison.same_external_candidates}")
    print(f"  same_bridge_candidate_set={comparison.same_bridge_candidate_set}")
    print(f"  generated_learned_category={comparison.generated_learned_category}")
    print(
        "  selected_musical_interpretation="
        f"{comparison.selected_musical_interpretation}"
    )
    print(f"  with_target_status={with_target.status}")
    print(f"  without_target_status={without_target.status}")
    print(
        "  bridge_candidates="
        + ", ".join(
            candidate.learned_candidate.label for candidate in with_target.bridge_candidates
        )
    )


if __name__ == "__main__":
    main()
