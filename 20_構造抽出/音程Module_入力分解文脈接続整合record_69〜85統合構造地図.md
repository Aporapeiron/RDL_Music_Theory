# 構造抽出：音程Module・入力分解文脈接続整合record 69〜85統合構造地図

*対象：core module input candidateからinterval module state record candidateまでの境界列*  
*状態：DRAFT v0.1 / 69〜85統合圧縮*  

---

## ■ 0. 抽出目的

69〜85では、基層-learned側から得たcore module input candidateを、音程Moduleへ受理し、音程ラベル候補へ分解し、target selection、voice leading、next context、harmonic function annotation、context-harmony consistency、module state record候補へ接続するまでを、単一の自動処理として閉じずに分解した。

この統合地図は、次の五つの構造抽出版を一枚にまとめる。

```text
69〜73:
  基層-learned-core inputから音程ラベル候補境界

74〜76:
  音程ラベル候補からtarget selection境界

77〜79:
  selected targetから実現・bridge境界

80〜82:
  実現後next contextとharmonic annotation境界

83〜85:
  next context / harmonic annotation整合とrecord境界
```

---

## ■ 1. 全体地図

```text
core module input candidate
  + B_interval_module_reception
  + Gamma_interval_module_reception
  ↓
interval module boundary input candidate

interval module boundary input candidate
  + external pitch relation payload
  + B_chromatic
  + B_spelling
  + Gamma_interval_processing_frame
  ↓
interval module processing frame candidate

processing frame candidate
  + Gamma_generic
  ↓
generic interval candidate

generic interval candidate
  + chromatic distance
  + Gamma_quality
  ↓
quality candidate

generic interval candidate
  + quality candidate
  + Gamma_interval_label
  ↓
interval label candidate

interval label candidate
  + external interval context
  + Gamma_contextual_role
  ↓
contextual role annotation candidate

contextual role annotation candidate
  + external target candidate inventory
  + Gamma_interval_target_candidate_filter
  ↓
target candidate set observed

target candidate set observed
  + Gamma_interval_target_selection
  ↓
selected interval target candidate
```

selected interval target candidateから後段は二経路へ分かれる。

```text
selected interval target candidate
  + external voice leading plan
  + Gamma_voice_leading_request
  ↓
voice leading request candidate
  + external realization boundary
  + Gamma_voice_leading_realization
  ↓
concrete voice leading observation
  + external next context inventory
  + Gamma_next_context_candidate_filter
  ↓
next context candidate set observed
  + Gamma_next_context_selection
  ↓
selected next context candidate
```

```text
selected interval target candidate
  + external harmonic bridge inventory
  + Gamma_interval_harmonic_bridge
  ↓
harmonic function bridge candidate
  + external function vocabulary
  + Gamma_harmonic_function_annotation
  ↓
harmonic function annotation candidate
```

二経路の末端は、さらに整合境界へ入る。

```text
selected next context candidate
  + harmonic function annotation candidate
  + external consistency evidence
  + Gamma_context_harmony_consistency
  ↓
context-harmony consistency candidates
  + Gamma_context_harmony_consistency_selection
  ↓
selected consistency candidate
  + external record boundary
  + Gamma_interval_module_state_record
  ↓
interval module state record candidate
```

これは因果列ではない。各段階に外部payload、context、inventory、plan、boundary、vocabulary、evidence、B、Gamma、selection controllerが横から入る。

---

## ■ 2. 圧縮された工程

69〜85から見える工程は、次のように圧縮できる。

```text
module reception
internal frame activation
learned interval decomposition
contextual role annotation
target candidate observation
target selection
realization / bridge branching
next context observation / selection
harmonic function annotation
context-harmony consistency observation / selection
module state record candidate
```

ただしこれは実行順序や因果順序ではない。各段階は、外部条件を明示した接続境界である。

---

## ■ 3. 非同一性

69〜85から保持する非同一性は次である。

```text
core module input candidate
  ≠ interval module boundary input candidate

interval module boundary input candidate
  ≠ pitch relation payload generation
  ≠ interval module processing frame candidate

processing frame candidate
  ≠ generic interval candidate

generic interval candidate
  ≠ quality candidate
  ≠ interval label candidate

interval label candidate
  ≠ contextual role annotation candidate

contextual role annotation candidate
  ≠ target candidate set observed

target candidate set observed
  ≠ selected interval target candidate

selected interval target candidate
  ≠ voice leading request candidate
  ≠ harmonic function bridge candidate

voice leading request candidate
  ≠ concrete voice leading observation

concrete voice leading observation
  ≠ next context candidate set observed

next context candidate set observed
  ≠ selected next context candidate

harmonic function bridge candidate
  ≠ harmonic function annotation candidate

selected next context candidate
  ≠ harmonic function annotation candidate

selected next context candidate
  + harmonic function annotation candidate
  ≠ context-harmony consistency candidate

context-harmony consistency candidates
  ≠ selected consistency candidate

selected consistency candidate
  ≠ interval module state record candidate

interval module state record candidate
  ≠ confirmed M_B
  ≠ RDL Core昇格
```

---

## ■ 4. 禁止補完

69〜85から、次は補完しない。

```text
core module inputがあれば、
音程Module内部処理が自動開始する

processing frameがあれば、
generic / quality / labelが自動生成される

interval labelがあれば、
contextual roleやtarget候補が自動生成される

target候補集合があれば、
selected targetが自動確定する

selected targetがあれば、
具体声部進行や和声機能が自動生成される

concrete voice leadingがあれば、
next contextが自動確定する

harmonic bridgeがあれば、
harmonic function annotationが自動確定する

selected next contextがあれば、
harmonic function annotationと自動整合する

整合候補があれば、
selected consistencyが自動確定する

selected consistencyがあれば、
Module state recordへ自動保存される

module state recordがあれば、
confirmed M_BやRDL Coreへ自動昇格する
```

---

## ■ 5. 関係式としての読み

fixture内の限定表現として、最終的なstate record候補は次のように読める。

```text
interval module state record candidate
  =
C(
  core input,
  external pitch relation payload,
  internal B,
  external context,
  target inventory,
  voice leading plan,
  realization boundary,
  next context inventory,
  harmonic bridge inventory,
  function vocabulary,
  consistency evidence,
  record boundary;
  Gamma_reception,
  Gamma_processing_frame,
  Gamma_generic,
  Gamma_quality,
  Gamma_interval_label,
  Gamma_contextual_role,
  Gamma_target_filter,
  Gamma_target_selection,
  Gamma_voice_leading_request,
  Gamma_voice_leading_realization,
  Gamma_next_context_filter,
  Gamma_next_context_selection,
  Gamma_interval_harmonic_bridge,
  Gamma_harmonic_function_annotation,
  Gamma_context_harmony_consistency,
  Gamma_context_harmony_consistency_selection,
  Gamma_interval_module_state_record
)
```

これは一般式ではない。重要なのは、state record候補が単一入力の属性ではなく、多数の外部条件・B・Gamma・controllerを明示した関係から生じる候補として見えていることである。

---

## ■ 6. 未解決ξ

69〜85から残る未解決ξは次である。

```text
ξ_payload_origin:
  pitch relation payloadをどこから供給するか

ξ_internal_B_selection:
  B_chromatic / B_spelling / B_direction / B_octave_spanを
  どの条件で採用するか

ξ_interval_context_origin:
  interval labelに接続するcontextをどこから供給するか

ξ_inventory_origin:
  target / next context / harmonic bridge inventoryを
  どこから供給するか

ξ_function_vocabulary_origin:
  harmonic function annotation vocabularyをどこから供給するか

ξ_consistency_evidence_origin:
  selected next contextとharmonic annotationの整合evidenceを
  どこから供給するか

ξ_selection_controller_origin:
  target / next context / consistency selection controllerの由来

ξ_record_boundary_selection:
  どのrecord boundaryでModule状態候補として保存するか

ξ_confirmed_M_B_condition:
  state record candidateをconfirmed M_Bへ進める条件

ξ_core_promotion_condition:
  record / invariant / controllerのどれがCore昇格候補になり得るか
```

---

## ■ 7. 暫定結論

69〜85により、音程Moduleは次のような形で見えてきた。

```text
input
× payload
× internal B
× context
× inventory
× plan
× boundary
× vocabulary
× evidence
× Gamma
× controller
↓
候補 / 注釈 / 選択 / 観測 / record候補
```

音程Moduleは、物理差やlearned labelを受け取って自動的に意味・target・文脈・和声機能・状態recordへ変換する装置ではない。

むしろ、各段階で外部条件とGammaを明示し、どこで候補が生じ、どこで選択され、どこで整合し、どこでrecord候補として保存され、どこで停止しているかを保存するModuleとして見えている。

次に進むなら、`interval module state record candidate ≠ confirmed M_B` の境界を開く段階である。
