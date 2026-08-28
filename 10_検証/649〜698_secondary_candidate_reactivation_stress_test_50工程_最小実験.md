# 検証記録：secondary candidate reactivation stress test 50工程

*対象：599〜648で保持したsecondary_retained候補を、文脈変化で再活性化する*  
*状態：DRAFT v0.1 / Music secondary candidate reactivation stress test*  
*実装：`10_検証/secondary_candidate_reactivation_649_698.py`*

---

## ■ 0. 検証目的

599〜648では、thresholdを下回った候補を `secondary_retained` として保持した。

649〜698では、その候補が後続条件で再び前面化できるかを検査する。

```text
secondary_retained candidate
  ↓
context shift / B shift / policy shift
  ↓
reactivated
```

目的は、低weight候補を削除しなかったことが後続検査で意味を持つかを見ることである。

---

## ■ 1. 観測した50工程

```text
649 reuse_599_648_threshold_retention
650 next_xi_received
651 secondary_retained_recheck
652 reactivation_surface_request
653 reactivation_not_generation_guard
654 reactivation_not_deletion_reversal_guard
655 reactivation_not_truth_guard
656 context_shift_condition
657 B_shift_condition
658 policy_shift_condition
659 condition_not_generator_guard
660 condition_not_Core_guard
661 analysis_secondary_candidate_recheck
662 performance_secondary_candidate_recheck
663 listener_secondary_candidate_recheck
664 composition_secondary_candidate_recheck
665 candidate_retention_before_reactivation
666 context_shift_reactivation
667 B_shift_reactivation
668 policy_shift_reactivation
669 support_delta_application
670 reactivated_status_assignment
671 reactivation_not_source_mutation_guard
672 reactivation_not_final_selection_guard
673 reactivated_entry_schema
674 previous_status_field
675 reactivated_status_field
676 previous_weight_field
677 reactivated_weight_field
678 condition_trace_field
679 non_reactivated_candidates_retained
680 reactivated_candidates_retained
681 no_candidate_deletion
682 reactivation_lifecycle_record
683 secondary_vs_reactivated_split
684 reactivation_vs_selection_split
685 reactivation_vs_truth_split
686 reactivation_vs_generation_split
687 delayed_interpretation_return
688 contextual_reaccentuation_return
689 music_memory_of_low_salience
690 reactivation_surface_summary
691 prior_retention_summary
692 no_generation_summary
693 no_deletion_summary
694 no_mutation_summary
695 reactivation_record_lifecycle_open_xi
696 context_shift_evidence_open_xi
697 candidate_lifecycle_map_next_candidate
698 next_xi_selection
```

---

## ■ 2. 実行結果

```text
secondary_candidate_reactivation_649_698_observed_without_generating_new_candidates
```

確認したこと。

```text
step_count = 50
first_step = 649
last_step = 698
secondary_candidates_exist = True
secondary_candidates_reactivated = True
reactivation_requires_prior_retention = True
reactivation_generates_new_candidates = False
source_threshold_views_preserved = True
deleted_candidates = False
generated_mutation = False
```

---

## ■ 3. 再活性化条件

```text
context_shift_to_relative_minor
B_shift_to_performance_reaccentuation
policy_shift_to_future_pivot
```

これらは新候補生成器ではない。保持されていた候補の読みを再び前面化する条件である。

---

## ■ 4. 再活性化された候補

```text
A minor reinterpretation frame
```

この候補は、threshold時点では `secondary_retained` になり得る。しかし削除されていなかったため、後続の文脈変化で `reactivated` として戻ってくる。

---

## ■ 5. 停止線

```text
reactivation
≠ new candidate generation
≠ deletion reversal
≠ final selection
≠ truth

secondary_retained
≠ rejected
≠ erased
```

---

## ■ 6. 暫定結論

649〜698では、低weight候補を `secondary_retained` として残すことに意味があると確認した。

```text
低weightで保留
  ↓
削除しない
  ↓
後続条件で再活性化できる
```

Music側では、弱く見える解釈を消さずに記憶しておくことで、文脈変化・B変化・policy変化に応答できる。

```text
次ξ:
  candidate_lifecycle_map_stress
```

---

## ■ 7. まだ言えないこと

```text
再活性化条件の実証的由来があること
どのsecondary候補が再活性化すべきか一般化できること
support_deltaの値が妥当であること
reactivated候補をいつselectionへ渡すか
候補ライフサイクルが全Moduleで同じであること
Core側へ接続すべきか判断できたこと
```

これらは未解決ξとして残す。
