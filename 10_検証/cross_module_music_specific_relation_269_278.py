"""四Moduleの音楽的固有性どうしの関係を観測する最小検証。"""

from dataclasses import dataclass

from cross_module_spiral_difference_259_268 import (
    observe_cross_module_spiral_difference,
)


@dataclass(frozen=True)
class MusicSpecificRelation:
    number: int
    relation_kind: str
    source_module: str
    source_boundary: str
    target_module: str
    target_boundary: str
    music_specific_reading: str
    collapses_difference: bool


@dataclass(frozen=True)
class MusicSpecificRelationObservation:
    compared_modules: tuple[str, ...]
    source_status: str
    relations: tuple[MusicSpecificRelation, ...]
    relation_kinds: tuple[str, ...]
    preserves_music_subject: bool
    collapses_to_common_vocabulary: bool
    generated_mutation: bool
    status: str


RELATIONS = (
    MusicSpecificRelation(
        number=269,
        relation_kind="connection",
        source_module="音高調律Module",
        source_boundary="physical relation and tuning category do not become pitch name",
        target_module="音程Module",
        target_boundary="spelling-aware interval label and target-context separation",
        music_specific_reading="調律の12TETカテゴリーは、音程の綴り境界へ渡されても音程名に自動昇格しない",
        collapses_difference=False,
    ),
    MusicSpecificRelation(
        number=270,
        relation_kind="connection",
        source_module="音程Module",
        source_boundary="spelling-aware interval label and target-context separation",
        target_module="和声機能Module",
        target_boundary="function annotation does not generate target by itself",
        music_specific_reading="音程のtarget/context分離は、和声機能のtarget候補境界へ接続してもfunction生成器にはならない",
        collapses_difference=False,
    ),
    MusicSpecificRelation(
        number=271,
        relation_kind="interference",
        source_module="和声機能Module",
        source_boundary="function annotation does not generate target by itself",
        target_module="リズム拍節Module",
        target_boundary="grid reopen changes candidate space without becoming realization",
        music_specific_reading="和声機能のhistory依存target候補は、リズムの履歴投影と比較できるが同じ履歴軸へ潰せない",
        collapses_difference=False,
    ),
    MusicSpecificRelation(
        number=272,
        relation_kind="complement",
        source_module="リズム拍節Module",
        source_boundary="grid reopen changes candidate space without becoming realization",
        target_module="和声機能Module",
        target_boundary="function annotation does not generate target by itself",
        music_specific_reading="リズムの候補空間変更は、和声target選択の時間的位置づけを補うが機能注釈そのものではない",
        collapses_difference=False,
    ),
    MusicSpecificRelation(
        number=273,
        relation_kind="non_identity",
        source_module="音高調律Module",
        source_boundary="physical relation and tuning category do not become pitch name",
        target_module="和声機能Module",
        target_boundary="function annotation does not generate target by itself",
        music_specific_reading="物理比や調律カテゴリーは、和声機能候補の根拠入力にはなり得るが機能語彙とは同一でない",
        collapses_difference=False,
    ),
    MusicSpecificRelation(
        number=274,
        relation_kind="non_identity",
        source_module="リズム拍節Module",
        source_boundary="grid reopen changes candidate space without becoming realization",
        target_module="音程Module",
        target_boundary="spelling-aware interval label and target-context separation",
        music_specific_reading="リズムのgrid境界と音程の綴り境界は、どちらもB差を持つが同じ境界型にはしない",
        collapses_difference=False,
    ),
    MusicSpecificRelation(
        number=275,
        relation_kind="difference_origin_check",
        source_module="音程Module",
        source_boundary="B差 + Gamma差 + 音楽的固有性",
        target_module="音高調律Module",
        target_boundary="B差 + Gamma差 + 音楽的固有性",
        music_specific_reading="同じB差+Gamma差でも、音程では綴りとquality、調律では物理比と離散化の差として現れる",
        collapses_difference=False,
    ),
    MusicSpecificRelation(
        number=276,
        relation_kind="difference_origin_check",
        source_module="和声機能Module",
        source_boundary="Gamma差 + controller差 + 音楽的固有性",
        target_module="リズム拍節Module",
        target_boundary="B差 + 実装差 + 音楽的固有性",
        music_specific_reading="和声機能のcontroller差とリズムの実装差は、どちらも選択前の停止線だが由来を同一視しない",
        collapses_difference=False,
    ),
    MusicSpecificRelation(
        number=277,
        relation_kind="music_subject_check",
        source_module="四Module比較",
        source_boundary="music-specific differences",
        target_module="RDL Music Theory",
        target_boundary="music subject preservation",
        music_specific_reading="共通骨格ではなく、音楽領域間の接続・干渉・補完・非同一性を主対象として保持する",
        collapses_difference=False,
    ),
    MusicSpecificRelation(
        number=278,
        relation_kind="next_verification_target",
        source_module="RDL Music Theory",
        source_boundary="music-specific relation map",
        target_module="次検証",
        target_boundary="module-pair relation stress test",
        music_specific_reading="次は一つのModule対を選び、接続が差異を保存したまま実データ列を通れるかを見る",
        collapses_difference=False,
    ),
)


def observe_music_specific_relations() -> MusicSpecificRelationObservation:
    difference = observe_cross_module_spiral_difference()
    relation_kinds = tuple(dict.fromkeys(relation.relation_kind for relation in RELATIONS))
    return MusicSpecificRelationObservation(
        compared_modules=difference.compared_modules,
        source_status=difference.status,
        relations=RELATIONS,
        relation_kinds=relation_kinds,
        preserves_music_subject=True,
        collapses_to_common_vocabulary=any(
            relation.collapses_difference for relation in RELATIONS
        ),
        generated_mutation=False,
        status="cross_module_music_specific_relation_269_278_observed_without_collapsing_module_differences",
    )


def run_checks() -> None:
    observation = observe_music_specific_relations()
    assert observation.compared_modules == (
        "音程Module",
        "和声機能Module",
        "リズム拍節Module",
        "音高調律Module",
    )
    assert observation.source_status == (
        "cross_module_spiral_difference_259_268_observed_without_collapsing_music_specific_boundaries"
    )
    assert len(observation.relations) == 10
    assert observation.relations[0].number == 269
    assert observation.relations[-1].number == 278
    assert observation.relation_kinds == (
        "connection",
        "interference",
        "complement",
        "non_identity",
        "difference_origin_check",
        "music_subject_check",
        "next_verification_target",
    )
    assert observation.preserves_music_subject is True
    assert observation.collapses_to_common_vocabulary is False
    assert observation.generated_mutation is False
    assert all(not relation.collapses_difference for relation in observation.relations)


if __name__ == "__main__":
    run_checks()
    print(observe_music_specific_relations().status)
