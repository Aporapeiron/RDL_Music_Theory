# 検証記録：音程Module・qualityとinterval label生成境界

*対象：generic interval candidateとquality candidateからinterval label candidateが生じる条件*  
*状態：DRAFT v0.1 / 72 quality生成境界後のinterval label生成最小検証*  
*実装：`10_検証/interval_module_label_boundary.py`*

---

## ■ 0. 検証目的

72では、generic interval candidateとchromatic distanceに`Gamma_quality`を与えた場合だけquality candidateが生じることを確認した。

73では、generic interval candidateとquality candidateを固定し、`Gamma_interval_label`を外部に与えた場合だけinterval label candidateが生じることを確認する。

```text
generic interval candidate
  + quality candidate
  + Gamma_interval_label_fixture
  ↓
interval label candidate
  ↓
contextual role / target は未生成
```

ここで確認するのは、qualityがあることと、音程ラベルが生成されたことを分けることである。

---

## ■ 1. 固定する入力

72で得たfixture用のquality candidateと、71のgeneric interval candidateを使う。

```text
generic interval candidate:
  generic_number = 5

quality candidate:
  quality_code = P
```

これらはinterval label生成の入力候補であり、まだ文脈的役割やtarget候補ではない。

```text
quality candidate
  ≠ interval label candidate
  ≠ contextual role annotation
```

---

## ■ 2. Interval label生成Gamma

二つの経路を比較する。

```text
Gamma_interval_label = None
  → interval label candidate = None
```

```text
Gamma_interval_label_fixture
  → generic_number = 5 と quality_code = P を読み、
     label = 完全五度 を候補として作る
```

このGammaはfixture用であり、contextual role annotationやtarget候補生成規則ではない。

---

## ■ 3. 観測結果

| generic interval | quality | Gamma_interval_label | interval label | contextual role | target |
|---:|---|---|---|---|---|
| 5 | P | None | `None` | `None` | `None` |
| 5 | P | fixture | `完全五度` | `None` | `None` |

確認できたこと。

```text
same generic interval candidate
same quality candidate
different Gamma_interval_label
↓
interval label candidate appears / does not appear
```

さらに、

```text
interval label candidate
  ≠ contextual role annotation
  ≠ target candidate generation
  ≠ harmonic function
```

である。

---

## ■ 4. まだ言えないこと

今回の検証から、次は言えない。

```text
完全五度が文脈上どの役割を持つこと
interval labelからtarget候補が生成されたこと
和声機能Moduleや声部進行Moduleへ接続できること
人間が同じラベルとして聴取すること
RDL Coreへ昇格できること
```

---

## ■ 5. 暫定結論

73では、generic interval candidateとquality candidateだけではinterval label candidateは生じず、`Gamma_interval_label`を与えた場合だけinterval label candidateが生じることを確認した。

```text
generic interval candidate
  + quality candidate
  + Gamma_interval_label_fixture
  ↓
interval label candidate
```

ただし、ここで停止する。

```text
interval label candidate
  ≠ contextual role annotation
  ≠ target candidate generation
  ≠ harmonic function
  ≠ Core昇格
```

次に進むなら、69〜73を構造抽出し、base/learned/core入力から音程ラベル候補までの境界列を圧縮する。
