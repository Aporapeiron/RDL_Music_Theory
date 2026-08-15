"""selected next ξ候補とhandoff summary候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_next_xi_selection_boundary import (
    NextXiSelectionObservation,
    compare_next_xi_selection,
)


@dataclass(frozen=True)
class HandoffRecordBoundary:
    name: str
    generated_by_selected_xi: bool


@dataclass(frozen=True)
class HandoffSummaryCandidate:
    label: str
    source_selected_xi_label: str
    summarizes_range: str
    next_work_started: bool


@dataclass(frozen=True)
class HandoffSummaryObservation:
    xi_selection_observation: NextXiSelectionObservation
    handoff_boundary: HandoffRecordBoundary | None
    handoff_summary: HandoffSummaryCandidate | None
    status: str


def xi_selection_observation() -> NextXiSelectionObservation:
    return compare_next_xi_selection()[1]


def handoff_boundary_fixture() -> HandoffRecordBoundary:
    return HandoffRecordBoundary(
        name="interval_handoff_record_boundary_fixture",
        generated_by_selected_xi=False,
    )


def create_handoff_summary(
    xi_selection: NextXiSelectionObservation,
    boundary: HandoffRecordBoundary | None,
) -> HandoffSummaryObservation:
    selected = xi_selection.selected_xi
    if selected is None:
        return HandoffSummaryObservation(xi_selection, boundary, None, "no_selected_next_xi")
    if boundary is None:
        return HandoffSummaryObservation(
            xi_selection, None, None, "handoff_summary_not_created_without_boundary"
        )
    summary = HandoffSummaryCandidate(
        label="interval_101_115_handoff_summary_candidate",
        source_selected_xi_label=selected.label,
        summarizes_range="101-115",
        next_work_started=False,
    )
    return HandoffSummaryObservation(
        xi_selection, boundary, summary, "handoff_summary_candidate_observed_not_next_work"
    )


def compare_handoff_summary() -> tuple[
    HandoffSummaryObservation, HandoffSummaryObservation
]:
    selection = xi_selection_observation()
    return (
        create_handoff_summary(selection, None),
        create_handoff_summary(selection, handoff_boundary_fixture()),
    )


def run_checks() -> None:
    without_boundary, with_boundary = compare_handoff_summary()
    assert without_boundary.status == "handoff_summary_not_created_without_boundary"
    assert with_boundary.status == "handoff_summary_candidate_observed_not_next_work"
    assert with_boundary.handoff_summary is not None
    assert with_boundary.handoff_summary.summarizes_range == "101-115"
    assert with_boundary.handoff_summary.next_work_started is False
    assert with_boundary.handoff_boundary is not None
    assert with_boundary.handoff_boundary.generated_by_selected_xi is False


if __name__ == "__main__":
    run_checks()
    print(compare_handoff_summary()[1].status)
