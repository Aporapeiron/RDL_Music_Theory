# refrain variation lifecycle 1099〜1148 構造抽出版

## 位置づけ

1049〜1098で same with difference として成立したリフレインが、その後 variation として展開・保持・再圧縮される境界である。

この構造は、リフレインの回帰を終点にせず、同一anchorを保持したまま変奏的に生き続ける lifecycle として扱う。

## 位相

```text
source_reentry
↓
variation_request
↓
move_layer
↓
move_guard
↓
lifecycle_layer
↓
compression_view
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

1049〜1098の refrain identity bundle を再入する。

```text
refrain identity = same with difference
identity anchor = C major continuation frame anchor
```

## variation_request

variation lifecycle request は、次の崩壊を止める。

```text
variation ≠ repetition
variation ≠ new object
variation ≠ identity collapse
```

## move_layer

variation move は以下である。

```text
surface_variation
B_coloring_variation
cadential_position_variation
contextual_echo_variation
```

各moveは anchor を保持しつつ、surfaceまたはcontextを変える。

## lifecycle_layer

variation lifecycle record は以下を保持する。

```text
lifecycle_state = variation_lifecycle_after_refrain_identity
active_variations = surface_variation / cadential_position_variation
latent_variations = B_coloring_variation
compressed_variations = contextual_echo_variation
preserves_same_with_difference = True
repeats_identically = False
becomes_new_object = False
deleted_variation = False
```

## compression_view

compressed variation は削除ではない。

```text
compressed variation keeps anchor
compressed variation keeps reentry
compression ≠ deletion
```

## integrity

確認された整合条件は以下である。

```text
variation_preserves_identity_anchor = True
variation_is_not_identical_repetition = True
variation_is_not_new_object = True
lifecycle_keeps_active_and_latent = True
compression_is_not_deletion = True
generated_mutation = False
```

## non_identity

1099〜1148で保持された非同一性は以下である。

```text
variation ≠ repetition
variation ≠ new object
lifecycle ≠ final form
compression ≠ erasure
```

## music_subject

リフレインは、戻った時点で閉じるのではなく、その後もvariationとして展開する。

その展開は、聞こえの表層や文脈を変えながら、記憶上のanchorを保持する。したがって、variation lifecycle は「同じ主題の反復」でも「別主題への切断」でもなく、同一性と差異の持続的な配分として扱われる。

## 次の境界

1099〜1148の次の ξ は以下である。

```text
variation_sequence_boundary_stress
```

次は、個々のvariation moveを単発ではなく、sequenceとして並べたときに、どこで同一anchorが保たれ、どこで別系列へ分岐するかを検査する。
