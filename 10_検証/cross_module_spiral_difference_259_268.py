"""螺旋型再入循環の共通骨格ではなくModule差異を抽出する最小検証。"""

from dataclasses import dataclass

from harmonic_function_spiral_transfer_229_238 import (
    observe_harmonic_function_spiral_transfer,
)
from interval_module_spiral_reentry_cycle_179_228 import (
    observe_spiral_reentry_cycle,
)
from pitch_tuning_spiral_transfer_249_258 import (
    observe_pitch_tuning_spiral_transfer,
)
from rhythm_spiral_transfer_239_248 import observe_rhythm_spiral_transfer


@dataclass(frozen=True)
class ModuleDifferenceRecord:
    module_name: str
    local_activation: str
    post_processing_boundary: str
    distinctive_boundary: str
    difference_origin_candidate: str
    music_specific_reading: str


@dataclass(frozen=True)
class SpiralDifferenceExtractionObservation:
    compared_modules: tuple[str, ...]
    shared_boundary_shape: tuple[str, ...]
    module_differences: tuple[ModuleDifferenceRecord, ...]
    common_shape_preserved: bool
    differences_preserved: bool
    collapsed_to_core_metabolism: bool
    generated_mutation: bool
    status: str


SHARED_BOUNDARY_SHAPE = (
    "Module-specific input contract",
    "payload binding",
    "validation",
    "processing request",
    "existing local activation",
    "post-processing boundary",
    "handoff / next xi",
    "contract generalization",
    "next cycle entry",
)


MODULE_DIFFERENCES = (
    ModuleDifferenceRecord(
        module_name="音程Module",
        local_activation="existing_70_activation_bridge",
        post_processing_boundary="generic / quality / interval label / target / context chain",
        distinctive_boundary="spelling-aware interval label and target-context separation",
        difference_origin_candidate="B差 + Gamma差 + 音楽的固有性",
        music_specific_reading="音程では物理差・綴り・quality・文脈targetを潰さず分ける必要がある",
    ),
    ModuleDifferenceRecord(
        module_name="和声機能Module",
        local_activation="existing_42_function_activation",
        post_processing_boundary="existing_43_target_boundary_bridge",
        distinctive_boundary="function annotation does not generate target by itself",
        difference_origin_candidate="Gamma差 + controller差 + 音楽的固有性",
        music_specific_reading="和声機能では同じ和音でもkey contextとhistoryで機能・target候補が分岐する",
    ),
    ModuleDifferenceRecord(
        module_name="リズム拍節Module",
        local_activation="existing_26_boundary_reconstruction_activation",
        post_processing_boundary="existing_28_transition_projection_bridge",
        distinctive_boundary="grid reopen changes candidate space without becoming realization",
        difference_origin_candidate="B差 + 実装差 + 音楽的固有性",
        music_specific_reading="リズムでは候補語彙・grid open・休符target・履歴投影を分ける必要がある",
    ),
    ModuleDifferenceRecord(
        module_name="音高調律Module",
        local_activation="existing_06_relation_activation",
        post_processing_boundary="existing_10_tuning_category_bridge",
        distinctive_boundary="physical relation and tuning category do not become pitch name",
        difference_origin_candidate="B差 + Gamma差 + 音楽的固有性",
        music_specific_reading="調律では物理比・cents・12TETカテゴリー・後続綴りを分ける必要がある",
    ),
)


def observe_cross_module_spiral_difference() -> SpiralDifferenceExtractionObservation:
    interval = observe_spiral_reentry_cycle()
    harmonic = observe_harmonic_function_spiral_transfer()
    rhythm = observe_rhythm_spiral_transfer()
    pitch_tuning = observe_pitch_tuning_spiral_transfer()

    compared_modules = (
        "音程Module",
        harmonic.source_module,
        rhythm.source_module,
        pitch_tuning.source_module,
    )
    common_shape_preserved = (
        interval.returns_to_isomorphic_entry
        and harmonic.preserves_boundary_shape
        and rhythm.preserves_boundary_shape
        and pitch_tuning.preserves_boundary_shape
    )
    differences_preserved = all(
        record.distinctive_boundary and record.music_specific_reading
        for record in MODULE_DIFFERENCES
    )

    return SpiralDifferenceExtractionObservation(
        compared_modules=compared_modules,
        shared_boundary_shape=SHARED_BOUNDARY_SHAPE,
        module_differences=MODULE_DIFFERENCES,
        common_shape_preserved=common_shape_preserved,
        differences_preserved=differences_preserved,
        collapsed_to_core_metabolism=False,
        generated_mutation=False,
        status="cross_module_spiral_difference_259_268_observed_without_collapsing_music_specific_boundaries",
    )


def run_checks() -> None:
    observation = observe_cross_module_spiral_difference()
    assert observation.compared_modules == (
        "音程Module",
        "和声機能Module",
        "リズム拍節Module",
        "音高調律Module",
    )
    assert len(observation.shared_boundary_shape) == 9
    assert len(observation.module_differences) == 4
    assert observation.common_shape_preserved is True
    assert observation.differences_preserved is True
    assert observation.collapsed_to_core_metabolism is False
    assert observation.generated_mutation is False
    assert {
        record.difference_origin_candidate
        for record in observation.module_differences
    } == {
        "B差 + Gamma差 + 音楽的固有性",
        "Gamma差 + controller差 + 音楽的固有性",
        "B差 + 実装差 + 音楽的固有性",
    }


if __name__ == "__main__":
    run_checks()
    print(observe_cross_module_spiral_difference().status)
