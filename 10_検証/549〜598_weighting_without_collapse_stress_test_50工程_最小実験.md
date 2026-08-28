# 検証記録：weighting without collapse stress test 50工程

*対象：499〜548で観測したB依存選択差に、weight viewを付ける*  
*状態：DRAFT v0.1 / Music weighting without collapse stress test*  
*実装：`10_検証/weighting_without_collapse_549_598.py`*

---

## ■ 0. 検証目的

499〜548では、同じ候補集合でもB文脈によってpolicy originとselected labelが変わることを確認した。

549〜598では、同じ候補集合にweightを付ける。

```text
same prediction candidates
  ↓
B-dependent weighting view
  ↓
support_weight
+ retention_weight
  ↓
highest weight can differ
  ↓
all candidates retained
```

目的は、weightを確率・真理・削除条件へ圧縮しないことである。

---

## ■ 1. 観測した50工程

```text
549 reuse_499_548_B_policy_selection
550 next_xi_received
551 same_candidate_set_recheck
552 weight_view_request
553 weight_not_probability_guard
554 weight_not_truth_guard
555 weight_not_deletion_guard
556 weight_not_selection_generator_guard
557 analysis_weight_view
558 performance_weight_view
559 listener_weight_view
560 composition_weight_view
561 weight_source_per_B
562 B_weight_non_universal_guard
563 continuation_support_weight
564 reinterpretation_support_weight
565 retention_weight_for_selected_path
566 retention_weight_for_alternative_path
567 weight_not_confidence_guard
568 weight_not_certainty_guard
569 analysis_highest_weight
570 performance_highest_weight
571 listener_highest_weight
572 composition_highest_weight
573 highest_weight_differs_by_B
574 ranking_not_selection_guard
575 analysis_candidate_retention
576 performance_candidate_retention
577 listener_candidate_retention
578 composition_candidate_retention
579 low_weight_not_error_guard
580 low_weight_not_deletion_guard
581 weight_record_schema
582 support_vs_retention_weight_split
583 weight_source_trace
584 weight_view_not_source_record_mutation
585 weight_vs_policy_split
586 weight_vs_score_split
587 weight_vs_probability_split
588 weight_vs_truth_split
589 music_preference_gradient
590 ambiguity_not_flattened
591 performance_listener_difference
592 weighting_surface_summary
593 no_collapse_summary
594 alternative_retention_summary
595 no_mutation_summary
596 threshold_policy_open_xi
597 real_evidence_weight_origin_open_xi
598 next_xi_selection
```

---

## ■ 2. 実行結果

```text
weighting_without_collapse_549_598_observed_without_turning_weight_into_probability_or_truth
```

確認したこと。

```text
step_count = 50
first_step = 549
last_step = 598
weight_varies_by_B = True
highest_weight_can_differ = True
all_candidates_retained = True
weight_is_probability = False
weight_is_truth = False
weight_generates_selection = False
generated_mutation = False
```

---

## ■ 3. B別weight view

```text
analysis_B:
  C major continuation = 0.72
  A minor reinterpretation = 0.38

performance_B:
  C major continuation = 0.41
  A minor reinterpretation = 0.76

listener_B:
  C major continuation = 0.66
  A minor reinterpretation = 0.44

composition_B:
  C major continuation = 0.45
  A minor reinterpretation = 0.81
```

highest weightはBによって変わる。

---

## ■ 4. support / retention 分離

```text
support_weight:
  そのB文脈における支持の強さ

retention_weight:
  候補を後続検査へ残す強さ
```

この二つを分けることで、低support候補でも削除されない。

---

## ■ 5. 停止線

```text
weight
≠ probability
≠ truth
≠ confidence
≠ certainty
≠ deletion condition
≠ selection generator

highest weight
≠ selected truth

low weight
≠ error
≠ deletion target
```

---

## ■ 6. 暫定結論

549〜598では、B依存選択差に対してweight viewを付けても、候補空間が潰れないことを確認した。

```text
weightは付く
rankingも見える
しかし候補は消えない
```

Music側では、weightは曖昧性を消すためではなく、曖昧性の内部構造を読むためのviewとして扱うのがよい。

```text
次ξ:
  threshold_policy_and_low_weight_retention_stress
```

---

## ■ 7. まだ言えないこと

```text
weight値の実証的由来があること
weightを確率へ変換できること
threshold policyが妥当であること
低weight候補をいつ削除してよいか
聴取者Bごとのweight差が測定されたこと
演奏・作曲上のweightが同じ形式で扱えること
Core側へ接続すべきか判断できたこと
```

これらは未解決ξとして残す。
