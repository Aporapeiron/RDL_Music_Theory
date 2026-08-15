"""周波数差と弁別可能性をM_B^base候補として観測する最小検証。

50_既知基層解釈参照のA2を、基層M_B確定ではなく、
B_baseとΓ_baseを明示した候補関係として扱う。

    known A2 reference
      + B_base fixture
      + Γ_base fixture
      + behavioral response observations
      -> M_B^base candidate observed
      -> confirmed M_B remains false
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class KnownBaseReference:
    label: str
    relation_kind: str
    claim_scope: str


@dataclass(frozen=True)
class FrequencyPair:
    label: str
    base_frequency_hz: float
    comparison_frequency_hz: float

    @property
    def delta_frequency_hz(self) -> float:
        return abs(self.comparison_frequency_hz - self.base_frequency_hz)


@dataclass(frozen=True)
class DiscriminationBoundary:
    name: str
    base_frequency_hz: float
    stimulus_form: str
    stimulus_duration_ms: int
    response_axis: str
    measurement_form: str


@dataclass(frozen=True)
class BaseGamma:
    name: str
    compares: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class BehavioralResponseObservation:
    frequency_pair: FrequencyPair
    response_label: str
    discriminability_level: str
    observed_by: str
    generated_pitch_category: str | None


@dataclass(frozen=True)
class BaseCandidateObservation:
    reference: KnownBaseReference
    boundary: DiscriminationBoundary
    gamma: BaseGamma | None
    responses: tuple[BehavioralResponseObservation, ...]
    mb_base_candidate_label: str | None
    confirmed_mb_base: bool
    generated_pitch_category: str | None
    generated_semitone_category: str | None
    status: str


@dataclass(frozen=True)
class FrequencyDiscriminabilityComparison:
    with_gamma: BaseCandidateObservation
    without_gamma: BaseCandidateObservation
    same_boundary: bool
    same_gamma: bool
    different_physical_delta_f: bool
    different_behavioral_discriminability: bool
    candidate_observed: bool
    confirmed_mb_base: bool


def known_a2_reference() -> KnownBaseReference:
    return KnownBaseReference(
        label="A2 frequency-difference discriminability relation",
        relation_kind="physical_delta_f_to_behavioral_discriminability",
        claim_scope="fixture_limited_reference_point",
    )


def base_frequency_discrimination_boundary() -> DiscriminationBoundary:
    return DiscriminationBoundary(
        name="B_base_frequency_discrimination_fixture",
        base_frequency_hz=1000.0,
        stimulus_form="pure_tone_pair_fixture",
        stimulus_duration_ms=200,
        response_axis="same_different_behavioral_response",
        measurement_form="abstract_psychometric_response_label",
    )


def frequency_discrimination_gamma() -> BaseGamma:
    return BaseGamma(
        name="Gamma_frequency_discriminability_comparison_fixture",
        compares=("physical_delta_f", "behavioral_discriminability"),
        rule_scope="fixture_limited_not_general_psychometric_model",
    )


def behavioral_response_observations() -> tuple[
    BehavioralResponseObservation,
    BehavioralResponseObservation,
]:
    small_delta = FrequencyPair(
        label="small delta fixture pair",
        base_frequency_hz=1000.0,
        comparison_frequency_hz=1002.0,
    )
    larger_delta = FrequencyPair(
        label="larger delta fixture pair",
        base_frequency_hz=1000.0,
        comparison_frequency_hz=1040.0,
    )
    return (
        BehavioralResponseObservation(
            frequency_pair=small_delta,
            response_label="mostly_same_response_region",
            discriminability_level="low_discriminability",
            observed_by="fixture_behavioral_observation",
            generated_pitch_category=None,
        ),
        BehavioralResponseObservation(
            frequency_pair=larger_delta,
            response_label="mostly_different_response_region",
            discriminability_level="high_discriminability",
            observed_by="fixture_behavioral_observation",
            generated_pitch_category=None,
        ),
    )


def observe_base_candidate(
    reference: KnownBaseReference,
    boundary: DiscriminationBoundary,
    gamma: BaseGamma | None,
    responses: tuple[BehavioralResponseObservation, ...],
) -> BaseCandidateObservation:
    if gamma is None:
        return BaseCandidateObservation(
            reference=reference,
            boundary=boundary,
            gamma=None,
            responses=responses,
            mb_base_candidate_label=None,
            confirmed_mb_base=False,
            generated_pitch_category=None,
            generated_semitone_category=None,
            status="no_gamma_base_comparison",
        )

    delta_f_values = tuple(
        response.frequency_pair.delta_frequency_hz for response in responses
    )
    discriminability_levels = tuple(
        response.discriminability_level for response in responses
    )
    if len(set(delta_f_values)) < 2 or len(set(discriminability_levels)) < 2:
        return BaseCandidateObservation(
            reference=reference,
            boundary=boundary,
            gamma=gamma,
            responses=responses,
            mb_base_candidate_label=None,
            confirmed_mb_base=False,
            generated_pitch_category=None,
            generated_semitone_category=None,
            status="no_observed_delta_f_discriminability_difference",
        )

    return BaseCandidateObservation(
        reference=reference,
        boundary=boundary,
        gamma=gamma,
        responses=responses,
        mb_base_candidate_label=(
            "frequency_difference_to_behavioral_discriminability_candidate"
        ),
        confirmed_mb_base=False,
        generated_pitch_category=None,
        generated_semitone_category=None,
        status="mb_base_candidate_observed_not_confirmed",
    )


def compare_frequency_discriminability_candidate() -> FrequencyDiscriminabilityComparison:
    reference = known_a2_reference()
    boundary = base_frequency_discrimination_boundary()
    gamma = frequency_discrimination_gamma()
    responses = behavioral_response_observations()
    with_gamma = observe_base_candidate(reference, boundary, gamma, responses)
    without_gamma = observe_base_candidate(reference, boundary, None, responses)
    first, second = responses
    return FrequencyDiscriminabilityComparison(
        with_gamma=with_gamma,
        without_gamma=without_gamma,
        same_boundary=with_gamma.boundary == without_gamma.boundary,
        same_gamma=with_gamma.gamma == without_gamma.gamma,
        different_physical_delta_f=(
            first.frequency_pair.delta_frequency_hz
            != second.frequency_pair.delta_frequency_hz
        ),
        different_behavioral_discriminability=(
            first.discriminability_level != second.discriminability_level
        ),
        candidate_observed=with_gamma.status == "mb_base_candidate_observed_not_confirmed",
        confirmed_mb_base=with_gamma.confirmed_mb_base,
    )


def run_checks() -> None:
    comparison = compare_frequency_discriminability_candidate()
    assert comparison.same_boundary is True
    assert comparison.same_gamma is False
    assert comparison.different_physical_delta_f is True
    assert comparison.different_behavioral_discriminability is True
    assert comparison.candidate_observed is True
    assert comparison.confirmed_mb_base is False

    assert comparison.without_gamma.status == "no_gamma_base_comparison"
    assert comparison.with_gamma.generated_pitch_category is None
    assert comparison.with_gamma.generated_semitone_category is None
    assert comparison.with_gamma.mb_base_candidate_label is not None
    assert (
        comparison.with_gamma.reference.label
        == "A2 frequency-difference discriminability relation"
    )
    assert all(
        response.generated_pitch_category is None
        for response in comparison.with_gamma.responses
    )


def main() -> None:
    run_checks()
    comparison = compare_frequency_discriminability_candidate()
    observation = comparison.with_gamma

    print("[pipeline]")
    print("  known A2 reference")
    print("  + B_base_frequency_discrimination_fixture")
    print("  + Gamma_frequency_discriminability_comparison_fixture")
    print("  + behavioral response observations")
    print("  -> M_B^base candidate observed")
    print("  -> confirmed M_B remains false")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={observation.status}")
    print(f"  different_physical_delta_f={comparison.different_physical_delta_f}")
    print(
        "  different_behavioral_discriminability="
        f"{comparison.different_behavioral_discriminability}"
    )
    print(f"  candidate_observed={comparison.candidate_observed}")
    print(f"  confirmed_mb_base={comparison.confirmed_mb_base}")
    print(f"  generated_pitch_category={observation.generated_pitch_category}")
    print(
        "  generated_semitone_category="
        f"{observation.generated_semitone_category}"
    )
    print(
        "  responses="
        + ", ".join(
            f"delta_f={response.frequency_pair.delta_frequency_hz:g}Hz"
            f"->{response.discriminability_level}"
            for response in observation.responses
        )
    )


if __name__ == "__main__":
    main()
