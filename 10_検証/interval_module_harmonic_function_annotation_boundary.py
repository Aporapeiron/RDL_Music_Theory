"""音程Module harmonic bridgeとfunction annotation境界の最小検証。"""

from dataclasses import dataclass

from interval_module_harmonic_bridge_boundary import (
    IntervalHarmonicBridgeObservation,
    compare_interval_harmonic_bridge,
)


@dataclass(frozen=True)
class HarmonicFunctionAnnotation:
    label: str
    vocabulary_tag: str
    generated_by_harmonic_bridge: bool


@dataclass(frozen=True)
class HarmonicFunctionVocabulary:
    name: str
    annotations: tuple[HarmonicFunctionAnnotation, ...]
    generated_by_harmonic_bridge: bool


@dataclass(frozen=True)
class HarmonicFunctionAnnotationGamma:
    name: str
    reads: tuple[str, str]
    accepted_vocabulary_tag: str
    rule_scope: str


@dataclass(frozen=True)
class HarmonicFunctionAnnotationObservation:
    harmonic_bridge_observation: IntervalHarmonicBridgeObservation
    function_vocabulary: HarmonicFunctionVocabulary | None
    gamma_function_annotation: HarmonicFunctionAnnotationGamma | None
    harmonic_function_annotation: HarmonicFunctionAnnotation | None
    target_generated: bool
    voice_leading_generated: bool
    core_promoted: bool
    status: str
    annotation_reason: str | None


@dataclass(frozen=True)
class HarmonicFunctionAnnotationComparison:
    without_gamma: HarmonicFunctionAnnotationObservation
    with_gamma: HarmonicFunctionAnnotationObservation
    same_harmonic_bridge: bool
    same_function_vocabulary: bool
    same_gamma_function_annotation: bool
    function_annotation_observed: bool
    target_generated: bool
    voice_leading_generated: bool
    core_promoted: bool


def harmonic_bridge_observation() -> IntervalHarmonicBridgeObservation:
    return compare_interval_harmonic_bridge().with_gamma


def function_vocabulary_fixture() -> HarmonicFunctionVocabulary:
    return HarmonicFunctionVocabulary(
        name="external_harmonic_function_vocabulary_fixture",
        annotations=(
            HarmonicFunctionAnnotation(
                label="tonic_support_annotation_candidate",
                vocabulary_tag="tonic_support",
                generated_by_harmonic_bridge=False,
            ),
            HarmonicFunctionAnnotation(
                label="consonant_span_annotation_candidate",
                vocabulary_tag="consonance_description",
                generated_by_harmonic_bridge=False,
            ),
            HarmonicFunctionAnnotation(
                label="dominant_resolution_annotation_candidate",
                vocabulary_tag="dominant_resolution",
                generated_by_harmonic_bridge=False,
            ),
        ),
        generated_by_harmonic_bridge=False,
    )


def gamma_function_annotation_fixture() -> HarmonicFunctionAnnotationGamma:
    return HarmonicFunctionAnnotationGamma(
        name="Gamma_harmonic_function_annotation_fixture",
        reads=("harmonic_function_bridge", "external_function_vocabulary"),
        accepted_vocabulary_tag="tonic_support",
        rule_scope="fixture_limited_not_target_or_voice_leading_generation_rule",
    )


def annotate_harmonic_function(
    harmonic_bridge: IntervalHarmonicBridgeObservation,
    function_vocabulary: HarmonicFunctionVocabulary | None,
    gamma_function_annotation: HarmonicFunctionAnnotationGamma | None,
) -> HarmonicFunctionAnnotationObservation:
    bridge = harmonic_bridge.harmonic_bridge
    if bridge is None:
        return HarmonicFunctionAnnotationObservation(
            harmonic_bridge_observation=harmonic_bridge,
            function_vocabulary=function_vocabulary,
            gamma_function_annotation=gamma_function_annotation,
            harmonic_function_annotation=None,
            target_generated=False,
            voice_leading_generated=False,
            core_promoted=False,
            status="no_harmonic_bridge_candidate",
            annotation_reason=None,
        )
    if function_vocabulary is None:
        return HarmonicFunctionAnnotationObservation(
            harmonic_bridge_observation=harmonic_bridge,
            function_vocabulary=None,
            gamma_function_annotation=gamma_function_annotation,
            harmonic_function_annotation=None,
            target_generated=False,
            voice_leading_generated=False,
            core_promoted=False,
            status="function_annotation_not_observed_without_vocabulary",
            annotation_reason=None,
        )
    if gamma_function_annotation is None:
        return HarmonicFunctionAnnotationObservation(
            harmonic_bridge_observation=harmonic_bridge,
            function_vocabulary=function_vocabulary,
            gamma_function_annotation=None,
            harmonic_function_annotation=None,
            target_generated=False,
            voice_leading_generated=False,
            core_promoted=False,
            status="function_annotation_not_observed_without_gamma",
            annotation_reason=None,
        )

    matches = tuple(
        annotation
        for annotation in function_vocabulary.annotations
        if annotation.vocabulary_tag
        == gamma_function_annotation.accepted_vocabulary_tag
    )
    if len(matches) != 1:
        return HarmonicFunctionAnnotationObservation(
            harmonic_bridge_observation=harmonic_bridge,
            function_vocabulary=function_vocabulary,
            gamma_function_annotation=gamma_function_annotation,
            harmonic_function_annotation=None,
            target_generated=False,
            voice_leading_generated=False,
            core_promoted=False,
            status="function_annotation_ambiguous_or_absent",
            annotation_reason=None,
        )

    return HarmonicFunctionAnnotationObservation(
        harmonic_bridge_observation=harmonic_bridge,
        function_vocabulary=function_vocabulary,
        gamma_function_annotation=gamma_function_annotation,
        harmonic_function_annotation=matches[0],
        target_generated=False,
        voice_leading_generated=False,
        core_promoted=False,
        status="harmonic_function_annotation_observed_not_generating",
        annotation_reason="harmonic_bridge_and_external_vocabulary_read_by_Gamma_harmonic_function_annotation",
    )


def compare_harmonic_function_annotation() -> HarmonicFunctionAnnotationComparison:
    bridge = harmonic_bridge_observation()
    vocabulary = function_vocabulary_fixture()
    without_gamma = annotate_harmonic_function(bridge, vocabulary, None)
    with_gamma = annotate_harmonic_function(
        bridge, vocabulary, gamma_function_annotation_fixture()
    )
    return HarmonicFunctionAnnotationComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_harmonic_bridge=(
            without_gamma.harmonic_bridge_observation.harmonic_bridge
            == with_gamma.harmonic_bridge_observation.harmonic_bridge
        ),
        same_function_vocabulary=(
            without_gamma.function_vocabulary == with_gamma.function_vocabulary
        ),
        same_gamma_function_annotation=(
            without_gamma.gamma_function_annotation
            == with_gamma.gamma_function_annotation
        ),
        function_annotation_observed=(
            with_gamma.status
            == "harmonic_function_annotation_observed_not_generating"
        ),
        target_generated=with_gamma.target_generated,
        voice_leading_generated=with_gamma.voice_leading_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_harmonic_function_annotation()
    assert comparison.same_harmonic_bridge is True
    assert comparison.same_function_vocabulary is True
    assert comparison.same_gamma_function_annotation is False
    assert comparison.function_annotation_observed is True
    assert comparison.target_generated is False
    assert comparison.voice_leading_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_gamma.status
        == "function_annotation_not_observed_without_gamma"
    )
    assert comparison.without_gamma.harmonic_function_annotation is None
    assert comparison.with_gamma.harmonic_function_annotation is not None
    assert comparison.with_gamma.harmonic_function_annotation.label == (
        "tonic_support_annotation_candidate"
    )
    assert (
        comparison.with_gamma.harmonic_function_annotation.generated_by_harmonic_bridge
        is False
    )
    assert comparison.with_gamma.function_vocabulary is not None
    assert comparison.with_gamma.function_vocabulary.generated_by_harmonic_bridge is False


def main() -> None:
    run_checks()
    comparison = compare_harmonic_function_annotation()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  harmonic function bridge candidate")
    print("  + external function vocabulary")
    print("  + Gamma_harmonic_function_annotation_fixture")
    print("  -> harmonic function annotation candidate")
    print("  -> target and voice leading remain None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_harmonic_bridge={comparison.same_harmonic_bridge}")
    print(f"  same_function_vocabulary={comparison.same_function_vocabulary}")
    print(f"  same_gamma_function_annotation={comparison.same_gamma_function_annotation}")
    print(f"  function_annotation_observed={comparison.function_annotation_observed}")
    print(
        "  harmonic_function_annotation="
        + (
            with_gamma.harmonic_function_annotation.label
            if with_gamma.harmonic_function_annotation
            else "None"
        )
    )
    print(f"  target_generated={comparison.target_generated}")
    print(f"  voice_leading_generated={comparison.voice_leading_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
