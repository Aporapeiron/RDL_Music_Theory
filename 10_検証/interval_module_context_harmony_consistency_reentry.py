"""再入selected next contextとharmonic annotationの整合候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_context_harmony_consistency_boundary import (
    ContextHarmonyConsistencyCandidate,
    ContextHarmonyConsistencyEvidence,
    ContextHarmonyConsistencyGamma,
    consistency_evidence_fixture,
    gamma_consistency_fixture,
)
from interval_module_harmonic_function_annotation_reentry import (
    HarmonicFunctionAnnotationReentryObservation,
    ReenteredHarmonicFunctionAnnotationObservation,
    compare_harmonic_function_annotation_reentry,
)
from interval_module_next_context_selection_reentry import (
    NextContextSelectionReentryObservation,
    ReenteredNextContextSelectionObservation,
    compare_next_context_selection_reentry,
)


@dataclass(frozen=True)
class ContextHarmonyConsistencyReentryGamma:
    name: str
    reads: tuple[str, str, str]
    generated_by_inputs: bool


@dataclass(frozen=True)
class ReenteredContextHarmonyConsistencyObservation:
    next_context_observation: ReenteredNextContextSelectionObservation
    harmonic_function_observation: ReenteredHarmonicFunctionAnnotationObservation
    consistency_evidence: ContextHarmonyConsistencyEvidence | None
    gamma_consistency: ContextHarmonyConsistencyGamma | None
    consistency_candidates: tuple[ContextHarmonyConsistencyCandidate, ...]
    selected_consistency: ContextHarmonyConsistencyCandidate | None
    module_state_record_generated: bool
    core_promoted: bool
    status: str


@dataclass(frozen=True)
class ContextHarmonyConsistencyReentryObservation:
    next_context_reentry: NextContextSelectionReentryObservation
    harmonic_annotation_reentry: HarmonicFunctionAnnotationReentryObservation
    consistency_reentry_gamma: ContextHarmonyConsistencyReentryGamma | None
    consistency_observation: ReenteredContextHarmonyConsistencyObservation | None
    consistency_candidate_observed: bool
    selected_consistency_generated: bool
    module_state_record_generated: bool
    status: str


def consistency_reentry_gamma_fixture() -> ContextHarmonyConsistencyReentryGamma:
    return ContextHarmonyConsistencyReentryGamma(
        name="Gamma_reentered_context_and_harmony_to_consistency_fixture",
        reads=("reentered_selected_next_context", "reentered_harmonic_annotation", "external_evidence"),
        generated_by_inputs=False,
    )


def observe_reentered_context_harmony_consistency(
    next_obs: ReenteredNextContextSelectionObservation,
    function_obs: ReenteredHarmonicFunctionAnnotationObservation,
    evidence: ContextHarmonyConsistencyEvidence | None,
    gamma: ContextHarmonyConsistencyGamma | None,
) -> ReenteredContextHarmonyConsistencyObservation:
    selected_context = next_obs.selected_next_context
    annotation = function_obs.harmonic_function_annotation
    candidates: tuple[ContextHarmonyConsistencyCandidate, ...] = ()
    status = "context_harmony_consistency_not_observed"
    if selected_context is None:
        status = "no_reentered_selected_next_context"
    elif annotation is None:
        status = "no_reentered_harmonic_function_annotation"
    elif evidence is None:
        status = "reentered_consistency_not_observed_without_evidence"
    elif gamma is None:
        status = "reentered_consistency_not_observed_without_gamma"
    elif (
        selected_context.label == evidence.context_label
        and annotation.vocabulary_tag == evidence.compatible_function_tag
    ):
        candidates = (
            ContextHarmonyConsistencyCandidate(
                label="C_major_tonic_support_consistency_candidate",
                selected_context_label=selected_context.label,
                harmonic_function_label=annotation.label,
                selected=False,
                module_state_record_generated=False,
            ),
        )
        status = "context_harmony_consistency_candidate_observed_from_reentered_inputs_unselected"
    else:
        status = "reentered_consistency_evidence_not_applicable"
    return ReenteredContextHarmonyConsistencyObservation(
        next_obs, function_obs, evidence, gamma, candidates, None, False, False, status
    )


def reenter_context_harmony_consistency(
    reentry_gamma: ContextHarmonyConsistencyReentryGamma | None,
) -> ContextHarmonyConsistencyReentryObservation:
    next_reentry = compare_next_context_selection_reentry()[1]
    function_reentry = compare_harmonic_function_annotation_reentry()[1]
    next_obs = next_reentry.next_context_selection_observation
    function_obs = function_reentry.function_annotation_observation
    if next_obs is None or function_obs is None:
        return ContextHarmonyConsistencyReentryObservation(
            next_reentry, function_reentry, reentry_gamma, None, False, False, False,
            "missing_reentered_context_or_harmonic_annotation",
        )
    if reentry_gamma is None:
        return ContextHarmonyConsistencyReentryObservation(
            next_reentry, function_reentry, None, None, False, False, False,
            "reentered_context_harmony_not_connected_without_reentry_gamma",
        )
    obs = observe_reentered_context_harmony_consistency(
        next_obs, function_obs, consistency_evidence_fixture(), gamma_consistency_fixture()
    )
    return ContextHarmonyConsistencyReentryObservation(
        next_reentry,
        function_reentry,
        reentry_gamma,
        obs,
        bool(obs.consistency_candidates),
        obs.selected_consistency is not None,
        obs.module_state_record_generated,
        "reentered_context_harmony_connected_to_consistency_candidates_unselected",
    )


def compare_context_harmony_consistency_reentry() -> tuple[
    ContextHarmonyConsistencyReentryObservation,
    ContextHarmonyConsistencyReentryObservation,
]:
    return (
        reenter_context_harmony_consistency(None),
        reenter_context_harmony_consistency(consistency_reentry_gamma_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_context_harmony_consistency_reentry()
    assert without_gamma.consistency_candidate_observed is False
    assert with_gamma.consistency_candidate_observed is True
    assert with_gamma.selected_consistency_generated is False
    assert with_gamma.module_state_record_generated is False
    assert with_gamma.consistency_observation is not None
    assert len(with_gamma.consistency_observation.consistency_candidates) == 1


if __name__ == "__main__":
    run_checks()
    print(compare_context_harmony_consistency_reentry()[1].status)
