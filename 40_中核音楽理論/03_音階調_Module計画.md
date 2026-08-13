# 音階・調｜Module計画

*状態：DRAFT v0.1*

## 0. 目的

音程・綴りModuleで得た音名・音程ラベル・文脈注釈を受け取り、音階、調、音度役割をRDL音楽側のModule境界として整理する。

このModuleは、音階名や調名を音楽構造の最終説明にしない。音階は音高集合・順序・間隔構造のlearned記述、調は主音・音階・綴り慣習・中心性・和声文脈を含む文脈境界として扱う。

```text
spelled pitch / interval label
  ↓
B_key_scale + Γ_scale_degree
  ↓
scale degree / key-context候補
  ↓
和声機能 / 声部進行 / 旋律Module
```

ここでは、調性感、解決感、主音中心の知覚を完成モデルとして置かない。

## 1. 参照する既知音楽理論

- `30_既知音楽理論参照/03_音階と調.md`
- `20_構造抽出/音程実現_候補生成と制約の構造抽出版.md`
- `10_検証/13_音程分解_解決候補の文脈分解_最小実験.md`
- `10_検証/14_音程分解_音度から具体音への実現_最小実験.md`

既知音楽理論側では、次の語彙が参照される。

| 語彙 | このModuleでの扱い |
|---|---|
| major scale | 間隔構造と綴りを持つ音階体系候補 |
| natural minor | 短音階の代表的体系候補 |
| harmonic minor | 第7音変化を含む短音階候補 |
| melodic minor | 上行・下行で異なる候補を持つ短音階記述 |
| key signature | 調号としての綴り慣習 |
| scale degree | 主音から数える役割記述 |

これらは既知理論の辞書であり、RDL Coreへ直接置かない。

## 2. 既存検証との接続

主に接続する検証は次の通り。

| 検証 | 接続内容 |
|---|---|
| `13_音程分解_解決候補の文脈分解_最小実験.md` | 調性文脈、音度役割、learned tendency、既選択targetの分解 |
| `14_音程分解_音度から具体音への実現_最小実験.md` | 目標音度から具体音への候補生成・範囲投影・選択の分離 |
| `15_音程分解_実現制約の競合と候補消滅_最小実験.md` | 音度実現で候補が消える条件 |
| `20_構造抽出/音程実現_候補生成と制約の構造抽出版.md` | target degreeとconcrete pitchの非同一性 |

既存検証から受け取る最小構造は次の通り。

```text
key context
  ↓
scale degree role
  ↓
learned tendency
  ↓
target degree
  ↓ B_realization
concrete pitch candidates
```

このModuleは、主に `key context → scale degree role` と `scale degree role → 後続Moduleへの注釈` の境界を扱う。

## 3. B

このModuleの境界候補。

| 境界 | 役割 |
|---|---|
| `B_tonic` | 主音候補を置く |
| `B_scale_pattern` | major / minor等の間隔構造を置く |
| `B_spelling_policy` | 調号・綴り慣習を保持する |
| `B_degree_role` | 音度番号と機能的役割を注釈する |
| `B_mode_variant` | natural / harmonic / melodicなどの変種を切り替える |
| `B_direction` | melodic minorなどで上行・下行を区別する |
| `B_context_scope` | どの範囲を同一調文脈として扱うか |

`B_tonic` と `B_scale_pattern` を置いても、和声機能や旋律選択は自動的には決まらない。

```text
key = C major
  ≠ 全ての音の機能が確定
  ≠ 次の和音が確定
  ≠ 具体音配置が確定
```

## 4. Γ

このModuleで使う関係抽出・変換規則の候補。

| Γ | 入力 | 出力 |
|---|---|---|
| `Γ_scale_pattern` | tonic、scale pattern | scale pitch-class候補 |
| `Γ_key_signature` | key候補 | 調号・標準綴り候補 |
| `Γ_scale_degree` | spelled pitch、key context | scale degree |
| `Γ_degree_to_spelling` | key context、scale degree | 綴り付き音名候補 |
| `Γ_degree_role` | scale degree、context | tonic/leading tone等の役割注釈 |
| `Γ_mode_variant` | mode、direction、context | 変化音・上行下行候補 |

これらは、音階・調の記述規則であり、調性感や知覚上の中心性そのものではない。

## 5. M_B候補

このModuleのM_B候補。

| M_B候補 | 内容 |
|---|---|
| `scale_pattern_candidate` | 全全半全全全半などの間隔構造候補 |
| `key_context_candidate` | tonic + scale pattern + spelling policyの束 |
| `degree_role_candidate` | 1〜7度と役割注釈 |
| `mode_variant_candidate` | harmonic minor / melodic minor等の変種候補 |
| `key_signature_record` | 調号・綴り慣習の記録 |
| `target_degree_candidate` | 後続Moduleへ渡す目標音度候補 |

音階・調のM_B候補は、物理音高集合ではなく、learnedな文脈境界として扱う。

```text
pitch collection
  ≠ key context
  ≠ tonal function
  ≠ concrete realization
```

## 6. 候補生成・制約・選択

### 候補生成

- tonic候補からscale pattern候補を生成する
- key候補から調号・綴り候補を生成する
- spelled pitchをscale degreeへ写す
- scale degreeから役割注釈を生成する
- 文脈に応じてtarget degree候補を生成する

### 制約

- 調号と実音の一致・不一致
- mode variantの選択
- 上行・下行の扱い
- 臨時記号の許容
- 転調・借用和音・一時的中心の扱い
- 文脈範囲をどこまで同一keyとみなすか

### 選択

このModule単独では、和声進行や旋律の次音を選ばない。選択は後続Moduleへ渡す。

```text
degree_role_candidate
  ↓
和声機能Module
声部進行Module
旋律Module
```

具体音が必要な場合は、実現Module側で `B_realization`、`Γ_spelling`、`Γ_select` を明示する。

## 7. 破断条件

このModuleが破断する、または未解決ξを残す条件。

- 同じ音高集合が複数のkeyとして読める
- 調号と実際の臨時記号が一致しない
- tonic候補が複数立つ
- natural / harmonic / melodic minorの選択が文脈依存になる
- 転調、一時的 tonicization、借用和音で単一key境界が崩れる
- scale degreeはあるが、具体音・オクターブ・声部配置が決まらない
- 調性感を物理比または音階集合から直接導いてしまう

禁止する短絡は次の通り。

```text
C major scale = C major key context
key signature = actual sounding collection
scale degree = concrete pitch
leading tone = always resolves
tonic = human perceptual center as completed model
```

## 8. 未解決ξ

現時点で残す未解決領域。

- tonic候補をどう選ぶか
- 調性感・中心感の成立条件
- 転調境界の検出
- 借用和音や旋法混合の扱い
- mode variantの選択原理
- 調号、実音、綴り慣習のズレ
- scale degreeからtarget degreeを生成する規則
- target degree候補の競合・優先順位
- 文化差・様式差・学習履歴
- 基層知覚としての中心性をどこまで仮設できるか

これらは、音階・調Moduleだけで閉じず、和声機能Module、旋律Module、形式Moduleへ渡す。

## 9. 次の最小検証

次に必要な最小検証は、同じ音高または同じ音高集合が、key contextによって異なるscale degreeへ写ることの確認である。

```text
same spelled / sounding pitch
  + different key context
  ↓
different scale degree role
```

最小ケース。

| ケース | 検証したいこと |
|---|---|
| `B` in C major | `7` / leading-tone候補として注釈される |
| `B` in G major | `3` / chord-tone候補として注釈される |
| `F` in C major | `4` として注釈される |
| `F#` in G major | `7` として注釈される |

この検証により、音名・実音だけではscale degree roleが確定せず、key contextがModule境界として必要であることを確認する。

## 10. 現時点の短縮式

```text
音階・調Moduleは、
音高集合を調性感へ直結せず、
tonic・scale pattern・spelling policy・degree roleを
文脈境界として保持する。

scale degreeは具体音でも、
和声機能そのものでもない。
```
