# Music v0.2 旋律×拍節 duration articulation分離 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/Melody_Meter/Music_v0.2_旋律拍節_duration_articulation分離_最小ループ.md
10_Music_Validation/Melody_Meter/music_v02_melody_meter_duration_articulation_probe.py
artifacts/json/music_v02_melody_meter_duration_articulation_probe.json
```

## 1. 抽出主題

syncopation位相分離で分けた `onset_phase` と `note_accent` に対して、今回は duration articulation を分ける。

```text
duration_articulation
  ≠ onset_phase
  ≠ note_accent
```

音楽状態は、音の開始位置だけでなく、音が次のonsetまでどのように残るかによっても変わる。

## 2. 保存されるもの

```text
melody:
  C4 D4 E4 G4 E4 D4 C4 G3

contour:
  up up up down down down down

onset_positions:
  0 1 2 3 4 5 6 7

note_accent_indices:
  0, 4

meter_reference:
  4/4 click grid
```

## 3. 変化するもの

```text
staccato_gap:
  note ends well before next onset

detached_reference:
  note leaves a short rest before next onset

connected_tenuto:
  note fills the inter-onset interval

overlap_legato:
  note continues beyond the next onset

entailed_vertical_overlap:
  duration extension makes neighboring pitches briefly simultaneous
```

## 4. 候補状態

```text
detached_reference_same_onsets:
  duration_reference_candidate

staccato_gap_same_onsets:
  staccato_gap_candidate

tenuto_connected_same_onsets:
  connected_tenuto_candidate

overlap_legato_same_onsets:
  overlap_legato_candidate
```

## 5. Music Core v0.2へ返す命題

```text
same onset positions
  ≠ same melodic-metric state

duration articulation is a relation between neighboring events,
not merely a rendering parameter.

one primary duration intervention may entail secondary relation changes,
such as local vertical simultaneity.
```

旋律同一性は、点としてのonset列だけではなく、onset間に残る余白・接続・重なりでも変化する。ただし、overlapで生じる局所的同時発音は、ただちに和声状態へのcommitmentではない。

## 6. syncopation位相分離からの差分

```text
syncopation位相分離:
  meter fixed
  + onset phase changed
  + note accent optionally changed

duration articulation分離:
  meter fixed
  + onset positions fixed
  + note accent fixed
  + duration / gap / overlap changed
```

syncopationでは「音がmeter gridのどこへ入るか」が主題だった。今回のduration articulationでは、「入った音が次の音との間に何を残すか」が主題になる。

## 7. 停止線

```text
duration_articulation_is_not_identical_to_onset_phase
duration_thresholds_are_fixture_parameters_not_universal_articulation_constants
primary_duration_intervention_is_not_identical_to_entailed_vertical_overlap
staccato_gap_is_not_deletion_of_melody_identity
overlap_legato_is_not_harmonic_state_commitment
click_track_is_device_fixture_not_human_meter_confirmation
actual_listening_observation_remains_null_until_recorded
```

この抽出は、実聴取上のstaccato / tenuto / legato感を断定しない。現段階では、Music fixtureとして候補状態を実聴取へ渡す。
