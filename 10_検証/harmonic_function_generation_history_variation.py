"""同じfunction observationと生成規則でhistoryを変えた場合の候補集合分岐。

46〜48では、target候補集合がfunction annotation単独ではなく、
function observationとΓ_generationの関係として生じることを確認した。

49では、同じcurrent function observationと同じ生成規則を固定し、
historyだけを差し替えるとtarget候補集合が変わることを確認する。

    same current function observation
      + same Γ_target_candidate_generation_fixture
      + different history
      -> different generated target candidate sets

historyはselected targetではなく、候補生成の追加入力として扱う。
"""

from dataclasses import dataclass

from harmonic_function_target_candidate_boundary import TargetCandidate
from harmonic_function_target_generation_rule_boundary import (
    GeneratedTargetCandidateSet,
    TargetGenerationRule,
    build_function_observation,
)


@dataclass(frozen=True)
class HarmonicHistory:
    label: str
    prior_context: str
    local_pattern: str


@dataclass(frozen=True)
class HistoryGeneratedTargetCandidateSet:
    generated: GeneratedTargetCandidateSet
    history: HarmonicHistory


@dataclass(frozen=True)
class HistoryComparison:
    first: HistoryGeneratedTargetCandidateSet
    second: HistoryGeneratedTargetCandidateSet
    same_function_observation: bool
    same_generation_rule: bool
    same_history: bool
    same_candidate_set: bool


def history_sensitive_fixture_rule() -> TargetGenerationRule:
    return TargetGenerationRule(
        name="history_sensitive_dominant_fixture_targets",
        rule_scope="fixture_limited_not_general_harmony",
    )


def fixture_histories() -> tuple[HarmonicHistory, HarmonicHistory]:
    return (
        HarmonicHistory(
            label="ordinary dominant preparation",
            prior_context="C major",
            local_pattern="ordinary_preparation",
        ),
        HarmonicHistory(
            label="deceptive setup",
            prior_context="C major",
            local_pattern="deceptive_setup",
        ),
    )


def generate_with_history(
    generation_rule: TargetGenerationRule,
    history: HarmonicHistory,
) -> HistoryGeneratedTargetCandidateSet:
    function_observation = build_function_observation()
    if generation_rule.name != "history_sensitive_dominant_fixture_targets":
        raise ValueError(f"unknown target generation rule: {generation_rule.name}")

    if (
        function_observation.function_annotation != "dominant_candidate"
        or function_observation.key_context.label != "C major"
    ):
        generated = GeneratedTargetCandidateSet(
            function_observation=function_observation,
            generation_rule=generation_rule,
            candidates=tuple(),
            generated_by_function_annotation_alone=False,
            status="rule_not_applicable",
        )
        return HistoryGeneratedTargetCandidateSet(generated=generated, history=history)

    if history.local_pattern == "ordinary_preparation":
        candidates = (
            TargetCandidate(
                label="history-sensitive tonic resolution candidate",
                target_chord="C major",
                source="history_fixture_primary",
            ),
        )
    elif history.local_pattern == "deceptive_setup":
        candidates = (
            TargetCandidate(
                label="history-sensitive tonic resolution candidate",
                target_chord="C major",
                source="history_fixture_primary",
            ),
            TargetCandidate(
                label="history-sensitive deceptive resolution candidate",
                target_chord="A minor",
                source="history_fixture_deceptive",
            ),
        )
    else:
        return HistoryGeneratedTargetCandidateSet(
            generated=GeneratedTargetCandidateSet(
                function_observation=function_observation,
                generation_rule=generation_rule,
                candidates=tuple(),
                generated_by_function_annotation_alone=False,
                status="history_not_supported_by_fixture",
            ),
            history=history,
        )

    generated = GeneratedTargetCandidateSet(
        function_observation=function_observation,
        generation_rule=generation_rule,
        candidates=candidates,
        generated_by_function_annotation_alone=False,
        status="generated_candidate_set",
    )
    return HistoryGeneratedTargetCandidateSet(generated=generated, history=history)


def compare_histories() -> HistoryComparison:
    rule = history_sensitive_fixture_rule()
    first_history, second_history = fixture_histories()
    first = generate_with_history(rule, first_history)
    second = generate_with_history(rule, second_history)
    return HistoryComparison(
        first=first,
        second=second,
        same_function_observation=(
            first.generated.function_observation
            == second.generated.function_observation
        ),
        same_generation_rule=(
            first.generated.generation_rule == second.generated.generation_rule
        ),
        same_history=first.history == second.history,
        same_candidate_set=first.generated.candidates == second.generated.candidates,
    )


def run_checks() -> None:
    comparison = compare_histories()
    assert comparison.same_function_observation is True
    assert comparison.same_generation_rule is True
    assert comparison.same_history is False
    assert comparison.same_candidate_set is False

    assert comparison.first.generated.status == "generated_candidate_set"
    assert comparison.second.generated.status == "generated_candidate_set"
    assert comparison.first.generated.generated_by_function_annotation_alone is False
    assert comparison.second.generated.generated_by_function_annotation_alone is False

    assert comparison.first.generated.function_observation.function_annotation == "dominant_candidate"
    assert comparison.first.generated.function_observation.key_context.label == "C major"
    assert comparison.second.generated.function_observation == comparison.first.generated.function_observation

    assert tuple(candidate.target_chord for candidate in comparison.first.generated.candidates) == (
        "C major",
    )
    assert tuple(candidate.target_chord for candidate in comparison.second.generated.candidates) == (
        "C major",
        "A minor",
    )


def main() -> None:
    run_checks()
    comparison = compare_histories()
    rule = comparison.first.generated.generation_rule

    print("[pipeline]")
    print("  same current function observation")
    print("  + same history-sensitive Gamma_target_candidate_generation_fixture")
    print("  + different history")
    print("  -> different generated target candidate sets")
    print(f"  same_function_observation={comparison.same_function_observation}")
    print(f"  same_generation_rule={comparison.same_generation_rule}")
    print(f"  same_history={comparison.same_history}")
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
