"""音程Module interval labelとcontextual role注釈境界の最小検証。"""

from dataclasses import dataclass

from interval_module_label_boundary import (
    IntervalLabelObservation,
    compare_interval_label_generation,
)


@dataclass(frozen=True)
class IntervalContext:
    name: str
    key_context: str
    lower_degree: int
    upper_degree: int
    role_scope: str
    generated_by_interval_label: bool


@dataclass(frozen=True)
class ContextualRoleGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class ContextualRoleAnnotationCandidate:
    label: str
    source_interval_label: str
    key_context: str
    lower_degree: int
    upper_degree: int
    target_generated: bool
    harmonic_function_generated: bool


@dataclass(frozen=True)
class ContextualRoleObservation:
    interval_label_observation: IntervalLabelObservation
    interval_context: IntervalContext | None
    gamma_contextual_role: ContextualRoleGamma | None
    contextual_role: ContextualRoleAnnotationCandidate | None
    target_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    annotation_reason: str | None


@dataclass(frozen=True)
class ContextualRoleComparison:
    without_gamma: ContextualRoleObservation
    with_gamma: ContextualRoleObservation
    same_interval_label: bool
    same_interval_context: bool
    same_gamma_contextual_role: bool
    contextual_role_observed: bool
    target_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool


def interval_label_observation() -> IntervalLabelObservation:
    return compare_interval_label_generation().with_gamma


def interval_context_fixture() -> IntervalContext:
    return IntervalContext(
        name="C_major_C_to_G_context_fixture",
        key_context="C major",
        lower_degree=1,
        upper_degree=5,
        role_scope="local_pitch_relation_role",
        generated_by_interval_label=False,
    )


def gamma_contextual_role_fixture() -> ContextualRoleGamma:
    return ContextualRoleGamma(
        name="Gamma_contextual_role_fixture",
        reads=("interval_label", "external_interval_context"),
        rule_scope="fixture_limited_not_target_or_harmonic_function_rule",
    )


def annotate_contextual_role(
    interval_label_observation: IntervalLabelObservation,
    interval_context: IntervalContext | None,
    gamma_contextual_role: ContextualRoleGamma | None,
) -> ContextualRoleObservation:
    interval_label = interval_label_observation.interval_label
    if interval_label is None:
        return ContextualRoleObservation(
            interval_label_observation=interval_label_observation,
            interval_context=interval_context,
            gamma_contextual_role=gamma_contextual_role,
            contextual_role=None,
            target_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="no_interval_label_candidate",
            annotation_reason=None,
        )
    if interval_context is None:
        return ContextualRoleObservation(
            interval_label_observation=interval_label_observation,
            interval_context=None,
            gamma_contextual_role=gamma_contextual_role,
            contextual_role=None,
            target_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="interval_label_not_contextualized_without_context",
            annotation_reason=None,
        )
    if gamma_contextual_role is None:
        return ContextualRoleObservation(
            interval_label_observation=interval_label_observation,
            interval_context=interval_context,
            gamma_contextual_role=None,
            contextual_role=None,
            target_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="interval_label_not_contextualized_without_gamma",
            annotation_reason=None,
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
    return ContextualRoleObservation(
        interval_label_observation=interval_label_observation,
        interval_context=interval_context,
        gamma_contextual_role=gamma_contextual_role,
        contextual_role=role,
        target_generated=False,
        harmonic_function_generated=False,
        core_promoted=False,
        status="contextual_role_candidate_observed_not_targeted",
        annotation_reason="interval_label_and_external_context_read_by_Gamma_contextual_role",
    )


def compare_contextual_role_annotation() -> ContextualRoleComparison:
    label_observation = interval_label_observation()
    context = interval_context_fixture()
    without_gamma = annotate_contextual_role(label_observation, context, None)
    with_gamma = annotate_contextual_role(
        label_observation, context, gamma_contextual_role_fixture()
    )
    return ContextualRoleComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_interval_label=(
            without_gamma.interval_label_observation.interval_label
            == with_gamma.interval_label_observation.interval_label
        ),
        same_interval_context=without_gamma.interval_context == with_gamma.interval_context,
        same_gamma_contextual_role=(
            without_gamma.gamma_contextual_role == with_gamma.gamma_contextual_role
        ),
        contextual_role_observed=(
            with_gamma.status == "contextual_role_candidate_observed_not_targeted"
        ),
        target_generated=with_gamma.target_generated,
        harmonic_function_generated=with_gamma.harmonic_function_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_contextual_role_annotation()
    assert comparison.same_interval_label is True
    assert comparison.same_interval_context is True
    assert comparison.same_gamma_contextual_role is False
    assert comparison.contextual_role_observed is True
    assert comparison.target_generated is False
    assert comparison.harmonic_function_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_gamma.status
        == "interval_label_not_contextualized_without_gamma"
    )
    assert comparison.without_gamma.contextual_role is None
    assert comparison.with_gamma.contextual_role is not None
    assert (
        comparison.with_gamma.contextual_role.label
        == "tonic_to_fifth_span_role_candidate"
    )
    assert comparison.with_gamma.contextual_role.key_context == "C major"
    assert comparison.with_gamma.contextual_role.lower_degree == 1
    assert comparison.with_gamma.contextual_role.upper_degree == 5
    assert comparison.with_gamma.interval_context is not None
    assert comparison.with_gamma.interval_context.generated_by_interval_label is False


def main() -> None:
    run_checks()
    comparison = compare_contextual_role_annotation()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  interval label candidate")
    print("  + external interval context")
    print("  + Gamma_contextual_role_fixture")
    print("  -> contextual role annotation candidate")
    print("  -> target and harmonic function remain None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_interval_label={comparison.same_interval_label}")
    print(f"  same_interval_context={comparison.same_interval_context}")
    print(f"  same_gamma_contextual_role={comparison.same_gamma_contextual_role}")
    print(f"  contextual_role_observed={comparison.contextual_role_observed}")
    print(
        "  contextual_role="
        + (with_gamma.contextual_role.label if with_gamma.contextual_role else "None")
    )
    print(f"  target_generated={comparison.target_generated}")
    print(f"  harmonic_function_generated={comparison.harmonic_function_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
