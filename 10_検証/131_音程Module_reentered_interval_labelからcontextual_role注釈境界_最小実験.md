# 検証記録：reentered interval labelからcontextual role注釈境界

*対象：再入生成されたinterval label candidateが、外部contextとGammaによってcontextual role annotation candidateへ接続される条件*  
*状態：DRAFT v0.1 / 130 reentered interval label後の既存74再接続境界*  
*実装：`10_検証/interval_module_label_to_contextual_role_reentry.py`*

---

## ■ 0. 検証目的

130では、再入quality candidateからinterval label candidateを生成できることを確認した。

131では、そのreentered interval label candidateを固定し、外部interval contextと`Gamma_contextual_role`を与えた場合だけcontextual role annotation candidateが生じることを確認する。

```text
reentered interval label candidate
  + external interval context
  + Gamma_reentered_interval_label_to_contextual_role
  + Gamma_contextual_role_fixture
  ↓
contextual role annotation candidate
  ↓
target候補 / harmonic function は未生成
```

ここで確認するのは、再入によって得たinterval labelが、旧74の文脈役割注釈境界へ接続可能であることと、interval labelからtargetやharmonic functionを自動生成しないことである。

---

## ■ 1. 入力として固定するreentered interval label

130で得た再入ラベルを使う。

```text
reentered interval label candidate:
  label = 完全五度
  generic_number = 5
  quality_code = P
```

これは音程ラベル候補であり、まだcontextual role annotation candidateではない。

```text
reentered interval label candidate
  ≠ contextual role annotation candidate
```

---

## ■ 2. 外部context

74と同じfixture contextを外部から与える。

```text
external interval context:
  key_context = C major
  lower_degree = 1
  upper_degree = 5
  role_scope = local_pitch_relation_role
```

このcontextはreentered interval labelから自動生成されたものではない。

---

## ■ 3. 観測結果

| reentered interval label | context | reentry Gamma | contextual role | target | harmonic function |
|---|---|---|---|---|---|
| 完全五度 | same | None | `None` | `None` | `None` |
| 完全五度 | same | fixture | `tonic_to_fifth_span_role_candidate` | `None` | `None` |

実行結果。

```text
reentered_interval_label_connected_to_contextual_role_not_target
```

確認できたこと。

```text
same reentered interval label
same external context
different Gamma_reentered_interval_label_to_contextual_role
↓
contextual role annotation appears / does not appear
```

さらに、

```text
contextual role annotation candidate
  ≠ target candidate generation
  ≠ harmonic function
```

である。

---

## ■ 4. 暫定結論

131では、reentered interval label candidateだけではcontextual role annotation candidateは生じず、外部contextと再入Gammaを与えた場合だけcontextual role annotation candidateが生じることを確認した。

これにより、125〜127で既存70へ着地したprocessing request系列は、128〜131を通じて既存71〜74の次の境界まで再接続された。

```text
processing request
  ↓
adoption
  ↓
activation input bundle
  ↓
existing 70 activation
  ↓
processing frame
  ↓
generic interval
  ↓
quality
  ↓
interval label
  ↓
contextual role annotation
```

ただし、まだtarget候補集合、selection controller、voice leading計画、harmonic annotationは生成しない。

次に進むなら、reentered contextual role annotation candidateと外部target candidate inventoryを接続する境界を見る。
