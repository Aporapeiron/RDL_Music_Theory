"""confirmed learned categoryとmusical interpretation境界の最小検証。

65で得たconfirmed learned category candidateを固定し、interpretation
contextとGamma_musical_interpretationを与えた場合だけselected musical
interpretation candidateが生じることを確認する。Core music moduleには接続しない。

    confirmed learned category candidate
      + external interpretation context
      + Gamma_musical_interpretation_fixture
      -> selected musical interpretation candidate
      -> core music module connection remains None
"""

from dataclasses import dataclass

from base_to_learned_category_confirmation_boundary import (
    CategoryConfirmationObservation,
    ConfirmedLearnedCategoryCandidate,
    compare_category_confirmation,
)


@dataclass(frozen=True)
class MusicalInterpretationContext:
    label: str
    context_kind: str
    interpretation_family: str
    generated_by_confirmed_category: bool


@dataclass(frozen=True)
class MusicalInterpretationGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class SelectedMusicalInterpretationCandidate:
    label: str
    source_confirmed_category_label: str
    interpretation_context_label: str
    core_music_module_connection: str | None


@dataclass(frozen=True)
class MusicalInterpretationObservation:
    confirmation_observation: CategoryConfirmationObservation
    interpretation_context: MusicalInterpretationContext | None
    interpretation_gamma: MusicalInterpretationGamma | None
    selected_musical_interpretation: SelectedMusicalInterpretationCandidate | None
    core_music_module_connection: str | None
    status: str
    interpretation_reason: str | None


@dataclass(frozen=True)
class MusicalInterpretationComparison:
    without_gamma: MusicalInterpretationObservation
    with_gamma: MusicalInterpretationObservation
    same_confirmed_category: bool
    same_interpretation_context: bool
    same_interpretation_gamma: bool
    interpretation_observed: bool
    core_music_module_connection: str | None


def confirmed_category_observation() -> CategoryConfirmationObservation:
    return compare_category_confirmation().with_gamma


def pitch_relation_interpretation_context() -> MusicalInterpretationContext:
    return MusicalInterpretationContext(
        label="pitch_relation_interpretation_context_fixture",
        context_kind="external_interpretation_context_fixture",
        interpretation_family="pitch_relation_judgement",
        generated_by_confirmed_category=False,
    )


def musical_interpretation_gamma() -> MusicalInterpretationGamma:
    return MusicalInterpretationGamma(
        name="Gamma_musical_interpretation_fixture",
        reads=("confirmed_learned_category_candidate", "interpretation_context"),
        rule_scope="fixture_limited_not_general_musical_interpretation_rule",
    )


def confirmed_category_label(
    confirmation_observation: CategoryConfirmationObservation,
) -> str | None:
    if confirmation_observation.confirmed_category is None:
        return None
    return confirmation_observation.confirmed_category.label


def interpret_confirmed_category(
    confirmation_observation: CategoryConfirmationObservation,
    interpretation_context: MusicalInterpretationContext | None,
    interpretation_gamma: MusicalInterpretationGamma | None,
) -> MusicalInterpretationObservation:
    confirmed = confirmation_observation.confirmed_category
    if confirmed is None:
        return MusicalInterpretationObservation(
            confirmation_observation=confirmation_observation,
            interpretation_context=interpretation_context,
            interpretation_gamma=interpretation_gamma,
            selected_musical_interpretation=None,
            core_music_module_connection=None,
            status="no_confirmed_learned_category_candidate",
            interpretation_reason=None,
        )

    if interpretation_context is None:
        return MusicalInterpretationObservation(
            confirmation_observation=confirmation_observation,
            interpretation_context=None,
            interpretation_gamma=interpretation_gamma,
            selected_musical_interpretation=None,
            core_music_module_connection=None,
            status="confirmed_category_uninterpreted_without_context",
            interpretation_reason=None,
        )

    if interpretation_gamma is None:
        return MusicalInterpretationObservation(
            confirmation_observation=confirmation_observation,
            interpretation_context=interpretation_context,
            interpretation_gamma=None,
            selected_musical_interpretation=None,
            core_music_module_connection=None,
            status="confirmed_category_uninterpreted_without_gamma",
            interpretation_reason=None,
        )

    if (
        confirmed.label != "different_pitch_relation_label_candidate"
        or interpretation_context.interpretation_family != "pitch_relation_judgement"
    ):
        return MusicalInterpretationObservation(
            confirmation_observation=confirmation_observation,
            interpretation_context=interpretation_context,
            interpretation_gamma=interpretation_gamma,
            selected_musical_interpretation=None,
            core_music_module_connection=None,
            status="interpretation_context_not_applicable",
            interpretation_reason=None,
        )

    interpretation = SelectedMusicalInterpretationCandidate(
        label="pitch_relation_different_interpretation_candidate",
        source_confirmed_category_label=confirmed.label,
        interpretation_context_label=interpretation_context.label,
        core_music_module_connection=None,
    )
    return MusicalInterpretationObservation(
        confirmation_observation=confirmation_observation,
        interpretation_context=interpretation_context,
        interpretation_gamma=interpretation_gamma,
        selected_musical_interpretation=interpretation,
        core_music_module_connection=None,
        status="selected_musical_interpretation_candidate_not_connected_to_core",
        interpretation_reason="confirmed_category_matches_interpretation_context",
    )


def compare_musical_interpretation() -> MusicalInterpretationComparison:
    confirmation = confirmed_category_observation()
    context = pitch_relation_interpretation_context()
    without_gamma = interpret_confirmed_category(
        confirmation_observation=confirmation,
        interpretation_context=context,
        interpretation_gamma=None,
    )
    with_gamma = interpret_confirmed_category(
        confirmation_observation=confirmation,
        interpretation_context=context,
        interpretation_gamma=musical_interpretation_gamma(),
    )
    return MusicalInterpretationComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_confirmed_category=(
            without_gamma.confirmation_observation.confirmed_category
            == with_gamma.confirmation_observation.confirmed_category
        ),
        same_interpretation_context=(
            without_gamma.interpretation_context == with_gamma.interpretation_context
        ),
        same_interpretation_gamma=(
            without_gamma.interpretation_gamma == with_gamma.interpretation_gamma
        ),
        interpretation_observed=(
            with_gamma.status
            == "selected_musical_interpretation_candidate_not_connected_to_core"
        ),
        core_music_module_connection=with_gamma.core_music_module_connection,
    )


def run_checks() -> None:
    comparison = compare_musical_interpretation()
    assert comparison.same_confirmed_category is True
    assert comparison.same_interpretation_context is True
    assert comparison.same_interpretation_gamma is False
    assert comparison.interpretation_observed is True
    assert comparison.core_music_module_connection is None

    assert (
        comparison.without_gamma.status
        == "confirmed_category_uninterpreted_without_gamma"
    )
    assert comparison.without_gamma.selected_musical_interpretation is None

    assert (
        comparison.with_gamma.status
        == "selected_musical_interpretation_candidate_not_connected_to_core"
    )
    assert comparison.with_gamma.selected_musical_interpretation is not None
    assert comparison.with_gamma.selected_musical_interpretation.label == (
        "pitch_relation_different_interpretation_candidate"
    )
    assert comparison.with_gamma.core_music_module_connection is None
    assert comparison.with_gamma.interpretation_context is not None
    assert (
        comparison.with_gamma.interpretation_context.generated_by_confirmed_category
        is False
    )
    assert comparison.with_gamma.interpretation_reason == (
        "confirmed_category_matches_interpretation_context"
    )

    confirmed: ConfirmedLearnedCategoryCandidate | None = (
        comparison.with_gamma.confirmation_observation.confirmed_category
    )
    assert confirmed is not None
    assert confirmed.selected_musical_interpretation is None


def main() -> None:
    run_checks()
    comparison = compare_musical_interpretation()
    with_gamma = comparison.with_gamma

    print("[pipeline]")
    print("  confirmed learned category candidate")
    print("  + external interpretation context")
    print("  + Gamma_musical_interpretation_fixture")
    print("  -> selected musical interpretation candidate")
    print("  -> core music module connection remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_confirmed_category={comparison.same_confirmed_category}")
    print(f"  same_interpretation_context={comparison.same_interpretation_context}")
    print(f"  same_interpretation_gamma={comparison.same_interpretation_gamma}")
    print(f"  interpretation_observed={comparison.interpretation_observed}")
    print(
        "  confirmed_category="
        + (confirmed_category_label(with_gamma.confirmation_observation) or "None")
    )
    print(
        "  selected_musical_interpretation="
        + (
            with_gamma.selected_musical_interpretation.label
            if with_gamma.selected_musical_interpretation
            else "None"
        )
    )
    print(
        "  core_music_module_connection="
        f"{comparison.core_music_module_connection}"
    )


if __name__ == "__main__":
    main()
