"""音程Module voice leading requestと具体実現境界の最小検証。"""

from dataclasses import dataclass

from interval_module_voice_leading_plan_boundary import (
    VoiceLeadingPlanObservation,
    compare_voice_leading_plan_boundary,
)


@dataclass(frozen=True)
class VoiceLeadingRealizationBoundary:
    name: str
    lower_voice_range: tuple[str, str]
    upper_voice_range: tuple[str, str]
    candidate_octaves: tuple[int, ...]
    generated_by_voice_leading_request: bool


@dataclass(frozen=True)
class VoiceLeadingRealizationGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class ConcreteVoiceLeadingObservation:
    label: str
    source_request_label: str
    lower_pitch: str
    upper_pitch: str
    lower_motion: int
    upper_motion: int
    harmonic_function_generated: bool
    next_context_generated: bool


@dataclass(frozen=True)
class VoiceLeadingRealizationObservation:
    plan_observation: VoiceLeadingPlanObservation
    realization_boundary: VoiceLeadingRealizationBoundary | None
    gamma_realization: VoiceLeadingRealizationGamma | None
    concrete_voice_leading: ConcreteVoiceLeadingObservation | None
    harmonic_function_generated: bool
    next_context_generated: bool
    core_promoted: bool
    status: str
    realization_reason: str | None


@dataclass(frozen=True)
class VoiceLeadingRealizationComparison:
    without_gamma: VoiceLeadingRealizationObservation
    with_gamma: VoiceLeadingRealizationObservation
    same_voice_leading_request: bool
    same_realization_boundary: bool
    same_gamma_realization: bool
    concrete_voice_leading_observed: bool
    harmonic_function_generated: bool
    next_context_generated: bool
    core_promoted: bool


def plan_observation() -> VoiceLeadingPlanObservation:
    return compare_voice_leading_plan_boundary().with_gamma


def realization_boundary_fixture() -> VoiceLeadingRealizationBoundary:
    return VoiceLeadingRealizationBoundary(
        name="C_G_span_realization_boundary_fixture",
        lower_voice_range=("C3", "C5"),
        upper_voice_range=("G3", "G5"),
        candidate_octaves=(3, 4, 5),
        generated_by_voice_leading_request=False,
    )


def gamma_realization_fixture() -> VoiceLeadingRealizationGamma:
    return VoiceLeadingRealizationGamma(
        name="Gamma_voice_leading_realization_fixture",
        reads=("voice_leading_request", "external_realization_boundary"),
        rule_scope="fixture_limited_not_harmonic_function_or_next_context_rule",
    )


def realize_voice_leading(
    plan: VoiceLeadingPlanObservation,
    boundary: VoiceLeadingRealizationBoundary | None,
    gamma_realization: VoiceLeadingRealizationGamma | None,
) -> VoiceLeadingRealizationObservation:
    request = plan.voice_leading_request
    if request is None:
        return VoiceLeadingRealizationObservation(
            plan_observation=plan,
            realization_boundary=boundary,
            gamma_realization=gamma_realization,
            concrete_voice_leading=None,
            harmonic_function_generated=False,
            next_context_generated=False,
            core_promoted=False,
            status="no_voice_leading_request_candidate",
            realization_reason=None,
        )
    if boundary is None:
        return VoiceLeadingRealizationObservation(
            plan_observation=plan,
            realization_boundary=None,
            gamma_realization=gamma_realization,
            concrete_voice_leading=None,
            harmonic_function_generated=False,
            next_context_generated=False,
            core_promoted=False,
            status="voice_leading_not_realized_without_boundary",
            realization_reason=None,
        )
    if gamma_realization is None:
        return VoiceLeadingRealizationObservation(
            plan_observation=plan,
            realization_boundary=boundary,
            gamma_realization=None,
            concrete_voice_leading=None,
            harmonic_function_generated=False,
            next_context_generated=False,
            core_promoted=False,
            status="voice_leading_not_realized_without_gamma",
            realization_reason=None,
        )

    concrete = ConcreteVoiceLeadingObservation(
        label="C4_G4_voice_leading_observation",
        source_request_label=request.label,
        lower_pitch="C4",
        upper_pitch="G4",
        lower_motion=0,
        upper_motion=0,
        harmonic_function_generated=False,
        next_context_generated=False,
    )
    return VoiceLeadingRealizationObservation(
        plan_observation=plan,
        realization_boundary=boundary,
        gamma_realization=gamma_realization,
        concrete_voice_leading=concrete,
        harmonic_function_generated=False,
        next_context_generated=False,
        core_promoted=False,
        status="concrete_voice_leading_observed_not_interpreted",
        realization_reason="request_and_external_boundary_read_by_Gamma_voice_leading_realization",
    )


def compare_voice_leading_realization() -> VoiceLeadingRealizationComparison:
    plan = plan_observation()
    boundary = realization_boundary_fixture()
    without_gamma = realize_voice_leading(plan, boundary, None)
    with_gamma = realize_voice_leading(plan, boundary, gamma_realization_fixture())
    return VoiceLeadingRealizationComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_voice_leading_request=(
            without_gamma.plan_observation.voice_leading_request
            == with_gamma.plan_observation.voice_leading_request
        ),
        same_realization_boundary=(
            without_gamma.realization_boundary == with_gamma.realization_boundary
        ),
        same_gamma_realization=without_gamma.gamma_realization == with_gamma.gamma_realization,
        concrete_voice_leading_observed=(
            with_gamma.status == "concrete_voice_leading_observed_not_interpreted"
        ),
        harmonic_function_generated=with_gamma.harmonic_function_generated,
        next_context_generated=with_gamma.next_context_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_voice_leading_realization()
    assert comparison.same_voice_leading_request is True
    assert comparison.same_realization_boundary is True
    assert comparison.same_gamma_realization is False
    assert comparison.concrete_voice_leading_observed is True
    assert comparison.harmonic_function_generated is False
    assert comparison.next_context_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_gamma.status
        == "voice_leading_not_realized_without_gamma"
    )
    assert comparison.without_gamma.concrete_voice_leading is None
    assert comparison.with_gamma.concrete_voice_leading is not None
    assert comparison.with_gamma.concrete_voice_leading.lower_pitch == "C4"
    assert comparison.with_gamma.concrete_voice_leading.upper_pitch == "G4"
    assert comparison.with_gamma.concrete_voice_leading.lower_motion == 0
    assert comparison.with_gamma.concrete_voice_leading.upper_motion == 0
    assert comparison.with_gamma.realization_boundary is not None
    assert comparison.with_gamma.realization_boundary.generated_by_voice_leading_request is False


def main() -> None:
    run_checks()
    comparison = compare_voice_leading_realization()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  voice leading request candidate")
    print("  + external realization boundary")
    print("  + Gamma_voice_leading_realization_fixture")
    print("  -> concrete voice leading observation")
    print("  -> harmonic function and next context remain None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_voice_leading_request={comparison.same_voice_leading_request}")
    print(f"  same_realization_boundary={comparison.same_realization_boundary}")
    print(f"  same_gamma_realization={comparison.same_gamma_realization}")
    print(f"  concrete_voice_leading_observed={comparison.concrete_voice_leading_observed}")
    print(
        "  concrete_voice_leading="
        + (
            f"{with_gamma.concrete_voice_leading.lower_pitch}-"
            f"{with_gamma.concrete_voice_leading.upper_pitch}"
            if with_gamma.concrete_voice_leading
            else "None"
        )
    )
    print(f"  harmonic_function_generated={comparison.harmonic_function_generated}")
    print(f"  next_context_generated={comparison.next_context_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
