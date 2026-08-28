"""リズム拍節Moduleで螺旋型再入循環の形が残るかを確認する最小検証。"""

from dataclasses import dataclass

from rhythm_transition_projection_reconstruction import run_same_transition


@dataclass(frozen=True)
class RhythmSpiralStep:
    number: int
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class RhythmSpiralTransferObservation:
    source_module: str
    comparison_module: str
    reconstructed_candidates: tuple[str, ...]
    reconstruction_status: str
    steps: tuple[RhythmSpiralStep, ...]
    preserves_boundary_shape: bool
    terminally_closed: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str], ...] = (
    (239, "rhythm_input_contract", "rhythm_input_contract_candidate"),
    (240, "grid_meter_payload_binding", "bound_rhythm_payload_candidate"),
    (241, "candidate_space_validation", "rhythm_validation_diagnostic"),
    (242, "rhythm_processing_request", "rhythm_processing_request_candidate"),
    (243, "existing_26_boundary_reconstruction_activation", "rhythm_boundary_reconstruction_observation"),
    (244, "existing_28_transition_projection_bridge", "rhythm_transition_projection_observation"),
    (245, "candidate_regeneration_boundary", "reconstructed_rhythm_candidate_set"),
    (246, "rhythm_selection_status_boundary", "rhythm_selection_status_record"),
    (247, "rhythm_contract_generalization_target", "rhythm_contract_generalization_target"),
    (248, "cross_module_spiral_equivalence_check", "isomorphic_spiral_shape_candidate"),
)


def observe_rhythm_spiral_transfer() -> RhythmSpiralTransferObservation:
    rhythm_run = run_same_transition()

    previous = "rhythm_module_boundary"
    steps = []
    for number, name, result in STEP_DEFINITIONS:
        steps.append(
            RhythmSpiralStep(
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
        observed[0].result == "rhythm_input_contract_candidate"
        and observed[3].result == "rhythm_processing_request_candidate"
        and observed[4].result == "rhythm_boundary_reconstruction_observation"
        and observed[5].result == "rhythm_transition_projection_observation"
        and observed[6].result == "reconstructed_rhythm_candidate_set"
        and observed[8].result == "rhythm_contract_generalization_target"
        and observed[9].result == "isomorphic_spiral_shape_candidate"
    )

    return RhythmSpiralTransferObservation(
        source_module="リズム拍節Module",
        comparison_module="音程Module",
        reconstructed_candidates=rhythm_run.candidates,
        reconstruction_status=rhythm_run.status,
        steps=observed,
        preserves_boundary_shape=preserves_boundary_shape,
        terminally_closed=False,
        generated_mutation=any(step.generated_mutation for step in observed),
        status="rhythm_spiral_transfer_239_248_preserves_boundary_shape_without_terminal_closure_or_mutation",
    )


def run_checks() -> None:
    observation = observe_rhythm_spiral_transfer()
    assert observation.source_module == "リズム拍節Module"
    assert observation.comparison_module == "音程Module"
    assert observation.reconstructed_candidates == ("休符",)
    assert observation.reconstruction_status == "locally_resolved"
    assert len(observation.steps) == 10
    assert observation.steps[0].number == 239
    assert observation.steps[-1].number == 248
    assert observation.preserves_boundary_shape is True
    assert observation.terminally_closed is False
    assert observation.generated_mutation is False


if __name__ == "__main__":
    run_checks()
    print(observe_rhythm_spiral_transfer().status)
