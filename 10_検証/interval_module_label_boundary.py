"""音程Module qualityとinterval label生成境界の最小検証。"""

from dataclasses import dataclass

from interval_module_quality_boundary import (
    QualityObservation,
    compare_quality_generation,
)


INTERVAL_NAMES = {
    1: "一度",
    2: "二度",
    3: "三度",
    4: "四度",
    5: "五度",
    6: "六度",
    7: "七度",
    8: "八度",
}
QUALITY_NAMES = {
    "P": "完全",
    "M": "長",
    "m": "短",
    "d": "減",
    "A": "増",
}


@dataclass(frozen=True)
class IntervalLabelGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class IntervalLabelCandidate:
    label: str
    source_quality_label: str
    generic_number: int
    quality_code: str
    contextual_role_generated: bool
    target_generated: bool
    harmonic_function_generated: bool


@dataclass(frozen=True)
class IntervalLabelObservation:
    quality_observation: QualityObservation
    gamma_interval_label: IntervalLabelGamma | None
    interval_label: IntervalLabelCandidate | None
    contextual_role_generated: bool
    target_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    generation_reason: str | None


@dataclass(frozen=True)
class IntervalLabelComparison:
    without_gamma: IntervalLabelObservation
    with_gamma: IntervalLabelObservation
    same_generic_interval: bool
    same_quality: bool
    same_gamma_interval_label: bool
    interval_label_observed: bool
    contextual_role_generated: bool
    target_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool


def quality_observation() -> QualityObservation:
    return compare_quality_generation().with_gamma


def gamma_interval_label_fixture() -> IntervalLabelGamma:
    return IntervalLabelGamma(
        name="Gamma_interval_label_fixture",
        reads=("generic_interval", "quality"),
        rule_scope="fixture_limited_not_context_role_or_target_rule",
    )


def make_interval_label(generic_number: int, quality_code: str) -> str:
    return (
        QUALITY_NAMES.get(quality_code, "不明")
        + INTERVAL_NAMES.get(generic_number, f"{generic_number}度")
    )


def generate_interval_label(
    quality_observation: QualityObservation,
    gamma_interval_label: IntervalLabelGamma | None,
) -> IntervalLabelObservation:
    quality = quality_observation.quality
    if quality is None:
        return IntervalLabelObservation(
            quality_observation=quality_observation,
            gamma_interval_label=gamma_interval_label,
            interval_label=None,
            contextual_role_generated=False,
            target_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="no_quality_candidate",
            generation_reason=None,
        )
    if gamma_interval_label is None:
        return IntervalLabelObservation(
            quality_observation=quality_observation,
            gamma_interval_label=None,
            interval_label=None,
            contextual_role_generated=False,
            target_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="interval_label_not_generated_without_gamma",
            generation_reason=None,
        )

    candidate = IntervalLabelCandidate(
        label=make_interval_label(quality.generic_number, quality.quality_code),
        source_quality_label=quality.label,
        generic_number=quality.generic_number,
        quality_code=quality.quality_code,
        contextual_role_generated=False,
        target_generated=False,
        harmonic_function_generated=False,
    )
    return IntervalLabelObservation(
        quality_observation=quality_observation,
        gamma_interval_label=gamma_interval_label,
        interval_label=candidate,
        contextual_role_generated=False,
        target_generated=False,
        harmonic_function_generated=False,
        core_promoted=False,
        status="interval_label_candidate_observed_not_contextualized",
        generation_reason="generic_interval_and_quality_read_by_Gamma_interval_label",
    )


def compare_interval_label_generation() -> IntervalLabelComparison:
    quality = quality_observation()
    without_gamma = generate_interval_label(quality, None)
    with_gamma = generate_interval_label(quality, gamma_interval_label_fixture())
    return IntervalLabelComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_generic_interval=(
            without_gamma.quality_observation.quality.generic_number
            == with_gamma.quality_observation.quality.generic_number
        ),
        same_quality=(
            without_gamma.quality_observation.quality
            == with_gamma.quality_observation.quality
        ),
        same_gamma_interval_label=(
            without_gamma.gamma_interval_label == with_gamma.gamma_interval_label
        ),
        interval_label_observed=(
            with_gamma.status == "interval_label_candidate_observed_not_contextualized"
        ),
        contextual_role_generated=with_gamma.contextual_role_generated,
        target_generated=with_gamma.target_generated,
        harmonic_function_generated=with_gamma.harmonic_function_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_interval_label_generation()
    assert comparison.same_generic_interval is True
    assert comparison.same_quality is True
    assert comparison.same_gamma_interval_label is False
    assert comparison.interval_label_observed is True
    assert comparison.contextual_role_generated is False
    assert comparison.target_generated is False
    assert comparison.harmonic_function_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_gamma.status
        == "interval_label_not_generated_without_gamma"
    )
    assert comparison.without_gamma.interval_label is None
    assert comparison.with_gamma.interval_label is not None
    assert comparison.with_gamma.interval_label.label == "完全五度"
    assert comparison.with_gamma.interval_label.generic_number == 5
    assert comparison.with_gamma.interval_label.quality_code == "P"
    assert comparison.with_gamma.interval_label.contextual_role_generated is False
    assert comparison.with_gamma.interval_label.target_generated is False
    assert comparison.with_gamma.interval_label.harmonic_function_generated is False


def main() -> None:
    run_checks()
    comparison = compare_interval_label_generation()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  generic interval candidate")
    print("  + quality candidate")
    print("  + Gamma_interval_label_fixture")
    print("  -> interval label candidate")
    print("  -> contextual role and target remain None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_generic_interval={comparison.same_generic_interval}")
    print(f"  same_quality={comparison.same_quality}")
    print(f"  same_gamma_interval_label={comparison.same_gamma_interval_label}")
    print(f"  interval_label_observed={comparison.interval_label_observed}")
    print(
        "  interval_label="
        + (with_gamma.interval_label.label if with_gamma.interval_label else "None")
    )
    print(f"  contextual_role_generated={comparison.contextual_role_generated}")
    print(f"  target_generated={comparison.target_generated}")
    print(f"  harmonic_function_generated={comparison.harmonic_function_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
