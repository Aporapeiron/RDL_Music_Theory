# Music v0.2 C6 / Am7 実聴取前小括 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/C6_Am7/Music_v0.2_C6_Am7_実聴取前小括_最小ループ.md
10_Music_Validation/C6_Am7/music_v02_c6_am7_pre_listening_closure.py
artifacts/json/music_v02_c6_am7_pre_listening_closure.json
```

## 1. 抽出主題

C6 / Am7題材は、実聴取前に次の境界まで到達した。

```text
same material
↓
changed relation configuration
↓
different candidate state
↓
device-side fixtures prepared
↓
actual listening still pending
```

この状態を、Music Coreへ返す命題と、実聴取まで保留する命題に分ける。

## 2. Music Core v0.2へ返せるもの

```text
同一音集合の保存
  ≠ 和声状態の保存

同一target音響の保存
  ≠ 時間文脈状態の保存

C6 / Am7候補差は、少なくとも
  bass_relation
  register_gravity
  temporal_context
  history / presentation memory
に依存する。
```

これらは、人間聴取の断定ではなく、Music構造として返せる。

## 3. まだ返さないもの

```text
この音源が人間にC6として聞こえた
この音源が人間にAm7として聞こえた
pivot再解釈がtarget時点で起きた
順序variantが知覚強度を変えた
```

これらは `actual_listening_observation` の記録後に、E / H / θ / Updateの経路へ送る。

## 4. C6 / Am7から得た停止線

```text
候補分類
  ≠ 和音名の確定

構造予測
  ≠ 実聴取

重み数値
  ≠ 普遍定数

音声生成
  ≠ 人間知覚の確認
```

この停止線により、C6 / Am7題材を閉じても、未確認の聴取命題をMusic Coreへ混ぜない。

## 5. 次対象への橋

C6 / Am7で扱った保存と変化の型は、次のように移せる。

```text
harmony:
  pitch material preserved
  relation configuration changed

melody / meter:
  melodic contour preserved
  accent / metric placement changed
```

次のMusic本線では、旋律輪郭を保存したまま拍節配置を変え、同一旋律候補が保持されるか、別状態へ再解釈されるかを観測する。

## 6. 小括

C6 / Am7は未解決のまま残すのではなく、実聴取前の構造命題として一度閉じる。

```text
closed for structural return
open for actual listening observation
```

この二重状態を保つことで、Music Coreは前へ進みつつ、後から実聴取に戻れる。