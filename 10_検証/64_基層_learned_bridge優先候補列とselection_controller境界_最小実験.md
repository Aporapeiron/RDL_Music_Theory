# 検証記録：基層-learned bridge・優先候補列とselection controller境界

*対象：同じprioritized bridge orderingに対してselection controllerを与えたとき、selected bridge candidateだけが生じる条件*  
*状態：DRAFT v0.1 / 63 bridge prioritization境界検証後のselection controller最小検証*  
*実装：`10_検証/base_to_learned_bridge_selection_controller_boundary.py`*

---

## ■ 0. 検証目的

63では、複数bridge candidatesに`Γ_bridge_prioritization`を与えた場合だけ、prioritized bridge orderingが生じることを確認した。

64では、同じprioritized bridge orderingを固定し、selection controllerの有無・種類だけを差し替える。

```text
same prioritized bridge ordering
  + no selection controller
  → unselected

same prioritized bridge ordering
  + Γ_bridge_selection_fixture
  → selected bridge candidate
```

ここで確認するのは、prioritized bridge orderingがselected bridge candidateではなく、selected bridge candidateもconfirmed learned categoryやselected musical interpretationではないことである。

---

## ■ 1. 固定するprioritized bridge ordering

63で得たfixture用のprioritized bridge orderingを使う。

```text
prioritized bridge ordering:
  rank 1: different_pitch_relation_label_candidate
  rank 2: uncertain_pitch_relation_label_candidate
```

このorderingは候補の順序であり、まだselectionではない。

```text
priority_rank = 1
  ≠ selected bridge candidate
```

---

## ■ 2. 差し替えるselection controller

三つの経路を比較する。

```text
selection controller = None
  → unselected
```

```text
Γ_bridge_selection_top_rank_fixture
  → priority_rank 1 をselected bridge candidateとして読む
```

```text
Γ_bridge_selection_uncertain_label_fixture
  → uncertain label candidateをselected bridge candidateとして読む
```

どちらのcontrollerもfixture用であり、一般的な音楽解釈選択規則ではない。

---

## ■ 3. 最小ケースの比較

### 3.1 controllerなし

```text
prioritized bridge ordering
+ selection controller = None
↓
status = prioritized_bridge_ordering_unselected
selected bridge candidate = None
```

### 3.2 top-rank controller

```text
prioritized bridge ordering
+ Γ_bridge_selection_top_rank_fixture
↓
selected bridge candidate
  = different_pitch_relation_label_candidate
```

### 3.3 uncertain-label controller

```text
prioritized bridge ordering
+ Γ_bridge_selection_uncertain_label_fixture
↓
selected bridge candidate
  = uncertain_pitch_relation_label_candidate
```

同じprioritized bridge orderingでも、selection controllerが変わるとselected bridge candidateは変わる。

---

## ■ 4. 観測結果

| prioritized ordering | selection controller | selected bridge candidate | selected musical interpretation | confirmed learned category |
|---|---|---|---|---|
| same | None | `None` | `None` | `False` |
| same | top-rank fixture | `different_pitch_relation_label_candidate` | `None` | `False` |
| same | uncertain-label fixture | `uncertain_pitch_relation_label_candidate` | `None` | `False` |

確認できたこと。

```text
same prioritized bridge ordering
different Γ_bridge_selection
↓
different selected bridge candidates
```

さらに、

```text
selected bridge candidate
  ≠ confirmed learned category
  ≠ selected musical interpretation
```

である。

---

## ■ 5. Module責務の確認

今回の接続は、次のように分かれる。

```text
Γ_bridge_prioritization:
  bridge候補へ順序を与える

Γ_bridge_selection:
  ordered candidatesからselected bridge candidateを選ぶ

category confirmation:
  今回は未接続

musical interpretation selection:
  今回は未接続
```

したがって、selection controllerはprioritizationではない。また、selected bridge candidateはlearned category確定でも音楽解釈確定でもない。

---

## ■ 6. まだ言えないこと

今回の検証から、次は言えない。

```text
selected bridge candidateが正しいlearned categoryであること
selected bridge candidateがselected musical interpretationであること
top-rank controllerが一般に正しいこと
uncertain-label controllerが一般に正しいこと
selection controllerの由来や採用条件が決まったこと
confirmed learned categoryの条件が決まったこと
中核音楽理論Moduleへ接続できること
```

また、今回の`Γ_bridge_selection`はfixture用であり、一般的なbridge selection ruleではない。

---

## ■ 7. 暫定結論

64では、同じprioritized bridge orderingでも、selection controllerがなければselected bridge candidateは生じず、controllerを与えた場合だけselected bridge candidateが生じることを確認した。

```text
prioritized bridge ordering
  + Γ_bridge_selection_fixture
  ↓
selected bridge candidate
```

ただし、ここで停止する。

```text
selected bridge candidate
  ≠ confirmed learned category
  ≠ selected musical interpretation
```

次に進むなら、selected bridge candidateをconfirmed learned categoryへ昇格できる条件、またはselected bridge candidateを中核音楽理論側の解釈候補へ渡す境界を見る。
