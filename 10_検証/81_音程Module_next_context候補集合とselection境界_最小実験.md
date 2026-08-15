# 検証記録：音程Module・next context候補集合とselection境界

*対象：next context candidate set observedからselected next context candidateが生じる条件*  
*状態：DRAFT v0.1 / 80 next context候補集合境界後のselection最小検証*  
*実装：`10_検証/interval_module_next_context_selection_boundary.py`*

---

## ■ 0. 検証目的

80では、concrete voice leading observation、外部next context inventory、`Gamma_next_context_candidate_filter`を与えた場合だけnext context candidate set observedが生じることを確認した。

81では、そのnext context candidate set observedを固定し、`Gamma_next_context_selection`を与えた場合だけselected next context candidateが生じることを確認する。

```text
next context candidate set observed
  + Gamma_next_context_selection_fixture
  ↓
selected next context candidate
  ↓
harmonic function / Core昇格 は未生成
```

ここで確認するのは、候補集合があることと、候補が選ばれていることを分けることである。

---

## ■ 1. 固定するnext context候補集合

80で得たfixture用のnext context candidate set observedを使う。

```text
next context candidates:
  C major continuation
  G major reinterpretation
```

これは候補集合であり、まだselected next contextではない。

---

## ■ 2. 暫定結論

81では、next context candidate set observedだけではselected next context candidateは生じず、`Gamma_next_context_selection`を与えた場合だけselected next context candidateが生じることを確認する。

ただし、

```text
selected next context candidate
  ≠ harmonic function
  ≠ Core昇格
```

で停止する。
