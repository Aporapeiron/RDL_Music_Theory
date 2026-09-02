# Music v0.2 検証記録：旋律×拍節 duration articulation 実聴取前小括

*状態：DRAFT v0.1 / duration articulation分離後のpre-listening closure*
*対象：`music_v02_melody_meter_duration_articulation_probe.py`*

## 0. 目的

duration articulation系列を、追加のduration値へ細分化せず、一旦実聴取前closureとして閉じる。

今回返せるのは、実聴取上のstaccato / tenuto / legato断定ではなく、device-side fixture上で分離できた関係である。

## 1. 構造として返せるもの

```text
same melody
+ same contour
+ same onset positions
+ same note accent
+ same meter reference
+ changed duration articulation
-> different melodic-metric candidate state
```

ここでduration articulationは、単なるrendering parameterではなく、隣接する音事象のあいだに余白・接続・重なりを作る関係である。

## 2. 閉じる関係

```text
staccato_gap:
  duration shortens
  -> larger inter-onset rest

detached_reference:
  duration leaves short rest
  -> clear onset identity remains

connected_tenuto:
  duration fills inter-onset interval
  -> zero inter-onset rest

overlap_legato:
  duration exceeds inter-onset interval
  -> negative inter-onset gap
  -> local vertical overlap
  -> neighboring pitches briefly simultaneous
```

## 3. primary intervention と entailed changes

```text
primary intervention
  ≠ entailed relational changes
```

overlap版では、一次介入はduration extensionである。しかし、その実現により、局所的な垂直同時発音が派生する。

これはC6 / Am7の `bass intervention -> register relation change` と同型ではないが、Music内で再出現した近い型である。

```text
one music relation is changed
-> another relation may be unavoidably produced by realization
```

ただし、現段階では汎用原理として確定しない。Music内の複数領域に再出現している候補として保持する。

## 4. 実聴取まで保留するもの

```text
whether 0.36 is heard as staccato
whether 1.00 is heard as tenuto
whether 1.16 is heard as legato
whether overlap is heard as continuity or harmonic blur
whether local vertical simultaneity affects perceived melodic identity
```

duration thresholdはfixture parameterであり、普遍的なarticulation定数ではない。

## 5. 停止線

```text
pre_listening_closure_is_not_actual_listening_observation
duration_thresholds_are_fixture_parameters_not_universal_articulation_constants
primary_duration_intervention_is_not_identical_to_entailed_vertical_overlap
local_vertical_overlap_is_not_harmonic_state_commitment
do_not_extend_by_micro_duration_sweep_before_actual_listening
```

## 6. 次へ渡すもの

この系列は、実聴取slotを開いたまま一旦閉じる。

次に進む場合は、duration値の微細化ではなく、別のMusic対象へ移す。

候補は次のどちらかである。

```text
melody phrase / motif memory:
  same contour fragment
  + changed recurrence / return timing
  -> refrain or motif-memory candidate

timbre / attack:
  same pitch and onset
  + changed attack envelope / spectrum
  -> timbre-articulation candidate
```