# Music v0.2 検証記録：旋律×拍節 duration articulation分離 最小ループ

*状態：DRAFT v0.1 / syncopation位相分離後の次対象*
*実装：`10_Music_Validation/Melody_Meter/music_v02_melody_meter_duration_articulation_probe.py`*

## 0. 目的

syncopation位相分離では、`note_accent_displacement` と `onset_phase_displacement` を分けた。

今回は、onset位置・meter reference・note accentを固定したまま、音価と余白だけを変える。

```text
duration_articulation
  ≠ onset_phase
  ≠ note_accent
```

つまり、音がいつ始まるかではなく、始まった音がどこまで持続し、次のonsetまでどんな余白や重なりを作るかを見る。

## 1. 境界B

```text
B_melody_meter_duration_articulation_probe:
  preserved_melody = C4 D4 E4 G4 E4 D4 C4 G3
  preserved_contour = up up up down down down down
  preserved_onset_positions = 0 1 2 3 4 5 6 7
  preserved_note_accent_indices = 0, 4
  fixed_meter_reference = 4/4 click grid
  changed_relations:
    note duration
    inter-onset gap
    overlap carry-over
```

今回保存するのは、旋律の音高列・輪郭・onset位置・note accent・meter referenceである。変えるのは、音価が次のonsetまでに作る余白または重なりである。

## 2. 検証状態

### 2.1 detached_reference_same_onsets

```text
note_duration_beats = 0.72
inter_onset_gap_beats = 0.28
classification = duration_reference_candidate
```

同じonset grid上で、短い余白を持つ参照状態である。

### 2.2 staccato_gap_same_onsets

```text
note_duration_beats = 0.36
inter_onset_gap_beats = 0.64
classification = staccato_gap_candidate
```

onsetは変えず、音価だけを短くして、次の音までの無音関係を強くする。

### 2.3 tenuto_connected_same_onsets

```text
note_duration_beats = 1.0
inter_onset_gap_beats = 0.0
classification = connected_tenuto_candidate
```

onset間隔をちょうど埋め、余白も重なりも作らない接続状態である。

### 2.4 overlap_legato_same_onsets

```text
note_duration_beats = 1.16
inter_onset_gap_beats = -0.16
classification = overlap_legato_candidate
```

onsetは変えず、前の音が次のonsetへ持ち越される重なりを作る。

## 3. 生成artifact

```text
artifacts/audio/music_v02_melody_meter_duration_articulation_probe.wav
artifacts/json/music_v02_melody_meter_duration_articulation_probe.json
```

音声は4状態を順に鳴らすdevice-side fixtureである。

## 4. 実聴取slot

今回も `actual_listening_observation = null` として保持する。

```text
structural prediction
  ≠ perceptual hypothesis
  ≠ actual listening observation
```

staccato、tenuto、legatoが実聴取上どの程度そう聞こえるかは、actual listeningで別に記録する。

## 5. Music上の仮説

```text
same melodic contour
+ fixed onset positions
+ fixed meter reference
+ changed duration articulation
-> different melodic-metric candidate state
```

旋律同一性は、音が始まる位置だけでなく、次の音までの余白・接続・重なりによっても変わる。

## 6. 停止線

```text
duration_articulation_is_not_identical_to_onset_phase
staccato_gap_is_not_deletion_of_melody_identity
overlap_legato_is_not_harmonic_state_commitment
click_track_is_device_fixture_not_human_meter_confirmation
actual_listening_observation_remains_null_until_recorded
```
