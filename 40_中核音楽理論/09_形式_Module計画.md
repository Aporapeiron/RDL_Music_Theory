# 形式｜Module計画

*状態：DRAFT v0.1*

## 0. 目的

旋律、リズム、和声、反復、対比、展開、終止を長い時間範囲で束ね、形式候補として扱うModule境界を定める。

このModuleは、楽式名を作品の唯一の因果構造として扱わない。形式は、素材の反復・変形・対比・終止・文脈範囲によって立ち上がる上位の記述候補である。

```text
motif / phrase / harmonic span / rhythm span
  ↓
B_form + Γ_form_relation
  ↓
section / form candidate
```

## 1. 参照する既知音楽理論

- `30_既知音楽理論参照/09_形式.md`
- `40_中核音楽理論/08_旋律_Module計画.md`
- `40_中核音楽理論/05_和声機能_Module計画.md`
- `40_中核音楽理論/07_リズム拍節_Module計画.md`

| 語彙 | このModuleでの扱い |
|---|---|
| motive / phrase / period | 小規模構成単位候補 |
| binary / ternary form | 大域的区分候補 |
| rondo | 主題反復候補 |
| variation | 素材保存と変形候補 |
| sonata form | 歴史的・様式的な大規模形式候補 |

## 2. 既存検証との接続

形式専用検証は未着手である。既存Moduleから次を受け取る。

```text
旋律Module   → motif / phrase候補
リズムModule → time span / repetition
和声機能Module → cadence / functional span候補
声部進行Module → realized transition history
```

## 3. B

| 境界 | 役割 |
|---|---|
| `B_form_span` | 形式として読む時間範囲 |
| `B_section_boundary` | section候補境界 |
| `B_repetition_scope` | 反復として比較する範囲 |
| `B_contrast_axis` | 対比とみなす軸 |
| `B_variation_tolerance` | 変形を同一素材として扱う許容度 |
| `B_cadential_context` | 終止候補を保持する |

## 4. Γ

| Γ | 入力 | 出力 |
|---|---|---|
| `Γ_repetition` | span同士 | 反復候補 |
| `Γ_contrast` | span同士 | 対比候補 |
| `Γ_variation` | 素材、変形後素材 | 変奏候補 |
| `Γ_section_boundary` | phrase、cadence、休止 | section境界候補 |
| `Γ_form_label` | section関係 | binary / ternary等の形式ラベル候補 |

## 5. M_B候補

| M_B候補 | 内容 |
|---|---|
| `section_candidate` | 区分候補 |
| `repetition_candidate` | 反復候補 |
| `contrast_candidate` | 対比候補 |
| `variation_candidate` | 保存と変形の候補 |
| `cadential_span_candidate` | 終止を含むまとまり |
| `form_label_candidate` | 楽式名候補 |

## 6. 候補生成・制約・選択

- motif / phrase候補からsection候補を生成する
- section同士の反復・対比・変形を比較する
- cadence候補をsection境界の一要素として扱う
- form labelは複数候補として保持する

このModule単独では、作品の形式を一意に確定しない。

## 7. 破断条件

- 同じ素材が反復とも変奏とも読める
- section境界が旋律・和声・記譜・聴取で一致しない
- 楽式名と実際の構造がずれる
- 歴史的用法を普遍構造として扱ってしまう
- form labelから聴取上のまとまりを一意に導いてしまう

## 8. 未解決ξ

- 反復と変形の許容境界
- section境界の選択原理
- cadenceと形式境界の接続
- 聴取記憶、期待、回帰感
- 歴史的・様式的な楽式語彙の扱い
- 長時間構造と局所Moduleの接続

## 9. 次の最小検証

```text
same motif
  ↓ repetition / variation
  ↓ section candidate
```

最小ケースは、短いmotif A、変形A'、対比Bを作り、`A-A'` を反復/変奏候補、`A-B` を対比候補として分ける。

## 10. 現時点の短縮式

```text
形式Moduleは、
楽式名を構造そのものへ直結せず、
反復・対比・変形・終止・区分境界から
form candidateを扱う。
```
