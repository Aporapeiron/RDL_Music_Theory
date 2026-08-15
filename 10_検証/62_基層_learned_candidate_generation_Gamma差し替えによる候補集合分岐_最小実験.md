# 検証記録：基層-learned bridge・Γ_learned_candidate_generation差し替えによる候補集合分岐

*対象：同じhuman-side response differenceと同じlearned candidate generation sourceで、Γ_learned_candidate_generationだけを差し替えたときcandidate setが分岐する条件*  
*状態：DRAFT v0.1 / 61 source差し替え検証後のΓ_generation差し替え最小検証*  
*実装：`10_検証/learned_candidate_generation_gamma_variation.py`*

---

## ■ 0. 検証目的

61では、同じhuman-side response differenceと同じ`Γ_learned_candidate_generation`でも、learned candidate generation sourceを差し替えるとcandidate setが分岐することを確認した。

62では、human-side response differenceとlearned candidate generation sourceを固定し、`Γ_learned_candidate_generation`だけを差し替える。

```text
same human-side response difference
  + same learned candidate generation source
  + different Γ_learned_candidate_generation_fixture
  ↓
different learned category candidate sets
```

ここで確認するのは、learned category candidate setがhuman-side response differenceの属性でも、source単独の属性でもなく、sourceとΓの関係として分岐することである。

---

## ■ 1. 固定するhuman-side response difference

60〜61と同じA2系のhuman-side response differenceを使う。

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

## ■ 2. 固定するlearned candidate generation source

61のsource Aを固定する。

```text
source:
  label = learned_pitch_relation_label_inventory_fixture
  category_family = learned_pitch_relation_label
  inventory_profile = same_different_uncertain_profile
  generated_by_response_difference = False
```

これはfixture用のlearned inventoryであり、human-side response differenceから生成されたものではない。

---

## ■ 3. 差し替えるΓ_learned_candidate_generation

二つのfixture用Γを用意する。

```text
Γ_full_inventory:
  sourceのfull inventory profileを読む
```

```text
Γ_binary_only:
  sourceのinventoryからbinary labelだけを読む
```

どちらも一般的なlearned category generation ruleではない。

---

## ■ 4. 最小ケースの比較

### 4.1 Γ_full_inventory

```text
same response difference
+ same source
+ Γ_full_inventory
↓
learned candidate set:
  same_pitch_relation_label_candidate
  different_pitch_relation_label_candidate
  uncertain_pitch_relation_label_candidate
```

### 4.2 Γ_binary_only

```text
same response difference
+ same source
+ Γ_binary_only
↓
learned candidate set:
  same_pitch_relation_label_candidate
  different_pitch_relation_label_candidate
```

両方とも、bridge candidate、generated learned category、selected musical interpretationは生成しない。

---

## ■ 5. 観測結果

| human-side response difference | source | Γ_generation | observed learned candidates | bridge candidate |
|---|---|---|---|---|
| same | same | full inventory | same / different / uncertain | `None` |
| same | same | binary only | same / different | `None` |

確認できたこと。

```text
same human-side response difference
same learned candidate generation source
different Γ_learned_candidate_generation
↓
different learned category candidate sets
```

したがって、候補集合はhuman-side response differenceとsourceだけでは決まらない。

```text
learned category candidates observed
  ≠ human-side response difference の属性
  ≠ source単体の属性
  ≠ bridge candidate
  ≠ selected musical interpretation
```

---

## ■ 6. Module責務の確認

今回の接続は、次のように分かれる。

```text
基層候補側:
  同じhuman-side response differenceを渡す

learned側:
  同じlearned candidate generation sourceを渡す

Γ_learned_candidate_generation:
  candidate generation Γを差し替える

learned candidate set:
  Γ差によって分岐する

bridge Γ:
  今回は未接続

bridge候補:
  今回は未生成
```

したがって、learned候補集合の構成はsourceだけでなく、どのΓ_generationがsourceを読むかにも依存する。

---

## ■ 7. まだ言えないこと

今回の検証から、次は言えない。

```text
どちらのcandidate setが正しいlearned category集合であること
Γ_generationの由来や採用条件が決まったこと
candidate setからbridge候補が自動生成されること
candidate setからselected musical interpretationが生成されること
culture / training / notation systemの差が説明されたこと
周波数弁別からpitch categoryが生成されたこと
```

また、今回のsourceと二つの`Γ_generation`はfixture用であり、一般的なlearned candidate generation modelではない。

---

## ■ 8. 暫定結論

62では、同じhuman-side response differenceと同じlearned candidate generation sourceでも、`Γ_learned_candidate_generation`を差し替えるとcandidate setが分岐することを確認した。

```text
learned category candidate set
  = C(learned candidate generation source; Γ_learned_candidate_generation_fixture)
```

ただし、これはfixture内の限定表現である。human-side response differenceは保持されているが、今回のfixture Γは候補集合生成にresponse differenceを読まない。

60〜62をまとめると、learned category candidatesは少なくとも次の境界として扱う必要がある。

```text
learned candidate generation source
× Γ_learned_candidate_generation
→ learned category candidate set
```

そして、このcandidate setはbridge候補でも、learned category確定でも、音楽解釈選択でもない。

次に進むなら、60〜62を一度構造抽出し、`ξ_learned_candidate_generation` の現在地を圧縮する。
