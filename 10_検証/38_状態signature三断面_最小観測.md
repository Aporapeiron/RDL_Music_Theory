# 検証記録：状態signatureの三断面

*対象：音程Moduleの`DynamicSearchState`*  
*状態：DRAFT v0.1 / state IDの比較可能範囲の観測*

37のsource／resultingを、既存fieldから三つの比較用signatureへ分ける。

```text
同じ state_id
├─ candidate-generation signature : 同じ
├─ controller signature           : 異なる
└─ history signature              : 同じ
```

candidate-generation signatureはcontext・最後の実現ペア・target・boundary・ordering ruleである。controller signatureは最後のpolicy・branch・change axes・具体実現履歴、history signatureは三履歴列である。

三signatureは排他的な状態分割ではない。同一fieldが複数の観測断面に含まれ得る。たとえば`realized_transition_history`は、現行controllerが読むためcontroller signatureにも、保存済み記録であるためhistory signatureにも入る。signatureは永久の型定義ではなく、現在の利用関係から得る比較用projectionである。

このfixtureでは`last_change_axes`だけがcontroller signatureを異ならせる。`state_after_transition()`は履歴を追加しないので、history signatureは同一に留まる。

したがって、現在の`state_id`は少なくとも三signatureすべての完全同一性IDではない。これはstateを三クラスへ分割する提案でも、共通state・共通controller・state ID規則を導入する提案でもない。
