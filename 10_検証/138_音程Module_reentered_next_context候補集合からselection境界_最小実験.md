# 検証記録：reentered next context候補集合からselection境界

*対象：再入生成されたnext context candidate set observedが、selection controllerによってselected next context candidateへ接続される条件*  
*状態：DRAFT v0.1 / 137 reentered next context候補集合後の既存81再接続境界*  
*実装：`10_検証/interval_module_next_context_selection_reentry.py`*

---

## ■ 0. 検証目的

137では、reentered concrete voice leadingからnext context candidate set observedを生成できることを確認した。

138では、そのreentered next context candidate setを固定し、`Gamma_next_context_selection`を与えた場合だけselected next context candidateが生じることを確認する。

```text
reentered next context candidate set observed
  + Gamma_reentered_next_context_candidates_to_selection
  + Gamma_next_context_selection_fixture
  ↓
selected next context candidate
  ↓
harmonic function は未生成
```

実行結果。

```text
reentered_next_context_candidates_connected_to_selection_not_harmonic_function
```

## ■ 1. 暫定結論

reentered next context candidate setだけではselected next contextは生じず、再入Gammaとselection controllerを与えた場合だけselected next context candidateが生じる。

次に進むなら、selected next contextとharmonic function annotationの整合候補境界を見る。
