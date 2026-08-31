# Music v0.2 検証記録：C6 / Am7 介入分離 最小ループ

*対象：同一音集合 `{C,E,G,A}` を保存したまま、bass / register / contextの介入軸を分離して比較する*  
*状態：DRAFT v0.1 / Music Core v0.2 C6-Am7小ループ後の介入分離*  
*実装：`10_Music_Validation/C6_Am7/music_v02_c6_am7_intervention_separation.py`*

---

## ■ 0. 検証目的

前回のC6 / Am7小ループでは、同一音集合を保存し、低音・配置・文脈をまとめて変えることで、C6候補からAm7候補への傾きを生成した。

今回は、その束を一度分ける。

```text
保存:
  pitch_class_set = {C,E,G,A}

介入:
  context only
  register only
  bass primary
  full tilt
```

ここで目的は、C6 / Am7の正解判定ではない。

```text
同じ材料を保存したまま、
どの関係を変えると、
どの音楽状態候補が前景化するか
```

を見ることである。

---

## ■ 1. 停止線

音響実現では、介入軸が完全に純粋になるとは限らない。

例えば、低音をCからAへ変えると、実際にはregister gravityも変わりうる。

```text
bass intervention
  ≠ always pure bass-only change
```

したがって、今回は `primary_intervention` と `residual_changes` を分けて記録する。

```text
primary_intervention:
  何を主に変えたか

residual_changes:
  実現上どうしても伴う副作用
```

---

## ■ 2. source

```text
source_C6_stable:
  notes = C3 E3 G3 A3
  bass = C
  preceding_context = C-centered arrival
  following_context = C-centered continuation expected
  classification = C6_candidate
```

---

## ■ 3. intervention cases

### 3.1 context_only

```text
notes = C3 E3 G3 A3
bass = C
following_context = A-centered continuation becomes available

primary_intervention = following_context
residual_changes = none
```

構造予測:

```text
C6 remains foregrounded, with Am7 context pressure added
```

これは音声だけでは差が出にくい。contextはdevice audio単独の差ではなく、聴取・記述のBに入る関係である。

### 3.2 register_only

```text
notes = C2 E3 G3 A3
bass = C
context = C-centered

primary_intervention = register_gravity
residual_changes = none
```

構造予測:

```text
C6 is reinforced by lower C register gravity
```

同じ音集合でも、Cが低くなることでC側の重心が強まる。

### 3.3 bass_primary

```text
notes = A2 C3 E3 G3
bass = A
following_context = C-centered continuation expected

primary_intervention = bass_relation
residual_changes = register gravity changes because bass A is lower than source C
```

構造予測:

```text
Am7 candidate appears by bass relation, but C-context resists full rebasing
```

ここではA低音によりAm7候補が前景化するが、C中心の後続予測はまだ残る。

### 3.4 full_tilt

```text
notes = A2 C3 E3 G3
bass = A
preceding_context = C-centered memory retained
following_context = A-centered continuation becomes available

primary_intervention = bass_register_context_bundle
residual_changes = none
```

構造予測:

```text
Am7 candidate becomes available with bass, register, and context support
```

前回の小ループに近い、もっともAm7方向が強いケースである。

---

## ■ 4. 再聴取slot

全caseで、実聴取はまだ行わない。

```text
actual_listening_observation = null
```

ここでも、次を同一視しない。

```text
structural prediction
  ≠ perceptual hypothesis
  ≠ actual listening observation
```

---

## ■ 5. 出力

```text
artifacts/audio/music_v02_c6_am7_intervention_separation.wav
artifacts/json/music_v02_c6_am7_intervention_separation.json
```

音声fixtureは、sourceと4つの介入caseを順に提示する。

```text
source_C6_stable
↓
context_only
↓
register_only
↓
bass_primary
↓
full_tilt
```

これは `F_device` 側の提示物であり、人間聴取の確定記録ではない。

---

## ■ 6. 暫定結論

この検証では、C6 / Am7の傾きが単一要因ではないことを保持する。

```text
context only:
  C6候補は残り、Am7方向の文脈圧だけが加わる。

register only:
  C6側の重心がむしろ強まる。

bass primary:
  Am7候補が現れるが、C文脈は抵抗として残る。

full tilt:
  bass / register / contextが揃い、Am7候補がもっとも強くなる。
```

したがって、RDL Music v0.2では、同一音集合の状態遷移を次のように扱う。

```text
preserved material
  + separated relation intervention
  + residual change record
  -> graded musical state candidates
```

これはT2 Mechanismの追加ではなく、Music側で「何を保存し、何を変えたか」を細かく聴けるようにする検証である。