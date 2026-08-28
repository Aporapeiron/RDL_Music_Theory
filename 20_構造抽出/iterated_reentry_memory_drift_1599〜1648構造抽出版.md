# iterated reentry memory drift 1599〜1648 構造抽出版

## 位置づけ

1549〜1598のpost-resolution reentry cycleを反復したとき、memoryが同一性を保ちながら非同一の戻り方をできるかを検査する境界である。

この構造は、memory driftをerrorやresetにせず、同じ由来を持つ記憶が再聴取の中で違う期待や未完了線として戻ることを扱う。

## 位相

```text
source_reentry
↓
iteration_request
↓
policy_layer
↓
drift_layer
↓
drift_partition
↓
drift_view
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

1549〜1598のreentry candidatesを再入する。

```text
primary returned reentry
derivative returned reentry
latent redeferred reentry
```

## iteration_request

iterated reentry requestは以下を止める。

```text
drift ≠ error
drift ≠ identity collapse
drift ≠ memory reset
```

## policy_layer

iterated reentry drift policyは以下を持つ。

```text
permits_nonidentical_reentry = True
preserves_identity_anchor = True
rejects_error_collapse = True
rejects_identity_collapse = True
generates_memory_reset = False
```

## drift_layer

reentry candidateはdrift candidateになる。

```text
returned memory
  drift_kind = returned_memory_rehearing_drift
  drift_vector = changed_expectation_after_return

redeferred memory
  drift_kind = redeferred_memory_continuation_drift
  drift_vector = suspended_continuity_after_reentry
```

各candidateはorigin traceとreentry routeを保持し、errorやidentical memoryへ潰れない。

## drift_partition

drift partitionは以下である。

```text
returned_drifts = 2
redeferred_drifts = 1
```

partitionはrankingではなく、driftの由来と向きの配置である。

## integrity

確認された整合条件は以下である。

```text
all_reentries_generate_drift_candidates = True
origin_trace_and_route_preserved = True
drift_without_identity_collapse = True
drift_not_error_or_memory_reset = True
returned_and_redeferred_drifts_preserved = True
generated_mutation = False
```

## non_identity

1599〜1648で保持された非同一性は以下である。

```text
drift ≠ error
drift ≠ identical memory
iteration ≠ reset
redeferred drift ≠ failure
```

## music_subject

memory driftは、同じものが同じまま戻らないことを扱う。

反復された解決後memoryは、由来を失わずに聞こえ方を変える。returned driftは変化した期待として、redeferred driftは保留された連続性として次の音楽的判断に残る。

## 次の境界

1599〜1648の次の ξ は以下である。

```text
drift_accumulation_threshold_stress
```

次は、driftが反復蓄積したとき、どこまで同一性を保持できるか、どこから別候補として扱うべきかを検査する。
