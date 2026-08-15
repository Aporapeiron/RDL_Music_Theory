# 検証記録：基層-learned bridge・learned category候補集合生成境界

*対象：57〜59で外部入力だったlearned category candidatesを、human-side response differenceから直生成せずに候補集合として観測する最小条件*  
*状態：DRAFT v0.1 / 57〜59 bridge構造抽出後のlearned候補集合生成境界検証*  
*実装：`10_検証/learned_candidate_generation_boundary.py`*

---

## ■ 0. 検証目的

`20_構造抽出/基層_learned_bridge_57〜59構造抽出版.md` では、57〜59の後に残る未解決ξとして次を置いた。

```text
ξ_learned_candidate_generation:
  external learned category candidatesをどこから生成・供給するか

ξ_learned_candidate_scope:
  候補集合にどのcategory familyを含めるか
```

60では、bridge候補を生成しない。

57〜59で外部入力として扱っていたlearned category candidatesについて、learned側の候補生成sourceとfixture用の`Γ_learned_candidate_generation`を分け、候補集合が観測されることだけを確認する。

```text
human-side response difference
  + learned candidate generation source
  + Γ_learned_candidate_generation_fixture
  ↓
learned category candidates observed
  ↓
bridge candidateは未生成
```

---

## ■ 1. 固定するhuman-side response difference

57〜59と同じA2系のhuman-side response differenceを使う。

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

learned側の候補供給源を次に固定する。

```text
learned candidate generation source:
  label = learned_pitch_relation_label_inventory_fixture
  source_kind = external_learned_inventory_fixture
  category_family = learned_pitch_relation_label
  generated_by_response_difference = False
```

これはfixture用のlearned inventoryであり、人間側応答差から生成されたものではない。

---

## ■ 3. 固定するΓ_learned_candidate_generation

```text
Γ_learned_candidate_generation_fixture:
  learned candidate generation source
  と
  category_family
  から候補集合を観測する
```

このΓは、一般的な音楽学習モデルでも、category generation ruleの完成でもない。human-side response differenceから直接categoryを生成する規則でもない。

---

## ■ 4. 最小ケース

### 4.1 Γなし

```text
human-side response difference
+ learned candidate generation source
+ Γなし
↓
no_learned_candidate_generation_gamma
```

sourceがあっても、候補集合生成Γがなければ候補集合は観測しない。

### 4.2 Γあり

```text
human-side response difference
+ learned candidate generation source
+ Γ_learned_candidate_generation_fixture
↓
learned category candidates observed
```

ただし、ここで得られるのはlearned category候補集合であり、bridge候補でも、learned category確定でも、選択済み音楽解釈でもない。

---

## ■ 5. 観測結果

| human-side response difference | source | Γ_generation | status | bridge candidate |
|---|---|---|---|---|
| same | learned inventory fixture | none | `no_learned_candidate_generation_gamma` | `None` |
| same | learned inventory fixture | fixture | `learned_candidate_set_observed_not_bridged` | `None` |

観測された候補集合。

```text
same_pitch_relation_label_candidate
different_pitch_relation_label_candidate
uncertain_pitch_relation_label_candidate
```

確認できたこと。

```text
human-side response difference
+ learned candidate generation source
+ Γ_learned_candidate_generation_fixture
↓
learned category candidates observed
↓
bridge candidate remains None
```

したがって、候補集合が観測されてもbridgeは成立していない。

```text
learned category candidates observed
  ≠ bridge candidate observed
  ≠ generated learned category
  ≠ selected musical interpretation
```

---

## ■ 6. Module責務の確認

今回の接続は、次のように分かれる。

```text
基層候補側:
  human-side response differenceを渡す

learned側:
  learned candidate generation sourceを渡す

Γ_learned_candidate_generation:
  sourceとcategory_familyから候補集合を観測する

bridge Γ:
  今回は未接続

bridge候補:
  今回は未生成

中核音楽理論:
  今回は未接続
```

したがって、learned候補集合の観測はbridge成立や音楽解釈選択を自動的に含まない。

---

## ■ 7. まだ言えないこと

今回の検証から、次は言えない。

```text
learned category candidatesがhuman-side response differenceから生成されたこと
候補集合が正しいlearned category集合であること
候補集合からbridge候補が自動生成されること
候補集合からselected musical interpretationが生成されること
learned inventoryの由来が決まったこと
文化差・学習差・命名体系差が説明されたこと
周波数弁別からpitch categoryが生成されたこと
```

また、今回のsourceと`Γ_learned_candidate_generation`はfixture用であり、一般的なlearned category生成モデルではない。

---

## ■ 8. 暫定結論

60では、57〜59で外部入力として扱っていたlearned category candidatesを、次の最小形で候補集合として観測した。

```text
learned candidate generation source
  + Γ_learned_candidate_generation_fixture
  → learned category candidates observed
```

ただし、この候補集合はhuman-side response differenceから直生成されたものではなく、bridge候補でも、learned category確定でも、音楽解釈選択でもない。

```text
human-side response difference
  ≠ learned candidate generation source
  ≠ learned category candidates observed
  ≠ bridge candidate
  ≠ selected musical interpretation
```

次に進むなら、同じhuman-side response differenceと同じΓ_generationで、learned candidate generation sourceを差し替えるとcandidate setが分岐するかを見る。
