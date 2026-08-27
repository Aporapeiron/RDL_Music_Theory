# 検証記録：reentered selected targetからharmonic bridge境界

*対象：再入生成されたselected interval target candidateが、外部harmonic bridge inventoryとGammaによってharmonic bridge candidateへ接続される条件*  
*状態：DRAFT v0.1 / 133 reentered selected target後の既存79再接続境界*  
*実装：`10_検証/interval_module_harmonic_bridge_reentry.py`*

---

## ■ 0. 検証目的

136では、133で得たreentered selected targetを固定し、外部harmonic bridge inventoryと`Gamma_interval_harmonic_bridge`を与えた場合だけharmonic bridge candidateが生じることを確認する。

```text
reentered selected interval target
  + external harmonic bridge inventory
  + Gamma_reentered_selected_target_to_harmonic_bridge
  + Gamma_interval_harmonic_bridge_fixture
  ↓
harmonic bridge candidate
  ↓
harmonic function annotation は未生成
```

実行結果。

```text
reentered_selected_target_connected_to_harmonic_bridge_not_annotation
```

## ■ 1. 暫定結論

reentered selected targetだけではharmonic bridgeは生じず、外部inventoryと再入Gammaを与えた場合だけharmonic bridge candidateが生じる。

これはvoice leading系列とは別に、selected targetから和声機能側へ分岐する接続点である。
