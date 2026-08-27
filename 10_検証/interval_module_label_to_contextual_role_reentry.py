"""再入interval label candidateからcontextual role annotationへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_contextual_role_boundary import (
    ContextualRoleAnnotationCandidate,
    ContextualRoleGamma,
    IntervalContext,
    gamma_contextual_role_fixture,
    interval_context_fixture,
)
from interval_module_quality_to_label_reentry import (
    QualityToLabelReentryObservation,
    ReenteredIntervalLabelObservation,
    compare_quality_to_label_reentry,
)


@dataclass(frozen=True)
class LabelToContextualRoleReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_label_reentry: bool


@dataclass(frozen=True)
class ReenteredContextualRoleObservation:
    label_reentry_observation: ReenteredIntervalLabelObservation
    interval_context: IntervalContext | None
    gamma_contextual_role: ContextualRoleGamma | None
    contextual_role: ContextualRoleAnnotationCandidate | None
    target_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    annotation_reason: str | None


@dataclass(frozen=True)
class LabelToContextualRoleReentryObservation:
    quality_to_label_reentry: QualityToLabelReentryObservation
    contextual_role_reentry_gamma: LabelToContextualRoleReentryGamma | None
    contextual_role_observation: ReenteredContextualRoleObservation | None
    same_interval_label: bool
    same_external_context: bool
    contextual_role_generated: bool
    target_generated: bool
    harmonic_function_generated: bool
    status: str


def label_reentry_observation() -> QualityToLabelReentryObservation:
    return compare_quality_to_label_reentry()[1]


def contextual_role_reentry_gamma_fixture() -> LabelToContextualRoleReentryGamma:
    return LabelToContextualRoleReentryGamma(
        name="Gamma_reentered_interval_label_to_contextual_role_fixture",
        reads=("reentered_interval_label", "external_interval_context"),
        generated_by_label_reentry=False,
    )


def annotate_reentered_contextual_role(
    label_obs: ReenteredIntervalLabelObservation,
    interval_context: IntervalContext | None,
    gamma_contextual_role: ContextualRoleGamma | None,
) -> ReenteredContextualRoleObservation:
    interval_label = label_obs.interval_label
    if interval_label is None:
        return ReenteredContextualRoleObservation(
            label_obs,
            interval_context,
            gamma_contextual_role,
            None,
            False,
            False,
            False,
            "no_reentered_interval_label_candidate",
            None,
        )
    if interval_context is None:
        return ReenteredContextualRoleObservation(
            label_obs,
            None,
            gamma_contextual_role,
            None,
            False,
            False,
            False,
            "reentered_interval_label_not_contextualized_without_context",
            None,
        )
    if gamma_contextual_role is None:
        return ReenteredContextualRoleObservation(
            label_obs,
            interval_context,
            None,
            None,
            False,
            False,
            False,
            "reentered_interval_label_not_contextualized_without_gamma",
            None,
        )

    role = ContextualRoleAnnotationCandidate(
        label="tonic_to_fifth_span_role_candidate",
        source_interval_label=interval_label.label,
        key_context=interval_context.key_context,
        lower_degree=interval_context.lower_degree,
        upper_degree=interval_context.upper_degree,
        target_generated=False,
        harmonic_function_generated=False,
    )
    return ReenteredContextualRoleObservation(
        label_reentry_observation=label_obs,
        interval_context=interval_context,
        gamma_contextual_role=gamma_contextual_role,
        contextual_role=role,
        target_generated=False,
        harmonic_function_generated=False,
        core_promoted=False,
        status="contextual_role_candidate_observed_from_reentered_label_not_targeted",
        annotation_reason="reentered_interval_label_and_external_context_read_by_Gamma_contextual_role",
    )


def reenter_label_to_contextual_role(
    quality_to_label_obs: QualityToLabelReentryObservation,
    reentry_gamma: LabelToContextualRoleReentryGamma | None,
) -> LabelToContextualRoleReentryObservation:
    label_obs = quality_to_label_obs.interval_label_observation
    if label_obs is None or label_obs.interval_label is None:
        return LabelToContextualRoleReentryObservation(
            quality_to_label_obs,
            reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            False,
            "no_reentered_interval_label_candidate",
        )
    if reentry_gamma is None:
        return LabelToContextualRoleReentryObservation(
            quality_to_label_obs,
            None,
            None,
            True,
            False,
            False,
            False,
            False,
            "reentered_interval_label_not_connected_to_contextual_role_without_reentry_gamma",
        )

    context = interval_context_fixture()
    role_obs = annotate_reentered_contextual_role(
        label_obs, context, gamma_contextual_role_fixture()
    )
    role = role_obs.contextual_role
    return LabelToContextualRoleReentryObservation(
        quality_to_label_reentry=quality_to_label_obs,
        contextual_role_reentry_gamma=reentry_gamma,
        contextual_role_observation=role_obs,
        same_interval_label=(
            role is not None
            and role.source_interval_label == label_obs.interval_label.label
        ),
        same_external_context=role_obs.interval_context == context,
        contextual_role_generated=role is not None,
        target_generated=role_obs.target_generated,
        harmonic_function_generated=role_obs.harmonic_function_generated,
        status="reentered_interval_label_connected_to_contextual_role_not_target",
    )


def compare_label_to_contextual_role_reentry() -> tuple[
    LabelToContextualRoleReentryObservation,
    LabelToContextualRoleReentryObservation,
]:
    label_obs = label_reentry_observation()
    return (
        reenter_label_to_contextual_role(label_obs, None),
        reenter_label_to_contextual_role(
            label_obs, contextual_role_reentry_gamma_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_label_to_contextual_role_reentry()
    assert (
        without_gamma.status
        == "reentered_interval_label_not_connected_to_contextual_role_without_reentry_gamma"
    )
    assert without_gamma.contextual_role_generated is False
    assert (
        with_gamma.status
        == "reentered_interval_label_connected_to_contextual_role_not_target"
    )
    assert with_gamma.same_interval_label is True
    assert with_gamma.same_external_context is True
    assert with_gamma.contextual_role_generated is True
    assert with_gamma.target_generated is False
    assert with_gamma.harmonic_function_generated is False
    assert with_gamma.contextual_role_observation is not None
    assert with_gamma.contextual_role_observation.contextual_role is not None
    assert (
        with_gamma.contextual_role_observation.contextual_role.label
        == "tonic_to_fifth_span_role_candidate"
    )
    assert (
        with_gamma.contextual_role_observation.contextual_role.source_interval_label
        == "完全五度"
    )
    assert with_gamma.contextual_role_reentry_gamma is not None
    assert (
        with_gamma.contextual_role_reentry_gamma.generated_by_label_reentry
        is False
    )


if __name__ == "__main__":
    run_checks()
    print(compare_label_to_contextual_role_reentry()[1].status)
