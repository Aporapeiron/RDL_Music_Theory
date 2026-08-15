# 構造抽出：音程selected targetから実現・bridge境界 77〜79

*対象：selected interval target candidateからvoice leading realizationとharmonic function bridgeへ向かう境界列*  
*状態：DRAFT v0.1 / 77〜79横断圧縮*  

---

## ■ 0. 抽出目的

77〜79では、76で得たselected interval target candidateを、具体声部進行側と和声機能Module接続側へ進める境界を分けた。

圧縮すると、次の二経路である。

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
```

```text
selected interval target candidate
  + external harmonic bridge inventory
  + Gamma_interval_harmonic_bridge
  ↓
harmonic function bridge candidate
```

これは因果列ではない。各段階に外部plan、boundary、inventory、Gammaが横から入る。

---

## ■ 1. 非同一性

77〜79から保持する非同一性は次である。

```text
selected interval target candidate
  ≠ voice leading request candidate
  ≠ harmonic function bridge candidate

voice leading request candidate
  ≠ concrete voice leading observation

concrete voice leading observation
  ≠ harmonic function
  ≠ next context interpretation

harmonic function bridge candidate
  ≠ harmonic function annotation
  ≠ target generation
```

特に重要なのは、次の短絡を許していない点である。

```text
selected target
  → concrete voice leading

selected target
  → harmonic function

concrete voice leading
  → next context interpretation
```

---

## ■ 2. 抽出された共通型

今回のfixture内では、後段二経路は次のように見える。

```text
voice leading observation
  =
C(
  selected interval target,
  external voice leading plan,
  external realization boundary;
  Gamma_voice_leading_request,
  Gamma_voice_leading_realization
)
```

```text
harmonic function bridge candidate
  =
C(
  selected interval target,
  external harmonic bridge inventory;
  Gamma_interval_harmonic_bridge
)
```

ただしこれはfixture内の限定表現であり、一般的な音程Module規則ではない。

---

## ■ 3. 未解決ξ

77〜79から残る未解決ξは次である。

```text
ξ_voice_leading_plan_origin:
  selected targetから読むvoice leading planを
  どのModuleが生成・保持するか

ξ_realization_boundary_selection:
  realization boundaryをどの条件で採用するか

ξ_voice_leading_realization_controller:
  具体音候補から実現を選ぶcontrollerの由来

ξ_harmonic_bridge_inventory_origin:
  和声機能Moduleへ渡すbridge候補inventoryをどこから供給するか

ξ_interval_harmonic_bridge_gamma_selection:
  Gamma_interval_harmonic_bridgeを採用する条件

ξ_next_context_interpretation_boundary:
  concrete voice leading observationからnext context候補へ進む条件
```

---

## ■ 4. 暫定結論

77〜79により、selected interval targetの後段は、少なくとも次の二方向へ分解された。

```text
voice leading request / realization
harmonic function bridge
```

この結果、selected interval targetは、具体声部進行や和声機能の属性ではなく、

```text
target
× plan / boundary / inventory
× Gamma / controller
```

の関係から後段候補へ接続されるものとして扱うのが自然である。

次に進むなら、69〜79全体を、基層-learned-core inputから音程Module後段接続までの一枚の構造地図へ統合する段階である。
