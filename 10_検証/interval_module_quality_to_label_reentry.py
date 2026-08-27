"""再入quality candidateからinterval label candidateへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_generic_to_quality_reentry import (
    GenericToQualityReentryObservation,
    compare_generic_to_quality_reentry,
)
from interval_module_label_boundary import (
    IntervalLabelCandidate,
    IntervalLabelGamma,
    gamma_interval_label_fixture,
    make_interval_label,
)


@dataclass(frozen=True)
class QualityToLabelReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_quality_reentry: bool


@dataclass(frozen=True)
class ReenteredIntervalLabelObservation:
    quality_reentry_observation: GenericToQualityReentryObservation
    interval_label_gamma: IntervalLabelGamma | None
    interval_label: IntervalLabelCandidate | None
    contextual_role_generated: bool
    target_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    generation_reason: str | None


@dataclass(frozen=True)
class QualityToLabelReentryObservation:
    quality_reentry_observation: GenericToQualityReentryObservation
    label_reentry_gamma: QualityToLabelReentryGamma | None
    interval_label_observation: ReenteredIntervalLabelObservation | None
    same_generic_interval: bool
    same_quality: bool
    interval_label_generated: bool
    contextual_role_generated: bool
    target_generated: bool
    harmonic_function_generated: bool
    status: str


def quality_reentry_observation() -> GenericToQualityReentryObservation:
    return compare_generic_to_quality_reentry()[1]


def label_reentry_gamma_fixture() -> QualityToLabelReentryGamma:
    return QualityToLabelReentryGamma(
        name="Gamma_reentered_quality_to_interval_label_fixture",
        reads=("reentered_generic_interval", "reentered_quality"),
        generated_by_quality_reentry=False,
    )


def generate_reentered_interval_label(
    quality_reentry_obs: GenericToQualityReentryObservation,
    interval_label_gamma: IntervalLabelGamma | None,
) -> ReenteredIntervalLabelObservation:
    quality_obs = quality_reentry_obs.quality_observation
    quality = quality_obs.quality if quality_obs else None
    if quality is None:
        return ReenteredIntervalLabelObservation(
            quality_reentry_obs,
            interval_label_gamma,
            None,
            False,
            False,
            False,
            False,
            "no_reentered_quality_candidate",
            None,
        )
    if interval_label_gamma is None:
        return ReenteredIntervalLabelObservation(
            quality_reentry_obs,
            None,
            None,
            False,
            False,
            False,
            False,
            "interval_label_not_generated_without_gamma",
            None,
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
    return ReenteredIntervalLabelObservation(
        quality_reentry_observation=quality_reentry_obs,
        interval_label_gamma=interval_label_gamma,
        interval_label=candidate,
        contextual_role_generated=False,
        target_generated=False,
        harmonic_function_generated=False,
        core_promoted=False,
        status="interval_label_candidate_observed_from_reentered_quality_not_contextualized",
        generation_reason="reentered_generic_interval_and_quality_read_by_Gamma_interval_label",
    )


def reenter_quality_to_interval_label(
    quality_reentry_obs: GenericToQualityReentryObservation,
    label_reentry_gamma: QualityToLabelReentryGamma | None,
) -> QualityToLabelReentryObservation:
    quality_obs = quality_reentry_obs.quality_observation
    quality = quality_obs.quality if quality_obs else None
    if quality is None:
        return QualityToLabelReentryObservation(
            quality_reentry_obs,
            label_reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            False,
            False,
            "no_reentered_quality_candidate",
        )
    if label_reentry_gamma is None:
        return QualityToLabelReentryObservation(
            quality_reentry_obs,
            None,
            None,
            True,
            True,
            False,
            False,
            False,
            False,
            "reentered_quality_not_connected_to_label_without_reentry_gamma",
        )

    label_obs = generate_reentered_interval_label(
        quality_reentry_obs, gamma_interval_label_fixture()
    )
    interval_label = label_obs.interval_label
    generic_obs = quality_reentry_obs.reentry_observation.generic_observation
    return QualityToLabelReentryObservation(
        quality_reentry_observation=quality_reentry_obs,
        label_reentry_gamma=label_reentry_gamma,
        interval_label_observation=label_obs,
        same_generic_interval=(
            generic_obs is not None
            and interval_label is not None
            and interval_label.generic_number == generic_obs.generic_interval.generic_number
        ),
        same_quality=(
            interval_label is not None
            and interval_label.source_quality_label == quality.label
            and interval_label.quality_code == quality.quality_code
        ),
        interval_label_generated=interval_label is not None,
        contextual_role_generated=label_obs.contextual_role_generated,
        target_generated=label_obs.target_generated,
        harmonic_function_generated=label_obs.harmonic_function_generated,
        status="reentered_quality_connected_to_interval_label_not_contextual_role",
    )


def compare_quality_to_label_reentry() -> tuple[
    QualityToLabelReentryObservation, QualityToLabelReentryObservation
]:
    quality_obs = quality_reentry_observation()
    return (
        reenter_quality_to_interval_label(quality_obs, None),
        reenter_quality_to_interval_label(quality_obs, label_reentry_gamma_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_quality_to_label_reentry()
    assert without_gamma.status == "reentered_quality_not_connected_to_label_without_reentry_gamma"
    assert without_gamma.interval_label_generated is False
    assert with_gamma.status == "reentered_quality_connected_to_interval_label_not_contextual_role"
    assert with_gamma.same_generic_interval is True
    assert with_gamma.same_quality is True
    assert with_gamma.interval_label_generated is True
    assert with_gamma.contextual_role_generated is False
    assert with_gamma.target_generated is False
    assert with_gamma.harmonic_function_generated is False
    assert with_gamma.interval_label_observation is not None
    assert with_gamma.interval_label_observation.interval_label is not None
    assert with_gamma.interval_label_observation.interval_label.label == "完全五度"
    assert with_gamma.interval_label_observation.interval_label.generic_number == 5
    assert with_gamma.interval_label_observation.interval_label.quality_code == "P"
    assert with_gamma.label_reentry_gamma is not None
    assert with_gamma.label_reentry_gamma.generated_by_quality_reentry is False


if __name__ == "__main__":
    run_checks()
    print(compare_quality_to_label_reentry()[1].status)
