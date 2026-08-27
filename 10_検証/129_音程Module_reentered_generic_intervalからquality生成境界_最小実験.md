# 検証記録：reentered generic intervalからquality生成境界

*対象：128で再入生成したgeneric interval candidateを、既存72のquality生成境界へ接続する条件*
*状態：DRAFT v0.1*
*実装：`10_検証/interval_module_generic_to_quality_reentry.py`*

## ■ 0. 検証目的

128では、122〜127の入力契約経路を通って得たprocessing frame candidateが、既存71のgeneric interval生成境界へ再入できることを確認した。

129では、そのreentered generic interval candidateとchromatic distanceを、既存72のquality生成境界へ接続できるかを確認する。

```text
activation input bundle
+ Γ_existing_70_activation_bridge
↓
existing 70 activation pipeline
↓
processing frame candidate
+ Γ_processing_frame_to_generic_reentry
+ Γ_generic_fixture
↓
generic interval candidate
+ Γ_reentered_generic_to_quality
+ Γ_quality_fixture
↓
quality candidate
↓
interval label は未生成
```

ここで確認するのは、128の再入結果がquality生成へ接続可能であることと、quality生成がinterval labelを自動生成しないことである。

## ■ 1. 固定する入力

128で観測したgeneric interval candidateを固定する。

```text
generic interval candidate:
  generic_number = 5

chromatic distance:
  semitones = 7
```

これらはquality判定の入力候補であり、まだqualityそのものでもinterval labelでもない。

```text
generic interval candidate
≠ quality candidate
≠ interval label candidate
```

## ■ 2. Quality再入Gamma

二つの経路を比較する。

```text
Γ_reentered_generic_to_quality = None
  → quality candidate = None
```

```text
Γ_reentered_generic_to_quality_fixture
  + Γ_quality_fixture
  → generic_number = 5 と semitones = 7 を読み、
     quality_code = P を候補として作る
```

再入Gammaは、generic interval再入が自動生成するものではない。

ここでのreentry / contract系の名称はMusic側検証列の局所境界であり、RDL Core Primitiveではない。

## ■ 3. 観測結果

```text
without quality reentry gamma:
  reentered_generic_not_connected_to_quality_without_reentry_gamma

with quality reentry gamma:
  reentered_generic_connected_to_quality_not_interval_label
```

確認できたこと。

```text
same generic interval candidate
same chromatic distance
different quality reentry gamma
↓
quality candidate appears / does not appear
```

さらに、

```text
quality candidate
≠ interval label generation
≠ contextual role annotation
```

である。

## ■ 4. 非同一性

```text
activation input bundle
≠ existing70 activation execution
≠ processing frame
≠ generic interval
≠ quality reentry gamma
≠ quality
≠ interval label
```

## ■ 5. 暫定結論

129では、122〜128の入力契約・既存処理再入経路を通って得たgeneric interval candidateが、既存72のquality生成境界へ接続可能であることを確認した。

ただし、ここで停止する。

```text
quality candidate
  ≠ interval label
  ≠ contextual role annotation
  ≠ target generation
```

次に進むなら、再入後のgeneric interval candidateとquality candidateを`Gamma_interval_label`へ接続できるかを見る。
