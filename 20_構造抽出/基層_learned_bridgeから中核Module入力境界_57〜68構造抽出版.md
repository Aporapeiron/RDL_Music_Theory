# 基層-learned bridgeから中核Module入力境界｜57〜68構造抽出版

*対象：57〜68で確認した、learned候補集合生成から中核Module入力候補採用までの分解系列*  
*状態：DRAFT v0.1 / 68 core module input adoption境界検証後の横断構造抽出*

## ■ 0. 位置づけ

本書は、57〜68の最小検証列から、基層側のhuman-side response differenceがlearned候補集合、bridge、selection、confirmation、musical interpretationを経て、中核音楽理論Module入力候補へ届くまでの境界を抽出する。

57〜64では、learned candidate generation、bridge candidate observation、bridge prioritization、bridge selectionを分けた。

65〜68では、その後段をさらに分けた。

```text
selected bridge candidate
→ category confirmation
→ musical interpretation
→ core module bridge
→ core module input adoption
```

ただし、これは自動因果列ではない。各段階には、source、candidate set、evidence、context、Γ、controllerが横から入る。

本書は、音楽学習モデル、文化差モデル、音程認識モデル、中核音楽理論Moduleの内部処理を追加しない。57〜68のfixture列から見えた責務境界だけを圧縮する。

## ■ 1. 抽出された接続地図

```text
human-side response difference ───────────────────────────────────────┐
  └─ A2 behavioral discriminability difference                         │
                                                                       │
learned candidate generation source ────────┐                         │
                                            ├→ learned candidate generation boundary
Γ_learned_candidate_generation ─────────────┘                         │
                                            ↓                         │
                         learned category candidate set observed       │
                                            │                         │
                                            ├─────────────────────────┘
                                            │
Γ_bridge ───────────────────────────────────┤
                                            ↓
                              bridge candidates observed
                                            │
Γ_bridge_prioritization ────────────────────┤
                                            ↓
                              prioritized bridge ordering
                                            │
Γ_bridge_selection_controller ──────────────┤
                                            ↓
                              selected bridge candidate
                                            │
external confirmation evidence ─────────────┤
Γ_category_confirmation ────────────────────┤
                                            ↓
                     confirmed learned category candidate
                                            │
external interpretation context ────────────┤
Γ_musical_interpretation ───────────────────┤
                                            ↓
                  selected musical interpretation candidate
                                            │
external core module candidate set ─────────┤
Γ_core_module_bridge ───────────────────────┤
                                            ↓
                           core module bridge candidate
                                            │
Γ_core_module_input_adoption ───────────────┤
                                            ↓
                         core module input candidate
                                            │
                                            │ Module内部処理は未開始
                                            │ B/Γ更新ではない
                                            │ Core昇格ではない
                                            ↓
                         中核Module内部境界へ保持
```

この地図は、human-side response differenceからlearned category、musical interpretation、中核Module入力が直に生えることを示さない。各段階は、別の候補・観測・採用状態として扱う。

## ■ 2. 検証ごとの担当

| 検証 | 担当する範囲 | 確認した境界 |
|---|---|---|
| 57 | response difference + external candidates + Γ_bridge | Γなしではunderdetermined、Γありでbridge候補を観測 |
| 58 | same response + same candidates + different Γ_bridge | Γ_bridge差し替えでbridge候補が分岐 |
| 59 | same response + same Γ_bridge + different candidates | candidate set差し替えでbridge候補が観測 / 消滅 |
| 60 | source + Γ_generation | Γなしでは候補集合未生成、Γありでlearned candidate setを観測 |
| 61 | same response + same Γ_generation + different source | source差し替えでcandidate setが分岐 |
| 62 | same response + same source + different Γ_generation | Γ_generation差し替えでcandidate setが分岐 |
| 63 | bridge candidates + Γ_prioritization | Γ_prioritizationありでprioritized bridge orderingを観測 |
| 64 | same prioritized ordering + different Γ_selection | controller差し替えでselected bridge candidateが分岐 |
| 65 | selected bridge + evidence + Γ_confirmation | Γ_confirmationありでconfirmed learned category candidateを観測 |
| 66 | confirmed category + context + Γ_interpretation | Γ_interpretationありでselected musical interpretation candidateを観測 |
| 67 | selected interpretation + core module candidates + Γ_bridge | Γ_core_module_bridgeありでcore module bridge candidateを観測 |
| 68 | core module bridge + Γ_input_adoption | Γ_input_adoptionありでcore module input candidateを観測 |

57〜68はいずれも、中核Module内部処理、Module側B/Γ更新、RDL Core昇格を生成しない。

## ■ 3. 保持する非同一性

57〜68から、次の非同一性を保持する。

```text
human-side response difference
  ≠ learned category

learned category candidate set
  ≠ bridge candidate

bridge candidates observed
  ≠ prioritized bridge ordering

prioritized bridge ordering
  ≠ selected bridge candidate

priority_rank = 1
  ≠ 必ずselected bridge candidate

selected bridge candidate
  ≠ confirmed learned category candidate

confirmed learned category candidate
  ≠ selected musical interpretation candidate

selected musical interpretation candidate
  ≠ core module bridge candidate

core module bridge candidate
  ≠ core module input candidate

core module input candidate
  ≠ 中核Module内部処理開始
  ≠ 中核ModuleのB/Γ更新
  ≠ Core昇格
```

さらに、各Γやcontrollerも一般規則へ昇格しない。

```text
Γ_generation
Γ_bridge
Γ_prioritization
Γ_selection
Γ_confirmation
Γ_interpretation
Γ_core_module_bridge
Γ_input_adoption

  = fixture内の限定規則
  ≠ 一般音楽理論
  ≠ 一般学習モデル
  ≠ Core規則
```

## ■ 4. 依存関係として見えた形

fixture内では、各段階は次の関係として読むのが堅い。

```text
learned category candidate set
  = C(learned candidate generation source; Γ_generation_fixture)

bridge candidates
  = C(human-side response difference, learned category candidate set; Γ_bridge_fixture)

prioritized bridge ordering
  = C(bridge candidates; Γ_bridge_prioritization_fixture)

selected bridge candidate
  = C(prioritized bridge ordering; Γ_bridge_selection_fixture)

confirmed learned category candidate
  = C(selected bridge candidate, confirmation evidence; Γ_confirmation_fixture)

selected musical interpretation candidate
  = C(confirmed learned category candidate, interpretation context; Γ_interpretation_fixture)

core module bridge candidate
  = C(selected musical interpretation candidate, core module candidate set; Γ_core_module_bridge_fixture)

core module input candidate
  = C(core module bridge candidate; Γ_core_module_input_adoption_fixture)
```

ただし、これは一般式ではない。57〜68のfixtureでは、A2 behavioral discriminability difference、learned pitch relation label候補、限定的な中核Module候補、限定的なΓ群を使った。

将来のΓやcontrollerが、history、文化差、学習履歴、記譜体系、ジャンル、中核音楽理論Module側の状態や文脈を読む可能性は残る。現段階ではそれらを解決済みにしない。

## ■ 5. 確定接続

**57〜59**：human-side response difference、learned category candidate set、Γ_bridgeを分け、bridge候補が三者関係として生じることを確認した。

**60〜62**：learned category candidate setはresponse differenceの属性ではなく、sourceとΓ_generationの関係として供給されることを確認した。

**63〜64**：bridge candidatesからprioritized ordering、さらにselected bridge candidateへ進むには、それぞれΓ_prioritizationとΓ_selectionが必要であることを確認した。

**65**：selected bridge candidateだけではlearned categoryとして確定せず、confirmation evidenceとΓ_confirmationが必要であることを確認した。

**66**：confirmed learned category candidateだけではmusical interpretationにならず、interpretation contextとΓ_interpretationが必要であることを確認した。

**67**：selected musical interpretation candidateだけでは中核Moduleへ接続されず、core module candidate setとΓ_core_module_bridgeが必要であることを確認した。

**68**：core module bridge candidateだけでは中核Module入力にならず、Γ_core_module_input_adoptionが必要であることを確認した。

いずれも、中核Module内部処理、Module側B/Γ更新、Core昇格は生成していない。

## ■ 6. 未解決ξ

57〜68の後に残る主なξは次である。

```text
ξ_generation_source_origin:
  learned candidate generation sourceの由来

ξ_generation_gamma_selection:
  どのΓ_generationを採用するか

ξ_candidate_scope:
  candidate setにどのcategory family / granularityを含めるか

ξ_bridge_gamma_selection:
  どのΓ_bridgeを採用するか

ξ_bridge_prioritization_gamma_selection:
  どのΓ_bridge_prioritizationを採用するか

ξ_bridge_selection_controller:
  どのselection controllerを採用するか

ξ_confirmation_evidence_origin:
  confirmation evidenceの由来

ξ_category_confirmation_condition:
  confirmed learned category candidateへ昇格できる条件

ξ_interpretation_context_origin:
  interpretation contextの由来

ξ_musical_interpretation_boundary:
  selected musical interpretation candidateを作る条件

ξ_core_music_module_candidate_generation:
  中核Module候補集合をどこから供給するか

ξ_core_module_bridge_gamma_selection:
  どのΓ_core_module_bridgeを採用するか

ξ_core_module_input_adoption_controller:
  bridge candidateをModule入力候補として採用するcontroller

ξ_core_module_processing_boundary:
  core module input candidateを中核Module内部処理へ渡す条件

ξ_core_promotion_condition:
  Module固有構造をRDL Coreへ昇格できる条件
```

これらは現段階でCoreへ上げない。文化差・学習差・記述体系差・中核Module内部検証で扱う。

## ■ 7. 禁止補完

```text
human-side response differenceからlearned categoryを自動生成しない
human-side response differenceからlearned candidate setを自動生成しない
sourceをresponse differenceの産物とみなさない
candidate setをbridge candidateと同一視しない
bridge candidateをprioritized orderingと同一視しない
priority_rank = 1をselection済みとみなさない
selected bridge candidateをconfirmed learned categoryとみなさない
confirmed learned categoryをmusical interpretationとみなさない
musical interpretation candidateをcore module bridge candidateとみなさない
core module bridge candidateをcore module input candidateとみなさない
core module input candidateをModule内部処理開始とみなさない
core module input candidateをB/Γ更新やCore昇格とみなさない
各source・evidence・context・candidate set・Γ・controllerをCoreへ昇格しない
```

## ■ 8. 現時点の読み方

57〜68の成果は、base-to-learned-to-core接続を完成させたことではない。

むしろ、基層側のhuman-side response differenceから中核音楽理論Module入力候補へ向かう接続が、少なくとも次の境界列へ分解されることを確認したことである。

```text
base response
  × learned source
  × Γ_generation
  ↓
learned candidate set

learned candidate set
  × base response
  × Γ_bridge
  ↓
bridge candidates

bridge candidates
  × Γ_prioritization
  ↓
prioritized bridge ordering

prioritized bridge ordering
  × Γ_selection
  ↓
selected bridge candidate

selected bridge candidate
  × confirmation evidence
  × Γ_confirmation
  ↓
confirmed learned category candidate

confirmed learned category candidate
  × interpretation context
  × Γ_interpretation
  ↓
selected musical interpretation candidate

selected musical interpretation candidate
  × core module candidate set
  × Γ_core_module_bridge
  ↓
core module bridge candidate

core module bridge candidate
  × Γ_input_adoption
  ↓
core module input candidate

──── ここで停止 ────

中核Module内部処理
中核Module B/Γ更新
Core昇格
```

ここで見えてきたのは、base-to-learned-to-core接続が単一写像ではなく、候補集合生成・bridge形成・優先順位付け・選択・確定・解釈・Module接続・入力採用の境界を持つことである。

```text
generation
  ≠ bridge observation
  ≠ prioritization
  ≠ selection
  ≠ confirmation
  ≠ interpretation
  ≠ core module bridge
  ≠ input adoption
  ≠ module processing
```

この分離が保てる限り、後で文化差、学習差、命名体系差、記譜体系差、ジャンル差、中核音楽理論Module側の文脈を追加しても、基層応答そのものへlearned categoryや中核Module処理を埋め込まずに済む。
