"""再入context-harmony整合候補からselected consistencyへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_context_harmony_consistency_boundary import ContextHarmonyConsistencyCandidate
from interval_module_context_harmony_consistency_reentry import (
    ContextHarmonyConsistencyReentryObservation,
    ReenteredContextHarmonyConsistencyObservation,
    compare_context_harmony_consistency_reentry,
)
from interval_module_context_harmony_consistency_selection import (
    ContextHarmonyConsistencySelectionGamma,
    gamma_consistency_selection_fixture,
)


@dataclass(frozen=True)
class ConsistencySelectionReentryGamma:
    name: str
    reads: tuple[str, str]
    generated_by_consistency_reentry: bool


@dataclass(frozen=True)
class ReenteredConsistencySelectionObservation:
    consistency_observation: ReenteredContextHarmonyConsistencyObservation
    gamma_selection: ContextHarmonyConsistencySelectionGamma | None
    selected_consistency: ContextHarmonyConsistencyCandidate | None
    module_state_record_generated: bool
    core_promoted: bool
    status: str


def selection_reentry_gamma_fixture() -> ConsistencySelectionReentryGamma:
    return ConsistencySelectionReentryGamma(
        "Gamma_reentered_consistency_candidates_to_selection_fixture",
        ("reentered_consistency_candidates", "selection_controller"),
        False,
    )


def select_reentered_consistency(
    obs: ReenteredContextHarmonyConsistencyObservation,
    gamma: ContextHarmonyConsistencySelectionGamma | None,
) -> ReenteredConsistencySelectionObservation:
    if not obs.consistency_candidates:
        return ReenteredConsistencySelectionObservation(obs, gamma, None, False, False, "no_reentered_consistency_candidates")
    if gamma is None:
        return ReenteredConsistencySelectionObservation(obs, None, None, False, False, "reentered_consistency_candidates_unselected_without_controller")
    matches = tuple(c for c in obs.consistency_candidates if c.label == gamma.selected_label)
    selected = None
    status = "reentered_consistency_selection_ambiguous_or_absent"
    if len(matches) == 1:
        selected = ContextHarmonyConsistencyCandidate(
            matches[0].label,
            matches[0].selected_context_label,
            matches[0].harmonic_function_label,
            True,
            False,
        )
        status = "selected_consistency_observed_from_reentered_candidates_not_recorded"
    return ReenteredConsistencySelectionObservation(obs, gamma, selected, False, False, status)


def compare_consistency_selection_reentry() -> tuple[
    ReenteredConsistencySelectionObservation,
    ReenteredConsistencySelectionObservation,
]:
    consistency = compare_context_harmony_consistency_reentry()[1].consistency_observation
    assert consistency is not None
    return (
        select_reentered_consistency(consistency, None),
        select_reentered_consistency(consistency, gamma_consistency_selection_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_consistency_selection_reentry()
    assert without_gamma.selected_consistency is None
    assert with_gamma.selected_consistency is not None
    assert with_gamma.selected_consistency.selected is True
    assert with_gamma.module_state_record_generated is False


if __name__ == "__main__":
    run_checks()
    print(compare_consistency_selection_reentry()[1].status)
