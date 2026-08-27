"""再入selected targetからvoice leading requestへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_target_selection_reentry import (
    TargetSelectionReentryObservation,
    ReenteredTargetSelectionObservation,
    compare_target_selection_reentry,
)
from interval_module_voice_leading_plan_boundary import (
    VoiceLeadingPlan,
    VoiceLeadingRequestCandidate,
    VoiceLeadingRequestGamma,
    gamma_voice_leading_request_fixture,
    voice_leading_plan_fixture,
)


@dataclass(frozen=True)
class SelectedTargetToVoiceLeadingReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_target_selection_reentry: bool


@dataclass(frozen=True)
class ReenteredVoiceLeadingPlanObservation:
    target_selection_observation: ReenteredTargetSelectionObservation
    voice_leading_plan: VoiceLeadingPlan | None
    gamma_voice_leading_request: VoiceLeadingRequestGamma | None
    voice_leading_request: VoiceLeadingRequestCandidate | None
    concrete_realization_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    request_reason: str | None


@dataclass(frozen=True)
class SelectedTargetToVoiceLeadingReentryObservation:
    target_selection_reentry: TargetSelectionReentryObservation
    voice_leading_reentry_gamma: SelectedTargetToVoiceLeadingReentryGamma | None
    voice_leading_plan_observation: ReenteredVoiceLeadingPlanObservation | None
    same_selected_target: bool
    same_voice_leading_plan: bool
    request_observed: bool
    concrete_realization_generated: bool
    harmonic_function_generated: bool
    status: str


def target_selection_reentry_observation() -> TargetSelectionReentryObservation:
    return compare_target_selection_reentry()[1]


def voice_leading_reentry_gamma_fixture() -> SelectedTargetToVoiceLeadingReentryGamma:
    return SelectedTargetToVoiceLeadingReentryGamma(
        name="Gamma_reentered_selected_target_to_voice_leading_fixture",
        reads=("reentered_selected_target", "external_voice_leading_plan"),
        generated_by_target_selection_reentry=False,
    )


def create_reentered_voice_leading_request(
    target_selection: ReenteredTargetSelectionObservation,
    voice_leading_plan: VoiceLeadingPlan | None,
    gamma_voice_leading_request: VoiceLeadingRequestGamma | None,
) -> ReenteredVoiceLeadingPlanObservation:
    selected_target = target_selection.selected_target
    if selected_target is None:
        return ReenteredVoiceLeadingPlanObservation(
            target_selection,
            voice_leading_plan,
            gamma_voice_leading_request,
            None,
            False,
            False,
            False,
            "no_reentered_selected_interval_target",
            None,
        )
    if voice_leading_plan is None:
        return ReenteredVoiceLeadingPlanObservation(
            target_selection,
            None,
            gamma_voice_leading_request,
            None,
            False,
            False,
            False,
            "reentered_voice_leading_request_not_created_without_plan",
            None,
        )
    if gamma_voice_leading_request is None:
        return ReenteredVoiceLeadingPlanObservation(
            target_selection,
            voice_leading_plan,
            None,
            None,
            False,
            False,
            False,
            "reentered_voice_leading_request_not_created_without_gamma",
            None,
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
    return ReenteredVoiceLeadingPlanObservation(
        target_selection_observation=target_selection,
        voice_leading_plan=voice_leading_plan,
        gamma_voice_leading_request=gamma_voice_leading_request,
        voice_leading_request=request,
        concrete_realization_generated=False,
        harmonic_function_generated=False,
        core_promoted=False,
        status="voice_leading_request_observed_from_reentered_target_not_realized",
        request_reason="reentered_selected_target_and_external_plan_read_by_Gamma_voice_leading_request",
    )


def reenter_selected_target_to_voice_leading(
    target_selection_reentry: TargetSelectionReentryObservation,
    reentry_gamma: SelectedTargetToVoiceLeadingReentryGamma | None,
) -> SelectedTargetToVoiceLeadingReentryObservation:
    target_selection = target_selection_reentry.target_selection_observation
    if target_selection is None or target_selection.selected_target is None:
        return SelectedTargetToVoiceLeadingReentryObservation(
            target_selection_reentry,
            reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            False,
            "no_reentered_selected_interval_target",
        )
    if reentry_gamma is None:
        return SelectedTargetToVoiceLeadingReentryObservation(
            target_selection_reentry,
            None,
            None,
            True,
            False,
            False,
            False,
            False,
            "reentered_selected_target_not_connected_to_voice_leading_without_reentry_gamma",
        )

    plan = voice_leading_plan_fixture()
    request_obs = create_reentered_voice_leading_request(
        target_selection, plan, gamma_voice_leading_request_fixture()
    )
    return SelectedTargetToVoiceLeadingReentryObservation(
        target_selection_reentry=target_selection_reentry,
        voice_leading_reentry_gamma=reentry_gamma,
        voice_leading_plan_observation=request_obs,
        same_selected_target=(
            request_obs.target_selection_observation.selected_target
            == target_selection.selected_target
        ),
        same_voice_leading_plan=request_obs.voice_leading_plan == plan,
        request_observed=request_obs.voice_leading_request is not None,
        concrete_realization_generated=request_obs.concrete_realization_generated,
        harmonic_function_generated=request_obs.harmonic_function_generated,
        status="reentered_selected_target_connected_to_voice_leading_request_not_realized",
    )


def compare_selected_target_to_voice_leading_reentry() -> tuple[
    SelectedTargetToVoiceLeadingReentryObservation,
    SelectedTargetToVoiceLeadingReentryObservation,
]:
    selected = target_selection_reentry_observation()
    return (
        reenter_selected_target_to_voice_leading(selected, None),
        reenter_selected_target_to_voice_leading(
            selected, voice_leading_reentry_gamma_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_selected_target_to_voice_leading_reentry()
    assert (
        without_gamma.status
        == "reentered_selected_target_not_connected_to_voice_leading_without_reentry_gamma"
    )
    assert without_gamma.request_observed is False
    assert (
        with_gamma.status
        == "reentered_selected_target_connected_to_voice_leading_request_not_realized"
    )
    assert with_gamma.same_selected_target is True
    assert with_gamma.same_voice_leading_plan is True
    assert with_gamma.request_observed is True
    assert with_gamma.concrete_realization_generated is False
    assert with_gamma.harmonic_function_generated is False
    assert with_gamma.voice_leading_plan_observation is not None
    assert with_gamma.voice_leading_plan_observation.voice_leading_request is not None
    assert (
        with_gamma.voice_leading_plan_observation.voice_leading_request.label
        == "maintain_C_G_span_voice_leading_request_candidate"
    )


if __name__ == "__main__":
    run_checks()
    print(compare_selected_target_to_voice_leading_reentry()[1].status)
