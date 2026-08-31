# Music v0.2 検証記録：C6 / Am7 保存・変化・生成・再聴取 最小ループ

*対象：同一音集合 `{C,E,G,A}` を保存したまま、低音・配置・後続文脈だけを変える小さい実音楽ループ*  
*状態：DRAFT v0.1 / Music Core v0.2再構成入口後の最小検証*  
*実装：`10_Music_Validation/C6_Am7/music_v02_c6_am7_rehearing_loop.py`*

---

## ■ 0. 検証目的

この検証では、3398工程型の汎用状態遷移を延長しない。

C6 / Am7の既存題材を使い、Music v0.2本線の小さいループを一周させる。

```text
Bを置く
↓
関係を抽出
↓
保存関係を指定
↓
一つだけ変える
↓
生成
↓
聴取上どう変わったか確認
↓
Music Coreを修正する必要があるかを見る
```

ここで特に確認するのは、次である。

```text
同じ音集合を保存しても、
低音・配置・後続文脈を変えると、
C6としての安定からAm7方向の候補へ傾けられるか。
```

---

## ■ 1. Bの設定

今回のBは、音楽対象を次の関係として切る。

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

`pitch class set`だけではC6 / Am7を分けない。

```text
{C,E,G,A}
  ≠ C6確定
  ≠ Am7確定
```

`bass relation`、`register gravity`、`context`を加えたときだけ、C6方向またはAm7方向の候補が前景化する。

---

## ■ 2. 初期状態

初期状態はC6として安定している候補である。

```text
source:
  notes = C3 E3 G3 A3
  bass  = C
  preceding_context = C-centered arrival
  following_context = C-centered continuation expected
```

抽出される関係は次である。

```text
preserved:
  pitch_class_set = {C,E,G,A}

foregrounded:
  W_bass = C -> {E,G,A}
  W_register = C3が低い重心
  W_context = C中心の継続予測
```

---

## ■ 3. 保存条件

今回保存するのは音集合であり、ラベルではない。

```text
preserve:
  pitch_class_set:{C,E,G,A}
  upper_common_relation:C-E-G retained across the tilt
```

したがって、保存条件は次を意味しない。

```text
C6ラベルを保存すること
Cを常に低音に保つこと
聴取上の中心が必ずCに残ること
```

---

## ■ 4. 変更条件

今回変更するのは低音関係を中心とした一群である。

```text
change:
  bass_relation:C -> A
  register_gravity:C3 -> A2
  following_context:C-centered expectation -> A-centered availability
```

この変更は、音集合の変更ではない。

```text
pitch_class_set unchanged
bass/register/context changed
```

---

## ■ 5. 生成

生成後の状態は次である。

```text
generated:
  notes = A2 C3 E3 G3
  bass  = A
  preceding_context = C-centered memory retained
  following_context = A-centered continuation becomes available
```

このとき、構造上は次の候補が観測される。

```text
C6_candidate
  ↓ bass/register/context change
C6/Am7 ambiguity pressure
  ↓
Am7_candidate becomes available
```

ここで `Am7_candidate` は、人間が必ずAm7として聞いたという記録ではない。

---

## ■ 6. 再聴取の三分割

Music v0.2では、再聴取を次の三つに分ける。

```text
structural prediction
  RDL MusicのB/W/M_Bから、構造上どう変わったと予測するか。

perceptual hypothesis
  人間聴取ではどう聞こえる可能性があるかという仮説。

actual listening observation
  実際に聞いた観測記録。未実施ならNoneとして残す。
```

したがって、次を同一視しない。

```text
構造上の変化
  ≠ 人間がそう聴くこと

F_device
  ≠ F_human
```

今回の記録では、`actual listening observation` は未実施として保持する。実聴取を行う場合は、`10_Music_Validation/C6_Am7/actual_listening_observation_template.md` のslotへ、構造予測とは分けて記録する。不一致は、即予測失敗でも即ξでもない。まず `E: discrepancy` として記録し、現在のM_Bで吸収可能かを検査する。M_Bで未吸収の差はHとして保持し、θがmaintain / reorganize / Updateを判断する。有限Bに伴いなお未回収の関係が残る場合だけξとして保持する。

---

## ■ 7. 実行観測

実装は、C6候補、Am7方向候補、C6候補を順に鳴らすdevice-side audio fixtureを生成する。

```text
C3 E3 G3 A3
↓
A2 C3 E3 G3
↓
C3 E3 G3 A3
```

これは人間聴取の証明ではなく、聴取確認へ渡すための `F_device` 側提示物である。

出力予定:

```text
artifacts/audio/music_v02_c6_am7_rehearing_loop.wav
artifacts/json/music_v02_c6_am7_rehearing_observation.json
```

---

## ■ 8. 暫定結論

この小ループでは、音集合 `{C,E,G,A}` を保存したまま、低音・配置・後続文脈を変えることで、C6として安定していた状態からAm7方向の候補を生成できる。

ただし、これは次を意味しない。

```text
C6からAm7へ必ず知覚転換した
人間聴取でAm7と確認された
C6 / Am7問題が解決した
```

確認できたのは、次である。

```text
同じ材料を保存したまま、
関係配置だけを変え、
別の音楽状態候補を生成できる。
```

Music Core v0.2への返却点は、再聴取を `structural prediction / perceptual hypothesis / actual listening observation` に分けて記録することである。