"""human-side response differenceとlearned category候補のbridge境界を観測する最小検証。

54〜56構造抽出で残したξ_base_to_learned_bridgeを、
human-side response differenceからlearned categoryを直生成せずに検査する。

    human-side response difference
      + external learned category candidates
      + Gamma_bridge fixture
      -> bridge candidate observed
      -> selected musical interpretation remains None
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
    gamma: BridgeGamma | None
    bridge_candidates: tuple[BridgeCandidate, ...]
    generated_learned_category: str | None
    selected_musical_interpretation: str | None
    status: str


@dataclass(frozen=True)
class BridgeComparison:
    without_gamma: BridgeObservation
    with_gamma: BridgeObservation
    same_response_difference: bool
    same_external_candidates: bool
    same_gamma: bool
    bridge_candidate_observed: bool
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


def base_to_learned_bridge_gamma() -> BridgeGamma:
    return BridgeGamma(
        name="Gamma_base_to_learned_bridge_fixture",
        reads=("human_side_response_difference", "external_learned_category_candidate"),
        rule_scope="fixture_limited_not_general_category_generation_rule",
    )


def observe_bridge_boundary(
    response_difference: HumanSideResponseDifference,
    learned_candidates: tuple[LearnedCategoryCandidate, ...],
    gamma: BridgeGamma | None,
) -> BridgeObservation:
    if not learned_candidates:
        return BridgeObservation(
            response_difference=response_difference,
            external_learned_candidates=learned_candidates,
            gamma=gamma,
            bridge_candidates=(),
            generated_learned_category=None,
            selected_musical_interpretation=None,
            status="no_external_learned_candidates",
        )

    if gamma is None:
        return BridgeObservation(
            response_difference=response_difference,
            external_learned_candidates=learned_candidates,
            gamma=None,
            bridge_candidates=(),
            generated_learned_category=None,
            selected_musical_interpretation=None,
            status="underdetermined_without_bridge_gamma",
        )

    compatible = tuple(
        BridgeCandidate(
            response_difference=response_difference,
            learned_candidate=candidate,
            bridge_relation="compatible_bridge_candidate",
            confirmed_learned_category=False,
        )
        for candidate in learned_candidates
        if candidate.label == "different_pitch_relation_label_candidate"
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


def compare_base_to_learned_bridge() -> BridgeComparison:
    response_difference = a2_human_side_response_difference()
    learned_candidates = external_learned_category_candidates()
    gamma = base_to_learned_bridge_gamma()
    without_gamma = observe_bridge_boundary(
        response_difference=response_difference,
        learned_candidates=learned_candidates,
        gamma=None,
    )
    with_gamma = observe_bridge_boundary(
        response_difference=response_difference,
        learned_candidates=learned_candidates,
        gamma=gamma,
    )
    return BridgeComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_response_difference=(
            without_gamma.response_difference == with_gamma.response_difference
        ),
        same_external_candidates=(
            without_gamma.external_learned_candidates
            == with_gamma.external_learned_candidates
        ),
        same_gamma=without_gamma.gamma == with_gamma.gamma,
        bridge_candidate_observed=(
            with_gamma.status == "bridge_candidate_observed_not_selected"
        ),
        generated_learned_category=with_gamma.generated_learned_category,
        selected_musical_interpretation=with_gamma.selected_musical_interpretation,
    )


def run_checks() -> None:
    comparison = compare_base_to_learned_bridge()
    assert comparison.same_response_difference is True
    assert comparison.same_external_candidates is True
    assert comparison.same_gamma is False
    assert comparison.bridge_candidate_observed is True
    assert comparison.generated_learned_category is None
    assert comparison.selected_musical_interpretation is None

    assert comparison.without_gamma.status == "underdetermined_without_bridge_gamma"
    assert comparison.with_gamma.status == "bridge_candidate_observed_not_selected"
    assert comparison.with_gamma.response_difference.generated_learned_category is None
    assert len(comparison.with_gamma.bridge_candidates) == 1
    assert (
        comparison.with_gamma.bridge_candidates[0].learned_candidate.label
        == "different_pitch_relation_label_candidate"
    )
    assert comparison.with_gamma.bridge_candidates[0].confirmed_learned_category is False
    assert all(
        candidate.generated_by_response_difference is False
        for candidate in comparison.with_gamma.external_learned_candidates
    )


def main() -> None:
    run_checks()
    comparison = compare_base_to_learned_bridge()
    observation = comparison.with_gamma

    print("[pipeline]")
    print("  human-side response difference")
    print("  + external learned category candidates")
    print("  + Gamma_base_to_learned_bridge_fixture")
    print("  -> bridge candidate observed")
    print("  -> selected musical interpretation remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={observation.status}")
    print(f"  same_response_difference={comparison.same_response_difference}")
    print(f"  same_external_candidates={comparison.same_external_candidates}")
    print(f"  bridge_candidate_observed={comparison.bridge_candidate_observed}")
    print(f"  generated_learned_category={comparison.generated_learned_category}")
    print(
        "  selected_musical_interpretation="
        f"{comparison.selected_musical_interpretation}"
    )
    print(
        "  bridge_candidates="
        + ", ".join(
            candidate.learned_candidate.label for candidate in observation.bridge_candidates
        )
    )


if __name__ == "__main__":
    main()
