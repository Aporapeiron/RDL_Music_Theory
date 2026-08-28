# 構造抽出：candidate lifecycle map

*対象：699〜748*  
*状態：DRAFT v0.1*

## ■ 1. 接続地図

```text
649〜698 secondary candidate reactivation
  ↓
candidate lifecycle map
  ↓
candidate
  ├─ selected
  │    └─ retained_alternative
  └─ secondary_retained
       └─ reactivated
  ↓
reactivated_to_selection_boundary
```

## ■ 2. 状態 inventory

```text
candidate
selected
secondary_retained
reactivated
retained_alternative
```

これらは真偽値ではなく、候補の状態viewである。

## ■ 3. 50工程の位相

```text
source_reentry: 699〜701
lifecycle_request: 702〜705
state_inventory: 706〜711
transition_inventory: 712〜718
entry_map: 719〜724
global_map: 725〜729
non_identity: 730〜734
music_subject: 735〜738
summary: 739〜743
next_plan: 744〜748
```

## ■ 4. transition inventory

```text
candidate → selected
candidate → secondary_retained
secondary_retained → reactivated
selected → retained_alternative
```

transitionは候補削除ではなく、状態viewの履歴である。

## ■ 5. 停止線

```text
selected
≠ true

secondary_retained
≠ rejected

reactivated
≠ selected

retained_alternative
≠ deleted

lifecycle map
≠ processing pipeline
≠ Core primitive
≠ T2 finalization
```

## ■ 6. 未解決ξ

```text
ξ_reactivated_to_selection_boundary_stress
ξ_candidate_memory_limit
ξ_lifecycle_record_schema_view
ξ_lifecycle_transition_evidence
ξ_B_context_sensitive_lifecycle_validation
ξ_Core_connection_diagnostic_for_lifecycle
```

## ■ 7. 暫定結論

699〜748で、候補ライフサイクル地図を抽出した。

候補は、生成・選択・低weight化・再活性化・代替保持を持つ状態履歴として扱える。これにより、Music側では候補を一回限りの生成物ではなく、文脈やBに応じて変化する解釈資源として保存できる。
