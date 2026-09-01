# Music v0.2 検証記録：C6 / Am7 時間文脈実音化 最小ループ

*状態：DRAFT v0.1 / 関係重みプローブ後のcontext実音化*  
*実装：`10_Music_Validation/C6_Am7/music_v02_c6_am7_temporal_context_probe.py`*

## 0. 目的

前回の関係重みプローブでは、`context_support` を構造記述として持った。しかし音声生成では、`preceding_context` と `following_context` は鳴っていなかった。

今回は、contextをmanifest上の記述から、実際に時間上で鳴る前後関係へ移す。

```text
previous:
  context = 記述上の関係

this probe:
  context = preceding chord + identical target + following chord
```

## 1. 停止線

```text
同じtarget音響
  ≠ 同じ音楽状態

時間文脈を鳴らす
  ≠ 人間が必ずそう聞く

candidate classification
  ≠ 和音名の確定
```

今回も `actual_listening_observation = null` を維持する。

## 2. 境界B

```text
B_C6_Am7_temporal_context_probe:
  target_sonority = C3 E3 G3 A3
  target_is_identical_in_all_phrases = true
  variable_relations:
    preceding_chord
    following_chord
  observed_candidates:
    C6_candidate_by_temporal_context
    Am7_candidate_by_temporal_context
    C6_Am7_pivot_candidate
    Am7_pressure_with_C_reabsorption_candidate
```

ここで重要なのは、対象和音そのものは変えないことである。

## 3. Phrase設計

### 3.1 c_centered_frame

```text
C major arrival
↓
C3 E3 G3 A3  target identical
↓
C major continuation
```

構造予測：同一targetはC6側の安定候補として前景化する。

### 3.2 a_centered_frame

```text
A minor arrival
↓
C3 E3 G3 A3  target identical
↓
A minor continuation
```

構造予測：同一targetはAm7側の候補として利用可能になる。

### 3.3 c_to_a_pivot_frame

```text
C major arrival
↓
C3 E3 G3 A3  target identical
↓
A minor continuation
```

構造予測：同一targetはC6側からAm7側へのpivotとして働く。

### 3.4 a_to_c_resistance_frame

```text
A minor arrival
↓
C3 E3 G3 A3  target identical
↓
C major continuation
```

構造予測：Am7方向の期待は開くが、後続C文脈で再吸収される。

## 4. 生成artifact

```text
artifacts/audio/music_v02_c6_am7_temporal_context_probe.wav
artifacts/json/music_v02_c6_am7_temporal_context_probe.json
```

音声は次の順で鳴る。

```text
c_centered_frame
↓
a_centered_frame
↓
c_to_a_pivot_frame
↓
a_to_c_resistance_frame
```

各phraseは、前和音、同一target、後和音の三つからなる。

## 5. 今回のMusic上の意味

この検証では、C6 / Am7問題を「同一瞬間の音集合分類」から、時間的関係場の問題へ移す。

```text
same target sonority
+
different temporal frame
↓
different candidate state
```

これにより、C6 / Am7の差は単なるラベル選択ではなく、前後関係によってtargetの読まれ方が変わる現象として扱える。

## 6. 実聴取への接続

実聴取を入れる場合、次を分けて記録する。

```text
structural_prediction
perceptual_hypothesis
actual_listening_observation
E: discrepancy
H: M_Bで未吸収の差
θ: maintain / reorganize / Update判断
ξ: 有限Bに伴いなお残る未回収関係
```

今回の時点では、実聴取はまだ行わない。