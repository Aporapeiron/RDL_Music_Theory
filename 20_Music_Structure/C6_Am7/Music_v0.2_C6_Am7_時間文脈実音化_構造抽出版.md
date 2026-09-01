# Music v0.2 C6 / Am7 時間文脈実音化 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/C6_Am7/Music_v0.2_C6_Am7_時間文脈実音化_最小ループ.md
10_Music_Validation/C6_Am7/music_v02_c6_am7_temporal_context_probe.py
artifacts/json/music_v02_c6_am7_temporal_context_probe.json
```

## 1. 抽出主題

今回抽出するのは、`target` の物理的同一性と、時間的文脈同一性の非同一性である。

```text
same target:
  C3 E3 G3 A3

variable frame:
  preceding chord
  following chord

result:
  different candidate state
```

## 2. 保存されるもの

```text
preserved_target_sonority:
  C3 E3 G3 A3

target_is_identical_in_all_phrases:
  true
```

これにより、今回の差はtarget内部の音集合差ではなく、前後関係差として扱える。

## 3. 変化するもの

```text
c_centered_frame:
  C major arrival -> target -> C major continuation

a_centered_frame:
  A minor arrival -> target -> A minor continuation

c_to_a_pivot_frame:
  C major arrival -> target -> A minor continuation

a_to_c_resistance_frame:
  A minor arrival -> target -> C major continuation
```

## 4. 候補状態

```text
c_centered_frame:
  C6_candidate_by_temporal_context

a_centered_frame:
  Am7_candidate_by_temporal_context

c_to_a_pivot_frame:
  C6_Am7_pivot_candidate

a_to_c_resistance_frame:
  Am7_pressure_with_C_reabsorption_candidate
```

ここでは、同じ `C3 E3 G3 A3` targetが、異なる時間文脈で別候補として読まれる。

## 5. Music Core v0.2へ返す命題

```text
瞬間的音響材料の保存
  ≠ 音楽状態の保存

同一targetは、前後文脈によって
  C6安定候補
  Am7候補
  pivot候補
  再吸収候補
へ分岐しうる。
```

これは、RDL Musicが扱うべき「関係配置としての音楽状態」の中心例である。

## 6. 関係重みプローブとの接続

前回の関係重みプローブでは、`context_support` は数値fixtureとして置かれていた。

今回の実音化により、少なくとも次が分かれた。

```text
context_support_as_score
  = 構造仮説fixture

context_as_temporal_audio
  = 前後和音として鳴る関係場
```

したがって、今後は重み数値を増やす前に、時間文脈として鳴った関係を実聴取slotへ接続する。

## 7. 停止線

```text
target_sonority_identity_is_not_context_identity
temporal_context_is_realized_in_audio_not_only_manifest_text
structural_prediction_is_not_actual_human_listening
candidate_classification_is_not_final_chord_truth
```

この抽出は、C6 / Am7の正解判定ではなく、同じtargetが時間的関係場によって別状態候補へ分岐することを保持する。