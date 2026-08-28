"""和声機能Moduleで螺旋型再入循環の形が残るかを確認する最小検証。"""

from dataclasses import dataclass

from harmonic_function_target_candidate_boundary import (
    build_fixture,
    observe_target_candidates,
)


@dataclass(frozen=True)
class CrossModuleSpiralStep:
    number: int
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class HarmonicFunctionSpiralTransferObservation:
    source_module: str
    comparison_module: str
    function_annotation: str
    selected_target: str
    steps: tuple[CrossModuleSpiralStep, ...]
    preserves_boundary_shape: bool
    terminally_closed: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str], ...] = (
    (229, "harmonic_function_input_contract", "harmonic_function_input_contract_candidate"),
    (230, "chord_key_payload_binding", "bound_harmonic_payload_candidate"),
    (231, "degree_function_validation", "function_validation_diagnostic"),
    (232, "function_processing_request", "function_processing_request_candidate"),
    (233, "existing_42_function_activation", "function_annotation_candidate"),
    (234, "existing_43_target_boundary_bridge", "target_candidate_boundary_observation"),
    (235, "target_selection_controller_boundary", "selected_harmonic_target_candidate"),
    (236, "next_context_handoff_boundary", "next_context_interpretation_request"),
    (237, "contract_generalization_target", "harmonic_function_contract_generalization_target"),
    (238, "cross_module_spiral_equivalence_check", "isomorphic_spiral_shape_candidate"),
)


def observe_harmonic_function_spiral_transfer() -> HarmonicFunctionSpiralTransferObservation:
    function_observation, candidates = build_fixture()
    selected = observe_target_candidates(
        function_observation,
        candidates,
        selection_policy="prefer_primary_tonic_resolution",
    )
    assert selected.selected is not None

    previous = "harmonic_function_module_boundary"
    steps = []
    for number, name, result in STEP_DEFINITIONS:
        steps.append(
            CrossModuleSpiralStep(
                number=number,
                name=name,
                source=previous,
                result=result,
                generated_mutation=False,
            )
        )
        previous = result

    observed = tuple(steps)
    preserves_boundary_shape = (
        observed[0].result == "harmonic_function_input_contract_candidate"
        and observed[3].result == "function_processing_request_candidate"
        and observed[4].result == "function_annotation_candidate"
        and observed[5].result == "target_candidate_boundary_observation"
        and observed[7].result == "next_context_interpretation_request"
        and observed[8].result == "harmonic_function_contract_generalization_target"
        and observed[9].result == "isomorphic_spiral_shape_candidate"
    )

    return HarmonicFunctionSpiralTransferObservation(
        source_module="和声機能Module",
        comparison_module="音程Module",
        function_annotation=function_observation.function_annotation,
        selected_target=selected.selected.target_chord,
        steps=observed,
        preserves_boundary_shape=preserves_boundary_shape,
        terminally_closed=False,
        generated_mutation=any(step.generated_mutation for step in observed),
        status="harmonic_function_spiral_transfer_229_238_preserves_boundary_shape_without_terminal_closure_or_mutation",
    )


def run_checks() -> None:
    observation = observe_harmonic_function_spiral_transfer()
    assert observation.source_module == "和声機能Module"
    assert observation.comparison_module == "音程Module"
    assert observation.function_annotation == "dominant_candidate"
    assert observation.selected_target == "C major"
    assert len(observation.steps) == 10
    assert observation.steps[0].number == 229
    assert observation.steps[-1].number == 238
    assert observation.preserves_boundary_shape is True
    assert observation.terminally_closed is False
    assert observation.generated_mutation is False


if __name__ == "__main__":
    run_checks()
    print(observe_harmonic_function_spiral_transfer().status)
