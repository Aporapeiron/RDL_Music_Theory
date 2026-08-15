# 検証記録：音程Module・generic intervalとquality生成境界

*対象：generic interval candidateとchromatic distanceからquality candidateが生じる条件*  
*状態：DRAFT v0.1 / 71 generic interval生成境界後のquality生成最小検証*  
*実装：`10_検証/interval_module_quality_boundary.py`*

---

## ■ 0. 検証目的

71では、processing frame candidateに`Gamma_generic`を与えた場合だけgeneric interval candidateが生じることを確認した。

72では、そのgeneric interval candidateとchromatic distanceを固定し、`Gamma_quality`を外部に与えた場合だけquality candidateが生じることを確認する。

```text
generic interval candidate
  + chromatic distance
  + Gamma_quality_fixture
  ↓
quality candidate
  ↓
interval label は未生成
```

ここで確認するのは、generic intervalがあることと、qualityが生成されたことを分けることである。

---

## ■ 1. 固定する入力

71で得たfixture用のgeneric interval candidateを使う。

```text
generic interval candidate:
  generic_number = 5
```

また、70のpayloadから読めるchromatic distanceを使う。

```text
chromatic distance:
  semitones = 7
```

これらはquality判定の入力候補であり、まだinterval labelではない。

```text
generic interval candidate
  ≠ quality candidate
  ≠ interval label candidate
```

---

## ■ 2. Quality生成Gamma

二つの経路を比較する。

```text
Gamma_quality = None
  → quality candidate = None
```

```text
Gamma_quality_fixture
  → generic_number = 5 と semitones = 7 を読み、
     quality_code = P を候補として作る
```

このGammaはfixture用であり、interval label生成規則ではない。

---

## ■ 3. 観測結果

| generic interval | chromatic distance | Gamma_quality | quality | interval label |
|---:|---:|---|---|---|
| 5 | 7 | None | `None` | `None` |
| 5 | 7 | fixture | `P` | `None` |

確認できたこと。

```text
same generic interval candidate
same chromatic distance
different Gamma_quality
↓
quality candidate appears / does not appear
```

さらに、

```text
quality candidate
  ≠ interval label generation
```

である。

---

## ■ 4. まだ言えないこと

今回の検証から、次は言えない。

```text
完全五度というinterval labelが生成されたこと
qualityだけで音程名が決まること
contextual role annotationが生成されたこと
target候補が生成されたこと
和声機能Moduleや声部進行Moduleへ接続できること
```

---

## ■ 5. 暫定結論

72では、generic interval candidateとchromatic distanceだけではquality candidateは生じず、`Gamma_quality`を与えた場合だけquality candidateが生じることを確認した。

```text
generic interval candidate
  + chromatic distance
  + Gamma_quality_fixture
  ↓
quality candidate
```

ただし、ここで停止する。

```text
quality candidate
  ≠ interval label candidate
  ≠ contextual role annotation
  ≠ target generation
```

次に進むなら、generic interval candidateとquality candidateを`Gamma_interval_label`へ接続する境界を見る。
