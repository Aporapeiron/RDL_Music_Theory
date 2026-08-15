# 検証記録：音程Module・concrete voice leadingとnext context候補境界

*対象：concrete voice leading observationが、外部next context inventoryとGammaによってnext context candidate setへ接続される条件*  
*状態：DRAFT v0.1 / 78 concrete voice leading境界後のnext context候補最小検証*  
*実装：`10_検証/interval_module_next_context_candidate_boundary.py`*

---

## ■ 0. 検証目的

78では、voice leading request candidateに外部realization boundaryと`Gamma_voice_leading_realization`を与えた場合だけconcrete voice leading observationが生じることを確認した。

80では、そのconcrete voice leading observationを固定し、外部next context inventoryと`Gamma_next_context_candidate_filter`を与えた場合だけnext context candidate set observedが生じることを確認する。

```text
concrete voice leading observation
  + external next context inventory
  + Gamma_next_context_candidate_filter_fixture
  ↓
next context candidate set observed
  ↓
selected next context は未生成
```

ここで重要なのは、concrete voice leadingからnext context候補集合を自動生成しないことである。候補inventoryは外部入力として与える。

---

## ■ 1. 固定するconcrete voice leading

78で得たfixture用のconcrete voice leading observationを使う。

```text
concrete voice leading:
  lower_pitch = C4
  upper_pitch = G4
  lower_motion = 0
  upper_motion = 0
```

これは具体声部進行観測であり、まだnext context候補集合ではない。

---

## ■ 2. 外部next context inventory

今回はnext context候補を外部inventoryとして与える。

```text
external next context inventory:
  C major continuation
  G major reinterpretation
  A minor reinterpretation
```

このinventoryはconcrete voice leadingから自動生成されたものではない。

---

## ■ 3. 暫定結論

80では、concrete voice leading observationだけではnext context candidate setは生じず、外部next context inventoryと`Gamma_next_context_candidate_filter`を与えた場合だけnext context candidate set observedが生じることを確認する。

ただし、

```text
next context candidate set observed
  ≠ selected next context
  ≠ harmonic function
  ≠ Core昇格
```

で停止する。
