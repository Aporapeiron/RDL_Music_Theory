# 検証記録：reentered target候補集合からselection境界

*対象：再入生成されたtarget candidate set observedが、selection controllerによってselected interval target candidateへ接続される条件*  
*状態：DRAFT v0.1 / 132 reentered target候補集合後の既存76再接続境界*  
*実装：`10_検証/interval_module_target_selection_reentry.py`*

---

## ■ 0. 検証目的

132では、reentered contextual role annotation candidateからtarget candidate set observedを生成できることを確認した。

133では、そのreentered target candidate set observedを固定し、`Gamma_interval_target_selection`を与えた場合だけselected interval target candidateが生じることを確認する。

```text
reentered target candidate set observed
  + Gamma_reentered_target_candidates_to_selection
  + Gamma_interval_target_selection_fixture
  ↓
selected interval target candidate
  ↓
voice leading / harmonic function は未生成
```

ここで確認するのは、候補集合があることと、候補が選択されていることを分けることである。

---

## ■ 1. 入力として固定するreentered target candidate set

132で得た再入target candidate setを使う。

```text
reentered target candidate set:
  maintain_C_G_span
  collapse_to_C_unison
```

これは候補集合であり、まだselected targetではない。

```text
reentered target candidate set observed
  ≠ selected interval target candidate
```

---

## ■ 2. Selection controller

既存76と同じfixture controllerを使う。

```text
Gamma_interval_target_selection_fixture:
  selected_policy_tag = preserve_span
```

このcontrollerはfixture用であり、一般的な音程解決規則ではない。

---

## ■ 3. 観測結果

| reentered target candidate set | reentry Gamma | selection controller | selected target | voice leading |
|---|---|---|---|---|
| same | None | None | `None` | `None` |
| same | fixture | fixture | `maintain_C_G_span` | `None` |

実行結果。

```text
reentered_target_candidates_connected_to_selection_not_voice_leading
```

確認できたこと。

```text
same reentered target candidate set
different Gamma_reentered_target_candidates_to_selection
↓
selected interval target appears / does not appear
```

さらに、

```text
selected interval target candidate
  ≠ voice leading plan
  ≠ harmonic function
```

である。

---

## ■ 4. 暫定結論

133では、reentered target candidate set observedだけではselected interval target candidateは生じず、再入Gammaとselection controllerを与えた場合だけselected interval target candidateが生じることを確認した。

これにより、125〜127で既存70へ着地したprocessing request系列は、128〜133を通じて既存71〜76のselection境界まで再接続された。

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
  ↓
selected interval target
```

ただし、まだvoice leading計画、具体音実現、harmonic annotationは生成しない。

次に進むなら、reentered selected targetとvoice leading計画境界を接続する。
