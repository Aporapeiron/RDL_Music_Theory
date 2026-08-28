# 構造抽出：weighting without collapse

*対象：549〜598*  
*状態：DRAFT v0.1*

## ■ 1. 接続地図

```text
499〜548 B-dependent policy selection
  ↓
same prediction candidates
  ↓
B-dependent weighting view
  ↓
support_weight
  +
retention_weight
  ↓
highest weight differs by B
  ↓
all candidates retained
  ↓
next ξ selection
```

## ■ 2. weightの分離

```text
support_weight:
  B文脈における支持の強さ

retention_weight:
  後続検査へ候補を残す強さ
```

この分離により、supportが低い候補も未解決ξとして保持できる。

## ■ 3. 50工程の位相

```text
source_reentry: 549〜551
weight_request: 552〜556
B_weighting: 557〜562
candidate_weights: 563〜568
ranking_view: 569〜574
retention: 575〜580
record_view: 581〜584
non_identity: 585〜588
music_subject: 589〜591
summary: 592〜595
next_plan: 596〜598
```

## ■ 4. B別highest weight

```text
C major continuation frame:
  analysis_B
  listener_B

A minor reinterpretation frame:
  performance_B
  composition_B
```

これは499〜548のselection view差と同型だが、selectionそのものではない。

## ■ 5. 停止線

```text
weight
≠ probability
≠ truth
≠ confidence
≠ certainty
≠ deletion condition
≠ selection generator

ranking view
≠ selection boundary

low weight candidate
≠ error
```

## ■ 6. 未解決ξ

```text
ξ_threshold_policy_and_low_weight_retention_stress
ξ_real_evidence_weight_origin
ξ_weight_measurement_by_listener_B
ξ_weight_measurement_by_performer_B
ξ_weighted_record_schema_view
ξ_weight_to_selection_policy_boundary
ξ_Core_connection_diagnostic_for_weight
```

## ■ 7. 暫定結論

549〜598で、weightを付けても複数解釈空間を潰さない構造を抽出した。

weightは候補削除や真理確定ではなく、音楽的曖昧性の内部構造を見るためのviewである。Music側では、supportとretentionを分けて扱うことで、低weight候補も後続検査へ渡せる。
