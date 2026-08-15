"""音程Module processing frameとgeneric interval生成境界の最小検証。"""

from dataclasses import dataclass

from interval_module_internal_boundary_activation import (
    IntervalInternalActivationObservation,
    compare_interval_internal_activation,
)


LETTER_INDEX = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}


@dataclass(frozen=True)
class GenericIntervalGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class GenericIntervalCandidate:
    label: str
    source_processing_frame_label: str
    spelling_pair: tuple[str, str]
    generic_number: int
    quality_generated: bool
    interval_label_generated: bool
    contextual_role_generated: bool


@dataclass(frozen=True)
class GenericIntervalObservation:
    activation_observation: IntervalInternalActivationObservation
    gamma_generic: GenericIntervalGamma | None
    generic_interval: GenericIntervalCandidate | None
    quality_generated: bool
    interval_label_generated: bool
    contextual_role_generated: bool
    core_promoted: bool
    status: str
    generation_reason: str | None


@dataclass(frozen=True)
class GenericIntervalComparison:
    without_gamma: GenericIntervalObservation
    with_gamma: GenericIntervalObservation
    same_processing_frame: bool
    same_spelling_pair: bool
    same_gamma_generic: bool
    generic_interval_observed: bool
    quality_generated: bool
    interval_label_generated: bool
    contextual_role_generated: bool
    core_promoted: bool


def activation_observation() -> IntervalInternalActivationObservation:
    return compare_interval_internal_activation().with_gamma


def gamma_generic_fixture() -> GenericIntervalGamma:
    return GenericIntervalGamma(
        name="Gamma_generic_fixture",
        reads=("processing_frame", "spelling_pair"),
        rule_scope="fixture_limited_not_quality_or_interval_label_rule",
    )


def generate_generic_interval(
    activation: IntervalInternalActivationObservation,
    gamma_generic: GenericIntervalGamma | None,
) -> GenericIntervalObservation:
    frame = activation.processing_frame
    payload = activation.pitch_payload
    if frame is None:
        return GenericIntervalObservation(
            activation_observation=activation,
            gamma_generic=gamma_generic,
            generic_interval=None,
            quality_generated=False,
            interval_label_generated=False,
            contextual_role_generated=False,
            core_promoted=False,
            status="no_processing_frame",
            generation_reason=None,
        )
    if payload is None:
        return GenericIntervalObservation(
            activation_observation=activation,
            gamma_generic=gamma_generic,
            generic_interval=None,
            quality_generated=False,
            interval_label_generated=False,
            contextual_role_generated=False,
            core_promoted=False,
            status="no_pitch_relation_payload",
            generation_reason=None,
        )
    if gamma_generic is None:
        return GenericIntervalObservation(
            activation_observation=activation,
            gamma_generic=None,
            generic_interval=None,
            quality_generated=False,
            interval_label_generated=False,
            contextual_role_generated=False,
            core_promoted=False,
            status="generic_interval_not_generated_without_gamma",
            generation_reason=None,
        )

    lower, upper = payload.spelling_pair
    generic_number = LETTER_INDEX[upper] - LETTER_INDEX[lower] + 1
    candidate = GenericIntervalCandidate(
        label="generic_interval_fifth_candidate",
        source_processing_frame_label=frame.label,
        spelling_pair=payload.spelling_pair,
        generic_number=generic_number,
        quality_generated=False,
        interval_label_generated=False,
        contextual_role_generated=False,
    )
    return GenericIntervalObservation(
        activation_observation=activation,
        gamma_generic=gamma_generic,
        generic_interval=candidate,
        quality_generated=False,
        interval_label_generated=False,
        contextual_role_generated=False,
        core_promoted=False,
        status="generic_interval_candidate_observed_not_qualified",
        generation_reason="spelling_pair_read_by_Gamma_generic",
    )


def compare_generic_interval_generation() -> GenericIntervalComparison:
    activation = activation_observation()
    without_gamma = generate_generic_interval(activation, None)
    with_gamma = generate_generic_interval(activation, gamma_generic_fixture())
    return GenericIntervalComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_processing_frame=(
            without_gamma.activation_observation.processing_frame
            == with_gamma.activation_observation.processing_frame
        ),
        same_spelling_pair=(
            without_gamma.activation_observation.pitch_payload.spelling_pair
            == with_gamma.activation_observation.pitch_payload.spelling_pair
        ),
        same_gamma_generic=without_gamma.gamma_generic == with_gamma.gamma_generic,
        generic_interval_observed=(
            with_gamma.status == "generic_interval_candidate_observed_not_qualified"
        ),
        quality_generated=with_gamma.quality_generated,
        interval_label_generated=with_gamma.interval_label_generated,
        contextual_role_generated=with_gamma.contextual_role_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_generic_interval_generation()
    assert comparison.same_processing_frame is True
    assert comparison.same_spelling_pair is True
    assert comparison.same_gamma_generic is False
    assert comparison.generic_interval_observed is True
    assert comparison.quality_generated is False
    assert comparison.interval_label_generated is False
    assert comparison.contextual_role_generated is False
    assert comparison.core_promoted is False
    assert comparison.without_gamma.status == "generic_interval_not_generated_without_gamma"
    assert comparison.without_gamma.generic_interval is None
    assert comparison.with_gamma.generic_interval is not None
    assert comparison.with_gamma.generic_interval.generic_number == 5
    assert comparison.with_gamma.generic_interval.quality_generated is False
    assert comparison.with_gamma.generic_interval.interval_label_generated is False


def main() -> None:
    run_checks()
    comparison = compare_generic_interval_generation()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  interval module processing frame candidate")
    print("  + Gamma_generic_fixture")
    print("  -> generic interval candidate")
    print("  -> quality and interval label remain None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_processing_frame={comparison.same_processing_frame}")
    print(f"  same_spelling_pair={comparison.same_spelling_pair}")
    print(f"  same_gamma_generic={comparison.same_gamma_generic}")
    print(f"  generic_interval_observed={comparison.generic_interval_observed}")
    print(
        "  generic_number="
        + (
            str(with_gamma.generic_interval.generic_number)
            if with_gamma.generic_interval
            else "None"
        )
    )
    print(f"  quality_generated={comparison.quality_generated}")
    print(f"  interval_label_generated={comparison.interval_label_generated}")
    print(f"  contextual_role_generated={comparison.contextual_role_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
