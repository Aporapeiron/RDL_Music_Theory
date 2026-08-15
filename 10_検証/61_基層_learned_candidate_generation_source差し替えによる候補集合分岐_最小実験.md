# 検証記録：基層-learned bridge・learned candidate generation source差し替えによる候補集合分岐

*対象：同じhuman-side response differenceと同じΓ_learned_candidate_generationで、learned candidate generation sourceだけを差し替えたときcandidate setが分岐する条件*  
*状態：DRAFT v0.1 / 60 learned候補集合生成境界後のsource差し替え最小検証*  
*実装：`10_検証/learned_candidate_source_variation.py`*

---

## ■ 0. 検証目的

60では、57〜59で外部入力として扱っていたlearned category candidatesを、learned candidate generation sourceと`Γ_learned_candidate_generation`から候補集合として観測した。

61では、human-side response differenceと`Γ_learned_candidate_generation`を固定し、learned candidate generation sourceだけを差し替える。

```text
same human-side response difference
  + same Γ_learned_candidate_generation_fixture
  + different learned candidate generation sources
  ↓
different learned category candidate sets
```

ここで確認するのは、learned category candidate setがhuman-side response differenceの属性でも、Γ単体の属性でもなく、sourceとΓの関係として分岐することである。

---

## ■ 1. 固定するhuman-side response difference

60と同じA2系のhuman-side response differenceを使う。

```text
human-side response difference:
  label = A2 behavioral discriminability difference
  source_base_candidate = frequency_difference_to_behavioral_discriminability_candidate
  response_axis = behavioral_discriminability
  lower_response = low_discriminability
  higher_response = high_discriminability
  generated_learned_category = None
```

これは弁別応答差であり、learned category候補集合の生成器ではない。

---

## ■ 2. 固定するΓ_learned_candidate_generation

60と同じfixture Γを固定する。

```text
Γ_learned_candidate_generation_fixture:
  learned candidate generation source
  と
  inventory_profile
  から候補集合を観測する
```

このΓは一般的な音楽学習モデルでも、category generation ruleの完成でもない。

---

## ■ 3. 差し替えるsource

二つのlearned candidate generation sourceを用意する。

```text
source A:
  label = learned_pitch_relation_label_inventory_fixture
  category_family = learned_pitch_relation_label
  inventory_profile = same_different_uncertain_profile
  generated_by_response_difference = False
```

```text
source B:
  label = learned_pitch_binary_label_inventory_fixture
  category_family = learned_pitch_relation_label
  inventory_profile = same_different_only_profile
  generated_by_response_difference = False
```

どちらもfixture用のlearned inventoryであり、human-side response differenceから生成されたものではない。

---

## ■ 4. 最小ケースの比較

### 4.1 source A

```text
same response difference
+ same Γ_generation
+ source A
↓
learned candidate set:
  same_pitch_relation_label_candidate
  different_pitch_relation_label_candidate
  uncertain_pitch_relation_label_candidate
```

### 4.2 source B

```text
same response difference
+ same Γ_generation
+ source B
↓
learned candidate set:
  same_pitch_relation_label_candidate
  different_pitch_relation_label_candidate
```

両方とも、bridge candidate、generated learned category、selected musical interpretationは生成しない。

---

## ■ 5. 観測結果

| human-side response difference | Γ_generation | source | observed learned candidates | bridge candidate |
|---|---|---|---|---|
| same | same | source A | same / different / uncertain | `None` |
| same | same | source B | same / different | `None` |

確認できたこと。

```text
same human-side response difference
same Γ_learned_candidate_generation
different learned candidate generation source
↓
different learned category candidate sets
```

したがって、候補集合はhuman-side response differenceとΓだけでは決まらない。

```text
learned category candidates observed
  ≠ human-side response difference の属性
  ≠ Γ_generation 単体の属性
  ≠ bridge candidate
  ≠ selected musical interpretation
```

---

## ■ 6. Module責務の確認

今回の接続は、次のように分かれる。

```text
基層候補側:
  同じhuman-side response differenceを渡す

Γ_learned_candidate_generation:
  同じcandidate generation Γを渡す

learned側:
  learned candidate generation sourceを差し替える

learned candidate set:
  source差によって分岐する

bridge Γ:
  今回は未接続

bridge候補:
  今回は未生成
```

したがって、learned候補集合の構成はlearned側sourceの粒度・語彙にも依存する。

---

## ■ 7. まだ言えないこと

今回の検証から、次は言えない。

```text
どちらのcandidate setが正しいlearned category集合であること
sourceの由来や採用条件が決まったこと
candidate setからbridge候補が自動生成されること
candidate setからselected musical interpretationが生成されること
culture / training / notation systemの差が説明されたこと
周波数弁別からpitch categoryが生成されたこと
```

また、今回のsourceと`Γ_generation`はfixture用であり、一般的なlearned candidate generation modelではない。

---

## ■ 8. 暫定結論

61では、同じhuman-side response differenceと同じ`Γ_learned_candidate_generation`でも、learned candidate generation sourceを差し替えるとcandidate setが分岐することを確認した。

```text
learned category candidate set
  = C(learned candidate generation source; Γ_learned_candidate_generation_fixture)
```

ただし、これはfixture内の限定表現である。human-side response differenceは保持されているが、今回のfixture Γは候補集合生成にresponse differenceを読まない。

したがって、候補集合生成はbridge候補生成とは別境界である。

```text
learned category candidate set
  ≠ bridge candidate
  ≠ generated learned category
  ≠ selected musical interpretation
```

次に進むなら、same source、same response differenceで、Γ_learned_candidate_generationを差し替えるとcandidate setが分岐するかを見る。
