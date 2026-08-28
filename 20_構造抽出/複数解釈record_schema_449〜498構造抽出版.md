# 構造抽出：複数解釈record schema

*対象：449〜498*  
*状態：DRAFT v0.1*

## ■ 1. 接続地図

```text
399〜448 policy decision record
  ↓
multiple interpretation record schema
  ↓
selected entry
  +
retained alternative entry
  +
policy trace
  +
score trace
  +
stop lines
  +
next ξ candidates
  ↓
record without closing interpretation space
```

## ■ 2. record schema候補

```text
MultipleInterpretationRecord:
  source_status
  policy_name
  entries
  selected_label
  retained_labels
  stop_lines
  next_xi_candidates
  generated_resolution
  deleted_alternatives
  status
```

entryは、選択済み候補と未選択候補を同じ型で保持する。

```text
InterpretationRecordEntry:
  label
  role
  prediction
  harmonic_reading
  rhythm_alignment
  score
  matched_criteria
  retained_for
  status
```

## ■ 3. 50工程の位相

```text
source_reentry: 449〜451
schema_request: 452〜455
required_fields: 456〜462
selected_entry: 463〜467
alternative_entry: 468〜472
retention_purpose: 473〜476
stop_lines: 477〜481
schema_integrity: 482〜487
music_subject: 488〜491
summary: 492〜495
next_plan: 496〜498
```

## ■ 4. 保持した差

```text
selected entry:
  selected_without_resolving_future

retained alternative entry:
  retained_without_error_classification
```

つまり、selected / retained alternative は役割差であり、true / false の差ではない。

## ■ 5. 停止線

```text
selected prediction
≠ resolved future

retained alternative
≠ error

score
≠ probability

policy
≠ generator

record
≠ Core primitive
```

## ■ 6. 未解決ξ

```text
ξ_policy_origin_and_B_dependent_selection_stress
ξ_policy_origin_for_prediction_selection
ξ_weighting_without_collapse
ξ_listener_B_dependent_policy
ξ_performer_B_dependent_policy
ξ_composition_policy_vs_analysis_policy
ξ_Core_connection_diagnostic_for_record_schema
```

## ■ 7. 暫定結論

449〜498で、複数解釈を保持するrecord schema候補を抽出した。

このschemaは解釈空間を閉じず、どのpolicyで何が選ばれ、何が未選択候補として保持されたかを保存する。Music側では、曖昧性を削除せず後続工程へ渡すためのrecord境界として使える。
