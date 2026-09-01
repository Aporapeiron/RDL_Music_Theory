# Music v0.2 旋律×拍節 pre-roll付きpickup 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/Melody_Meter/Music_v0.2_旋律拍節_preroll付きpickup_最小ループ.md
10_Music_Validation/Melody_Meter/music_v02_melody_meter_preroll_pickup_probe.py
artifacts/json/music_v02_melody_meter_preroll_pickup_probe.json
```

## 1. 抽出主題

前回の分離で、pickupはfirst note accentではなく、拍節境界に対する開始位置関係として扱われた。

今回さらに、pickupを次の二層へ分けたうえで、pre-rollから旋律中まで同じmeter phaseが継続するかを確認する。

```text
pickup_offset
  ≠ meter_history
```

## 2. 分離された関係

```text
pickup_offset:
  melody entry occurs before the next downbeat

meter_history:
  audible meter reference exists before melody entry

meter_phase_continuity:
  downbeat is computed by (beat - downbeat_origin) % beats_per_bar == 0

downbeat_entry_control:
  meter history and meter phase continuity exist, but melody starts on downbeat
```

## 3. 候補状態

```text
no_preroll_local_pickup:
  local_pickup_without_preroll_candidate

two_beat_preroll_pickup:
  preroll_supported_pickup_candidate

four_beat_preroll_pickup:
  strong_preroll_pickup_candidate

four_beat_preroll_downbeat_entry:
  preroll_downbeat_entry_control_candidate
```

## 4. Music Core v0.2へ返す命題

```text
weak pickup relation is strengthened when a meter field exists before melody entry.

しかし、meter history and meter phase continuity alone do not create pickup:
  same pre-roll + downbeat entry
  -> arrival candidate, not pickup candidate
```

したがって、弱起は `pickup_offset`、`meter_history`、`meter_phase_continuity` の相互作用として扱う必要がある。

## 5. 前回との差分

```text
meter / accent / pickup分離:
  meter_reference, note_accent, pickup_offsetを分けた

pre-roll付きpickup:
  pickup_offset, meter_history, meter_phase_continuity をさらに分けた
```

これにより、旋律×拍節では、関係が次のような階層で見える。

```text
note accent
meter reference
pickup offset
meter history
meter phase continuity
```

## 6. 停止線

```text
meter_history_is_not_identical_to_local_pickup_offset
meter_phase_continuity_is_not_optional_for_preroll_pickup
pre_roll_clicks_are_device_fixture_not_human_meter_confirmation
pickup_candidate_is_not_actual_listening_observation
actual_listening_observation_remains_null_until_recorded
```

この抽出は、実聴取を断定せず、弱起候補を実聴取へ渡すためのMusic fixtureである。