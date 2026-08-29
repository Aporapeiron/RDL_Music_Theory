# split candidate reintegration 1699〜1748 構造抽出版

## 位置づけ

1649〜1698でsplit zoneに入った候補が、後続文脈で再統合されうるか、あるいは独立候補として残るかを検査する境界である。

この構造は、reintegrationをforced unificationにせず、split candidateをrejectionにも失敗にもせず、origin traceつきの再統合可能候補として保持する。

## 位相

```text
source_reentry
↓
reintegration_request
↓
policy_layer
↓
candidate_layer
↓
partition_layer
↓
reintegration_view
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

1649〜1698のthreshold candidatesを再入する。

```text
below threshold candidate
boundary ambiguity candidate
split zone candidate
```

## reintegration_request

split candidate reintegration requestは以下を止める。

```text
reintegration ≠ rejection
reintegration ≠ forced unification
reintegration ≠ origin deletion
```

## policy_layer

split reintegration policyは以下を持つ。

```text
accepts_split_candidate = True
permits_contextual_reintegration = True
permits_independent_retention = True
preserves_boundary_ambiguity = True
generates_forced_unification = False
```

## candidate_layer

threshold candidateはreintegration candidateになる。

```text
below threshold
  reintegration_kind = same_memory_reintegration_candidate
  context_relation = already_within_identity_context

boundary zone
  reintegration_kind = ambiguous_reintegration_candidate
  context_relation = waits_for_later_context

split zone
  reintegration_kind = split_candidate_reintegration_candidate
  context_relation = parallel_candidate_with_origin_trace
```

各candidateはsplit traceとorigin traceを保持し、forced unificationを生成しない。

## partition_layer

reintegration partitionは以下である。

```text
contextual_reintegrations = 1
independent_retentions = 1
ambiguous_reintegrations = 1
```

partitionはfinal mergeではなく、後続文脈に対する候補の戻り方を分ける。

## integrity

確認された整合条件は以下である。

```text
split_and_retained_candidates_carried = True
contextual_and_independent_paths_preserved = True
split_trace_preserved = True
reintegration_not_forced_unification = True
no_split_rejection_or_origin_deletion = True
generated_mutation = False
```

## non_identity

1699〜1748で保持された非同一性は以下である。

```text
reintegration ≠ forced unification
split candidate ≠ rejection
independent retention ≠ failure
contextual merge ≠ final merge
```

## music_subject

split candidate reintegrationは、別候補化した記憶が後続文脈によって戻りうることを扱う。

候補は、同一記憶への再統合、曖昧な保留、独立候補としての保持に分かれる。どの場合もorigin traceが残るため、後で「なぜその聞こえが戻ったのか」を追跡できる。

## 次の境界

1699〜1748の次の ξ は以下である。

```text
reintegration_context_pressure_stress
```

次は、後続文脈がどの程度強く候補の再統合を促すか、その圧力を検査する。
