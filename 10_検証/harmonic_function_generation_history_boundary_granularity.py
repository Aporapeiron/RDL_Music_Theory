"""B_historyの粒度差によるtarget候補集合分岐の最小検証。

50では、同一history大分類内のlocal_pattern差がcandidate setへ影響することを確認した。
51では、同じunderlying historyに対してB_historyを差し替え、
coarse representationとfine representationでΓが読める特徴が変わることを確認する。

    same underlying history
      -> B_history_coarse -> coarse representation
      -> B_history_fine   -> fine representation

    same current function observation
      + same Γ_target_candidate_generation_fixture
      + different history representation under B_history
      -> different generated target candidate sets

underlying historyはhistory representation under Bと同一ではない。
"""

from dataclasses import dataclass

from harmonic_function_target_candidate_boundary import TargetCandidate
from harmonic_function_target_generation_rule_boundary import (
    GeneratedTargetCandidateSet,
    TargetGenerationRule,
    build_function_observation,
)


@dataclass(frozen=True)
class UnderlyingHistory:
    label: str
    prior_context: str
    broad_pattern: str
    local_pattern: str


@dataclass(frozen=True)
class HistoryBoundary:
    name: str
    exposes_broad_pattern: bool
    exposes_local_pattern: bool


@dataclass(frozen=True)
class HistoryRepresentation:
    boundary: HistoryBoundary
    prior_context: str
    broad_pattern: str | None
    local_pattern: str | None


@dataclass(frozen=True)
class BoundaryGeneratedSet:
    generated: GeneratedTargetCandidateSet
    underlying_history: UnderlyingHistory
    history_representation: HistoryRepresentation


@dataclass(frozen=True)
class BoundaryGranularityComparison:
    first: BoundaryGeneratedSet
    second: BoundaryGeneratedSet
    same_underlying_history: bool
    same_function_observation: bool
    same_generation_rule: bool
    same_history_representation: bool
    same_candidate_set: bool


def fixture_underlying_history() -> UnderlyingHistory:
    return UnderlyingHistory(
        label="underlying deceptive dominant preparation",
        prior_context="C major",
        broad_pattern="dominant_preparation",
        local_pattern="deceptive_setup",
    )


def history_boundaries() -> tuple[HistoryBoundary, HistoryBoundary]:
    return (
        HistoryBoundary(
            name="B_history_coarse",
            exposes_broad_pattern=True,
            exposes_local_pattern=False,
        ),
        HistoryBoundary(
            name="B_history_fine",
            exposes_broad_pattern=True,
            exposes_local_pattern=True,
        ),
    )


def project_history(
    underlying_history: UnderlyingHistory,
    boundary: HistoryBoundary,
) -> HistoryRepresentation:
    return HistoryRepresentation(
        boundary=boundary,
        prior_context=underlying_history.prior_context,
        broad_pattern=(
            underlying_history.broad_pattern if boundary.exposes_broad_pattern else None
        ),
        local_pattern=(
            underlying_history.local_pattern if boundary.exposes_local_pattern else None
        ),
    )


def boundary_sensitive_fixture_rule() -> TargetGenerationRule:
    return TargetGenerationRule(
        name="history_boundary_sensitive_dominant_fixture_targets",
        rule_scope="fixture_limited_not_general_harmony",
    )


def generate_with_history_representation(
    generation_rule: TargetGenerationRule,
    underlying_history: UnderlyingHistory,
    representation: HistoryRepresentation,
) -> BoundaryGeneratedSet:
    function_observation = build_function_observation()
    if generation_rule.name != "history_boundary_sensitive_dominant_fixture_targets":
        raise ValueError(f"unknown target generation rule: {generation_rule.name}")

    if (
        function_observation.function_annotation != "dominant_candidate"
        or function_observation.key_context.label != "C major"
        or representation.broad_pattern != "dominant_preparation"
    ):
        generated = GeneratedTargetCandidateSet(
            function_observation=function_observation,
            generation_rule=generation_rule,
            candidates=tuple(),
            generated_by_function_annotation_alone=False,
            status="rule_not_applicable",
        )
        return BoundaryGeneratedSet(
            generated=generated,
            underlying_history=underlying_history,
            history_representation=representation,
        )

    if representation.local_pattern == "deceptive_setup":
        candidates = (
            TargetCandidate(
                label="fine-history tonic resolution candidate",
                target_chord="C major",
                source="history_boundary_fixture_primary",
            ),
            TargetCandidate(
                label="fine-history deceptive resolution candidate",
                target_chord="A minor",
                source="history_boundary_fixture_deceptive",
            ),
        )
    elif representation.local_pattern is None:
        candidates = (
            TargetCandidate(
                label="coarse-history broad dominant candidate",
                target_chord="C major",
                source="history_boundary_fixture_broad",
            ),
        )
    else:
        generated = GeneratedTargetCandidateSet(
            function_observation=function_observation,
            generation_rule=generation_rule,
            candidates=tuple(),
            generated_by_function_annotation_alone=False,
            status="local_pattern_not_supported_by_fixture",
        )
        return BoundaryGeneratedSet(
            generated=generated,
            underlying_history=underlying_history,
            history_representation=representation,
        )

    generated = GeneratedTargetCandidateSet(
        function_observation=function_observation,
        generation_rule=generation_rule,
        candidates=candidates,
        generated_by_function_annotation_alone=False,
        status="generated_candidate_set",
    )
    return BoundaryGeneratedSet(
        generated=generated,
        underlying_history=underlying_history,
        history_representation=representation,
    )


def compare_history_boundaries() -> BoundaryGranularityComparison:
    underlying_history = fixture_underlying_history()
    coarse_boundary, fine_boundary = history_boundaries()
    rule = boundary_sensitive_fixture_rule()
    first = generate_with_history_representation(
        rule,
        underlying_history,
        project_history(underlying_history, coarse_boundary),
    )
    second = generate_with_history_representation(
        rule,
        underlying_history,
        project_history(underlying_history, fine_boundary),
    )
    return BoundaryGranularityComparison(
        first=first,
        second=second,
        same_underlying_history=first.underlying_history == second.underlying_history,
        same_function_observation=(
            first.generated.function_observation
            == second.generated.function_observation
        ),
        same_generation_rule=(
            first.generated.generation_rule == second.generated.generation_rule
        ),
        same_history_representation=(
            first.history_representation == second.history_representation
        ),
        same_candidate_set=first.generated.candidates == second.generated.candidates,
    )


def run_checks() -> None:
    comparison = compare_history_boundaries()
    assert comparison.same_underlying_history is True
    assert comparison.same_function_observation is True
    assert comparison.same_generation_rule is True
    assert comparison.same_history_representation is False
    assert comparison.same_candidate_set is False

    assert comparison.first.history_representation.boundary.name == "B_history_coarse"
    assert comparison.first.history_representation.broad_pattern == "dominant_preparation"
    assert comparison.first.history_representation.local_pattern is None

    assert comparison.second.history_representation.boundary.name == "B_history_fine"
    assert comparison.second.history_representation.broad_pattern == "dominant_preparation"
    assert comparison.second.history_representation.local_pattern == "deceptive_setup"

    assert tuple(candidate.target_chord for candidate in comparison.first.generated.candidates) == (
        "C major",
    )
    assert tuple(candidate.target_chord for candidate in comparison.second.generated.candidates) == (
        "C major",
        "A minor",
    )


def main() -> None:
    run_checks()
    comparison = compare_history_boundaries()
    rule = comparison.first.generated.generation_rule

    print("[pipeline]")
    print("  same underlying history")
    print("  -> different B_history representations")
    print("  + same current function observation")
    print("  + same history-boundary-sensitive Gamma_target_candidate_generation_fixture")
    print("  -> different generated target candidate sets")
    print(f"  same_underlying_history={comparison.same_underlying_history}")
    print(f"  same_function_observation={comparison.same_function_observation}")
    print(f"  same_generation_rule={comparison.same_generation_rule}")
    print(f"  same_history_representation={comparison.same_history_representation}")
    print(f"  generation_rule={rule.name if rule else None}")
    print(f"  first_boundary={comparison.first.history_representation.boundary.name}")
    print("  first_candidates=" + ", ".join(
        candidate.target_chord for candidate in comparison.first.generated.candidates
    ))
    print(f"  second_boundary={comparison.second.history_representation.boundary.name}")
    print("  second_candidates=" + ", ".join(
        candidate.target_chord for candidate in comparison.second.generated.candidates
    ))
    print(f"  same_candidate_set={comparison.same_candidate_set}")


if __name__ == "__main__":
    main()
