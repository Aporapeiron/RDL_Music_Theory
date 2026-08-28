# polyphonic memory coordination 1299〜1348 構造抽出版

## 位置づけ

1249〜1298で保持された並行variation memory trackを、polyphonic memoryとして協調させる境界である。

この構造は、複数trackのcue exchangeを許しながら、track merge、sync collapse、interference erasureを止める。

## 位相

```text
source_reentry
↓
coordination_request
↓
signal_layer
↓
signal_guard
↓
track_state_layer
↓
track_guard
↓
coordination_view
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

1249〜1298の parallel variation memory を再入する。

```text
primary_variation_sequence
B_coloring_derivative_sequence
contextual_echo_derivative_sequence
```

## coordination_request

polyphonic coordination request は以下を止める。

```text
coordination ≠ merge
coordination ≠ sync collapse
interference ≠ erasure
```

## signal_layer

coordination signal は以下である。

```text
anchor_reference_signal
cadential_alignment_signal
B_coloring_feedback_signal
latent_echo_pressure_signal
```

signal は、track間の関係を作るが、track equivalence や truth claim ではない。

## track_state_layer

各trackは協調状態を持つ。

```text
primary track
  synchronization = loosely_aligned_not_synchronized
  interference = receives_controlled_interference

derivative track
  synchronization = asynchronous_derivative_alignment
  interference = feeds_coloring_difference

latent track
  synchronization = background_asynchronous
  interference = latent_pressure_retained
```

## coordination_view

coordination mode は以下である。

```text
loose_coordination_with_controlled_interference
```

これは、完全同期ではなく、非合流なpolyphonyとして保持される。

## integrity

確認された整合条件は以下である。

```text
coordination_preserves_tracks = True
coordination_is_not_sync_collapse = True
interference_is_retained_not_erased = True
latent_track_remains_background = True
signals_do_not_assert_equivalence = True
generated_mutation = False
```

## non_identity

1299〜1348で保持された非同一性は以下である。

```text
coordination ≠ merge
coordination ≠ sync
interference ≠ erasure
polyphony ≠ single voice
```

## music_subject

polyphonic memory は、単に複数の候補が並んでいる状態ではない。

各trackが同じanchorを参照しながら、別々の時間感、別々の文脈圧、別々の干渉を持つ。協調はそれらを一つにまとめるのではなく、差異を残したまま互いの聞こえを調整する。

## 次の境界

1299〜1348の次の ξ は以下である。

```text
coordination_resolution_pressure_stress
```

次は、協調が強くなったときに発生するresolution pressureを、mergeやsync collapseにせずどう保持するかを検査する。
