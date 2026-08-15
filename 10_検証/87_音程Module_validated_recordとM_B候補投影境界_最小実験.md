# 検証記録：validated record候補とM_B候補投影境界

*対象：validated state record候補からM_B候補を作る投影境界*  
*状態：DRAFT v0.1 / 86後の最小検証*  
*実装：`10_検証/interval_module_mb_candidate_boundary.py`*

## ■ 0. 検証目的

validated state record候補を、confirmed M_Bへ直結しない。

```text
validated state record candidate
+ external M_B candidate criteria
+ Γ_M_B_candidate_projection
↓
M_B^interval candidate
↓
confirmed M_Bではない
Core昇格でもない
```

## ■ 1. 固定入力

```text
validated record:
  validated_interval_module_state_record_candidate
  validation_scope = fixture_replay_consistency

external criteria:
  required_validation_scope = fixture_replay_consistency
  generated_by_validated_record = false
```

## ■ 2. 観測結果

```text
Γ_M_B_candidate_projectionなし
→ M_B_candidate_not_projected_without_gamma

Γ_M_B_candidate_projectionあり
→ interval_M_B_candidate_observed_not_confirmed
```

## ■ 3. 非同一性

```text
validated state record candidate
≠ M_B candidate criteria
≠ M_B^interval candidate
≠ confirmed M_B
≠ Core promotion
```

## ■ 4. 暫定結論

87では、validated record候補からM_B候補を観測する境界を作った。

ただし、ここで得たものは`M_B^interval candidate`であり、confirmed M_Bではない。
