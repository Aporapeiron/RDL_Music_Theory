# Music v0.2 C6 / Am7 関係重みプローブ 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/C6_Am7/Music_v0.2_C6_Am7_関係重みプローブ_最小ループ.md
10_Music_Validation/C6_Am7/music_v02_c6_am7_relation_weight_probe.py
artifacts/json/music_v02_c6_am7_relation_weight_probe.json
```

## 1. 抽出主題

同一音集合 `{C,E,G,A}` を保存しても、C6 / Am7の候補状態は同一ではない。

今回抽出するのは、次の関係である。

```text
pitch-class preservation
+
bass relation
+
register gravity
+
context support
+
C-centered resistance
↓
C6 / Am7 state pressure
```

## 2. Music構造

```text
preserved:
  pitch_class_set:{C,E,G,A}

varied:
  bass_relation
  register_gravity
  preceding_context
  following_context

observed:
  structural_pressure_to_am7
  c_center_resistance
  candidate_classification
```

ここでの `candidate_classification` は、和音名の真理値ではなく、現在Bでの状態候補である。

## 3. 状態配置

```text
source_C6_stable:
  pressure_to_am7 = 0
  c_resistance = 3
  classification = C6_candidate

context_only:
  pressure_to_am7 = 1
  c_resistance = 3
  classification = C6_candidate_with_Am7_pressure

register_only:
  pressure_to_am7 = 0
  c_resistance = 4
  classification = C6_candidate

bass_only:
  pressure_to_am7 = 3
  c_resistance = 2
  classification = Am7_tilt_candidate

bass_plus_context:
  pressure_to_am7 = 4
  c_resistance = 1
  classification = Am7_tilt_candidate

full_tilt:
  pressure_to_am7 = 5
  c_resistance = 1
  classification = Am7_candidate_strong
```

## 4. 抽出された差

### 4.1 context support

```text
context_only
  changed = following_context
  pressure_to_am7 = 1
```

文脈はAm7方向の可能性を開くが、低音関係がCのままなら状態全体を単独でAm7へ反転させない。

### 4.2 register gravity

```text
register_only
  changed = lower C register
  pressure_to_am7 = 0
  c_resistance = 4
```

registerは単独でAm7方向へ働くとは限らない。どの音が重力を持つかによって、むしろC6側を強める。

### 4.3 bass relation

```text
bass_only
  changed = bass C -> A
  pressure_to_am7 = 3
```

同じ音集合であっても、低音関係は候補状態を大きく動かす。

### 4.4 relation bundle

```text
bass_plus_context / full_tilt
  bass_relation + register_gravity + context_support
  pressure_to_am7 = 4..5
```

C6 / Am7の傾きは単一操作ではなく、複数関係が同方向へ揃ったときに強くなる。

## 5. Music Core v0.2への戻り

この検証から、Music Core側へ返すべき最小命題は次である。

```text
同一音集合の保存
  ≠ 同一和声状態の保存

和声状態候補は、少なくとも
  bass_relation
  register_gravity
  context_support
  history / memory
の配置差によって変わる。
```

特に重要なのは、`register_gravity` が常にAm7方向の補助とは限らないことである。Cを低く置けばC6側を強め、Aを低く置けばAm7側を強める。

## 6. 未確定領域

```text
structural_pressure_to_am7
  ≠ 実聴取上のAm7感

c_center_resistance
  ≠ 人間がCを聞き続けた証拠

candidate_classification
  ≠ 和音名の確定
```

人間聴取による確認は、別途 `actual_listening_observation` として記録される。

## 7. 次のMusic実験候補

```text
1. 実聴取を入れて pressure / resistance と聴こえのズレを記録する。
2. C6 / Am7と同じ方式で、sus4 / add11 の同一音素材近傍へ移す。
3. 和声だけでなく、同一旋律輪郭を保存した拍節変更へ進む。
```

この抽出はT2側の汎用状態機械ではなく、Music側の「保存された材料と変化した関係が聴こえ候補をどう動かすか」を扱う。