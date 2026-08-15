# 検証記録：音程Module・contextual roleとtarget候補集合境界

*対象：contextual role annotation candidateが、外部target inventoryとGammaによってtarget candidate setへ接続される条件*  
*状態：DRAFT v0.1 / 74 contextual role注釈境界後のtarget候補集合最小検証*  
*実装：`10_検証/interval_module_target_candidate_boundary.py`*

---

## ■ 0. 検証目的

74では、interval label candidateに外部contextと`Gamma_contextual_role`を与えた場合だけcontextual role annotation candidateが生じることを確認した。

75では、そのcontextual role annotation candidateを固定し、外部target candidate inventoryと`Gamma_interval_target_candidate_filter`を与えた場合だけtarget candidate set observedが生じることを確認する。

```text
contextual role annotation candidate
  + external target candidate inventory
  + Gamma_interval_target_candidate_filter_fixture
  ↓
target candidate set observed
  ↓
selected target は未生成
```

ここで重要なのは、contextual roleからtarget候補集合を自動生成しないことである。候補inventoryは外部入力として与える。

---

## ■ 1. 固定するcontextual role

74で得たfixture用のcontextual role annotation candidateを使う。

```text
contextual role:
  role_label = tonic_to_fifth_span_role_candidate
  key_context = C major
  lower_degree = 1
  upper_degree = 5
```

これは文脈役割注釈であり、まだtarget候補集合ではない。

---

## ■ 2. 外部target inventory

今回はtarget候補を外部inventoryとして与える。

```text
external target candidate inventory:
  maintain_C_G_span
  collapse_to_C_unison
  move_to_E_C_contextual_resolution
```

このinventoryはcontextual role annotationから自動生成されたものではない。

---

## ■ 3. 観測結果

| contextual role | external inventory | Gamma_filter | target candidate set | selected target |
|---|---|---|---|---|
| same | same | None | `None` | `None` |
| same | same | fixture | `{maintain_C_G_span, collapse_to_C_unison}` | `None` |

確認できたこと。

```text
same contextual role annotation
same external target inventory
different Gamma_interval_target_candidate_filter
↓
target candidate set appears / does not appear
```

さらに、

```text
target candidate set observed
  ≠ selected target
```

である。

---

## ■ 4. 暫定結論

75では、contextual role annotation candidateだけではtarget candidate setは生じず、外部target inventoryと`Gamma_interval_target_candidate_filter`を与えた場合だけtarget candidate set observedが生じることを確認した。

次に進むなら、target candidate setとselection controllerを接続する境界を見る。
