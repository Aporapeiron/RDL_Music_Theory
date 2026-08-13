# 動態Adapter候補｜構造抽出版

*対象：音程・リズムModuleで24〜41までに観測した動態境界*  
*状態：DRAFT v0.1 / 検証列からの構造配置*

## ■ 0. 位置づけ

本書は29の証拠圧縮を置き換えない。29が「何を二標本で確認し、何を一般化していないか」を記録するのに対し、本書は検証番号を一度外し、現時点で見えている接続形だけを配置する。

ここに共通state・共通controller・共通候補生成器・因果順序を導入しない。

## ■ 1. Module固有状態と用途別projection

```text
Module State
  ├─ candidate-generation view
  ├─ controller view
  └─ history view
```

一つのstate objectに入るfieldは、一つの意味単位であるとは限らない。各viewは既存利用関係から取り出す比較用projectionであり、排他的な状態分割ではない。同一fieldは複数viewに関与し得る。

```text
same_for_candidate_generation
same_for_controller
same_for_history
```

は、それぞれのviewでの同一性を読む薄い観測APIである。`state_id`の置換でも完全同一性IDでもない。

## ■ 2. Module固有recordとGeneric event

```text
Module Record
  ├─ Module固有の後続処理
  │    ├─ state再構成
  │    └─ candidate regeneration
  └─ Module固有projector
       ↓
     GenericDynamicEvent
       ├─ event_kind
       ├─ operation_kind
       ├─ operation_status
       ├─ change_axes
       └─ realization_status
```

Generic eventはrecordの抽象観測であり、Module固有stateを復元する実行命令ではない。状態再構成と候補再生成はrecordのresulting conditionを読むModule固有処理として残る。

## ■ 3. 動態経路

```text
状態
  ↓
候補生成 → 制約 → 観測
  ├─ nonempty → 選択 → realized transition
  └─ empty → 再探索 → structural record
                         ├─ operation_status
                         │    ├─ applied
                         │    └─ no_effect
                         └─ record由来の再生成を実行
                              ├─ final nonempty
                              └─ final empty
```

`empty`が生じる位置、候補生成規則、制約構造、controllerはModule固有である。再生成実行と非空結果は別軸である。

## ■ 4. 保持する非同一性

```text
record ≠ event
event_kind ≠ 実差分
operation_status=no_effect ≠ システム全体の無変化
effect ≠ realization
regeneration executed ≠ candidate nonempty
同じstate object ≠ 一つの意味単位
state identity ≠ 用途別同一性
same_for_X ≠ complete identity
same_for_X ≠ execution omission
```

候補生成入力と候補結果が同じfixtureでも、record、controller入力、履歴上の位置は別に残り得る。したがって用途別同一性は比較・説明・検査のためのものであり、遷移や再生成の省略条件ではない。

## ■ 5. 確定接続・ξ・禁止補完

**確定接続**：Module固有構造recordは、抽象event投影とrecord由来の候補再生成処理へ接続できる。音程・リズムの二標本で確認済みである。

**未解決ξ**：state IDがどのviewまで識別するか、no_effect recordの永続保存・圧縮、no_effect後のcontroller入力、Module間因果順序、第三Moduleでの接続形。

**禁止補完**：viewを共通state classへ昇格しない。Generic eventからstateを復元したことにしない。`same_for_X`から処理省略を導かない。空結果の位置を共通分類しない。
