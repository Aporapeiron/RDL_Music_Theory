"""publication plan候補とnext ξ selection境界の最小検証。"""

from dataclasses import dataclass

from interval_module_publication_plan_boundary import (
    PublicationPlanObservation,
    compare_publication_plan,
)


@dataclass(frozen=True)
class NextXiInventory:
    name: str
    candidates: tuple[str, ...]
    generated_by_publication_plan: bool


@dataclass(frozen=True)
class SelectedNextXiCandidate:
    label: str
    source_publication_plan_label: str
    selected_xi: str
    next_work_started: bool


@dataclass(frozen=True)
class NextXiSelectionObservation:
    publication_observation: PublicationPlanObservation
    xi_inventory: NextXiInventory | None
    selected_xi: SelectedNextXiCandidate | None
    status: str


def publication_observation() -> PublicationPlanObservation:
    return compare_publication_plan()[1]


def next_xi_inventory_fixture() -> NextXiInventory:
    return NextXiInventory(
        name="interval_next_xi_inventory_fixture",
        candidates=("xi_interval_module_contract_generalization", "xi_cross_module_reuse"),
        generated_by_publication_plan=False,
    )


def select_next_xi(
    publication: PublicationPlanObservation,
    inventory: NextXiInventory | None,
) -> NextXiSelectionObservation:
    plan = publication.publication_plan
    if plan is None:
        return NextXiSelectionObservation(publication, inventory, None, "no_publication_plan")
    if inventory is None:
        return NextXiSelectionObservation(
            publication, None, None, "next_xi_not_selected_without_inventory"
        )
    selected = SelectedNextXiCandidate(
        label="selected_next_xi_candidate",
        source_publication_plan_label=plan.label,
        selected_xi=inventory.candidates[0],
        next_work_started=False,
    )
    return NextXiSelectionObservation(
        publication, inventory, selected, "next_xi_candidate_selected_not_started"
    )


def compare_next_xi_selection() -> tuple[
    NextXiSelectionObservation, NextXiSelectionObservation
]:
    publication = publication_observation()
    return (
        select_next_xi(publication, None),
        select_next_xi(publication, next_xi_inventory_fixture()),
    )


def run_checks() -> None:
    without_inventory, with_inventory = compare_next_xi_selection()
    assert without_inventory.status == "next_xi_not_selected_without_inventory"
    assert with_inventory.status == "next_xi_candidate_selected_not_started"
    assert with_inventory.selected_xi is not None
    assert with_inventory.selected_xi.next_work_started is False
    assert with_inventory.xi_inventory is not None
    assert with_inventory.xi_inventory.generated_by_publication_plan is False


if __name__ == "__main__":
    run_checks()
    print(compare_next_xi_selection()[1].status)
