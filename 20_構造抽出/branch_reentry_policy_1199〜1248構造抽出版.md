# branch reentry policy 1199〜1248 構造抽出版

## 位置づけ

1149〜1198で保持された branch candidate が、再入可能性を持つか、latent branchとして残るかを検査する境界である。

この構造は、branchを主系列への合流や削除にせず、derivative sequence と latent memory の分岐として扱う。

## 位相

```text
source_reentry
↓
policy_request
↓
condition_layer
↓
condition_guard
↓
decision_layer
↓
reentry_view
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

1149〜1198の branch candidates を再入する。

```text
B_coloring_derivative_sequence
contextual_echo_derivative_sequence
```

## policy_request

branch reentry policy は次の崩壊を止める。

```text
reentry ≠ primary confluence
reentry ≠ final selection
latent ≠ deletion
```

## condition_layer

再入条件は branch ごとに分けられる。

```text
B_context_returns_with_anchor_strength
  permits_reentry = True

echo_context_remains_below_reentry_threshold
  permits_reentry = False
  keeps_latent_if_unmet = True
```

condition は判定材料であって truth authority ではない。

## decision_layer

branch decision は以下である。

```text
B_coloring_derivative_sequence
  reentry_state = derivative_sequence_reentry_candidate
  enters_primary_sequence = False
  starts_derivative_sequence = True
  selected_as_final = False
  deleted = False

contextual_echo_derivative_sequence
  reentry_state = latent_branch_retained
  remains_latent = True
  selected_as_final = False
  deleted = False
```

## reentry_view

reentry view は、再入候補とlatent branchを同時に保持する。

```text
reentry candidate
+
latent branch
+
non-confluent branch policy
```

## integrity

確認された整合条件は以下である。

```text
reentry_policy_distinguishes_conditions = True
permitted_branch_starts_derivative_sequence = True
latent_branch_retained = True
reentry_not_primary_confluence = True
reentry_not_final_selection_or_deletion = True
generated_mutation = False
```

## non_identity

1199〜1248で保持された非同一性は以下である。

```text
reentry ≠ primary merge
reentry ≠ final selection
latent ≠ deletion
policy ≠ truth
```

## music_subject

branch reentry は、主系列へ戻す操作ではなく、派生系列を開く操作である。

再入条件を満たしたbranchは derivative return として別系列を開始し、条件を満たさないbranchは unheard option として潜在保持される。これにより、音楽的展開は単一路線ではなく、主系列と並行展開memoryを持つ。

## 次の境界

1199〜1248の次の ξ は以下である。

```text
parallel_variation_memory_stress
```

次は、主系列と派生系列が並行して保持されるとき、どのmemoryを共有し、どのmemoryを分離するかを検査する。
