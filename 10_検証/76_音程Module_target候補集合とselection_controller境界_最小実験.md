# 検証記録：音程Module・target候補集合とselection controller境界

*対象：target candidate set observedからselected interval target candidateが生じる条件*  
*状態：DRAFT v0.1 / 75 target候補集合境界後のselection最小検証*  
*実装：`10_検証/interval_module_target_selection_boundary.py`*

---

## ■ 0. 検証目的

75では、contextual role annotation candidate、外部target inventory、`Gamma_interval_target_candidate_filter`を与えた場合だけtarget candidate set observedが生じることを確認した。

76では、そのtarget candidate set observedを固定し、`Gamma_interval_target_selection`を与えた場合だけselected interval target candidateが生じることを確認する。

```text
target candidate set observed
  + Gamma_interval_target_selection_fixture
  ↓
selected interval target candidate
  ↓
voice leading / harmonic function は未生成
```

ここで確認するのは、候補集合があることと、候補が選ばれていることを分けることである。

---

## ■ 1. 固定するtarget候補集合

75で得たfixture用のtarget candidate set observedを使う。

```text
target candidate set:
  maintain_C_G_span
  collapse_to_C_unison
```

これは候補集合であり、まだselected targetではない。

---

## ■ 2. Selection controller

二つの経路を比較する。

```text
Gamma_interval_target_selection = None
  → selected target = None
```

```text
Gamma_interval_target_selection_fixture
  → policy_tag = preserve_span を読み、
     selected target = maintain_C_G_span
```

このcontrollerはfixture用であり、一般的な音程解決規則ではない。

---

## ■ 3. 観測結果

| target candidate set | selection controller | selected target | voice leading | harmonic function |
|---|---|---|---|---|
| same | None | `None` | `None` | `None` |
| same | fixture | `maintain_C_G_span` | `None` | `None` |

確認できたこと。

```text
same target candidate set
different selection controller
↓
selected interval target appears / does not appear
```

さらに、

```text
selected interval target candidate
  ≠ voice leading realization
  ≠ harmonic function
```

である。

---

## ■ 4. 暫定結論

76では、target candidate set observedだけではselected interval target candidateは生じず、`Gamma_interval_target_selection`を与えた場合だけselected interval target candidateが生じることを確認した。

次に進むなら、74〜76を構造抽出し、interval labelからcontextual role / target candidate / selectionへ進む境界列を圧縮する。
