# 検証記録：音程Module・interval labelとcontextual role注釈境界

*対象：interval label candidateが、外部contextとGammaによってcontextual role annotation candidateへ接続される条件*  
*状態：DRAFT v0.1 / 73 interval label生成境界後のcontextual role最小検証*  
*実装：`10_検証/interval_module_contextual_role_boundary.py`*

---

## ■ 0. 検証目的

73では、generic interval candidateとquality candidateに`Gamma_interval_label`を与えた場合だけ、interval label candidateが生じることを確認した。

74では、そのinterval label candidateを固定し、外部contextと`Gamma_contextual_role`を与えた場合だけcontextual role annotation candidateが生じることを確認する。

```text
interval label candidate
  + external interval context
  + Gamma_contextual_role_fixture
  ↓
contextual role annotation candidate
  ↓
target候補 / harmonic function は未生成
```

ここで確認するのは、音程ラベルがあることと、文脈役割注釈があることを分けることである。

---

## ■ 1. 固定するinterval label

73で得たfixture用のinterval label candidateを使う。

```text
interval label candidate:
  label = 完全五度
  generic_number = 5
  quality_code = P
```

これは音程ラベル候補であり、まだ文脈役割ではない。

```text
interval label candidate
  ≠ contextual role annotation candidate
```

---

## ■ 2. 外部context

今回は文脈を外部fixtureとして与える。

```text
external interval context:
  key_context = C major
  lower_degree = 1
  upper_degree = 5
  role_scope = local_pitch_relation_role
```

このcontextはinterval labelから自動生成されたものではない。

---

## ■ 3. 観測結果

| interval label | context | Gamma_contextual_role | role annotation | target | harmonic function |
|---|---|---|---|---|---|
| 完全五度 | same | None | `None` | `None` | `None` |
| 完全五度 | same | fixture | `tonic_to_fifth_span_role_candidate` | `None` | `None` |

確認できたこと。

```text
same interval label candidate
same external context
different Gamma_contextual_role
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

74では、interval label candidateだけではcontextual role annotation candidateは生じず、外部contextと`Gamma_contextual_role`を与えた場合だけcontextual role annotation candidateが生じることを確認した。

次に進むなら、contextual role annotation candidateと外部target candidate inventoryを接続する境界を見る。
