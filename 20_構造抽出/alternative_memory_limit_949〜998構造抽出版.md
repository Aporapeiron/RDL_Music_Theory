# alternative memory limit 949〜998 構造抽出版

## 位置づけ

899〜948で分離された alternative memory に、保持圧力をかける境界である。

この構造は、memoryを残すこと自体から一段進み、どのmemoryをactive viewに置き、どのmemoryをcompressed latent memoryに回すかを観測する。

## 位相

```text
source_reentry
↓
pressure_setup
↓
limit_request
↓
policy_layer
↓
bounded_view
↓
compressed_view
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

899〜948の selection update memory bundle を再入する。

```text
source alternative = C major continuation frame
retained_for = future_context_shift / B_shift_reentry / policy_comparison
```

## pressure_setup

alternative memory を4件に展開し、保持圧力を作る。

```text
C major continuation frame
C major continuation frame under delayed cadence
C major continuation frame under altered B
C major continuation frame for policy audit
```

ここでの展開は実mutationではなく、保持制限を観測するためのstress inputである。

## limit_request

limit policy は以下を禁止する。

```text
limit ≠ deletion
limit ≠ truth
limit ≠ final ranking
```

## policy_layer

保持制限policyは次のように記録される。

```text
max_active_entries = 2
active_selection_rule = highest_retention_weight_with_music_reason
overflow_handling = compress_to_latent_reactivation_memory
preserves_inactive_memory = True
permits_reactivation = True
deletes_overflow = False
asserts_final_ranking = False
```

## bounded_view

active memory view は、現在文脈で直接参照する候補だけを保持する。

```text
active_memory_count = 2
```

active view は total memory ではない。

## compressed_view

compressed memory view は、優先度が下がった候補を削除せず、latent reactivation memoryとして保持する。

```text
compressed_memory_count = 2
deleted = False
retained_for remains available
```

## integrity

確認された整合条件は以下である。

```text
limit_is_not_deletion = True
compression_preserves_reactivation = True
active_memory_bounded = True
inactive_memory_retained = True
ranking_not_final_truth = True
generated_mutation = False
```

## non_identity

949〜998で保持された非同一性は以下である。

```text
limit ≠ deletion
compression ≠ rejection
priority ≠ truth
active view ≠ total memory
inactive memory ≠ erased memory
```

## music_subject

音楽的には、複数の読みが増えたとき、すべてを同じ強度で現在文脈に置くと読みの密度が過剰になる。

949〜998では、強く参照する読みと潜在保持する読みを分けることで、候補の多様性を消さずに、現在の音楽的処理を進められることを確認した。

## 次の境界

949〜998の次の ξ は以下である。

```text
memory_reactivation_priority_stress
```

次は、compressed latent memory がどの条件で再びactive viewへ戻るか、その優先順位境界を検査する。
