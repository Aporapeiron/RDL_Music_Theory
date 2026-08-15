"""時間間隔差と統合/分離応答差をM_B^base候補として観測する最小検証。

50_既知基層解釈参照のA3を、基層M_B確定ではなく、
B_baseとΓ_baseを明示した候補関係として扱う。

    known A3 reference
      + B_base fixture
      + Γ_base fixture
      + perceptual response observations
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
class TemporalEventPair:
    label: str
    first_event_ms: float
    second_event_ms: float

    @property
    def temporal_separation_ms(self) -> float:
        return abs(self.second_event_ms - self.first_event_ms)


@dataclass(frozen=True)
class TemporalIntegrationBoundary:
    name: str
    stimulus_form: str
    event_duration_ms: int
    observation_window_ms: int
    response_axis: str
    measurement_form: str


@dataclass(frozen=True)
class BaseGamma:
    name: str
    compares: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class PerceptualResponseObservation:
    event_pair: TemporalEventPair
    response_label: str
    integration_state: str
    observed_by: str
    generated_rhythm_category: str | None


@dataclass(frozen=True)
class BaseCandidateObservation:
    reference: KnownBaseReference
    boundary: TemporalIntegrationBoundary
    gamma: BaseGamma | None
    responses: tuple[PerceptualResponseObservation, ...]
    mb_base_candidate_label: str | None
    confirmed_mb_base: bool
    generated_rhythm_category: str | None
    generated_meter_category: str | None
    status: str


@dataclass(frozen=True)
class TemporalIntegrationComparison:
    with_gamma: BaseCandidateObservation
    without_gamma: BaseCandidateObservation
    same_boundary: bool
    same_gamma: bool
    different_physical_temporal_separation: bool
    different_perceptual_integration_state: bool
    candidate_observed: bool
    confirmed_mb_base: bool


def known_a3_reference() -> KnownBaseReference:
    return KnownBaseReference(
        label="A3 temporal-separation integration relation",
        relation_kind="physical_temporal_separation_to_integration_response",
        claim_scope="fixture_limited_reference_point",
    )


def base_temporal_integration_boundary() -> TemporalIntegrationBoundary:
    return TemporalIntegrationBoundary(
        name="B_base_temporal_integration_fixture",
        stimulus_form="two_click_event_fixture",
        event_duration_ms=5,
        observation_window_ms=250,
        response_axis="integrated_or_separated_perceptual_response",
        measurement_form="abstract_temporal_response_label",
    )


def temporal_integration_gamma() -> BaseGamma:
    return BaseGamma(
        name="Gamma_temporal_integration_comparison_fixture",
        compares=("physical_temporal_separation", "perceptual_integration_state"),
        rule_scope="fixture_limited_not_general_temporal_integration_model",
    )


def perceptual_response_observations() -> tuple[
    PerceptualResponseObservation,
    PerceptualResponseObservation,
]:
    short_gap = TemporalEventPair(
        label="short separation fixture pair",
        first_event_ms=0.0,
        second_event_ms=8.0,
    )
    longer_gap = TemporalEventPair(
        label="longer separation fixture pair",
        first_event_ms=0.0,
        second_event_ms=80.0,
    )
    return (
        PerceptualResponseObservation(
            event_pair=short_gap,
            response_label="one_event_response_region",
            integration_state="integrated_response",
            observed_by="fixture_temporal_response_observation",
            generated_rhythm_category=None,
        ),
        PerceptualResponseObservation(
            event_pair=longer_gap,
            response_label="separate_events_response_region",
            integration_state="separated_response",
            observed_by="fixture_temporal_response_observation",
            generated_rhythm_category=None,
        ),
    )


def observe_base_candidate(
    reference: KnownBaseReference,
    boundary: TemporalIntegrationBoundary,
    gamma: BaseGamma | None,
    responses: tuple[PerceptualResponseObservation, ...],
) -> BaseCandidateObservation:
    if gamma is None:
        return BaseCandidateObservation(
            reference=reference,
            boundary=boundary,
            gamma=None,
            responses=responses,
            mb_base_candidate_label=None,
            confirmed_mb_base=False,
            generated_rhythm_category=None,
            generated_meter_category=None,
            status="no_gamma_base_comparison",
        )

    separations = tuple(
        response.event_pair.temporal_separation_ms for response in responses
    )
    integration_states = tuple(response.integration_state for response in responses)
    if len(set(separations)) < 2 or len(set(integration_states)) < 2:
        return BaseCandidateObservation(
            reference=reference,
            boundary=boundary,
            gamma=gamma,
            responses=responses,
            mb_base_candidate_label=None,
            confirmed_mb_base=False,
            generated_rhythm_category=None,
            generated_meter_category=None,
            status="no_observed_temporal_integration_difference",
        )

    return BaseCandidateObservation(
        reference=reference,
        boundary=boundary,
        gamma=gamma,
        responses=responses,
        mb_base_candidate_label=(
            "temporal_separation_to_integration_state_difference_candidate"
        ),
        confirmed_mb_base=False,
        generated_rhythm_category=None,
        generated_meter_category=None,
        status="mb_base_candidate_observed_not_confirmed",
    )


def compare_temporal_integration_candidate() -> TemporalIntegrationComparison:
    reference = known_a3_reference()
    boundary = base_temporal_integration_boundary()
    gamma = temporal_integration_gamma()
    responses = perceptual_response_observations()
    with_gamma = observe_base_candidate(reference, boundary, gamma, responses)
    without_gamma = observe_base_candidate(reference, boundary, None, responses)
    first, second = responses
    return TemporalIntegrationComparison(
        with_gamma=with_gamma,
        without_gamma=without_gamma,
        same_boundary=with_gamma.boundary == without_gamma.boundary,
        same_gamma=with_gamma.gamma == without_gamma.gamma,
        different_physical_temporal_separation=(
            first.event_pair.temporal_separation_ms
            != second.event_pair.temporal_separation_ms
        ),
        different_perceptual_integration_state=(
            first.integration_state != second.integration_state
        ),
        candidate_observed=with_gamma.status == "mb_base_candidate_observed_not_confirmed",
        confirmed_mb_base=with_gamma.confirmed_mb_base,
    )


def run_checks() -> None:
    comparison = compare_temporal_integration_candidate()
    assert comparison.same_boundary is True
    assert comparison.same_gamma is False
    assert comparison.different_physical_temporal_separation is True
    assert comparison.different_perceptual_integration_state is True
    assert comparison.candidate_observed is True
    assert comparison.confirmed_mb_base is False

    assert comparison.without_gamma.status == "no_gamma_base_comparison"
    assert comparison.with_gamma.generated_rhythm_category is None
    assert comparison.with_gamma.generated_meter_category is None
    assert comparison.with_gamma.mb_base_candidate_label is not None
    assert (
        comparison.with_gamma.reference.label
        == "A3 temporal-separation integration relation"
    )
    assert all(
        response.generated_rhythm_category is None
        for response in comparison.with_gamma.responses
    )


def main() -> None:
    run_checks()
    comparison = compare_temporal_integration_candidate()
    observation = comparison.with_gamma

    print("[pipeline]")
    print("  known A3 reference")
    print("  + B_base_temporal_integration_fixture")
    print("  + Gamma_temporal_integration_comparison_fixture")
    print("  + perceptual response observations")
    print("  -> M_B^base candidate observed")
    print("  -> confirmed M_B remains false")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={observation.status}")
    print(
        "  different_physical_temporal_separation="
        f"{comparison.different_physical_temporal_separation}"
    )
    print(
        "  different_perceptual_integration_state="
        f"{comparison.different_perceptual_integration_state}"
    )
    print(f"  candidate_observed={comparison.candidate_observed}")
    print(f"  confirmed_mb_base={comparison.confirmed_mb_base}")
    print(f"  generated_rhythm_category={observation.generated_rhythm_category}")
    print(f"  generated_meter_category={observation.generated_meter_category}")
    print(
        "  responses="
        + ", ".join(
            f"separation={response.event_pair.temporal_separation_ms:g}ms"
            f"->{response.integration_state}"
            for response in observation.responses
        )
    )


if __name__ == "__main__":
    main()
