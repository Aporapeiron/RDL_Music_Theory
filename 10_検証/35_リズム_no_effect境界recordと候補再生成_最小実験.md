# 検証記録：リズムのno_effect境界recordと候補再生成

*対象：リズムModuleの`BoundaryTransition`*  
*状態：DRAFT v0.1 / no_effectと再生成の関係検証*

---

## ■ 0. 目的

31では、`no_effect`構造遷移と候補再生成の関係を未解決ξとして残した。

35では、すでに開いているgridへ`reopen_grid_boundary`を再適用するrecordを使う。

```text
BoundaryTransition
  source_grid_open=True
  resulting_grid_open=True
  ├─ project_boundary_transition
  │    → event_kind=structural_transition
  │    → operation_status=no_effect
  │    → change_axes=()
  └─ dynamic_candidate_space
       → source / resulting とも同じ候補空間
```

## ■ 1. 実測

| 観測 | 値 |
|---|---|
| source候補空間 | `(表拍, 裏拍, 休符)` |
| resulting候補空間 | `(表拍, 裏拍, 休符)` |
| source制約後候補 | `(休符,)` |
| resulting制約後候補 | `(休符,)` |
| `operation_status` | `no_effect` |
| `change_axes` | `()` |

recordの`resulting_grid_open`から再生成処理を実行しても、source条件と同じ結果になる。候補再生成の実行可能性は、候補空間の変更を意味しない。

## ■ 2. event種別との境界

projectorは`BoundaryTransition`の履歴チャンネルを`structural_transition`へ投影する。そのためeventの種別は`structural_transition`のままだが、実差分の有無は`operation_status`と`change_axes`から別に読む。

```text
event_kind=structural_transition
  ≠ 実際に構造が変化した証明

operation_status=no_effect
change_axes=()
  → 今回のrecordは構造条件を変えていない
```

これはevent種別を変更する提案ではない。投影先の履歴分類と、recordがもつ実差分を区別するための一標本である。

## ■ 3. 確定範囲

```text
no_effect record
  → event投影は可能
  → record由来の再生成処理は実行可能
  → source / resulting候補条件は同じ
```

候補結果が非空なのは今回のfixture結果であり、`no_effect`一般の性質ではない。

## ■ 4. 未解決ξ

- 音程Moduleのno_effect構造遷移record
- no_effect recordを`structural_transition`以外へ投影すべき条件
- no_effect後の再生成を省略できる安全な条件
- no_effectと観測履歴の因果順序

03の静的候補生成器、共通Adapter・共通状態・共通controllerは変更しない。
