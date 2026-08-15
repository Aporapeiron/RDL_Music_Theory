# 検証記録：和声機能・target候補集合と優先順位付け境界

*対象：同じgenerated target candidate setでも、prioritization policyが違うと候補順序が分岐する条件*  
*状態：DRAFT v0.1 / 51の後続検証*  
*実装：`10_検証/harmonic_function_target_candidate_prioritization_boundary.py`*

---

## ■ 0. 検証目的

46〜51では、function observation、context、history、`B_history`、`Γ_target_candidate_generation` により、generated target candidate setが分岐しうることを確認した。

ただし、generated candidate setが得られたことは、候補に優先順位が付いたことでも、selected targetが生じたことでもない。

52では、51のfine history representationから得た同じ候補集合を固定し、外部から与えたprioritization policyだけを差し替える。

```text
same generated target candidate set
  + different Γ_target_candidate_prioritization_fixture
  ↓
different prioritized candidate ordering
  ↓
selected targetは未生成
```

ここで確認するのは、次の分離である。

```text
generated target candidate set
  ≠ prioritized target candidate set
  ≠ selected target
```

---

## ■ 1. 固定するgenerated candidate set

51のfine history representationから得られる候補集合を使う。

```text
underlying history
  ↓ B_history_fine
broad_pattern = dominant_preparation
local_pattern = deceptive_setup
  + Γ_history_boundary_sensitive_fixture
  ↓
generated target candidate set = {C major, A minor}
```

このcandidate setは、52では固定入力として扱う。52はtarget候補を新しく生成しない。

---

## ■ 2. 差し替えるprioritization policy

二つのfixture用prioritization policyを用意する。

```text
Γ_prioritize_primary_fixture:
  source = history_boundary_fixture_primary を先に置く

Γ_prioritize_deceptive_fixture:
  source = history_boundary_fixture_deceptive を先に置く
```

どちらも一般和声規則ではない。候補集合と優先順位付け境界を分けるための限定fixtureである。

---

## ■ 3. 最小比較

### 3.1 primary優先

```text
generated target candidate set = {C major, A minor}
  + Γ_prioritize_primary_fixture
  ↓
prioritized order = C major, A minor
selected target = None
```

### 3.2 deceptive優先

```text
generated target candidate set = {C major, A minor}
  + Γ_prioritize_deceptive_fixture
  ↓
prioritized order = A minor, C major
selected target = None
```

同じ候補集合でも、prioritization policyが変わると候補順序は変わる。ただし、順序づけられた先頭候補をselected targetとは扱わない。

---

## ■ 4. 観測結果

| generated candidates | prioritization policy | prioritized order | selected target |
|---|---|---|---|
| `C major`, `A minor` | `prefer_primary_fixture` | `C major`, `A minor` | `None` |
| `C major`, `A minor` | `prefer_deceptive_fixture` | `A minor`, `C major` | `None` |

確認できたこと。

```text
same generated target candidate set
  ≠ same prioritized target candidate ordering

prioritized target candidate ordering
  ≠ selected target
```

さらに、prioritization policyなしの場合は、候補集合をそのまま保持し、prioritized orderを作らない。

```text
generated candidate set observed
  + Γ_prioritizationなし
  → unprioritized_candidate_set
```

---

## ■ 5. Module責務の確認

今回の接続は、次のように分かれる。

```text
target候補生成境界:
  51のfine representationによりcandidate setを生成済み入力として渡す

prioritization境界:
  generated candidate setとprioritization policyから候補順序を作る

selection境界:
  今回は未接続
```

したがって、prioritization境界はselected targetを作らない。

---

## ■ 6. まだ言えないこと

今回の検証から、次は言えない。

```text
どのprioritization policyが正しいか
prioritization policyをどのcontrollerが選ぶか
候補順序の先頭をselected targetにしてよいこと
優先順位が声部進行・形式・聴取上の安定と一致すること
prioritization fixtureが一般和声規則であること
```

prioritization policyの由来と、prioritized candidate setからselected targetへ進むcontrollerは未解決ξとして残る。

---

## ■ 7. 暫定結論

52では、同じgenerated target candidate setでも、prioritization policyが違うと候補順序が分岐することを確認した。

```text
{C major, A minor}
  + Γ_prioritize_primary_fixture
  → C major, A minor

{C major, A minor}
  + Γ_prioritize_deceptive_fixture
  → A minor, C major
```

ただし、どちらの場合もselected targetは生成しない。

```text
generated target candidate set
  ≠ prioritized candidate ordering
  ≠ selected target
```

したがって、46〜52の流れでは、target候補生成の後段にある優先順位付け境界を、selection境界へ吸収せずに保持できた。