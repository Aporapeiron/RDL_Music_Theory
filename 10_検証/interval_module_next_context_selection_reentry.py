"""再入next context candidate setからselected next contextへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_next_context_candidate_boundary import NextContextCandidate
from interval_module_next_context_candidate_reentry import (
    NextContextCandidateReentryObservation,
    ReenteredNextContextCandidateSetObservation,
    compare_next_context_candidate_reentry,
)
from interval_module_next_context_selection_boundary import (
    NextContextSelectionGamma,
    gamma_next_context_selection_fixture,
)


@dataclass(frozen=True)
class NextContextSelectionReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_next_context_candidate_reentry: bool


@dataclass(frozen=True)
class ReenteredNextContextSelectionObservation:
    candidate_set_observation: ReenteredNextContextCandidateSetObservation
    gamma_next_context_selection: NextContextSelectionGamma | None
    selected_next_context: NextContextCandidate | None
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    selection_reason: str | None


@dataclass(frozen=True)
class NextContextSelectionReentryObservation:
    next_context_candidate_reentry: NextContextCandidateReentryObservation
    selection_reentry_gamma: NextContextSelectionReentryGamma | None
    next_context_selection_observation: ReenteredNextContextSelectionObservation | None
    same_next_context_candidate_set: bool
    selected_next_context_observed: bool
    harmonic_function_generated: bool
    core_promoted: bool
    status: str


def next_context_candidate_reentry_observation() -> NextContextCandidateReentryObservation:
    return compare_next_context_candidate_reentry()[1]


def next_context_selection_reentry_gamma_fixture() -> NextContextSelectionReentryGamma:
    return NextContextSelectionReentryGamma(
        name="Gamma_reentered_next_context_candidates_to_selection_fixture",
        reads=("reentered_next_context_candidate_set", "selection_controller"),
        generated_by_next_context_candidate_reentry=False,
    )


def select_reentered_next_context(
    candidate_set: ReenteredNextContextCandidateSetObservation,
    gamma_next_context_selection: NextContextSelectionGamma | None,
) -> ReenteredNextContextSelectionObservation:
    if not candidate_set.next_context_candidates:
        return ReenteredNextContextSelectionObservation(
            candidate_set,
            gamma_next_context_selection,
            None,
            False,
            False,
            "no_reentered_next_context_candidate_set",
            None,
        )
    if gamma_next_context_selection is None:
        return ReenteredNextContextSelectionObservation(
            candidate_set,
            None,
            None,
            False,
            False,
            "reentered_next_context_candidate_set_unselected_without_controller",
            None,
        )

    matches = tuple(
        candidate
        for candidate in candidate_set.next_context_candidates
        if candidate.source == gamma_next_context_selection.selected_source
    )
    if len(matches) != 1:
        return ReenteredNextContextSelectionObservation(
            candidate_set,
            gamma_next_context_selection,
            None,
            False,
            False,
            "reentered_next_context_selection_ambiguous_or_absent",
            None,
        )

    return ReenteredNextContextSelectionObservation(
        candidate_set_observation=candidate_set,
        gamma_next_context_selection=gamma_next_context_selection,
        selected_next_context=matches[0],
        harmonic_function_generated=False,
        core_promoted=False,
        status="selected_next_context_observed_from_reentered_candidates_not_harmonized",
        selection_reason="reentered_next_context_candidate_matched_selected_source",
    )


def reenter_next_context_candidates_to_selection(
    next_context_candidate_reentry: NextContextCandidateReentryObservation,
    reentry_gamma: NextContextSelectionReentryGamma | None,
) -> NextContextSelectionReentryObservation:
    candidate_set = next_context_candidate_reentry.next_context_candidate_set_observation
    if candidate_set is None or not candidate_set.next_context_candidates:
        return NextContextSelectionReentryObservation(
            next_context_candidate_reentry,
            reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            "no_reentered_next_context_candidate_set",
        )
    if reentry_gamma is None:
        return NextContextSelectionReentryObservation(
            next_context_candidate_reentry,
            None,
            None,
            True,
            False,
            False,
            False,
            "reentered_next_context_candidates_not_connected_to_selection_without_reentry_gamma",
        )

    selection_obs = select_reentered_next_context(
        candidate_set, gamma_next_context_selection_fixture()
    )
    return NextContextSelectionReentryObservation(
        next_context_candidate_reentry=next_context_candidate_reentry,
        selection_reentry_gamma=reentry_gamma,
        next_context_selection_observation=selection_obs,
        same_next_context_candidate_set=(
            selection_obs.candidate_set_observation.next_context_candidates
            == candidate_set.next_context_candidates
        ),
        selected_next_context_observed=selection_obs.selected_next_context is not None,
        harmonic_function_generated=selection_obs.harmonic_function_generated,
        core_promoted=selection_obs.core_promoted,
        status="reentered_next_context_candidates_connected_to_selection_not_harmonic_function",
    )


def compare_next_context_selection_reentry() -> tuple[
    NextContextSelectionReentryObservation,
    NextContextSelectionReentryObservation,
]:
    candidate_reentry = next_context_candidate_reentry_observation()
    return (
        reenter_next_context_candidates_to_selection(candidate_reentry, None),
        reenter_next_context_candidates_to_selection(
            candidate_reentry, next_context_selection_reentry_gamma_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_next_context_selection_reentry()
    assert (
        without_gamma.status
        == "reentered_next_context_candidates_not_connected_to_selection_without_reentry_gamma"
    )
    assert without_gamma.selected_next_context_observed is False
    assert (
        with_gamma.status
        == "reentered_next_context_candidates_connected_to_selection_not_harmonic_function"
    )
    assert with_gamma.same_next_context_candidate_set is True
    assert with_gamma.selected_next_context_observed is True
    assert with_gamma.harmonic_function_generated is False
    assert with_gamma.core_promoted is False
    assert with_gamma.next_context_selection_observation is not None
    assert with_gamma.next_context_selection_observation.selected_next_context is not None
    assert (
        with_gamma.next_context_selection_observation.selected_next_context.label
        == "C major continuation"
    )


if __name__ == "__main__":
    run_checks()
    print(compare_next_context_selection_reentry()[1].status)
