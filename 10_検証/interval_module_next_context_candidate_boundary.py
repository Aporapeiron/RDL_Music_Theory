"""音程Module concrete voice leadingとnext context候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_voice_leading_realization_boundary import (
    VoiceLeadingRealizationObservation,
    compare_voice_leading_realization,
)


@dataclass(frozen=True)
class NextContextCandidate:
    label: str
    tonic: str
    mode: str
    source: str
    generated_by_voice_leading: bool


@dataclass(frozen=True)
class NextContextInventory:
    name: str
    candidates: tuple[NextContextCandidate, ...]
    generated_by_voice_leading: bool


@dataclass(frozen=True)
class NextContextCandidateFilterGamma:
    name: str
    reads: tuple[str, str]
    accepted_sources: tuple[str, ...]
    rule_scope: str


@dataclass(frozen=True)
class NextContextCandidateSetObservation:
    voice_leading_observation: VoiceLeadingRealizationObservation
    next_context_inventory: NextContextInventory | None
    gamma_next_context_filter: NextContextCandidateFilterGamma | None
    next_context_candidates: tuple[NextContextCandidate, ...]
    selected_next_context: NextContextCandidate | None
    harmonic_function_generated: bool
    core_promoted: bool
    status: str
    filter_reason: str | None


@dataclass(frozen=True)
class NextContextCandidateSetComparison:
    without_gamma: NextContextCandidateSetObservation
    with_gamma: NextContextCandidateSetObservation
    same_voice_leading_observation: bool
    same_next_context_inventory: bool
    same_gamma_next_context_filter: bool
    candidate_set_observed: bool
    selected_next_context_generated: bool
    harmonic_function_generated: bool
    core_promoted: bool


def voice_leading_observation() -> VoiceLeadingRealizationObservation:
    return compare_voice_leading_realization().with_gamma


def next_context_inventory_fixture() -> NextContextInventory:
    return NextContextInventory(
        name="external_next_context_inventory_fixture",
        candidates=(
            NextContextCandidate(
                label="C major continuation",
                tonic="C",
                mode="major",
                source="continuation_fixture",
                generated_by_voice_leading=False,
            ),
            NextContextCandidate(
                label="G major reinterpretation",
                tonic="G",
                mode="major",
                source="reinterpretation_fixture",
                generated_by_voice_leading=False,
            ),
            NextContextCandidate(
                label="A minor reinterpretation",
                tonic="A",
                mode="minor",
                source="remote_fixture",
                generated_by_voice_leading=False,
            ),
        ),
        generated_by_voice_leading=False,
    )


def gamma_next_context_filter_fixture() -> NextContextCandidateFilterGamma:
    return NextContextCandidateFilterGamma(
        name="Gamma_next_context_candidate_filter_fixture",
        reads=("concrete_voice_leading", "external_next_context_inventory"),
        accepted_sources=("continuation_fixture", "reinterpretation_fixture"),
        rule_scope="fixture_limited_not_next_context_selection_rule",
    )


def observe_next_context_candidates(
    voice_leading: VoiceLeadingRealizationObservation,
    inventory: NextContextInventory | None,
    gamma_next_context_filter: NextContextCandidateFilterGamma | None,
) -> NextContextCandidateSetObservation:
    if voice_leading.concrete_voice_leading is None:
        return NextContextCandidateSetObservation(
            voice_leading_observation=voice_leading,
            next_context_inventory=inventory,
            gamma_next_context_filter=gamma_next_context_filter,
            next_context_candidates=(),
            selected_next_context=None,
            harmonic_function_generated=False,
            core_promoted=False,
            status="no_concrete_voice_leading_observation",
            filter_reason=None,
        )
    if inventory is None:
        return NextContextCandidateSetObservation(
            voice_leading_observation=voice_leading,
            next_context_inventory=None,
            gamma_next_context_filter=gamma_next_context_filter,
            next_context_candidates=(),
            selected_next_context=None,
            harmonic_function_generated=False,
            core_promoted=False,
            status="next_context_candidates_not_observed_without_inventory",
            filter_reason=None,
        )
    if gamma_next_context_filter is None:
        return NextContextCandidateSetObservation(
            voice_leading_observation=voice_leading,
            next_context_inventory=inventory,
            gamma_next_context_filter=None,
            next_context_candidates=(),
            selected_next_context=None,
            harmonic_function_generated=False,
            core_promoted=False,
            status="next_context_candidates_not_observed_without_filter_gamma",
            filter_reason=None,
        )

    filtered = tuple(
        candidate
        for candidate in inventory.candidates
        if candidate.source in gamma_next_context_filter.accepted_sources
    )
    return NextContextCandidateSetObservation(
        voice_leading_observation=voice_leading,
        next_context_inventory=inventory,
        gamma_next_context_filter=gamma_next_context_filter,
        next_context_candidates=filtered,
        selected_next_context=None,
        harmonic_function_generated=False,
        core_promoted=False,
        status="next_context_candidate_set_observed_unselected",
        filter_reason="external_inventory_filtered_by_Gamma_next_context_candidate_filter",
    )


def compare_next_context_candidate_set() -> NextContextCandidateSetComparison:
    voice_leading = voice_leading_observation()
    inventory = next_context_inventory_fixture()
    without_gamma = observe_next_context_candidates(voice_leading, inventory, None)
    with_gamma = observe_next_context_candidates(
        voice_leading, inventory, gamma_next_context_filter_fixture()
    )
    return NextContextCandidateSetComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_voice_leading_observation=(
            without_gamma.voice_leading_observation.concrete_voice_leading
            == with_gamma.voice_leading_observation.concrete_voice_leading
        ),
        same_next_context_inventory=(
            without_gamma.next_context_inventory == with_gamma.next_context_inventory
        ),
        same_gamma_next_context_filter=(
            without_gamma.gamma_next_context_filter
            == with_gamma.gamma_next_context_filter
        ),
        candidate_set_observed=(
            with_gamma.status == "next_context_candidate_set_observed_unselected"
        ),
        selected_next_context_generated=with_gamma.selected_next_context is not None,
        harmonic_function_generated=with_gamma.harmonic_function_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_next_context_candidate_set()
    assert comparison.same_voice_leading_observation is True
    assert comparison.same_next_context_inventory is True
    assert comparison.same_gamma_next_context_filter is False
    assert comparison.candidate_set_observed is True
    assert comparison.selected_next_context_generated is False
    assert comparison.harmonic_function_generated is False
    assert comparison.core_promoted is False
    assert (
        comparison.without_gamma.status
        == "next_context_candidates_not_observed_without_filter_gamma"
    )
    assert comparison.without_gamma.next_context_candidates == ()
    assert comparison.with_gamma.next_context_inventory is not None
    assert comparison.with_gamma.next_context_inventory.generated_by_voice_leading is False
    assert tuple(
        candidate.label for candidate in comparison.with_gamma.next_context_candidates
    ) == ("C major continuation", "G major reinterpretation")
    assert all(
        candidate.generated_by_voice_leading is False
        for candidate in comparison.with_gamma.next_context_candidates
    )


def main() -> None:
    run_checks()
    comparison = compare_next_context_candidate_set()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  concrete voice leading observation")
    print("  + external next context inventory")
    print("  + Gamma_next_context_candidate_filter_fixture")
    print("  -> next context candidate set observed")
    print("  -> selected next context remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_voice_leading_observation={comparison.same_voice_leading_observation}")
    print(f"  same_next_context_inventory={comparison.same_next_context_inventory}")
    print(f"  same_gamma_next_context_filter={comparison.same_gamma_next_context_filter}")
    print(f"  candidate_set_observed={comparison.candidate_set_observed}")
    print(
        "  next_context_candidates="
        + ",".join(candidate.label for candidate in with_gamma.next_context_candidates)
    )
    print(
        "  selected_next_context_generated="
        f"{comparison.selected_next_context_generated}"
    )
    print(f"  harmonic_function_generated={comparison.harmonic_function_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
