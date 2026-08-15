# 検証記録：音程Module・selected targetと和声機能bridge境界

*対象：selected interval target candidateが、外部harmonic function bridge inventoryとGammaによって和声機能bridge candidateへ接続される条件*  
*状態：DRAFT v0.1 / 76 target selection境界後の和声機能Module接続最小検証*  
*実装：`10_検証/interval_module_harmonic_bridge_boundary.py`*

---

## ■ 0. 検証目的

76では、target candidate set observedに`Gamma_interval_target_selection`を与えた場合だけselected interval target candidateが生じることを確認した。

79では、そのselected interval target candidateを固定し、外部harmonic function bridge inventoryと`Gamma_interval_harmonic_bridge`を与えた場合だけharmonic function bridge candidateが生じることを確認する。

```text
selected interval target candidate
  + external harmonic bridge inventory
  + Gamma_interval_harmonic_bridge_fixture
  ↓
harmonic function bridge candidate
  ↓
harmonic function annotation は未生成
```

ここで確認するのは、selected interval targetがあることと、和声機能Moduleへ渡せるbridge候補があることを分けることである。

---

## ■ 1. 外部bridge inventory

今回はharmonic bridge候補を外部inventoryとして与える。

```text
external harmonic bridge inventory:
  consonant_span_bridge_candidate
  tonic_support_bridge_candidate
  dominant_resolution_bridge_candidate
```

このinventoryはselected targetから自動生成されたものではない。

---

## ■ 2. 暫定結論

79では、selected interval target candidateだけではharmonic function bridge candidateは生じず、外部harmonic bridge inventoryと`Gamma_interval_harmonic_bridge`を与えた場合だけharmonic function bridge candidateが生じることを確認する。

ただし、

```text
harmonic function bridge candidate
  ≠ harmonic function annotation
  ≠ target generation
  ≠ Core昇格
```

で停止する。
