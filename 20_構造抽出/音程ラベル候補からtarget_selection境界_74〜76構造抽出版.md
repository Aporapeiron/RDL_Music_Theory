# 構造抽出：音程ラベル候補からtarget selection境界 74〜76

*対象：interval label candidateからcontextual role、target candidate set、selected targetまでの境界列*  
*状態：DRAFT v0.1 / 74〜76横断圧縮*  

---

## ■ 0. 抽出目的

74〜76では、73で得たinterval label candidateを文脈役割・target候補集合・selected targetへ接続するまでを、単一の自動処理として閉じずに分解した。

圧縮すると、次の系列である。

```text
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

これは因果列ではない。各段階に外部context、外部inventory、Gamma、selection controllerが横から入る。

---

## ■ 1. 非同一性

74〜76から保持する非同一性は次である。

```text
interval label candidate
  ≠ contextual role annotation candidate

contextual role annotation candidate
  ≠ target candidate set

target candidate set observed
  ≠ selected interval target candidate

selected interval target candidate
  ≠ voice leading realization
  ≠ harmonic function
  ≠ Core昇格
```

特に重要なのは、次の短絡を許していない点である。

```text
完全五度
  → 文脈役割

文脈役割
  → target候補集合

target候補集合
  → selected target

selected target
  → voice leading / harmonic function
```

---

## ■ 2. 抽出された共通型

今回のfixture内では、selected interval target candidateは次のように見える。

```text
selected interval target candidate
  =
C(
  interval label candidate,
  external interval context,
  external target candidate inventory;
  Gamma_contextual_role,
  Gamma_interval_target_candidate_filter,
  Gamma_interval_target_selection
)
```

ただしこれはfixture内の限定表現であり、一般的な音程Module規則ではない。

より安全に書けば、

```text
selected targetは、
音程ラベルの属性ではなく、
context・候補inventory・filter・selection controllerの関係から生じる。
```

である。

---

## ■ 3. 未解決ξ

74〜76から残る未解決ξは次である。

```text
ξ_interval_context_origin:
  interval labelに接続するcontextを
  どのModuleが生成・保持するか

ξ_contextual_role_gamma_selection:
  Gamma_contextual_roleを採用する条件

ξ_target_inventory_origin:
  target candidate inventoryをどこから供給するか

ξ_target_candidate_filter_generalization:
  target候補集合をfilterする一般条件

ξ_interval_target_selection_controller:
  selected interval targetを選ぶcontrollerの由来

ξ_voice_leading_realization_boundary:
  selected targetを具体声部進行へ接続する条件

ξ_harmonic_function_bridge:
  音程Module内のselected targetと和声機能Moduleを接続する条件
```

---

## ■ 4. 暫定結論

74〜76により、音程ラベル候補の後段は、少なくとも次の境界へ分解された。

```text
contextual role annotation
target candidate set observation
target selection
```

この結果、音程ラベルからtargetへ向かう道筋は、

```text
label
→ role
→ target
```

という自動列ではなく、

```text
label
× context
× inventory
× Gamma
× controller
```

の関係として扱うのが自然である。

次に進むなら、69〜76全体を、基層-learned-core inputからselected interval targetまでの一枚の構造地図へ統合する段階である。
