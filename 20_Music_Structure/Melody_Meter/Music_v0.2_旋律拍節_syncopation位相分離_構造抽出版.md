# Music v0.2 旋律×拍節 syncopation位相分離 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/Melody_Meter/Music_v0.2_旋律拍節_syncopation位相分離_最小ループ.md
10_Music_Validation/Melody_Meter/music_v02_melody_meter_syncopation_probe.py
artifacts/json/music_v02_melody_meter_syncopation_probe.json
```

## 1. 抽出主題

pre-roll付きpickupで分けた拍節関係を、syncopation候補へ移す。

```text
note_accent_displacement
  ≠ onset_phase_displacement
```

拍節状態は、どの音が強いかだけでなく、音の開始位置がmeter gridのどのphaseへ入るかでも変わる。

## 2. 保存されるもの

```text
melody:
  C4 D4 E4 G4 E4 D4 C4 G3

contour:
  up up up down down down down

meter_reference:
  4/4 click grid

downbeat_origin:
  0
```

## 3. 変化するもの

```text
note_accent_displacement:
  amplitude accent moves while onset phase remains on beat

onset_phase_displacement:
  note onset moves to the offbeat while meter reference remains fixed

combined_displacement:
  offbeat onset and note accent support the same displaced relation
```

## 4. 候補状態

```text
onbeat_accent_aligned_reference:
  aligned_onbeat_reference_candidate

accent_displaced_onbeat_onsets:
  accent_only_syncopation_candidate

offbeat_onsets_without_note_accent:
  onset_phase_syncopation_candidate

offbeat_onsets_with_note_accent:
  onset_accent_syncopation_candidate
```

## 5. Music Core v0.2へ返す命題

```text
syncopation candidate
  ≠ note accent displacement alone

onset phase is a relation to meter,
not just a rendering detail.
```

旋律同一性を保っても、onset phaseが変わると melodic-metric state candidate は変わる。

## 6. pre-roll付きpickupからの差分

```text
pre-roll付きpickup:
  melody entry before downbeat
  + pulse / bar-phase history
  + meter phase continuity

syncopation位相分離:
  meter reference fixed
  + local onset phase shift
  + optional note accent support
```

弱起では「旋律が拍節場へどこから入るか」が主題だった。今回のsyncopationでは、旋律が始まった後の各onsetが、固定されたmeter referenceのどのphaseへ入るかが主題になる。

## 7. 停止線

```text
syncopation_candidate_is_not_identical_to_note_accent_displacement
onset_phase_displacement_is_not_identical_to_note_accent
meter_reference_is_fixed_across_frames
click_track_is_device_fixture_not_human_meter_confirmation
actual_listening_observation_remains_null_until_recorded
```

この抽出は、実聴取上のsyncopation感を断定しない。現段階では、Music fixtureとして候補状態を実聴取へ渡す。
