# C6 / Am7 actual listening observation template

*対象：`artifacts/audio/music_v02_c6_am7_rehearing_loop.wav`*  
*状態：未実施の人間聴取slot / structural predictionとは分離*

---

## 0. 停止線

この記録は、人間聴取の観測を後から入れるためのslotである。

```text
structural prediction
  ≠ perceptual hypothesis
  ≠ actual listening observation
```

したがって、構造上 `Am7_candidate becomes available` と予測されていても、それを実聴取済みとは扱わない。

---

## 1. 提示物

```text
audio fixture:
  artifacts/audio/music_v02_c6_am7_rehearing_loop.wav

sequence:
  C3 E3 G3 A3
  ↓
  A2 C3 E3 G3
  ↓
  C3 E3 G3 A3
```

これは `F_device` 側の提示物である。

---

## 2. 構造予測

```text
C6_candidate
  ↓ bass/register/context change
C6/Am7 ambiguity pressure
  ↓
Am7_candidate becomes available
```

---

## 3. 聴取仮説

```text
second chord may be heard as a bass-driven tilt toward Am7,
while C-centered memory remains active.
```

---

## 4. 実聴取観測

未実施の場合:

```text
actual_listening_observation: null
```

実施後は、次を分けて記録する。

```text
heard_center:
  C / A / ambiguous / other

heard_change:
  stable shift / temporary color / ambiguous pressure / no salient change / other

confidence:
  low / medium / high

listener_context:
  headphone / speaker / internal playback / other

notes:
  free description
```

---

## 5. Music Coreへの返却条件

実聴取観測が入っても、それだけでCoreを更新しない。

Coreへ返すのは、次が分離して記録できた場合である。

```text
構造予測
聴取仮説
実聴取観測
それらの一致または不一致
```

不一致が出た場合は、まずdiscrepancyとして記録する。

```text
予測 / 仮説
↓
actual observation
↓
E: discrepancy
↓
現在のM_Bで吸収可能か検査
↓
H: M_Bで未吸収の差
↓
θ: maintain / reorganize / Update判断
↓
有限Bに伴いなお未回収の関係
↓
ξ
```

したがって、次の二つを同時に守る。

```text
不一致
  ≠ 即予測失敗
  ≠ 即ξ

E
  ≠ 吸収可能だった場合だけ出るもの

H
  ≠ ξ
```

この不一致は、Music Coreが人間聴取から修正される可能性を持つ学習信号として保持する。
