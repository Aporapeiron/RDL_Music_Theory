# 検証記録：音程Module・harmonic bridgeとfunction annotation境界

*対象：harmonic function bridge candidateが、外部function vocabularyとGammaによってharmonic function annotation candidateへ接続される条件*  
*状態：DRAFT v0.1 / 79 harmonic bridge境界後のfunction annotation最小検証*  
*実装：`10_検証/interval_module_harmonic_function_annotation_boundary.py`*

---

## ■ 0. 検証目的

79では、selected interval target candidate、外部harmonic bridge inventory、`Gamma_interval_harmonic_bridge`を与えた場合だけharmonic function bridge candidateが生じることを確認した。

82では、そのharmonic function bridge candidateを固定し、外部function vocabularyと`Gamma_harmonic_function_annotation`を与えた場合だけharmonic function annotation candidateが生じることを確認する。

```text
harmonic function bridge candidate
  + external function vocabulary
  + Gamma_harmonic_function_annotation_fixture
  ↓
harmonic function annotation candidate
  ↓
target generation は未生成
```

ここで重要なのは、bridge候補があることと、和声機能注釈があることを分けることである。

---

## ■ 1. 固定するharmonic bridge

79で得たfixture用のharmonic function bridge candidateを使う。

```text
harmonic bridge:
  label = tonic_support_bridge_candidate
  bridge_tag = tonic_support
```

これはbridge候補であり、まだharmonic function annotationではない。

---

## ■ 2. 外部function vocabulary

今回はfunction vocabularyを外部fixtureとして与える。

```text
external function vocabulary:
  tonic_support_annotation
  consonant_span_annotation
  dominant_resolution_annotation
```

このvocabularyはharmonic bridge candidateから自動生成されたものではない。

---

## ■ 3. 暫定結論

82では、harmonic function bridge candidateだけではharmonic function annotation candidateは生じず、外部function vocabularyと`Gamma_harmonic_function_annotation`を与えた場合だけharmonic function annotation candidateが生じることを確認する。

ただし、

```text
harmonic function annotation candidate
  ≠ target generation
  ≠ voice leading generation
  ≠ Core昇格
```

で停止する。
