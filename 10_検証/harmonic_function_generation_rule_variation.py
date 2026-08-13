"""同じfunction annotationで生成規則を変えた場合のtarget候補集合分岐。

46では、外部fixtureの生成規則を一つだけ置いた。
47では、同じfunction annotation candidateとkey contextに対して、
生成規則を差し替えるとtarget候補集合が変わることを確認する。

    same function annotation candidate
      + same key context
      + different Γ_target_candidate_generation_fixture
      -> different generated target candidate sets

生成結果はfunction annotationの属性ではない。
"""

from dataclasses import dataclass

from harmonic_function_target_candidate_boundary import TargetCandidate
from harmonic_function_target_generation_rule_boundary import (
    GeneratedTargetCandidateSet,
    TargetGenerationRule,
    build_function_observation,
)


@dataclass(frozen=True)
class RuleComparison:
    first: GeneratedTargetCandidateSet
    second: GeneratedTargetCandidateSet
    same_function_observation: bool
    same_key_context: bool
    same_generation_rule: bool
    same_candidate_set: bool


def fixture_generation_rules() -> tuple[TargetGenerationRule, TargetGenerationRule]:
    return (
        TargetGenerationRule(
            name="dominant_in_c_major_tonic_and_deceptive",
            rule_scope="fixture_limited_not_general_harmony",
        ),
        TargetGenerationRule(
            name="dominant_in_c_major_tonic_only",
            rule_scope="fixture_limited_not_general_harmony",
        ),
    )


def generate_with_variant_rule(
    generation_rule: TargetGenerationRule,
) -> GeneratedTargetCandidateSet:
    function_observation = build_function_observation()
    if (
        function_observation.function_annotation != "dominant_candidate"
        or function_observation.key_context.label != "C major"
    ):
        return GeneratedTargetCandidateSet(
            function_observation=function_observation,
            generation_rule=generation_rule,
            candidates=tuple(),
            generated_by_function_annotation_alone=False,
            status="rule_not_applicable",
        )

    if generation_rule.name == "dominant_in_c_major_tonic_and_deceptive":
        candidates = (
            TargetCandidate(
                label="fixture primary tonic resolution candidate",
                target_chord="C major",
                source="generated_fixture_primary",
            ),
            TargetCandidate(
                label="fixture deceptive resolution candidate",
                target_chord="A minor",
                source="generated_fixture_alternative",
            ),
        )
    elif generation_rule.name == "dominant_in_c_major_tonic_only":
        candidates = (
            TargetCandidate(
                label="fixture tonic-only resolution candidate",
                target_chord="C major",
                source="generated_fixture_tonic_only",
            ),
        )
    else:
        raise ValueError(f"unknown target generation rule: {generation_rule.name}")

    return GeneratedTargetCandidateSet(
        function_observation=function_observation,
        generation_rule=generation_rule,
        candidates=candidates,
        generated_by_function_annotation_alone=False,
        status="generated_candidate_set",
    )


def compare_rules() -> RuleComparison:
    first_rule, second_rule = fixture_generation_rules()
    first = generate_with_variant_rule(first_rule)
    second = generate_with_variant_rule(second_rule)
    return RuleComparison(
        first=first,
        second=second,
        same_function_observation=first.function_observation == second.function_observation,
        same_key_context=(
            first.function_observation.key_context
            == second.function_observation.key_context
        ),
        same_generation_rule=first.generation_rule == second.generation_rule,
        same_candidate_set=first.candidates == second.candidates,
    )


def run_checks() -> None:
    comparison = compare_rules()
    assert comparison.same_function_observation is True
    assert comparison.same_key_context is True
    assert comparison.same_generation_rule is False
    assert comparison.same_candidate_set is False

    assert comparison.first.status == "generated_candidate_set"
    assert comparison.second.status == "generated_candidate_set"
    assert comparison.first.generated_by_function_annotation_alone is False
    assert comparison.second.generated_by_function_annotation_alone is False

    assert tuple(candidate.target_chord for candidate in comparison.first.candidates) == (
        "C major",
        "A minor",
    )
    assert tuple(candidate.target_chord for candidate in comparison.second.candidates) == (
        "C major",
    )


def main() -> None:
    run_checks()
    comparison = compare_rules()
    first_rule = comparison.first.generation_rule
    second_rule = comparison.second.generation_rule

    print("[pipeline]")
    print("  same function annotation candidate")
    print("  + same key context")
    print("  + different Gamma_target_candidate_generation_fixture")
    print("  -> different generated target candidate sets")
    print(f"  same_function_observation={comparison.same_function_observation}")
    print(f"  same_key_context={comparison.same_key_context}")
    print(f"  first_rule={first_rule.name if first_rule else None}")
    print("  first_candidates=" + ", ".join(
        candidate.target_chord for candidate in comparison.first.candidates
    ))
    print(f"  second_rule={second_rule.name if second_rule else None}")
    print("  second_candidates=" + ", ".join(
        candidate.target_chord for candidate in comparison.second.candidates
    ))
    print(f"  same_candidate_set={comparison.same_candidate_set}")


if __name__ == "__main__":
    main()
