# 検証記録：音程分解・列挙済みaction set枯渇後のfallback outcome観測

*対象：現在状態から列挙した再探索枝が全てemptyになった場合の、停止・voice B境界再開・target破棄の分離*
*状態：DRAFT v0.1 / 音程分解Module候補*
*実装：`10_検証/exhaustion_fallback_observation.py`*

---

## ■ 0. 検証目的

20では、操作後も候補がemptyなら、その操作観測を消さずに履歴へ残した。
ただし、`B_change`・`Γ_change`・`upstream_target_change`を同一source stateから独立に評価しても候補が戻らない場合の扱いは、未解決ξとして残っていた。

21では、voice A側のBを狭めた後、voice B側の境界も閉じることで、列挙済みの三枝が全てemptyになる状態を作る。その後のfallback outcomeを、単一の「失敗」や自動選択へ潰さず、同じsource stateから比較観測する。

```text
current action set exhausted
  ├─ stop_search
  ├─ reopen_voice_B_boundary
  └─ discard_target
```

これは、どのfallbackが音楽一般に正しいかを決める実験ではない。候補枯渇後にどの境界を動かしたかによって、観測された候補・targetの扱いが変わることを記録する。fallback outcomeは、まだ正式な次状態遷移として採用しない。

---

## ■ 1. 列挙済みaction set枯渇状態の構成

まず20の`B_tighten`でvoice Aのtarget候補を範囲外へ置く。その後、検証用の`voice_B_boundary_tighten`でvoice Bのtarget候補も範囲外へ置く。

```text
S0
  → B_tighten
  → S1_empty

S1_empty
  → voice_B_boundary_tighten
  → S2_empty
```

voice Bのtarget degree 1（F♯）をBで除くため、現在状態から列挙した三つの再探索枝を独立に評価しても、全て`B_range_projection`で候補が消える。

```text
S2_empty
├─ B_change
│  → constraint_no_candidate
├─ Γ_change
│  → constraint_no_candidate
└─ upstream_target_change
   → constraint_no_candidate
```

ここでの`empty`は、候補が存在しないという既知の診断である。これは可能な操作全体が消滅したことではなく、現在列挙したaction setの一手先枝が枯渇したことを意味する。探索を停止すべきか、voice Bの境界を再開すべきか、targetを破棄すべきかはまだ決まっていない。

---

## ■ 2. 列挙済みaction set枯渇の記録

`ExhaustionObservation`は、同一source stateから列挙した三操作を独立に評価したことと、その全てがemptyだったことを保持する。

```text
ExhaustionObservation
├─ enumerated_branch_kinds
├─ empty_branch_kinds
└─ observations
   ├─ ActionObservation[B_change]
   ├─ ActionObservation[Γ_change]
   └─ ActionObservation[upstream_target_change]
```

三つの枝は逐次適用されず、同じ`source state`から次のように独立に記録される。

```text
operation_status = applied
candidate_status = constraint_no_candidate
evaluation = None
failure_stage = B_range_projection
```

したがって、

```text
操作を試した
≠ 候補が生まれた
≠ 比較可能である
≠ 採用された
```

という20までの分離は、action set枯渇の段階でも維持される。

---

## ■ 3. 三つのfallback outcome観測

### `stop_search`

現在のB・Γ・targetを変えずに探索を停止する。

```text
S2_empty
  → stop_search
  → terminal / no concrete transition
```

具体音は作らず、`realized_transition_history`も増やさない。停止は候補が空だった事実から自動的に導出された正解ではなく、fallback候補の一つである。

### `reopen_voice_B_boundary`

voice B側の実現境界を再び開き、同じ三操作を現在状態から再生成する。これはvoice Bの境界を開く局所操作であり、RDL的な意味で上位層のBへ退避する操作ではない。

```text
S2_empty
  → voice B境界を再開
  → candidate regeneration
```

voice Bの境界を開くと、`B_change`と`upstream_target_change`には候補が戻る。`Γ_change`はこの条件ではemptyのままである。その後どの候補を採用するかは選ばず、`selected_branch_kind = None`で保持する。

### `discard_target`

現在のtargetを破棄する。ただし、別のtargetや具体音を自動生成しない。

```text
S2_empty
  → target_discarded
  → no fabricated target
  → no concrete transition
```

`DynamicSearchState`はtarget degreeを必須入力とするため、target破棄後の完全な実現状態はまだ構成しない。`FallbackOutcomeObservation`へ`target_status = discarded`を記録し、代替target・具体音・採用枝を持たない観測で止める。

三つのfallbackは、いずれも`DynamicSearchState`の正式な次状態を返さない。ここで返すのは、同じ枯渇状態をsourceとして各fallbackを見たときのoutcome観測である。

---

## ■ 4. 三fallbackの比較

| fallback | 動かす層 | 候補 | 具体音遷移 | target |
|---|---|---|---|---|
| `stop_search` | なし | なし | なし | 保持 |
| `reopen_voice_B_boundary` | voice B境界 | 再開 | この実験では未採用 | 保持 |
| `discard_target` | 上流target | 代替生成しない | なし | 破棄 |

三者は同じ「列挙済みaction set枯渇」から出発するが、outcome観測の構造が異なる。`action_set_exhausted → failure`の一語へ潰すと、どの層を動かしたかと、その後に何が観測されたかが消える。

---

## ■ 5. `empty`と未解決ξ

既知として観測できるものは次である。

```text
enumerated_branch_kinds = B_change / Γ_change / upstream_target_change
empty_branch_kinds = B_change / Γ_change / upstream_target_change
failure_stage = B_range_projection
```

一方、次はまだ決めない。

```text
どのfallbackをcontrollerが選ぶか
voice B境界を開く権限・範囲をどう定めるか
target破棄後に何を次targetとするか
停止を終端とみなすか、上位controllerへ返すか
```

これらは未解決ξとして残す。`empty`は候補集合に関する診断であり、fallback選択の未定義性そのものではない。

---

## ■ 6. Coreとの境界

21で追加したのは、列挙済みaction setの一手先枝が枯渇した後のfallback outcomeを比較観測する検証構造である。

```text
Core
  共通の状態・操作・観測・ξの分離

21 Module
  voice B側のB閉鎖・再開
  列挙済みaction set枯渇の診断
  stop / voice-B boundary reopening / target discardの比較
```

`voice_B_boundary_tighten`、`reopen_voice_B_boundary`、target破棄後の状態形式は、音程分解Moduleの仮設に留める。Coreへ昇格させない。

---

## ■ 7. 実行結果

```text
state=S0_empty->B_tighten[empty]->voice_B_boundary_tighten[empty]->action_set_exhausted
enumerated=B_change / Γ_change / upstream_target_change
empty=B_change / Γ_change / upstream_target_change

stop_search              -> stopped
reopen_voice_B_boundary -> candidate_space_reopened
discard_target           -> target_discarded
```

assertで、列挙済みaction set枯渇の保持、voice B境界再開による候補復帰、target破棄時の具体音非生成、三fallbackの非自動選択を確認する。これらは正式な次状態の構成ではなく、fallback outcome観測として記録される。

---

## ■ 8. 未解決ξ

```text
列挙済みaction set枯渇後のfallback選択controller
voice B境界を再開する上限と権限
target破棄後の代替target生成
停止後にB_contextや上位target controllerへ戻る接続
fallback自体を履歴へどう記録するか
```

21では、fallbackを一つに決めず、候補枯渇後のoutcomeを正式な次状態へ昇格させないまま、観測可能にしたところで閉じる。
