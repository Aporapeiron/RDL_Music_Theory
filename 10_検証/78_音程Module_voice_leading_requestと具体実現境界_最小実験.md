# 検証記録：音程Module・voice leading requestと具体実現境界

*対象：voice leading request candidateが、外部realization boundaryとGammaによって具体voice leading observationへ接続される条件*  
*状態：DRAFT v0.1 / 77 voice leading計画境界後の具体実現最小検証*  
*実装：`10_検証/interval_module_voice_leading_realization_boundary.py`*

---

## ■ 0. 検証目的

77では、selected interval target candidate、外部voice leading plan、`Gamma_voice_leading_request`を与えた場合だけvoice leading request candidateが生じることを確認した。

78では、そのvoice leading request candidateを固定し、外部realization boundaryと`Gamma_voice_leading_realization`を与えた場合だけconcrete voice leading observationが生じることを確認する。

```text
voice leading request candidate
  + external realization boundary
  + Gamma_voice_leading_realization_fixture
  ↓
concrete voice leading observation
  ↓
harmonic function は未生成
```

ここで確認するのは、声部進行要求があることと、具体音として実現されたことを分けることである。

---

## ■ 1. 固定するvoice leading request

77で得たfixture用のvoice leading request candidateを使う。

```text
voice leading request:
  lower_target_degree = 1
  upper_target_degree = 5
```

これは実現要求であり、まだ具体音の選択ではない。

---

## ■ 2. 外部realization boundary

今回はrealization boundaryを外部fixtureとして与える。

```text
external realization boundary:
  lower_voice_range = C3-C5
  upper_voice_range = G3-G5
  candidate_octaves = 3, 4, 5
```

このboundaryはvoice leading requestから自動生成されたものではない。

---

## ■ 3. 暫定結論

78では、voice leading request candidateだけではconcrete voice leading observationは生じず、外部realization boundaryと`Gamma_voice_leading_realization`を与えた場合だけconcrete voice leading observationが生じることを確認する。

ただし、

```text
concrete voice leading observation
  ≠ harmonic function
  ≠ next context interpretation
  ≠ Core昇格
```

で停止する。
