# 構造抽出：音程実現後 next context と harmonic annotation 境界 80〜82

*対象：concrete voice leading observationからnext context、harmonic bridgeからfunction annotationへ向かう境界列*  
*状態：DRAFT v0.1 / 80〜82横断圧縮*  

---

## ■ 0. 抽出目的

80〜82では、77〜79で得た二つの後段候補を、さらにnext context候補とharmonic function annotationへ接続する境界を分けた。

圧縮すると、次の二経路である。

```text
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
harmonic function bridge candidate
  + external function vocabulary
  + Gamma_harmonic_function_annotation
  ↓
harmonic function annotation candidate
```

これは因果列ではない。各段階に外部inventory、vocabulary、Gamma、selection controllerが横から入る。

---

## ■ 1. 非同一性

80〜82から保持する非同一性は次である。

```text
concrete voice leading observation
  ≠ next context candidate set

next context candidate set observed
  ≠ selected next context candidate

selected next context candidate
  ≠ harmonic function
  ≠ Core昇格

harmonic function bridge candidate
  ≠ harmonic function annotation candidate

harmonic function annotation candidate
  ≠ target generation
  ≠ voice leading generation
  ≠ Core昇格
```

特に重要なのは、次の短絡を許していない点である。

```text
concrete voice leading
  → next context

next context
  → harmonic function

harmonic bridge
  → harmonic function annotation

harmonic function annotation
  → target / voice leading
```

---

## ■ 2. 抽出された共通型

今回のfixture内では、後段二経路は次のように見える。

```text
selected next context
  =
C(
  concrete voice leading observation,
  external next context inventory;
  Gamma_next_context_candidate_filter,
  Gamma_next_context_selection
)
```

```text
harmonic function annotation
  =
C(
  harmonic function bridge candidate,
  external function vocabulary;
  Gamma_harmonic_function_annotation
)
```

ただしこれはfixture内の限定表現であり、一般的な音程Module規則ではない。

---

## ■ 3. 未解決ξ

80〜82から残る未解決ξは次である。

```text
ξ_next_context_inventory_origin:
  next context候補inventoryをどこから供給するか

ξ_next_context_filter_generalization:
  concrete voice leading observationから候補集合をfilterする一般条件

ξ_next_context_selection_controller:
  selected next contextを選ぶcontrollerの由来

ξ_function_vocabulary_origin:
  harmonic function annotation語彙をどこから供給するか

ξ_harmonic_function_annotation_gamma_selection:
  Gamma_harmonic_function_annotationを採用する条件

ξ_target_generation_after_function_annotation:
  harmonic function annotationからtarget候補生成へ進む条件

ξ_cross_module_core_promotion:
  音程Module・和声機能Module・文脈解釈のどの境界がCore昇格候補になり得るか
```

---

## ■ 4. 暫定結論

80〜82により、音程Module後段の二方向は、少なくとも次の境界へ分解された。

```text
next context candidate observation / selection
harmonic function annotation
```

この結果、具体声部進行やharmonic bridgeから上位文脈へ向かう道筋は、

```text
observation / bridge
× inventory / vocabulary
× Gamma / controller
```

の関係から生じる候補として扱うのが自然である。

次に進むなら、69〜82全体を、base/learned/core inputから音程Module後段文脈接続までの一枚の構造地図へ統合する段階である。
