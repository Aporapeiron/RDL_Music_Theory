# 基層-learned bridgeからselection境界｜57〜64構造抽出版

*対象：57〜64で確認した、learned候補集合生成からbridge selectionまでの分解系列*  
*状態：DRAFT v0.1 / 64 bridge selection controller境界検証後の横断構造抽出*

## ■ 0. 位置づけ

本書は、57〜64の最小検証列から、`ξ_base_to_learned_bridge`、`ξ_learned_candidate_generation`、`ξ_bridge_candidate_prioritization`、`ξ_bridge_selection_controller` の現在地を横断的に抽出する。

54〜56では、human-side response differenceをlearned musical categoryへ接続しなかった。

57〜64では、その接続を直結せず、次の段階へ分けた。

```text
learned candidate generation
→ bridge candidate observation
→ bridge prioritization
→ bridge selection
```

ただし、これは自動因果列ではない。各段階には、source、candidate set、Γ、controllerが横から入る。

本書は、音楽学習モデル、文化差モデル、音程認識モデル、音楽解釈選択モデルを追加しない。57〜64のfixture列から見えた責務境界だけを圧縮する。

## ■ 1. 抽出された接続地図

```text
human-side response difference ───────────────────────────────┐
  └─ A2 behavioral discriminability difference                 │
                                                               │
learned candidate generation source ────────┐                 │
                                            ├→ learned candidate generation boundary
Γ_learned_candidate_generation ─────────────┘                 │
                                            ↓                 │
                         learned category candidate set observed
                                            │                 │
                                            ├─────────────────┘
                                            │
Γ_bridge ───────────────────────────────────┤
                                            ↓
                              bridge candidates observed
                                            │
                                            │ selectionではない
                                            │
Γ_bridge_prioritization ────────────────────┤
                                            ↓
                              prioritized bridge ordering
                                            │
                                            │ rank 1 = selectedではない
                                            │
Γ_bridge_selection_controller ──────────────┤
                                            ↓
                              selected bridge candidate
                                            │
                                            │ confirmed learned categoryではない
                                            │ selected musical interpretationではない
                                            ↓
                         confirmation / interpretation境界へ保持
```

この地図は、human-side response differenceからlearned categoryが直に生えることを示さない。また、candidate set、bridge candidates、prioritized ordering、selected bridge candidateは、それぞれ別状態として扱う。

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

57〜64はいずれも、confirmed learned category、selected musical interpretation、中核音楽理論Moduleへの接続を生成しない。

## ■ 3. 保持する非同一性

57〜64から、次の非同一性を保持する。

```text
human-side response difference
  ≠ learned category

human-side response difference
  ≠ learned candidate generation source
  ≠ learned category candidate set

learned candidate generation source
  ≠ learned category candidate set

learned category candidate set
  ≠ bridge candidate

bridge candidates observed
  ≠ prioritized bridge ordering

prioritized bridge ordering
  ≠ selected bridge candidate

priority_rank = 1
  ≠ 必ずselected bridge candidate

selected bridge candidate
  ≠ confirmed learned category
  ≠ selected musical interpretation
```

さらに、各Γやcontrollerも一般規則へ昇格しない。

```text
Γ_learned_candidate_generation fixture
  ≠ 一般learned category generation rule

Γ_bridge fixture
  ≠ 一般base-to-learned mapping

Γ_bridge_prioritization fixture
  ≠ selection controller

Γ_bridge_selection fixture
  ≠ category confirmation rule
  ≠ musical interpretation rule
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
```

ただし、これは一般式ではない。57〜64のfixtureでは、A2 behavioral discriminability difference、learned pitch relation label候補、限定的なΓ群、限定的なselection controllerを使った。

将来のΓやcontrollerが、history、文化差、学習履歴、記譜体系、ジャンル、中核音楽理論Module側の文脈を読む可能性は残る。現段階ではそれらを解決済みにしない。

## ■ 5. 確定接続

**57〜59**：human-side response difference、learned category candidate set、Γ_bridgeを分け、bridge候補が三者関係として生じることを確認した。候補集合やΓを差し替えるとbridge候補は分岐または消滅する。

**60〜62**：learned category candidate setはresponse differenceの属性ではなく、sourceとΓ_generationの関係として供給されることを確認した。sourceまたはΓ_generationを差し替えるとcandidate setは分岐する。

**63**：複数bridge候補が観測された後でも、Γ_bridge_prioritizationなしではprioritized orderingは生じない。Γ_bridge_prioritizationを与えた場合だけordered candidatesが生じる。

**64**：同じprioritized bridge orderingでも、selection controllerがなければselected bridge candidateは生じない。controllerを差し替えるとselected bridge candidateは分岐する。

いずれも、confirmed learned category、selected musical interpretation、中核音楽理論Moduleへの接続は生成していない。

## ■ 6. 未解決ξ

57〜64の後に残る主なξは次である。

```text
ξ_generation_source_origin:
  learned candidate generation sourceの由来

ξ_generation_source_selection:
  どのsourceを採用するか

ξ_generation_gamma_selection:
  どのΓ_generationを採用するか

ξ_candidate_scope:
  candidate setにどのcategory family / granularityを含めるか

ξ_bridge_gamma_selection:
  どのΓ_bridgeを採用するか

ξ_bridge_applicability_condition:
  response differenceやcandidate setのどの特徴をbridge条件として読むか

ξ_bridge_prioritization_gamma_selection:
  どのΓ_bridge_prioritizationを採用するか

ξ_bridge_selection_controller:
  どのselection controllerを採用するか

ξ_category_confirmation_condition:
  selected bridge candidateをconfirmed learned categoryへ昇格できる条件

ξ_musical_interpretation_boundary:
  selected bridge candidateをselected musical interpretationへ接続する条件

ξ_core_music_module_bridge:
  中核音楽理論Module側のcandidate / contextとどう接続するか
```

これらは現段階でCoreへ上げない。文化差・学習差・記述体系差・音楽理論Module接続で扱う。

## ■ 7. 禁止補完

```text
human-side response differenceからlearned categoryを自動生成しない
human-side response differenceからlearned candidate setを自動生成しない
sourceをresponse differenceの産物とみなさない
candidate setをbridge candidateと同一視しない
bridge candidateをprioritized orderingと同一視しない
priority_rank = 1をselection済みとみなさない
selected bridge candidateをconfirmed learned categoryとみなさない
selected bridge candidateをselected musical interpretationとみなさない
Γ_generation / Γ_bridge / Γ_prioritization / Γ_selectionを一般規則とみなさない
候補集合にないlearned categoryをbridge側で生成しない
周波数弁別からpitch categoryやsemitone categoryを直接生成しない
音程認識・音名・調性をbridge selectionから自動生成しない
各source・Γ・controller・candidate setをCoreへ昇格しない
```

## ■ 8. 現時点の読み方

57〜64の成果は、base-to-learned bridgeを完成させたことではない。

むしろ、基層側のhuman-side response differenceからlearned音楽カテゴリーへ向かう接続が、少なくとも次の境界列へ分解されることを確認したことである。

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

──── ここで停止 ────

confirmed learned category
selected musical interpretation
中核音楽理論Moduleへの接続
```

ここで見えてきたのは、base-to-learned接続が単一写像ではなく、候補集合生成・bridge形成・優先順位付け・選択・確定・解釈の境界を持つことである。

```text
generation
  ≠ bridge observation
  ≠ prioritization
  ≠ selection
  ≠ confirmation
  ≠ interpretation
```

この分離が保てる限り、後で文化差、学習差、命名体系差、記譜体系差、ジャンル差、中核音楽理論Module側の文脈を追加しても、基層応答そのものへlearned categoryや音楽解釈を埋め込まずに済む。
