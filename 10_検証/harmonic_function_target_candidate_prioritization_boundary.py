"""target候補集合と優先順位付け境界の最小検証。

51で生成した同じfine-history candidate setを固定し、
prioritization policyだけを差し替える。

    same generated target candidate set
      + different Γ_target_candidate_prioritization_fixture
      -> different prioritized candidate ordering
      -> selected target remains ungenerated

generated candidate setはprioritized orderingでもselected targetでもない。
"""

from dataclasses import dataclass

from harmonic_function_generation_history_boundary_granularity import (
    BoundaryGeneratedSet,
    compare_history_boundaries,
)
from harmonic_function_target_candidate_boundary import TargetCandidate


@dataclass(frozen=True)
class PrioritizationPolicy:
    name: str
    rule_scope: str


@dataclass(frozen=True)
class PrioritizedTargetCandidate:
    candidate: TargetCandidate
    priority_rank: int
    priority_reason: str


@dataclass(frozen=True)
class PrioritizationObservation:
    generated_set: BoundaryGeneratedSet
    prioritization_policy: PrioritizationPolicy | None
    prioritized_candidates: tuple[PrioritizedTargetCandidate, ...]
    selected_target: TargetCandidate | None
    status: str


@dataclass(frozen=True)
class PrioritizationComparison:
    first: PrioritizationObservation
    second: PrioritizationObservation
    without_policy: PrioritizationObservation
    same_generated_candidate_set: bool
    same_prioritization_policy: bool
    same_prioritized_order: bool
    selected_target_generated: bool


def fine_history_generated_set() -> BoundaryGeneratedSet:
    return compare_history_boundaries().second


def prioritization_policies() -> tuple[PrioritizationPolicy, PrioritizationPolicy]:
    return (
        PrioritizationPolicy(
            name="prefer_primary_fixture",
            rule_scope="fixture_limited_not_general_harmony",
        ),
        PrioritizationPolicy(
            name="prefer_deceptive_fixture",
            rule_scope="fixture_limited_not_general_harmony",
        ),
    )


def priority_key(candidate: TargetCandidate, policy: PrioritizationPolicy) -> tuple[int, str]:
    if policy.name == "prefer_primary_fixture":
        if candidate.source == "history_boundary_fixture_primary":
            return (0, candidate.target_chord)
        if candidate.source == "history_boundary_fixture_deceptive":
            return (1, candidate.target_chord)
        return (2, candidate.target_chord)

    if policy.name == "prefer_deceptive_fixture":
        if candidate.source == "history_boundary_fixture_deceptive":
            return (0, candidate.target_chord)
        if candidate.source == "history_boundary_fixture_primary":
            return (1, candidate.target_chord)
        return (2, candidate.target_chord)

    raise ValueError(f"unknown prioritization policy: {policy.name}")


def priority_reason(candidate: TargetCandidate, policy: PrioritizationPolicy) -> str:
    if policy.name == "prefer_primary_fixture":
        return (
            "primary_source_preferred"
            if candidate.source == "history_boundary_fixture_primary"
            else "not_primary_source"
        )
    if policy.name == "prefer_deceptive_fixture":
        return (
            "deceptive_source_preferred"
            if candidate.source == "history_boundary_fixture_deceptive"
            else "not_deceptive_source"
        )
    raise ValueError(f"unknown prioritization policy: {policy.name}")


def prioritize_candidates(
    generated_set: BoundaryGeneratedSet,
    prioritization_policy: PrioritizationPolicy | None,
) -> PrioritizationObservation:
    if prioritization_policy is None:
        return PrioritizationObservation(
            generated_set=generated_set,
            prioritization_policy=None,
            prioritized_candidates=tuple(),
            selected_target=None,
            status="unprioritized_candidate_set",
        )

    ordered = sorted(
        generated_set.generated.candidates,
        key=lambda candidate: priority_key(candidate, prioritization_policy),
    )
    prioritized_candidates = tuple(
        PrioritizedTargetCandidate(
            candidate=candidate,
            priority_rank=index + 1,
            priority_reason=priority_reason(candidate, prioritization_policy),
        )
        for index, candidate in enumerate(ordered)
    )
    return PrioritizationObservation(
        generated_set=generated_set,
        prioritization_policy=prioritization_policy,
        prioritized_candidates=prioritized_candidates,
        selected_target=None,
        status="prioritized_candidate_set_selected_target_not_generated",
    )


def compare_prioritization_policies() -> PrioritizationComparison:
    generated_set = fine_history_generated_set()
    primary_policy, deceptive_policy = prioritization_policies()
    first = prioritize_candidates(generated_set, primary_policy)
    second = prioritize_candidates(generated_set, deceptive_policy)
    without_policy = prioritize_candidates(generated_set, None)
    return PrioritizationComparison(
        first=first,
        second=second,
        without_policy=without_policy,
        same_generated_candidate_set=(
            first.generated_set.generated.candidates
            == second.generated_set.generated.candidates
        ),
        same_prioritization_policy=(
            first.prioritization_policy == second.prioritization_policy
        ),
        same_prioritized_order=(
            tuple(item.candidate.target_chord for item in first.prioritized_candidates)
            == tuple(item.candidate.target_chord for item in second.prioritized_candidates)
        ),
        selected_target_generated=(
            first.selected_target is not None or second.selected_target is not None
        ),
    )


def run_checks() -> None:
    comparison = compare_prioritization_policies()
    assert comparison.same_generated_candidate_set is True
    assert comparison.same_prioritization_policy is False
    assert comparison.same_prioritized_order is False
    assert comparison.selected_target_generated is False

    assert comparison.without_policy.status == "unprioritized_candidate_set"
    assert comparison.without_policy.prioritized_candidates == tuple()
    assert comparison.without_policy.selected_target is None

    assert tuple(
        item.candidate.target_chord for item in comparison.first.prioritized_candidates
    ) == ("C major", "A minor")
    assert tuple(
        item.candidate.target_chord for item in comparison.second.prioritized_candidates
    ) == ("A minor", "C major")

    assert comparison.first.selected_target is None
    assert comparison.second.selected_target is None


def main() -> None:
    run_checks()
    comparison = compare_prioritization_policies()

    print("[pipeline]")
    print("  same generated target candidate set")
    print("  + different Gamma_target_candidate_prioritization_fixture")
    print("  -> different prioritized candidate ordering")
    print("  -> selected target remains ungenerated")
    print(f"  same_generated_candidate_set={comparison.same_generated_candidate_set}")
    print(f"  same_prioritization_policy={comparison.same_prioritization_policy}")
    print(f"  same_prioritized_order={comparison.same_prioritized_order}")
    print(f"  without_policy_status={comparison.without_policy.status}")
    print(
        "  first_policy="
        + (comparison.first.prioritization_policy.name if comparison.first.prioritization_policy else "None")
    )
    print(
        "  first_order="
        + ", ".join(
            item.candidate.target_chord for item in comparison.first.prioritized_candidates
        )
    )
    print(
        "  second_policy="
        + (comparison.second.prioritization_policy.name if comparison.second.prioritization_policy else "None")
    )
    print(
        "  second_order="
        + ", ".join(
            item.candidate.target_chord for item in comparison.second.prioritized_candidates
        )
    )
    print(f"  selected_target_generated={comparison.selected_target_generated}")


if __name__ == "__main__":
    main()