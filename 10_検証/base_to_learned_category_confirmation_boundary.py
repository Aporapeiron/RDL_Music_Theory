"""selected bridge candidateとcategory confirmation境界の最小検証。

64で得たselected bridge candidateを固定し、confirmation evidenceと
Gamma_category_confirmationを与えた場合だけconfirmed learned category
candidateへ昇格することを確認する。musical interpretationは生成しない。

    selected bridge candidate
      + external confirmation evidence
      + Gamma_category_confirmation_fixture
      -> confirmed learned category candidate
      -> selected musical interpretation remains None
"""

from dataclasses import dataclass

from base_to_learned_bridge_selection_controller_boundary import (
    BridgeSelectionObservation,
    compare_bridge_selection_controllers,
    selected_label,
)


@dataclass(frozen=True)
class CategoryConfirmationEvidence:
    label: str
    evidence_kind: str
    supports_candidate_label: str
    generated_by_selected_bridge: bool


@dataclass(frozen=True)
class CategoryConfirmationGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class ConfirmedLearnedCategoryCandidate:
    label: str
    source_selected_bridge_label: str
    evidence_label: str
    selected_musical_interpretation: str | None


@dataclass(frozen=True)
class CategoryConfirmationObservation:
    selection_observation: BridgeSelectionObservation
    confirmation_evidence: CategoryConfirmationEvidence | None
    confirmation_gamma: CategoryConfirmationGamma | None
    confirmed_category: ConfirmedLearnedCategoryCandidate | None
    selected_musical_interpretation: str | None
    status: str
    confirmation_reason: str | None


@dataclass(frozen=True)
class CategoryConfirmationComparison:
    without_gamma: CategoryConfirmationObservation
    with_gamma: CategoryConfirmationObservation
    same_selected_bridge_candidate: bool
    same_confirmation_evidence: bool
    same_confirmation_gamma: bool
    confirmation_observed: bool
    selected_musical_interpretation: str | None


def selected_bridge_observation() -> BridgeSelectionObservation:
    return compare_bridge_selection_controllers().top_rank_selection


def stable_label_use_evidence() -> CategoryConfirmationEvidence:
    return CategoryConfirmationEvidence(
        label="stable_label_use_fixture",
        evidence_kind="external_confirmation_fixture",
        supports_candidate_label="different_pitch_relation_label_candidate",
        generated_by_selected_bridge=False,
    )


def category_confirmation_gamma() -> CategoryConfirmationGamma:
    return CategoryConfirmationGamma(
        name="Gamma_category_confirmation_fixture",
        reads=("selected_bridge_candidate", "confirmation_evidence"),
        rule_scope="fixture_limited_not_general_category_confirmation_rule",
    )


def confirm_selected_bridge_candidate(
    selection_observation: BridgeSelectionObservation,
    confirmation_evidence: CategoryConfirmationEvidence | None,
    confirmation_gamma: CategoryConfirmationGamma | None,
) -> CategoryConfirmationObservation:
    if selection_observation.selected_bridge_candidate is None:
        return CategoryConfirmationObservation(
            selection_observation=selection_observation,
            confirmation_evidence=confirmation_evidence,
            confirmation_gamma=confirmation_gamma,
            confirmed_category=None,
            selected_musical_interpretation=None,
            status="no_selected_bridge_candidate",
            confirmation_reason=None,
        )

    if confirmation_evidence is None:
        return CategoryConfirmationObservation(
            selection_observation=selection_observation,
            confirmation_evidence=None,
            confirmation_gamma=confirmation_gamma,
            confirmed_category=None,
            selected_musical_interpretation=None,
            status="selected_bridge_unconfirmed_without_evidence",
            confirmation_reason=None,
        )

    if confirmation_gamma is None:
        return CategoryConfirmationObservation(
            selection_observation=selection_observation,
            confirmation_evidence=confirmation_evidence,
            confirmation_gamma=None,
            confirmed_category=None,
            selected_musical_interpretation=None,
            status="selected_bridge_unconfirmed_without_gamma",
            confirmation_reason=None,
        )

    bridge_label = selected_label(selection_observation)
    if bridge_label != confirmation_evidence.supports_candidate_label:
        return CategoryConfirmationObservation(
            selection_observation=selection_observation,
            confirmation_evidence=confirmation_evidence,
            confirmation_gamma=confirmation_gamma,
            confirmed_category=None,
            selected_musical_interpretation=None,
            status="confirmation_evidence_not_applicable",
            confirmation_reason=None,
        )

    confirmed = ConfirmedLearnedCategoryCandidate(
        label=bridge_label,
        source_selected_bridge_label=bridge_label,
        evidence_label=confirmation_evidence.label,
        selected_musical_interpretation=None,
    )
    return CategoryConfirmationObservation(
        selection_observation=selection_observation,
        confirmation_evidence=confirmation_evidence,
        confirmation_gamma=confirmation_gamma,
        confirmed_category=confirmed,
        selected_musical_interpretation=None,
        status="confirmed_learned_category_candidate_not_interpreted",
        confirmation_reason="evidence_supports_selected_bridge_label",
    )


def compare_category_confirmation() -> CategoryConfirmationComparison:
    selection = selected_bridge_observation()
    evidence = stable_label_use_evidence()
    without_gamma = confirm_selected_bridge_candidate(
        selection_observation=selection,
        confirmation_evidence=evidence,
        confirmation_gamma=None,
    )
    with_gamma = confirm_selected_bridge_candidate(
        selection_observation=selection,
        confirmation_evidence=evidence,
        confirmation_gamma=category_confirmation_gamma(),
    )
    return CategoryConfirmationComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_selected_bridge_candidate=(
            without_gamma.selection_observation.selected_bridge_candidate
            == with_gamma.selection_observation.selected_bridge_candidate
        ),
        same_confirmation_evidence=(
            without_gamma.confirmation_evidence == with_gamma.confirmation_evidence
        ),
        same_confirmation_gamma=(
            without_gamma.confirmation_gamma == with_gamma.confirmation_gamma
        ),
        confirmation_observed=(
            with_gamma.status
            == "confirmed_learned_category_candidate_not_interpreted"
        ),
        selected_musical_interpretation=(
            with_gamma.selected_musical_interpretation
        ),
    )


def run_checks() -> None:
    comparison = compare_category_confirmation()
    assert comparison.same_selected_bridge_candidate is True
    assert comparison.same_confirmation_evidence is True
    assert comparison.same_confirmation_gamma is False
    assert comparison.confirmation_observed is True
    assert comparison.selected_musical_interpretation is None

    assert (
        comparison.without_gamma.status
        == "selected_bridge_unconfirmed_without_gamma"
    )
    assert comparison.without_gamma.confirmed_category is None

    assert (
        comparison.with_gamma.status
        == "confirmed_learned_category_candidate_not_interpreted"
    )
    assert comparison.with_gamma.confirmed_category is not None
    assert comparison.with_gamma.confirmed_category.label == (
        "different_pitch_relation_label_candidate"
    )
    assert comparison.with_gamma.confirmed_category.selected_musical_interpretation is None
    assert comparison.with_gamma.selected_musical_interpretation is None
    assert comparison.with_gamma.confirmation_evidence is not None
    assert (
        comparison.with_gamma.confirmation_evidence.generated_by_selected_bridge
        is False
    )
    assert comparison.with_gamma.confirmation_reason == (
        "evidence_supports_selected_bridge_label"
    )


def main() -> None:
    run_checks()
    comparison = compare_category_confirmation()
    with_gamma = comparison.with_gamma

    print("[pipeline]")
    print("  selected bridge candidate")
    print("  + external confirmation evidence")
    print("  + Gamma_category_confirmation_fixture")
    print("  -> confirmed learned category candidate")
    print("  -> selected musical interpretation remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(
        "  same_selected_bridge_candidate="
        f"{comparison.same_selected_bridge_candidate}"
    )
    print(f"  same_confirmation_evidence={comparison.same_confirmation_evidence}")
    print(f"  same_confirmation_gamma={comparison.same_confirmation_gamma}")
    print(f"  confirmation_observed={comparison.confirmation_observed}")
    print(
        "  selected_bridge_candidate="
        + (selected_label(with_gamma.selection_observation) or "None")
    )
    print(
        "  confirmed_category="
        + (with_gamma.confirmed_category.label if with_gamma.confirmed_category else "None")
    )
    print(
        "  selected_musical_interpretation="
        f"{comparison.selected_musical_interpretation}"
    )


if __name__ == "__main__":
    main()
