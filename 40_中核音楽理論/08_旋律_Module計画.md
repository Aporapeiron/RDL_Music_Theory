# 旋律｜Module計画

*状態：DRAFT v0.1*

## 0. 目的

音高・音程・リズム・和声文脈を時間列として束ね、旋律として扱うためのModule境界を定める。

このModuleは、音程列から旋律の良さや自然さを一意に導かない。旋律は、音高列、リズム、輪郭、反復、フレーズ、和声文脈、履歴によって立ち上がる候補構造として扱う。

```text
pitch / rhythm / harmonic context
  ↓
B_melody + Γ_melodic_relation
  ↓
melodic candidate / motif / phrase候補
```

## 1. 参照する既知音楽理論

- `30_既知音楽理論参照/08_旋律.md`
- `40_中核音楽理論/02_音程_Module計画.md`
- `40_中核音楽理論/07_リズム拍節_Module計画.md`
- `40_中核音楽理論/05_和声機能_Module計画.md`

| 語彙 | このModuleでの扱い |
|---|---|
| conjunct / disjunct motion | 音程列上の局所運動ラベル |
| contour | 上昇・下降・反復などの輪郭候補 |
| motif | 反復・変形される短いまとまり候補 |
| phrase | 終止・呼吸・まとまり候補 |
| non-chord tone | 和声文脈内での音の役割注釈候補 |

## 2. 既存検証との接続

現時点では、旋律専用検証は未着手である。既存Moduleから次を受け取る。

```text
音程Module       → interval / contourの局所材料
リズムModule     → time position / duration
和声機能Module   → chord tone / non-chord tone注釈候補
声部進行Module   → concrete pitch transition
```

## 3. B

| 境界 | 役割 |
|---|---|
| `B_melodic_span` | 旋律として読む時間範囲 |
| `B_pitch_sequence` | 音高列を保持する |
| `B_rhythm_sequence` | 時間位置・長さ列を保持する |
| `B_harmonic_context` | 和声・key contextを注釈する |
| `B_repetition_scope` | 反復・変形として比較する範囲 |
| `B_phrase_boundary` | フレーズ境界候補を保持する |

## 4. Γ

| Γ | 入力 | 出力 |
|---|---|---|
| `Γ_interval_sequence` | 音高列 | 音程列 |
| `Γ_contour` | 音高列 | 上昇・下降・反復輪郭 |
| `Γ_motif_match` | 部分列同士 | 反復・変形候補 |
| `Γ_phrase_boundary` | 旋律列、休止、終止候補 | phrase候補 |
| `Γ_non_chord_tone` | melody note、chord context | non-chord tone注釈候補 |

## 5. M_B候補

| M_B候補 | 内容 |
|---|---|
| `melodic_sequence_candidate` | 音高・リズムを含む旋律列候補 |
| `contour_candidate` | 輪郭候補 |
| `motif_candidate` | 反復・変形される短いまとまり |
| `phrase_candidate` | フレーズ境界を持つまとまり |
| `non_chord_tone_annotation` | 和声文脈内の非和声音注釈 |

## 6. 候補生成・制約・選択

- 音高列から音程列を生成する
- 時間列からリズム輪郭を生成する
- 部分列比較からmotif候補を生成する
- 和声文脈からchord tone / non-chord tone候補を注釈する
- phrase境界は休止、長音、終止、反復などの複数条件から候補化する

このModule単独では、旋律の良し悪しや次音を最終選択しない。

## 7. 破断条件

- 同じ音程列でもリズムや和声文脈で旋律機能が変わる
- 同じ輪郭でもmotifとして認識されるとは限らない
- non-chord tone分類が和声文脈に依存する
- phrase境界が記譜、演奏、聴取で一致しない
- 旋律の自然さを音程幅だけで説明してしまう

## 8. 未解決ξ

- motif抽出の条件
- phrase境界の成立条件
- 記憶・反復・期待の関与
- 和声と旋律の優先順位
- 楽器・声域・歌いやすさ
- 文化差・様式差
- 聴取上のまとまりと記譜上のまとまりの差

## 9. 次の最小検証

```text
same pitch contour
  + different rhythm
  ↓
different melodic candidate
```

最小ケースは、同じ `C-D-E` でも、均等リズムと長短リズムでphrase / motif候補が変わるかを見る。

## 10. 現時点の短縮式

```text
旋律Moduleは、
音程列を旋律へ直結せず、
音高・リズム・和声文脈・反復・境界を束ねて
melodic candidateを扱う。
```
