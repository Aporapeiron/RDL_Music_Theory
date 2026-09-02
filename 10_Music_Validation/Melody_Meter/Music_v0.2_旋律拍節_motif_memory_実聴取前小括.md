# Music v0.2 検証記録：旋律×拍節 motif memory 実聴取前小括

*状態：DRAFT v0.1 / motif memory分離後のpre-listening closure*
*実装：`10_Music_Validation/Melody_Meter/music_v02_melody_meter_motif_memory_pre_listening_closure.py`*

## 0. 目的

motif memory系列を、追加条件へ拡張し続けず、一旦実聴取前closureとして閉じる。

今回返せるのは、人間が実際にrefrain / echo / answerとして聞いたという断定ではなく、device-side fixture上で分離できた関係である。

## 1. 入力manifest

```text
artifacts/json/music_v02_melody_meter_motif_memory_probe.json
```

このmanifestでは、同じ `C4 D4 E4 G4` motifを保存し、return start、absence interval、return phase、sounding filler、melodic material silenceを分けている。

## 2. 実聴取前に返せる命題

```text
same_motif_material_does_not_preserve_motif_memory_candidate_state
return_start_time_derives_return_gap_and_return_phase_under_fixed_meter
absence_interval_is_not_identical_to_sounding_intervening_material
melodic_material_silence_is_not_total_acoustic_silence_when_meter_reference_continues
intervening_material_identity_can_change_while_return_start_gap_and_phase_are_held
motif_memory_fixture_extends_local_timing_relations_to_mid_range_absence_retention_return
```

これらは、人間聴取の確定ではなく、Music側の生成・構造fixtureとして返せる。

## 3. 閉じる関係

```text
same motif material
  + same motif duration
  + same motif contour
  ≠ same motif-memory candidate state

return start time
  -> return gap / absence interval
  -> return phase under fixed meter

absence interval
  ≠ sounding intervening material
  ≠ total acoustic silence
```

特に `delayed_return_after_filler` と `delayed_return_after_silence` は、return start、gap、phaseを揃えたまま、sounding fillerの有無だけを変える比較である。

## 4. 実聴取まで保留する命題

```text
whether direct repetition is heard as confirmation or simple echo
whether delayed return is heard as refrain answer or recollection
whether silent gap or sounding filler better supports motif retention
whether offphase return is heard as interruption compression or syncopated return
whether contrast before return increases perceived return strength
which discrepancies are absorbed by current M_B or remain as H
which unrecovered relation due to the chosen finite B is described as xi in this observation
```

これらは、actual listening observationなしにCore命題へ昇格しない。ξの存在そのものはT0側で既定とし、ここで保留するのは、このBと観測でどの未回収関係をξとして記述するかである。

## 5. Coreへ返さないもの

```text
device_candidate_classification_as_actual_listener_memory_state
melodic_material_silence_as_total_acoustic_silence
return_phase_as_independent_intervention_under_fixed_meter
motif_return_candidate_as_confirmed_refrain_perception
```

`candidate_classification` は、実聴取上のmemory stateではなく、現在B内のdevice-side候補分類である。

## 6. 生成artifact

```text
artifacts/json/music_v02_melody_meter_motif_memory_pre_listening_closure.json
```

このmanifestは、motif memory題材を実聴取前に一区切りするための索引である。

## 7. 次のMusic本線

motif memoryは、実聴取slotを開いたまま一旦閉じる。

次に進む対象候補は、音色 / attackである。

```text
same pitch
+ same onset
+ changed attack envelope / spectrum
-> timbre-articulation candidate
```

旋律×拍節で得た時間関係をさらに刻むのではなく、別の音楽関係へ移す。