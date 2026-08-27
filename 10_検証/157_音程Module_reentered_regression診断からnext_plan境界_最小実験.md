# 検証記録：reentered regression診断からnext plan境界

*対象：再入regression diagnosticが、planning controllerによってnext verification plan candidateへ接続される条件*  
*状態：DRAFT v0.1 / 156後の既存100再接続境界*  
*実装：`10_検証/interval_module_next_verification_plan_reentry.py`*

```text
reentered regression diagnostic
  + planning controller
  ↓
next verification plan candidate
```

実行結果。

```text
next_verification_plan_observed_from_reentered_regression_not_committed
```

next plan候補は生成するが、まだcommitしない。
