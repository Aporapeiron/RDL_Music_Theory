"""bridge候補集合と優先順位付け境界を分離する最小検証。

57〜62で分けたbase-to-learned bridgeについて、複数bridge候補が
観測された後、Gamma_prioritizationを与えた場合だけordered candidatesが
生じることを確認する。selection / confirmationは生成しない。

    bridge candidates observed
      + Gamma_bridge_prioritization_fixture
      -> prioritized bridge ordering
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
    target_candidate_labels: tuple[str, ...]
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class BridgePrioritizationGamma:
    name: str
    preferred_label_order: tuple[str, ...]
    reads: tuple[str, ...]
    rule_scope: str


@dataclass(frozen=True)
class BridgeCandidate:
    response_difference: HumanSideResponseDifference
    learned_candidate: LearnedCategoryCandidate
    bridge_relation: str
    confirmed_learned_category: bool


@dataclass(frozen=True)
class PrioritizedBridgeCandidate:
    bridge_candidate: BridgeCandidate
    priority_rank: int
    selected_musical_interpretation: str | None
    confirmed_learned_category: bool


@dataclass(frozen=True)
class BridgeCandidateObservation:
    response_difference: HumanSideResponseDifference
    learned_candidates: tuple[LearnedCategoryCandidate, ...]
    bridge_gamma: BridgeGamma
    bridge_candidates: tuple[BridgeCandidate, ...]
    generated_learned_category: str | None
    selected_musical_interpretation: str | None
    status: str


@dataclass(frozen=True)
class BridgePrioritizationObservation:
    bridge_candidate_observation: BridgeCandidateObservation
    prioritization_gamma: BridgePrioritizationGamma | None
    prioritized_bridge_candidates: tuple[PrioritizedBridgeCandidate, ...]
    selected_musical_interpretation: str | None
    confirmed_learned_category: bool
    status: str


@dataclass(frozen=True)
class BridgePrioritizationComparison:
    without_prioritization: BridgePrioritizationObservation
    with_prioritization: BridgePrioritizationObservation
    same_bridge_candidates: bool
    same_prioritization_gamma: bool
    prioritized_ordering_observed: bool
    priority_rank_one_selected: bool
    selected_musical_interpretation: str | None
    confirmed_learned_category: bool


def a2_human_side_response_difference() -> HumanSideResponseDifference:
    return HumanSideResponseDifference(
        label="A2 behavioral discriminability difference",
        source_base_candidate="frequency_difference_to_behavioral_discriminability_candidate",
        response_axis="behavioral_discriminability",
        lower_response="low_discriminability",
        higher_response="high_discriminability",
        generated_learned_category=None,
    )


def learned_pitch_relation_candidates() -> tuple[LearnedCategoryCandidate, ...]:
    return (
        LearnedCategoryCandidate(
            label="same_pitch_relation_label_candidate",
            category_family="learned_pitch_relation_label",
            supplied_by="learned_pitch_relation_label_inventory_fixture",
            generated_by_response_difference=False,
        ),
        LearnedCategoryCandidate(
            label="different_pitch_relation_label_candidate",
            category_family="learned_pitch_relation_label",
            supplied_by="learned_pitch_relation_label_inventory_fixture",
            generated_by_response_difference=False,
        ),
        LearnedCategoryCandidate(
            label="uncertain_pitch_relation_label_candidate",
            category_family="learned_pitch_relation_label",
            supplied_by="learned_pitch_relation_label_inventory_fixture",
            generated_by_response_difference=False,
        ),
    )


def bridge_multi_candidate_gamma() -> BridgeGamma:
    return BridgeGamma(
        name="Gamma_bridge_multi_candidate_fixture",
        target_candidate_labels=(
            "different_pitch_relation_label_candidate",
            "uncertain_pitch_relation_label_candidate",
        ),
        reads=("human_side_response_difference", "learned_category_candidate_set"),
        rule_scope="fixture_limited_not_general_category_generation_rule",
    )


def bridge_prioritization_gamma() -> BridgePrioritizationGamma:
    return BridgePrioritizationGamma(
        name="Gamma_bridge_prioritization_label_preference_fixture",
        preferred_label_order=(
            "different_pitch_relation_label_candidate",
            "uncertain_pitch_relation_label_candidate",
        ),
        reads=("bridge_candidates",),
        rule_scope="fixture_limited_not_selection_controller",
    )


def observe_bridge_candidates(
    response_difference: HumanSideResponseDifference,
    learned_candidates: tuple[LearnedCategoryCandidate, ...],
    bridge_gamma: BridgeGamma,
) -> BridgeCandidateObservation:
    bridge_candidates = tuple(
        BridgeCandidate(
            response_difference=response_difference,
            learned_candidate=candidate,
            bridge_relation="compatible_bridge_candidate",
            confirmed_learned_category=False,
        )
        for candidate in learned_candidates
        if candidate.label in bridge_gamma.target_candidate_labels
    )

    if not bridge_candidates:
        return BridgeCandidateObservation(
            response_difference=response_difference,
            learned_candidates=learned_candidates,
            bridge_gamma=bridge_gamma,
            bridge_candidates=(),
            generated_learned_category=None,
            selected_musical_interpretation=None,
            status="no_bridge_candidate_observed",
        )

    return BridgeCandidateObservation(
        response_difference=response_difference,
        learned_candidates=learned_candidates,
        bridge_gamma=bridge_gamma,
        bridge_candidates=bridge_candidates,
        generated_learned_category=None,
        selected_musical_interpretation=None,
        status="bridge_candidates_observed_not_prioritized",
    )


def prioritize_bridge_candidates(
    bridge_observation: BridgeCandidateObservation,
    prioritization_gamma: BridgePrioritizationGamma | None,
) -> BridgePrioritizationObservation:
    if not bridge_observation.bridge_candidates:
        return BridgePrioritizationObservation(
            bridge_candidate_observation=bridge_observation,
            prioritization_gamma=prioritization_gamma,
            prioritized_bridge_candidates=(),
            selected_musical_interpretation=None,
            confirmed_learned_category=False,
            status="no_bridge_candidates_to_prioritize",
        )

    if prioritization_gamma is None:
        return BridgePrioritizationObservation(
            bridge_candidate_observation=bridge_observation,
            prioritization_gamma=None,
            prioritized_bridge_candidates=(),
            selected_musical_interpretation=None,
            confirmed_learned_category=False,
            status="bridge_candidates_observed_not_prioritized",
        )

    candidate_by_label = {
        candidate.learned_candidate.label: candidate
        for candidate in bridge_observation.bridge_candidates
    }
    prioritized = tuple(
        PrioritizedBridgeCandidate(
            bridge_candidate=candidate_by_label[label],
            priority_rank=rank,
            selected_musical_interpretation=None,
            confirmed_learned_category=False,
        )
        for rank, label in enumerate(prioritization_gamma.preferred_label_order, start=1)
        if label in candidate_by_label
    )

    return BridgePrioritizationObservation(
        bridge_candidate_observation=bridge_observation,
        prioritization_gamma=prioritization_gamma,
        prioritized_bridge_candidates=prioritized,
        selected_musical_interpretation=None,
        confirmed_learned_category=False,
        status="prioritized_bridge_ordering_observed_not_selected",
    )


def compare_bridge_prioritization() -> BridgePrioritizationComparison:
    bridge_observation = observe_bridge_candidates(
        response_difference=a2_human_side_response_difference(),
        learned_candidates=learned_pitch_relation_candidates(),
        bridge_gamma=bridge_multi_candidate_gamma(),
    )
    without_prioritization = prioritize_bridge_candidates(
        bridge_observation=bridge_observation,
        prioritization_gamma=None,
    )
    with_prioritization = prioritize_bridge_candidates(
        bridge_observation=bridge_observation,
        prioritization_gamma=bridge_prioritization_gamma(),
    )
    without_labels = tuple(
        candidate.learned_candidate.label
        for candidate in without_prioritization.bridge_candidate_observation.bridge_candidates
    )
    with_labels = tuple(
        candidate.learned_candidate.label
        for candidate in with_prioritization.bridge_candidate_observation.bridge_candidates
    )
    rank_one = with_prioritization.prioritized_bridge_candidates[0]
    return BridgePrioritizationComparison(
        without_prioritization=without_prioritization,
        with_prioritization=with_prioritization,
        same_bridge_candidates=(without_labels == with_labels),
        same_prioritization_gamma=(
            without_prioritization.prioritization_gamma
            == with_prioritization.prioritization_gamma
        ),
        prioritized_ordering_observed=(
            with_prioritization.status
            == "prioritized_bridge_ordering_observed_not_selected"
        ),
        priority_rank_one_selected=rank_one.selected_musical_interpretation is not None,
        selected_musical_interpretation=(
            with_prioritization.selected_musical_interpretation
        ),
        confirmed_learned_category=with_prioritization.confirmed_learned_category,
    )


def run_checks() -> None:
    comparison = compare_bridge_prioritization()
    assert comparison.same_bridge_candidates is True
    assert comparison.same_prioritization_gamma is False
    assert comparison.prioritized_ordering_observed is True
    assert comparison.priority_rank_one_selected is False
    assert comparison.selected_musical_interpretation is None
    assert comparison.confirmed_learned_category is False

    without = comparison.without_prioritization
    with_priority = comparison.with_prioritization
    assert without.status == "bridge_candidates_observed_not_prioritized"
    assert with_priority.status == "prioritized_bridge_ordering_observed_not_selected"
    assert len(without.bridge_candidate_observation.bridge_candidates) == 2
    assert len(with_priority.prioritized_bridge_candidates) == 2
    assert with_priority.prioritized_bridge_candidates[0].priority_rank == 1
    assert (
        with_priority.prioritized_bridge_candidates[0].bridge_candidate.learned_candidate.label
        == "different_pitch_relation_label_candidate"
    )
    assert (
        with_priority.prioritized_bridge_candidates[1].bridge_candidate.learned_candidate.label
        == "uncertain_pitch_relation_label_candidate"
    )
    assert all(
        candidate.confirmed_learned_category is False
        for candidate in with_priority.prioritized_bridge_candidates
    )
    assert all(
        candidate.selected_musical_interpretation is None
        for candidate in with_priority.prioritized_bridge_candidates
    )
    assert all(
        candidate.generated_by_response_difference is False
        for candidate in with_priority.bridge_candidate_observation.learned_candidates
    )


def main() -> None:
    run_checks()
    comparison = compare_bridge_prioritization()
    without = comparison.without_prioritization
    with_priority = comparison.with_prioritization

    print("[pipeline]")
    print("  bridge candidates observed")
    print("  + Gamma_bridge_prioritization_fixture")
    print("  -> prioritized bridge ordering")
    print("  -> selected musical interpretation remains None")
    print(f"  without_prioritization_status={without.status}")
    print(f"  with_prioritization_status={with_priority.status}")
    print(f"  same_bridge_candidates={comparison.same_bridge_candidates}")
    print(f"  same_prioritization_gamma={comparison.same_prioritization_gamma}")
    print(
        "  prioritized_ordering_observed="
        f"{comparison.prioritized_ordering_observed}"
    )
    print(f"  priority_rank_one_selected={comparison.priority_rank_one_selected}")
    print(
        "  selected_musical_interpretation="
        f"{comparison.selected_musical_interpretation}"
    )
    print(f"  confirmed_learned_category={comparison.confirmed_learned_category}")
    print(
        "  prioritized_bridge_candidates="
        + ", ".join(
            f"{candidate.priority_rank}:"
            f"{candidate.bridge_candidate.learned_candidate.label}"
            for candidate in with_priority.prioritized_bridge_candidates
        )
    )


if __name__ == "__main__":
    main()
