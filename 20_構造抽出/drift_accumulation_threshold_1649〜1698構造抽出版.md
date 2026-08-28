# drift accumulation threshold 1649〜1698 構造抽出版

## 位置づけ

1599〜1648のmemory driftが反復蓄積したとき、どこまで同一記憶の変形として保持し、どこから別候補として分岐させるかを検査する境界である。

この構造は、thresholdをtruthやforced selectionにせず、同一性保持、境界曖昧性、新候補分岐を同時に残す。

## 位相

```text
source_reentry
↓
threshold_request
↓
policy_layer
↓
threshold_layer
↓
partition_layer
↓
threshold_view
↓
bundle
↓
integrity
↓
non_identity
↓
music_subject
↓
summary
↓
next_plan
```

## source_reentry

1599〜1648のdrift candidatesを再入する。

```text
primary returned drift
derivative returned drift
latent redeferred drift
```

## threshold_request

drift accumulation threshold requestは以下を止める。

```text
threshold ≠ truth
threshold ≠ forced selection
threshold ≠ origin deletion
```

## policy_layer

drift threshold policyは以下を持つ。

```text
soft_threshold = 2
split_threshold = 3
permits_below_threshold_drift = True
preserves_boundary_ambiguity = True
treats_threshold_as_final_truth = False
generates_forced_selection = False
```

## threshold_layer

drift candidateはthreshold candidateになる。

```text
accumulation_level = 1
  threshold_zone = below_soft_threshold
  handling_kind = same_memory_variation

accumulation_level = 2
  threshold_zone = boundary_ambiguity_zone
  handling_kind = ambiguous_identity_drift

accumulation_level = 3
  threshold_zone = split_threshold_zone
  handling_kind = new_candidate_with_origin_trace
```

split candidateもorigin traceを削除しない。

## partition_layer

threshold partitionは以下である。

```text
retained_identity_drifts = 2
split_candidate_drifts = 1
boundary_zone_drifts = 1
```

partitionはdeletionでもrankingでもなく、蓄積圧力に対する扱いの差である。

## integrity

確認された整合条件は以下である。

```text
threshold_candidates_cover_source_drifts = True
retained_and_split_paths_preserved = True
boundary_zone_preserved = True
threshold_not_truth_or_forced_selection = True
origin_trace_preserved_across_split = True
generated_mutation = False
```

## non_identity

1649〜1698で保持された非同一性は以下である。

```text
threshold ≠ truth
split ≠ rejection
boundary zone ≠ decision
accumulation ≠ reset
```

## music_subject

thresholdは、記憶が別候補化し始める認識圧である。

below thresholdは同じ記憶の変奏として残り、boundary zoneは未確定の聞こえとして保留され、split zoneはorigin traceを持つ新しい音楽候補として分岐する。

## 次の境界

1649〜1698の次の ξ は以下である。

```text
split_candidate_reintegration_stress
```

次は、分岐した候補が後続文脈で再統合されうるか、あるいは独立候補として残るかを検査する。
