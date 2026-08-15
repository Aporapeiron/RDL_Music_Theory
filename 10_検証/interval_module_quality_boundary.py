"""音程Module generic intervalとquality生成境界の最小検証。"""

from dataclasses import dataclass

from interval_module_generic_interval_boundary import (
    GenericIntervalObservation,
    compare_generic_interval_generation,
)


PERFECT_EXPECTED = {1: 0, 4: 5, 5: 7, 8: 12}
MAJOR_EXPECTED = {2: 2, 3: 4, 6: 9, 7: 11}


@dataclass(frozen=True)
class QualityGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class QualityCandidate:
    label: str
    source_generic_interval_label: str
    generic_number: int
    chromatic_distance: int
    quality_code: str
    interval_label_generated: bool
    contextual_role_generated: bool


@dataclass(frozen=True)
class QualityObservation:
    generic_observation: GenericIntervalObservation
    gamma_quality: QualityGamma | None
    quality: QualityCandidate | None
    interval_label_generated: bool
    contextual_role_generated: bool
    target_generated: bool
    core_promoted: bool
    status: str
    generation_reason: str | None


@dataclass(frozen=True)
class QualityComparison:
    without_gamma: QualityObservation
    with_gamma: QualityObservation
    same_generic_interval: bool
    same_chromatic_distance: bool
    same_gamma_quality: bool
    quality_observed: bool
    interval_label_generated: bool
    contextual_role_generated: bool
    target_generated: bool
    core_promoted: bool


def generic_observation() -> GenericIntervalObservation:
    return compare_generic_interval_generation().with_gamma


def gamma_quality_fixture() -> QualityGamma:
    return QualityGamma(
        name="Gamma_quality_fixture",
        reads=("generic_interval", "chromatic_distance"),
        rule_scope="fixture_limited_not_interval_label_rule",
    )


def quality_code(generic_number: int, semitones: int) -> str:
    if generic_number in PERFECT_EXPECTED:
        delta = semitones - PERFECT_EXPECTED[generic_number]
        return {0: "P", -1: "d", 1: "A"}.get(delta, "?")
    if generic_number in MAJOR_EXPECTED:
        delta = semitones - MAJOR_EXPECTED[generic_number]
        return {0: "M", -1: "m", -2: "d", 1: "A"}.get(delta, "?")
    return "?"


def generate_quality(
    generic: GenericIntervalObservation,
    gamma_quality: QualityGamma | None,
) -> QualityObservation:
    generic_interval = generic.generic_interval
    payload = generic.activation_observation.pitch_payload
    if generic_interval is None:
        return QualityObservation(
            generic_observation=generic,
            gamma_quality=gamma_quality,
            quality=None,
            interval_label_generated=False,
            contextual_role_generated=False,
            target_generated=False,
            core_promoted=False,
            status="no_generic_interval_candidate",
            generation_reason=None,
        )
    if payload is None:
        return QualityObservation(
            generic_observation=generic,
            gamma_quality=gamma_quality,
            quality=None,
            interval_label_generated=False,
            contextual_role_generated=False,
            target_generated=False,
            core_promoted=False,
            status="no_chromatic_distance_payload",
            generation_reason=None,
        )
    if gamma_quality is None:
        return QualityObservation(
            generic_observation=generic,
            gamma_quality=None,
            quality=None,
            interval_label_generated=False,
            contextual_role_generated=False,
            target_generated=False,
            core_promoted=False,
            status="quality_not_generated_without_gamma",
            generation_reason=None,
        )

    code = quality_code(generic_interval.generic_number, payload.chromatic_distance)
    candidate = QualityCandidate(
        label="quality_perfect_candidate",
        source_generic_interval_label=generic_interval.label,
        generic_number=generic_interval.generic_number,
        chromatic_distance=payload.chromatic_distance,
        quality_code=code,
        interval_label_generated=False,
        contextual_role_generated=False,
    )
    return QualityObservation(
        generic_observation=generic,
        gamma_quality=gamma_quality,
        quality=candidate,
        interval_label_generated=False,
        contextual_role_generated=False,
        target_generated=False,
        core_promoted=False,
        status="quality_candidate_observed_not_labeled",
        generation_reason="generic_interval_and_chromatic_distance_read_by_Gamma_quality",
    )


def compare_quality_generation() -> QualityComparison:
    generic = generic_observation()
    without_gamma = generate_quality(generic, None)
    with_gamma = generate_quality(generic, gamma_quality_fixture())
    return QualityComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_generic_interval=(
            without_gamma.generic_observation.generic_interval
            == with_gamma.generic_observation.generic_interval
        ),
        same_chromatic_distance=(
            without_gamma.generic_observation.activation_observation.pitch_payload.chromatic_distance
            == with_gamma.generic_observation.activation_observation.pitch_payload.chromatic_distance
        ),
        same_gamma_quality=without_gamma.gamma_quality == with_gamma.gamma_quality,
        quality_observed=with_gamma.status == "quality_candidate_observed_not_labeled",
        interval_label_generated=with_gamma.interval_label_generated,
        contextual_role_generated=with_gamma.contextual_role_generated,
        target_generated=with_gamma.target_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_quality_generation()
    assert comparison.same_generic_interval is True
    assert comparison.same_chromatic_distance is True
    assert comparison.same_gamma_quality is False
    assert comparison.quality_observed is True
    assert comparison.interval_label_generated is False
    assert comparison.contextual_role_generated is False
    assert comparison.target_generated is False
    assert comparison.core_promoted is False
    assert comparison.without_gamma.status == "quality_not_generated_without_gamma"
    assert comparison.without_gamma.quality is None
    assert comparison.with_gamma.quality is not None
    assert comparison.with_gamma.quality.generic_number == 5
    assert comparison.with_gamma.quality.chromatic_distance == 7
    assert comparison.with_gamma.quality.quality_code == "P"
    assert comparison.with_gamma.quality.interval_label_generated is False


def main() -> None:
    run_checks()
    comparison = compare_quality_generation()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  generic interval candidate")
    print("  + chromatic distance")
    print("  + Gamma_quality_fixture")
    print("  -> quality candidate")
    print("  -> interval label remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_generic_interval={comparison.same_generic_interval}")
    print(f"  same_chromatic_distance={comparison.same_chromatic_distance}")
    print(f"  same_gamma_quality={comparison.same_gamma_quality}")
    print(f"  quality_observed={comparison.quality_observed}")
    print(
        "  quality_code="
        + (with_gamma.quality.quality_code if with_gamma.quality else "None")
    )
    print(f"  interval_label_generated={comparison.interval_label_generated}")
    print(f"  contextual_role_generated={comparison.contextual_role_generated}")
    print(f"  target_generated={comparison.target_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
