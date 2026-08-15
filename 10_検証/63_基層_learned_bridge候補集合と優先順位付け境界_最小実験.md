# 検証記録：基層-learned bridge・bridge候補集合と優先順位付け境界

*対象：複数bridge候補が観測された後、prioritizationを与えたときordered bridge candidatesだけが生じる条件*  
*状態：DRAFT v0.1 / 60〜62 learned候補集合生成構造抽出後のbridge prioritization最小検証*  
*実装：`10_検証/base_to_learned_bridge_candidate_prioritization_boundary.py`*

---

## ■ 0. 検証目的

57〜59では、human-side response difference、learned category candidate set、`Γ_bridge`からbridge candidateが観測されることを確認した。

60〜62では、learned category candidate set自体も、sourceと`Γ_learned_candidate_generation`の関係として生成されることを確認した。

63では、複数のbridge candidatesが観測された後、`Γ_bridge_prioritization`を外部に与えたとき、prioritized bridge orderingだけが生じることを確認する。

```text
bridge candidates observed
  + Γ_bridge_prioritization_fixture
  ↓
prioritized bridge ordering
  ↓
selected musical interpretationは未生成
```

ここで確認するのは、bridge候補の存在と、候補の優先順位付けと、選択済み音楽解釈を分けることである。

---

## ■ 1. 固定するhuman-side response difference

57〜62と同じA2系のhuman-side response differenceを使う。

```text
human-side response difference:
  label = A2 behavioral discriminability difference
  source_base_candidate = frequency_difference_to_behavioral_discriminability_candidate
  response_axis = behavioral_discriminability
  lower_response = low_discriminability
  higher_response = high_discriminability
  generated_learned_category = None
```

これは弁別応答差であり、learned categoryでもbridge候補の優先順位でもない。

---

## ■ 2. 固定するlearned category candidate set

60〜62で扱ったpitch relation label候補集合を外部入力として使う。

```text
learned category candidate set:
  same_pitch_relation_label_candidate
  different_pitch_relation_label_candidate
  uncertain_pitch_relation_label_candidate
```

これらは、今回のbridge prioritization Γから生成されるものではない。

---

## ■ 3. bridge候補集合の観測

fixture用の`Γ_bridge_multi_candidate_fixture`を与え、二つのbridge候補を観測する。

```text
human-side response difference
+ learned category candidate set
+ Γ_bridge_multi_candidate_fixture
↓
bridge candidates observed:
  different_pitch_relation_label_candidate
  uncertain_pitch_relation_label_candidate
```

この段階では、候補は観測されただけである。

```text
bridge candidates observed
  ≠ prioritized bridge ordering
  ≠ selected musical interpretation
```

---

## ■ 4. 優先順位付け境界

二つの経路を比較する。

### 4.1 Γ_prioritizationなし

```text
bridge candidates observed
+ Γ_bridge_prioritization = None
↓
status = bridge_candidates_observed_not_prioritized
```

候補集合はあるが、順序はない。

### 4.2 Γ_prioritizationあり

```text
bridge candidates observed
+ Γ_bridge_prioritization_fixture
↓
prioritized bridge ordering:
  rank 1: different_pitch_relation_label_candidate
  rank 2: uncertain_pitch_relation_label_candidate
```

優先順位は生じるが、選択済み音楽解釈はまだ生成しない。

---

## ■ 5. 観測結果

| bridge candidates | Γ_prioritization | prioritized ordering | selected musical interpretation |
|---|---|---|---|
| different / uncertain | None | none | `None` |
| different / uncertain | label preference fixture | different → uncertain | `None` |

確認できたこと。

```text
same bridge candidates observed
different Γ_bridge_prioritization
↓
prioritized ordering appears / does not appear
```

さらに、

```text
priority_rank = 1
  ≠ selected musical interpretation
  ≠ confirmed learned category
```

である。

---

## ■ 6. Module責務の確認

今回の接続は、次のように分かれる。

```text
基層候補側:
  human-side response differenceを渡す

learned候補集合側:
  learned category candidate setを渡す

Γ_bridge:
  bridge候補集合を観測する

Γ_bridge_prioritization:
  観測済みbridge候補に順序を与える

selection controller:
  今回は未接続

category confirmation:
  今回は未接続
```

したがって、prioritizationはselectionではない。

---

## ■ 7. まだ言えないこと

今回の検証から、次は言えない。

```text
rank 1候補が正しいlearned categoryであること
rank 1候補がselected musical interpretationであること
Γ_bridge_prioritizationの由来や採用条件が決まったこと
bridge候補の優先順位が文化差・学習差を説明したこと
bridge候補から中核音楽理論Moduleへ接続できること
confirmed learned categoryの条件が決まったこと
```

また、今回の`Γ_bridge_prioritization`はfixture用であり、一般的なbridge selection ruleではない。

---

## ■ 8. 暫定結論

63では、複数のbridge候補が観測された後でも、`Γ_bridge_prioritization`なしでは優先順位が生じず、`Γ_bridge_prioritization`を与えた場合だけordered candidatesが生じることを確認した。

```text
bridge candidates observed
  + Γ_bridge_prioritization_fixture
  ↓
prioritized bridge ordering
```

ただし、prioritized bridge orderingはselectionではない。

```text
prioritized bridge ordering
  ≠ selected musical interpretation
  ≠ confirmed learned category
```

次に進むなら、同じprioritized bridge orderingに対してselection controllerを与えた場合だけ、selected bridge / selected musical interpretation候補が生じるかを見る。
