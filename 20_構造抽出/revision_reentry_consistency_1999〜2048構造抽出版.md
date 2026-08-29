# revision reentry consistency 1999〜2048 構造抽出版

## 位置づけ

1949〜1998で保持したrevision memoryが再入したとき、元のcommitment履歴と整合しながら後続判断へ接続できるかを検査する境界である。

この構造は、consistencyをhistory rewriteや削除による矛盾解消にせず、commitment traceとrevision traceを保持したまま、非同一の再聴取を整合リンクとして扱う。

## 位相

```text
source_reentry
↓
consistency_request
↓
policy_layer
↓
link_layer
↓
partition_layer
↓
consistency_view
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

1949〜1998のrevision entriesを再入する。

```text
reference commitment revision memory
boundary commitment revision memory
active pull commitment revision memory
```

## consistency_request

revision reentry consistency requestは以下を止める。

```text
consistency ≠ history rewrite
consistency ≠ deletion based consistency
consistency ≠ commitment overwrite
```

## policy_layer

revision reentry consistency policyは以下を持つ。

```text
accepts_revision_reentry = True
preserves_original_commitment = True
permits_nonidentical_consistency = True
rejects_deletion_based_consistency = True
generates_history_rewrite = False
```

## link_layer

revision memory entryはconsistency linkになる。

```text
committed revision
  link_kind = committed_revision_consistency_link
  consistency_relation = reheard_commitment_consistent_with_original_weight

boundary revision
  link_kind = boundary_revision_consistency_link
  consistency_relation = open_responsibility_consistent_with_noncommitment_trace
```

各linkはrevision traceとcommitment traceを保持し、元のcommitmentを書き換えない。

## partition_layer

consistency partitionは以下である。

```text
consistency_links = 3
committed_consistency_links = 2
boundary_consistency_links = 1
```

partitionはcorrectionではなく、再入したrevision memoryと元のcommitment履歴の接続配置である。

## integrity

確認された整合条件は以下である。

```text
revision_entries_reentered_as_links = True
committed_and_boundary_links_preserved = True
revision_and_commitment_traces_preserved = True
consistency_without_rewrite_or_deletion = True
original_commitment_not_overwritten = True
generated_mutation = False
```

## non_identity

1999〜2048で保持された非同一性は以下である。

```text
consistency ≠ history rewrite
consistency ≠ deletion
revision reentry ≠ correction
boundary consistency ≠ failure
```

## music_subject

revision reentry consistencyは、後から読み替えられた判断を、過去のcommitmentと追跡可能に接続する。

再聴取は過去の聞こえの否定ではない。元の重みづけと新しい読みをtraceで接続することで、音楽的解釈の変化を履歴つきで扱える。

## 次の境界

1999〜2048の次の ξ は以下である。

```text
revision_conflict_detection_stress
```

次は、revision reentryによって実際の衝突が生じる場合、その検出境界を検査する。
