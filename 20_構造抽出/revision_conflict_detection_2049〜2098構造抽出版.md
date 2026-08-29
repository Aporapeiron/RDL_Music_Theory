# revision conflict detection 2049〜2098 構造抽出版

## 位置づけ

1999〜2048でrevision memoryがcommitment履歴へ整合リンクとして再入した後、実際に衝突が生じる場合、その検出境界を検査する。

この構造は、conflict detectionをresolutionや削除による矛盾解消にせず、revision traceとcommitment traceを保持したまま、どこに差異が出たかを観測する。

## 位相

```text
source_reentry
↓
conflict_request
↓
policy_layer
↓
conflict_layer
↓
partition_layer
↓
conflict_view
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

1999〜2048のconsistency linksを再入する。

```text
reference revision consistency link
boundary revision consistency link
committed revision tension link
```

## conflict_request

revision conflict detection requestは以下を止める。

```text
detection ≠ resolution
detection ≠ deletion
detection ≠ trace erasure
```

## policy_layer

revision conflict detection policyは以下を持つ。

```text
accepts_consistency_links = True
detects_nonidentical_conflicts = True
preserves_conflict_trace = True
rejects_resolution_collapse = True
generates_deletion_resolution = False
```

## conflict_layer

consistency linkはconflict candidateになる。

```text
reference link
  conflict_kind = reference_revision_nonconflict
  conflict_site = stable_reference_trace

boundary link
  conflict_kind = boundary_revision_conflict
  conflict_site = noncommitment_trace_vs_reentry_pressure

committed tension
  conflict_kind = committed_revision_tension
  conflict_site = active_pull_vs_original_weight
```

各candidateはrevision traceとcommitment traceを保持し、衝突を即時解決しない。

## partition_layer

conflict partitionは以下である。

```text
conflict_candidates = 3
detected_conflicts = 2
nonconflict_links = 1
boundary_conflicts = 1
```

partitionはverdictではなく、どこに張力が出たかの配置である。

## integrity

確認された整合条件は以下である。

```text
consistency_links_examined = True
detected_and_nonconflict_paths_preserved = True
revision_and_commitment_traces_preserved = True
detection_not_resolution_or_deletion = True
boundary_conflict_preserved = True
generated_mutation = False
```

## non_identity

2049〜2098で保持された非同一性は以下である。

```text
detection ≠ resolution
conflict ≠ failure
conflict detection ≠ verdict
trace conflict ≠ trace erasure
```

## music_subject

revision conflict detectionは、過去のcommitmentと新しい再聴取の間に出る張力を扱う。

衝突は失敗ではない。音楽的には、聞こえの摩擦や未解決の圧力として保持され、後続の解釈が応答すべき差異を可視化する。

## 次の境界

2049〜2098の次の ξ は以下である。

```text
conflict_resolution_policy_stress
```

次は、検出された衝突をどのpolicyで解決へ向けるかを検査する。
