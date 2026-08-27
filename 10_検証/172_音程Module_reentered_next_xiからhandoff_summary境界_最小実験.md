# 検証記録：reentered next xiからhandoff summary境界

*実装：`10_検証/interval_module_handoff_summary_reentry.py`*

```text
reentered selected next xi
  + handoff boundary
  ↓
handoff summary candidate
```

実行結果：`handoff_summary_observed_from_reentered_next_xi_not_next_work`

handoff summaryは生成するが、次作業はまだ開始しない。
