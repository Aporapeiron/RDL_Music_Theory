# 和声機能｜target候補生成 46〜48構造抽出版

*対象：46〜48で確認した `ξ_target_candidate_generation` の最小構造*  
*状態：DRAFT v0.1 / 42〜45循環分解後の局所構造抽出*

## ■ 0. 位置づけ

本書は、46〜48の最小検証列から、function annotation candidateの後段にあるtarget候補生成境界を抽出する。

42〜45では、function annotationからtarget候補集合を生成しなかった。

46〜48では、fixture用の限定 `Γ_target_candidate_generation` を置いた場合でも、annotation、生成規則、規則の適用可否、生成済み候補集合、選択を同一視しないことを確認した。

本書は一般和声規則を追加しない。

## ■ 1. 抽出された接続地図

```text
function observation ───────────────┐
  ├─ function annotation label       │
  └─ key context                     │
                                    ├→ applicability check
Γ_target_candidate_generation ──────┘
                                    ↓
                         generated target candidate set
                                    │
                                    │ selected targetを生成しない
                                    ↓
                         selection boundaryへ渡す
```

この地図は、function annotation labelからtarget候補集合が直に生えることを示さない。生成済み候補集合は、少なくともfunction observationと生成規則の組に依存する。

## ■ 2. 検証ごとの担当

| 検証 | 担当する範囲 | 確認した境界 |
|---|---|---|
| 46 | annotation / generation rule / generated setの分離 | function annotation単独では候補生成しない |
| 47 | same annotation + same context + different Γ | 生成規則差し替えで候補集合が変わる |
| 48 | same annotation label + different context + same Γ | context差し替えで候補集合が変わる |

## ■ 3. 保持する非同一性

46〜48から、次の非同一性を保持する。

```text
function annotation
  ≠ target candidate generation rule

generation ruleの存在
  ≠ 現在のfunction observationへの適用可能性

rule applicability result
  ≠ generated target candidate set

generated target candidate set
  ≠ selected target
```

特に46で、生成規則の適用可能性もfunction annotation単独では決まらず、key contextとの組に依存することを確認した。

## ■ 4. 依存関係として見えた形

fixture内では、target候補集合は次のように読むのが堅い。

```text
generated target candidate set
  = C(function observation; Γ_target_candidate_generation)
```

今回のfixture用Γは、function observationのうちfunction annotation labelとkey contextを参照した。

47では、function annotationとcontextを固定して、Γを変えた。

```text
same annotation
same context
different Γ
↓
different candidate set
```

48では、function annotation labelとΓを固定して、contextを変えた。

```text
same annotation label
different context
same Γ
↓
different candidate set
```

したがって、candidate setはfunction annotationの属性ではない。

## ■ 5. 確定接続

**46**：`dominant_candidate + C major + Γ_target_candidate_generation_fixture` から `{C major, A minor}` を生成できる。ただし、規則なしでは `no_generation_rule`、適用外では `rule_not_applicable` となる。

**47**：同じ `dominant_candidate + C major` でも、生成規則を変えると `{C major, A minor}` と `{C major}` へ分岐する。

**48**：同じ `dominant_candidate` labelと同じ文脈依存fixture規則でも、contextを `C major` から `G major` へ変えると `{C major, A minor}` と `{G major, E minor}` へ分岐する。

## ■ 6. 未解決ξ

46〜48の後に残る主なξは次である。

```text
ξ_target_candidate_generation_controller:
  どのΓ_target_candidate_generationを採用するか

ξ_generation_rule_origin:
  生成規則の由来、様式差、学習差、記述体系差

ξ_applicability_condition:
  function observation内のどの情報を適用条件として読むか

ξ_history_sensitive_generation:
  同じannotation・context・Γでも履歴により候補集合が変わるか

ξ_target_candidate_prioritization:
  生成された候補集合に優先順位や重みを与えるか

ξ_target_selection_controller:
  生成済み候補集合からselected targetを選ぶ一般controller
```

これらは現段階でCoreへ上げない。和声機能Module内の後続検証、または声部進行Module・形式Moduleとの接続で扱う。

## ■ 7. 禁止補完

```text
dominant_candidateからtarget候補集合を自動生成しない
生成規則が存在することを一般和声規則の完成とみなさない
fixtureで生成された候補集合を正しい解決候補集合とみなさない
候補集合の生成をselected targetと同一視しない
生成規則の選択controllerをCoreへ昇格しない
```

## ■ 8. 現時点の読み方

46〜48の成果は、`ξ_target_candidate_generation` を完成させたことではない。

むしろ、target候補生成が次の関係として現れることを、fixture上で二方向から確認したことである。

```text
function observation
  + Γ_target_candidate_generation
  ↓
applicability check
  ↓
generated target candidate set
  ↓
selection boundary
```

この分離が保てる限り、後で履歴依存、様式依存、形式依存の生成規則を追加しても、function annotationそのものへtarget生成を埋め込まずに済む。

