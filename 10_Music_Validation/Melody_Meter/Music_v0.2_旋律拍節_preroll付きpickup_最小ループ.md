# Music v0.2 検証記録：旋律×拍節 pre-roll付きpickup 最小ループ

*状態：DRAFT v0.1 / meter-accent-pickup分離後のmeter history検査*  
*実装：`10_Music_Validation/Melody_Meter/music_v02_melody_meter_preroll_pickup_probe.py`*

## 0. 目的

前回は、`meter_reference`、`note_accent`、`pickup_offset` を分離した。

しかし、弱起をより音楽的に扱うには、旋律が始まる前に拍節場が成立しているかどうかが重要になる。

```text
local pickup offset
  = melody onset before next downbeat

meter history
  = melody begins after an already audible meter field
```

今回は、pre-roll clicksを使い、旋律開始前に拍節参照を鳴らす。

## 1. 保存されるもの

```text
melody:
  C4 D4 E4 G4 E4 D4 C4 G3

durations:
  1 1 1 1 1 1 1 1

contour:
  up up up down down down down
```

## 2. 検証状態

### 2.1 no_preroll_local_pickup

```text
preroll_beats = 0
melody_entry_beat = 0
first_downbeat_after_entry = 1
```

弱起関係は局所的に作られるが、旋律前の拍節履歴はない。

### 2.2 two_beat_preroll_pickup

```text
preroll_beats = 2
melody_entry_beat = 2
first_downbeat_after_entry = 3
```

2拍のclickが先に鳴り、その後C4がdownbeat前に入る。

### 2.3 four_beat_preroll_pickup

```text
preroll_beats = 4
melody_entry_beat = 4
first_downbeat_after_entry = 5
```

1小節分の拍節場を先に作ってから、C4をpickupとして入れる。

### 2.4 four_beat_preroll_downbeat_entry

```text
preroll_beats = 4
melody_entry_beat = 4
first_downbeat_after_entry = 4
```

同じpre-rollがあっても、C4がdownbeat上に入るcontrolである。

## 3. 生成artifact

```text
artifacts/audio/music_v02_melody_meter_preroll_pickup_probe.wav
artifacts/json/music_v02_melody_meter_preroll_pickup_probe.json
```

## 4. Music上の意味

この検証は、弱起を次の二層に分ける。

```text
pickup_offset:
  旋律開始が次のdownbeatより前にある

meter_history:
  旋律開始前に拍節参照がすでに聞こえている
```

したがって、弱起は単なるnote accentでも、単なる局所offsetでもなく、事前に成立した拍節場へのentryとして扱える。

## 5. 実聴取slot

今回も `actual_listening_observation = null` として保持する。

pre-roll clickはdevice fixtureであり、人間がその拍節場を実際に採用した証拠ではない。

## 6. 停止線

```text
meter_history_is_not_identical_to_local_pickup_offset
pre_roll_clicks_are_device_fixture_not_human_meter_confirmation
pickup_candidate_is_not_actual_listening_observation
actual_listening_observation_remains_null_until_recorded
```