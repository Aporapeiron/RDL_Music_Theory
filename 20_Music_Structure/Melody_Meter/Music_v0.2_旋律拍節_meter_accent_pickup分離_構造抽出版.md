# Music v0.2 旋律×拍節 meter / accent / pickup 分離 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/Melody_Meter/Music_v0.2_旋律拍節_meter_accent_pickup分離_最小ループ.md
10_Music_Validation/Melody_Meter/music_v02_melody_meter_pickup_separation_probe.py
artifacts/json/music_v02_melody_meter_pickup_separation_probe.json
```

## 1. 抽出主題

前回の旋律×拍節プローブで、`pickup` が `accent index shift` に潰れる破断が見えた。

今回抽出するのは、次の三者の非同一性である。

```text
meter_reference
  ≠ note_accent
  ≠ pickup_offset
```

## 2. 分離された関係

```text
meter_reference:
  click / audible grid / bar downbeat

note_accent:
  note amplitude emphasis

pickup_offset:
  melody onset before the next downbeat
```

この三つは実音上では相互作用するが、同じ関係ではない。

## 3. 状態候補

```text
downbeat_note_accent_aligned:
  meter_reference + note_accent aligned

true_one_beat_pickup:
  pickup_offset present
  first note not accented
  second note receives downbeat support

pickup_without_note_accent:
  pickup_offset present
  no note accent emphasis

accent_without_pickup:
  note accent displaced
  melody still begins on downbeat
```

## 4. Music Core v0.2へ返す命題

```text
弱起
  ≠ 最初の音を強く鳴らすこと

弱起
  = 拍節境界に対する開始位置関係

accent displacement
  ≠ pickup relation
```

したがって、旋律同一性は、音高輪郭だけでなく、拍節参照・音符強調・開始位置の関係配置で変わる。

## 5. C6 / Am7との固有差

```text
C6 / Am7で見えた結合:
  bass relation と register gravity が同時に動きやすい

Melody / Meterで見えた結合:
  meter reference, note accent, pickup offset が同じ実装に圧縮されやすい
```

この差は、単なる実装差ではなく、音楽領域ごとの関係配置の違いとして保持する。

## 6. 停止線

```text
pickup_relation_is_not_identical_to_first_note_accent
meter_reference_is_not_identical_to_note_accent_schedule
click_track_is_device_fixture_not_human_meter_confirmation
actual_listening_observation_remains_null_until_recorded
```

click trackは拍節参照を実音化するfixtureであって、実聴取の確認ではない。