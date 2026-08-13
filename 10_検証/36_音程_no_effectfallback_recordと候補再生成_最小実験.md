# 検証記録：音程のno_effect fallback recordと候補再生成

*対象：音程Moduleの`FallbackStateTransition`*  
*状態：DRAFT v0.1 / no_effectと再生成の関係検証*

---

## ■ 0. 目的

35ではリズムModuleで、実差分のない`BoundaryTransition`が`structural_transition`へ投影されても、実効果は`no_effect`として別に残ることを確認した。

36は音程Moduleの対称標本である。すでに開いているvoice B境界へ同じ`reopen_voice_B_boundary`recordを置く。

```text
FallbackStateTransition
  source_voice_b_boundary = F♯4–F♯4
  resulting_voice_b_boundary = F♯4–F♯4
  ├─ project_fallback
  │    → structural_transition
  │    → no_effect / ()
  └─ state_after_transition
       → observe_actions
       → source / resulting で同じ有効枝
```

## ■ 1. 実測

| 観測 | 値 |
|---|---|
| `event_kind` | `structural_transition` |
| `operation_status` | `no_effect` |
| `change_axes` | 空の`ChangeAxes` |
| source有効枝 | `B_change`、`upstream_target_change` |
| resulting有効枝 | `B_change`、`upstream_target_change` |

source／resultingのvoice B境界とstate IDは同じである。`state_after_transition()`は操作名から再開を推定せず、recordのresulting boundaryを反映するため、候補再観測もsourceと一致する。

## ■ 2. event種別との境界

```text
event_kind=structural_transition
  = fallback transition historyに属するrecordの投影

operation_status=no_effect
change_axes=()
  = record上で構造条件は変わっていない
```

35・36により、履歴・操作系統の分類と、record実差分から導く実効果は二標本で別に読める。Genericイベントへ投影した際に`RealizationBoundary`自体は渡さず、状態復元と候補再生成は引き続きModule固有recordから行う。

## ■ 3. 確定範囲

```text
no_effect fallback record
  → event投影は可能
  → record由来の候補再生成は実行可能
  → source / resultingの候補結果は今回fixtureで一致
```

最後の一致はno_effect一般の性質ではない。二標本で確認したのは、実差分がなくても`event_kind`・実効果・再生成結果を別軸で記録できることまでである。

## ■ 4. 未解決ξ

- no_effect recordの再生成を省略できる安全な条件
- no_effectをどの履歴へ保存すべきか
- no_effect後のcontroller入力
- 連続するno_effect recordの圧縮・忘却

共通Adapter・共通状態・共通controller・因果順序・Core変更は追加しない。
