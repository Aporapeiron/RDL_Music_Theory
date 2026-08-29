# commitment revision memory 1949〜1998 構造抽出版

## 位置づけ

1899〜1948でcommitmentへ進んだ候補が、後から修正可能なmemoryとして保持されるかを検査する境界である。

この構造は、revision memoryをerror correctionだけにせず、過去のcommitmentの書き換えや削除にもせず、再聴取・読み替え可能な判断履歴として扱う。

## 位相

```text
source_reentry
↓
revision_request
↓
policy_layer
↓
revision_layer
↓
partition_layer
↓
revision_view
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

1899〜1948のcommitment candidatesを再入する。

```text
reference commitment candidate
boundary commitment candidate
active pull commitment candidate
```

## revision_request

commitment revision memory requestは以下を止める。

```text
revision ≠ error correction only
revision ≠ past rewrite
revision ≠ commitment deletion
```

## policy_layer

revision memory policyは以下を持つ。

```text
accepts_committed_candidates = True
accepts_noncommitment_candidates = True
preserves_commitment_history = True
rejects_past_rewrite = True
generates_error_only_revision = False
```

## revision_layer

commitment candidateはrevision memory entryになる。

```text
committed candidate
  revision_kind = committed_candidate_revision_memory
  revision_reason = committed_weight_can_be_reheard_later

noncommitment boundary
  revision_kind = noncommitment_boundary_revision_memory
  revision_reason = suspended_responsibility_requires_revision_route
```

各entryはcommitment traceとprecommitment traceを保持し、過去のcommitmentを書き換えない。

## partition_layer

revision partitionは以下である。

```text
committed_revision_entries = 2
noncommitment_revision_entries = 1
boundary_revision_entries = 1
```

partitionはcorrectionではなく、後から読み替えられる判断履歴の配置である。

## integrity

確認された整合条件は以下である。

```text
revision_entries_cover_commitment_candidates = True
committed_and_noncommitment_histories_preserved = True
commitment_and_precommitment_traces_preserved = True
revision_not_error_only_or_past_rewrite = True
no_commitment_deletion = True
generated_mutation = False
```

## non_identity

1949〜1998で保持された非同一性は以下である。

```text
revision ≠ error correction
revision ≠ past rewrite
revision memory ≠ commitment deletion
noncommitment revision ≠ failure
```

## music_subject

commitment revision memoryは、選んだこと自体を後続の聞こえの材料として保持する。

commitmentは消されず、固定もされない。後続文脈によって再聴取され、読み替えられ、次の判断へ渡される。

## 次の境界

1949〜1998の次の ξ は以下である。

```text
revision_reentry_consistency_stress
```

次は、revision memoryが再入したときにcommitment履歴との整合性を保てるかを検査する。
