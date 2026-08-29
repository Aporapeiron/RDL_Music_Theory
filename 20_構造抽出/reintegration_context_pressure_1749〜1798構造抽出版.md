# reintegration context pressure 1749〜1798 構造抽出版

## 位置づけ

1699〜1748で保持したsplit candidate reintegrationに対し、後続文脈がどの程度再統合を促すかを検査する境界である。

この構造は、context pressureをdecisionやtruthにせず、弱・中・強の圧力として観測し、forced reintegrationとindependent path deletionを止める。

## 位相

```text
source_reentry
↓
pressure_request
↓
policy_layer
↓
pressure_layer
↓
partition_layer
↓
pressure_view
↓
bundle
↓
integrity
↓
non_identity
↓
music_subject
↓
summary
↓
next_plan
```

## source_reentry

1699〜1748のreintegration candidatesを再入する。

```text
same memory reintegration candidate
ambiguous reintegration candidate
split candidate reintegration candidate
```

## pressure_request

reintegration context pressure requestは以下を止める。

```text
pressure ≠ forced reintegration
pressure ≠ context truth
pressure ≠ independent path deletion
```

## policy_layer

context pressure policyは以下を持つ。

```text
accepts_weak_pressure = True
accepts_medium_pressure = True
accepts_strong_pressure = True
preserves_ambiguity_under_pressure = True
generates_forced_reintegration = False
```

## pressure_layer

reintegration candidateはcontext pressure candidateになる。

```text
same memory reintegration
  pressure_level = weak
  pressure_source = identity_context_continuity

ambiguous reintegration
  pressure_level = medium
  pressure_source = ambiguous_later_context_pressure

split candidate reintegration
  pressure_level = strong
  pressure_source = parallel_path_recognition_pressure
```

どのcandidateもcandidate traceとcontext traceを保持し、forced reintegrationを生成しない。

## partition_layer

pressure partitionは以下である。

```text
weak_pressure_paths = 1
medium_pressure_paths = 1
strong_pressure_paths = 1
```

partitionはdecisionではなく、文脈による引力の配置である。

## integrity

確認された整合条件は以下である。

```text
pressure_candidates_cover_reintegration_candidates = True
pressure_levels_preserved = True
candidate_and_context_traces_preserved = True
pressure_not_forced_reintegration = True
no_independent_path_deletion_or_context_truth = True
generated_mutation = False
```

## non_identity

1749〜1798で保持された非同一性は以下である。

```text
pressure ≠ decision
strong pressure ≠ forced merge
context trace ≠ truth
independent path ≠ deletion
```

## music_subject

context pressureは、後続文脈が候補を引き戻す力である。

弱い圧力は同一文脈の継続として、中程度の圧力は曖昧な聞こえとして、強い圧力は戻りへの招待として保持される。ただし圧力が強くても、統合決定や独立候補削除にはしない。

## 次の境界

1749〜1798の次の ξ は以下である。

```text
context_pressure_selection_delay_stress
```

次は、文脈圧があっても選択を遅延させる条件を検査する。
