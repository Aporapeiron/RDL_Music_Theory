# 検証記録：threshold policy と低weight候補保持 stress test 50工程

*対象：549〜598で作ったweight viewにthreshold policyを通す*  
*状態：DRAFT v0.1 / Music threshold retention stress test*  
*実装：`10_検証/threshold_low_weight_retention_599_648.py`*

---

## ■ 0. 検証目的

549〜598では、候補にweightを付けても確率・真理・削除条件へ潰さないことを確認した。

599〜648では、thresholdを導入する。

```text
weight view
  ↓
threshold policy
  ↓
primary_display
+ secondary_retained
  ↓
all candidates retained
```

目的は、thresholdを使って表示や優先度を分けても、低weight候補をerrorやdeletion targetにしないことである。

---

## ■ 1. 観測した50工程

```text
599 reuse_549_598_weighting_view
600 next_xi_received
601 weight_view_recheck
602 threshold_policy_request
603 threshold_not_truth_guard
604 threshold_not_deletion_guard
605 threshold_not_selection_generator_guard
606 threshold_source_external_guard
607 support_threshold_set
608 low_weight_status_set
609 delete_flag_false
610 threshold_as_view_policy
611 threshold_not_probability_guard
612 analysis_threshold_application
613 performance_threshold_application
614 listener_threshold_application
615 composition_threshold_application
616 above_threshold_labels
617 below_threshold_labels
618 threshold_not_source_mutation_guard
619 analysis_low_weight_retention
620 performance_low_weight_retention
621 listener_low_weight_retention
622 composition_low_weight_retention
623 low_weight_not_error_guard
624 low_weight_not_deleted_guard
625 low_weight_future_xi_record
626 primary_display_status
627 secondary_retained_status
628 status_not_truth_guard
629 status_not_error_guard
630 thresholded_record_schema
631 retention_reason_field
632 deletion_reason_empty_check
633 threshold_policy_trace
634 threshold_vs_weight_split
635 threshold_vs_selection_split
636 threshold_vs_truth_split
637 threshold_vs_deletion_split
638 low_salience_music_reading
639 secondary_interpretation_space
640 ambiguity_survives_threshold
641 threshold_boundary_summary
642 low_weight_retention_summary
643 no_deletion_summary
644 no_mutation_summary
645 real_evidence_threshold_origin_open_xi
646 secondary_candidate_reactivation_open_xi
647 threshold_record_schema_next_candidate
648 next_xi_selection
```

---

## ■ 2. 実行結果

```text
threshold_low_weight_retention_599_648_observed_without_deleting_low_weight_candidates
```

確認したこと。

```text
step_count = 50
first_step = 599
last_step = 648
support_threshold = 0.60
low_weight_candidates_exist = True
low_weight_candidates_retained = True
threshold_deletes_candidates = False
threshold_is_truth_boundary = False
threshold_is_selection_generator = False
all_candidates_retained = True
generated_mutation = False
```

---

## ■ 3. threshold policy

```text
name = support_threshold_with_low_weight_retention
support_threshold = 0.60
low_weight_status = secondary_retained
deletes_below_threshold = False
threshold_source = external_display_policy_fixture
```

thresholdは表示・優先度分類のための境界であり、削除条件ではない。

---

## ■ 4. display status

```text
above threshold:
  primary_display

below threshold:
  secondary_retained
```

`secondary_retained` は、弱い候補ではあるが、失敗候補ではない。後続の文脈変化や別B文脈で再活性化し得る候補として残す。

---

## ■ 5. 停止線

```text
threshold
≠ truth boundary
≠ deletion boundary
≠ selection generator
≠ probability conversion

below threshold
≠ error
≠ deletion target

secondary_retained
≠ rejected
```

---

## ■ 6. 暫定結論

599〜648では、thresholdを置いても低weight候補を保持できることを確認した。

```text
thresholdで見え方を分ける
しかし候補空間は閉じない
```

Music側では、低weight候補を消すのではなく、`secondary_retained` として保持することで、後続の再解釈やB文脈変化を扱える。

```text
次ξ:
  secondary_candidate_reactivation_stress
```

---

## ■ 7. まだ言えないこと

```text
0.60というthreshold値が妥当であること
thresholdの実証的由来があること
secondary_retainedをいつ再活性化するか
低weight候補を永久保持すべきこと
thresholdが全B文脈で同じでよいこと
表示上の低優先候補が知覚上も低優先であること
Core側へ接続すべきか判断できたこと
```

これらは未解決ξとして残す。
