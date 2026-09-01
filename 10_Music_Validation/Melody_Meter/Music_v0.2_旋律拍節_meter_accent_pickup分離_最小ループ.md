# Music v0.2 検証記録：旋律×拍節 meter / accent / pickup 分離 最小ループ

*状態：DRAFT v0.1 / 輪郭保存アクセント変位後の破断修正*  
*実装：`10_Music_Validation/Melody_Meter/music_v02_melody_meter_pickup_separation_probe.py`*

## 0. 目的

前回の旋律×拍節プローブでは、`meter frame`、`accent positions`、`pickup relation` を概念上分けた。

しかしdevice audioでは、ほぼ「どのnoteを強く鳴らすか」という `accent schedule` へ圧縮されていた。特に `one_beat_pickup_shift` では、最初の音そのものがaccentedになり、弱起という構造予測とズレた。

今回は、次の三つを実音上でも分ける。

```text
meter_reference
  = 聞こえる拍節参照、downbeat click

note_accent
  = note自体の局所強調

pickup_offset
  = melodyが次のdownbeatより前に始まる位置関係
```

## 1. 保存されるもの

```text
melody:
  C4 D4 E4 G4 E4 D4 C4 G3

durations:
  1 1 1 1 1 1 1 1

contour:
  up up up down down down down
```

旋律材料は前回と同じである。

## 2. 検証状態

### 2.1 downbeat_note_accent_aligned

```text
pickup_offset_beats = 0
meter_downbeat_positions = 0, 4
note_accent_indices = 0, 4
```

拍節参照とnote accentが揃う安定状態。

### 2.2 true_one_beat_pickup

```text
pickup_offset_beats = 1
meter_downbeat_positions = 1, 5
note_accent_indices = 1, 5
```

最初のC4はdownbeat前に出る。downbeat supportは次のD4へ来る。

```text
C4 = pickup
D4 = first metrical arrival
```

### 2.3 pickup_without_note_accent

```text
pickup_offset_beats = 1
meter_downbeat_positions = 1, 5
note_accent_indices = none
```

note loudnessではなく、拍節参照だけでpickup関係を作る。

### 2.4 accent_without_pickup

```text
pickup_offset_beats = 0
meter_downbeat_positions = 0, 4
note_accent_indices = 1, 5
```

melodyはdownbeat上で始まるが、note accentだけがずれる。これは弱起ではなくsyncopation候補として保持する。

## 3. 生成artifact

```text
artifacts/audio/music_v02_melody_meter_pickup_separation_probe.wav
artifacts/json/music_v02_melody_meter_pickup_separation_probe.json
```

音声には、noteだけでなくclickによるmeter referenceを入れる。

## 4. 今回の破断修正

```text
pickup relation
  ≠ first note accent

meter reference
  ≠ note accent schedule

accent displacement
  ≠ pickup
```

弱起は、最初の音を強くすることではなく、拍節境界に対して最初の音が先行する関係として扱う。

## 5. 実聴取slot

今回も `actual_listening_observation = null` として保持する。

click trackはdevice fixtureであり、人間が実際にその拍節を採用した証拠ではない。

## 6. Music上の仮説

旋律×拍節では、C6/Am7とは違う結合問題が出る。

```text
C6 / Am7:
  bass と register が音響上連動しやすい

melody / meter:
  meter, accent, pickup が音響実装で混ざりやすい
```

この差は、Music領域ごとの固有差として保持する。