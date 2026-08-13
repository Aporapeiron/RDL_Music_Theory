"""同じfunction annotationと生成規則でkey contextを変えた場合の候補集合分岐。

47では、同じfunction annotation candidateと同じkey contextに対して、
生成規則を差し替えるとtarget候補集合が変わることを確認した。

48では、function annotation labelと生成規則を固定し、
key contextを変えるとtarget候補集合が変わることを確認する。

    same function annotation label
      + different key context
      + same context-sensitive Γ_target_candidate_generation_fixture
      -> different generated target candidate sets

生成結果はfunction annotation labelの属性ではない。
"""

from dataclasses import dataclass

from harmonic_function_key_context_branch import (
    FunctionObservation,
    KeyContext,
    annotate_function,
    make_major_triad,
)
from harmonic_function_target_candidate_boundary import TargetCandidate
from harmonic_function_target_generation_rule_boundary import (
    GeneratedTargetCandidateSet,
    TargetGenerationRule,
)


@dataclass(frozen=True)
class ContextComparison:
    first: GeneratedTargetCandidateSet
    second: GeneratedTargetCandidateSet
    same_function_annotation: bool
    same_key_context: bool
    same_generation_rule: bool
    same_candidate_set: bool


def context_sensitive_fixture_rule() -> TargetGenerationRule:
    return TargetGenerationRule(
        name="context_sensitive_dominant_fixture_targets",
        rule_scope="fixture_limited_not_general_harmony",
    )


def build_dominant_observations() -> tuple[FunctionObservation, FunctionObservation]:
    in_c_major = annotate_function(make_major_triad("G"), KeyContext("C major", "C"))
    in_g_major = annotate_function(make_major_triad("D"), KeyContext("G major", "G"))
    return in_c_major, in_g_major


def generate_with_context_sensitive_rule(
    function_observation: FunctionObservation,
    generation_rule: TargetGenerationRule,
) -> GeneratedTargetCandidateSet:
    if generation_rule.name != "context_sensitive_dominant_fixture_targets":
        raise ValueError(f"unknown target generation rule: {generation_rule.name}")

    if function_observation.function_annotation != "dominant_candidate":
        return GeneratedTargetCandidateSet(
            function_observation=function_observation,
            generation_rule=generation_rule,
            candidates=tuple(),
            generated_by_function_annotation_alone=False,
            status="rule_not_applicable",
        )

    if function_observation.key_context.label == "C major":
        candidates = (
            TargetCandidate(
                label="C major tonic resolution candidate",
                target_chord="C major",
                source="context_sensitive_fixture_primary",
            ),
            TargetCandidate(
                label="A minor deceptive resolution candidate",
                target_chord="A minor",
                source="context_sensitive_fixture_alternative",
            ),
        )
    elif function_observation.key_context.label == "G major":
        candidates = (
            TargetCandidate(
                label="G major tonic resolution candidate",
                target_chord="G major",
                source="context_sensitive_fixture_primary",
            ),
            TargetCandidate(
                label="E minor deceptive resolution candidate",
                target_chord="E minor",
                source="context_sensitive_fixture_alternative",
            ),
        )
    else:
        return GeneratedTargetCandidateSet(
            function_observation=function_observation,
            generation_rule=generation_rule,
            candidates=tuple(),
            generated_by_function_annotation_alone=False,
            status="context_not_supported_by_fixture",
        )

    return GeneratedTargetCandidateSet(
        function_observation=function_observation,
        generation_rule=generation_rule,
        candidates=candidates,
        generated_by_function_annotation_alone=False,
        status="generated_candidate_set",
    )


def compare_contexts() -> ContextComparison:
    rule = context_sensitive_fixture_rule()
    first_observation, second_observation = build_dominant_observations()
    first = generate_with_context_sensitive_rule(first_observation, rule)
    second = generate_with_context_sensitive_rule(second_observation, rule)
    return ContextComparison(
        first=first,
        second=second,
        same_function_annotation=(
            first.function_observation.function_annotation
            == second.function_observation.function_annotation
        ),
        same_key_context=(
            first.function_observation.key_context
            == second.function_observation.key_context
        ),
        same_generation_rule=first.generation_rule == second.generation_rule,
        same_candidate_set=first.candidates == second.candidates,
    )


def run_checks() -> None:
    comparison = compare_contexts()
    assert comparison.same_function_annotation is True
    assert comparison.same_key_context is False
    assert comparison.same_generation_rule is True
    assert comparison.same_candidate_set is False

    assert comparison.first.status == "generated_candidate_set"
    assert comparison.second.status == "generated_candidate_set"
    assert comparison.first.generated_by_function_annotation_alone is False
    assert comparison.second.generated_by_function_annotation_alone is False

    assert comparison.first.function_observation.key_context.label == "C major"
    assert comparison.second.function_observation.key_context.label == "G major"
    assert comparison.first.function_observation.function_annotation == "dominant_candidate"
    assert comparison.second.function_observation.function_annotation == "dominant_candidate"

    assert tuple(candidate.target_chord for candidate in comparison.first.candidates) == (
        "C major",
        "A minor",
    )
    assert tuple(candidate.target_chord for candidate in comparison.second.candidates) == (
        "G major",
        "E minor",
    )


def main() -> None:
    run_checks()
    comparison = compare_contexts()
    rule = comparison.first.generation_rule

    print("[pipeline]")
    print("  same function annotation label")
    print("  + different key context")
    print("  + same context-sensitive Gamma_target_candidate_generation_fixture")
    print("  -> different generated target candidate sets")
    print(f"  same_function_annotation={comparison.same_function_annotation}")
    print(f"  same_key_context={comparison.same_key_context}")
    print(f"  same_generation_rule={comparison.same_generation_rule}")
    print(f"  generation_rule={rule.name if rule else None}")
    print(
        "  first_context="
        f"{comparison.first.function_observation.key_context.label}"
    )
    print("  first_candidates=" + ", ".join(
        candidate.target_chord for candidate in comparison.first.candidates
    ))
    print(
        "  second_context="
        f"{comparison.second.function_observation.key_context.label}"
    )
    print("  second_candidates=" + ", ".join(
        candidate.target_chord for candidate in comparison.second.candidates
    ))
    print(f"  same_candidate_set={comparison.same_candidate_set}")


if __name__ == "__main__":
    main()
