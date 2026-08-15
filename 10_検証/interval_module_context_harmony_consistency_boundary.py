"""音程Module next contextとharmonic annotation整合候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_harmonic_function_annotation_boundary import (
    HarmonicFunctionAnnotationObservation,
    compare_harmonic_function_annotation,
)
from interval_module_next_context_selection_boundary import (
    NextContextSelectionObservation,
    compare_next_context_selection,
)


@dataclass(frozen=True)
class ContextHarmonyConsistencyEvidence:
    name: str
    context_label: str
    compatible_function_tag: str
    generated_by_context_or_function: bool


@dataclass(frozen=True)
class ContextHarmonyConsistencyGamma:
    name: str
    reads: tuple[str, str, str]
    rule_scope: str


@dataclass(frozen=True)
class ContextHarmonyConsistencyCandidate:
    label: str
    selected_context_label: str
    harmonic_function_label: str
    selected: bool
    module_state_record_generated: bool


@dataclass(frozen=True)
class ContextHarmonyConsistencyObservation:
    next_context_observation: NextContextSelectionObservation
    harmonic_function_observation: HarmonicFunctionAnnotationObservation
    consistency_evidence: ContextHarmonyConsistencyEvidence | None
    gamma_consistency: ContextHarmonyConsistencyGamma | None
    consistency_candidates: tuple[ContextHarmonyConsistencyCandidate, ...]
    selected_consistency: ContextHarmonyConsistencyCandidate | None
    module_state_record_generated: bool
    core_promoted: bool
    status: str
    consistency_reason: str | None


@dataclass(frozen=True)
class ContextHarmonyConsistencyComparison:
    without_gamma: ContextHarmonyConsistencyObservation
    with_gamma: ContextHarmonyConsistencyObservation
    same_selected_next_context: bool
    same_harmonic_function_annotation: bool
    same_consistency_evidence: bool
    same_gamma_consistency: bool
    consistency_candidate_observed: bool
    selected_consistency_generated: bool
    module_state_record_generated: bool
    core_promoted: bool


def next_context_observation() -> NextContextSelectionObservation:
    return compare_next_context_selection().with_controller


def harmonic_function_observation() -> HarmonicFunctionAnnotationObservation:
    return compare_harmonic_function_annotation().with_gamma


def consistency_evidence_fixture() -> ContextHarmonyConsistencyEvidence:
    return ContextHarmonyConsistencyEvidence(
        name="C_major_tonic_support_consistency_evidence_fixture",
        context_label="C major continuation",
        compatible_function_tag="tonic_support",
        generated_by_context_or_function=False,
    )


def gamma_consistency_fixture() -> ContextHarmonyConsistencyGamma:
    return ContextHarmonyConsistencyGamma(
        name="Gamma_context_harmony_consistency_fixture",
        reads=(
            "selected_next_context",
            "harmonic_function_annotation",
            "external_consistency_evidence",
        ),
        rule_scope="fixture_limited_not_consistency_selection_or_record_rule",
    )


def observe_context_harmony_consistency(
    next_context: NextContextSelectionObservation,
    harmonic_function: HarmonicFunctionAnnotationObservation,
    evidence: ContextHarmonyConsistencyEvidence | None,
    gamma_consistency: ContextHarmonyConsistencyGamma | None,
) -> ContextHarmonyConsistencyObservation:
    selected_context = next_context.selected_next_context
    function_annotation = harmonic_function.harmonic_function_annotation
    if selected_context is None:
        return ContextHarmonyConsistencyObservation(
            next_context_observation=next_context,
            harmonic_function_observation=harmonic_function,
            consistency_evidence=evidence,
            gamma_consistency=gamma_consistency,
            consistency_candidates=(),
            selected_consistency=None,
            module_state_record_generated=False,
            core_promoted=False,
            status="no_selected_next_context",
            consistency_reason=None,
        )
    if function_annotation is None:
        return ContextHarmonyConsistencyObservation(
            next_context_observation=next_context,
            harmonic_function_observation=harmonic_function,
            consistency_evidence=evidence,
            gamma_consistency=gamma_consistency,
            consistency_candidates=(),
            selected_consistency=None,
            module_state_record_generated=False,
            core_promoted=False,
            status="no_harmonic_function_annotation",
            consistency_reason=None,
        )
    if evidence is None:
        return ContextHarmonyConsistencyObservation(
            next_context_observation=next_context,
            harmonic_function_observation=harmonic_function,
            consistency_evidence=None,
            gamma_consistency=gamma_consistency,
            consistency_candidates=(),
            selected_consistency=None,
            module_state_record_generated=False,
            core_promoted=False,
            status="consistency_not_observed_without_evidence",
            consistency_reason=None,
        )
    if gamma_consistency is None:
        return ContextHarmonyConsistencyObservation(
            next_context_observation=next_context,
            harmonic_function_observation=harmonic_function,
            consistency_evidence=evidence,
            gamma_consistency=None,
            consistency_candidates=(),
            selected_consistency=None,
            module_state_record_generated=False,
            core_promoted=False,
            status="consistency_not_observed_without_gamma",
            consistency_reason=None,
        )

    if (
        selected_context.label != evidence.context_label
        or function_annotation.vocabulary_tag != evidence.compatible_function_tag
    ):
        return ContextHarmonyConsistencyObservation(
            next_context_observation=next_context,
            harmonic_function_observation=harmonic_function,
            consistency_evidence=evidence,
            gamma_consistency=gamma_consistency,
            consistency_candidates=(),
            selected_consistency=None,
            module_state_record_generated=False,
            core_promoted=False,
            status="consistency_evidence_not_applicable",
            consistency_reason=None,
        )

    candidate = ContextHarmonyConsistencyCandidate(
        label="C_major_tonic_support_consistency_candidate",
        selected_context_label=selected_context.label,
        harmonic_function_label=function_annotation.label,
        selected=False,
        module_state_record_generated=False,
    )
    return ContextHarmonyConsistencyObservation(
        next_context_observation=next_context,
        harmonic_function_observation=harmonic_function,
        consistency_evidence=evidence,
        gamma_consistency=gamma_consistency,
        consistency_candidates=(candidate,),
        selected_consistency=None,
        module_state_record_generated=False,
        core_promoted=False,
        status="context_harmony_consistency_candidate_observed_unselected",
        consistency_reason="context_function_and_external_evidence_read_by_Gamma_context_harmony_consistency",
    )


def compare_context_harmony_consistency() -> ContextHarmonyConsistencyComparison:
    next_context = next_context_observation()
    harmonic_function = harmonic_function_observation()
    evidence = consistency_evidence_fixture()
    without_gamma = observe_context_harmony_consistency(
        next_context, harmonic_function, evidence, None
    )
    with_gamma = observe_context_harmony_consistency(
        next_context, harmonic_function, evidence, gamma_consistency_fixture()
    )
    return ContextHarmonyConsistencyComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_selected_next_context=(
            without_gamma.next_context_observation.selected_next_context
            == with_gamma.next_context_observation.selected_next_context
        ),
        same_harmonic_function_annotation=(
            without_gamma.harmonic_function_observation.harmonic_function_annotation
            == with_gamma.harmonic_function_observation.harmonic_function_annotation
        ),
        same_consistency_evidence=(
            without_gamma.consistency_evidence == with_gamma.consistency_evidence
        ),
        same_gamma_consistency=(
            without_gamma.gamma_consistency == with_gamma.gamma_consistency
        ),
        consistency_candidate_observed=(
            with_gamma.status
            == "context_harmony_consistency_candidate_observed_unselected"
        ),
        selected_consistency_generated=with_gamma.selected_consistency is not None,
        module_state_record_generated=with_gamma.module_state_record_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_context_harmony_consistency()
    assert comparison.same_selected_next_context is True
    assert comparison.same_harmonic_function_annotation is True
    assert comparison.same_consistency_evidence is True
    assert comparison.same_gamma_consistency is False
    assert comparison.consistency_candidate_observed is True
    assert comparison.selected_consistency_generated is False
    assert comparison.module_state_record_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_gamma.status
        == "consistency_not_observed_without_gamma"
    )
    assert comparison.without_gamma.consistency_candidates == ()
    assert len(comparison.with_gamma.consistency_candidates) == 1
    assert comparison.with_gamma.consistency_candidates[0].label == (
        "C_major_tonic_support_consistency_candidate"
    )
    assert comparison.with_gamma.consistency_evidence is not None
    assert (
        comparison.with_gamma.consistency_evidence.generated_by_context_or_function
        is False
    )


def main() -> None:
    run_checks()
    comparison = compare_context_harmony_consistency()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  selected next context candidate")
    print("  + harmonic function annotation candidate")
    print("  + external consistency evidence")
    print("  + Gamma_context_harmony_consistency_fixture")
    print("  -> context-harmony consistency candidate")
    print("  -> selected consistency remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_selected_next_context={comparison.same_selected_next_context}")
    print(
        "  same_harmonic_function_annotation="
        f"{comparison.same_harmonic_function_annotation}"
    )
    print(f"  same_consistency_evidence={comparison.same_consistency_evidence}")
    print(f"  same_gamma_consistency={comparison.same_gamma_consistency}")
    print(f"  consistency_candidate_observed={comparison.consistency_candidate_observed}")
    print(
        "  consistency_candidates="
        + ",".join(candidate.label for candidate in with_gamma.consistency_candidates)
    )
    print(
        "  selected_consistency_generated="
        f"{comparison.selected_consistency_generated}"
    )
    print(
        "  module_state_record_generated="
        f"{comparison.module_state_record_generated}"
    )
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
