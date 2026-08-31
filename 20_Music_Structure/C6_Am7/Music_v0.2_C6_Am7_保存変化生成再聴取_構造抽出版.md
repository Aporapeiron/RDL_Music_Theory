# Music v0.2 C6 / Am7 保存・変化・生成・再聴取 構造抽出版

## 0. 抽出対象

対象:

```text
10_Music_Validation/C6_Am7/Music_v0.2_C6_Am7_保存変化生成再聴取_最小ループ.md
10_Music_Validation/C6_Am7/music_v02_c6_am7_rehearing_loop.py
10_Music_Validation/C6_Am7/actual_listening_observation_template.md
```

この抽出は、3398工程型のT2候補列を延長しない。

Music v0.2本線として、実音楽対象に対する小さい分析・生成・再聴取ループを抽出する。

---

## 1. B

```text
B_C6_Am7_rehearing:
  pitch class set
  bass relation
  register gravity
  preceding context
  following context
  device rendering
  listening observation slot
```

このBでは、音集合だけを和音ラベルへ直結しない。

```text
{C,E,G,A}
  ≠ C6確定
  ≠ Am7確定
```

---

## 2. 保存関係

```text
preserved_relations:
  pitch_class_set:{C,E,G,A}
  upper_common_relation:C-E-G retained across the tilt
```

保存されるのは音素材と一部上部関係であり、C6という圧縮ラベルではない。

---

## 3. 変更関係

```text
changed_relations:
  bass_relation:C->A
  register_gravity:C3->A2
  following_context:C-centered expectation->A-centered availability
```

変更は音集合ではなく、関係配置に置かれる。

---

## 4. 生成された状態候補

```text
source:
  C3 E3 G3 A3
  bass = C
  classification = C6_candidate

generated:
  A2 C3 E3 G3
  bass = A
  classification = Am7_candidate
```

```text
source.pitch_classes == generated.pitch_classes
source.bass != generated.bass
```

したがって、同一音集合を保存したまま、音楽状態候補だけを変えるfixtureになっている。

---

## 5. 再聴取の分離

今回の重要な抽出点は、再聴取を一つの判定へ潰さないことである。

```text
structural prediction:
  C6_candidate -> C6/Am7 ambiguity pressure -> Am7_candidate becomes available

perceptual hypothesis:
  listener may hear the second chord as a bass-driven tilt toward Am7,
  while C-centered memory remains active

actual listening observation:
  None
```

```text
structural prediction
  ≠ perceptual hypothesis
  ≠ actual listening observation
```

この分離により、`F_device` と `F_human` を同一視しない停止線がMusic v0.2の実験形式に入る。

---

## 6. F_device fixture

実装は、次の音声提示物を生成する。

```text
C6_candidate
↓
Am7_tilt_candidate
↓
C6_candidate
```

出力:

```text
artifacts/audio/music_v02_c6_am7_rehearing_loop.wav
artifacts/json/music_v02_c6_am7_rehearing_observation.json
```

これは人間聴取の証明ではなく、actual listening observationへ渡すためのdevice-side fixtureである。

---

## 7. Music Core v0.2への返却

この検証からMusic Core v0.2へ返す最小更新候補:

```text
re-hearing record must distinguish:
  structural prediction
  perceptual hypothesis
  actual listening observation
```

```text
generated musical state candidate
  ≠ confirmed human hearing
```

```text
preserve material
  + change relation placement
  -> generate different musical state candidate
```

---

## 8. 停止線

この検証では次を行わない。

```text
50工程列へ拡張する
T2 Runtime mechanismを増やす
C6 / Am7を単一正解へ解決する
F_deviceからF_humanを導く
perceptual hypothesisをactual observationとして記録する
```