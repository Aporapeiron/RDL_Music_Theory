# variation sequence boundary 1149〜1198 構造抽出版

## 位置づけ

1099〜1148の variation lifecycle を、順序列として接続した境界である。

この構造は、variation を単発moveではなく、anchor保持の連鎖とbranch candidate生成を伴う sequence として扱う。

## 位相

```text
source_reentry
↓
sequence_request
↓
sequence_layer
↓
sequence_guard
↓
branch_layer
↓
branch_guard
↓
boundary_view
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

1099〜1148の variation lifecycle bundle を再入する。

```text
active variations = surface_variation / cadential_position_variation
latent variations = B_coloring_variation
compressed variations = contextual_echo_variation
identity anchor = C_major_continuation_frame_anchor
```

## sequence_request

variation sequence request は以下を止める。

```text
sequence ≠ final form
sequence ≠ single lineage
branch ≠ deletion
```

## sequence_layer

sequence events は以下である。

```text
1. surface_variation
2. B_coloring_variation
3. cadential_position_variation
4. contextual_echo_variation
```

各eventは anchor を保持し、cumulative anchor strength が threshold を下回らない。

```text
sequence_threshold_rule = anchor_strength_above_0_70_allows_sequence_continuity
```

## branch_layer

branch candidates は以下である。

```text
B_coloring_derivative_sequence
contextual_echo_derivative_sequence
```

これらは shared anchor を持つが、新しい sequence を要求する派生候補である。

## boundary_view

sequence boundary は、anchor retention view と branch retention view を同時に保持する。

```text
primary sequence
+
branch candidates
+
non-confluent variation memory
```

## integrity

確認された整合条件は以下である。

```text
sequence_preserves_anchor_chain = True
branch_candidates_retained = True
sequence_is_not_final_form = True
sequence_is_not_single_lineage = True
branches_are_not_deletions = True
generated_mutation = False
```

## non_identity

1149〜1198で保持された非同一性は以下である。

```text
sequence ≠ final form
sequence ≠ single lineage
branch ≠ deletion
branch ≠ error
```

## music_subject

variation sequence は、ひとつの完成形へ向かう直線ではない。

同じanchorを保つ展開列が進む一方で、latent / compressed variation は派生系列を開く。したがって、音楽的展開は「主系列」と「派生可能性」を同時に保持する non-confluent な記憶構造として扱われる。

## 次の境界

1149〜1198の次の ξ は以下である。

```text
branch_reentry_policy_stress
```

次は、保持されたbranch candidateが、どの条件で再入を許可され、どの条件でlatentのまま残るかを検査する。
