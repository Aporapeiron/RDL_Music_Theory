# 検証記録：音程Module・boundary inputと内部B/Gamma接続境界

*対象：interval module boundary input candidateを、音程Module内部の処理フレームへ接続する条件*  
*状態：DRAFT v0.1 / 69 音程Module受理境界検証後の内部B/Gamma接続最小検証*  
*実装：`10_検証/interval_module_internal_boundary_activation.py`*

---

## ■ 0. 検証目的

69では、core module input candidateに対して`B_interval_module_reception`と`Gamma_interval_module_reception`を与えた場合だけ、interval module boundary input candidateが生じることを確認した。

70では、そのinterval module boundary input candidateを固定し、音程Module内部で使うfixture用の`B_chromatic`、`B_spelling`、`Gamma_interval_processing_frame`を外部に与えた場合だけ、interval module processing frame candidateが生じることを確認する。

```text
interval module boundary input candidate
  + pitch relation payload fixture
  + B_chromatic_fixture
  + B_spelling_fixture
  + Gamma_interval_processing_frame_fixture
  ↓
interval module processing frame candidate
  ↓
generic interval / quality / interval label は未生成
```

ここで確認するのは、受理境界に入ったことと、音程Module内部の処理フレームが立つことを分けることである。

---

## ■ 1. 固定するinterval module boundary input

69で得たfixture用のinterval module boundary input candidateを使う。

```text
interval module boundary input candidate:
  label = interval_module_received_pitch_relation_candidate
  module_name = 音程_Module
```

これは音程Moduleが受け取った入力候補であり、まだ`B_chromatic`や`B_spelling`へ接続されていない。

```text
interval module boundary input candidate
  ≠ interval module processing frame candidate
```

---

## ■ 2. 外部payloadと内部B

今回は音程Module内部で読める最小payloadをfixtureとして外部に置く。

```text
pitch relation payload fixture:
  lower_note = C4
  upper_note = G4
  chromatic_distance = 7
  spelling_pair = C-G
```

このpayloadは、69のboundary inputから自動生成されたものではない。

```text
interval module boundary input
  ≠ pitch relation payload generation
```

また、内部境界として次を与える。

```text
B_chromatic_fixture:
  chromatic distanceを読める

B_spelling_fixture:
  spelling pairを読める
```

---

## ■ 3. 内部接続Gamma

二つの経路を比較する。

```text
Gamma_interval_processing_frame = None
  → boundary inputはあるが、内部処理フレームは立たない
```

```text
Gamma_interval_processing_frame_fixture
  → boundary input、payload、B_chromatic、B_spellingを読み、
     interval module processing frame candidateを作る
```

このGammaはfixture用であり、`Gamma_generic`、`Gamma_quality`、`Gamma_interval_label`ではない。

---

## ■ 4. 最小ケースの比較

### 4.1 内部接続Gammaなし

```text
interval module boundary input candidate
+ pitch relation payload
+ B_chromatic
+ B_spelling
+ Gamma_interval_processing_frame = None
↓
status = boundary_input_not_connected_without_processing_gamma
processing frame = None
```

### 4.2 内部接続Gammaあり

```text
interval module boundary input candidate
+ pitch relation payload
+ B_chromatic
+ B_spelling
+ Gamma_interval_processing_frame_fixture
↓
interval module processing frame candidate
  label = interval_processing_frame_C4_G4_candidate
```

ただし、音程ラベルはまだ生成しない。

---

## ■ 5. 観測結果

| boundary input | payload | B_chromatic | B_spelling | Gamma_frame | processing frame | interval label |
|---|---|---|---|---|---|---|
| same | same | same | same | None | `None` | `None` |
| same | same | same | same | fixture | `interval_processing_frame_C4_G4_candidate` | `None` |

確認できたこと。

```text
same interval module boundary input
same pitch relation payload
same B_chromatic
same B_spelling
different Gamma_interval_processing_frame
↓
interval module processing frame appears / does not appear
```

さらに、

```text
interval module processing frame candidate
  ≠ generic interval generation
  ≠ quality generation
  ≠ interval label generation
  ≠ contextual role annotation
```

である。

---

## ■ 6. Module責務の確認

今回の接続は、次のように分かれる。

```text
Gamma_interval_module_reception:
  interval module boundary input candidateを作る

pitch relation payload:
  今回は外部fixtureとして与える

B_chromatic / B_spelling:
  音程Module内部で読む境界を置く

Gamma_interval_processing_frame:
  boundary inputと内部Bを処理フレームへ接続する

Gamma_generic / Gamma_quality / Gamma_interval_label:
  今回は未接続
```

したがって、内部処理フレームの成立は、音程名の生成ではない。

---

## ■ 7. まだ言えないこと

今回の検証から、次は言えない。

```text
generic intervalが生成されたこと
qualityが生成されたこと
P5やd6などのinterval labelが生成されたこと
このpayloadが一般的な音程Module入力形式であること
B_chromatic / B_spellingが一般Module境界として確定したこと
contextual role annotationが生成されたこと
和声機能Moduleや声部進行Moduleへ接続できること
RDL Coreへ昇格できること
```

また、今回の`B_chromatic`、`B_spelling`、`Gamma_interval_processing_frame`はfixture用であり、一般的な音程Module内部処理規則ではない。

---

## ■ 8. 暫定結論

70では、interval module boundary input candidateだけでは音程Module内部の処理フレームは立たず、外部payload、`B_chromatic`、`B_spelling`、`Gamma_interval_processing_frame`を与えた場合だけinterval module processing frame candidateが生じることを確認した。

```text
interval module boundary input candidate
  + pitch relation payload fixture
  + B_chromatic_fixture
  + B_spelling_fixture
  + Gamma_interval_processing_frame_fixture
  ↓
interval module processing frame candidate
```

ただし、ここで停止する。

```text
interval module processing frame candidate
  ≠ generic interval generation
  ≠ quality generation
  ≠ interval label generation
  ≠ contextual role annotation
  ≠ Core昇格
```

次に進むなら、processing frame candidateから`Gamma_generic`を接続し、generic interval candidateが生じる境界を見る。
