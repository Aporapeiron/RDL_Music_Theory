"""function annotationとtarget候補生成規則を分離する最小検証。

43では、target候補集合を外部入力として与えた。
46では、外部に与えた限定的な生成規則からtarget候補集合を作る。

    function annotation candidate
      + key context
      + Γ_target_candidate_generation_fixture
      -> generated target candidate set

function annotationは生成規則そのものではない。
生成されたtarget候補集合も、selected targetではない。
"""

from dataclasses import dataclass

from harmonic_function_key_context_branch import (
    FunctionObservation,
    KeyContext,
    annotate_function,
    make_major_triad,
)
from harmonic_function_target_candidate_boundary import TargetCandidate


@dataclass(frozen=True)
class TargetGenerationRule:
    name: str
    rule_scope: str


@dataclass(frozen=True)
class GeneratedTargetCandidateSet:
    function_observation: FunctionObservation
    generation_rule: TargetGenerationRule | None
    candidates: tuple[TargetCandidate, ...]
    generated_by_function_annotation_alone: bool
    status: str


def build_function_observation() -> FunctionObservation:
    return annotate_function(make_major_triad("G"), KeyContext("C major", "C"))


def fixture_target_generation_rule() -> TargetGenerationRule:
    return TargetGenerationRule(
        name="dominant_in_c_major_fixture_targets",
        rule_scope="fixture_limited_not_general_harmony",
    )


def generate_target_candidates_with_rule(
    function_observation: FunctionObservation,
    generation_rule: TargetGenerationRule | None,
) -> GeneratedTargetCandidateSet:
    if generation_rule is None:
        return GeneratedTargetCandidateSet(
            function_observation=function_observation,
            generation_rule=None,
            candidates=tuple(),
            generated_by_function_annotation_alone=False,
            status="no_generation_rule",
        )

    if generation_rule.name != "dominant_in_c_major_fixture_targets":
        raise ValueError(f"unknown target generation rule: {generation_rule.name}")

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
    return GeneratedTargetCandidateSet(
        function_observation=function_observation,
        generation_rule=generation_rule,
        candidates=candidates,
        generated_by_function_annotation_alone=False,
        status="generated_candidate_set",
    )


def run_checks() -> None:
    function_observation = build_function_observation()
    assert function_observation.function_annotation == "dominant_candidate"
    assert function_observation.key_context.label == "C major"
    assert function_observation.generated_target is None

    without_rule = generate_target_candidates_with_rule(function_observation, None)
    assert without_rule.status == "no_generation_rule"
    assert without_rule.generation_rule is None
    assert without_rule.candidates == tuple()
    assert without_rule.generated_by_function_annotation_alone is False

    rule = fixture_target_generation_rule()
    generated = generate_target_candidates_with_rule(function_observation, rule)
    assert generated.status == "generated_candidate_set"
    assert generated.generation_rule == rule
    assert generated.generated_by_function_annotation_alone is False
    assert tuple(candidate.target_chord for candidate in generated.candidates) == (
        "C major",
        "A minor",
    )
    assert tuple(candidate.source for candidate in generated.candidates) == (
        "generated_fixture_primary",
        "generated_fixture_alternative",
    )

    g_major_tonic = annotate_function(make_major_triad("G"), KeyContext("G major", "G"))
    not_applicable = generate_target_candidates_with_rule(g_major_tonic, rule)
    assert not_applicable.status == "rule_not_applicable"
    assert not_applicable.candidates == tuple()

    # function annotation、生成規則、生成済み候補集合は別物として保持する。
    assert generated.function_observation.function_annotation == "dominant_candidate"
    assert generated.generation_rule.name == "dominant_in_c_major_fixture_targets"
    assert generated.candidates != tuple()


def main() -> None:
    run_checks()
    function_observation = build_function_observation()
    without_rule = generate_target_candidates_with_rule(function_observation, None)
    rule = fixture_target_generation_rule()
    generated = generate_target_candidates_with_rule(function_observation, rule)

    print("[pipeline]")
    print("  function annotation candidate")
    print("  + key context")
    print("  + externally supplied Gamma_target_candidate_generation_fixture")
    print("  -> generated target candidate set")
    print(f"  function_annotation={function_observation.function_annotation}")
    print(f"  key_context={function_observation.key_context.label}")
    print(f"  without_rule={without_rule.status}")
    print(f"  generation_rule={generated.generation_rule.name if generated.generation_rule else None}")
    print(f"  rule_scope={generated.generation_rule.rule_scope if generated.generation_rule else None}")
    print(f"  generated_by_function_annotation_alone={generated.generated_by_function_annotation_alone}")
    print("  candidates=" + ", ".join(candidate.target_chord for candidate in generated.candidates))


if __name__ == "__main__":
    main()


