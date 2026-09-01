# Music v0.2 旋律×拍節 輪郭保存アクセント変位 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/Melody_Meter/Music_v0.2_旋律拍節_輪郭保存アクセント変位_最小ループ.md
10_Music_Validation/Melody_Meter/music_v02_melody_meter_identity_probe.py
artifacts/json/music_v02_melody_meter_identity_probe.json
```

## 1. 抽出主題

C6 / Am7で得た命題を、旋律×拍節へ移す。

```text
保存された材料
  ≠ 保存された音楽状態
```

今回の材料は、旋律の音高列、長さ列、輪郭である。変えるのは、拍節フレームとアクセント配置である。

## 2. 保存されるもの

```text
melody:
  C4 D4 E4 G4 E4 D4 C4 G3

durations:
  1 1 1 1 1 1 1 1

contour:
  up up up down down down down
```

## 3. 変化するもの

```text
meter frame:
  4/4 stable
  8-beat 3+3+2 grouping
  4/4 with one-beat pickup shift
  4/4 with cadence accent displacement

accent relation:
  periodic balance
  asymmetric propulsion
  pickup reinterpretation
  directional descent foregrounding
```

## 4. 候補状態

```text
four_four_downbeat_stable:
  melody_identity_stable_meter_candidate

three_three_two_grouping:
  same_melody_as_metric_rephrasing_candidate

one_beat_pickup_shift:
  melody_identity_with_pickup_reinterpretation_candidate

cadence_accent_displacement:
  same_melody_with_directional_accent_candidate
```

ここでは、同じ旋律を同じ旋律名として固定しない。輪郭が同じでも、拍節配置が変わればMusic状態候補は変わる。

## 5. Music Core v0.2へ返す命題

```text
melodic contour preservation
  ≠ melodic-metric state preservation

accent placement is a relation,
not a decoration added after melody identity is fixed.
```

旋律同一性は、音高列だけでなく、どの拍節関係の中で現れるかによって変化する。

## 6. C6 / Am7からの移植差

```text
C6 / Am7:
  pitch material preserved
  bass / register / context changed

melody / meter:
  pitch contour preserved
  accent / meter / pickup relation changed
```

共通するのは「材料保存と状態保存の非同一性」である。異なるのは、状態を動かす主な関係が、低音・文脈から拍節・アクセントへ移る点である。

## 7. 停止線

```text
melodic_contour_preservation_is_not_meter_state_preservation
accent_pattern_is_structural_fixture_not_actual_hearing
candidate_classification_is_not_final_melodic_identity_truth
actual_listening_observation_remains_null_until_recorded
```

この抽出は、旋律が実際に同じものとして聞かれるかを断定しない。実聴取は後続slotで分けて記録する。