"""再入generic intervalからquality candidateへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_processing_frame_reentry import (
    ProcessingFrameReentryObservation,
    compare_processing_frame_reentry,
)
from interval_module_quality_boundary import QualityCandidate, QualityGamma, gamma_quality_fixture, quality_code


@dataclass(frozen=True)
class GenericToQualityReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_generic_reentry: bool


@dataclass(frozen=True)
class ReenteredQualityObservation:
    reentry_observation: ProcessingFrameReentryObservation
    quality_gamma: QualityGamma | None
    quality: QualityCandidate | None
    interval_label_generated: bool
    contextual_role_generated: bool
    target_generated: bool
    core_promoted: bool
    status: str
    generation_reason: str | None


@dataclass(frozen=True)
class GenericToQualityReentryObservation:
    reentry_observation: ProcessingFrameReentryObservation
    quality_reentry_gamma: GenericToQualityReentryGamma | None
    quality_observation: ReenteredQualityObservation | None
    same_generic_interval: bool
    same_chromatic_distance: bool
    quality_generated: bool
    interval_label_generated: bool
    contextual_role_generated: bool
    status: str


def generic_reentry_observation() -> ProcessingFrameReentryObservation:
    return compare_processing_frame_reentry()[1]


def quality_reentry_gamma_fixture() -> GenericToQualityReentryGamma:
    return GenericToQualityReentryGamma(
        name="Gamma_reentered_generic_to_quality_fixture",
        reads=("reentered_generic_interval", "payload_chromatic_distance"),
        generated_by_generic_reentry=False,
    )


def generate_reentered_quality(
    reentry_obs: ProcessingFrameReentryObservation,
    quality_gamma: QualityGamma | None,
) -> ReenteredQualityObservation:
    generic_obs = reentry_obs.generic_observation
    generic = generic_obs.generic_interval if generic_obs else None
    payload = generic_obs.frame_payload_view.pitch_payload if generic_obs else None
    if generic is None:
        return ReenteredQualityObservation(
            reentry_obs,
            quality_gamma,
            None,
            False,
            False,
            False,
            False,
            "no_reentered_generic_interval_candidate",
            None,
        )
    if payload is None:
        return ReenteredQualityObservation(
            reentry_obs,
            quality_gamma,
            None,
            False,
            False,
            False,
            False,
            "no_reentered_chromatic_distance_payload",
            None,
        )
    if quality_gamma is None:
        return ReenteredQualityObservation(
            reentry_obs,
            None,
            None,
            False,
            False,
            False,
            False,
            "quality_not_generated_without_gamma",
            None,
        )

    candidate = QualityCandidate(
        label="quality_perfect_candidate",
        source_generic_interval_label=generic.label,
        generic_number=generic.generic_number,
        chromatic_distance=payload.chromatic_distance,
        quality_code=quality_code(generic.generic_number, payload.chromatic_distance),
        interval_label_generated=False,
        contextual_role_generated=False,
    )
    return ReenteredQualityObservation(
        reentry_observation=reentry_obs,
        quality_gamma=quality_gamma,
        quality=candidate,
        interval_label_generated=False,
        contextual_role_generated=False,
        target_generated=False,
        core_promoted=False,
        status="quality_candidate_observed_from_reentered_generic_not_labeled",
        generation_reason="reentered_generic_interval_and_chromatic_distance_read_by_Gamma_quality",
    )


def reenter_generic_to_quality(
    reentry_obs: ProcessingFrameReentryObservation,
    quality_reentry_gamma: GenericToQualityReentryGamma | None,
) -> GenericToQualityReentryObservation:
    generic_obs = reentry_obs.generic_observation
    if generic_obs is None or generic_obs.generic_interval is None:
        return GenericToQualityReentryObservation(
            reentry_obs,
            quality_reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            False,
            "no_reentered_generic_interval_candidate",
        )
    if quality_reentry_gamma is None:
        return GenericToQualityReentryObservation(
            reentry_obs,
            None,
            None,
            True,
            True,
            False,
            False,
            False,
            "reentered_generic_not_connected_to_quality_without_reentry_gamma",
        )

    quality_obs = generate_reentered_quality(reentry_obs, gamma_quality_fixture())
    quality = quality_obs.quality
    return GenericToQualityReentryObservation(
        reentry_observation=reentry_obs,
        quality_reentry_gamma=quality_reentry_gamma,
        quality_observation=quality_obs,
        same_generic_interval=(
            quality is not None
            and quality.source_generic_interval_label == generic_obs.generic_interval.label
        ),
        same_chromatic_distance=(
            quality is not None
            and quality.chromatic_distance == generic_obs.frame_payload_view.pitch_payload.chromatic_distance
        ),
        quality_generated=quality is not None,
        interval_label_generated=quality_obs.interval_label_generated,
        contextual_role_generated=quality_obs.contextual_role_generated,
        status="reentered_generic_connected_to_quality_not_interval_label",
    )


def compare_generic_to_quality_reentry() -> tuple[
    GenericToQualityReentryObservation, GenericToQualityReentryObservation
]:
    reentry_obs = generic_reentry_observation()
    return (
        reenter_generic_to_quality(reentry_obs, None),
        reenter_generic_to_quality(reentry_obs, quality_reentry_gamma_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_generic_to_quality_reentry()
    assert without_gamma.status == "reentered_generic_not_connected_to_quality_without_reentry_gamma"
    assert without_gamma.quality_generated is False
    assert with_gamma.status == "reentered_generic_connected_to_quality_not_interval_label"
    assert with_gamma.same_generic_interval is True
    assert with_gamma.same_chromatic_distance is True
    assert with_gamma.quality_generated is True
    assert with_gamma.interval_label_generated is False
    assert with_gamma.contextual_role_generated is False
    assert with_gamma.quality_observation is not None
    assert with_gamma.quality_observation.quality is not None
    assert with_gamma.quality_observation.quality.generic_number == 5
    assert with_gamma.quality_observation.quality.chromatic_distance == 7
    assert with_gamma.quality_observation.quality.quality_code == "P"
    assert with_gamma.quality_reentry_gamma is not None
    assert with_gamma.quality_reentry_gamma.generated_by_generic_reentry is False


if __name__ == "__main__":
    run_checks()
    print(compare_generic_to_quality_reentry()[1].status)
