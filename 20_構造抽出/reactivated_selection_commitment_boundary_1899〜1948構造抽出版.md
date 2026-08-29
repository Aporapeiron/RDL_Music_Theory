# reactivated selection commitment boundary 1899〜1948 構造抽出版

## 位置づけ

1849〜1898で再活性化された候補が、どの条件でcommitmentへ進むかを検査する境界である。

この構造は、commitmentをfinal truthやresolutionにせず、再活性化候補へ解釈上の重みを与えるが、不可逆固定や終端的な正解化は行わない。

## 位相

```text
source_reentry
↓
commitment_request
↓
policy_layer
↓
commitment_layer
↓
partition_layer
↓
commitment_view
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

1849〜1898のreactivated candidatesを再入する。

```text
immediate candidate reactivation record
ambiguous delay reactivation candidate
strong delay reactivation candidate
```

## commitment_request

reactivated selection commitment requestは以下を止める。

```text
commitment ≠ final truth
commitment ≠ resolution
commitment ≠ irreversible fixation
```

## policy_layer

commitment boundary policyは以下を持つ。

```text
permits_commitment_after_reactivation = True
permits_noncommitment_retention = True
preserves_precommitment_trace = True
rejects_final_truth_collapse = True
rejects_resolution_collapse = True
```

## commitment_layer

reactivated candidateはcommitment candidateになる。

```text
weak reference
  commitment_kind = reference_commitment_candidate
  commitment_reason = stable_reference_can_receive_interpretive_weight

medium reopened reading
  commitment_kind = boundary_commitment_candidate
  commitment_reason = reopened_reading_needs_suspended_responsibility

strong active pull
  commitment_kind = active_pull_commitment_candidate
  commitment_reason = strong_reactivation_can_receive_provisional_weight
```

各candidateはreactivation traceとdelay traceを保持し、final truthやresolutionへ潰れない。

## partition_layer

commitment partitionは以下である。

```text
committed_candidates = 2
retained_noncommitment_candidates = 1
boundary_commitment_candidates = 1
```

partitionはfinal rankingではなく、解釈上の重みづけに入る候補と、まだ開いたまま保持される候補の配置である。

## integrity

確認された整合条件は以下である。

```text
reactivated_candidates_cover_commitment_candidates = True
committed_and_retained_paths_preserved = True
precommitment_traces_preserved = True
commitment_not_truth_or_resolution = True
no_irreversible_fixation = True
generated_mutation = False
```

## non_identity

1899〜1948で保持された非同一性は以下である。

```text
commitment ≠ final truth
commitment ≠ resolution
commitment ≠ irreversible fixation
noncommitment retention ≠ failure
```

## music_subject

reactivated selection commitmentは、再活性化された候補に解釈上の重みを与える境界である。

commitmentは「選び始める」ことに近いが、「閉じる」ことではない。強い引力や安定参照はcommitmentへ進み、曖昧な読みは保留責任として残る。

## 次の境界

1899〜1948の次の ξ は以下である。

```text
commitment_revision_memory_stress
```

次は、commitment後にrevision memoryがどう保持されるかを検査する。
