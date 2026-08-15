# 和声機能｜target候補生成からselection境界 46〜53構造抽出版

*対象：46〜53で確認した target candidate generation / prioritization / selection の分解構造*  
*状態：DRAFT v0.2 / 42〜45循環分解後の局所構造抽出更新*

## ■ 0. 位置づけ

本書は、46〜53の最小検証列から、function annotation candidateの後段にあるtarget候補生成、履歴表現、優先順位付け、selection境界を抽出する。

42〜45では、function annotationからtarget候補集合を生成しなかった。

46〜53では、fixture用の限定Γを置いた場合でも、次を同一視しないことを確認した。

```text
function observation
history / B_history representation
Γ_target_candidate_generation
applicability check
generated target candidate set
Γ_prioritization
prioritized candidate ordering
Γ_selection
selected target
target degree plan
```

本書は一般和声規則を追加しない。fixture列から見えた責務境界だけを圧縮する。

## ■ 1. 抽出された接続地図

```text
function observation ───────────────┐
  ├─ function annotation label       │
  └─ key context                     │
                                     ├→ applicability check
underlying history ──→ B_history ───┤
                       representation│
Γ_target_candidate_generation ───────┘
                                     ↓
                          generated target candidate set
                                     │
                                     │ selected targetを生成しない
                                     ↓
Γ_target_candidate_prioritization ─→ prioritized candidate ordering
                                     │
                                     │ rank 1をselected targetへ自動昇格しない
                                     ↓
Γ_selection / controller ──────────→ selected target
                                     │
                                     │ target degree planを生成しない
                                     ↓
                          planning / realization boundaryへ渡す
```

この地図は、function annotation labelからtarget候補集合が直に生えることも、candidate setの生成からselected targetが直に生じることも示さない。各段階には、外部から与えられるB・Γ・controller・fixture入力が挟まる。

## ■ 2. 検証ごとの担当

| 検証 | 担当する範囲 | 確認した境界 |
|---|---|---|
| 46 | annotation / generation rule / generated set | function annotation単独では候補生成しない |
| 47 | same annotation + same context + different Γ_generation | 生成規則差し替えで候補集合が変わる |
| 48 | same annotation label + different context + same Γ_generation | context差し替えで候補集合が変わる |
| 49 | same current observation + same Γ_generation + different history | history.local_pattern差で候補集合が変わる |
| 50 | same broad history + different local_pattern | 大分類だけでは候補集合の差を保存できない |
| 51 | same underlying history + different B_history | history representation粒度で候補集合が変わる |
| 52 | same generated candidate set + different Γ_prioritization | 候補順序が分岐し、selected targetは未生成 |
| 53 | same prioritized ordering + different Γ_selection | selected targetが分岐し、target degree planは未生成 |

## ■ 3. 保持する非同一性

46〜53から、次の非同一性を保持する。

```text
function annotation
  ≠ target candidate generation rule

current function observation
  ≠ generated target candidate set

underlying history
  ≠ history representation under B_history
  ≠ Γが参照できるhistory features

generation ruleの存在
  ≠ 現在のfunction observationへの適用可能性

rule applicability result
  ≠ generated target candidate set

generated target candidate set
  ≠ prioritized candidate ordering

prioritized candidate ordering
  ≠ selected target

priority_rank = 1
  ≠ 必ずselected target

selected target
  ≠ target degree plan
```

特に49〜51で、historyはcurrent function observationとは別入力であり、さらにunderlying historyとB_historyによるrepresentationを同一視しない必要が見えた。52〜53では、candidate setが得られても、それはprioritizationでもselectionでもないことを確認した。

## ■ 4. 依存関係として見えた形

fixture内では、target候補生成は次の関係として読むのが堅い。

```text
generated target candidate set
  = C(function observation, history representation; Γ_target_candidate_generation)
```

ただし、これは一般式ではない。46〜48のfixture用Γはfunction observationのうちfunction annotation labelとkey contextを参照した。49〜51ではhistory.local_patternやB_history representationが読まれた。

52以降では、生成済み候補集合の後段がさらに分かれた。

```text
prioritized candidate ordering
  = P(generated target candidate set; Γ_prioritization)

selected target
  = S(prioritized candidate ordering; Γ_selection)
```

ここでも、PやSはfixture内の限定写像である。prioritization policyやselection controllerの由来は未解決ξとして残る。

## ■ 5. 確定接続

**46**：`dominant_candidate + C major + Γ_target_candidate_generation_fixture` から `{C major, A minor}` を生成できる。ただし、規則なしでは `no_generation_rule`、適用外では `rule_not_applicable` となる。

**47**：同じ `dominant_candidate + C major` でも、生成規則を変えると `{C major, A minor}` と `{C major}` へ分岐する。

**48**：同じ `dominant_candidate` labelと同じ文脈依存fixture規則でも、contextを `C major` から `G major` へ変えると `{C major, A minor}` と `{G major, E minor}` へ分岐する。

**49**：同じcurrent function observationと同じhistory-sensitive fixture規則でも、`history.local_pattern` を `ordinary_preparation` から `deceptive_setup` へ変えると `{C major}` と `{C major, A minor}` へ分岐する。

**50**：同じ `history.broad_pattern = dominant_preparation` でも、`local_pattern` が `ordinary_preparation` か `deceptive_setup` かで `{C major}` と `{C major, A minor}` へ分岐する。

**51**：同じunderlying historyでも、`B_history_coarse` では `{C major}`、`B_history_fine` では `{C major, A minor}` へ分岐する。

**52**：同じgenerated target candidate set `{C major, A minor}` でも、prioritization policyにより `C major, A minor` と `A minor, C major` の候補順序へ分岐する。selected targetは生成しない。

**53**：同じprioritized ordering `C major(rank 1), A minor(rank 2)` でも、selection controllerなしでは未選択、`Γ_select_top_rank_fixture` では `C major`、`Γ_select_deceptive_source_fixture` では `A minor` がselected targetになる。target degree planは生成しない。

## ■ 6. 未解決ξ

46〜53の後に残る主なξは次である。

```text
ξ_target_candidate_generation_controller:
  どのΓ_target_candidate_generationを採用するか

ξ_generation_rule_origin:
  生成規則の由来、様式差、学習差、記述体系差

ξ_applicability_condition:
  function observation内のどの情報を適用条件として読むか

ξ_history_granularity:
  historyをどの長さ・粒度・軸で保持し、どのB_historyでrepresentation化するか

ξ_history_sensitive_generation:
  history representationのどの軸をΓ_target_candidate_generationが読むか

ξ_target_candidate_prioritization_controller:
  生成された候補集合にどの優先順位・重み・順序を与えるか

ξ_prioritization_rule_origin:
  prioritization policyの由来、様式差、形式差、履歴差

ξ_target_selection_controller:
  prioritized candidate orderingからselected targetを選ぶcontroller

ξ_selection_controller_origin:
  selection controllerの由来、適用条件、上位controllerとの接続

ξ_target_degree_planning:
  selected targetからtarget degree planをどう作るか
```

これらは現段階でCoreへ上げない。和声機能Module内の後続検証、声部進行Module、形式Moduleとの接続で扱う。

## ■ 7. 禁止補完

```text
dominant_candidateからtarget候補集合を自動生成しない
生成規則が存在することを一般和声規則の完成とみなさない
fixtureで生成された候補集合を正しい解決候補集合とみなさない
underlying historyをhistory representationと同一視しない
B_historyの粒度選択を一般原理として確定しない
候補集合の生成をprioritizationやselectionと同一視しない
prioritized orderの先頭候補をselected targetへ自動昇格しない
selected targetからtarget degree planを自動生成しない
各Γ・controllerをCoreへ昇格しない
```

## ■ 8. 現時点の読み方

46〜53の成果は、`ξ_target_candidate_generation` や `ξ_target_selection_controller` を完成させたことではない。

むしろ、targetへ向かう一本の因果列に見えていたものが、複数の境界へ分解されることを確認したことである。

```text
representation
  ↓
generation
  ↓
prioritization
  ↓
selection
  ↓
planning
```

ただし、この列も単純な自動パイプラインではない。各段階には、B、Γ、history representation、policy、controllerが横から入り、その採用条件や由来は未解決ξとして残る。

この分離が保てる限り、後で履歴依存、様式依存、形式依存の生成規則やselection controllerを追加しても、function annotationそのものへtarget生成・優先順位付け・選択を埋め込まずに済む。