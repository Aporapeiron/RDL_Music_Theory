# 検証記録：reentered validated recordからM_B候補境界

*対象：再入validated state record candidateが、外部M_B criteriaとGammaによってM_B候補へ接続される条件*  
*状態：DRAFT v0.1 / 143後の既存87再接続境界*  
*実装：`10_検証/interval_module_mb_candidate_reentry.py`*

```text
reentered validated state record candidate
  + external M_B candidate criteria
  + Gamma_interval_M_B_candidate_projection_fixture
  ↓
M_B^interval candidate
```

実行結果。

```text
interval_M_B_candidate_observed_from_reentered_record_not_confirmed
```

confirmed M_B / Core promotionはまだ生じない。
