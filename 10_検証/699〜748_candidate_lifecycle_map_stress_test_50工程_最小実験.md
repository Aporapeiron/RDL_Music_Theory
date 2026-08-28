# 検証記録：candidate lifecycle map stress test 50工程

*対象：649〜698で観測したsecondary候補再活性化を、候補ライフサイクル地図へ整理する*  
*状態：DRAFT v0.1 / Music candidate lifecycle map stress test*  
*実装：`10_検証/candidate_lifecycle_map_699_748.py`*

---

## ■ 0. 検証目的

649〜698では、`secondary_retained` 候補が後続条件で `reactivated` へ戻れることを確認した。

699〜748では、候補の状態履歴を地図化する。

```text
candidate
  ↓
selected / secondary_retained
  ↓
retained_alternative / reactivated
```

目的は、候補を生成された一点として扱わず、保持・沈静化・再活性化・選択view差を持つライフサイクルとして保存することである。

---

## ■ 1. 観測した50工程

```text
699 reuse_649_698_reactivation
700 next_xi_received
701 reactivation_view_recheck
702 candidate_lifecycle_map_request
703 lifecycle_not_generation_guard
704 lifecycle_not_deletion_guard
705 lifecycle_not_truth_guard
706 candidate_state_inventory
707 selected_state_inventory
708 secondary_retained_state_inventory
709 reactivated_state_inventory
710 retained_alternative_state_inventory
711 state_not_truth_guard
712 candidate_to_selected_transition
713 candidate_to_secondary_transition
714 secondary_to_reactivated_transition
715 selected_to_retained_alternative_transition
716 reactivated_to_selection_boundary_open
717 transition_not_mutation_guard
718 transition_not_finalization_guard
719 continuation_lifecycle_entry
720 reinterpretation_lifecycle_entry
721 entry_retention_check
722 entry_state_history_check
723 entry_transition_history_check
724 entry_not_error_guard
725 global_stop_lines
726 next_xi_candidates
727 map_status_assignment
728 map_not_Core_guard
729 map_not_T2_final_guard
730 selected_vs_true_split
731 secondary_vs_rejected_split
732 reactivated_vs_selected_split
733 retained_vs_deleted_split
734 lifecycle_vs_processing_pipeline_split
735 musical_memory_of_candidates
736 interpretation_history_as_music_information
737 B_context_sensitive_lifecycle
738 context_shift_sensitive_lifecycle
739 lifecycle_map_summary
740 no_candidate_deletion_summary
741 no_truth_assignment_summary
742 no_final_resolution_summary
743 no_mutation_summary
744 reactivated_to_selection_boundary_candidate
745 lifecycle_memory_limit_open_xi
746 Core_side_path_record
747 module_generalization_limit_record
748 next_xi_selection
```

---

## ■ 2. 実行結果

```text
candidate_lifecycle_map_699_748_observed_without_finalizing_candidate_states
```

確認したこと。

```text
step_count = 50
first_step = 699
last_step = 748
selected_lifecycle_preserved = True
secondary_reactivated_lifecycle_preserved = True
transitions_do_not_delete_candidates = True
transitions_do_not_assert_truth = True
map_is_not_final_resolution = True
generated_mutation = False
```

---

## ■ 3. 候補ごとのライフサイクル

```text
C major continuation frame:
  candidate
  selected
  retained_alternative

A minor reinterpretation frame:
  candidate
  secondary_retained
  reactivated
```

これは固定された身分ではなく、B文脈・policy・context shiftによって変わる状態履歴である。

---

## ■ 4. transition

```text
candidate → selected:
  trigger = policy_or_threshold_view

candidate → secondary_retained:
  trigger = policy_or_threshold_view

secondary_retained → reactivated:
  trigger = context_B_or_policy_shift

selected → retained_alternative:
  trigger = B_or_policy_view_change
```

すべてのtransitionは候補を削除せず、truthも付与しない。

---

## ■ 5. 停止線

```text
state
≠ truth

transition
≠ deletion
≠ finalization

reactivated
≠ selected

selected
≠ true

lifecycle map
≠ Core primitive
≠ T2 finalization
```

---

## ■ 6. 暫定結論

699〜748では、候補ライフサイクル地図を作った。

```text
候補は生成されて終わらない
候補は選択されても閉じない
候補は低weightでも消えない
候補は後続条件で再活性化し得る
```

Music側では、候補を「正解/不正解」で消費するのではなく、文脈・B・policyに応じて状態を変える解釈資源として扱うのがよい。

```text
次ξ:
  reactivated_to_selection_boundary_stress
```

---

## ■ 7. まだ言えないこと

```text
lifecycle mapが最終形であること
reactivated候補をいつselectionへ渡すか
候補記憶の上限が決まったこと
全Module候補に同じライフサイクルが適用できること
Core側へ接続すべきか判断できたこと
T2候補として確定したこと
```

これらは未解決ξとして残す。
