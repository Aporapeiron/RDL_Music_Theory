# reactivation conflict with commitment 2649〜2698 構造抽出版

## 位置づけ

2599〜2648で得たalternative reactivation after commitmentが、既存commitmentと衝突する場合を扱う構造である。

この構造は、conflictをcommitment cancellationやreplacementにせず、採用後に戻ってきた別の聞こえと既存recordの摩擦として保持する。

## 位相

```text
source_reentry
↓
conflict_request
↓
conflict_layer
↓
conflict_content_layer
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

2599〜2648のreactivationsを再入する。

```text
contextual_alternative_reactivation
hearing_shift_alternative_reactivation
reference_alternative_reactivation
```

## conflict_request

reactivation conflict with commitment requestは以下を止める。

```text
conflict ≠ commitment cancellation
conflict ≠ commitment replacement
conflict ≠ resolution
```

## conflict_layer

reactivationはcommitment conflictになる。

```text
contextual_alternative_reactivation
  conflict_kind = contextual_reactivation_commitment_conflict

hearing_shift_alternative_reactivation
  conflict_kind = hearing_shift_reactivation_commitment_conflict

reference_alternative_reactivation
  conflict_kind = reference_reactivation_commitment_conflict
```

conflictは検出されるが、commitment cancellationやreplacementは生成されない。

## conflict_content_layer

conflictは以下の内容を持つ。

```text
later_phrase_pressure_conflicts_with_existing_record
returned_weight_pressure_conflicts_with_committed_reading
reference_axis_check_conflicts_with_record_scope
```

## partition_layer

conflict partitionは以下である。

```text
conflicts = 3
contextual_conflicts = 1
hearing_shift_conflicts = 1
reference_conflicts = 1
```

partitionはcancellationでもsolutionでもなく、摩擦の配置である。

## integrity

確認された整合条件は以下である。

```text
every_reactivation_gets_conflict_check = True
conflict_variety_preserved = True
reactivation_commitment_conflict_traces_preserved = True
conflict_detected_without_cancellation = True
no_replacement_or_resolution = True
generated_mutation = False
```

## non_identity

2649〜2698で保持された非同一性は以下である。

```text
conflict ≠ cancellation
conflict ≠ replacement
conflict ≠ resolution
```

## music_subject

reactivation conflict with commitmentは、採用後に戻ってきた別の聞こえと、既存採用recordの摩擦を保持する境界である。

ここで摩擦を観測しても、採用は取り消されない。別の聞こえが戻ったことと、既存recordが無効になることを分けることで、音楽的な再聴取の厚みを残せる。

## 次の境界

2649〜2698の次の ξ は以下である。

```text
conflict_mediation_after_reactivation_stress
```

次は、再活性化による衝突をmediationへ渡すとき、仲介と解決済み判定を分離できるかを検査する。
