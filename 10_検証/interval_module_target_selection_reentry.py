"""再入target candidate setからselected targetへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_contextual_role_to_target_reentry import (
    ContextualRoleToTargetReentryObservation,
    ReenteredTargetCandidateSetObservation,
    compare_contextual_role_to_target_reentry,
)
from interval_module_target_candidate_boundary import IntervalTargetCandidate
from interval_module_target_selection_boundary import (
    IntervalTargetSelectionGamma,
    gamma_target_selection_fixture,
)


@dataclass(frozen=True)
class TargetSelectionReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_target_candidate_reentry: bool


@dataclass(frozen=True)
class ReenteredTargetSelectionObservation:
    target_candidate_set_observation: ReenteredTargetCandidateSetObservation
    gamma_target_selection: IntervalTargetSelectionGamma | None
    selected_target: IntervalTargetCandidate | None
    voice_leading_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    selection_reason: str | None


@dataclass(frozen=True)
class TargetSelectionReentryObservation:
    target_candidate_reentry: ContextualRoleToTargetReentryObservation
    selection_reentry_gamma: TargetSelectionReentryGamma | None
    target_selection_observation: ReenteredTargetSelectionObservation | None
    same_target_candidate_set: bool
    selected_target_observed: bool
    voice_leading_generated: bool
    harmonic_function_generated: bool
    status: str


def target_candidate_reentry_observation() -> ContextualRoleToTargetReentryObservation:
    return compare_contextual_role_to_target_reentry()[1]


def selection_reentry_gamma_fixture() -> TargetSelectionReentryGamma:
    return TargetSelectionReentryGamma(
        name="Gamma_reentered_target_candidates_to_selection_fixture",
        reads=("reentered_target_candidate_set", "selection_controller"),
        generated_by_target_candidate_reentry=False,
    )


def select_reentered_interval_target(
    target_set: ReenteredTargetCandidateSetObservation,
    gamma_target_selection: IntervalTargetSelectionGamma | None,
) -> ReenteredTargetSelectionObservation:
    if not target_set.target_candidates:
        return ReenteredTargetSelectionObservation(
            target_set,
            gamma_target_selection,
            None,
            False,
            False,
            False,
            "no_reentered_target_candidate_set",
            None,
        )
    if gamma_target_selection is None:
        return ReenteredTargetSelectionObservation(
            target_set,
            None,
            None,
            False,
            False,
            False,
            "reentered_target_candidate_set_unselected_without_controller",
            None,
        )

    matches = tuple(
        candidate
        for candidate in target_set.target_candidates
        if candidate.policy_tag == gamma_target_selection.selected_policy_tag
    )
    if len(matches) != 1:
        return ReenteredTargetSelectionObservation(
            target_set,
            gamma_target_selection,
            None,
            False,
            False,
            False,
            "reentered_target_selection_ambiguous_or_absent",
            None,
        )

    return ReenteredTargetSelectionObservation(
        target_candidate_set_observation=target_set,
        gamma_target_selection=gamma_target_selection,
        selected_target=matches[0],
        voice_leading_generated=False,
        harmonic_function_generated=False,
        core_promoted=False,
        status="selected_target_observed_from_reentered_candidate_set_not_realized",
        selection_reason="reentered_target_candidate_matched_selected_policy_tag",
    )


def reenter_target_candidates_to_selection(
    target_candidate_reentry: ContextualRoleToTargetReentryObservation,
    reentry_gamma: TargetSelectionReentryGamma | None,
) -> TargetSelectionReentryObservation:
    target_set = target_candidate_reentry.target_candidate_set_observation
    if target_set is None or not target_set.target_candidates:
        return TargetSelectionReentryObservation(
            target_candidate_reentry,
            reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            "no_reentered_target_candidate_set",
        )
    if reentry_gamma is None:
        return TargetSelectionReentryObservation(
            target_candidate_reentry,
            None,
            None,
            True,
            False,
            False,
            False,
            "reentered_target_candidates_not_connected_to_selection_without_reentry_gamma",
        )

    selection_obs = select_reentered_interval_target(
        target_set, gamma_target_selection_fixture()
    )
    return TargetSelectionReentryObservation(
        target_candidate_reentry=target_candidate_reentry,
        selection_reentry_gamma=reentry_gamma,
        target_selection_observation=selection_obs,
        same_target_candidate_set=(
            selection_obs.target_candidate_set_observation.target_candidates
            == target_set.target_candidates
        ),
        selected_target_observed=selection_obs.selected_target is not None,
        voice_leading_generated=selection_obs.voice_leading_generated,
        harmonic_function_generated=selection_obs.harmonic_function_generated,
        status="reentered_target_candidates_connected_to_selection_not_voice_leading",
    )


def compare_target_selection_reentry() -> tuple[
    TargetSelectionReentryObservation,
    TargetSelectionReentryObservation,
]:
    target_candidate_reentry = target_candidate_reentry_observation()
    return (
        reenter_target_candidates_to_selection(target_candidate_reentry, None),
        reenter_target_candidates_to_selection(
            target_candidate_reentry, selection_reentry_gamma_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_target_selection_reentry()
    assert (
        without_gamma.status
        == "reentered_target_candidates_not_connected_to_selection_without_reentry_gamma"
    )
    assert without_gamma.selected_target_observed is False
    assert (
        with_gamma.status
        == "reentered_target_candidates_connected_to_selection_not_voice_leading"
    )
    assert with_gamma.same_target_candidate_set is True
    assert with_gamma.selected_target_observed is True
    assert with_gamma.voice_leading_generated is False
    assert with_gamma.harmonic_function_generated is False
    assert with_gamma.target_selection_observation is not None
    assert with_gamma.target_selection_observation.selected_target is not None
    assert with_gamma.target_selection_observation.selected_target.label == "maintain_C_G_span"
    assert with_gamma.target_selection_observation.selected_target.policy_tag == "preserve_span"
    assert with_gamma.selection_reentry_gamma is not None
    assert (
        with_gamma.selection_reentry_gamma.generated_by_target_candidate_reentry
        is False
    )


if __name__ == "__main__":
    run_checks()
    print(compare_target_selection_reentry()[1].status)
