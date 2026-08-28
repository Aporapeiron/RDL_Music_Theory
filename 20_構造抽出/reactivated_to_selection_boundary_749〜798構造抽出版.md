# 構造抽出：reactivated to selection boundary

*対象：749〜798*  
*状態：DRAFT v0.1*

## ■ 1. 接続地図

```text
699〜748 candidate lifecycle map
  ↓
reactivated candidate
  ↓
selection request
  ↓
selection readiness
  ↓
selection controller pending
```

## ■ 2. 抽出した境界

```text
reactivated candidate:
  A minor reinterpretation frame

selection request:
  reactivated_candidate_can_reenter_selection_boundary

selection readiness:
  eligible = True
  selected = False
```

## ■ 3. 50工程の位相

```text
source_reentry: 749〜751
selection_request: 752〜756
eligibility: 757〜761
policy_boundary: 762〜765
readiness: 766〜771
boundary_stop: 772〜776
alternative_retention: 777〜780
record_schema: 781〜784
non_identity: 785〜788
music_subject: 789〜791
summary: 792〜795
next_plan: 796〜798
```

## ■ 4. 停止線

```text
reactivated
≠ selected
≠ true

request
≠ selection

eligible
≠ selected

selection boundary
≠ truth boundary
```

## ■ 5. 未解決ξ

```text
ξ_selection_controller_after_reactivation_stress
ξ_selection_controller_origin
ξ_post_selection_lifecycle
ξ_reactivated_candidate_priority
ξ_eligible_candidate_competition
ξ_Core_connection_diagnostic_for_reactivation_selection
```

## ■ 6. 暫定結論

749〜798で、reactivated候補をselection boundaryへ戻す構造を抽出した。

再活性化は選択ではないが、選択可能性を回復する。Music側では、候補は再活性化後にただちに確定されるのではなく、selection controllerへ渡される readiness として扱うのがよい。
