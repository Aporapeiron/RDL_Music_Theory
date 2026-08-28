# selection record update と alternative memory 899〜948 構造抽出版

## 位置づけ

849〜898の post-selection lifecycle から、選択後record更新と代替候補memory保持を分離した境界である。

この構造は、選択を終端確定に変換せず、selected record の更新と unselected alternative の保持を同時に扱うための層である。

## 位相

```text
source_reentry
↓
update_request
↓
update_layer
↓
memory_layer
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

849〜898で得られた post-selection lifecycle record を再入する。

```text
selected_label = A minor reinterpretation frame
current_state = selected_after_reactivation
retained_alternatives = C major continuation frame
next_open_states = future_reinterpretation / B_shift_reentry / policy_comparison
```

## update_request

selection record update request は作るが、以下とは同一視しない。

```text
update ≠ truth assertion
update ≠ history overwrite
update ≠ alternative deletion
```

## update_layer

更新recordは、選択後状態を記録するための層である。

```text
selected_label
previous_state
updated_state
controller_trace
update_reason
overwrites_history = False
asserts_truth = False
```

この層は、選択済み候補の履歴を進めるが、過去の候補状態や分岐履歴を上書きしない。

## memory_layer

alternative memory は、未選択候補を保持するための層である。

```text
label = C major continuation frame
memory_role = retained_alternative_memory
retained_from_state = retained_alternative
retained_for =
  - future_context_shift
  - B_shift_reentry
  - policy_comparison
erased_by_update = False
error_classified = False
```

ここでは未選択候補を、棄却候補ではなく、後続文脈で再活性化されうる音楽的memoryとして扱う。

## bundle

update layer と memory layer は、selection update memory bundle として束ねられる。

```text
selection update
+
alternative memory
+
open reentry states
+
stop lines
```

ただし、このbundle自体は final resolution ではない。

## integrity

保持された整合条件は以下である。

```text
update_record_separated_from_memory = True
alternative_memory_preserved = True
update_does_not_overwrite_history = True
update_does_not_assert_truth = True
open_reentry_states_preserved = True
generated_mutation = False
```

## non_identity

899〜948で保持された非同一性は以下である。

```text
record update ≠ alternative memory
record update ≠ candidate mutation
alternative memory ≠ selection
alternative memory ≠ rejection
bundle ≠ final resolution
```

## music_subject

音楽的には、選択後のA minor reinterpretation frameと、未選択のC major continuation frameが同時に履歴へ残る。

これは「一つを選んだので他方を消す」ではなく、「現在文脈では一方を選び、他方を別文脈・別B・別policyで再解釈可能なmemoryとして残す」構造である。

## 次の境界

899〜948の次の ξ は以下である。

```text
alternative_memory_limit_stress
```

次は、alternative memory を無制限に残し続けるのではなく、どの条件で保持制限・圧縮・優先順位付けが必要になるかを検査する。
