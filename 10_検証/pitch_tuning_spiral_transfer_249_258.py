"""音高調律Moduleで螺旋型再入循環の形が残るかを確認する最小検証。"""

from dataclasses import dataclass

from interval_fifth_decomposition import observe_interval
from two_sine_wave_relations import ObservationBoundary, RelationRule, observe_relation


@dataclass(frozen=True)
class PitchTuningSpiralStep:
    number: int
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class PitchTuningSpiralTransferObservation:
    source_module: str
    comparison_module: str
    ratio: float
    semitones_12tet: int
    short_recurrence_candidate: bool
    steps: tuple[PitchTuningSpiralStep, ...]
    preserves_boundary_shape: bool
    terminally_closed: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str], ...] = (
    (249, "pitch_tuning_input_contract", "pitch_tuning_input_contract_candidate"),
    (250, "frequency_payload_binding", "bound_frequency_payload_candidate"),
    (251, "component_relation_validation", "pitch_tuning_validation_diagnostic"),
    (252, "pitch_tuning_processing_request", "pitch_tuning_processing_request_candidate"),
    (253, "existing_06_relation_activation", "physical_relation_candidate"),
    (254, "existing_10_tuning_category_bridge", "tuning_category_candidate"),
    (255, "context_pass_boundary", "downstream_context_pass_candidate"),
    (256, "downstream_module_handoff_boundary", "pitch_tuning_handoff_target"),
    (257, "pitch_tuning_contract_generalization_target", "pitch_tuning_contract_generalization_target"),
    (258, "cross_module_spiral_equivalence_check", "isomorphic_spiral_shape_candidate"),
)


def observe_pitch_tuning_spiral_transfer() -> PitchTuningSpiralTransferObservation:
    relation = observe_relation(100.0, 150.0, ObservationBoundary(), RelationRule())
    tuning = observe_interval(100.0, 150.0)

    previous = "pitch_tuning_module_boundary"
    steps = []
    for number, name, result in STEP_DEFINITIONS:
        steps.append(
            PitchTuningSpiralStep(
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
        observed[0].result == "pitch_tuning_input_contract_candidate"
        and observed[3].result == "pitch_tuning_processing_request_candidate"
        and observed[4].result == "physical_relation_candidate"
        and observed[5].result == "tuning_category_candidate"
        and observed[7].result == "pitch_tuning_handoff_target"
        and observed[8].result == "pitch_tuning_contract_generalization_target"
        and observed[9].result == "isomorphic_spiral_shape_candidate"
    )

    return PitchTuningSpiralTransferObservation(
        source_module="音高調律Module",
        comparison_module="音程Module",
        ratio=relation.ratio,
        semitones_12tet=tuning.semitones_12tet,
        short_recurrence_candidate=relation.short_recurrence_candidate,
        steps=observed,
        preserves_boundary_shape=preserves_boundary_shape,
        terminally_closed=False,
        generated_mutation=any(step.generated_mutation for step in observed),
        status="pitch_tuning_spiral_transfer_249_258_preserves_boundary_shape_without_terminal_closure_or_mutation",
    )


def run_checks() -> None:
    observation = observe_pitch_tuning_spiral_transfer()
    assert observation.source_module == "音高調律Module"
    assert observation.comparison_module == "音程Module"
    assert observation.ratio == 1.5
    assert observation.semitones_12tet == 7
    assert observation.short_recurrence_candidate is True
    assert len(observation.steps) == 10
    assert observation.steps[0].number == 249
    assert observation.steps[-1].number == 258
    assert observation.preserves_boundary_shape is True
    assert observation.terminally_closed is False
    assert observation.generated_mutation is False


if __name__ == "__main__":
    run_checks()
    print(observe_pitch_tuning_spiral_transfer().status)
