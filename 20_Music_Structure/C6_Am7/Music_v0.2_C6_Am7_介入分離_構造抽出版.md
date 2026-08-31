# Music v0.2 C6 / Am7 介入分離 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/C6_Am7/Music_v0.2_C6_Am7_介入分離_最小ループ.md
10_Music_Validation/C6_Am7/music_v02_c6_am7_intervention_separation.py
artifacts/audio/music_v02_c6_am7_intervention_separation.wav
artifacts/json/music_v02_c6_am7_intervention_separation.json
```

この抽出は、C6 / Am7の状態遷移を単一原因へ圧縮しないためのMusic構造抽出である。

---

## 1. 保存されたもの

全caseで次を保存する。

```text
pitch_class_set = {C,E,G,A}
```

保存されるのは材料であり、C6ラベルでもAm7ラベルでもない。

---

## 2. 分離した介入軸

```text
context_only:
  primary_intervention = following_context
  residual_changes = none

register_only:
  primary_intervention = register_gravity
  residual_changes = none

bass_primary:
  primary_intervention = bass_relation
  residual_changes = register_gravity residual

full_tilt:
  primary_intervention = bass_register_context_bundle
  residual_changes = none
```

重要なのは、音響実現では介入が完全に純粋でない場合があることを、失敗ではなく `residual_changes` として保持する点である。

---

## 3. 状態候補の勾配

```text
source:
  C6_candidate

context_only:
  C6_candidate_with_Am7_context_pressure

register_only:
  C6_candidate

bass_primary:
  Am7_candidate_by_bass_relation

full_tilt:
  Am7_candidate_with_context_support
```

ここでは、C6 / Am7を二値判定しない。

```text
C6
  ↓ context pressure
C6 with Am7 pressure
  ↓ bass intervention
Am7 candidate with C-memory
  ↓ bass + register + context support
Am7 candidate with stronger support
```

---

## 4. Music Core v0.2への返却

この検証から返す構造は次である。

```text
preserved material
  + primary intervention axis
  + residual change record
  + structural prediction
  + perceptual hypothesis
  + actual observation slot
```

これにより、Music側では次を分けられる。

```text
同じ材料が残った
どの関係を主に動かした
どの副作用が出た
どの候補が前景化した
人間聴取はまだ確認されたか
```

---

## 5. 停止線

この抽出では次を行わない。

```text
C6 / Am7の正解を決める
contextだけで人間聴取が変わったと断定する
bass介入を純粋なbass-only変化と偽装する
structural predictionをactual listening observationへ昇格する
T2 Runtime mechanismを追加する
```