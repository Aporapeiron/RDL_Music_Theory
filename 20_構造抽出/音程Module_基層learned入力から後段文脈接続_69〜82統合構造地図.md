# 構造抽出：音程Module・基層learned入力から後段文脈接続 69〜82統合構造地図

*対象：core module input candidateから音程Module内部生成、target selection、voice leading、next context、harmonic annotationまでの境界列*  
*状態：DRAFT v0.1 / 69〜82統合圧縮*  

---

## ■ 0. 抽出目的

69〜82では、基層-learned側から得たcore module input candidateを、音程Moduleへ受理し、音程ラベル候補へ分解し、文脈役割・target選択・具体声部進行・next context・harmonic function annotationへ接続するまでを、単一の自動処理として閉じずに分解した。

この統合地図は、69〜73、74〜76、77〜79、80〜82の四つの構造抽出版を一枚にまとめる。

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

ここから後段は二方向へ分かれる。

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

これは因果列ではない。各段階に外部payload、context、inventory、plan、boundary、vocabulary、B、Gamma、selection controllerが横から入る。

---

## ■ 2. 四つの圧縮範囲

```text
69〜73:
core input
→ interval module reception
→ processing frame
→ generic interval
→ quality
→ interval label

74〜76:
interval label
→ contextual role
→ target candidate set
→ selected interval target

77〜79:
selected interval target
→ voice leading request / concrete realization
→ harmonic bridge

80〜82:
concrete voice leading
→ next context candidate / selected next context

harmonic bridge
→ harmonic function annotation
```

それぞれの矢印は、外部条件とGammaを明示した場合だけ成立するfixture内の接続である。

---

## ■ 3. 非同一性

69〜82から保持する非同一性は次である。

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
  ≠ harmonic function

next context candidate set observed
  ≠ selected next context candidate

harmonic function bridge candidate
  ≠ harmonic function annotation candidate

harmonic function annotation candidate
  ≠ target generation
  ≠ voice leading generation
  ≠ Core昇格
```

---

## ■ 4. 禁止補完

69〜82から、次は補完しない。

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

harmonic function annotationがあれば、
targetやvoice leadingが自動生成される
```

---

## ■ 5. 抽出された系列

69〜82から見える系列は、次のように圧縮できる。

```text
reception
→ internal frame activation
→ learned interval decomposition
→ contextual role annotation
→ target candidate observation
→ target selection
→ realization / bridge branching
→ next context observation / selection
→ harmonic function annotation
```

ただし、これは実行順序や因果順序ではない。各段階は、外部条件を明示した接続境界である。

---

## ■ 6. 関係式としての読み

fixture内の限定表現として、音程Module後段の出力は次のように読める。

```text
interval label candidate
  =
C(
  core input,
  external pitch relation payload,
  B_chromatic,
  B_spelling;
  Gamma_reception,
  Gamma_processing_frame,
  Gamma_generic,
  Gamma_quality,
  Gamma_interval_label
)
```

```text
selected interval target
  =
C(
  interval label,
  external interval context,
  external target inventory;
  Gamma_contextual_role,
  Gamma_target_filter,
  Gamma_target_selection
)
```

```text
selected next context
  =
C(
  selected interval target,
  external voice leading plan,
  external realization boundary,
  external next context inventory;
  Gamma_voice_leading_request,
  Gamma_voice_leading_realization,
  Gamma_next_context_filter,
  Gamma_next_context_selection
)
```

```text
harmonic function annotation
  =
C(
  selected interval target,
  external harmonic bridge inventory,
  external function vocabulary;
  Gamma_interval_harmonic_bridge,
  Gamma_harmonic_function_annotation
)
```

これらは一般式ではない。重要なのは、どの結果も単一入力の属性ではなく、入力候補、外部条件、B、Gamma、controllerの関係から生じる候補として見えていることである。

---

## ■ 7. 未解決ξ

69〜82から残る未解決ξは次である。

```text
ξ_payload_origin:
  pitch relation payloadをどこから供給するか

ξ_internal_B_selection:
  B_chromatic / B_spelling / B_direction / B_octave_spanを
  どの条件で採用するか

ξ_interval_label_vocabulary:
  interval label語彙の範囲と文化・記譜体系差

ξ_interval_context_origin:
  interval labelに接続するcontextをどこから供給するか

ξ_target_inventory_origin:
  target candidate inventoryをどこから供給するか

ξ_selection_controller_origin:
  target / next context selection controllerの由来

ξ_voice_leading_plan_origin:
  voice leading planをどこから供給するか

ξ_realization_boundary_selection:
  concrete realization boundaryをどの条件で採用するか

ξ_next_context_inventory_origin:
  next context inventoryをどこから供給するか

ξ_harmonic_bridge_inventory_origin:
  harmonic bridge inventoryをどこから供給するか

ξ_function_vocabulary_origin:
  harmonic function annotation vocabularyをどこから供給するか

ξ_cross_module_consistency:
  selected next contextとharmonic function annotationを
  どの境界で整合させるか

ξ_core_promotion_condition:
  どの境界・record・不変条件がRDL Core昇格候補になり得るか
```

---

## ■ 8. 暫定結論

69〜82により、基層-learned-core inputから音程Moduleの後段文脈接続までが、次のような多段境界列として見えてきた。

```text
input
× payload
× internal B
× context
× inventory
× plan
× boundary
× vocabulary
× Gamma
× controller
↓
候補 / 注釈 / 選択 / 観測
```

音程Moduleは、物理差やlearned labelを受け取って自動的に意味・target・文脈・和声機能へ変換する装置ではない。

むしろ、各段階で外部条件とGammaを明示し、どこで候補が生じ、どこで選択され、どこで停止しているかを保存するModuleとして見えている。

次に進むなら、`selected next context` と `harmonic function annotation` の整合境界を開く段階である。
