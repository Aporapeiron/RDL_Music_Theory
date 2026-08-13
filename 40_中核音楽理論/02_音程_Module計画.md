# 音程・綴り｜Module計画

*状態：DRAFT v0.1*

## 0. 目的

音高・調律Moduleから渡された連続座標・12TETカテゴリー・偏差recordを受け取り、音程名と綴り関係がどの境界で分岐するかを整理する。

このModuleは、周波数比や半音数から音程名を一意に導かない。音程名は、少なくとも半音距離、音名上のgeneric interval、quality判定、綴り、文脈注釈を通って成立するlearned記述として扱う。

```text
tuning_category_candidate
  ↓
B_spelling + Γ_interval
  ↓
generic interval / quality / interval label
  ↓
contextual role annotation
```

ここでは、文脈targetの生成器や普遍的な解決規則を作らない。targetが与えられた後の運動記述と、targetを選ぶ過程は分けて保持する。

## 1. 参照する既知音楽理論

- `30_既知音楽理論参照/01_音程.md`
- `20_構造抽出/物理音高から音楽ラベルへの分岐構造抽出版.md`

既知音楽理論側では、次の分類が参照される。

| 語彙 | このModuleでの扱い |
|---|---|
| chromatic semitone distance | 12TET上の半音距離 |
| generic interval | 音名文字の間隔から得る度数 |
| quality | generic intervalの基準半音数との差による品質 |
| compound interval | 1オクターブを超える音程の扱い |
| A4 / d5 / P5 / d6 | learned記述としての音程ラベル候補 |

音程名は既知音楽理論の圧縮ラベルであり、RDL Coreへ直接昇格しない。

## 2. 既存検証との接続

主に接続する検証は次の通り。

| 検証 | 接続内容 |
|---|---|
| `10_音程分解_周波数比から12TET半音数_最小実験.md` | 物理比からcents、12TET半音カテゴリーまで |
| `11_音程分解_同一7半音と綴り_P5_d6_最小実験.md` | 同じ7半音が綴りでP5/d6へ分岐 |
| `12_音程分解_同一トライトーンと綴りによる解決方向_最小実験.md` | 同じ6半音がA4/d5へ分岐し、外部targetに対して運動方向が分かれる |
| `13_音程分解_解決候補の文脈分解_最小実験.md` | 既選択targetを文脈・音度役割・learned tendencyへ分解 |

既存検証から受け取る最小構造は次の通り。

```text
frequency ratio
  ↓ Γ_cents
continuous interval coordinate
  ↓ Γ_12TET_round
chromatic semitone category
  ↓ B_spelling + Γ_generic
generic interval
  ↓ Γ_quality
interval label
```

さらに文脈が接続される場合は、次のように分ける。

```text
interval label
  ↓ context / role / learned tendency
selected target annotation
  ↓ Γ_motion
motion description
```

## 3. B

このModuleの境界候補。

| 境界 | 役割 |
|---|---|
| `B_chromatic` | 12TET上の半音距離を保持する |
| `B_spelling` | 音名・臨時記号・綴りを比較関係として保持する |
| `B_direction` | 上行・下行、順序付き二音関係を保持する |
| `B_octave_span` | compound intervalを扱うか、単純音程へ折り畳むか |
| `B_context_role` | 調性・音度役割・和声文脈を注釈として接続する |
| `B_target_given` | targetが外部から与えられているか、候補生成の対象にするか |

特に、`B_spelling` がない場合、同じ7半音はP5/d6へ分岐できない。

```text
7 semitones
  ↓ B_spellingなし
7 semitonesで停止

7 semitones
  ↓ B_spellingあり
P5 / d6へ分岐可能
```

## 4. Γ

このModuleで使う関係抽出・変換規則の候補。

| Γ | 入力 | 出力 |
|---|---|---|
| `Γ_chromatic` | 二音の12TET位置 | 半音距離 |
| `Γ_generic` | 音名文字の順序 | generic interval |
| `Γ_quality` | generic interval、半音距離 | quality |
| `Γ_interval_label` | generic interval、quality | 音程ラベル |
| `Γ_role_annotation` | 文脈、開始音度、目標音度 | 役割注釈 |
| `Γ_motion` | selected target | 半音移動量、外向き/内向き等の運動記述 |

`Γ_motion` は、targetが選ばれた後の記述規則である。`A4 / d5` からtargetを一意に生成する規則ではない。

## 5. M_B候補

このModuleのM_B候補。

| M_B候補 | 内容 |
|---|---|
| `chromatic_interval_candidate` | 半音距離としての候補 |
| `spelled_interval_candidate` | 綴りを保持した二音関係 |
| `generic_interval_candidate` | 五度、六度などの度数候補 |
| `quality_candidate` | 完全、長短、増減などの品質候補 |
| `interval_label_candidate` | P5、d6、A4、d5などのラベル候補 |
| `contextual_role_annotation` | 音度役割、調性、代表的進行規則への注釈 |
| `selected_target_motion_record` | targetが与えられた後の運動記述 |

このModuleで重要なのは、同じ物理関係が複数のlearned記述へ分岐できることを保存することである。

```text
same physical pitch pair
  ≠ same spelling relation
  ≠ same interval label
  ≠ same contextual target
```

## 6. 候補生成・制約・選択

### 候補生成

- 半音距離候補を生成する
- 綴りからgeneric interval候補を生成する
- generic intervalと半音距離からquality候補を生成する
- interval label候補を生成する
- 文脈が与えられた場合、音度役割やlearned tendencyの注釈候補を生成する
- targetが既に選択されている場合、運動記述を生成する

### 制約

- 12TETか、他の調律体系か
- 綴り情報が保持されているか
- 上行・下行を区別するか
- compound intervalを保持するか
- 文脈を音程Module内で注釈するか、和声機能Moduleへ送るか
- targetが外部入力か、未解決ξとして残るか

### 選択

このModule単独では、文脈targetを最終選択しない。

```text
interval label
  ↓
target候補を自動生成しない
  ↓
和声機能Module / 声部進行Module / 音階・調Moduleへ送る
```

targetが入力済みの場合のみ、`Γ_motion` で運動を記述する。

## 7. 破断条件

このModuleが破断する、または未解決ξを残す条件。

- 半音距離は同じだが、綴りが異なる
- 綴りは同じだが、文脈が異なりtarget候補が変わる
- interval labelは同じだが、様式差で機能が変わる
- 12TET上の異名同音を同一物理音として扱っても、記譜・役割が分岐する
- targetが外部から与えられていないのに、解決方向を生成してしまう
- 音程ラベルを人間の基層知覚と同一視してしまう

禁止する短絡は次の通り。

```text
7 semitones = P5
6 semitones = tritone = fixed resolution
P5 / d6 = same because physical pitch pair is same
A4 / d5 → targetを自動生成
interval label = human perception
```

## 8. 未解決ξ

現時点で残す未解決領域。

- 音程ラベルが実際の聴取でどの程度区別されるか
- 綴り情報が知覚前の構造か、知覚後の記述か
- 文化・教育・様式による音程名の重み
- A4/d5、P5/d6などの機能差が成立する条件
- target候補を生成・選択する規則
- 競合するtarget候補の優先順位
- 具体音・オクターブ・配置への実現規則
- 音程ラベルと和声機能・声部進行の接続境界

これらは、和声機能Module、声部進行Module、記譜・綴りModuleへ分配して検証する。

## 9. 次の最小検証

次に必要な最小検証は、音程Moduleから音階・調Moduleまたは和声機能Moduleへの接続である。

```text
interval label
  + key / scale-degree role
  + learned tendency
  ↓
target候補の集合
  ↓
声部進行Moduleで具体実現
```

最小ケースは、13の構造を候補集合化すること。

| ケース | 検証したいこと |
|---|---|
| `F4-B4` in C major | A4ラベル、4→3・7→1注釈、target候補集合 |
| `E♯4-B4` in F♯ major | d5ラベル、7→1・4→3注釈、target候補集合 |

現状の13は既選択targetの分解で止まっている。次は、targetを一つに固定せず、候補集合として出し、どのModuleが選択するのかを分ける。

## 10. 現時点の短縮式

```text
音程・綴りModuleは、
半音距離を音程名へ直結せず、
綴り・generic interval・quality・文脈注釈を通して
learned側の分岐を保持する。

target選択はここで確定しない。
```
