# 検証記録：M_B候補とCore昇格診断境界

*対象：M_B^interval候補をCoreへ昇格させず、昇格診断に留める条件*  
*状態：DRAFT v0.1 / 87後の最小検証*  
*実装：`10_検証/interval_module_core_promotion_diagnostic.py`*

## ■ 0. 検証目的

M_B候補をCoreへ直結しない。

```text
M_B^interval candidate
+ external Core promotion criteria
+ Γ_core_promotion_diagnostic
↓
Core promotion diagnostic
↓
Coreは変化しない
```

## ■ 1. 固定入力

```text
M_B^interval candidate:
  confirmed_mb = false

Core promotion criteria:
  requires_confirmed_mb = true
  allows_candidate_only = false
  generated_by_mb_candidate = false
```

## ■ 2. 観測結果

```text
Γ_core_promotion_diagnosticなし
→ core_promotion_not_checked_without_gamma

Γ_core_promotion_diagnosticあり
→ core_promotion_blocked_unconfirmed_M_B
```

## ■ 3. 非同一性

```text
M_B^interval candidate
≠ Core promotion criteria
≠ Core promotion diagnostic
≠ Core mutation
```

## ■ 4. 暫定結論

88では、M_B候補をCoreへ昇格させるのではなく、昇格不可の診断候補を作るところで停止した。

confirmed M_Bでない候補は、Core昇格条件を満たさない。
