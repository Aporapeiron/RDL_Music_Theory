# Music v0.2 検証記録：C6 / Am7 時間文脈提示順序分離 最小ループ

*状態：DRAFT v0.1 / 時間文脈実音化後の提示順序依存分離*  
*実装：`10_Music_Validation/C6_Am7/music_v02_c6_am7_temporal_context_order_split.py`*

## 0. 目的

前回の時間文脈実音化では、4つのphraseを1つのWAV内に順番に並べた。

```text
c_centered_frame
↓
a_centered_frame
↓
c_to_a_pivot_frame
↓
a_to_c_resistance_frame
```

この形式は実聴取しやすい一方で、phrase間の記憶が次のphraseへ影響する可能性がある。

今回は、phrase内contextと提示順序memoryを分けるため、次の二種類のfixtureを追加する。

```text
1. each phrase as a separate WAV
2. reordered multi-phrase WAV variants
```

## 1. 停止線

```text
single phrase WAV
  ≠ 記憶影響の完全除去

order variant
  ≠ 和音名の正解判定

提示順序差
  ≠ ただちにMusic Core更新
```

提示順序差が聴取上出た場合、まず `actual_listening_observation` へ記録し、構造予測との差をEとして扱う。

## 2. 単独phrase file

各phraseを単独WAVとして出力する。

```text
artifacts/audio/c6_am7_temporal_context_order_split/c_centered_frame.wav
artifacts/audio/c6_am7_temporal_context_order_split/a_centered_frame.wav
artifacts/audio/c6_am7_temporal_context_order_split/c_to_a_pivot_frame.wav
artifacts/audio/c6_am7_temporal_context_order_split/a_to_c_resistance_frame.wav
```

これにより、各phrase内の

```text
preceding chord
↓
identical target C3 E3 G3 A3
↓
following chord
```

だけを聴取対象として切り出せる。

## 3. 順序variant

### 3.1 canonical_order

```text
c_centered_frame
↓
a_centered_frame
↓
c_to_a_pivot_frame
↓
a_to_c_resistance_frame
```

前回の提示順序を保持する。

### 3.2 reversed_context_order

```text
a_centered_frame
↓
c_centered_frame
↓
a_to_c_resistance_frame
↓
c_to_a_pivot_frame
```

C中心からA中心へ進む印象だけでなく、A中心からC中心へ戻る提示でも候補状態が保たれるかを見る。

## 4. 生成artifact

```text
artifacts/audio/c6_am7_temporal_context_order_split/
artifacts/json/music_v02_c6_am7_temporal_context_order_split.json
```

manifestには、単独phrase file、順序variant、実聴取slotを分けて記録する。

## 5. Music上の意味

この検証で分けるのは次である。

```text
phrase-internal context:
  前和音 -> target -> 後和音

presentation-order memory:
  あるphraseを聞いた後に、次のphraseをどう聞くか
```

前者は対象phrase内部の時間的関係であり、後者は検証提示によって生じる聴取条件である。

## 6. 次の接続

実聴取を入れる場合は、まず単独phrase fileでphrase内contextを記録し、その後に順序variantで提示順序memoryを記録する。

```text
single phrase listening
↓
order variant listening
↓
E: prediction / actual discrepancy
↓
H / θ / Update候補
```

今回も実聴取はまだ行わず、`actual_listening_observation = null` を維持する。