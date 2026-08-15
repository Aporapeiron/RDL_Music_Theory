"""selected musical interpretationと中核Module候補接続境界の最小検証。

66で得たselected musical interpretation candidateを固定し、中核音楽理論側の
module candidate setとGamma_core_module_bridgeを与えた場合だけcore module
bridge candidateが生じることを確認する。core module inputへは確定しない。

    selected musical interpretation candidate
      + external core music module candidate set
      + Gamma_core_module_bridge_fixture
      -> core module bridge candidate
      -> core module input remains None
"""

from dataclasses import dataclass

from base_to_learned_musical_interpretation_boundary import (
    MusicalInterpretationObservation,
    SelectedMusicalInterpretationCandidate,
    compare_musical_interpretation,
)


@dataclass(frozen=True)
class CoreMusicModuleCandidate:
    label: str
    module_name: str
    candidate_family: str
    generated_by_musical_interpretation: bool


@dataclass(frozen=True)
class CoreModuleBridgeGamma:
    name: str
    target_module_candidate_label: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class CoreModuleBridgeCandidate:
    interpretation_label: str
    module_candidate: CoreMusicModuleCandidate
    bridge_relation: str
    core_module_input: str | None


@dataclass(frozen=True)
class CoreModuleBridgeObservation:
    musical_interpretation_observation: MusicalInterpretationObservation
    core_module_candidates: tuple[CoreMusicModuleCandidate, ...]
    bridge_gamma: CoreModuleBridgeGamma | None
    bridge_candidate: CoreModuleBridgeCandidate | None
    core_module_input: str | None
    status: str
    bridge_reason: str | None


@dataclass(frozen=True)
class CoreModuleBridgeComparison:
    without_gamma: CoreModuleBridgeObservation
    with_gamma: CoreModuleBridgeObservation
    same_musical_interpretation: bool
    same_core_module_candidates: bool
    same_bridge_gamma: bool
    bridge_candidate_observed: bool
    core_module_input: str | None


def selected_musical_interpretation_observation() -> MusicalInterpretationObservation:
    return compare_musical_interpretation().with_gamma


def external_core_module_candidates() -> tuple[CoreMusicModuleCandidate, ...]:
    return (
        CoreMusicModuleCandidate(
            label="interval_module_pitch_relation_candidate",
            module_name="音程_Module",
            candidate_family="pitch_relation_interpretation_receiver",
            generated_by_musical_interpretation=False,
        ),
        CoreMusicModuleCandidate(
            label="scale_key_module_degree_role_candidate",
            module_name="音階調_Module",
            candidate_family="degree_role_context_receiver",
            generated_by_musical_interpretation=False,
        ),
    )


def core_module_bridge_gamma() -> CoreModuleBridgeGamma:
    return CoreModuleBridgeGamma(
        name="Gamma_core_module_bridge_fixture",
        target_module_candidate_label="interval_module_pitch_relation_candidate",
        reads=("selected_musical_interpretation_candidate", "core_module_candidate_set"),
        rule_scope="fixture_limited_not_general_base_to_core_module_bridge",
    )


def selected_interpretation_label(
    observation: MusicalInterpretationObservation,
) -> str | None:
    if observation.selected_musical_interpretation is None:
        return None
    return observation.selected_musical_interpretation.label


def observe_core_module_bridge(
    musical_interpretation_observation: MusicalInterpretationObservation,
    core_module_candidates: tuple[CoreMusicModuleCandidate, ...],
    bridge_gamma: CoreModuleBridgeGamma | None,
) -> CoreModuleBridgeObservation:
    interpretation = musical_interpretation_observation.selected_musical_interpretation
    if interpretation is None:
        return CoreModuleBridgeObservation(
            musical_interpretation_observation=musical_interpretation_observation,
            core_module_candidates=core_module_candidates,
            bridge_gamma=bridge_gamma,
            bridge_candidate=None,
            core_module_input=None,
            status="no_selected_musical_interpretation_candidate",
            bridge_reason=None,
        )

    if not core_module_candidates:
        return CoreModuleBridgeObservation(
            musical_interpretation_observation=musical_interpretation_observation,
            core_module_candidates=core_module_candidates,
            bridge_gamma=bridge_gamma,
            bridge_candidate=None,
            core_module_input=None,
            status="no_core_module_candidates",
            bridge_reason=None,
        )

    if bridge_gamma is None:
        return CoreModuleBridgeObservation(
            musical_interpretation_observation=musical_interpretation_observation,
            core_module_candidates=core_module_candidates,
            bridge_gamma=None,
            bridge_candidate=None,
            core_module_input=None,
            status="selected_interpretation_unbridged_without_gamma",
            bridge_reason=None,
        )

    matched = next(
        (
            candidate
            for candidate in core_module_candidates
            if candidate.label == bridge_gamma.target_module_candidate_label
        ),
        None,
    )
    if matched is None:
        return CoreModuleBridgeObservation(
            musical_interpretation_observation=musical_interpretation_observation,
            core_module_candidates=core_module_candidates,
            bridge_gamma=bridge_gamma,
            bridge_candidate=None,
            core_module_input=None,
            status="no_core_module_bridge_candidate_observed",
            bridge_reason=None,
        )

    bridge_candidate = CoreModuleBridgeCandidate(
        interpretation_label=interpretation.label,
        module_candidate=matched,
        bridge_relation="compatible_core_module_bridge_candidate",
        core_module_input=None,
    )
    return CoreModuleBridgeObservation(
        musical_interpretation_observation=musical_interpretation_observation,
        core_module_candidates=core_module_candidates,
        bridge_gamma=bridge_gamma,
        bridge_candidate=bridge_candidate,
        core_module_input=None,
        status="core_module_bridge_candidate_observed_not_adopted",
        bridge_reason="interpretation_matches_module_candidate_family",
    )


def compare_core_module_bridge() -> CoreModuleBridgeComparison:
    interpretation = selected_musical_interpretation_observation()
    module_candidates = external_core_module_candidates()
    without_gamma = observe_core_module_bridge(
        musical_interpretation_observation=interpretation,
        core_module_candidates=module_candidates,
        bridge_gamma=None,
    )
    with_gamma = observe_core_module_bridge(
        musical_interpretation_observation=interpretation,
        core_module_candidates=module_candidates,
        bridge_gamma=core_module_bridge_gamma(),
    )
    return CoreModuleBridgeComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_musical_interpretation=(
            without_gamma.musical_interpretation_observation.selected_musical_interpretation
            == with_gamma.musical_interpretation_observation.selected_musical_interpretation
        ),
        same_core_module_candidates=(
            without_gamma.core_module_candidates == with_gamma.core_module_candidates
        ),
        same_bridge_gamma=without_gamma.bridge_gamma == with_gamma.bridge_gamma,
        bridge_candidate_observed=(
            with_gamma.status == "core_module_bridge_candidate_observed_not_adopted"
        ),
        core_module_input=with_gamma.core_module_input,
    )


def run_checks() -> None:
    comparison = compare_core_module_bridge()
    assert comparison.same_musical_interpretation is True
    assert comparison.same_core_module_candidates is True
    assert comparison.same_bridge_gamma is False
    assert comparison.bridge_candidate_observed is True
    assert comparison.core_module_input is None

    assert (
        comparison.without_gamma.status
        == "selected_interpretation_unbridged_without_gamma"
    )
    assert comparison.without_gamma.bridge_candidate is None

    assert (
        comparison.with_gamma.status
        == "core_module_bridge_candidate_observed_not_adopted"
    )
    assert comparison.with_gamma.bridge_candidate is not None
    assert comparison.with_gamma.bridge_candidate.module_candidate.label == (
        "interval_module_pitch_relation_candidate"
    )
    assert comparison.with_gamma.bridge_candidate.core_module_input is None
    assert comparison.with_gamma.core_module_input is None
    assert all(
        candidate.generated_by_musical_interpretation is False
        for candidate in comparison.with_gamma.core_module_candidates
    )
    assert comparison.with_gamma.bridge_reason == (
        "interpretation_matches_module_candidate_family"
    )

    interpretation: SelectedMusicalInterpretationCandidate | None = (
        comparison.with_gamma.musical_interpretation_observation.selected_musical_interpretation
    )
    assert interpretation is not None
    assert interpretation.core_music_module_connection is None


def main() -> None:
    run_checks()
    comparison = compare_core_module_bridge()
    with_gamma = comparison.with_gamma

    print("[pipeline]")
    print("  selected musical interpretation candidate")
    print("  + external core music module candidate set")
    print("  + Gamma_core_module_bridge_fixture")
    print("  -> core module bridge candidate")
    print("  -> core module input remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(
        "  same_musical_interpretation="
        f"{comparison.same_musical_interpretation}"
    )
    print(f"  same_core_module_candidates={comparison.same_core_module_candidates}")
    print(f"  same_bridge_gamma={comparison.same_bridge_gamma}")
    print(f"  bridge_candidate_observed={comparison.bridge_candidate_observed}")
    print(
        "  selected_musical_interpretation="
        + (selected_interpretation_label(with_gamma.musical_interpretation_observation) or "None")
    )
    print(
        "  core_module_bridge_candidate="
        + (
            with_gamma.bridge_candidate.module_candidate.label
            if with_gamma.bridge_candidate
            else "None"
        )
    )
    print(f"  core_module_input={comparison.core_module_input}")


if __name__ == "__main__":
    main()
