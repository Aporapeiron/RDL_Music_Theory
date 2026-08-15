"""周波数入力差と周波数選択的応答差をM_B^base候補として観測する最小検証。

50_既知基層解釈参照のA1を、基層M_B確定ではなく、
B_baseとΓ_baseを明示した候補関係として扱う。

    known A1 reference
      + B_base fixture
      + Γ_base fixture
      + response observations
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
class BaseBoundary:
    name: str
    frequency_range_hz: tuple[float, float]
    stimulus_form: str
    response_axis: str
    measurement_form: str


@dataclass(frozen=True)
class BaseGamma:
    name: str
    compares: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class FrequencyInput:
    label: str
    frequency_hz: float


@dataclass(frozen=True)
class ResponseObservation:
    input_frequency: FrequencyInput
    response_selective_region: str
    observed_by: str


@dataclass(frozen=True)
class BaseCandidateObservation:
    reference: KnownBaseReference
    boundary: BaseBoundary
    gamma: BaseGamma | None
    responses: tuple[ResponseObservation, ...]
    mb_base_candidate_label: str | None
    confirmed_mb_base: bool
    generated_pitch_category: str | None
    status: str


@dataclass(frozen=True)
class FrequencyResponseComparison:
    with_gamma: BaseCandidateObservation
    without_gamma: BaseCandidateObservation
    same_boundary: bool
    same_gamma: bool
    different_frequency_inputs: bool
    different_response_regions: bool
    candidate_observed: bool
    confirmed_mb_base: bool


def known_a1_reference() -> KnownBaseReference:
    return KnownBaseReference(
        label="A1 frequency-selective response relation",
        relation_kind="physical_frequency_to_frequency_selective_response",
        claim_scope="fixture_limited_reference_point",
    )


def base_frequency_response_boundary() -> BaseBoundary:
    return BaseBoundary(
        name="B_base_frequency_response_fixture",
        frequency_range_hz=(100.0, 5000.0),
        stimulus_form="pure_tone_fixture",
        response_axis="frequency_selective_region",
        measurement_form="abstract_response_label",
    )


def frequency_response_gamma() -> BaseGamma:
    return BaseGamma(
        name="Gamma_frequency_response_comparison_fixture",
        compares=("physical_frequency_input", "response_selective_region"),
        rule_scope="fixture_limited_not_general_auditory_model",
    )


def response_observations() -> tuple[ResponseObservation, ResponseObservation]:
    low_input = FrequencyInput(label="low fixture tone", frequency_hz=500.0)
    high_input = FrequencyInput(label="high fixture tone", frequency_hz=2000.0)
    return (
        ResponseObservation(
            input_frequency=low_input,
            response_selective_region="low_frequency_response_region",
            observed_by="fixture_response_observation",
        ),
        ResponseObservation(
            input_frequency=high_input,
            response_selective_region="high_frequency_response_region",
            observed_by="fixture_response_observation",
        ),
    )


def observe_base_candidate(
    reference: KnownBaseReference,
    boundary: BaseBoundary,
    gamma: BaseGamma | None,
    responses: tuple[ResponseObservation, ...],
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
            status="no_gamma_base_comparison",
        )

    frequencies = tuple(response.input_frequency.frequency_hz for response in responses)
    regions = tuple(response.response_selective_region for response in responses)
    if len(set(frequencies)) < 2 or len(set(regions)) < 2:
        return BaseCandidateObservation(
            reference=reference,
            boundary=boundary,
            gamma=gamma,
            responses=responses,
            mb_base_candidate_label=None,
            confirmed_mb_base=False,
            generated_pitch_category=None,
            status="no_observed_frequency_response_difference",
        )

    return BaseCandidateObservation(
        reference=reference,
        boundary=boundary,
        gamma=gamma,
        responses=responses,
        mb_base_candidate_label=(
            "frequency_input_difference_to_frequency_selective_response_difference_candidate"
        ),
        confirmed_mb_base=False,
        generated_pitch_category=None,
        status="mb_base_candidate_observed_not_confirmed",
    )


def compare_frequency_response_candidate() -> FrequencyResponseComparison:
    reference = known_a1_reference()
    boundary = base_frequency_response_boundary()
    gamma = frequency_response_gamma()
    responses = response_observations()
    with_gamma = observe_base_candidate(reference, boundary, gamma, responses)
    without_gamma = observe_base_candidate(reference, boundary, None, responses)
    first, second = responses
    return FrequencyResponseComparison(
        with_gamma=with_gamma,
        without_gamma=without_gamma,
        same_boundary=with_gamma.boundary == without_gamma.boundary,
        same_gamma=with_gamma.gamma == without_gamma.gamma,
        different_frequency_inputs=(
            first.input_frequency.frequency_hz != second.input_frequency.frequency_hz
        ),
        different_response_regions=(
            first.response_selective_region != second.response_selective_region
        ),
        candidate_observed=with_gamma.status == "mb_base_candidate_observed_not_confirmed",
        confirmed_mb_base=with_gamma.confirmed_mb_base,
    )


def run_checks() -> None:
    comparison = compare_frequency_response_candidate()
    assert comparison.same_boundary is True
    assert comparison.same_gamma is False
    assert comparison.different_frequency_inputs is True
    assert comparison.different_response_regions is True
    assert comparison.candidate_observed is True
    assert comparison.confirmed_mb_base is False

    assert comparison.without_gamma.status == "no_gamma_base_comparison"
    assert comparison.with_gamma.generated_pitch_category is None
    assert comparison.with_gamma.mb_base_candidate_label is not None
    assert comparison.with_gamma.reference.label == "A1 frequency-selective response relation"


def main() -> None:
    run_checks()
    comparison = compare_frequency_response_candidate()
    observation = comparison.with_gamma

    print("[pipeline]")
    print("  known A1 reference")
    print("  + B_base_frequency_response_fixture")
    print("  + Gamma_frequency_response_comparison_fixture")
    print("  + response observations")
    print("  -> M_B^base candidate observed")
    print("  -> confirmed M_B remains false")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={observation.status}")
    print(f"  different_frequency_inputs={comparison.different_frequency_inputs}")
    print(f"  different_response_regions={comparison.different_response_regions}")
    print(f"  candidate_observed={comparison.candidate_observed}")
    print(f"  confirmed_mb_base={comparison.confirmed_mb_base}")
    print(f"  generated_pitch_category={observation.generated_pitch_category}")
    print("  responses=" + ", ".join(
        f"{response.input_frequency.frequency_hz:g}Hz->{response.response_selective_region}"
        for response in observation.responses
    ))


if __name__ == "__main__":
    main()