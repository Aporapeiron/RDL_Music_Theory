"""history粒度差によるtarget候補集合分岐の最小検証。

49では、same current function observation + same Γで、
history.local_patternを変えるとtarget候補集合が変わることを確認した。

50では、同じhistory broad patternの中でもlocal_patternが変わると、
同じ生成規則でcandidate setが変わることを確認する。

    same current function observation
      + same Γ_target_candidate_generation_fixture
      + same history.broad_pattern
      + different history.local_pattern
      -> different generated target candidate sets

historyの大分類は、今回のfixtureでΓが読む粒度を代替しない。
"""

from dataclasses import dataclass

from harmonic_function_target_candidate_boundary import TargetCandidate
from harmonic_function_target_generation_rule_boundary import (
    GeneratedTargetCandidateSet,
    TargetGenerationRule,
    build_function_observation,
)


@dataclass(frozen=True)
class GranularHarmonicHistory:
    label: str
    prior_context: str
    broad_pattern: str
    local_pattern: str


@dataclass(frozen=True)
class GranularHistoryGeneratedSet:
    generated: GeneratedTargetCandidateSet
    history: GranularHarmonicHistory


@dataclass(frozen=True)
class GranularityComparison:
    first: GranularHistoryGeneratedSet
    second: GranularHistoryGeneratedSet
    same_function_observation: bool
    same_generation_rule: bool
    same_broad_pattern: bool
    same_local_pattern: bool
    same_candidate_set: bool


def local_pattern_sensitive_fixture_rule() -> TargetGenerationRule:
    return TargetGenerationRule(
        name="local_pattern_sensitive_dominant_fixture_targets",
        rule_scope="fixture_limited_not_general_harmony",
    )


def fixture_histories() -> tuple[GranularHarmonicHistory, GranularHarmonicHistory]:
    return (
        GranularHarmonicHistory(
            label="dominant preparation with ordinary local pattern",
            prior_context="C major",
            broad_pattern="dominant_preparation",
            local_pattern="ordinary_preparation",
        ),
        GranularHarmonicHistory(
            label="dominant preparation with deceptive local pattern",
            prior_context="C major",
            broad_pattern="dominant_preparation",
            local_pattern="deceptive_setup",
        ),
    )


def generate_with_granular_history(
    generation_rule: TargetGenerationRule,
    history: GranularHarmonicHistory,
) -> GranularHistoryGeneratedSet:
    function_observation = build_function_observation()
    if generation_rule.name != "local_pattern_sensitive_dominant_fixture_targets":
        raise ValueError(f"unknown target generation rule: {generation_rule.name}")

    if (
        function_observation.function_annotation != "dominant_candidate"
        or function_observation.key_context.label != "C major"
        or history.broad_pattern != "dominant_preparation"
    ):
        generated = GeneratedTargetCandidateSet(
            function_observation=function_observation,
            generation_rule=generation_rule,
            candidates=tuple(),
            generated_by_function_annotation_alone=False,
            status="rule_not_applicable",
        )
        return GranularHistoryGeneratedSet(generated=generated, history=history)

    if history.local_pattern == "ordinary_preparation":
        candidates = (
            TargetCandidate(
                label="local-pattern tonic resolution candidate",
                target_chord="C major",
                source="granularity_fixture_primary",
            ),
        )
    elif history.local_pattern == "deceptive_setup":
        candidates = (
            TargetCandidate(
                label="local-pattern tonic resolution candidate",
                target_chord="C major",
                source="granularity_fixture_primary",
            ),
            TargetCandidate(
                label="local-pattern deceptive resolution candidate",
                target_chord="A minor",
                source="granularity_fixture_deceptive",
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
        return GranularHistoryGeneratedSet(generated=generated, history=history)

    generated = GeneratedTargetCandidateSet(
        function_observation=function_observation,
        generation_rule=generation_rule,
        candidates=candidates,
        generated_by_function_annotation_alone=False,
        status="generated_candidate_set",
    )
    return GranularHistoryGeneratedSet(generated=generated, history=history)


def compare_history_granularity() -> GranularityComparison:
    rule = local_pattern_sensitive_fixture_rule()
    first_history, second_history = fixture_histories()
    first = generate_with_granular_history(rule, first_history)
    second = generate_with_granular_history(rule, second_history)
    return GranularityComparison(
        first=first,
        second=second,
        same_function_observation=(
            first.generated.function_observation
            == second.generated.function_observation
        ),
        same_generation_rule=(
            first.generated.generation_rule == second.generated.generation_rule
        ),
        same_broad_pattern=first.history.broad_pattern == second.history.broad_pattern,
        same_local_pattern=first.history.local_pattern == second.history.local_pattern,
        same_candidate_set=first.generated.candidates == second.generated.candidates,
    )


def run_checks() -> None:
    comparison = compare_history_granularity()
    assert comparison.same_function_observation is True
    assert comparison.same_generation_rule is True
    assert comparison.same_broad_pattern is True
    assert comparison.same_local_pattern is False
    assert comparison.same_candidate_set is False

    assert comparison.first.generated.status == "generated_candidate_set"
    assert comparison.second.generated.status == "generated_candidate_set"
    assert comparison.first.generated.generated_by_function_annotation_alone is False
    assert comparison.second.generated.generated_by_function_annotation_alone is False

    assert tuple(candidate.target_chord for candidate in comparison.first.generated.candidates) == (
        "C major",
    )
    assert tuple(candidate.target_chord for candidate in comparison.second.generated.candidates) == (
        "C major",
        "A minor",
    )


def main() -> None:
    run_checks()
    comparison = compare_history_granularity()
    rule = comparison.first.generated.generation_rule

    print("[pipeline]")
    print("  same current function observation")
    print("  + same local-pattern-sensitive Gamma_target_candidate_generation_fixture")
    print("  + same history.broad_pattern")
    print("  + different history.local_pattern")
    print("  -> different generated target candidate sets")
    print(f"  same_function_observation={comparison.same_function_observation}")
    print(f"  same_generation_rule={comparison.same_generation_rule}")
    print(f"  same_broad_pattern={comparison.same_broad_pattern}")
    print(f"  same_local_pattern={comparison.same_local_pattern}")
    print(f"  generation_rule={rule.name if rule else None}")
    print(f"  first_history={comparison.first.history.label}")
    print("  first_candidates=" + ", ".join(
        candidate.target_chord for candidate in comparison.first.generated.candidates
    ))
    print(f"  second_history={comparison.second.history.label}")
    print("  second_candidates=" + ", ".join(
        candidate.target_chord for candidate in comparison.second.generated.candidates
    ))
    print(f"  same_candidate_set={comparison.same_candidate_set}")


if __name__ == "__main__":
    main()
