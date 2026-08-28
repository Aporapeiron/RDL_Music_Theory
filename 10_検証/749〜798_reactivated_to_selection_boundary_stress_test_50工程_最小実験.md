# 検証記録：reactivated to selection boundary stress test 50工程

*対象：699〜748で地図化したreactivated候補をselection境界へ戻す*  
*状態：DRAFT v0.1 / Music reactivated-to-selection boundary stress test*  
*実装：`10_検証/reactivated_to_selection_boundary_749_798.py`*

---

## ■ 0. 検証目的

699〜748では、候補の状態をライフサイクルとして地図化した。

749〜798では、そのうち `reactivated` になった候補を selection boundary へ戻す。

```text
reactivated candidate
  ↓
selection request
  ↓
selection readiness
  ↓
selection controller pending
```

目的は、再活性化された候補が選択境界へ戻れることを確認しつつ、`reactivated = selected` へ潰さないことである。

---

## ■ 1. 観測した50工程

```text
749 reuse_699_748_lifecycle_map
750 next_xi_received
751 reactivated_state_recheck
752 reactivated_selection_request
753 request_not_selection_guard
754 request_not_generation_guard
755 request_not_truth_guard
756 request_source_lifecycle_trace
757 reactivated_state_eligibility
758 candidate_retention_eligibility
759 lifecycle_status_eligibility
760 eligibility_not_selection_guard
761 eligibility_not_truth_guard
762 selection_policy_request
763 reactivation_policy_fixture
764 policy_not_candidate_generator_guard
765 policy_not_lifecycle_mutation_guard
766 readiness_record_creation
767 eligible_true_record
768 selected_false_record
769 retained_alternatives_record
770 generated_selection_false_record
771 deleted_alternatives_false_record
772 reactivated_not_selected_stop
773 request_not_selection_stop
774 eligible_not_selected_stop
775 selection_requires_controller_stop
776 reactivated_not_true_stop
777 continuation_alternative_retained
778 reactivated_candidate_retained
779 no_candidate_deletion
780 alternative_not_error_guard
781 selection_request_schema
782 selection_readiness_schema
783 policy_trace_field
784 lifecycle_trace_field
785 reactivation_vs_selection_request_split
786 selection_request_vs_selection_split
787 selection_readiness_vs_selection_split
788 selection_boundary_vs_truth_split
789 returning_interpretation_to_choice
790 delayed_choice_without_erasure
791 music_context_memory
792 reactivated_selection_boundary_summary
793 policy_required_summary
794 alternatives_retained_summary
795 no_mutation_summary
796 selection_controller_next_candidate
797 post_selection_lifecycle_open_xi
798 next_xi_selection
```

---

## ■ 2. 実行結果

```text
reactivated_to_selection_boundary_749_798_observed_without_treating_reactivation_as_selection
```

確認したこと。

```text
step_count = 50
first_step = 749
last_step = 798
reactivated_candidate_found = True
candidate_label = A minor reinterpretation frame
request_created_from_lifecycle = True
reactivated_is_selected = False
selection_requires_policy = True
alternatives_retained = True
generated_mutation = False
```

---

## ■ 3. selection request

```text
candidate_label = A minor reinterpretation frame
source_state = reactivated
request_reason = reactivated_candidate_can_reenter_selection_boundary
generated_candidate = False
```

このrequestは、候補生成ではない。既に保持されていた候補の状態履歴から作られる。

---

## ■ 4. selection readiness

```text
eligible = True
selected = False
status = reactivated_candidate_ready_for_selection_controller
```

`eligible=True` は、選択されたことを意味しない。selection controllerが必要である。

---

## ■ 5. 停止線

```text
reactivated
≠ selected
≠ true

selection request
≠ selection
≠ candidate generation

eligible
≠ selected

selection boundary
≠ truth boundary
```

---

## ■ 6. 暫定結論

749〜798では、再活性化された候補をselection boundaryへ戻せることを確認した。

ただし、

```text
再活性化された
  ↓
選択可能性が戻った
  ↓
selection controller待ち
```

であり、再活性化そのものは選択ではない。

```text
次ξ:
  selection_controller_after_reactivation_stress
```

---

## ■ 7. まだ言えないこと

```text
selection controllerの具体的由来が確定したこと
reactivated候補が常に選択可能であること
eligible候補をいつ選ぶべきか
再活性化後の選択が真であること
post-selection lifecycleが定義できたこと
Core側へ接続すべきか判断できたこと
```

これらは未解決ξとして残す。
