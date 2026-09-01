# Music v0.2 検証記録：旋律×拍節 syncopation位相分離 最小ループ

*状態：DRAFT v0.1 / pre-roll付きpickup fixture後の次対象*
*実装：`10_Music_Validation/Melody_Meter/music_v02_melody_meter_syncopation_probe.py`*

## 0. 目的

pre-roll付きpickupでは、弱起を `pickup_offset`、`pulse_history`、`audible_bar_phase_history`、`meter_phase_continuity` に分けた。

今回は、同じ旋律材料を使い、4/4のmeter referenceを固定したまま、syncopation候補を次の二つへ分ける。

```text
note_accent_displacement
  ≠ onset_phase_displacement
```

つまり、強く鳴る位置がずれることと、音の開始位置そのものが拍の間へ入ることを同一視しない。

## 1. 境界B

```text
B_melody_meter_syncopation_probe:
  preserved_melody = C4 D4 E4 G4 E4 D4 C4 G3
  preserved_contour = up up up down down down down
  fixed_meter_reference = 4/4 click grid
  fixed_downbeat_origin = 0
  changed_relations:
    note accent displacement
    onset phase displacement
```

今回保存するのは旋律の音高列・輪郭・音価・meter referenceである。変えるのは、note accentの位置と、onset phaseである。

## 2. 検証状態

### 2.1 onbeat_accent_aligned_reference

```text
onset_phase = 0.0
note_accent_indices = 0, 4
classification = aligned_onbeat_reference_candidate
```

音の開始位置とnote accentが4/4のdownbeatと揃う参照状態である。

### 2.2 accent_displaced_onbeat_onsets

```text
onset_phase = 0.0
note_accent_indices = 1, 5
classification = accent_only_syncopation_candidate
```

onsetは拍上に残したまま、note accentだけをずらす。

### 2.3 offbeat_onsets_without_note_accent

```text
onset_phase = 0.5
note_accent_indices = none
classification = onset_phase_syncopation_candidate
```

note accentを加えず、音の開始位置だけを拍の中間へずらす。

### 2.4 offbeat_onsets_with_note_accent

```text
onset_phase = 0.5
note_accent_indices = 0, 4
classification = onset_accent_syncopation_candidate
```

offbeat onsetとnote accentが同じ変位関係を支える候補である。

## 3. 生成artifact

```text
artifacts/audio/music_v02_melody_meter_syncopation_probe.wav
artifacts/json/music_v02_melody_meter_syncopation_probe.json
```

音声は4状態を順に鳴らすdevice-side fixtureである。

## 4. 実聴取slot

今回も `actual_listening_observation = null` として保持する。

```text
structural prediction
  ≠ perceptual hypothesis
  ≠ actual listening observation
```

syncopation候補が実際にどの程度「シンコペーション」として聞こえるかは、実聴取で別に記録する。

## 5. Music上の仮説

```text
same melodic contour
+ fixed meter reference
+ changed note accent / onset phase
-> different melodic-metric candidate state
```

syncopationは、note accentの変位だけではなく、onset phaseがmeter gridに対してどこへ入るかによっても成立しうる。

## 6. 停止線

```text
syncopation_candidate_is_not_identical_to_note_accent_displacement
onset_phase_displacement_is_not_identical_to_note_accent
meter_reference_is_fixed_across_frames
click_track_is_device_fixture_not_human_meter_confirmation
actual_listening_observation_remains_null_until_recorded
```
