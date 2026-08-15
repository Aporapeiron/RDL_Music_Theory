# 検証記録：音程Module・selected targetとvoice leading計画境界

*対象：selected interval target candidateが、外部voice leading planとGammaによってvoice leading request candidateへ接続される条件*  
*状態：DRAFT v0.1 / 76 target selection境界後のvoice leading計画最小検証*  
*実装：`10_検証/interval_module_voice_leading_plan_boundary.py`*

---

## ■ 0. 検証目的

76では、target candidate set observedに`Gamma_interval_target_selection`を与えた場合だけselected interval target candidateが生じることを確認した。

77では、そのselected interval target candidateを固定し、外部voice leading planと`Gamma_voice_leading_request`を与えた場合だけvoice leading request candidateが生じることを確認する。

```text
selected interval target candidate
  + external voice leading plan
  + Gamma_voice_leading_request_fixture
  ↓
voice leading request candidate
  ↓
concrete voice leading realization は未生成
```

ここで確認するのは、selected targetがあることと、具体声部進行の要求候補があることを分けることである。

---

## ■ 1. 固定するselected target

76で得たfixture用のselected interval target candidateを使う。

```text
selected interval target:
  label = maintain_C_G_span
  policy_tag = preserve_span
```

これは選択済みtarget候補であり、まだ声部進行要求ではない。

---

## ■ 2. 外部voice leading plan

今回はvoice leading planを外部fixtureとして与える。

```text
external voice leading plan:
  request_name = maintain C-G span realization
  lower_target_degree = 1
  upper_target_degree = 5
  realization_scope = interval_module_fixture
```

このplanはselected targetから自動生成されたものではない。

---

## ■ 3. 暫定結論

77では、selected interval target candidateだけではvoice leading request candidateは生じず、外部voice leading planと`Gamma_voice_leading_request`を与えた場合だけvoice leading request candidateが生じることを確認する。

ただし、

```text
voice leading request candidate
  ≠ concrete voice leading realization
  ≠ harmonic function
  ≠ Core昇格
```

で停止する。
