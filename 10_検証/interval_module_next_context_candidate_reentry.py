"""再入concrete voice leadingからnext context candidate setへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_next_context_candidate_boundary import (
    NextContextCandidate,
    NextContextCandidateFilterGamma,
    NextContextInventory,
    gamma_next_context_filter_fixture,
    next_context_inventory_fixture,
)
from interval_module_voice_leading_realization_reentry import (
    ReenteredVoiceLeadingRealizationObservation,
    VoiceLeadingRealizationReentryObservation,
    compare_voice_leading_realization_reentry,
)


@dataclass(frozen=True)
class NextContextCandidateReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_realization_reentry: bool


@dataclass(frozen=True)
class ReenteredNextContextCandidateSetObservation:
    voice_leading_observation: ReenteredVoiceLeadingRealizationObservation
    next_context_inventory: NextContextInventory | None
    gamma_next_context_filter: NextContextCandidateFilterGamma | None
    next_context_candidates: tuple[NextContextCandidate, ...]
    selected_next_context: NextContextCandidate | None
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    filter_reason: str | None


@dataclass(frozen=True)
class NextContextCandidateReentryObservation:
    realization_reentry: VoiceLeadingRealizationReentryObservation
    next_context_reentry_gamma: NextContextCandidateReentryGamma | None
    next_context_candidate_set_observation: ReenteredNextContextCandidateSetObservation | None
    same_voice_leading_observation: bool
    same_next_context_inventory: bool
    candidate_set_observed: bool
    selected_next_context_generated: bool
    harmonic_function_generated: bool
    status: str


def realization_reentry_observation() -> VoiceLeadingRealizationReentryObservation:
    return compare_voice_leading_realization_reentry()[1]


def next_context_reentry_gamma_fixture() -> NextContextCandidateReentryGamma:
    return NextContextCandidateReentryGamma(
        name="Gamma_reentered_voice_leading_to_next_context_candidates_fixture",
        reads=("reentered_concrete_voice_leading", "external_next_context_inventory"),
        generated_by_realization_reentry=False,
    )


def observe_reentered_next_context_candidates(
    voice_leading_obs: ReenteredVoiceLeadingRealizationObservation,
    inventory: NextContextInventory | None,
    gamma_next_context_filter: NextContextCandidateFilterGamma | None,
) -> ReenteredNextContextCandidateSetObservation:
    if voice_leading_obs.concrete_voice_leading is None:
        return ReenteredNextContextCandidateSetObservation(
            voice_leading_obs,
            inventory,
            gamma_next_context_filter,
            (),
            None,
            False,
            False,
            "no_reentered_concrete_voice_leading_observation",
            None,
        )
    if inventory is None:
        return ReenteredNextContextCandidateSetObservation(
            voice_leading_obs,
            None,
            gamma_next_context_filter,
            (),
            None,
            False,
            False,
            "reentered_next_context_candidates_not_observed_without_inventory",
            None,
        )
    if gamma_next_context_filter is None:
        return ReenteredNextContextCandidateSetObservation(
            voice_leading_obs,
            inventory,
            None,
            (),
            None,
            False,
            False,
            "reentered_next_context_candidates_not_observed_without_filter_gamma",
            None,
        )

    filtered = tuple(
        candidate
        for candidate in inventory.candidates
        if candidate.source in gamma_next_context_filter.accepted_sources
    )
    return ReenteredNextContextCandidateSetObservation(
        voice_leading_observation=voice_leading_obs,
        next_context_inventory=inventory,
        gamma_next_context_filter=gamma_next_context_filter,
        next_context_candidates=filtered,
        selected_next_context=None,
        harmonic_function_generated=False,
        core_promoted=False,
        status="next_context_candidate_set_observed_from_reentered_voice_leading_unselected",
        filter_reason="external_inventory_filtered_by_Gamma_next_context_candidate_filter",
    )


def reenter_voice_leading_to_next_context_candidates(
    realization_reentry: VoiceLeadingRealizationReentryObservation,
    reentry_gamma: NextContextCandidateReentryGamma | None,
) -> NextContextCandidateReentryObservation:
    realization_obs = realization_reentry.realization_observation
    if realization_obs is None or realization_obs.concrete_voice_leading is None:
        return NextContextCandidateReentryObservation(
            realization_reentry,
            reentry_gamma,
            None,
            False,
            False,
            False,
            False,
            False,
            "no_reentered_concrete_voice_leading_observation",
        )
    if reentry_gamma is None:
        return NextContextCandidateReentryObservation(
            realization_reentry,
            None,
            None,
            True,
            False,
            False,
            False,
            False,
            "reentered_voice_leading_not_connected_to_next_context_without_reentry_gamma",
        )

    inventory = next_context_inventory_fixture()
    candidate_obs = observe_reentered_next_context_candidates(
        realization_obs, inventory, gamma_next_context_filter_fixture()
    )
    return NextContextCandidateReentryObservation(
        realization_reentry=realization_reentry,
        next_context_reentry_gamma=reentry_gamma,
        next_context_candidate_set_observation=candidate_obs,
        same_voice_leading_observation=(
            candidate_obs.voice_leading_observation.concrete_voice_leading
            == realization_obs.concrete_voice_leading
        ),
        same_next_context_inventory=candidate_obs.next_context_inventory == inventory,
        candidate_set_observed=bool(candidate_obs.next_context_candidates),
        selected_next_context_generated=candidate_obs.selected_next_context is not None,
        harmonic_function_generated=candidate_obs.harmonic_function_generated,
        status="reentered_voice_leading_connected_to_next_context_candidates_unselected",
    )


def compare_next_context_candidate_reentry() -> tuple[
    NextContextCandidateReentryObservation,
    NextContextCandidateReentryObservation,
]:
    realization = realization_reentry_observation()
    return (
        reenter_voice_leading_to_next_context_candidates(realization, None),
        reenter_voice_leading_to_next_context_candidates(
            realization, next_context_reentry_gamma_fixture()
        ),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_next_context_candidate_reentry()
    assert (
        without_gamma.status
        == "reentered_voice_leading_not_connected_to_next_context_without_reentry_gamma"
    )
    assert without_gamma.candidate_set_observed is False
    assert (
        with_gamma.status
        == "reentered_voice_leading_connected_to_next_context_candidates_unselected"
    )
    assert with_gamma.same_voice_leading_observation is True
    assert with_gamma.same_next_context_inventory is True
    assert with_gamma.candidate_set_observed is True
    assert with_gamma.selected_next_context_generated is False
    assert with_gamma.harmonic_function_generated is False
    assert with_gamma.next_context_candidate_set_observation is not None
    assert tuple(
        candidate.label
        for candidate in with_gamma.next_context_candidate_set_observation.next_context_candidates
    ) == ("C major continuation", "G major reinterpretation")


if __name__ == "__main__":
    run_checks()
    print(compare_next_context_candidate_reentry()[1].status)
