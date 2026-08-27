# 検証記録：reentered concrete voice leadingからnext context候補境界

*対象：再入生成されたconcrete voice leading observationが、外部next context inventoryとGammaによってnext context candidate setへ接続される条件*  
*状態：DRAFT v0.1 / 135 reentered concrete voice leading後の既存80再接続境界*  
*実装：`10_検証/interval_module_next_context_candidate_reentry.py`*

---

## ■ 0. 検証目的

135では、reentered voice leading requestからconcrete voice leading observationを生成できることを確認した。

137では、そのreentered concrete voice leadingを固定し、外部next context inventoryと`Gamma_next_context_candidate_filter`を与えた場合だけnext context candidate set observedが生じることを確認する。

```text
reentered concrete voice leading observation
  + external next context inventory
  + Gamma_reentered_voice_leading_to_next_context_candidates
  + Gamma_next_context_candidate_filter_fixture
  ↓
next context candidate set observed
  ↓
selected next context / harmonic function は未生成
```

実行結果。

```text
reentered_voice_leading_connected_to_next_context_candidates_unselected
```

## ■ 1. 暫定結論

reentered concrete voice leadingだけではnext context候補集合は生じず、外部inventoryと再入Gammaを与えた場合だけnext context candidate setが観測される。

次に進むなら、next context候補集合とselection controllerを接続する。
