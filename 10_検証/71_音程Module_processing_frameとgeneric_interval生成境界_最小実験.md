# 検証記録：音程Module・processing frameとgeneric interval生成境界

*対象：interval module processing frame candidateからgeneric interval candidateが生じる条件*  
*状態：DRAFT v0.1 / 70 内部B/Gamma接続境界後のgeneric生成最小検証*  
*実装：`10_検証/interval_module_generic_interval_boundary.py`*

---

## ■ 0. 検証目的

70では、interval module boundary input candidate、外部payload、`B_chromatic`、`B_spelling`、`Gamma_interval_processing_frame`を与えた場合だけ、interval module processing frame candidateが生じることを確認した。

71では、そのprocessing frame candidateを固定し、`Gamma_generic`を外部に与えた場合だけgeneric interval candidateが生じることを確認する。

```text
interval module processing frame candidate
  + spelling pair from payload
  + Gamma_generic_fixture
  ↓
generic interval candidate
  ↓
quality / interval label は未生成
```

ここで確認するのは、processing frameが立ったことと、generic intervalが生成されたことを分けることである。

---

## ■ 1. 固定するprocessing frame

70で得たfixture用のprocessing frameを使う。

```text
processing frame:
  label = interval_processing_frame_C4_G4_candidate
  payload = pitch_relation_payload_C4_G4_fixture
  spelling pair = C-G
```

これは内部処理の準備候補であり、まだgeneric intervalではない。

```text
processing frame candidate
  ≠ generic interval candidate
```

---

## ■ 2. Generic生成Gamma

二つの経路を比較する。

```text
Gamma_generic = None
  → generic interval candidate = None
```

```text
Gamma_generic_fixture
  → spelling pair C-G を読み、
     generic_number = 5 を候補として作る
```

このGammaはfixture用であり、quality判定やinterval label生成規則ではない。

---

## ■ 3. 観測結果

| processing frame | spelling pair | Gamma_generic | generic interval | quality | interval label |
|---|---|---|---:|---|---|
| same | C-G | None | `None` | `None` | `None` |
| same | C-G | fixture | `5` | `None` | `None` |

確認できたこと。

```text
same processing frame
same spelling pair
different Gamma_generic
↓
generic interval candidate appears / does not appear
```

さらに、

```text
generic interval candidate
  ≠ quality generation
  ≠ interval label generation
```

である。

---

## ■ 4. まだ言えないこと

今回の検証から、次は言えない。

```text
qualityが生成されたこと
P5などのinterval labelが生成されたこと
generic intervalだけで音程名が決まること
contextual role annotationが生成されたこと
和声機能Moduleや声部進行Moduleへ接続できること
```

---

## ■ 5. 暫定結論

71では、processing frame candidateだけではgeneric interval candidateは生じず、`Gamma_generic`を与えた場合だけgeneric interval candidateが生じることを確認した。

```text
processing frame candidate
  + Gamma_generic_fixture
  ↓
generic interval candidate
```

ただし、ここで停止する。

```text
generic interval candidate
  ≠ quality
  ≠ interval label
  ≠ contextual role annotation
```

次に進むなら、generic interval candidateとchromatic distanceを`Gamma_quality`へ接続する境界を見る。
