"""再入selected next xi候補とhandoff summary候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_handoff_summary_boundary import HandoffRecordBoundary, HandoffSummaryCandidate, handoff_boundary_fixture
from interval_module_next_xi_selection_reentry import ReenteredNextXiSelectionObservation, compare_next_xi_selection_reentry


@dataclass(frozen=True)
class ReenteredHandoffSummaryObservation:
    xi_selection_observation: ReenteredNextXiSelectionObservation
    handoff_boundary: HandoffRecordBoundary | None
    handoff_summary: HandoffSummaryCandidate | None
    status: str


def create_reentered_handoff_summary(selection: ReenteredNextXiSelectionObservation, boundary: HandoffRecordBoundary | None) -> ReenteredHandoffSummaryObservation:
    selected = selection.selected_xi
    if selected is None:
        return ReenteredHandoffSummaryObservation(selection, boundary, None, "no_reentered_selected_next_xi")
    if boundary is None:
        return ReenteredHandoffSummaryObservation(selection, None, None, "reentered_handoff_summary_not_created_without_boundary")
    summary = HandoffSummaryCandidate("interval_159_178_handoff_summary_candidate", selected.label, "159-178", False)
    return ReenteredHandoffSummaryObservation(selection, boundary, summary, "handoff_summary_observed_from_reentered_next_xi_not_next_work")


def compare_handoff_summary_reentry() -> tuple[ReenteredHandoffSummaryObservation, ReenteredHandoffSummaryObservation]:
    selection = compare_next_xi_selection_reentry()[1]
    return create_reentered_handoff_summary(selection, None), create_reentered_handoff_summary(selection, handoff_boundary_fixture())


def run_checks() -> None:
    without_boundary, with_boundary = compare_handoff_summary_reentry()
    assert without_boundary.handoff_summary is None
    assert with_boundary.handoff_summary is not None
    assert with_boundary.handoff_summary.summarizes_range == "159-178"


if __name__ == "__main__":
    run_checks()
    print(compare_handoff_summary_reentry()[1].status)
