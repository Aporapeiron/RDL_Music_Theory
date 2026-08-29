# delayed selection reactivation 1849〜1898 構造抽出版

## 位置づけ

1799〜1848で遅延されたselectionが、後続文脈で再活性化される条件を検査する境界である。

この構造は、reactivationをimmediate adoptionやdelay clearanceにせず、delay traceとpressure traceを保持したまま、選択前の開いた候補として扱う。

## 位相

```text
source_reentry
↓
reactivation_request
↓
policy_layer
↓
reactivation_layer
↓
partition_layer
↓
reactivation_view
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

1799〜1848のdelay candidatesを再入する。

```text
weak immediate selection candidate
medium ambiguity delay candidate
strong selection delay candidate
```

## reactivation_request

delayed selection reactivation requestは以下を止める。

```text
reactivation ≠ immediate adoption
reactivation ≠ delay clearance
reactivation ≠ pressure trace deletion
```

## policy_layer

delayed selection reactivation policyは以下を持つ。

```text
accepts_delayed_candidates = True
permits_reactivation_without_selection = True
preserves_delay_trace = True
rejects_delay_clearance = True
generates_immediate_adoption = False
```

## reactivation_layer

delay candidateはreactivated selection candidateになる。

```text
weak immediate candidate
  reactivation_kind = immediate_candidate_reactivation_record
  reactivation_trigger = stable_context_returns_as_reference

medium delayed candidate
  reactivation_kind = ambiguous_delay_reactivation_candidate
  reactivation_trigger = later_context_reopens_suspended_reading

strong delayed candidate
  reactivation_kind = strong_delay_reactivation_candidate
  reactivation_trigger = unresolved_pull_becomes_active_again
```

各candidateはdelay traceとpressure traceを保持し、delay recordを消さない。

## partition_layer

reactivation partitionは以下である。

```text
reactivated_without_selection = 2
reactivated_with_immediate_selection = 1
still_delayed_candidates = 2
```

partitionはresolutionではなく、再活性化後の選択状態を分ける。

## integrity

確認された整合条件は以下である。

```text
delayed_candidates_reactivated = True
selection_and_nonselection_paths_preserved = True
delay_and_pressure_traces_preserved = True
reactivation_not_immediate_adoption = True
no_delay_clearance_or_trace_deletion = True
generated_mutation = False
```

## non_identity

1849〜1898で保持された非同一性は以下である。

```text
reactivation ≠ immediate adoption
reactivation ≠ delay clearance
still delayed ≠ failure
reactivation ≠ resolution
```

## music_subject

delayed selection reactivationは、保留された聞こえが後続文脈で再び前景化することを扱う。

再活性化は採用ではない。戻ってきた注意は、開かれた読み、能動的な引力、または安定参照として残り、delay traceによって以前の保留理由を追跡できる。

## 次の境界

1849〜1898の次の ξ は以下である。

```text
reactivated_selection_commitment_boundary_stress
```

次は、再活性化された候補がいつcommitmentへ進むのか、その境界を検査する。
