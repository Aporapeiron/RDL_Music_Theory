"""再入selected consistencyからmodule state recordへ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_consistency_selection_reentry import (
    ReenteredConsistencySelectionObservation,
    compare_consistency_selection_reentry,
)
from interval_module_state_record_boundary import (
    IntervalModuleStateRecordBoundary,
    IntervalModuleStateRecordCandidate,
    IntervalModuleStateRecordGamma,
    gamma_state_record_fixture,
    record_boundary_fixture,
)


@dataclass(frozen=True)
class ReenteredStateRecordObservation:
    consistency_selection_observation: ReenteredConsistencySelectionObservation
    record_boundary: IntervalModuleStateRecordBoundary | None
    gamma_state_record: IntervalModuleStateRecordGamma | None
    state_record: IntervalModuleStateRecordCandidate | None
    confirmed_mb: bool
    core_promoted: bool
    status: str


def create_reentered_state_record(
    selection_obs: ReenteredConsistencySelectionObservation,
    boundary: IntervalModuleStateRecordBoundary | None,
    gamma: IntervalModuleStateRecordGamma | None,
) -> ReenteredStateRecordObservation:
    selected = selection_obs.selected_consistency
    if selected is None:
        return ReenteredStateRecordObservation(selection_obs, boundary, gamma, None, False, False, "no_reentered_selected_consistency")
    if boundary is None:
        return ReenteredStateRecordObservation(selection_obs, None, gamma, None, False, False, "reentered_state_record_not_created_without_boundary")
    if gamma is None:
        return ReenteredStateRecordObservation(selection_obs, boundary, None, None, False, False, "reentered_state_record_not_created_without_gamma")
    record = IntervalModuleStateRecordCandidate(
        "interval_module_context_harmony_state_record_candidate",
        selected.label,
        boundary.record_scope,
        False,
        False,
    )
    return ReenteredStateRecordObservation(selection_obs, boundary, gamma, record, False, False, "state_record_candidate_observed_from_reentered_consistency_not_confirmed")


def compare_state_record_reentry() -> tuple[
    ReenteredStateRecordObservation, ReenteredStateRecordObservation
]:
    selection = compare_consistency_selection_reentry()[1]
    boundary = record_boundary_fixture()
    return (
        create_reentered_state_record(selection, boundary, None),
        create_reentered_state_record(selection, boundary, gamma_state_record_fixture()),
    )


def run_checks() -> None:
    without_gamma, with_gamma = compare_state_record_reentry()
    assert without_gamma.state_record is None
    assert with_gamma.state_record is not None
    assert with_gamma.confirmed_mb is False
    assert with_gamma.core_promoted is False


if __name__ == "__main__":
    run_checks()
    print(compare_state_record_reentry()[1].status)
