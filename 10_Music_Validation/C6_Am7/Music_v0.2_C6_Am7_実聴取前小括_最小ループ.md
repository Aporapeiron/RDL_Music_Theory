# Music v0.2 検証記録：C6 / Am7 実聴取前小括 最小ループ

*状態：DRAFT v0.1 / 時間文脈提示順序分離後のpre-listening closure*  
*実装：`10_Music_Validation/C6_Am7/music_v02_c6_am7_pre_listening_closure.py`*

## 0. 目的

C6 / Am7題材では、これまで次を行った。

```text
基本生成
↓
介入分離
↓
関係重み仮説fixture
↓
時間文脈実音化
↓
提示順序分離
```

ただし、すべての実聴取slotはまだ `actual_listening_observation = null` である。

今回は、実聴取前でもMusic Core v0.2へ返せる命題と、実聴取後でないと返してはいけない命題を分ける。

## 1. 入力manifest

```text
artifacts/json/music_v02_c6_am7_rehearing_observation.json
artifacts/json/music_v02_c6_am7_intervention_separation.json
artifacts/json/music_v02_c6_am7_relation_weight_probe.json
artifacts/json/music_v02_c6_am7_temporal_context_probe.json
artifacts/json/music_v02_c6_am7_temporal_context_order_split.json
```

## 2. 実聴取前に返せる命題

```text
pitch_class_set_preservation_does_not_preserve_harmonic_state
bass_relation_can_rebase_the_same_material_toward_Am7
register_gravity_depends_on_which_pitch_receives_low_support
context_must_be_distinguished_as_score_fixture_and_temporal_audio_relation
identical_target_sonority_can_have_different_candidate_states_under_different_temporal_frames
presentation_order_memory_is_a_separate_listening_condition_from_phrase_internal_context
```

これらは、人間が実際にどう聞いたかではなく、Music側の生成・構造fixtureとして返せる。

## 3. 実聴取まで保留する命題

```text
whether_listener_hears_C6_or_Am7_in_each_fixture
whether_pivot_reinterpretation_occurs_at_target_or_after_following_chord
whether_order_variants_change perceived candidate strength
whether_structural_prediction_discrepancies_are_absorbed_by_current_M_B_or_remain_as_H
whether_any_residual_relation_after_finite_B_should_be_held_as_xi
```

これらは、actual listening observationなしにCore命題へ昇格しない。

## 4. Coreへ返さないもの

```text
relation_weight_numbers_as_universal_constants
candidate_classification_as_final_chord_truth
device_audio_generation_as_human_listening_confirmation
C6_Am7_problem_as_resolved_binary_label_choice
```

特に `candidate_classification` は、和音名の真理値ではなく、現在B内の状態候補である。

## 5. 生成artifact

```text
artifacts/json/music_v02_c6_am7_pre_listening_closure.json
```

このmanifestは、C6 / Am7題材を実聴取前に一区切りするための索引である。

## 6. 次のMusic本線

C6 / Am7は、実聴取slotを開いたまま一旦閉じる。

次に進む対象候補は、旋律と拍節である。

```text
melody contour preservation
+
meter / accent displacement
↓
identity retained or reinterpreted
```

C6 / Am7で得た中心命題、つまり「材料保存と音楽状態保存は同一ではない」を、和声から旋律×拍節へ移す。