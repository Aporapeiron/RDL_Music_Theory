# 和音｜Module計画

*状態：DRAFT v0.1*

## 0. 目的

音階・調Moduleから渡されたkey context、scale degree、spelling policyを受け取り、複数音の同時的・和声的まとまりを候補集合として扱うModule境界を定める。

このModuleは、音集合から和音名を一意に決めない。同じ音集合でも、root、bass、配置、綴り、履歴、後続関係によって複数の和音M_B候補が成立しうる。

```text
key context / pitch collection
  ↓
B_chord + Γ_chord_candidate
  ↓
chord candidate set
  ↓
和声機能 / 声部進行 / 形式Module
```

和音名は圧縮ラベルであり、次の進行・機能・聴取上の安定を単独では決めない。

## 1. 参照する既知音楽理論

- `30_既知音楽理論参照/04_和音.md`
- `10_検証/01_C6とAm7.md`
- `10_検証/02_C_major_候補集合と制約.md`
- `10_検証/05_Bから候補空間生成_最小実験.md`

既知音楽理論側では、次の語彙が参照される。

| 語彙 | このModuleでの扱い |
|---|---|
| triad | root, third, fifthからなる候補生成規則 |
| major / minor / diminished / augmented | 和音種候補 |
| seventh chord | 七度を含む拡張候補 |
| inversion | bassに置かれる構成音による配置分類 |
| extension / alteration | 9th, 11th, 13thや変化音を含む候補拡張 |

これらは既知音楽理論の辞書であり、RDL Coreへ直接置かない。

## 2. 既存検証との接続

主に接続する検証は次の通り。

| 検証 | 接続内容 |
|---|---|
| `01_C6とAm7.md` | 同じ音集合がbass、配置、履歴、文脈で別M_Bへ分岐する |
| `02_C_major_候補集合と制約.md` | C major境界、候補空間、保存条件、目標条件による候補集合 |
| `05_Bから候補空間生成_最小実験.md` | BとM_Bだけでは候補空間が決まらず、Γが必要であること |

既存検証から受け取る最小構造は次の通り。

```text
B + M_B
  ↓ Γ_chord_candidate
C(B, M_B; Γ)
  ↓ R
C'
```

また、同一音集合問題は次のように圧縮できる。

```text
{C, E, G, A}
  + B_bass = C
  + B_context = C中心
  ↓
C6候補

{C, E, G, A}
  + B_bass = A
  + B_context = A中心
  ↓
Am7候補
```

## 3. B

このModuleの境界候補。

| 境界 | 役割 |
|---|---|
| `B_pitch_collection` | 同時音・候補音集合を保持する |
| `B_key_context` | key / scale / degree文脈を保持する |
| `B_root_candidate` | root候補をどこから取るかを指定する |
| `B_bass` | 実際の低音、最低音、ペダルを保持する |
| `B_voicing` | 音域、重複、密集/開離配置を保持する |
| `B_spelling` | 異名同音を区別する綴り情報を保持する |
| `B_time_context` | 持続、拍位置、直前・直後関係を保持する |
| `B_generation_scope` | triadだけか、seventh、extensionまで含むかを切る |

`B_pitch_collection` だけでは、C6とAm7のような分岐を回収できない。

```text
same pitch collection
  ≠ same bass relation
  ≠ same root candidate
  ≠ same chord label
  ≠ same M_B
```

## 4. Γ

このModuleで使う候補生成・関係抽出規則。

| Γ | 入力 | 出力 |
|---|---|---|
| `Γ_triad_candidate` | root候補、quality集合 | triad候補 |
| `Γ_seventh_candidate` | triad候補、七度候補 | seventh chord候補 |
| `Γ_diatonic_closure` | key context、candidate tones | key内に閉じる候補 |
| `Γ_root_inference` | pitch collection、spelling、context | root候補 |
| `Γ_bass_relation` | bass、upper tones | inversion / bass relation |
| `Γ_chord_label` | root、quality、extension、bass | chord label候補 |
| `Γ_candidate_filter` | 候補集合、保存条件、target条件 | 制約後候補 |

`Γ_chord_label` はラベル生成規則であり、機能や次進行を生成する規則ではない。

## 5. M_B候補

このModuleのM_B候補。

| M_B候補 | 内容 |
|---|---|
| `pitch_collection_candidate` | 同時的に現れる音集合 |
| `rooted_chord_candidate` | rootを持つ和音候補 |
| `bass_weighted_candidate` | bassを基準にした和音候補 |
| `voicing_candidate` | 配置・重複・音域を含む候補 |
| `diatonic_chord_candidate_set` | key内で生成された和音候補集合 |
| `ambiguous_chord_candidate_set` | 複数ラベルが並存する候補集合 |
| `chord_transition_record` | 直前・直後関係を含む履歴記録 |

同じ音集合に対して複数のM_B候補が立つ場合は、曖昧さとして保持する。

```text
ambiguous
  ≠ error
  ≠ no_candidate
```

## 6. 候補生成・制約・選択

### 候補生成

- key contextからdiatonic triad候補を生成する
- pitch collectionからroot候補を生成する
- bass relationから転回・slash chord候補を生成する
- seventh / extension / alteration候補を拡張する
- 同じ音集合に対する複数ラベル候補を保持する

### 制約

- key内に閉じるか
- triad / seventh / extensionのどこまで候補化するか
- root候補をscale内に限定するか
- bassを強い基準として扱うか
- voicingや音域を候補判定に含めるか
- 直前・直後の文脈を含めるか

### 選択

このModule単独では、和声機能や次の和音を最終選択しない。

```text
chord candidate set
  ↓
和声機能Module
声部進行Module
形式Module
```

候補が一つに絞られた場合も、それは現在の `B / M_B / Γ / R` 内での局所解である。

```text
locally_resolved
  ≠ 音楽的に唯一正しい
```

## 7. 破断条件

このModuleが破断する、または未解決ξを残す条件。

- 音集合は同じだがroot候補が複数ある
- bassによって和音名候補が変わる
- 同じ和音名でもvoicingや履歴が変わる
- key外音、alteration、borrowed chordでdiatonic closureが破れる
- Γを指定しないため候補生成規則が不足する
- 候補生成後に制約で空集合になる
- 和音名から機能や次進行を自動生成してしまう

禁止する短絡は次の通り。

```text
pitch collection = chord identity
C-E-G-A = C6 or Am7として一意確定
diatonic triads = C majorそのもの
chord label = harmonic function
chord label = next chord generator
bass = always root
```

## 8. 未解決ξ

現時点で残す未解決領域。

- root候補の選択原理
- bassとrootの重みづけ
- 転回形と独立したslash chordの境界
- extension / alterationの候補生成範囲
- 同じ音集合の曖昧さをいつ収束させるか
- voicing、音域、楽器、音色が和音候補へ与える影響
- 履歴・反復・後続関係によるM_B安定化
- 和音名と和声機能の接続条件
- 実際の聴取で同じ和音候補がどう分離・融合されるか

これらは、和声機能Module、声部進行Module、物理・基層側の後続検証へ渡す。

## 9. 次の最小検証

次に必要な最小検証は、和音Moduleから和声機能Moduleへの受け渡しである。

```text
same chord candidate
  + different key / degree context
  ↓
different functional annotation候補
```

最小ケース。

| ケース | 検証したいこと |
|---|---|
| `G-B-D` in C major | V候補として注釈される |
| `G-B-D` in G major | I候補として注釈される |
| `{C,E,G,A}` with C bass | C6候補として保持される |
| `{C,E,G,A}` with A bass | Am7候補として保持される |

この検証により、和音名が機能を単独で決めず、key / degree / contextが別Module境界として必要であることを確認する。

## 10. 現時点の短縮式

```text
和音Moduleは、
音集合を和音名へ直結せず、
root・bass・voicing・spelling・履歴・生成規則を通して
候補集合として保持する。

和音名は機能でも、
次進行の生成器でもない。
```
