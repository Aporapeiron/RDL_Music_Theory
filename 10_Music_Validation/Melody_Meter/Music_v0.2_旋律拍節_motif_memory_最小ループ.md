# Music v0.2 検証記録：旋律×拍節 motif memory 最小ループ

*状態：DRAFT v0.1 / duration articulation実聴取前小括後の次対象*
*実装：`10_Music_Validation/Melody_Meter/music_v02_melody_meter_motif_memory_probe.py`*

## 0. 目的

duration articulationまでは、主に隣接音どうしの局所時間関係を扱った。

今回はスケールを少し広げ、同じmotif断片が再び現れるとき、再帰時刻・間隔・間に挟まる材料によって記憶状態候補が変わるかを見る。

```text
same motif material
  ≠ same return timing
  ≠ same motif-memory state
```

## 1. 境界B

```text
B_melody_meter_motif_memory_probe:
  preserved_motif = C4 D4 E4 G4
  preserved_motif_durations = 1 1 1 1
  preserved_motif_contour = up up up
  fixed_meter_reference = 4/4 click grid
  primary_interventions:
    return start time
    intervening material
  derived_relations:
    return gap
    return phase
  entailed_condition:
    memory condition before return
```

今回保存するのは、戻ってくるmotifそのものの音高列・長さ列・輪郭である。一次介入として変えるのは、motifのreturn start timeと、戻る前に鳴るintervening materialである。return gapとreturn phaseは、固定meter内でreturn start timeから派生する。

## 2. 検証状態

### 2.1 immediate_return_bar_aligned

```text
return_gap_beats = 0
return_phase = 0
classification = immediate_repetition_candidate
```

motifがすぐ次の小節頭に戻る。記憶というより、直接反復の候補である。

### 2.2 delayed_return_after_filler

```text
return_gap_beats = 4
return_phase = 0
classification = delayed_motif_return_candidate
```

1小節分のfillerを挟んで、同じmotifが小節頭に戻る。motifは不在期間を持つ。

### 2.3 offphase_return_after_filler

```text
return_gap_beats = 2
return_phase = 2
classification = offphase_motif_return_candidate
```

同じmotifが小節頭ではなく、拍節phaseの途中で戻る。

### 2.4 transformed_filler_then_return

```text
return_gap_beats = 4
return_phase = 0
classification = contrast_supported_motif_return_candidate
```

対照的なcontourを挟んだあと、同じmotifが小節頭へ戻る。

## 3. 生成artifact

```text
artifacts/audio/music_v02_melody_meter_motif_memory_probe.wav
artifacts/json/music_v02_melody_meter_motif_memory_probe.json
```

音声は4状態を順に鳴らすdevice-side fixtureである。

## 4. 実聴取slot

今回も `actual_listening_observation = null` として保持する。

```text
structural prediction
  ≠ perceptual hypothesis
  ≠ actual listening observation
```

実際にrefrain、echo、answer、interruptionとして聞こえるかは、actual listeningで別に記録する。

## 5. Music上の仮説

```text
same motif
+ changed return timing
+ changed intervening material
-> different motif-memory candidate state
```

motif-memory candidate stateは、断片そのものだけでなく、戻るまでの不在期間、戻る拍節phase、直前に保持されている局所記憶によって条件づけられる。ここでは等式として確定しない。

## 6. 停止線

```text
same_motif_material_is_not_same_memory_state
return_timing_is_not_identical_to_motif_identity
intervening_material_is_not_erasure_of_motif_memory
motif_return_candidate_is_not_actual_refrain_perception
click_track_is_device_fixture_not_human_meter_confirmation
actual_listening_observation_remains_null_until_recorded
```
