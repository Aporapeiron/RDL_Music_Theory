# 検証記録：音程分解・動態Adapterの最小境界

*対象：23で圧縮した音程分解Moduleの動態を、音楽語彙を含まないイベント表現へ投影する最小検証*
*状態：DRAFT v0.1 / Adapter候補*
*参照：`10_検証/23_音程分解_10〜22の動態圧縮_全体構造.md`*

---

## ■ 0. 目的と範囲

23では、音程分解Module内で次の循環が閉じた。

```text
候補生成 → 制約 → 採用 → 状態更新 → 再探索
                                ↓
                         empty / action-set exhaustion
                                ↓
                             fallback
                                ↓
                          通常探索へ復帰
```

24では、この循環を別の音楽理論へ一般化しない。音程Moduleの具体状態を、後段の動態観測が読める最小イベントへ投影できるかだけを確認する。

Adapterの対象は次の三つである。

```text
module observation
  → generic observation event

module fallback transition
  → generic structural transition event

module realized transition
  → generic realized transition event
```

ここでのAdapterは、次を行わない。

- `B`・`Γ`・targetの意味をCoreへ移す
- fallbackの選択controllerを決める
- emptyを自動的にξへ変換する
- 音楽固有の候補生成や採用規則を一般法則にする
- 投影後のイベントから新しい状態を推定する

したがって、24の成果は「一般動態が確定した」ことではなく、「Module固有の実装を壊さず、観測単位だけを共通化できる最小境界」である。

---

## ■ 1. Adapterの入力境界

音程Moduleには、すでに三種類の記録がある。

| Module側の記録 | 内容 | Adapterでの扱い |
|---|---|---|
| `ActionAttemptRecord` | 操作を評価・観測した結果。候補がemptyでも含む | 観測イベントへ投影 |
| `FallbackStateTransition` | fallbackを実状態へ適用した構造遷移 | 構造遷移イベントへ投影 |
| `DynamicStateTransition` | ordinary actionを採用し、具体音を実現した遷移 | 実現遷移イベントへ投影 |

同じ操作から三種類が同時に生じるとは限らない。Adapterは、入力された記録の種類を保ったまま、共通の最小フィールドへ写像する。

```text
module-specific record
  ├─ source_state_id
  ├─ resulting_state_id（Module記録に存在する場合）
  ├─ operation_kind（Module側の識別子を不透明に保持）
  ├─ operation_status
  ├─ change_axes
  └─ outcome-specific fields
          ↓ Adapter
generic event
  ├─ event_kind
  ├─ history_channel
  ├─ operation_kind
  ├─ source_state_id
  ├─ resulting_state_id（Module記録に存在する場合）
  ├─ operation_status
  ├─ change_axes
  └─ realization_status
```

`change_axes`は、音程Moduleの`B_change`や`Γ_change`という名前ではなく、変更の有無を示す抽象軸へ投影する。軸の意味そのものをCoreの状態変数へ追加するわけではない。

---

## ■ 2. 共通イベントの最小語彙

24で共通化するのは、次の分類と記録関係だけである。

```text
event_kind
  observation
  structural_transition
  realized_transition

history_channel
  observation_history
  fallback_transition_history
  realized_transition_history

operation_kind
  Module側の操作・遷移識別子を、意味を解釈せず不透明な値として保持

realization_status
  not_realized
  realized
```

この四つは同じ意味を重ねて持たない。

| 軸 | 読むこと |
|---|---|
| `event_kind` | どの履歴・操作系統のrecordを投影したか |
| `operation_status` / `change_axes` | record上で実際に作用・変更があったか |
| `realization_status` | 具体状態の実現まで進んだか |

したがって、`event_kind = structural_transition`は「実際に構造が変わった」という保証ではない。35の同値`BoundaryTransition`のように、構造遷移系の履歴recordとして投影されながら、`operation_status = no_effect`かつ`change_axes = ()`となる場合がある。`event_kind`は改名せず、履歴・操作系統の分類として保持する。

この分類は、次の三つを分けるために置く。

```text
見た
  ≠ 構造状態を変更した
  ≠ 具体状態を実現した
```

特に、候補がemptyである観測は`event_kind = observation`かつ`realization_status = not_realized`になる。これはemptyをξと断定することでも、fallbackを選択することでもない。

---

## ■ 3. Adapterが保持するもの／保持しないもの

### 3.1 保持するもの

- 操作・遷移の種類
- source stateと、Module記録に存在する場合のresulting state識別子
- Module側の操作・遷移識別子（`branch_kind`・`fallback_kind`・`selected_branch_kind`）
- 適用されたか、効果がなかったかという操作状態
- 状態差分から得た変更軸
- 具体状態が実現したかどうか
- どの履歴層へ記録されたか
- Module側で既知のoutcomeと、別途残された未解決接続の区別

### 3.2 保持しないもの

- `voice_A`・`voice_B`、音度、声域などの音楽固有の意味
- `B`・`Γ`・targetを共通状態の構成要素とすること
- fallbackの優先順位や権限
- controllerの更新規則
- targetなし状態の生成方法
- 履歴の忘却・重み付け・終端条件

後者を保持しないのは情報を捨てるためではない。音楽Moduleがまだ確定していない規則を、Adapterが先回りして一般化しないためである。

---

## ■ 4. 最小投影

概念上の投影は次の通りである。

```text
project_observation(ActionAttemptRecord)
  → event_kind = observation
  → history_channel = observation_history
  → operation_kind = record.branch_kind
  → realization_status = not_realized

project_fallback(FallbackStateTransition)
  → event_kind = structural_transition
  → history_channel = fallback_transition_history
  → operation_kind = transition.fallback_kind
  → realization_status = not_realized

project_realized(DynamicStateTransition)
  → event_kind = realized_transition
  → history_channel = realized_transition_history
  → operation_kind = transition.selected_branch_kind
  → realization_status = realized
```

この投影で`structural_transition`となるのは、fallback transition historyに属するrecordだからである。実差分の有無は、投影後も`operation_status`と`change_axes`を確認して読む。

`project_fallback`は、fallback後に具体音が続けて実現した場合でも、その後続の実現遷移を自身へ吸収しない。同様に、`project_observation`は候補が存在した観測であっても、採用された実現遷移へ昇格しない。

---

## ■ 5. 実測対象

`dynamic_adapter_boundary.py`では、二つの経路を投影する。

### 5.1 通常探索経路

```text
S0
  ↓ ordinary action
S1_realized
```

ここでは、操作観測は`observation_history`へ、採用された具体音遷移は`realized_transition_history`へ投影される。fallbackイベントは生成されない。

### 5.2 fallback復帰経路

```text
S2_action_set_exhausted
  ↓ reopen_voice_B_boundary
S3_structural
  ↓ ordinary action
S4_realized
```

ここでは、境界再開は`fallback_transition_history`へ、S3以降の具体音採用は`realized_transition_history`へ投影される。S2での枯渇枝の観測は`observation_history`へ残る。

期待する分離は次の通りである。

| 経路 | observation | structural transition | realized transition |
|---|---:|---:|---:|
| 通常探索 | あり | なし | あり |
| fallback復帰直後 | あり | あり | なし |
| fallback後の通常探索 | あり | あり（累積） | あり |

---

## ■ 6. 観測結果の意味

この実験が確認するのは、次の構造だけである。

```text
Module固有の三履歴
  ↓ 保持したまま投影
共通イベント群
  ↓
観測・構造遷移・具体実現を別イベントとして読める
```

これは、異なるModuleでも同じイベント分類が使える可能性を示す。しかし、異なるModuleが同じ`change_axes`を持つこと、同じcontrollerで動くこと、同じfallbackを持つことまでは示さない。

```text
イベント境界を共通化できる
  ≠ 状態意味を共通化できる
  ≠ controllerを共通化できる
  ≠ Coreへ追加できる
```

---

## ■ 7. 未解決ξ

```text
複数Moduleで同じevent_kindを採用できるか
Moduleごとに異なるchange_axesをどう保持するか
fallback outcomeをAdapterへ入力する前の選択責任
stop_search / discard_targetの状態表現
三履歴間の因果順序を再構成できるか
イベント群から一般状態を再構成できるか
履歴の保持範囲・忘却・重み付け
```

`project_state()`の出力順は、`observation_history`・`fallback_transition_history`・`realized_transition_history`という履歴チャンネル別の投影順であり、実際の因果・時系列順を表さない。将来、時間軸を復元する必要が生じた場合の`sequence_id`・`event_id`・`caused_by`などは、24では追加しない。

24は、これらを埋めずにAdapterの入力・出力境界だけを検証する。

---

## ■ 8. Coreとの境界

24で追加するのは、音程Moduleの記録を観測イベントへ写像する検証器だけである。

```text
Core
  S_t → Δ → S_t+1
  B / M_B / W / F / E / H / ξ

音程分解Module
  DynamicSearchState
  ActionAttemptRecord
  FallbackStateTransition
  DynamicStateTransition

Adapter検証
  GenericDynamicEvent
  event_kind
  history_channel
  operation_kind
  realization_status
```

`GenericDynamicEvent`はCoreの新しい状態変数ではない。Moduleの履歴を別の観測器が読むための投影結果である。

---

## ■ 9. 検証状態

24は、通常探索とfallback復帰の二経路で、次をassertする。

```text
empty観測 → observation event
fallback適用 → structural transition event
具体音採用 → realized transition event
```

三イベントの履歴チャンネルが混ざらず、fallback後の具体音採用がfallbackイベントへ吸収されないことを確認して閉じる。
