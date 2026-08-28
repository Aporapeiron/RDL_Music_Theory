# memory reactivation priority 999〜1048 構造抽出版

## 位置づけ

949〜998で圧縮保持された latent memory が、後続文脈で active view へ戻る優先度境界である。

この構造は、compressed memory を消えた候補ではなく、文脈変化によって再び前景化しうる音楽的記憶として扱う。

## 位相

```text
source_reentry
↓
trigger_setup
↓
trigger_guard
↓
priority_request
↓
evaluation_layer
↓
promotion_view
↓
latent_remainder
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

949〜998の memory limit bundle を再入する。

```text
active memory = 2
compressed latent memory = 2
```

再活性化の対象は compressed latent memory である。

## trigger_setup

再活性化のtriggerは、単独の内部操作ではなく、音楽的文脈変化から発生する。

```text
context shift
B shift
cadential return
```

今回の主triggerは以下である。

```text
altered_B_with_cadential_return
```

## trigger_guard

trigger は以下とは同一視されない。

```text
trigger ≠ truth
trigger ≠ repetition
trigger ≠ selection
```

## priority_request

reactivation priority は、compressed memory をactive viewへ戻す候補優先度である。

これは選択確定ではなく、候補の前景復帰可能性を上げる操作である。

## evaluation_layer

compressed memory 2件を評価する。

```text
C major continuation frame under altered B
  previous = compressed_latent_memory
  new = reactivation_priority_candidate
  returns_to_active_view = True
  reinterpreted = True
  selected = False
  deleted = False

C major continuation frame for policy audit
  previous = compressed_latent_memory
  new = latent_memory_retained
  returns_to_active_view = False
  reinterpreted = False
  selected = False
  deleted = False
```

## promotion_view

promoted memory は active view に戻るが、selection されたわけではない。

```text
active return ≠ selection
```

ここでの回帰は refrain return として観測される。

## latent_remainder

active viewへ戻らなかった compressed memory は、rejection や deletion ではなく、latent remainder として保持される。

```text
remaining latent memory ≠ rejection
remaining latent memory ≠ deletion
```

## integrity

確認された整合条件は以下である。

```text
compressed_memory_was_reconsidered = True
reactivation_is_not_selection = True
refrain_is_not_repetition = True
reactivation_preserves_reinterpretation = True
latent_remainder_preserved = True
generated_mutation = False
```

## non_identity

999〜1048で保持された非同一性は以下である。

```text
reactivation ≠ selection
refrain ≠ repetition
priority ≠ truth
promotion ≠ deletion
latent remainder ≠ rejection
```

## music_subject

リフレイン的回帰は、単なる同一反復ではない。

以前の音楽的読みは潜在memoryとして不在期間を持ち、その後のB変化や終止的文脈によって再び前景化する。そのとき、戻ってきたものは過去と同じlabelを持ちながら、現在文脈によって再解釈される。

したがって、聞こえの上での「戻ってきた」は、構造上は `latent memory → reactivation priority → active return candidate` として扱われる。

## 次の境界

999〜1048の次の ξ は以下である。

```text
refrain_identity_boundary_stress
```

次は、リフレイン的回帰において「同じものが戻った」と言える条件と、「似ているが別のもの」と扱う条件の境界を検査する。
