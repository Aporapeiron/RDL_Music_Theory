# Music v0.2 旋律×拍節 motif memory 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/Melody_Meter/Music_v0.2_旋律拍節_motif_memory_最小ループ.md
10_Music_Validation/Melody_Meter/music_v02_melody_meter_motif_memory_probe.py
artifacts/json/music_v02_melody_meter_motif_memory_probe.json
```

## 1. 抽出主題

duration articulationまでの局所時間関係から、motifの再帰関係へスケールを広げる。

```text
same motif material
  ≠ same return timing
  ≠ same motif-memory state
```

同じ断片が戻っても、それが直接反復なのか、不在後の回帰なのか、拍節phaseをずらした割り込みなのかは異なる。

## 2. 保存されるもの

```text
motif:
  C4 D4 E4 G4

motif_durations:
  1 1 1 1

motif_contour:
  up up up

meter_reference:
  4/4 click grid
```

## 3. 変化するもの

```text
primary_interventions:
  return start time
  intervening material

derived_relations:
  return gap
  return phase

entailed_condition:
  memory condition before return
```

## 4. 候補状態

```text
immediate_return_bar_aligned:
  immediate_repetition_candidate

delayed_return_after_filler:
  delayed_motif_return_candidate

offphase_return_after_filler:
  offphase_motif_return_candidate

transformed_filler_then_return:
  contrast_supported_motif_return_candidate
```

## 5. Music Core v0.2へ返す命題

```text
motif identity
  ≠ material identity alone

motif-memory candidate state is conditioned by:
  preserved fragment
  absence interval
  intervening local memory
  derived return phase
```

同じmotif断片でも、戻り方が違えばMusic状態候補は変わる。ただし、現段階では `=` で確定せず、候補状態がこれらの関係に条件づけられると見る。

## 6. duration articulationからの差分

```text
duration articulation:
  neighboring event relation
  gap / connection / overlap

motif memory:
  mid-range temporal relation
  absence / retention / return
```

ここで扱う時間関係は、隣接音の接続ではなく、断片が不在期間を経て再び現れる関係である。

## 7. 停止線

```text
same_motif_material_is_not_same_memory_state
return_timing_is_not_identical_to_motif_identity
intervening_material_is_not_erasure_of_motif_memory
motif_return_candidate_is_not_actual_refrain_perception
click_track_is_device_fixture_not_human_meter_confirmation
actual_listening_observation_remains_null_until_recorded
```

この抽出は、実聴取上のrefrain感を断定しない。現段階では、同一motifを実聴取へ渡すためのmemory fixtureである。
