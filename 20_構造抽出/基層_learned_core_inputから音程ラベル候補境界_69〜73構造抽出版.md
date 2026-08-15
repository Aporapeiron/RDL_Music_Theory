# 構造抽出：基層-learned-core inputから音程ラベル候補境界 69〜73

*対象：core module input candidateから音程Module内のinterval label candidateまでの境界列*  
*状態：DRAFT v0.1 / 69〜73横断圧縮*  

---

## ■ 0. 抽出目的

69〜73では、基層-learned側から得たcore module input candidateを、音程Module内部の音程ラベル候補へ接続するまでを、単一の自動処理として閉じずに分解した。

圧縮すると、次の系列である。

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
```

これは因果列ではない。各段階に、外部payload、B、Gamma、fixture条件が横から入る。

---

## ■ 1. 69〜73の役割

```text
69:
core module input candidate
→ interval module boundary input candidate

70:
interval module boundary input candidate
→ interval module processing frame candidate

71:
processing frame candidate
→ generic interval candidate

72:
generic interval candidate + chromatic distance
→ quality candidate

73:
generic interval candidate + quality candidate
→ interval label candidate
```

どの段階でも、次段階を自動生成しない。

---

## ■ 2. 非同一性

69〜73から保持する非同一性は次である。

```text
core module input candidate
  ≠ interval module boundary input candidate

interval module boundary input candidate
  ≠ pitch relation payload generation
  ≠ interval module processing frame candidate

interval module processing frame candidate
  ≠ generic interval candidate

generic interval candidate
  ≠ quality candidate
  ≠ interval label candidate

quality candidate
  ≠ interval label candidate

interval label candidate
  ≠ contextual role annotation
  ≠ target candidate generation
  ≠ harmonic function
  ≠ Core昇格
```

特に重要なのは、69〜73が次の短絡を許していない点である。

```text
base/learned側のmusical interpretation
  → 音程ラベル

core module input
  → 音程Module内部処理開始

7 semitones
  → 完全五度

完全五度
  → 文脈役割 / target / harmonic function
```

---

## ■ 3. 抽出された共通型

今回のfixture内では、音程ラベル候補は次のように見える。

```text
interval label candidate
  =
C(
  interval module boundary input candidate,
  external pitch relation payload,
  B_chromatic,
  B_spelling;
  Gamma_processing_frame,
  Gamma_generic,
  Gamma_quality,
  Gamma_interval_label
)
```

ただしこれはfixture内の限定表現であり、一般的な音程Module規則ではない。

より安全に書けば、

```text
音程ラベル候補は、
入力候補・外部payload・内部B・複数Gammaの関係から生じる。
```

である。

---

## ■ 4. 禁止補完

69〜73から、次は補完しない。

```text
interval module boundary input candidateがあれば、
音程Module内部処理が自動開始する

processing frame candidateがあれば、
generic intervalが自動生成される

generic interval candidateがあれば、
qualityやinterval labelが自動生成される

interval label candidateがあれば、
contextual roleやtarget候補が自動生成される

interval label candidateがあれば、
和声機能Moduleや声部進行Moduleへ接続済みである
```

---

## ■ 5. 未解決ξ

69〜73から残る未解決ξは次である。

```text
ξ_pitch_relation_payload_origin:
  core module input candidateから読むpayloadを
  誰がどのBで生成・保持するか

ξ_interval_reception_boundary_generalization:
  B_interval_module_receptionを一般Module境界にできる条件

ξ_internal_boundary_selection:
  B_chromatic / B_spelling / B_direction / B_octave_spanを
  どの入力で採用するか

ξ_gamma_generic_generalization:
  generic interval生成規則の一般化条件

ξ_gamma_quality_generalization:
  quality判定規則の一般化条件

ξ_interval_label_vocabulary:
  interval label語彙の範囲と文化・記譜体系差

ξ_contextual_role_boundary:
  interval label candidateからcontextual role annotationへ進む条件

ξ_target_generation_boundary:
  interval labelやcontextual roleからtarget候補を生成する条件

ξ_core_promotion_condition:
  どの構造がRDL Coreへ昇格し得るか
```

---

## ■ 6. 暫定結論

69〜73により、基層-learned側から中核音楽理論Moduleへ入る経路は、少なくとも次の境界へ分解された。

```text
module reception
processing frame activation
generic interval generation
quality generation
interval label generation
```

この結果、音程ラベル候補は単一の物理差、learned category、core input、または半音距離の属性ではなく、

```text
入力候補
× 外部payload
× 内部B
× 複数Gamma
```

の関係から生じる候補として扱うのが自然である。

次に進むなら、`interval label candidate ≠ contextual role annotation` の境界を開く段階である。
