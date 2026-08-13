# 和声機能｜Module計画

*状態：DRAFT v0.1*

## 0. 目的

和音Moduleから渡された和音候補、音階・調Moduleから渡されたkey context、scale degree roleを受け取り、和声機能をRDL音楽側の文脈注釈Moduleとして整理する。

このModuleは、和音名からtonic / dominant / predominantなどの機能を一意に決めない。機能は、key context、音度役割、前後関係、様式、learned tendencyによって立ち上がる候補注釈として扱う。

```text
chord candidate
  + key context
  + degree role
  + local history
  ↓
B_harmonic_function + Γ_function_annotation
  ↓
functional annotation候補
  ↓
target候補 / 声部進行 / 形式Module
```

ここでは、緊張・安定・解決感を基層知覚の完成モデルとして置かない。

## 1. 参照する既知音楽理論

- `30_既知音楽理論参照/05_和声機能.md`
- `10_検証/12_音程分解_同一トライトーンと綴りによる解決方向_最小実験.md`
- `10_検証/13_音程分解_解決候補の文脈分解_最小実験.md`

既知音楽理論側では、次の語彙が参照される。

| 語彙 | このModuleでの扱い |
|---|---|
| tonic | 中心・安定として扱われる機能注釈候補 |
| predominant | dominantへ向かう前置機能注釈候補 |
| dominant | tonicへの解決傾向として扱われる機能注釈候補 |
| cadence | 終止として慣習的に分類される進行候補 |
| applied dominant | 一時的対象へのdominant的注釈候補 |

これらはlearnedな機能分類であり、物理法則や基層知覚そのものではない。

## 2. 既存検証との接続

主に接続する検証は次の通り。

| 検証 | 接続内容 |
|---|---|
| `12_音程分解_同一トライトーンと綴りによる解決方向_最小実験.md` | A4/d5ラベルからtargetを自動生成せず、外部target後に運動を記述 |
| `13_音程分解_解決候補の文脈分解_最小実験.md` | 文脈・音度役割・learned tendency・既選択targetの分解 |
| `04_和音_Module計画.md` | 同じ和音候補でもkey contextにより機能注釈が変わる |

既存検証から受け取る最小構造は次の通り。

```text
interval / chord label
  + key context
  + scale-degree role
  + learned tendency
  ↓
functional annotation候補
  ↓
selected targetがある場合のみ
Γ_motion
```

## 3. B

このModuleの境界候補。

| 境界 | 役割 |
|---|---|
| `B_key_context` | tonic、scale、key signature、局所調を保持する |
| `B_chord_degree` | 和音rootや構成音のscale degreeを保持する |
| `B_function_vocab` | tonic / predominant / dominant等の語彙体系を指定する |
| `B_local_history` | 直前・直後の和声状態、反復、持続を保持する |
| `B_cadential_frame` | 終止として読む範囲を指定する |
| `B_target_given` | 解決targetが外部から与えられているかを保持する |
| `B_style_context` | 様式・ジャンル・時代的慣習を注釈する |

`B_function_vocab` を置いても、個別の和音が自動的に機能化されるわけではない。

```text
chord label
  ≠ function
  ≠ target
  ≠ resolution
```

## 4. Γ

このModuleで使う関係抽出・注釈規則。

| Γ | 入力 | 出力 |
|---|---|---|
| `Γ_degree_annotation` | chord candidate、key context | root degree / chord degree |
| `Γ_function_annotation` | degree、history、vocab | function label候補 |
| `Γ_tendency_annotation` | function候補、learned体系 | tendency候補 |
| `Γ_cadence_annotation` | chord sequence、cadential frame | cadence候補 |
| `Γ_target_link` | function候補、外部target候補 | target注釈 |
| `Γ_motion` | selected target | 声部運動記述 |

`Γ_tendency_annotation` は傾向の注釈であり、具体的targetを必ず生成する規則ではない。

## 5. M_B候補

このModuleのM_B候補。

| M_B候補 | 内容 |
|---|---|
| `functional_annotation_candidate` | tonic / dominant等の機能注釈候補 |
| `degree_function_bundle` | scale degreeと機能語彙の束 |
| `learned_tendency_candidate` | 代表的進行傾向候補 |
| `cadential_candidate` | 終止候補として読める進行束 |
| `applied_function_candidate` | 一時的中心への機能注釈候補 |
| `target_annotation_record` | 既選択targetへの文脈注釈 |

和声機能のM_B候補は、現在文脈におけるlearnedな読みの束である。

```text
same chord candidate
  + different key context
  ↓
different function候補
```

## 6. 候補生成・制約・選択

### 候補生成

- 和音候補をkey context内のdegreeへ写す
- degreeから機能注釈候補を生成する
- 前後関係からcadence候補を生成する
- 一時的中心がある場合、applied function候補を生成する
- 既選択targetがある場合、target注釈とmotion recordを生成する

### 制約

- key contextが確定しているか
- 和音rootが確定しているか
- 局所調・転調・借用を許すか
- 終止範囲をどこまで見るか
- 様式語彙をどこまで採用するか
- targetが未指定か、外部入力済みか

### 選択

このModule単独では、次の和音や具体的声部進行を最終選択しない。

```text
functional annotation候補
  ↓
target候補集合
  ↓
声部進行Module / 実現Module
```

候補が複数残る場合は、`underdetermined` として保持する。

## 7. 破断条件

このModuleが破断する、または未解決ξを残す条件。

- 同じ和音がkey contextによって別機能になる
- key contextが複数候補あり、機能注釈が収束しない
- 和音rootが曖昧でdegree注釈が定まらない
- dominant候補はあるが、target候補が未指定である
- 終止候補が様式や前後関係によって分岐する
- applied dominantやtonicizationで局所中心が二重化する
- 機能ラベルを聴覚上の緊張・安定と同一視してしまう

禁止する短絡は次の通り。

```text
V = dominantとして常に確定
dominant = tonicへ必ず解決
function label = target generator
cadence label = actual closure
tonic = human perceptual center
H = harmonic tension
```

## 8. 未解決ξ

現時点で残す未解決領域。

- 機能注釈の選択原理
- tonic中心性の成立条件
- dominant的傾向の文化差・様式差
- cadenceが終止として成立する条件
- applied dominantや転調境界
- target候補集合の生成・競合・優先順位
- 機能注釈と実際の声部進行の接続
- 聴取上の緊張・解決感とlearned機能語彙の差分
- Hとの関係をどの層で扱うか

これらは、声部進行Module、形式Module、基層仮説へ送る。

## 9. 次の最小検証

次に必要な最小検証は、同じ和音候補がkey contextにより異なるfunction候補へ写ることの確認である。

```text
same chord candidate
  + different key context
  ↓
different function annotation
```

最小ケース。

| ケース | 検証したいこと |
|---|---|
| `G-B-D` in C major | V / dominant候補として注釈される |
| `G-B-D` in G major | I / tonic候補として注釈される |
| `D-F#-A` in C major | secondary dominant候補として注釈されうる |
| `D-F#-A` in G major | V / dominant候補として注釈される |

この検証により、和音名や音集合ではなく、key contextとdegree roleが機能注釈を分岐させることを確認する。

## 10. 現時点の短縮式

```text
和声機能Moduleは、
和音名を機能へ直結せず、
key context・degree role・履歴・learned tendencyを通して
機能注釈候補を保持する。

機能ラベルはtarget生成器でも、
基層知覚の完成モデルでもない。
```
