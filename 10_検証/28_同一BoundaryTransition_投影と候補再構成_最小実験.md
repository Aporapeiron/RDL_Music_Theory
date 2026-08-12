# 検証記録：同一BoundaryTransitionの投影と候補再構成

*対象：26のリズム境界変更実験*  
*状態：DRAFT v0.1 / 同一遷移record接続の最小検証*  
*実装：`10_検証/rhythm_transition_projection_reconstruction.py`*

## ■ 0. 検証目的

27で残った接続を、リズムModule内だけで検証する。26が生成した同じ
`BoundaryTransition`を、二つの経路へ分けずに通す。

```text
BoundaryTransition
  ├→ GenericDynamicEvent(structural_transition)
  └→ resulting_grid_open
       → dynamic_candidate_space
       → target=休符を再評価
```

ここで確認するのは、同一の境界遷移recordが、構造遷移イベントとしての投影と、
後続候補空間の再構成の双方へ接続できることだけである。

## ■ 1. 検証経路

26の`run_boundary_reconstruction()`から、次の一つの`BoundaryTransition`を取得する。

```text
source_grid_open       = False
resulting_grid_open    = True
operation_kind         = reopen_grid_boundary
```

このrecord自身を投影すると、次になる。

```text
event_kind             = structural_transition
operation_kind         = reopen_grid_boundary
realization_status     = not_realized
```

`operation_status`と`change_axes`は操作名から固定せず、recordの
`source_grid_open`と`resulting_grid_open`の実差分から算出する。差分があれば
`applied` / `grid_boundary_changed`、差分がなければ`no_effect` / 空tupleとなる。

同じrecordの`resulting_grid_open=True`を26専用の
`dynamic_candidate_space()`へ渡す。`current=裏拍`と`target=休符`は変更せず、
候補空間だけを再構成する。

## ■ 2. 実測結果

```text
同一transition record
  → structural_transition event
  → operation_kind = reopen_grid_boundary
  → resulting_grid_open = True
  → candidate space = 表拍 / 裏拍 / 休符
  → target=休符
  → candidates = (休符,)
  → status = locally_resolved
```

したがって、今回のリズム実験では、`structural_transition`として投影された境界遷移と、
候補空間を変更した境界遷移が同一recordである。

## ■ 3. 境界

これはリズムModule内の接続検証であり、次を意味しない。

- 音程Moduleでも同じ候補再構成が成立する
- 三分類の共通projectorが完成した
- `structural_transition`の一般的な因果作用が確定した
- `operation_kind`だけから変更軸や適用結果を推定できる
- 履歴の因果順・時系列順が復元された
- 03の静的`candidate_space`が動的化された

候補へ休符を追加する境界定義は、26専用の最小実験に固有である。

## ■ 4. 暫定結論

26の同じ`BoundaryTransition`を、`structural_transition`の投影と、
境界依存候補生成器による候補再構成へ接続できた。

これにより、少なくともこのリズム実験では、

```text
構造遷移record
  → 構造遷移イベントとしての投影
  → 次状態の候補生成条件の変更
```

が一本の実験経路として閉じた。ただし、これはModule固有の実効性であり、
共通AdapterやModule横断不変条件へは昇格させない。
