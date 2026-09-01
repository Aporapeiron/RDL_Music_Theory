# Music v0.2 検証記録：C6 / Am7 関係重みプローブ 最小ループ

*状態：DRAFT v0.1 / C6-Am7介入分離後の関係圧比較*  
*実装：`10_Music_Validation/C6_Am7/music_v02_c6_am7_relation_weight_probe.py`*

## 0. 目的

前回の介入分離では、C6 / Am7の傾きが単一要因ではなく、`bass_relation`、`register_gravity`、`context_support` の組み合わせで変化することを記録した。

今回は、同一音集合 `{C,E,G,A}` を保存したまま、各関係がAm7方向へどれだけ構造圧を生むかを比較する。

ただし、ここでの重みは人間聴取の測定値ではない。

```text
relation weight probe
  = このB内での構造上の圧力比較
  ≠ 普遍的な和声重み
  ≠ 実聴取された強度
  ≠ C6 / Am7の最終正解
```

## 1. 境界B

```text
B_C6_Am7_relation_weight_probe:
  preserved_pitch_class_set = {C,E,G,A}
  observable_relations:
    bass_relation
    register_gravity
    preceding_context
    following_context
  comparison_axis:
    structural_pressure_to_am7
    c_center_resistance
```

ここで保存されるのは音集合であり、C6ラベルではない。

## 2. 関係ベクトル

この検証では、各状態に暫定的な `relation_vector` を与える。

```text
bass_relation:
  0 = C低音保持
  2 = A低音へ移動

register_gravity:
  -1 = C低音を強める
   0 = 元配置保持
   1 = A低音が重力を持つ

context_support:
  0 = C中心文脈
  1 = A方向が利用可能
  2 = A方向文脈が強い
```

この値はMusic構造比較のためのfixtureであり、聴取結果ではない。

## 3. 検証状態

### 3.1 source_C6_stable

```text
notes = C3 E3 G3 A3
bass = C
following_context = C-centered continuation expected
relation_vector = {0, 0, 0}
structural_pressure_to_am7 = 0
c_center_resistance = 3
classification = C6_candidate
```

### 3.2 context_only

```text
notes = C3 E3 G3 A3
bass = C
following_context = A-centered continuation becomes available
relation_vector = {0, 0, 1}
structural_pressure_to_am7 = 1
c_center_resistance = 3
classification = C6_candidate_with_Am7_pressure
```

文脈だけでは、響きの低音関係はまだC側に残る。

### 3.3 register_only

```text
notes = C2 E3 G3 A3
bass = C
following_context = C-centered continuation expected
relation_vector = {0, -1, 0}
structural_pressure_to_am7 = 0
c_center_resistance = 4
classification = C6_candidate
```

Cを下げる操作は、Am7方向ではなくC6側の重心を強める。

### 3.4 bass_only

```text
notes = A2 C3 E3 G3
bass = A
following_context = C-centered continuation expected
relation_vector = {2, 1, 0}
structural_pressure_to_am7 = 3
c_center_resistance = 2
classification = Am7_tilt_candidate
```

A低音はAm7方向の強い候補を作るが、C中心文脈が抵抗として残る。

### 3.5 bass_plus_context

```text
notes = A2 C3 E3 G3
bass = A
following_context = A-centered continuation becomes available
relation_vector = {2, 1, 1}
structural_pressure_to_am7 = 4
c_center_resistance = 1
classification = Am7_tilt_candidate
```

低音と後続文脈が揃うことで、Am7候補がより前景化する。

### 3.6 bass_plus_register

```text
notes = A2 C3 E3 G3
bass = A
following_context = C-centered continuation expected
relation_vector = {2, 1, 0}
structural_pressure_to_am7 = 3
c_center_resistance = 2
classification = Am7_tilt_candidate
```

このfixtureでは `bass_only` と同じ音響実体を持つ。したがって、`bass_plus_register` は独立音源というより、A低音が同時に register gravity を変えてしまうことを明示する観測名である。

## 4. 生成artifact

```text
source_C6_stable
↓
context_only
↓
register_only
↓
bass_only
↓
bass_plus_context
↓
bass_plus_register
↓
full_tilt
```

生成先：

```text
artifacts/audio/music_v02_c6_am7_relation_weight_probe.wav
artifacts/json/music_v02_c6_am7_relation_weight_probe.json
```

## 5. 実聴取slot

今回も `actual_listening_observation = null` として保持する。

```text
structural_pressure_to_am7
  ≠ perceptual strength
  ≠ actual listening observation
```

実聴取で不一致が出た場合は、まず `E: discrepancy` として記録する。M_Bで未吸収の差はHへ、有限Bに伴いなお未回収の関係が残る場合だけξへ送る。

## 6. ここで見えたMusic側の仮説

```text
context_only:
  Am7方向の可能性は増えるが、低音がCのままならC6候補は崩れにくい。

register_only:
  C低音を強めると、Am7方向ではなくC6側の安定が増す。

bass_only:
  A低音はC6/Am7関係配置を大きく動かす。

bass_plus_context:
  A低音とA方向文脈が揃うと、Am7候補がより強くなる。

full_tilt:
  bass / register / contextが揃い、Am7方向候補がもっとも強い。
```

## 7. 停止線

```text
structural_pressure_score_is_not_actual_hearing_strength
classification_is_candidate_not_chord_truth
relation_weight_is_contextual_not_universal_constant
actual_listening_observation_remains_null_until_recorded
```

このプローブは、C6 / Am7の答えを決めるためではなく、同じ材料を保ったまま関係配置のどこが状態を動かすかを見るためのMusic検証である。