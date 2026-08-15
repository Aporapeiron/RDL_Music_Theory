# 検証記録：音程Module・next contextとharmonic annotation整合候補境界

*対象：selected next context candidateとharmonic function annotation candidateが、外部consistency evidenceとGammaによってconsistency candidateへ接続される条件*  
*状態：DRAFT v0.1 / 69〜82統合地図後のcross-module consistency最小検証*  
*実装：`10_検証/interval_module_context_harmony_consistency_boundary.py`*

---

## ■ 0. 検証目的

80〜82では、concrete voice leading observationからselected next context candidateが生じる経路と、harmonic bridge candidateからharmonic function annotation candidateが生じる経路を分けた。

83では、その二つを固定し、外部consistency evidenceと`Gamma_context_harmony_consistency`を与えた場合だけcontext-harmony consistency candidateが生じることを確認する。

```text
selected next context candidate
  + harmonic function annotation candidate
  + external consistency evidence
  + Gamma_context_harmony_consistency_fixture
  ↓
context-harmony consistency candidate
  ↓
confirmed module state は未生成
```

ここで重要なのは、selected next contextとharmonic function annotationを自動整合済みと扱わないことである。

---

## ■ 1. 固定する二入力

```text
selected next context:
  label = C major continuation

harmonic function annotation:
  label = tonic_support_annotation_candidate
```

これらは別経路で得られた候補であり、まだ整合済みrecordではない。

```text
selected next context candidate
  ≠ harmonic function annotation candidate
  ≠ context-harmony consistency candidate
```

---

## ■ 2. 外部consistency evidence

今回は整合evidenceを外部fixtureとして与える。

```text
external consistency evidence:
  context_label = C major continuation
  compatible_function_tag = tonic_support
```

このevidenceはselected next contextやharmonic annotationから自動生成されたものではない。

---

## ■ 3. 暫定結論

83では、selected next contextとharmonic function annotationだけでは整合候補は生じず、外部consistency evidenceと`Gamma_context_harmony_consistency`を与えた場合だけcontext-harmony consistency candidateが生じることを確認する。

ただし、

```text
context-harmony consistency candidate
  ≠ selected consistency
  ≠ confirmed module state
  ≠ Core昇格
```

で停止する。
