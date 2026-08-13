# 記譜・綴り｜Module計画

*状態：DRAFT v0.1*

## 0. 目的

音高、時間、綴り、調号、演奏指示を視覚的・慣習的記述として扱うModule境界を定める。

このModuleは、記譜を音響や知覚、演奏結果と同一視しない。記譜・綴りは、物理音高、12TETカテゴリー、音程ラベル、key context、演奏指示の間に置かれるlearnedな表記体系として扱う。

```text
physical / categorical / contextual relation
  ↓
B_notation + Γ_notation
  ↓
spelling / notation candidate
```

## 1. 参照する既知音楽理論

- `30_既知音楽理論参照/10_記譜と綴り.md`
- `30_既知音楽理論参照/01_音程.md`
- `20_構造抽出/物理音高から音楽ラベルへの分岐構造抽出版.md`

| 語彙 | このModuleでの扱い |
|---|---|
| staff / clef | 音高位置を読む枠組み |
| note value / rest | 時間長と無音の表記候補 |
| accidental | 音名変化の表記候補 |
| key signature | 調号・綴り慣習 |
| enharmonic spelling | 同じ12TET音高の異なる綴り候補 |
| articulation / dynamics | 演奏指示候補 |

## 2. 既存検証との接続

接続する既存構造。

```text
frequency ratio
  ↓ cents / 12TET category
same chromatic category
  + B_spelling
  ↓
different interval label
```

記譜・綴りModuleは、物理音高から音楽ラベルへの分岐のうち、`B_spelling` と表記選択を主に扱う。

## 3. B

| 境界 | 役割 |
|---|---|
| `B_notation_system` | 五線譜などの表記体系 |
| `B_clef` | 音高位置の読み枠 |
| `B_key_signature` | 調号・標準綴り |
| `B_spelling` | 音名・臨時記号・異名同音を保持する |
| `B_duration_notation` | 音価・休符表記 |
| `B_performance_marks` | articulation / dynamicsなど |
| `B_reading_context` | 調・声部・和声文脈による表記選択 |

## 4. Γ

| Γ | 入力 | 出力 |
|---|---|---|
| `Γ_pitch_to_spelling` | pitch category、key context | spelling候補 |
| `Γ_enharmonic_choice` | same chromatic category、context | 異名同音表記候補 |
| `Γ_interval_label_from_spelling` | spelling pair | generic interval / quality |
| `Γ_duration_notation` | duration候補 | note value / rest候補 |
| `Γ_staff_position` | clef、spelling、octave | 五線上の位置 |
| `Γ_performance_mark` | instruction候補 | 記号候補 |

## 5. M_B候補

| M_B候補 | 内容 |
|---|---|
| `spelling_candidate` | 音名・臨時記号候補 |
| `enharmonic_candidate_set` | 異名同音候補集合 |
| `notation_position_candidate` | 五線上の位置候補 |
| `duration_notation_candidate` | 音価・休符表記候補 |
| `key_signature_record` | 調号記録 |
| `performance_mark_candidate` | 発音・強弱指示候補 |

## 6. 候補生成・制約・選択

- 12TETカテゴリーから複数のspelling候補を生成する
- key contextやvoice contextで表記候補を制約する
- spelling pairから音程ラベルを分岐させる
- duration候補をnote value / restへ写す
- articulation / dynamicsは音響結果ではなく指示候補として保持する

このModule単独では、実際の演奏音響や聴取結果を確定しない。

## 7. 破断条件

- 同じ12TET音高が複数の綴りへ分岐する
- 調号と臨時記号が文脈上ずれる
- 記譜上の休符と音響上の無音が一致しない
- articulation / dynamicsから実音響を一意に導く
- 記譜を作曲者意図や聴取知覚と同一視する

禁止する短絡。

```text
same pitch class = same spelling
notation = sound
notation = performance
key signature = actual pitch collection
enharmonic equivalence = same learned relation
```

## 8. 未解決ξ

- 綴り選択の原理
- 調号、臨時記号、和声文脈の優先順位
- 記譜と実演の差
- dynamics / articulationの音響実現
- 読譜者の学習・文化差
- 記譜外の演奏慣習

## 9. 次の最小検証

```text
same chromatic category
  + different spelling
  ↓
different interval label / notation role
```

最小ケースは、既存の `C→G` と `C→A𝄫` を記譜・綴りModule側から読み直し、同じ12TET音高でもnotation candidateが別になることを確認する。

## 10. 現時点の短縮式

```text
記譜・綴りModuleは、
音響や知覚を表記へ直結せず、
spelling・notation・duration・instructionを
learnedな表記候補として扱う。
```
