# 基層-learned candidate generation｜60〜62構造抽出版

*対象：60〜62で確認した、learned category candidate set の生成・供給境界*  
*状態：DRAFT v0.1 / 57〜59 bridge構造抽出後のlearned候補集合生成構造抽出*

## ■ 0. 位置づけ

本書は、57〜59で未解決ξとして残した `ξ_learned_candidate_generation` を、60〜62の最小検証列から抽出する。

57〜59では、learned category candidatesを外部入力として置き、human-side response differenceからlearned categoryを直接生成しなかった。

60〜62では、その外部候補集合がどのような境界で供給されるかを、次の関係として局所的に検査した。

```text
learned candidate generation source
  + Γ_learned_candidate_generation_fixture
  ↓
learned category candidate set observed
  ↓
bridge candidateは未生成
```

本書は、音楽学習モデル、文化差モデル、一般的なcategory generation ruleを追加しない。60〜62のfixture列から見えた責務境界だけを圧縮する。

## ■ 1. 抽出された接続地図

```text
human-side response difference ───────────────┐
  └─ behavioral discriminability difference   │
                                               │ 生成器ではない
                                               │
learned candidate generation source ──────────┐
  ├─ inventory fixture                         ├→ candidate generation boundary
  ├─ category family                           │
  └─ inventory profile                         │
                                               │
Γ_learned_candidate_generation ────────────────┘
  ├─ full inventory fixture
  └─ binary only fixture
                                               ↓
learned category candidate set observed
  ├─ same_pitch_relation_label_candidate
  ├─ different_pitch_relation_label_candidate
  └─ uncertain_pitch_relation_label_candidate
                                               │
                                               │ bridge候補を生成しない
                                               │ confirmed learned categoryへ昇格しない
                                               │ selected musical interpretationを生成しない
                                               ↓
bridge / selection / confirmation境界へ保持
```

この地図は、human-side response differenceからlearned candidate setが生えることを示さない。今回のfixtureでは、response differenceは保持されるが、候補集合を生成する直接入力としては使っていない。

## ■ 2. 検証ごとの担当

| 検証 | 担当する範囲 | 確認した境界 |
|---|---|---|
| 60 | source + Γ_generation | Γなしでは候補集合未生成、Γありでlearned candidate setを観測 |
| 61 | same response difference + same Γ_generation + different source | source差し替えで候補集合が分岐 |
| 62 | same response difference + same source + different Γ_generation | Γ_generation差し替えで候補集合が分岐 |

60〜62はいずれも、bridge candidate、confirmed learned category、selected musical interpretationを生成しない。

## ■ 3. 保持する非同一性

60〜62から、次の非同一性を保持する。

```text
human-side response difference
  ≠ learned candidate generation source

human-side response difference
  ≠ learned category candidate set

learned candidate generation source
  ≠ learned category candidate set

Γ_generation fixture
  ≠ 一般learned category generation rule

learned category candidate set
  ≠ bridge candidate
  ≠ confirmed learned category
  ≠ selected musical interpretation

candidate set observed
  ≠ category selection
```

特に重要なのは、learned category candidate setがresponse側の属性でも、source単体の属性でも、Γ単体の属性でもないことである。

## ■ 4. 依存関係として見えた形

fixture内では、learned category candidate setは次の関係として読むのが堅い。

```text
learned category candidate set
  = C(learned candidate generation source; Γ_learned_candidate_generation_fixture)
```

ただし、これは一般式ではない。60〜62のfixtureでは、human-side response differenceを保持したまま、候補集合生成そのものはsourceとΓ_generationの組に限定した。

将来のΓ_generationが、response difference、history、文化差、学習履歴、記譜体系、ジャンルを読む可能性は残る。現段階ではそれらを生成条件として確定しない。

また、候補集合生成とbridge形成は別境界である。

```text
learned category candidate set
  ≠ bridge candidate

bridge candidate
  = later C(human-side response difference, learned category candidate set; Γ_bridge)
```

## ■ 5. 確定接続

**60**：learned candidate generation sourceと `Γ_learned_candidate_generation_fixture` を与えた場合だけ、`same_pitch_relation_label_candidate`、`different_pitch_relation_label_candidate`、`uncertain_pitch_relation_label_candidate` の候補集合が観測される。Γなしでは `no_learned_candidate_generation_gamma` となる。

**61**：同じhuman-side response differenceと同じΓ_generationでも、sourceを差し替えると、三候補の集合と二候補の集合へ分岐する。

**62**：同じhuman-side response differenceと同じsourceでも、Γ_generationを `full_inventory` と `binary_only` へ差し替えると、三候補の集合と二候補の集合へ分岐する。

いずれも、bridge candidate、confirmed learned category、selected musical interpretationは生成していない。

## ■ 6. 未解決ξ

60〜62の後に残る主なξは次である。

```text
ξ_generation_source_origin:
  learned candidate generation sourceの由来

ξ_generation_source_selection:
  どのsourceを採用するか

ξ_generation_gamma_selection:
  どのΓ_generationを採用するか

ξ_generation_gamma_origin:
  Γ_generationの由来、文化差、学習差、記述体系差

ξ_candidate_scope:
  候補集合にどのcategory family / granularityを含めるか

ξ_candidate_set_validation:
  観測された候補集合をどう検査するか

ξ_candidate_set_to_bridge:
  candidate setをbridge境界へどう渡すか

ξ_bridge_candidate_prioritization:
  bridge候補が複数ある場合にどう順序付けるか
```

これらは現段階でCoreへ上げない。候補集合の由来、採用条件、文化差・学習差、bridge側のprioritization / selectionで扱う。

## ■ 7. 禁止補完

```text
human-side response differenceからlearned candidate setを自動生成しない
sourceをresponse differenceの産物とみなさない
Γ_generationを一般learned category generation ruleとみなさない
candidate setをbridge candidateと同一視しない
candidate setをconfirmed learned categoryと同一視しない
candidate setをselected musical interpretationと同一視しない
候補集合にないlearned categoryをbridge側で生成しない
文化差・学習差・記譜体系差をfixture sourceで説明済みとみなさない
source / Γ_generation / candidate setをCoreへ昇格しない
```

## ■ 8. 現時点の読み方

60〜62の成果は、learned category candidate setの生成を完成させたことではない。

むしろ、57〜59で外部入力として置いたlearned候補集合が、少なくともsourceとΓ_generationの関係として分解されることを確認したことである。

```text
learned source
  × Γ_generation
  ↓
candidate set

candidate set
  × response difference
  × Γ_bridge
  ↓
bridge candidate

──── ここで停止 ────

bridge prioritization
bridge selection
confirmed learned category
selected musical interpretation
中核音楽理論Moduleへの接続
```

ここまでで、base-to-learned bridgeの手前に、learned側候補集合を供給する別境界が現れた。

```text
human-side response difference
  ≠ learned candidate generation
  ≠ bridge generation
  ≠ category confirmation
  ≠ musical interpretation selection
```

この分離が保てる限り、後で文化差、学習差、命名体系差、記譜体系差、音楽理論Module側の候補空間を追加しても、基層応答そのものへlearned category生成を埋め込まずに済む。
