# 検証記録：動態Adapter候補・二標本横断契約とModule固有結果の圧縮

*対象：24〜37で確認した音程Module・リズムModuleの動態境界*
*状態：DRAFT v0.5 / 二標本横断契約とModule固有結果の圧縮*
*参照：`10_検証/24_音程分解_動態Adapterの最小境界_検証.md`〜`37_音程_no_effectrecordの候補再構成とcontroller境界_最小実験.md`*

---

## ■ 0. 目的と範囲

24〜37は、音程ModuleとリズムModuleを同じ内部状態や同じ因果規則へ統合するための検証ではない。異なるModule固有記録を、どの最小境界まで共通イベントとして読めるか、また共通化しない結果をどこに残すかを段階的に確かめた記録である。

29の今回の更新は新しい共通実装を追加しない。既存の検証結果を、二標本の横断契約、fixtureで確認した結果分岐、Module固有に残す観測へ分ける。

```text
二標本で再現したこと
  ≠ Module一般の法則

一標本で実効性を確認したこと
  ≠ 共通Adapterの機能

未検証の接続
  ≠ 暗黙に成立している接続
```

## ■ 1. 最小Adapter候補

二標本で共通に確認したのは、Module固有の記録を次の三つへ**投影できる候補境界**である。

```text
observation
structural_transition
realized_transition
```

各イベントで保持する最小形式は、24・25・27で確認した範囲では次のとおりである。

| 項目 | 二標本で確認したこと | 共通化していないこと |
|---|---|---|
| `event_kind` | 三分類の許可値へ写せる | Module内部の記録形式 |
| `operation_kind` | 空にせず不透明値として保持できる | 操作名の意味・権限・選択理由 |
| `realization_status` | 観測・構造遷移は`not_realized`、具体実現だけは`realized`として分けられる | 実現の音楽的価値・成功の一般基準 |
| `change_axes` | Module側で保持した軸をイベントに残せる | 軸名・軸集合・比較規則の共通化 |

```text
Module固有記録
  ↓ Module固有projector
最小イベント分類 + 不透明な操作識別子 + Module由来の変更軸
```

ここには、共通の候補生成器、共通の状態遷移、共通のcontrollerは含まれない。

また、`event_kind`は実効果の断言ではない。35・36の二標本により、次を分けて読む必要が確認された。

```text
event_kind
  = どの履歴・操作系統のrecordを投影したか

operation_status / change_axes
  = record上で実際に何が作用・変更されたか

realization_status
  = 具体状態の実現まで進んだか
```

したがって、`structural_transition ≠ structural_changed`である。`event_kind=structural_transition`かつ`operation_status=no_effect`、`change_axes=()`は矛盾ではなく、構造遷移系recordへの投影と実差分を別軸に保った記録である。

## ■ 2. 証拠の配置

| 構造 | 音程Module | リズムModule | 現在の扱い |
|---|---|---|---|
| 三イベントへの投影 | 24 | 25 | 二標本で確認した横断契約候補 |
| `operation_kind`の不透明保持 | 24 | 25 | 二標本で確認した横断契約候補 |
| `event_kind`と`realization_status`の対応 | 24・27 | 25・27 | 二標本で確認した横断契約候補 |
| 実差分からの`change_axes`・`operation_status`算出 | 19でModule内の状態差分 | 28で`BoundaryTransition`差分 | 実差分を読む方針は確認済み。ただし共通算出器は未検証 |
| 同一遷移recordの投影と候補再構成への接続 | 30 | 28 | 二標本で比較した接続形式 |
| 構造遷移recordから再生成処理を実行 | 30・32・31 | 28・33・31 | 二標本の横断契約候補。非空性は含めない |
| 構造遷移後の候補再構成 | 30 | 26・28 | 二標本で比較したModule固有の実効性 |
| 再生成実行と最終結果の非空性の分離 | 30・32・31 | 28・33・31 | 非空・空の両結果を二標本のfixtureで確認。契約へは含めない |
| 生候補あり・最終空の位置 | 32・34 | 33・34 | 生候補は両標本で確認。ただし空位置の共通分類は未検証 |
| `no_effect`recordの再生成 | 36 | 35 | 再生成は実行でき、今回fixtureでsource / resulting候補結果は同じ。二標本 |
| `event_kind`と実差分の分離 | 36 | 35 | `structural_transition`は履歴・操作系統の分類。実差分は`operation_status`・`change_axes`から読む。二標本 |
| 候補再構成stateとcontroller入力の差 | 37 | — | 音程一標本。候補生成入力が同一でも`last_change_axes`とpolicyは変わり得る。横断契約へは含めない |

この表で「未検証」とした欄を、他方のModuleから推定して埋めない。二標本の欄も、候補生成規則や状態意味の共通性を意味しない。

## ■ 3. 二標本で比較できた一本化経路

28により、リズムModuleでは26の同じ`BoundaryTransition`が次の二経路へ接続された。

```text
BoundaryTransition
  source_grid_open=False
  resulting_grid_open=True
  operation_kind=reopen_grid_boundary
       ├─ 実差分を読む
       │    → structural_transition
       │    → operation_status=applied
       │    → change_axes=(grid_boundary_changed,)
       └─ resulting_grid_openを候補生成条件へ渡す
            → dynamic_candidate_space
            → target=休符の候補を再生成
```

30では音程Moduleでも、22の同じ`FallbackStateTransition`を二経路へ接続した。

```text
FallbackStateTransition
  source_voice_b_boundary=F4–F4
  resulting_voice_b_boundary=F♯4–F♯4
       ├─ project_fallback
       │    → structural_transition
       └─ resulting_voice_b_boundaryをsource stateへ反映
            → observe_actions
            → B_change / upstream_target_change
```

二標本で比較できるのは、次の限定形式である。

```text
Module固有の構造遷移recordは、
Module固有projectorによるstructural_transitionと、
recordが保存するresulting conditionを読む候補再生成の双方へ接続できる。
```

これは`structural_transition`一般が常に候補空間を変えるという主張ではない。リズムの休符追加は26専用の`dynamic_candidate_space()`、音程の有効枝再観測は19の`observe_actions()`に限られる。

31では、同一recordからの投影と再生成実行を横断契約として検査し、非空性はfixture条件へ分離した。32・33では、音程・リズム双方に、実差分を持つ同一recordから再生成を実行しても、最終結果が空のまま残る標本を追加した。

```text
再生成処理の実行
  ≠ 候補が非空であること
```

34では、32・33とも生候補が観測され、空はModule固有の後続段階で生じたことを確認した。音程は`B_range_projection`、リズムは現在値除外とtarget制約の交差である。これは再生成接続の二標本契約を強めるものではなく、空位置の共通分類へ昇格させる根拠にもならない。

35・36では、実差分のない構造遷移系recordも、`structural_transition`へ投影して再生成処理へ接続できることを確認した。`event_kind`は履歴・操作系統の分類であり、実差分は`operation_status`と`change_axes`から読む。source／resulting候補結果の一致は今回fixtureに限る。

```text
structural-transition系record
  ├─ applied
  │    └─ regeneration → final nonempty / final empty
  └─ no_effect
       └─ regeneration → source / resulting同一（35・36のfixture）
```

この分岐は候補結果の一般則ではない。`event_kind`、実効果、再生成結果を別軸として記録できることの現在地である。

37では、36の音程no_effect recordを`state_after_transition()`へ通したとき、候補生成器が読む入力はsourceと同一でも、controllerが読む`last_change_axes`は`boundary_changed=True`から空へ変わることを観測した。その結果、既存の`select_policy()`は別の方針を返す。さらにこのヘルパーはfallback履歴へrecordを追加しない。

```text
record由来の候補再構成
  ≠ controller状態の安全な再構成
  ≠ recordを永続履歴へ採用すること
```

これは音程一標本のModule固有境界であり、state identityやno_effect後のcontroller規則を決定する根拠ではない。

## ■ 4. 現時点で昇格しないもの

次は、29でもAdapter候補へ含めない。

```text
共通projector
共通change_axes
共通状態
共通候補生成器
共通controller
fallbackの選択原理
Module間の因果・時系列順
二標本のrecordから共通状態を再構成すること
状態内容と履歴を含めたstate identityの定義
連続するno_effect recordの保持・圧縮・忘却
```

特に、24・25の`project_state()`出力は履歴チャンネルごとの投影順であり、実際の時系列や因果順を表さない。29は`sequence_id`・`event_id`・`caused_by`を追加しない。

## ■ 5. 次の分岐条件

次に検証を増やす場合も、29の圧縮結果から自動的に共通Adapterを実装しない。

次は、二標本の形式から自動的に共通Adapterを実装しない。共通実装を検討するには、少なくとも二標本で保存される入出力契約と、反例として許容すべき差分を別に定める必要がある。

## ■ 6. 暫定結論

24〜36から、次の三層を区別して保持する。

```text
二標本で確認したAdapter候補境界
  三イベント分類
  operation_kindの不透明保持
  realization_statusの分離
  event_kindと実差分の分離

二標本で比較した接続形式
  Module固有の構造遷移record
    → structural_transitionへの投影
    → recordのresulting conditionによる再生成処理の実行

fixtureで二標本に確認した結果分岐
  regeneration executed
    → final nonempty
    → final empty

Module固有に残る観測
  リズム：raw candidate spaceと制約後候補の差
  音程：声部範囲投影後の空
  空結果が生じる位置
state identityとno_effect履歴の扱い
候補再構成stateとcontroller stateの関係
```

この区別を保つ限り、`structural_transition`は単なる分類名に留まらず、二つのModuleで後続候補生成処理へ接続された実遷移の投影として読める。一方で、その接続を共通Adapter・共通状態・共通empty分類・共通因果構造へ一般化する根拠は、まだ存在しない。
