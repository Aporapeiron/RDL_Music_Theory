# 検証記録：音程分解・fallback採用後の実状態遷移

*対象：`reopen_voice_B_boundary`を正式な実状態遷移として採用し、通常探索へ戻る接続*
*状態：DRAFT v0.1 / 音程分解Module候補*
*実装：`10_検証/fallback_state_adoption.py`*

---

## ■ 0. 検証目的

21では、列挙済みaction setの一手先枝が全てemptyになった状態から、三つのfallback outcomeを比較した。ただし、fallbackはまだ`DynamicSearchState`の次状態ではなかった。

22では、そのうち実状態を最小限構成できる`reopen_voice_B_boundary`を一つ採用する。

```text
S2_action_set_exhausted
  → reopen_voice_B_boundary
  → S3_boundary_reopened
  → ordinary action selection
  → S4_realized
```

ここで検証するのは、fallbackを選ぶ一般規則ではない。fallbackが実際にどの状態差分を作り、どの履歴へ入り、その後の通常探索へどう接続するかである。

---

## ■ 1. fallback採用の境界

21の`reopen_voice_B_boundary`は、次のoutcome観測だった。

```text
source = S2_action_set_exhausted
fallback_kind = reopen_voice_B_boundary
outcome_status = candidate_space_reopened
reopened_candidate_branch_kinds = B_change / upstream_target_change
selected_branch_kind = None
```

22では、この観測をそのまま次状態と呼ばず、fallback操作を実際に適用して新しい状態を作る。

```text
S2
  ├─ voice B boundary = F4–F4
  └─ enumerated action set exhausted

reopen_voice_B_boundary
  ↓

S3
  ├─ voice B boundary = F♯4–F♯4
  ├─ last_realized_pair = A♯4–F♯4
  └─ fallback_transition_history += 1
```

`last_realized_pair`は、fallback後に現在Bへ適合する具体音を意味しない。22でも、最後に具体音として実現した移動基準を保持する名前として扱う。

---

## ■ 2. 履歴の分離

fallbackはvoice Bの境界を変えるが、具体音をまだ採用していない。そのため履歴は次のように分かれる。

| 事象 | 保存先 | 22での増加 |
|---|---|---:|
| 列挙済みaction setのempty観測 | `observation_history` | 既存のまま |
| voice B境界を再開した実状態差分 | `fallback_transition_history` | +1 |
| fallback直後の具体音採用 | `realized_transition_history` | まだ0 |
| その後の`upstream_target_change`採用 | `realized_transition_history` | +1 |

したがって、

```text
fallbackを適用した
≠ 具体音を実現した
```

である。fallbackを`realized_transition_history`へ混ぜると、具体音遷移履歴の意味が崩れるため、別の`FallbackStateTransition`として保存する。

---

## ■ 3. fallback後の通常探索

S3からは、S2と同じ枯渇状態を参照せず、境界再開後のS3から三操作を再生成する。

```text
S3_boundary_reopened
├─ B_change
│  → selected: A♯3–F♯4
├─ Γ_change
│  → empty
└─ upstream_target_change
   → selected: E♯4–F♯4
```

直前の実差分は`boundary_changed`なので、現在の暫定controllerは`strict_relation_then_boundary`を選ぶ。この比較では、`upstream_target_change`が採用される。

```text
S3
  → upstream_target_change
  → S4_realized
  ├─ last_realized_pair = E♯4–F♯4
  ├─ voice_a_target_degree = 7
  ├─ fallback_transition_history = 1
  └─ realized_transition_history = 1
```

さらにS4からは、直前の`upstream_target_changed`を受けて`minimum_immediate_motion`へ接続する。この比較では、具体音を保ったままvoice Aの境界を広げる`B_change`が最小移動として採用される。

```text
S4
  → B_change
  → S5_realized
  ├─ fallback_transition_history = 1
  └─ realized_transition_history = 2
```

これにより、fallbackで探索が終端へ潰れず、実状態から通常の再探索循環へ戻ることを確認する。

---

## ■ 4. 22で採用しないfallback

`stop_search`と`discard_target`は、今回の実験では実状態へ採用しない。

`stop_search`は具体音を作らない終端候補であり、停止後にどのcontrollerへ返すかが未定義である。`discard_target`はtargetを破棄できても、破棄後のtarget表現と次状態の候補生成条件がまだない。

したがって、これらを無理に`DynamicSearchState`へ変換しない。

```text
stop_search     → 未解決ξ：停止後のcontroller接続
discard_target  → 未解決ξ：target破棄後の状態表現
```

---

## ■ 5. Coreとの境界

22で追加したのは、音程分解Module内のfallback採用・状態差分・履歴接続の検証である。

```text
Core
  S_t → Δ → S_t+1
  状態・操作・観測・ξの分離

22 Module
  voice B境界再開
  FallbackStateTransition
  fallback後の候補再生成
  通常actionから具体音状態への復帰
```

`fallback_transition_history`、`FallbackStateTransition`、voice B境界の再開条件はModule固有の仮設であり、Coreの状態変数や音楽一般の規則へ昇格させない。

---

## ■ 6. 実行結果

```text
S2_action_set_exhausted
  → reopen_voice_B_boundary
  → S3_boundary_reopened
  → upstream_target_change
  → S4_realized
  → B_change
  → S5_realized
```

assertで次を確認する。

- fallback適用後に`DynamicSearchState`が構成される
- `fallback_transition_history`が1件増える
- fallback直後は`realized_transition_history`が増えない
- S3から`upstream_target_change`を採用し、具体音遷移が1件増える
- S4からさらに`B_change`を採用し、通常探索が継続する
- `stop_search`・`discard_target`の未解決部分を自動的に埋めない

---

## ■ 7. 未解決ξ

```text
fallback選択controllerの一般化
stop_search後の上位controller接続
discard_target後のtarget状態表現
複数fallbackを一つの共通遷移型へ統合できるか
fallback履歴と観測履歴をどこまで永続化するか
```

22では、境界再開fallbackだけを実状態へ採用し、別のfallbackを同じ意味へ潰さない。fallback履歴と具体音遷移履歴を分離したまま、通常探索へ戻る接続を検証したところで閉じる。
