# 検証記録：reentered contextual roleからtarget候補集合境界

*対象：再入生成されたcontextual role annotation candidateが、外部target inventoryとGammaによってtarget candidate setへ接続される条件*  
*状態：DRAFT v0.1 / 131 reentered contextual role後の既存75再接続境界*  
*実装：`10_検証/interval_module_contextual_role_to_target_reentry.py`*

---

## ■ 0. 検証目的

131では、reentered interval label candidateからcontextual role annotation candidateを生成できることを確認した。

132では、そのreentered contextual role annotation candidateを固定し、外部target candidate inventoryと`Gamma_interval_target_candidate_filter`を与えた場合だけtarget candidate set observedが生じることを確認する。

```text
reentered contextual role annotation candidate
  + external target candidate inventory
  + Gamma_reentered_contextual_role_to_target_candidates
  + Gamma_interval_target_candidate_filter_fixture
  ↓
target candidate set observed
  ↓
selected target は未生成
```

ここで重要なのは、contextual role annotationからtarget候補そのものを自動生成しないことである。候補inventoryは外部入力として与える。

---

## ■ 1. 入力として固定するreentered contextual role

131で得た再入contextual role annotation candidateを使う。

```text
reentered contextual role:
  role_label = tonic_to_fifth_span_role_candidate
  key_context = C major
  lower_degree = 1
  upper_degree = 5
```

これは文脈役割注釈であり、まだtarget候補集合ではない。

```text
reentered contextual role annotation candidate
  ≠ target candidate set
```

---

## ■ 2. 外部target inventory

75と同じfixture inventoryを外部から与える。

```text
external target candidate inventory:
  maintain_C_G_span
  collapse_to_C_unison
  move_to_E_C_contextual_resolution
```

このinventoryはreentered contextual role annotationから自動生成されたものではない。

---

## ■ 3. 観測結果

| reentered contextual role | external inventory | reentry Gamma | target candidate set | selected target |
|---|---|---|---|---|
| same | same | None | `None` | `None` |
| same | same | fixture | `{maintain_C_G_span, collapse_to_C_unison}` | `None` |

実行結果。

```text
reentered_contextual_role_connected_to_target_candidates_unselected
```

確認できたこと。

```text
same reentered contextual role annotation
same external target inventory
different Gamma_reentered_contextual_role_to_target_candidates
↓
target candidate set appears / does not appear
```

さらに、

```text
target candidate set observed
  ≠ selected target
  ≠ voice leading plan
  ≠ harmonic function
```

である。

---

## ■ 4. 暫定結論

132では、reentered contextual role annotation candidateだけではtarget candidate setは生じず、外部target inventoryと再入Gammaを与えた場合だけtarget candidate set observedが生じることを確認した。

これにより、125〜127で既存70へ着地したprocessing request系列は、128〜132を通じて既存71〜75のtarget候補集合境界まで再接続された。

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
  ↓
target candidate set
```

ただし、まだselected target、selection controller、voice leading計画、harmonic annotationは生成しない。

次に進むなら、reentered target candidate setとselection controllerを接続する境界を見る。
