# 検証記録：policy origin と B依存選択 stress test 50工程

*対象：449〜498で作った複数解釈record schemaに、B文脈ごとのpolicyを通す*  
*状態：DRAFT v0.1 / Music B-dependent policy stress test*  
*実装：`10_検証/policy_origin_B_dependent_selection_499_548.py`*

---

## ■ 0. 検証目的

449〜498では、選択済み候補と未選択候補を同じrecord schemaへ保存した。

499〜548では、その候補集合を、複数のB文脈から来るpolicyへ通す。

```text
same prediction candidates
  ↓
analysis_B policy
performance_B policy
listener_B policy
composition_B policy
  ↓
B-dependent selection difference
```

目的は、Bを真理条件へ昇格することではない。B文脈が違うと、同じ候補集合に対する選択policyの由来と選択結果が変わり得ることを検査する。

---

## ■ 1. 観測した50工程

```text
499 reuse_449_498_record_schema
500 next_xi_received
501 record_schema_recheck
502 analysis_B_context_request
503 performance_B_context_request
504 listener_B_context_request
505 composition_B_context_request
506 B_not_truth_guard
507 B_not_candidate_generator_guard
508 analysis_policy_origin
509 performance_policy_origin
510 listener_policy_origin
511 composition_policy_origin
512 origin_not_Core_guard
513 origin_not_universal_guard
514 analysis_policy_build
515 performance_policy_build
516 listener_policy_build
517 composition_policy_build
518 policy_criteria_externalized
519 policy_not_generator_guard
520 analysis_selection_application
521 performance_selection_application
522 listener_selection_application
523 composition_selection_application
524 same_candidate_set_reuse
525 selection_difference_observation
526 selection_not_truth_guard
527 analysis_alternative_retention
528 performance_alternative_retention
529 listener_alternative_retention
530 composition_alternative_retention
531 retention_not_error_guard
532 B_vs_policy_split
533 policy_vs_selection_split
534 selection_vs_record_split
535 B_vs_module_split
536 record_schema_reuse
537 selected_label_update_as_view
538 retained_labels_update_as_view
539 source_record_not_mutated_guard
540 analysis_performance_difference
541 listener_composition_difference
542 music_use_case_specificity
543 B_dependent_policy_summary
544 selection_difference_summary
545 alternative_retention_summary
546 no_mutation_summary
547 weighting_without_collapse_next_candidate
548 next_xi_selection
```

---

## ■ 2. 実行結果

```text
policy_origin_B_dependent_selection_499_548_observed_without_treating_B_as_truth
```

確認したこと。

```text
step_count = 50
first_step = 499
last_step = 548
distinct_policy_origins_preserved = True
B_changes_selection = True
B_does_not_generate_candidates = True
alternative_retention_preserved = True
record_schema_reused = True
treats_B_as_truth = False
generated_mutation = False
```

---

## ■ 3. B文脈とpolicy origin

```text
analysis_B:
  policy_origin = theoretical_continuity_reading
  selected = C major continuation frame

performance_B:
  policy_origin = expressive_reaccentuation_reading
  selected = A minor reinterpretation frame

listener_B:
  policy_origin = local_expectation_reading
  selected = C major continuation frame

composition_B:
  policy_origin = future_pivot_potential_reading
  selected = A minor reinterpretation frame
```

同じ候補集合でも、B文脈によって選択が変わる。

---

## ■ 4. 保持した非同一性

```text
B
≠ truth
≠ candidate generator
≠ module

policy origin
≠ Core primitive
≠ universal rule

policy
≠ candidate generator

selection
≠ truth
≠ record mutation
```

---

## ■ 5. record schemaの扱い

449〜498のrecord schemaは再利用した。

```text
source record
  ↓
B-dependent policy view
  ↓
selected_label view changes
retained_labels view preserved
```

つまり、B依存選択は元recordを破壊するmutationではなく、同じ候補集合に対するview差として扱う。

---

## ■ 6. 暫定結論

499〜548では、policy originとB依存選択差を観測した。

```text
同じ候補集合
同じrecord schema
同じ停止線

しかし

B文脈が違うと
policy originとselected labelが変わる
```

これにより、Music側では policy を単一の正解規則ではなく、分析・演奏・聴取・作曲などのB文脈に依存する選択境界として扱える。

```text
次ξ:
  weighting_without_collapse_stress
```

---

## ■ 7. まだ言えないこと

```text
B文脈の分類が十分であること
policy originが実データから導出できること
weightを確率として扱えること
選択差が聴取実験で確認されたこと
演奏Bと作曲Bの差を一般化できること
未選択候補の重みづけ方式が決まったこと
Core側へ接続すべきか判断できたこと
```

これらは未解決ξとして残す。
