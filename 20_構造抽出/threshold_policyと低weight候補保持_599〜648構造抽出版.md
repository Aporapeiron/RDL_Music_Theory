# 構造抽出：threshold policy と低weight候補保持

*対象：599〜648*  
*状態：DRAFT v0.1*

## ■ 1. 接続地図

```text
549〜598 weighting view
  ↓
threshold policy
  ↓
above threshold / below threshold
  ↓
primary_display / secondary_retained
  ↓
low weight candidates retained
  ↓
next ξ selection
```

## ■ 2. thresholdの役割

```text
threshold:
  display / priority view boundary

not:
  truth boundary
  deletion boundary
  selection generator
  probability conversion
```

thresholdは候補の見え方を変えるが、候補空間を閉じない。

## ■ 3. 50工程の位相

```text
source_reentry: 599〜601
threshold_request: 602〜606
threshold_policy: 607〜611
threshold_application: 612〜618
low_weight_retention: 619〜625
classification: 626〜629
record_view: 630〜633
non_identity: 634〜637
music_subject: 638〜640
summary: 641〜644
next_plan: 645〜648
```

## ■ 4. 状態分類

```text
primary_display:
  above threshold

secondary_retained:
  below threshold, but retained
```

`secondary_retained` は rejected ではない。後続で再活性化され得る候補である。

## ■ 5. 停止線

```text
below threshold
≠ error
≠ deletion target
≠ rejected

threshold policy
≠ source record mutation
≠ selection boundary
≠ Core primitive
```

## ■ 6. 未解決ξ

```text
ξ_secondary_candidate_reactivation_stress
ξ_real_evidence_threshold_origin
ξ_threshold_by_B_context
ξ_threshold_record_schema_view
ξ_low_weight_candidate_lifecycle
ξ_weight_to_selection_policy_boundary
ξ_Core_connection_diagnostic_for_threshold
```

## ■ 7. 暫定結論

599〜648で、threshold policyを導入しても低weight候補が削除されないことを抽出した。

Music側では、thresholdは候補を消すためではなく、候補の表示・優先度・保留状態を分ける境界として扱うのがよい。低weight候補は `secondary_retained` として残り、後続の再活性化検査へ渡される。
