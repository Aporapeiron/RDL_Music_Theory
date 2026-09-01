# Music v0.2 検証記録：旋律×拍節 輪郭保存アクセント変位 最小ループ

*状態：DRAFT v0.1 / C6-Am7実聴取前小括後の次対象*  
*実装：`10_Music_Validation/Melody_Meter/music_v02_melody_meter_identity_probe.py`*

## 0. 目的

C6 / Am7では、同一音集合を保存しても、低音・配置・時間文脈によって和声状態候補が変わることを見た。

今回はその型を、和声から旋律×拍節へ移す。

```text
harmony:
  same pitch-class material
  + changed relation configuration
  -> different harmonic candidate state

melody / meter:
  same melodic contour
  + changed accent / metric placement
  -> different melodic-metric candidate state
```

## 1. 境界B

```text
B_melody_meter_identity_probe:
  preserved_melody = C4 D4 E4 G4 E4 D4 C4 G3
  preserved_duration_sequence = 1 1 1 1 1 1 1 1
  preserved_contour = up up up down down down down
  changed_relations:
    meter frame
    accent positions
    pickup relation
```

ここで保存するのは、旋律ラベルではなく、音高列・長さ列・輪郭である。

## 2. 検証状態

### 2.1 four_four_downbeat_stable

```text
beats_per_bar = 4
accent_positions = 0, 4
pickup_beats = 0
classification = melody_identity_stable_meter_candidate
```

旋律は2つの4拍単位として安定する候補を持つ。

### 2.2 three_three_two_grouping

```text
beats_per_bar = 8
accent_positions = 0, 3, 6
pickup_beats = 0
classification = same_melody_as_metric_rephrasing_candidate
```

同じ輪郭が、3+3+2の非対称推進として再句読される。

### 2.3 one_beat_pickup_shift

```text
beats_per_bar = 4
accent_positions = 1, 5
pickup_beats = 1
classification = melody_identity_with_pickup_reinterpretation_candidate
```

同じ第一音が、到達ではなく弱起として読まれる候補を持つ。

### 2.4 cadence_accent_displacement

```text
beats_per_bar = 4
accent_positions = 0, 3, 7
pickup_beats = 0
classification = same_melody_with_directional_accent_candidate
```

周期的安定よりも、頂点と下降方向が前景化する。

## 3. 生成artifact

```text
artifacts/audio/music_v02_melody_meter_identity_probe.wav
artifacts/json/music_v02_melody_meter_identity_probe.json
```

音声は4状態を順に鳴らすdevice-side fixtureである。

## 4. 実聴取slot

今回も `actual_listening_observation = null` として保持する。

```text
structural prediction
  ≠ perceptual hypothesis
  ≠ actual listening observation
```

実聴取で不一致が出た場合は、E / H / θの経路へ送る。ξは存在有無ではなく、このBでなお未回収として記述される具体的関係として扱う。

## 5. Music上の仮説

```text
melodic contour preservation
  ≠ melodic-metric state preservation

同じ旋律輪郭でも、拍節配置が変わると
  stable period
  asymmetric propulsion
  pickup reinterpretation
  directional accent
として別候補になりうる。
```

これは、C6 / Am7の「材料保存と状態保存の非同一性」を、旋律×拍節へ移した最初のMusic検証である。