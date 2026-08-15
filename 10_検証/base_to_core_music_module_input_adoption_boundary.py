"""core module bridge candidateとinput adoption境界の最小検証。

67で得たcore module bridge candidateを固定し、Gamma_core_module_input_adoption
を与えた場合だけcore module input candidateとして採用されることを確認する。
中核Module内部処理やCore昇格は行わない。

    core module bridge candidate
      + Gamma_core_module_input_adoption_fixture
      -> core module input candidate
      -> module processing remains not started
"""

from dataclasses import dataclass

from base_to_core_music_module_bridge_boundary import (
    CoreModuleBridgeObservation,
    compare_core_module_bridge,
)


@dataclass(frozen=True)
class CoreModuleInputAdoptionController:
    name: str
    reads: tuple[str, ...]
    rule_scope: str


@dataclass(frozen=True)
class CoreModuleInputCandidate:
    input_label: str
    module_name: str
    source_bridge_candidate_label: str
    module_processing_started: bool
    core_promoted: bool


@dataclass(frozen=True)
class CoreModuleInputAdoptionObservation:
    bridge_observation: CoreModuleBridgeObservation
    adoption_controller: CoreModuleInputAdoptionController | None
    core_module_input: CoreModuleInputCandidate | None
    module_processing_started: bool
    core_promoted: bool
    status: str
    adoption_reason: str | None


@dataclass(frozen=True)
class CoreModuleInputAdoptionComparison:
    without_controller: CoreModuleInputAdoptionObservation
    with_controller: CoreModuleInputAdoptionObservation
    same_bridge_candidate: bool
    same_adoption_controller: bool
    input_adoption_observed: bool
    module_processing_started: bool
    core_promoted: bool


def core_module_bridge_observation() -> CoreModuleBridgeObservation:
    return compare_core_module_bridge().with_gamma


def core_module_input_adoption_controller() -> CoreModuleInputAdoptionController:
    return CoreModuleInputAdoptionController(
        name="Gamma_core_module_input_adoption_fixture",
        reads=("core_module_bridge_candidate",),
        rule_scope="fixture_limited_not_general_core_module_input_adoption",
    )


def adopt_core_module_input(
    bridge_observation: CoreModuleBridgeObservation,
    adoption_controller: CoreModuleInputAdoptionController | None,
) -> CoreModuleInputAdoptionObservation:
    bridge_candidate = bridge_observation.bridge_candidate
    if bridge_candidate is None:
        return CoreModuleInputAdoptionObservation(
            bridge_observation=bridge_observation,
            adoption_controller=adoption_controller,
            core_module_input=None,
            module_processing_started=False,
            core_promoted=False,
            status="no_core_module_bridge_candidate",
            adoption_reason=None,
        )

    if adoption_controller is None:
        return CoreModuleInputAdoptionObservation(
            bridge_observation=bridge_observation,
            adoption_controller=None,
            core_module_input=None,
            module_processing_started=False,
            core_promoted=False,
            status="core_module_bridge_candidate_unadopted",
            adoption_reason=None,
        )

    module_candidate = bridge_candidate.module_candidate
    adopted = CoreModuleInputCandidate(
        input_label="interval_module_pitch_relation_input_candidate",
        module_name=module_candidate.module_name,
        source_bridge_candidate_label=module_candidate.label,
        module_processing_started=False,
        core_promoted=False,
    )
    return CoreModuleInputAdoptionObservation(
        bridge_observation=bridge_observation,
        adoption_controller=adoption_controller,
        core_module_input=adopted,
        module_processing_started=False,
        core_promoted=False,
        status="core_module_input_candidate_adopted_not_processed",
        adoption_reason="adoption_controller_accepts_bridge_candidate",
    )


def compare_core_module_input_adoption() -> CoreModuleInputAdoptionComparison:
    bridge_observation = core_module_bridge_observation()
    without_controller = adopt_core_module_input(
        bridge_observation=bridge_observation,
        adoption_controller=None,
    )
    with_controller = adopt_core_module_input(
        bridge_observation=bridge_observation,
        adoption_controller=core_module_input_adoption_controller(),
    )
    return CoreModuleInputAdoptionComparison(
        without_controller=without_controller,
        with_controller=with_controller,
        same_bridge_candidate=(
            without_controller.bridge_observation.bridge_candidate
            == with_controller.bridge_observation.bridge_candidate
        ),
        same_adoption_controller=(
            without_controller.adoption_controller == with_controller.adoption_controller
        ),
        input_adoption_observed=(
            with_controller.status
            == "core_module_input_candidate_adopted_not_processed"
        ),
        module_processing_started=with_controller.module_processing_started,
        core_promoted=with_controller.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_core_module_input_adoption()
    assert comparison.same_bridge_candidate is True
    assert comparison.same_adoption_controller is False
    assert comparison.input_adoption_observed is True
    assert comparison.module_processing_started is False
    assert comparison.core_promoted is False

    assert (
        comparison.without_controller.status
        == "core_module_bridge_candidate_unadopted"
    )
    assert comparison.without_controller.core_module_input is None

    assert (
        comparison.with_controller.status
        == "core_module_input_candidate_adopted_not_processed"
    )
    assert comparison.with_controller.core_module_input is not None
    assert comparison.with_controller.core_module_input.input_label == (
        "interval_module_pitch_relation_input_candidate"
    )
    assert comparison.with_controller.core_module_input.module_name == "音程_Module"
    assert comparison.with_controller.core_module_input.module_processing_started is False
    assert comparison.with_controller.core_module_input.core_promoted is False
    assert comparison.with_controller.adoption_reason == (
        "adoption_controller_accepts_bridge_candidate"
    )
    assert comparison.with_controller.bridge_observation.core_module_input is None


def main() -> None:
    run_checks()
    comparison = compare_core_module_input_adoption()
    with_controller = comparison.with_controller

    print("[pipeline]")
    print("  core module bridge candidate")
    print("  + Gamma_core_module_input_adoption_fixture")
    print("  -> core module input candidate")
    print("  -> module processing remains not started")
    print(f"  without_controller_status={comparison.without_controller.status}")
    print(f"  with_controller_status={with_controller.status}")
    print(f"  same_bridge_candidate={comparison.same_bridge_candidate}")
    print(f"  same_adoption_controller={comparison.same_adoption_controller}")
    print(f"  input_adoption_observed={comparison.input_adoption_observed}")
    print(
        "  core_module_bridge_candidate="
        + (
            with_controller.bridge_observation.bridge_candidate.module_candidate.label
            if with_controller.bridge_observation.bridge_candidate
            else "None"
        )
    )
    print(
        "  core_module_input_candidate="
        + (
            with_controller.core_module_input.input_label
            if with_controller.core_module_input
            else "None"
        )
    )
    print(f"  module_processing_started={comparison.module_processing_started}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
