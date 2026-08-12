# 検証記録：二標本における構造遷移record接続の横断検査

*対象：28のリズムModule、30の音程Module*  
*状態：DRAFT v0.1 / 二標本の接続形式検査*

---

## ■ 0. 目的

28と30はそれぞれ、同一のModule固有構造遷移recordを、抽象イベントへの投影と候補再生成へ接続した。

31は二つを共通実装へまとめない。既存の二実験を個別に実行し、次の**接続形式だけ**が二標本で成立するかを検査する。

```text
Module固有の構造遷移record
  ├─ Module固有projector
  │    → structural_transition
  └─ recordのsource / resulting差分を読む
       → Module固有の候補再生成
```

## ■ 1. 比較する契約

各標本について、31は次だけを確認する。

| 項目 | 確認内容 |
|---|---|
| record操作識別子 | 空でない |
| event種別 | `structural_transition` |
| 識別子保持 | eventの`operation_kind`がrecordの識別子と一致 |
| 実現状態 | `not_realized` |
| 実差分 | source conditionとresulting conditionが異なる |
| 状態操作の結果 | `operation_status=applied` |
| 再生成接続 | record由来の条件で再生成処理を実行する（`regeneration_status=executed`） |

ここで比較しないものは次の通りである。

```text
候補語彙
状態のフィールド構造
change_axesの名前
状態復元手順
候補生成規則
event後の因果順序
```

## ■ 2. 二つの標本

```text
リズム（28）
  BoundaryTransition
  grid_open: False → True
  → structural_transition
  → (休符,)

音程（30）
  FallbackStateTransition
  voice B boundary: F4–F4 → F♯4–F♯4
  → structural_transition
  → B_change / upstream_target_change
```

どちらも候補内容は異なる。その差を抽象化しない。また、候補数や非空性は接続契約へ含めない。

## ■ 3. 実測

```text
rhythm
  operation=reopen_grid_boundary
  fixture_result_count=1

pitch
  operation=reopen_voice_B_boundary
  fixture_result_count=2
```

両標本で、record由来の差分が存在し、同じrecordの投影eventは`structural_transition / not_realized`となった。両方で再生成処理を実行し、今回のfixtureでは結果も非空だった。

```text
接続契約
  record由来の再生成処理が executed である

今回のfixture結果
  rhythm: fixture_result_count=1
  pitch:  fixture_result_count=2
```

`executed`であっても結果が空になることは許容する。20〜21で確認した通り、状態条件の変更と候補の非空性は別軸である。32では、この許容範囲を構造遷移recordの同一record経路でも実測する。

```text
record由来の再生成処理
  executed
    ├─ nonempty: rhythm 28 / pitch 30
    └─ empty:    rhythm 33 / pitch 32
```

31の検査器は、上記の非空・空を**fixture coverage**として両Moduleで確認する。`fixture_result_count`は各Moduleの今回の最終結果を数える表示値であり、raw候補空間の共通計数ではない。これは再生成接続の契約に`fixture_result_count > 0`を戻すものではない。

## ■ 4. 確定範囲

二標本で確認できたのは、次の限定形式である。

```text
Module固有の構造遷移recordは、
抽象イベント投影と、record由来の後続候補再生成の双方へ接続できる。
```

これはGenericDynamicEventが状態を復元したり、候補を生成したりするという意味ではない。二経路の根はModule固有recordであり、eventはその一方への投影である。

## ■ 5. 未解決ξ

- 複数の状態条件が同時に変わるrecordの表現
- `no_effect`構造遷移と候補再生成の関係
- 共通状態または共通候補生成器の必要条件
- eventへ因果順序・復元情報を持たせるべきか
- 三標本目でも同じ限定形式が成立するか

共通projector・共通状態・共通controllerは追加しない。
