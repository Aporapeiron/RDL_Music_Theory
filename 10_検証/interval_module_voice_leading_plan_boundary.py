"""音程Module selected targetとvoice leading計画境界の最小検証。"""

from dataclasses import dataclass

from interval_module_target_selection_boundary import (
    IntervalTargetSelectionObservation,
    compare_interval_target_selection,
)


@dataclass(frozen=True)
class VoiceLeadingPlan:
    name: str
    lower_target_degree: int
    upper_target_degree: int
    realization_scope: str
    generated_by_selected_target: bool


@dataclass(frozen=True)
class VoiceLeadingRequestGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class VoiceLeadingRequestCandidate:
    label: str
    source_selected_target_label: str
    plan_name: str
    lower_target_degree: int
    upper_target_degree: int
    concrete_realization_generated: bool
    harmonic_function_generated: bool


@dataclass(frozen=True)
class VoiceLeadingPlanObservation:
    target_selection_observation: IntervalTargetSelectionObservation
    voice_leading_plan: VoiceLeadingPlan | None
    gamma_voice_leading_request: VoiceLeadingRequestGamma | None
    voice_leading_request: VoiceLeadingRequestCandidate | None
    concrete_realization_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    request_reason: str | None


@dataclass(frozen=True)
class VoiceLeadingPlanComparison:
    without_gamma: VoiceLeadingPlanObservation
    with_gamma: VoiceLeadingPlanObservation
    same_selected_target: bool
    same_voice_leading_plan: bool
    same_gamma_voice_leading_request: bool
    request_observed: bool
    concrete_realization_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool


def target_selection_observation() -> IntervalTargetSelectionObservation:
    return compare_interval_target_selection().with_controller


def voice_leading_plan_fixture() -> VoiceLeadingPlan:
    return VoiceLeadingPlan(
        name="maintain_C_G_span_realization_plan_fixture",
        lower_target_degree=1,
        upper_target_degree=5,
        realization_scope="interval_module_fixture",
        generated_by_selected_target=False,
    )


def gamma_voice_leading_request_fixture() -> VoiceLeadingRequestGamma:
    return VoiceLeadingRequestGamma(
        name="Gamma_voice_leading_request_fixture",
        reads=("selected_interval_target", "external_voice_leading_plan"),
        rule_scope="fixture_limited_not_concrete_realization_rule",
    )


def create_voice_leading_request(
    target_selection: IntervalTargetSelectionObservation,
    voice_leading_plan: VoiceLeadingPlan | None,
    gamma_voice_leading_request: VoiceLeadingRequestGamma | None,
) -> VoiceLeadingPlanObservation:
    selected_target = target_selection.selected_target
    if selected_target is None:
        return VoiceLeadingPlanObservation(
            target_selection_observation=target_selection,
            voice_leading_plan=voice_leading_plan,
            gamma_voice_leading_request=gamma_voice_leading_request,
            voice_leading_request=None,
            concrete_realization_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="no_selected_interval_target",
            request_reason=None,
        )
    if voice_leading_plan is None:
        return VoiceLeadingPlanObservation(
            target_selection_observation=target_selection,
            voice_leading_plan=None,
            gamma_voice_leading_request=gamma_voice_leading_request,
            voice_leading_request=None,
            concrete_realization_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="voice_leading_request_not_created_without_plan",
            request_reason=None,
        )
    if gamma_voice_leading_request is None:
        return VoiceLeadingPlanObservation(
            target_selection_observation=target_selection,
            voice_leading_plan=voice_leading_plan,
            gamma_voice_leading_request=None,
            voice_leading_request=None,
            concrete_realization_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="voice_leading_request_not_created_without_gamma",
            request_reason=None,
        )

    request = VoiceLeadingRequestCandidate(
        label="maintain_C_G_span_voice_leading_request_candidate",
        source_selected_target_label=selected_target.label,
        plan_name=voice_leading_plan.name,
        lower_target_degree=voice_leading_plan.lower_target_degree,
        upper_target_degree=voice_leading_plan.upper_target_degree,
        concrete_realization_generated=False,
        harmonic_function_generated=False,
    )
    return VoiceLeadingPlanObservation(
        target_selection_observation=target_selection,
        voice_leading_plan=voice_leading_plan,
        gamma_voice_leading_request=gamma_voice_leading_request,
        voice_leading_request=request,
        concrete_realization_generated=False,
        harmonic_function_generated=False,
        core_promoted=False,
        status="voice_leading_request_observed_not_realized",
        request_reason="selected_target_and_external_plan_read_by_Gamma_voice_leading_request",
    )


def compare_voice_leading_plan_boundary() -> VoiceLeadingPlanComparison:
    target_selection = target_selection_observation()
    plan = voice_leading_plan_fixture()
    without_gamma = create_voice_leading_request(target_selection, plan, None)
    with_gamma = create_voice_leading_request(
        target_selection, plan, gamma_voice_leading_request_fixture()
    )
    return VoiceLeadingPlanComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_selected_target=(
            without_gamma.target_selection_observation.selected_target
            == with_gamma.target_selection_observation.selected_target
        ),
        same_voice_leading_plan=without_gamma.voice_leading_plan == with_gamma.voice_leading_plan,
        same_gamma_voice_leading_request=(
            without_gamma.gamma_voice_leading_request
            == with_gamma.gamma_voice_leading_request
        ),
        request_observed=with_gamma.status == "voice_leading_request_observed_not_realized",
        concrete_realization_generated=with_gamma.concrete_realization_generated,
        harmonic_function_generated=with_gamma.harmonic_function_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_voice_leading_plan_boundary()
    assert comparison.same_selected_target is True
    assert comparison.same_voice_leading_plan is True
    assert comparison.same_gamma_voice_leading_request is False
    assert comparison.request_observed is True
    assert comparison.concrete_realization_generated is False
    assert comparison.harmonic_function_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_gamma.status
        == "voice_leading_request_not_created_without_gamma"
    )
    assert comparison.without_gamma.voice_leading_request is None
    assert comparison.with_gamma.voice_leading_request is not None
    assert comparison.with_gamma.voice_leading_request.label == (
        "maintain_C_G_span_voice_leading_request_candidate"
    )
    assert comparison.with_gamma.voice_leading_request.lower_target_degree == 1
    assert comparison.with_gamma.voice_leading_request.upper_target_degree == 5
    assert comparison.with_gamma.voice_leading_plan is not None
    assert comparison.with_gamma.voice_leading_plan.generated_by_selected_target is False


def main() -> None:
    run_checks()
    comparison = compare_voice_leading_plan_boundary()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  selected interval target candidate")
    print("  + external voice leading plan")
    print("  + Gamma_voice_leading_request_fixture")
    print("  -> voice leading request candidate")
    print("  -> concrete realization remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_selected_target={comparison.same_selected_target}")
    print(f"  same_voice_leading_plan={comparison.same_voice_leading_plan}")
    print(f"  same_gamma_voice_leading_request={comparison.same_gamma_voice_leading_request}")
    print(f"  request_observed={comparison.request_observed}")
    print(
        "  voice_leading_request="
        + (with_gamma.voice_leading_request.label if with_gamma.voice_leading_request else "None")
    )
    print(f"  concrete_realization_generated={comparison.concrete_realization_generated}")
    print(f"  harmonic_function_generated={comparison.harmonic_function_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
