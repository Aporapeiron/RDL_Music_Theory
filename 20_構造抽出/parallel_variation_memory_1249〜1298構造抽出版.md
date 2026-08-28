# parallel variation memory 1249〜1298 構造抽出版

## 位置づけ

1199〜1248で分岐した primary / derivative / latent branch を、並行variation memoryとして保持する境界である。

この構造は、共有anchorを持つ複数系列をmergeせず、cue exchange と local memory separation を両立させる。

## 位相

```text
source_reentry
↓
parallel_request
↓
track_layer
↓
track_guard
↓
exchange_layer
↓
exchange_guard
↓
memory_partition
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

1199〜1248の branch reentry policy を再入する。

```text
reentry candidate = B_coloring_derivative_sequence
latent branch = contextual_echo_derivative_sequence
```

## parallel_request

parallel memory request は以下を止める。

```text
parallel ≠ merge
shared anchor ≠ equivalence
local memory ≠ deletion
```

## track_layer

保持されるtrackは以下である。

```text
primary_variation_sequence
B_coloring_derivative_sequence
contextual_echo_derivative_sequence
```

各trackは同じanchorを参照するが、local memory は分離される。

## exchange_layer

memory exchange boundary は以下である。

```text
anchor_reference
cadential_cue_reference
B_coloring_feedback
latent_reference
```

exchange は cue の受け渡しであり、track merge でも equivalence claim でもない。

## memory_partition

memory partition は次のように分かれる。

```text
shared_memory =
  - C_major_continuation_frame_anchor
  - cadential_position_cue

separated_memory =
  - surface_variation
  - B_coloring_derivative_return
  - contextual_echo_unheard_option
```

## integrity

確認された整合条件は以下である。

```text
parallel_tracks_preserved = True
shared_anchor_without_merge = True
local_memory_separated = True
exchange_without_equivalence = True
latent_branch_memory_preserved = True
generated_mutation = False
```

## non_identity

1249〜1298で保持された非同一性は以下である。

```text
parallel ≠ merge
shared anchor ≠ equivalence
exchange ≠ truth
separation ≠ deletion
```

## music_subject

parallel variation memory は、複数の音楽的系列が同じ記憶anchorを共有しながら、互いに別のlocal memoryを持つ状態である。

これは単なる分岐の羅列ではなく、cue exchange を許す並行的な記憶構造である。主系列、派生系列、潜在系列は、同一化されずに互いを照らし合う。

## 次の境界

1249〜1298の次の ξ は以下である。

```text
polyphonic_memory_coordination_stress
```

次は、並行memory track同士がどのように協調し、どの条件で干渉・同期・非同期を保持するかを検査する。
