# 検証記録：reentered confirmed M_BからCore整合候補境界

*対象：再入confirmed M_B candidateが、外部Core surface inventoryとGammaによってCore alignment candidateへ接続される条件*  
*状態：DRAFT v0.1 / 149後の既存93再接続境界*  
*実装：`10_検証/interval_module_core_alignment_reentry.py`*

```text
reentered confirmed M_B candidate
  + external Core surface inventory
  + Gamma_interval_core_alignment_fixture
  ↓
Core alignment candidate
```

実行結果。

```text
core_alignment_candidate_observed_from_reentered_confirmed_M_B_not_adopted
```

Core alignment候補は生成するが、Core採用はまだ起こさない。
