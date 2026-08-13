# 検証記録：和声機能・B_history粒度差によるtarget候補集合分岐

*対象：同じunderlying historyでも、B_historyの保持粒度が違うとtarget候補集合が分岐する条件*  
*状態：DRAFT v0.1 / 50の後続検証*  
*実装：`10_検証/harmonic_function_generation_history_boundary_granularity.py`*

---

## ■ 0. 検証目的

50では、同一history大分類内のlocal_pattern差がcandidate setへ影響することを確認した。

ただし50は、coarse historyとfine historyを比較したわけではない。二つのhistory fixtureはどちらも `broad_pattern + local_pattern` を持っていた。

51では、同じunderlying historyを、異なる `B_history` で投影する。

```text
same underlying history
  ↓ B_history_coarse
coarse history representation

same underlying history
  ↓ B_history_fine
fine history representation
```

ここで確認するのは、次である。

```text
same underlying history
  + same current function observation
  + same Γ_target_candidate_generation_fixture
  + different history representation under B_history
  ↓
different generated target candidate sets
```

---

## ■ 1. 固定するunderlying history

underlying historyは一つに固定する。

```text
underlying history:
  prior_context = C major
  broad_pattern = dominant_preparation
  local_pattern = deceptive_setup
```

これは直接Γへ渡さない。`B_history` によってhistory representationへ投影する。

---

## ■ 2. 差し替えるB_history

二つのhistory境界を用意する。

```text
B_history_coarse:
  exposes broad_pattern
  does not expose local_pattern

B_history_fine:
  exposes broad_pattern
  exposes local_pattern
```

同じunderlying historyでも、B_historyが違えばΓが読めるhistory featureが変わる。

---

## ■ 3. 固定する生成規則

今回は一つのhistory-boundary-sensitive fixture規則を使う。

```text
Γ_history_boundary_sensitive_fixture:
  broad_pattern = dominant_preparation
  local_pattern = None
    → {C major}

  broad_pattern = dominant_preparation
  local_pattern = deceptive_setup
    → {C major, A minor}
```

これは一般和声規則ではない。B_historyによる履歴表現粒度の違いを観測するための限定fixtureである。

---

## ■ 4. 最小比較

### 4.1 coarse representation

```text
underlying history
  ↓ B_history_coarse
broad_pattern = dominant_preparation
local_pattern = None
  + Γ_history_boundary_sensitive_fixture
  ↓
generated target candidate set = {C major}
```

### 4.2 fine representation

```text
underlying history
  ↓ B_history_fine
broad_pattern = dominant_preparation
local_pattern = deceptive_setup
  + Γ_history_boundary_sensitive_fixture
  ↓
generated target candidate set = {C major, A minor}
```

同じunderlying history、同じcurrent function observation、同じ生成規則でも、B_historyが保持するhistory representationが変わると候補集合が変わる。

---

## ■ 5. 観測結果

| underlying history | B_history | exposed broad pattern | exposed local pattern | generated target candidates |
|---|---|---|---|---|
| same | `B_history_coarse` | `dominant_preparation` | `None` | `C major` |
| same | `B_history_fine` | `dominant_preparation` | `deceptive_setup` | `C major`, `A minor` |

確認できたこと。

```text
same underlying history
  ≠ same history representation under B_history

history representation under B_history
  ≠ generated target candidate set
```

さらに、同じunderlying historyでも、B_historyが違うと今回のΓが読めるfeaturesが変わり、candidate setが分岐した。

---

## ■ 6. Module責務の確認

今回の接続は、次のように分かれる。

```text
history境界:
  underlying historyを直接使わず、
  B_history_coarse / B_history_fineでrepresentationへ投影する

target候補生成境界:
  history representationとcurrent function observationを読む
  同じΓ_history_boundary_sensitive_fixtureでcandidate setを生成する

選択境界:
  今回は未接続
```

51では、target候補集合を生成するが、selected targetは作らない。

---

## ■ 7. まだ言えないこと

今回の検証から、次は言えない。

```text
underlying historyをどう観測するか
B_history_coarse / B_history_fineをどのcontrollerが選ぶか
history representationの正しい粒度
local_patternを保持すべき一般条件
history-boundary-sensitive fixtureが一般和声規則であること
selected targetが決まること
```

B_historyの選択とhistory representation粒度はfixtureであり、一般的な `ξ_history_granularity` は未解決である。

---

## ■ 8. 暫定結論

51では、同じunderlying historyでも、B_historyの保持粒度が違うと、同じΓが生成するtarget候補集合が変わることを確認した。

```text
underlying history
  ↓ B_history_coarse
broad_pattern only
  + Γ
  → {C major}

underlying history
  ↓ B_history_fine
broad_pattern + local_pattern
  + Γ
  → {C major, A minor}
```

したがって、次を分離して保持する必要がある。

```text
underlying history
  ≠ history representation under B_history
  ≠ Γが参照できるhistory features
  ≠ generated target candidate set
```

ただし、これはfixture内の限定表現であり、一般和声規則ではない。B_historyの粒度選択は未解決ξとして残る。
