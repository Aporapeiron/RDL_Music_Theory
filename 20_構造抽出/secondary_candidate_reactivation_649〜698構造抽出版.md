# 構造抽出：secondary candidate reactivation

*対象：649〜698*  
*状態：DRAFT v0.1*

## ■ 1. 接続地図

```text
599〜648 threshold retention
  ↓
secondary_retained candidates
  ↓
reactivation conditions
  ├─ context shift
  ├─ B shift
  └─ policy shift
  ↓
reactivated view
  ↓
candidate lifecycle map
```

## ■ 2. 再活性化の意味

```text
reactivation:
  retained candidateの状態view更新

not:
  new candidate generation
  deletion reversal
  final selection
  truth assignment
```

## ■ 3. 50工程の位相

```text
source_reentry: 649〜651
reactivation_request: 652〜655
condition_bundle: 656〜660
candidate_recheck: 661〜665
reactivation: 666〜672
reactivated_record: 673〜678
retention: 679〜682
non_identity: 683〜686
music_subject: 687〜689
summary: 690〜694
next_plan: 695〜698
```

## ■ 4. 再活性化条件

```text
context_shift_to_relative_minor:
  context変化により再解釈が前面化する

B_shift_to_performance_reaccentuation:
  演奏Bの再アクセント化により再解釈が前面化する

policy_shift_to_future_pivot:
  作曲的なfuture pivot policyにより再解釈が前面化する
```

## ■ 5. 停止線

```text
secondary_retained
≠ rejected
≠ erased

reactivated
≠ selected
≠ true
≠ newly generated
```

## ■ 6. 未解決ξ

```text
ξ_candidate_lifecycle_map_stress
ξ_reactivation_condition_evidence
ξ_support_delta_origin
ξ_reactivated_to_selection_boundary
ξ_secondary_candidate_memory_limit
ξ_B_shift_reactivation_validation
ξ_Core_connection_diagnostic_for_lifecycle
```

## ■ 7. 暫定結論

649〜698で、secondary_retained候補が後続条件で再活性化できることを抽出した。

低weight候補を削除しなかったことにより、音楽的文脈変化・B変化・policy変化に応答する余地が残る。候補は、生成されて終わるものではなく、保持・沈静化・再活性化を持つライフサイクルとして扱える。
