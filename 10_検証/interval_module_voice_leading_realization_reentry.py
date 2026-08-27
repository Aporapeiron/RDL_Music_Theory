"""再入voice leading requestからconcrete voice leadingへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_selected_target_to_voice_leading_reentry import (
    ReenteredVoiceLeadingPlanObservation,
    SelectedTargetToVoiceLeadingReentryObservation,
    compare_selected_target_to_voice_leading_reentry,
)
from interval_module_voice_leading_realization_boundary import (
    ConcreteVoiceLeadingObservation,
    VoiceLeadingRealizationBoundary,
    VoiceLeadingRealizationGamma,
    gamma_realization_fixture,
    realization_boundary_fixture,
)


@dataclass(frozen=True)
class VoiceLeadingRealizationReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_voice_leading_reentry: bool


@dataclass(frozen=True)
class ReenteredVoiceLeadingRealizationObservation:
    plan_observation: ReenteredVoiceLeadingPlanObservation
    realization_boundary: VoiceLeadingRealizationBoundary | None
    gamma_realization: VoiceLeadingRealizationGamma | None
    concrete_voice_leading: ConcreteVoiceLeadingObservation | None
    harmonic_function_generated: bool
    next_context_generated: bool
    core_promoted: bool
    status: str
    realization_reason: str | None


@dataclass(frozen=True)
class VoiceLeadingRealizationReentryObservation:
    voice_leading_reentry: SelectedTargetToVoiceLeadingReentryObservation
    realization_reentry_gamma: VoiceLeadingRealizationReentryGamma | None
    realization_observation: ReenteredVoiceLeadingRealizationObservation | None
    same_voice_leading_request: bool
    same_realization_boundary: bool
    concrete_voice_leading_observed: bool
    harmonic_function_generated: bool
    next_context_generated: bool
    status: str


def voice_leading_reentry_observation() -> SelectedTargetToVoiceLeadingReentryObservation:
    return compare_selected_target_to_voice_leading_reentry()[1]


def realization_reentry_gamma_fixture() -> VoiceLeadingRealizationReentryGamma:
    return VoiceLeadingRealizationReentryGamma(
        name="Gamma_reentered_voice_leading_request_to_realization_fixture",
        reads=("reentered_voice_leading_request", "external_realization_boundary"),
        generated_by_voice_leading_reentry=False,
    )


def realize_reentered_voice_leading(
    plan_obs: ReenteredVoiceLeadingPlanObservation,
    boundary: VoiceLeadingRealizationBoundary | None,
    gamma_realization: VoiceLeadingRealizationGamma | None,
) -> ReenteredVoiceLeadingRealizationObservation:
    request = plan_obs.voice_leading_request
    if request is None:
        return ReenteredVoiceLeadingRealizationObservation(
            plan_obs,
            boundary,
            gamma_realization,
            None,
            False,
            False,
            False,
            "no_reentered_voice_leading_request_candidate",
            None,
        )
    if boundary is None:
        return ReenteredVoiceLeadingRealizationObservation(
            plan_obs,
            None,
            gamma_realization,
            None,
            False,
            False,
            False,
            "reentered_voice_leading_not_realized_without_boundary",
            None,
        )
    if gamma_realization is None:
        return ReenteredVoiceLeadingRealizationObservation(
            plan_obs,
            boundary,
            None,
            None,
            False,
            False,
            False,
            "reentered_voice_leading_not_realized_without_gamma",
            None,
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
    return ReenteredVoiceLeadingRealizationObservation(
        plan_observation=plan_obs,
        realization_boundary=boundary,
        gamma_realization=gamma_realization,
        concrete_voice_leading=concrete,
        harmonic_function_generated=False,
        next_context_generated=False,
        core_promoted=False,
        status="concrete_voice_leading_observed_from_reentered_request_not_interpreted",
        realization_reason="reentered_request_and_external_boundary_read_by_Gamma_voice_leading_realization",
    )


def reenter_voice_leading_to_realization(
    voice_leading_reentry: SelectedTargetToVoiceLeadingReentryObservation,
    reentry_gamma: VoiceLeadingRealizationReentryGamma | None,
) -> VoiceLeadingRealizationReentryObservation:
    plan_obs = voice_leading_reentry.voice_leading_plan_observation
    if plan_obs is None or plan_obs.voice_leading_request is None:
        return VoiceLeadingRealizationReentryObservation(
            voice_leading_reentry,
            reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            False,
            "no_reentered_voice_leading_request_candidate",
        )
    if reentry_gamma is None:
        return VoiceLeadingRealizationReentryObservation(
            voice_leading_reentry,
            None,
            None,
            True,
            False,
            False,
            False,
            False,
            "reentered_voice_leading_request_not_connected_to_realization_without_reentry_gamma",
        )

    boundary = realization_boundary_fixture()
    realization_obs = realize_reentered_voice_leading(
        plan_obs, boundary, gamma_realization_fixture()
    )
    return VoiceLeadingRealizationReentryObservation(
        voice_leading_reentry=voice_leading_reentry,
        realization_reentry_gamma=reentry_gamma,
        realization_observation=realization_obs,
        same_voice_leading_request=(
            realization_obs.plan_observation.voice_leading_request
            == plan_obs.voice_leading_request
        ),
        same_realization_boundary=realization_obs.realization_boundary == boundary,
        concrete_voice_leading_observed=realization_obs.concrete_voice_leading is not None,
        harmonic_function_generated=realization_obs.harmonic_function_generated,
        next_context_generated=realization_obs.next_context_generated,
        status="reentered_voice_leading_request_connected_to_realization_not_next_context",
    )


def compare_voice_leading_realization_reentry() -> tuple[
    VoiceLeadingRealizationReentryObservation,
    VoiceLeadingRealizationReentryObservation,
]:
    voice_leading_obs = voice_leading_reentry_observation()
    return (
        reenter_voice_leading_to_realization(voice_leading_obs, None),
        reenter_voice_leading_to_realization(
            voice_leading_obs, realization_reentry_gamma_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_voice_leading_realization_reentry()
    assert (
        without_gamma.status
        == "reentered_voice_leading_request_not_connected_to_realization_without_reentry_gamma"
    )
    assert without_gamma.concrete_voice_leading_observed is False
    assert (
        with_gamma.status
        == "reentered_voice_leading_request_connected_to_realization_not_next_context"
    )
    assert with_gamma.same_voice_leading_request is True
    assert with_gamma.same_realization_boundary is True
    assert with_gamma.concrete_voice_leading_observed is True
    assert with_gamma.harmonic_function_generated is False
    assert with_gamma.next_context_generated is False
    assert with_gamma.realization_observation is not None
    assert with_gamma.realization_observation.concrete_voice_leading is not None
    assert with_gamma.realization_observation.concrete_voice_leading.lower_pitch == "C4"
    assert with_gamma.realization_observation.concrete_voice_leading.upper_pitch == "G4"


if __name__ == "__main__":
    run_checks()
    print(compare_voice_leading_realization_reentry()[1].status)
