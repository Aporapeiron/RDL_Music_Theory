"""音程Module contextual roleとtarget候補集合境界の最小検証。"""

from dataclasses import dataclass

from interval_module_contextual_role_boundary import (
    ContextualRoleObservation,
    compare_contextual_role_annotation,
)


@dataclass(frozen=True)
class IntervalTargetCandidate:
    label: str
    source: str
    policy_tag: str
    generated_by_contextual_role: bool


@dataclass(frozen=True)
class IntervalTargetInventory:
    name: str
    candidates: tuple[IntervalTargetCandidate, ...]
    generated_by_contextual_role: bool


@dataclass(frozen=True)
class IntervalTargetCandidateFilterGamma:
    name: str
    reads: tuple[str, str]
    accepted_policy_tags: tuple[str, ...]
    rule_scope: str


@dataclass(frozen=True)
class IntervalTargetCandidateSetObservation:
    contextual_role_observation: ContextualRoleObservation
    target_inventory: IntervalTargetInventory | None
    gamma_target_filter: IntervalTargetCandidateFilterGamma | None
    target_candidates: tuple[IntervalTargetCandidate, ...]
    selected_target: IntervalTargetCandidate | None
    voice_leading_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    filter_reason: str | None


@dataclass(frozen=True)
class IntervalTargetCandidateSetComparison:
    without_gamma: IntervalTargetCandidateSetObservation
    with_gamma: IntervalTargetCandidateSetObservation
    same_contextual_role: bool
    same_target_inventory: bool
    same_gamma_target_filter: bool
    target_candidate_set_observed: bool
    selected_target_generated: bool
    voice_leading_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool


def contextual_role_observation() -> ContextualRoleObservation:
    return compare_contextual_role_annotation().with_gamma


def target_inventory_fixture() -> IntervalTargetInventory:
    return IntervalTargetInventory(
        name="external_interval_target_inventory_fixture",
        candidates=(
            IntervalTargetCandidate(
                label="maintain_C_G_span",
                source="external_fixture",
                policy_tag="preserve_span",
                generated_by_contextual_role=False,
            ),
            IntervalTargetCandidate(
                label="collapse_to_C_unison",
                source="external_fixture",
                policy_tag="preserve_tonic",
                generated_by_contextual_role=False,
            ),
            IntervalTargetCandidate(
                label="move_to_E_C_contextual_resolution",
                source="external_fixture",
                policy_tag="contextual_resolution",
                generated_by_contextual_role=False,
            ),
        ),
        generated_by_contextual_role=False,
    )


def gamma_target_filter_fixture() -> IntervalTargetCandidateFilterGamma:
    return IntervalTargetCandidateFilterGamma(
        name="Gamma_interval_target_candidate_filter_fixture",
        reads=("contextual_role", "external_target_inventory"),
        accepted_policy_tags=("preserve_span", "preserve_tonic"),
        rule_scope="fixture_limited_not_target_selection_rule",
    )


def observe_target_candidate_set(
    contextual_role: ContextualRoleObservation,
    target_inventory: IntervalTargetInventory | None,
    gamma_target_filter: IntervalTargetCandidateFilterGamma | None,
) -> IntervalTargetCandidateSetObservation:
    if contextual_role.contextual_role is None:
        return IntervalTargetCandidateSetObservation(
            contextual_role_observation=contextual_role,
            target_inventory=target_inventory,
            gamma_target_filter=gamma_target_filter,
            target_candidates=(),
            selected_target=None,
            voice_leading_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="no_contextual_role_candidate",
            filter_reason=None,
        )
    if target_inventory is None:
        return IntervalTargetCandidateSetObservation(
            contextual_role_observation=contextual_role,
            target_inventory=None,
            gamma_target_filter=gamma_target_filter,
            target_candidates=(),
            selected_target=None,
            voice_leading_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="target_candidate_set_not_observed_without_inventory",
            filter_reason=None,
        )
    if gamma_target_filter is None:
        return IntervalTargetCandidateSetObservation(
            contextual_role_observation=contextual_role,
            target_inventory=target_inventory,
            gamma_target_filter=None,
            target_candidates=(),
            selected_target=None,
            voice_leading_generated=False,
            harmonic_function_generated=False,
            core_promoted=False,
            status="target_candidate_set_not_observed_without_filter_gamma",
            filter_reason=None,
        )

    filtered = tuple(
        candidate
        for candidate in target_inventory.candidates
        if candidate.policy_tag in gamma_target_filter.accepted_policy_tags
    )
    return IntervalTargetCandidateSetObservation(
        contextual_role_observation=contextual_role,
        target_inventory=target_inventory,
        gamma_target_filter=gamma_target_filter,
        target_candidates=filtered,
        selected_target=None,
        voice_leading_generated=False,
        harmonic_function_generated=False,
        core_promoted=False,
        status="target_candidate_set_observed_unselected",
        filter_reason="external_inventory_filtered_by_Gamma_interval_target_candidate_filter",
    )


def compare_target_candidate_set_observation() -> IntervalTargetCandidateSetComparison:
    role = contextual_role_observation()
    inventory = target_inventory_fixture()
    without_gamma = observe_target_candidate_set(role, inventory, None)
    with_gamma = observe_target_candidate_set(
        role, inventory, gamma_target_filter_fixture()
    )
    return IntervalTargetCandidateSetComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_contextual_role=(
            without_gamma.contextual_role_observation.contextual_role
            == with_gamma.contextual_role_observation.contextual_role
        ),
        same_target_inventory=without_gamma.target_inventory == with_gamma.target_inventory,
        same_gamma_target_filter=(
            without_gamma.gamma_target_filter == with_gamma.gamma_target_filter
        ),
        target_candidate_set_observed=(
            with_gamma.status == "target_candidate_set_observed_unselected"
        ),
        selected_target_generated=with_gamma.selected_target is not None,
        voice_leading_generated=with_gamma.voice_leading_generated,
        harmonic_function_generated=with_gamma.harmonic_function_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_target_candidate_set_observation()
    assert comparison.same_contextual_role is True
    assert comparison.same_target_inventory is True
    assert comparison.same_gamma_target_filter is False
    assert comparison.target_candidate_set_observed is True
    assert comparison.selected_target_generated is False
    assert comparison.voice_leading_generated is False
    assert comparison.harmonic_function_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_gamma.status
        == "target_candidate_set_not_observed_without_filter_gamma"
    )
    assert comparison.without_gamma.target_candidates == ()
    assert comparison.with_gamma.target_inventory is not None
    assert comparison.with_gamma.target_inventory.generated_by_contextual_role is False
    assert tuple(candidate.label for candidate in comparison.with_gamma.target_candidates) == (
        "maintain_C_G_span",
        "collapse_to_C_unison",
    )
    assert all(
        candidate.generated_by_contextual_role is False
        for candidate in comparison.with_gamma.target_candidates
    )


def main() -> None:
    run_checks()
    comparison = compare_target_candidate_set_observation()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  contextual role annotation candidate")
    print("  + external target candidate inventory")
    print("  + Gamma_interval_target_candidate_filter_fixture")
    print("  -> target candidate set observed")
    print("  -> selected target remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_contextual_role={comparison.same_contextual_role}")
    print(f"  same_target_inventory={comparison.same_target_inventory}")
    print(f"  same_gamma_target_filter={comparison.same_gamma_target_filter}")
    print(f"  target_candidate_set_observed={comparison.target_candidate_set_observed}")
    print(
        "  target_candidates="
        + ",".join(candidate.label for candidate in with_gamma.target_candidates)
    )
    print(f"  selected_target_generated={comparison.selected_target_generated}")
    print(f"  voice_leading_generated={comparison.voice_leading_generated}")
    print(f"  harmonic_function_generated={comparison.harmonic_function_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
