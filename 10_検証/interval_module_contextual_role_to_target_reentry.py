"""再入contextual role annotationからtarget candidate setへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_label_to_contextual_role_reentry import (
    LabelToContextualRoleReentryObservation,
    ReenteredContextualRoleObservation,
    compare_label_to_contextual_role_reentry,
)
from interval_module_target_candidate_boundary import (
    IntervalTargetCandidate,
    IntervalTargetCandidateFilterGamma,
    IntervalTargetInventory,
    gamma_target_filter_fixture,
    target_inventory_fixture,
)


@dataclass(frozen=True)
class ContextualRoleToTargetReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_contextual_role_reentry: bool


@dataclass(frozen=True)
class ReenteredTargetCandidateSetObservation:
    contextual_role_reentry_observation: ReenteredContextualRoleObservation
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
class ContextualRoleToTargetReentryObservation:
    contextual_role_reentry: LabelToContextualRoleReentryObservation
    target_reentry_gamma: ContextualRoleToTargetReentryGamma | None
    target_candidate_set_observation: ReenteredTargetCandidateSetObservation | None
    same_contextual_role: bool
    same_target_inventory: bool
    target_candidate_set_observed: bool
    selected_target_generated: bool
    voice_leading_generated: bool
    harmonic_function_generated: bool
    status: str


def contextual_role_reentry_observation() -> LabelToContextualRoleReentryObservation:
    return compare_label_to_contextual_role_reentry()[1]


def target_reentry_gamma_fixture() -> ContextualRoleToTargetReentryGamma:
    return ContextualRoleToTargetReentryGamma(
        name="Gamma_reentered_contextual_role_to_target_candidates_fixture",
        reads=("reentered_contextual_role", "external_target_inventory"),
        generated_by_contextual_role_reentry=False,
    )


def observe_reentered_target_candidate_set(
    contextual_role_obs: ReenteredContextualRoleObservation,
    target_inventory: IntervalTargetInventory | None,
    gamma_target_filter: IntervalTargetCandidateFilterGamma | None,
) -> ReenteredTargetCandidateSetObservation:
    contextual_role = contextual_role_obs.contextual_role
    if contextual_role is None:
        return ReenteredTargetCandidateSetObservation(
            contextual_role_obs,
            target_inventory,
            gamma_target_filter,
            (),
            None,
            False,
            False,
            False,
            "no_reentered_contextual_role_candidate",
            None,
        )
    if target_inventory is None:
        return ReenteredTargetCandidateSetObservation(
            contextual_role_obs,
            None,
            gamma_target_filter,
            (),
            None,
            False,
            False,
            False,
            "reentered_target_candidate_set_not_observed_without_inventory",
            None,
        )
    if gamma_target_filter is None:
        return ReenteredTargetCandidateSetObservation(
            contextual_role_obs,
            target_inventory,
            None,
            (),
            None,
            False,
            False,
            False,
            "reentered_target_candidate_set_not_observed_without_filter_gamma",
            None,
        )

    filtered = tuple(
        candidate
        for candidate in target_inventory.candidates
        if candidate.policy_tag in gamma_target_filter.accepted_policy_tags
    )
    return ReenteredTargetCandidateSetObservation(
        contextual_role_reentry_observation=contextual_role_obs,
        target_inventory=target_inventory,
        gamma_target_filter=gamma_target_filter,
        target_candidates=filtered,
        selected_target=None,
        voice_leading_generated=False,
        harmonic_function_generated=False,
        core_promoted=False,
        status="target_candidate_set_observed_from_reentered_contextual_role_unselected",
        filter_reason="external_inventory_filtered_by_Gamma_interval_target_candidate_filter",
    )


def reenter_contextual_role_to_target_candidates(
    contextual_role_reentry: LabelToContextualRoleReentryObservation,
    reentry_gamma: ContextualRoleToTargetReentryGamma | None,
) -> ContextualRoleToTargetReentryObservation:
    role_obs = contextual_role_reentry.contextual_role_observation
    if role_obs is None or role_obs.contextual_role is None:
        return ContextualRoleToTargetReentryObservation(
            contextual_role_reentry,
            reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            False,
            False,
            "no_reentered_contextual_role_candidate",
        )
    if reentry_gamma is None:
        return ContextualRoleToTargetReentryObservation(
            contextual_role_reentry,
            None,
            None,
            True,
            False,
            False,
            False,
            False,
            False,
            "reentered_contextual_role_not_connected_to_target_candidates_without_reentry_gamma",
        )

    inventory = target_inventory_fixture()
    target_obs = observe_reentered_target_candidate_set(
        role_obs, inventory, gamma_target_filter_fixture()
    )
    return ContextualRoleToTargetReentryObservation(
        contextual_role_reentry=contextual_role_reentry,
        target_reentry_gamma=reentry_gamma,
        target_candidate_set_observation=target_obs,
        same_contextual_role=(
            target_obs.contextual_role_reentry_observation.contextual_role
            == role_obs.contextual_role
        ),
        same_target_inventory=target_obs.target_inventory == inventory,
        target_candidate_set_observed=bool(target_obs.target_candidates),
        selected_target_generated=target_obs.selected_target is not None,
        voice_leading_generated=target_obs.voice_leading_generated,
        harmonic_function_generated=target_obs.harmonic_function_generated,
        status="reentered_contextual_role_connected_to_target_candidates_unselected",
    )


def compare_contextual_role_to_target_reentry() -> tuple[
    ContextualRoleToTargetReentryObservation,
    ContextualRoleToTargetReentryObservation,
]:
    role_obs = contextual_role_reentry_observation()
    return (
        reenter_contextual_role_to_target_candidates(role_obs, None),
        reenter_contextual_role_to_target_candidates(
            role_obs, target_reentry_gamma_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_contextual_role_to_target_reentry()
    assert (
        without_gamma.status
        == "reentered_contextual_role_not_connected_to_target_candidates_without_reentry_gamma"
    )
    assert without_gamma.target_candidate_set_observed is False
    assert (
        with_gamma.status
        == "reentered_contextual_role_connected_to_target_candidates_unselected"
    )
    assert with_gamma.same_contextual_role is True
    assert with_gamma.same_target_inventory is True
    assert with_gamma.target_candidate_set_observed is True
    assert with_gamma.selected_target_generated is False
    assert with_gamma.voice_leading_generated is False
    assert with_gamma.harmonic_function_generated is False
    assert with_gamma.target_candidate_set_observation is not None
    assert tuple(
        candidate.label
        for candidate in with_gamma.target_candidate_set_observation.target_candidates
    ) == (
        "maintain_C_G_span",
        "collapse_to_C_unison",
    )
    assert all(
        candidate.generated_by_contextual_role is False
        for candidate in with_gamma.target_candidate_set_observation.target_candidates
    )
    assert with_gamma.target_reentry_gamma is not None
    assert (
        with_gamma.target_reentry_gamma.generated_by_contextual_role_reentry
        is False
    )


if __name__ == "__main__":
    run_checks()
    print(compare_contextual_role_to_target_reentry()[1].status)
