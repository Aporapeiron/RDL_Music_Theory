# 検証記録：reentered Core整合候補からadoption proposal境界

*対象：再入Core alignment candidateが、adoption policyによってCore adoption proposalへ接続される条件*  
*状態：DRAFT v0.1 / 150後の既存95再接続境界*  
*実装：`10_検証/interval_module_core_adoption_proposal_reentry.py`*

```text
reentered Core alignment candidate
  + Gamma_core_adoption_proposal_fixture
  ↓
Core adoption proposal
```

実行結果。

```text
core_adoption_proposal_observed_from_reentered_alignment_not_core_mutation
```

proposalは生成するが、Core mutationはまだ起こさない。
