"""再入publication plan候補とnext xi selection境界の最小検証。"""

from dataclasses import dataclass

from interval_module_next_xi_selection_boundary import NextXiInventory, SelectedNextXiCandidate, next_xi_inventory_fixture
from interval_module_publication_plan_reentry import ReenteredPublicationPlanObservation, compare_publication_plan_reentry


@dataclass(frozen=True)
class ReenteredNextXiSelectionObservation:
    publication_observation: ReenteredPublicationPlanObservation
    xi_inventory: NextXiInventory | None
    selected_xi: SelectedNextXiCandidate | None
    status: str


def select_reentered_next_xi(publication: ReenteredPublicationPlanObservation, inventory: NextXiInventory | None) -> ReenteredNextXiSelectionObservation:
    plan = publication.publication_plan
    if plan is None:
        return ReenteredNextXiSelectionObservation(publication, inventory, None, "no_reentered_publication_plan")
    if inventory is None:
        return ReenteredNextXiSelectionObservation(publication, None, None, "reentered_next_xi_not_selected_without_inventory")
    selected = SelectedNextXiCandidate("selected_next_xi_candidate", plan.label, inventory.candidates[0], False)
    return ReenteredNextXiSelectionObservation(publication, inventory, selected, "next_xi_selected_from_reentered_publication_not_started")


def compare_next_xi_selection_reentry() -> tuple[ReenteredNextXiSelectionObservation, ReenteredNextXiSelectionObservation]:
    publication = compare_publication_plan_reentry()[1]
    return select_reentered_next_xi(publication, None), select_reentered_next_xi(publication, next_xi_inventory_fixture())


def run_checks() -> None:
    without_inventory, with_inventory = compare_next_xi_selection_reentry()
    assert without_inventory.selected_xi is None
    assert with_inventory.selected_xi is not None
    assert with_inventory.selected_xi.next_work_started is False


if __name__ == "__main__":
    run_checks()
    print(compare_next_xi_selection_reentry()[1].status)
