"""四Moduleの音楽的固有差から相互作用面を観測する最小検証。"""

from dataclasses import dataclass

from cross_module_music_specific_relation_269_278 import (
    observe_music_specific_relations,
)


@dataclass(frozen=True)
class InteractionSurface:
    number: int
    surface_kind: str
    modules: tuple[str, ...]
    relation_numbers: tuple[int, ...]
    interaction_reading: str
    requires_unified_module: bool
    collapses_module_difference: bool


@dataclass(frozen=True)
class InteractionSurfaceObservation:
    source_status: str
    compared_modules: tuple[str, ...]
    surfaces: tuple[InteractionSurface, ...]
    surface_kinds: tuple[str, ...]
    preserves_music_subject: bool
    treats_interaction_as_unification: bool
    generated_mutation: bool
    status: str


SURFACES = (
    InteractionSurface(
        number=279,
        surface_kind="directed_relation",
        modules=("音高調律Module", "音程Module"),
        relation_numbers=(269,),
        interaction_reading="調律カテゴリーは音程の綴り境界へ向かうが、音程名の確定は返さない",
        requires_unified_module=False,
        collapses_module_difference=False,
    ),
    InteractionSurface(
        number=280,
        surface_kind="directed_relation",
        modules=("音程Module", "和声機能Module"),
        relation_numbers=(270,),
        interaction_reading="音程のtarget/context分離は和声target境界へ向かうが、function annotationを生成しない",
        requires_unified_module=False,
        collapses_module_difference=False,
    ),
    InteractionSurface(
        number=281,
        surface_kind="mutual_constraint",
        modules=("和声機能Module", "リズム拍節Module"),
        relation_numbers=(271, 272),
        interaction_reading="和声historyとリズム履歴投影は互いに検査条件を変えるが、共通履歴軸にはならない",
        requires_unified_module=False,
        collapses_module_difference=False,
    ),
    InteractionSurface(
        number=282,
        surface_kind="asymmetric_dependency",
        modules=("リズム拍節Module", "和声機能Module"),
        relation_numbers=(272,),
        interaction_reading="リズムの候補空間変更は和声target選択の時間的位置を支えるが、和声機能からリズム実現は決まらない",
        requires_unified_module=False,
        collapses_module_difference=False,
    ),
    InteractionSurface(
        number=283,
        surface_kind="non_confluent_interaction",
        modules=("音高調律Module", "和声機能Module"),
        relation_numbers=(273,),
        interaction_reading="物理比・調律カテゴリーと機能語彙は同じ候補へ合流せず、根拠入力と文脈注釈に分かれる",
        requires_unified_module=False,
        collapses_module_difference=False,
    ),
    InteractionSurface(
        number=284,
        surface_kind="non_confluent_interaction",
        modules=("リズム拍節Module", "音程Module"),
        relation_numbers=(274,),
        interaction_reading="grid境界と綴り境界はいずれもB差を持つが、時間配置と記述綴りの別相として残る",
        requires_unified_module=False,
        collapses_module_difference=False,
    ),
    InteractionSurface(
        number=285,
        surface_kind="shared_origin_different_realization",
        modules=("音程Module", "音高調律Module"),
        relation_numbers=(275,),
        interaction_reading="同じB差+Gamma差でも、音程では綴り・quality、調律では物理比・離散化として実現される",
        requires_unified_module=False,
        collapses_module_difference=False,
    ),
    InteractionSurface(
        number=286,
        surface_kind="shared_stop_line_different_origin",
        modules=("和声機能Module", "リズム拍節Module"),
        relation_numbers=(276,),
        interaction_reading="どちらも選択前に停止線を持つが、和声はcontroller差、リズムは境界再構成の実装差として現れる",
        requires_unified_module=False,
        collapses_module_difference=False,
    ),
    InteractionSurface(
        number=287,
        surface_kind="music_subject_preservation",
        modules=("四Module比較", "RDL Music Theory"),
        relation_numbers=(277,),
        interaction_reading="相互作用面を扱っても、主語は共通Coreではなく音楽領域間の関係に置く",
        requires_unified_module=False,
        collapses_module_difference=False,
    ),
    InteractionSurface(
        number=288,
        surface_kind="next_stress_test_selection",
        modules=("RDL Music Theory", "次検証"),
        relation_numbers=(278,),
        interaction_reading="次は音高調律→音程、または音程→和声機能の片方向接続を実データ列でstress testする",
        requires_unified_module=False,
        collapses_module_difference=False,
    ),
)


def observe_interaction_surfaces() -> InteractionSurfaceObservation:
    relation_observation = observe_music_specific_relations()
    relation_numbers = {relation.number for relation in relation_observation.relations}
    assert all(
        number in relation_numbers
        for surface in SURFACES
        for number in surface.relation_numbers
    )
    surface_kinds = tuple(dict.fromkeys(surface.surface_kind for surface in SURFACES))
    return InteractionSurfaceObservation(
        source_status=relation_observation.status,
        compared_modules=relation_observation.compared_modules,
        surfaces=SURFACES,
        surface_kinds=surface_kinds,
        preserves_music_subject=relation_observation.preserves_music_subject,
        treats_interaction_as_unification=any(
            surface.requires_unified_module or surface.collapses_module_difference
            for surface in SURFACES
        ),
        generated_mutation=False,
        status="cross_module_interaction_surface_279_288_observed_without_unifying_music_domains",
    )


def run_checks() -> None:
    observation = observe_interaction_surfaces()
    assert observation.source_status == (
        "cross_module_music_specific_relation_269_278_observed_without_collapsing_module_differences"
    )
    assert observation.compared_modules == (
        "音程Module",
        "和声機能Module",
        "リズム拍節Module",
        "音高調律Module",
    )
    assert len(observation.surfaces) == 10
    assert observation.surfaces[0].number == 279
    assert observation.surfaces[-1].number == 288
    assert observation.surface_kinds == (
        "directed_relation",
        "mutual_constraint",
        "asymmetric_dependency",
        "non_confluent_interaction",
        "shared_origin_different_realization",
        "shared_stop_line_different_origin",
        "music_subject_preservation",
        "next_stress_test_selection",
    )
    assert observation.preserves_music_subject is True
    assert observation.treats_interaction_as_unification is False
    assert observation.generated_mutation is False
    assert all(not surface.requires_unified_module for surface in observation.surfaces)
    assert all(not surface.collapses_module_difference for surface in observation.surfaces)


if __name__ == "__main__":
    run_checks()
    print(observe_interaction_surfaces().status)
