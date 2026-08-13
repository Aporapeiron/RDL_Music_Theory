# 検証記録：音程no_effect recordの候補再構成とcontroller境界

*対象：音程Moduleの`FallbackStateTransition`と`state_after_transition()`*  
*状態：DRAFT v0.1 / 候補生成入力とcontroller入力の分離観測*

---

## ■ 0. 目的

36では、実差分のない`FallbackStateTransition`から候補再生成を実行し、source／resultingの有効枝が今回fixtureで一致することを確認した。

37は、その再構成stateをそのままcontroller状態と読めるかを検査する。共通controllerやstate identityを定義せず、既存音程Moduleの入力を二つに分けて観測する。

```text
no_effect FallbackStateTransition
  source / resulting boundary = F♯4–F♯4
       ↓ state_after_transition
candidate generation inputs
  = 同じ

controller input: last_change_axes
  boundary_changed -> ()
       ↓ select_policy
strict_relation_then_boundary
  -> target_continuity_then_relation
```

## ■ 1. 実測

| 観測 | source | record再構成resulting |
|---|---|---|
| `state_id` | `S2_action_set_exhausted->reopen_voice_B_boundary` | 同じ |
| 候補生成入力 | context、最後の実現ペア、target、両boundary、ordering rule | すべて同じ |
| `last_change_axes` | `boundary_changed=True` | 空の`ChangeAxes` |
| `select_policy()` | `strict_relation_then_boundary` | `target_continuity_then_relation` |
| `fallback_transition_history` | 採用済みrecord 1件 | 同じ1件（追加なし） |

候補生成入力が同一なので、36の有効枝一致と矛盾しない。一方、`last_change_axes`は既存controllerが読む別の入力であり、同じ`state_id`でもpolicy選択は一致しない。

## ■ 2. この実験が示す境界

```text
record由来の候補再構成
  ≠ controller状態の安全な再構成

同じstate_id
  ≠ DynamicSearchStateの全フィールドが同じ
```

`state_after_transition()`は30・32・36で必要だった、recordのresulting boundaryから候補を再観測するためのModule固有ヘルパーである。この関数が`last_change_axes`もrecord値へ置く現在の実装では、候補生成結果が同じでもcontroller入力まで同じとは言えない。

また、このヘルパーは`fallback_transition_history`へrecordを追加しない。したがって、これは履歴を永続採用する操作の実装でもない。

## ■ 3. 確定範囲

```text
no_effect record
  → candidate generation inputsは今回fixtureで不変
  → candidate regenerationは実行可能
  → controller inputは変わり得る
  → record採用履歴を追加するとは限らない
```

これはno_effect後のcontroller規則、またはno_effect recordの保存規則を定めるものではない。むしろ、その二つを候補再構成から推定してはならないことを示す。

## ■ 4. 未解決ξ

- `state_id`が候補生成状態・controller状態・履歴状態のどこまで識別するか
- no_effect recordを永続履歴へ追加する条件
- no_effect record後の`last_change_axes`をcontroller入力へ渡すか
- 連続するno_effect recordの保持・圧縮・忘却

共通Adapter・共通状態・共通controller・共通履歴圧縮・因果順序・Core変更は追加しない。
