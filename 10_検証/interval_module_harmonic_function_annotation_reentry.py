"""再入harmonic bridgeからharmonic function annotationへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_harmonic_bridge_reentry import (
    HarmonicBridgeReentryObservation,
    ReenteredHarmonicBridgeObservation,
    compare_harmonic_bridge_reentry,
)
from interval_module_harmonic_function_annotation_boundary import (
    HarmonicFunctionAnnotation,
    HarmonicFunctionAnnotationGamma,
    HarmonicFunctionVocabulary,
    function_vocabulary_fixture,
    gamma_function_annotation_fixture,
)


@dataclass(frozen=True)
class HarmonicFunctionAnnotationReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_harmonic_bridge_reentry: bool


@dataclass(frozen=True)
class ReenteredHarmonicFunctionAnnotationObservation:
    harmonic_bridge_observation: ReenteredHarmonicBridgeObservation
    function_vocabulary: HarmonicFunctionVocabulary | None
    gamma_function_annotation: HarmonicFunctionAnnotationGamma | None
    harmonic_function_annotation: HarmonicFunctionAnnotation | None
    target_generated: bool
    voice_leading_generated: bool
    core_promoted: bool
    status: str
    annotation_reason: str | None


@dataclass(frozen=True)
class HarmonicFunctionAnnotationReentryObservation:
    bridge_reentry: HarmonicBridgeReentryObservation
    annotation_reentry_gamma: HarmonicFunctionAnnotationReentryGamma | None
    function_annotation_observation: ReenteredHarmonicFunctionAnnotationObservation | None
    same_harmonic_bridge: bool
    same_function_vocabulary: bool
    function_annotation_observed: bool
    target_generated: bool
    voice_leading_generated: bool
    status: str


def bridge_reentry_observation() -> HarmonicBridgeReentryObservation:
    return compare_harmonic_bridge_reentry()[1]


def annotation_reentry_gamma_fixture() -> HarmonicFunctionAnnotationReentryGamma:
    return HarmonicFunctionAnnotationReentryGamma(
        name="Gamma_reentered_harmonic_bridge_to_function_annotation_fixture",
        reads=("reentered_harmonic_bridge", "external_function_vocabulary"),
        generated_by_harmonic_bridge_reentry=False,
    )


def annotate_reentered_harmonic_function(
    bridge_obs: ReenteredHarmonicBridgeObservation,
    vocabulary: HarmonicFunctionVocabulary | None,
    gamma: HarmonicFunctionAnnotationGamma | None,
) -> ReenteredHarmonicFunctionAnnotationObservation:
    bridge = bridge_obs.harmonic_bridge
    if bridge is None:
        status = "no_reentered_harmonic_bridge_candidate"
        annotation = None
    elif vocabulary is None:
        status = "reentered_function_annotation_not_observed_without_vocabulary"
        annotation = None
    elif gamma is None:
        status = "reentered_function_annotation_not_observed_without_gamma"
        annotation = None
    else:
        matches = tuple(
            item for item in vocabulary.annotations if item.vocabulary_tag == gamma.accepted_vocabulary_tag
        )
        annotation = matches[0] if len(matches) == 1 else None
        status = (
            "harmonic_function_annotation_observed_from_reentered_bridge_not_generating"
            if annotation
            else "reentered_function_annotation_ambiguous_or_absent"
        )
    return ReenteredHarmonicFunctionAnnotationObservation(
        bridge_obs,
        vocabulary,
        gamma,
        annotation,
        False,
        False,
        False,
        status,
        "reentered_bridge_and_external_vocabulary_read_by_Gamma_annotation" if annotation else None,
    )


def reenter_harmonic_bridge_to_function_annotation(
    bridge_reentry: HarmonicBridgeReentryObservation,
    reentry_gamma: HarmonicFunctionAnnotationReentryGamma | None,
) -> HarmonicFunctionAnnotationReentryObservation:
    bridge_obs = bridge_reentry.harmonic_bridge_observation
    if bridge_obs is None or bridge_obs.harmonic_bridge is None:
        return HarmonicFunctionAnnotationReentryObservation(
            bridge_reentry, reentry_gamma, None, False, False, False, False, False,
            "no_reentered_harmonic_bridge_candidate",
        )
    if reentry_gamma is None:
        return HarmonicFunctionAnnotationReentryObservation(
            bridge_reentry, None, None, True, False, False, False, False,
            "reentered_harmonic_bridge_not_connected_to_function_annotation_without_reentry_gamma",
        )
    vocabulary = function_vocabulary_fixture()
    obs = annotate_reentered_harmonic_function(
        bridge_obs, vocabulary, gamma_function_annotation_fixture()
    )
    return HarmonicFunctionAnnotationReentryObservation(
        bridge_reentry,
        reentry_gamma,
        obs,
        obs.harmonic_bridge_observation.harmonic_bridge == bridge_obs.harmonic_bridge,
        obs.function_vocabulary == vocabulary,
        obs.harmonic_function_annotation is not None,
        obs.target_generated,
        obs.voice_leading_generated,
        "reentered_harmonic_bridge_connected_to_function_annotation_not_generating",
    )


def compare_harmonic_function_annotation_reentry() -> tuple[
    HarmonicFunctionAnnotationReentryObservation,
    HarmonicFunctionAnnotationReentryObservation,
]:
    bridge = bridge_reentry_observation()
    return (
        reenter_harmonic_bridge_to_function_annotation(bridge, None),
        reenter_harmonic_bridge_to_function_annotation(
            bridge, annotation_reentry_gamma_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_harmonic_function_annotation_reentry()
    assert without_gamma.function_annotation_observed is False
    assert with_gamma.same_harmonic_bridge is True
    assert with_gamma.same_function_vocabulary is True
    assert with_gamma.function_annotation_observed is True
    assert with_gamma.target_generated is False
    assert with_gamma.voice_leading_generated is False
    assert with_gamma.function_annotation_observation is not None
    assert with_gamma.function_annotation_observation.harmonic_function_annotation is not None
    assert (
        with_gamma.function_annotation_observation.harmonic_function_annotation.label
        == "tonic_support_annotation_candidate"
    )


if __name__ == "__main__":
    run_checks()
    print(compare_harmonic_function_annotation_reentry()[1].status)
