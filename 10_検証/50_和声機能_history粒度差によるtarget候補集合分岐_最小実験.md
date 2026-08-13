# 検証記録：和声機能・history粒度差によるtarget候補集合分岐

*対象：同じhistory大分類でも、Γが読むhistory粒度が違えばtarget候補集合が分岐する条件*  
*状態：DRAFT v0.1 / 49の後続検証*  
*実装：`10_検証/harmonic_function_generation_history_granularity.py`*

---

## ■ 0. 検証目的

49では、同じcurrent function observationと同じ生成規則でも、`history.local_pattern` を変えるとtarget候補集合が変わることを確認した。

50では、historyの大分類を同じにしたまま、局所粒度だけを変える。

```text
same current function observation
  + same Γ_target_candidate_generation_fixture
  + same history.broad_pattern
  + different history.local_pattern
  ↓
different generated target candidate sets
```

ここで確認するのは、history大分類が同じであることだけでは、今回のΓが読む履歴粒度を代替できないことである。

---

## ■ 1. 固定するcurrent function observation

current function observationは49と同じものに固定する。

```text
G major triad
  + C major
  ↓
degree 5
  ↓
function annotation = dominant_candidate
```

---

## ■ 2. 固定する生成規則

今回は一つのlocal-pattern-sensitive fixture規則を使う。

```text
Γ_local_pattern_sensitive_fixture:
  dominant_candidate + C major
  + broad_pattern = dominant_preparation
  + local_pattern = ordinary_preparation
    → {C major}

  dominant_candidate + C major
  + broad_pattern = dominant_preparation
  + local_pattern = deceptive_setup
    → {C major, A minor}
```

これは一般和声規則ではない。history粒度境界を観測するための限定fixtureである。

---

## ■ 3. 差し替えるhistory粒度

二つのhistory fixtureを用意する。

```text
History A:
  broad_pattern = dominant_preparation
  local_pattern = ordinary_preparation

History B:
  broad_pattern = dominant_preparation
  local_pattern = deceptive_setup
```

大分類は同じである。

```text
same history.broad_pattern = true
```

局所粒度だけが異なる。

```text
same history.local_pattern = false
```

---

## ■ 4. 最小比較

### 4.1 ordinary local pattern

```text
dominant_candidate + C major
  + Γ_local_pattern_sensitive_fixture
  + broad_pattern = dominant_preparation
  + local_pattern = ordinary_preparation
  ↓
generated target candidate set = {C major}
```

### 4.2 deceptive local pattern

```text
dominant_candidate + C major
  + Γ_local_pattern_sensitive_fixture
  + broad_pattern = dominant_preparation
  + local_pattern = deceptive_setup
  ↓
generated target candidate set = {C major, A minor}
```

同じcurrent function observation、同じ生成規則、同じhistory大分類でも、Γが読むhistory局所粒度が変わると候補集合が変わる。

---

## ■ 5. 観測結果

| current function observation | generation rule | broad pattern | local pattern | generated target candidates |
|---|---|---|---|---|
| `dominant_candidate / C major` | `local_pattern_sensitive_dominant_fixture_targets` | `dominant_preparation` | `ordinary_preparation` | `C major` |
| `dominant_candidate / C major` | `local_pattern_sensitive_dominant_fixture_targets` | `dominant_preparation` | `deceptive_setup` | `C major`, `A minor` |

確認できたこと。

```text
same current function observation
  + same Γ_target_candidate_generation_fixture
  + same history.broad_pattern
  + different history.local_pattern
  ↓
different generated target candidate sets
```

したがって、history大分類は今回のfixtureでΓが読むhistory局所粒度を代替しない。

---

## ■ 6. Module責務の確認

今回の接続は、次のように分かれる。

```text
和声機能Module:
  current function observationを渡す

history境界:
  broad_patternとlocal_patternを持つhistory fixtureを渡す

target候補生成境界:
  同じΓ_local_pattern_sensitive_fixtureを適用する
  current observationと、
  今回参照するhistory.local_patternに応じて候補集合を生成する

選択境界:
  今回は未接続
```

50では、target候補集合を生成するが、selected targetは作らない。

---

## ■ 7. まだ言えないこと

今回の検証から、次は言えない。

```text
historyの正しい粒度
broad_patternとlocal_patternの一般的な分け方
local_patternをどう観測するか
local_pattern_sensitive fixtureが一般和声規則であること
生成規則をどのcontrollerが選ぶか
selected targetが決まること
```

history粒度はfixtureであり、一般的な `ξ_history_granularity` は未解決である。

---

## ■ 8. 暫定結論

50では、同じcurrent function observation、同じ生成規則、同じhistory大分類でも、history.local_patternを変えると生成されるtarget候補集合が変わることを確認した。

```text
dominant_candidate + C major
  + Γ_local_pattern_sensitive_fixture
  + broad_pattern = dominant_preparation
  + local_pattern = ordinary_preparation
  → {C major}

dominant_candidate + C major
  + Γ_local_pattern_sensitive_fixture
  + broad_pattern = dominant_preparation
  + local_pattern = deceptive_setup
  → {C major, A minor}
```

したがって、今回のfixtureでは、history大分類は候補生成に必要な履歴粒度を代替しない。

```text
generated target candidate set
  = C(current function observation, history.local_pattern; Γ_target_candidate_generation_fixture)
```

ただし、これはfixture内の限定表現であり、一般和声規則ではない。historyをどの粒度で保持し、どの軸をΓが読むかは未解決ξとして残る。
