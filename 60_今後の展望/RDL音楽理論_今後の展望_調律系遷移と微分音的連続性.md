# RDL音楽理論_今後の展望_調律系遷移と微分音的連続性

文書状態: 展望 / ξ候補  
位置づけ: RDL_Music_Theory 将来検討用  
作成日: 2026-08-28  

---

## 0. この文書の目的

この文書は、現在のRDL音楽理論で進めている音高調律、音程、和声機能、声部進行、リズム拍節、文脈、複数解釈保持、policy boundary の検証から見えてきた今後の応用可能性を保存するための展望文書である。

ここで扱う内容は、現時点で中核仕様として採用するものではない。

したがって、

> 今後検査する価値がある ξ 候補

として保持する。

---

## 1. 現在までに見えている入口

現在の検証では、少なくとも次の非同一性が重要になっている。

```text
frequency ratio
≠ cents coordinate
≠ tuning category
≠ interval spelling
≠ interval label
≠ harmonic function
```

また、Module間の接続についても、

```text
前段の出力
≠ 後段の意味確定
```

が維持されている。

例として、

```text
音高調律
→ 音程候補を制約する

しかし

音高調律
≠ 音程名の一意決定
```

がある。

同様に、

```text
same evidence
≠ same prediction
```

であり、同じ evidence bundle から複数の音楽的解釈が残り得る。

---

## 2. 展望A: 調律系遷移

将来的には、単一の調律系内部だけでなく、

```text
12TET
↓
tuning-system transition
↓
Just Intonation
```

のような、調律系そのものの遷移を扱える可能性がある。

ここでは「転調」という語はキー変更と混線するため、暫定的に

> 調律系遷移  
> tuning-system transition

として扱う。

重要なのは、音楽的関係と物理的実現を分離することである。

```text
musical relation
↓
interval / harmonic / spelling relation
↓
tuning policy
├─ 12TET realization
└─ JI realization
```

この構造が成立するなら、同じ音楽的関係を保持したまま、物理的ピッチ実現だけを変更できる。

---

## 3. 展望B: 動的純正律

純正律は固定した周波数表としてではなく、文脈に応じて再計算される動的系として扱える可能性がある。

```text
harmonic context
↓
candidate pure ratios
↓
voice-leading constraint
+
common-tone retention
+
previous pitch state
+
tuning policy
↓
selected frequency realization
```

この場合、

```text
harmonically pure
≠
smoothest voice leading
≠
smallest pitch displacement
≠
best continuity from previous tuning
```

となり得る。

したがって、単一の「最良調律」を求める問題ではなく、複数Module間の制約競合として扱う。

---

## 4. 展望C: 微分音化しても自然に聞こえる遷移

重要な候補として、

> 物理的には微分音化しているにもかかわらず、音楽的には自然な連続として知覚される遷移

がある。

暫定構造は次のようになる。

```text
current tuning state
↓
context change
↓
tuning policy change
↓
microtonal displacement
↓
cross-Module relation preservation
↓
perceptual continuity candidate
```

ここで検査したいのは、

```text
pitch displacement magnitude
≠
perceptual discontinuity magnitude
```

である。

例えば、ある音が12TET位置から十数cent移動しても、

- 和声機能が保たれる
- 声部進行が滑らか
- 共通音が保持される
- 文脈的期待と整合する

なら、知覚上は断絶として感じられない可能性がある。

---

## 5. 「自然さ」を単一値にしない

この展望では「自然さ」を一つの数値へ早期圧縮しない。

暫定的には、

```text
perceptual continuity candidate
=
pitch-motion continuity
+
voice-leading continuity
+
harmonic continuity
+
common-tone retention
+
rhythmic placement
+
context consistency
```

のような複数関係の束として扱う。

ただし、これは現時点では説明用の候補であり、Core primitive や確定式ではない。

---

## 6. 展望D: same musical identity / different physical realization

現在の

```text
same evidence
→ multiple interpretations
→ policy selection
```

という構造は、将来的に、

```text
same musical identity
→ multiple physical pitch realizations
→ tuning policy selection
```

へ拡張できる可能性がある。

つまり、

```text
同じ音程名
同じ和声機能
同じ声部上の役割
```

を保ちながら、

```text
physical pitch realization
```

だけが変化する構造である。

これは平均律・純正律・微分音的実現を一つの関係ネットワーク上で比較する入口になる。

---

## 7. 展望E: 作曲・演奏への応用

この系が成立した場合、RDL音楽理論は分析だけでなく、生成・演奏制御へ接続できる可能性がある。

候補として、

- 文脈依存の自動調律
- 声部進行を保存した純正化
- 微分音への自然な遷移
- 演奏中の動的tuning policy切替
- 複数調律候補を保持する作曲支援
- 調律変更による和声再解釈
- listener / performer / instrumentごとのB差を使った調律比較

などが考えられる。

ただし、これらは現時点ではすべて展望である。

---

## 8. 将来の検査候補

今後、実験化する場合は次の順序が考えられる。

```text
1. 12TET内で関係保存を確認
↓
2. 同一和音をJIへ再実現
↓
3. voice leadingを維持した動的再調律
↓
4. tuning policy切替
↓
5. microtonal displacement発生
↓
6. 音楽的関係がどこまで保持されるか確認
↓
7. 知覚的連続性候補を記録
↓
8. 破断点を探索
```

重要なのは、

> 何cent動いたら不自然か

だけを見るのではなく、

> どの関係を保存すると、どこまで物理ピッチが変化しても音楽的連続性が残るか

を見ることである。

---

## 9. 停止線

この展望を扱う際、以下を自動同一視しない。

```text
12TET
≠ 音楽そのもの

Just Intonation
≠ より正しい音楽

pure ratio
≠ perceptually optimal

microtonal
≠ dissonant

small pitch displacement
≠ perceptually continuous

large pitch displacement
≠ perceptually discontinuous

tuning transition
≠ key modulation

selected tuning policy
≠ alternative tuning erased
```

また、

```text
調律系遷移が可能
≠ 常に自然に聞こえる
```

である。

---

## 10. 現時点での位置づけ

本展望は、

```text
現在のMusic側検証
↓
Module間相互作用
↓
複数解釈保持
↓
policy boundary
↓
今後のξ候補
    ├─ tuning-system transition
    ├─ dynamic just intonation
    ├─ microtonal continuity
    └─ performance / composition application
```

として保持する。

現段階では本線を変更しない。

まず現在進行中の、

```text
調律
→ 音程
→ 和声機能
→ 声部進行 / 文脈
→ 複数解釈
```

の構造を十分に検査し、その後の応用候補として再接続する。

---

## 暫定要約

```text
物理的ピッチが変わっても
音楽的関係は同じであり得る。

音楽的関係が同じでも
物理的ピッチ実現は複数あり得る。

その間を調律policyが選択する。

そして、
微分音化したこと自体ではなく、
何の関係が保存され、
何が破断したかを見る。
```
