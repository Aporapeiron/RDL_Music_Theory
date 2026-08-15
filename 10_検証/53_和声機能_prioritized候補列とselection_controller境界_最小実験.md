# 検証記録：和声機能・prioritized候補列とselection controller境界

*対象：同じprioritized target candidate orderingでも、selection controllerの有無・種類によりselected targetが分岐する条件*  
*状態：DRAFT v0.1 / 52の後続検証*  
*実装：`10_検証/harmonic_function_prioritized_candidate_selection_boundary.py`*

---

## ■ 0. 検証目的

52では、同じgenerated target candidate setでも、prioritization policyが違うと候補順序が分岐することを確認した。

ただし、prioritized orderが得られたことは、selected targetが生じたことではない。

53では、52の `prefer_primary_fixture` による同じprioritized orderを固定し、selection controllerの有無・種類だけを差し替える。

```text
same prioritized target candidate ordering
  + Γ_selectionなし
  → selected targetなし

same prioritized target candidate ordering
  + Γ_select_top_rank_fixture
  → selected target = C major

same prioritized target candidate ordering
  + Γ_select_deceptive_source_fixture
  → selected target = A minor
```

ここで確認するのは、次の分離である。

```text
prioritized target candidate ordering
  ≠ selected target

selection controller
  ≠ prioritization policy
```

---

## ■ 1. 固定するprioritized order

52のprimary優先fixtureから得られる候補順序を固定する。

```text
generated target candidate set = {C major, A minor}
  + Γ_prioritize_primary_fixture
  ↓
prioritized order = C major(rank 1), A minor(rank 2)
```

これは53では固定入力である。53はtarget候補生成も、prioritizationも新しく行わない。

---

## ■ 2. 差し替えるselection controller

三つの状態を比較する。

```text
Γ_selectionなし:
  selected targetを作らない

Γ_select_top_rank_fixture:
  priority_rank = 1 を読む

Γ_select_deceptive_source_fixture:
  candidate.source = history_boundary_fixture_deceptive を読む
```

どちらのcontrollerもfixtureであり、一般和声規則ではない。

重要なのは、selection controllerが何を読むかを明示し、prioritized orderそのものをselected targetへ自動昇格しないことである。

---

## ■ 3. 最小比較

### 3.1 controllerなし

```text
prioritized order = C major, A minor
  + Γ_selectionなし
  ↓
status = prioritized_but_unselected
selected target = None
```

### 3.2 top rankを選ぶcontroller

```text
prioritized order = C major, A minor
  + Γ_select_top_rank_fixture
  ↓
selected target = C major
```

### 3.3 deceptive sourceを選ぶcontroller

```text
prioritized order = C major, A minor
  + Γ_select_deceptive_source_fixture
  ↓
selected target = A minor
```

同じprioritized orderでも、selection controllerが違えばselected targetは分岐しうる。

---

## ■ 4. 観測結果

| prioritized order | selection controller | selected target | status |
|---|---|---|---|
| `C major`, `A minor` | `None` | `None` | `prioritized_but_unselected` |
| `C major`, `A minor` | `select_top_rank_fixture` | `C major` | `selected_target` |
| `C major`, `A minor` | `select_deceptive_source_fixture` | `A minor` | `selected_target` |

確認できたこと。

```text
same prioritized target candidate ordering
  ≠ selected target

same prioritized target candidate ordering
  + different Γ_selection_fixture
  ↓
different selected target
```

さらに、rank 1候補が常にselected targetになるとは扱わない。

```text
priority_rank = 1
  ≠ selected target
```

---

## ■ 5. Module責務の確認

今回の接続は、次のように分かれる。

```text
prioritization境界:
  52のprimary優先fixtureによりprioritized orderを生成済み入力として渡す

selection境界:
  prioritized orderとselection controllerを読み、selected targetを作るかどうかを決める

声部進行境界:
  今回は未接続
```

したがって、selection境界はtarget degree planや具体音実現を作らない。

---

## ■ 6. まだ言えないこと

今回の検証から、次は言えない。

```text
どのselection controllerが正しいか
selection controllerをどの上位controllerが選ぶか
rank 1候補を常に選ぶべきこと
selected targetがtarget degree planを生成すること
selected targetが声部進行上実現可能であること
selection fixtureが一般和声規則であること
```

selection controllerの由来、適用条件、上位controllerとの接続は未解決ξとして残る。

---

## ■ 7. 暫定結論

53では、同じprioritized target candidate orderingでも、selection controllerの有無・種類によりselected targetが分岐することを確認した。

```text
C major(rank 1), A minor(rank 2)
  + Γ_selectionなし
  → selected targetなし

C major(rank 1), A minor(rank 2)
  + Γ_select_top_rank_fixture
  → C major

C major(rank 1), A minor(rank 2)
  + Γ_select_deceptive_source_fixture
  → A minor
```

したがって、次を保持する。

```text
generated target candidate set
  ≠ prioritized candidate ordering
  ≠ selected target
  ≠ target degree plan
```

53はselection境界を開いたが、44で分離したtarget degree planningや具体音実現へは進まない。