# 検証記録：confirmation evidence差し替えによるreadiness分岐

*実装：`10_検証/interval_module_confirmation_evidence_variation.py`*

## ■ 0. 検証目的

同じM_B候補と同じΓでも、外部evidence bundleが変わるとreadiness診断が分岐することを見る。

```text
same M_B^interval candidate
+ same Γ_confirmation_readiness
+ different evidence bundle
↓
different readiness diagnostic
```

## ■ 1. 暫定結論

readinessはM_B候補の属性ではない。今回のfixtureでは、外部evidence bundleとの関係として生じる。
