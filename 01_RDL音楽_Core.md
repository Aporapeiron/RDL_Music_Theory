# RDL音楽_Core

*T3：応用層 / CREATE・MATH / DRAFT v0.2*
*依存：RDL_Core 新T0 / RDL_Modules 新T1*
*上位：RDL音楽理論*

---

## ■ 0. 役割

**RDL音楽_Coreは、音楽領域で共通して使用する最小の状態記述と操作を定める。**

調律、和声、旋律、リズム、楽式などの具体理論はCoreに含めない。

Coreは、

```text
何があるか
```

より、

```text
どの有限境界Bで
何が対象側に提示され
自己側の有限整合構造が何を解釈・予測・応答し
何が差として現れ
何が更新候補になり
なお何が未回収として残るか
```

を扱う。

---

## ■ 1. 音楽状態パケット

時刻 \(t\) における音楽検証用の状態パケットを、次のように置く。

\[
S^{music}_t
=
\langle
B_t,
SILN^{music}_{B_t,t},
W^{music}_{B_t,t},
M^{self}_{B_t,t},
EFP_t,
F_t,
E_{B_t,t},
H_{B_t,t},
\xi_{B_t,t}
\rangle
\]

ここでの \(S^{music}_t\) は、T0へ新しい基底量を追加するものではない。音楽Moduleが現在の観測・記述に使う検証用パケットである。

新T0/T1との責務は次のように分ける。

```text
対象側の有限構造:
  SILN_music / W_music / EFP

自己側の有限整合構造:
  M_B^device
  M_B^analysis
  M_B^listener
  M_B^learned
  M_B^context

検証・接続側:
  B
  Γ
  record
  fixture
```

したがって、Music対象そのものを直ちに `M_B` と呼ばない。対象側に現れている音列・和声・拍節・音色・文脈は、まず `SILN_music` または `W_music` として扱い、それをどの自己側 `M_B` が解釈・予測・応答するかを分ける。

---

## ■ 2. B：境界

\(B\) は、現在何を音楽的単位・基準として扱うかを決める有限境界である。

Bは固定的な容器ではなく、対象・範囲・尺度・語彙・差異を選び、境界を引く操作である。

例：

```text
B_tuning
B_pitch
B_interval
B_meter
B_phrase
B_form
B_timbre
```

複数のBは同時に存在できる。Bは固定されず、時間と目的によって変化する。

---

## ■ 3. SILN_music / W_music：対象側の有限関係構造

`SILN_music` は、現在の有限境界Bのもとで対象側に提示される音楽的関係構造である。

`W_music` は、そのSILN内で回収・比較される関係である。

```text
W_pitch
W_interval
W_harmony
W_time
W_accent
W_motif
W_timbre
W_form
```

同じ要素でも、Bが変わればWの意味・重みは変わりうる。

---

## ■ 4. M_B：自己側の有限整合構造

新T0に合わせ、Music Coreでは `M_B` を次のように扱う。

```text
M_B
=
Bのもとで現在の
解釈・予測・応答を拘束する
自己側の有限整合構造
```

これは対象側の音楽構造そのものではない。

```text
Music対象
  -> SILN_music / W_music

listener / analyzer / device側
  -> M_B^listener
  -> M_B^analysis
  -> M_B^device
```

例：

```text
M_B^device:
  検出器・レンダラ・分析器が入力を読むための有限整合構造

M_B^analysis:
  分析者が関係を比較・分類するための有限整合構造

M_B^listener:
  聴取者が音楽入力を解釈・予測・応答するための有限整合構造

M_B^learned:
  経験・文化・訓練によって形成された音楽的整合構造

M_B^context:
  現在の曲・場面・目的の中で立ち上がる一時的な整合構造
```

既存音楽理論は、対象そのものではなく、特定条件で `M_B^learned` または `M_B^analysis` として使える高圧縮の整合構造候補として扱う。

---

## ■ 5. F：M_Bを通した解釈・予測・応答

新T0に合わせ、Fは「実際に鳴った音」そのものではない。

```text
F(t)      = interp(M_B, EFP(t))
F'(t+Δ)   = interp(M_B, EFP(t+Δ))
E(t+Δ)    = Δ(F, F')
```

`EFP` は対象側から現在のM_Bへ渡される入力断面である。音楽側では、実際に提示された音・波形・譜面・MIDI・クリック・文脈などをEFP側に置く。

`F` は、M_Bを通して形成された解釈・予測・応答である。Fの中には、現在入力の解釈だけでなく、後続関係への予測も含まれうる。ただし、加法的な内部構造は仮定しない。必要な場合だけ `prediction_in_F = pred(F)` と補助的に書く。

音楽側では少なくとも次を分ける。

```text
EFP_phys / device output
  ↓ interp(M_B^device)
F_device

EFP_human / presented sound
  ↓ interp(M_B^listener)
F_listener

analysis input
  ↓ interp(M_B^analysis)
F_analysis
```

したがって、

```text
F_device ≠ F_listener
F_analysis ≠ F_listener
```

として扱う。波形検出上のF、分析上のF、聴覚上のF、音楽文脈上のFを混同しない。

---

## ■ 6. E：予測・後続解釈との不整合

\(E\) は、同一の更新前 \(M_B\) によって形成された \(F(t)\) と、同じ \(M_B\) で解釈した後続入力 \(F'\) との差である。

```text
same M_B + EFP(t)
          ↓
          F(t)
          includes current interpretation and possible prediction

same M_B + EFP(t+Δ)
          ↓
          F'(t+Δ)
          ↓
E(t+Δ) = Δ(F, F')
```

ここで \(F'\) は更新後の \(M_B'\) による説明ではない。更新前の同一 \(M_B\) を使うことで、Eを「更新後なら説明できる差」ではなく「現行M_Bで予測・解釈した関係と後続入力から読まれた関係の不整合」として保持する。

音楽的には、予想していた解決、拍位置、旋律継続、和声機能、音色の立ち上がり、motif回帰などと、実際に来た後続関係との不整合もEとして扱える。

Eの存在を直ちに誤りとはみなさない。Eは変奏・逸脱・新構造形成の入口にもなる。

---

## ■ 7. H：未吸収差の残存・蓄積・伝播

Hは、Eのうち現在のM_Bで吸収・解消されず、残存・蓄積・伝播した状態である。

```text
E
↓ current M_B absorption / resolution
H
```

したがって、Hは単なる時間的積分ではない。

```text
H ≠ Eの単純な時間的蓄積
H ≠ 音楽的緊張
H ≠ 不快
H ≠ 不協和
```

これらは必要なら別の音楽的派生量として定義する。

---

## ■ 8. θ / M_Δ：高負荷再編相

`M_Δ` は、一般的な遷移中間状態ではない。

新T0/T1に合わせ、Music Coreでは次の条件でだけ高負荷再編相として扱う。

```text
H ≥ θ
  ↓
M_Δ
  ↓
maintain / reorganize / update candidate
```

したがって、転調、拍節のずれ、音色変化、motif回帰などのMusic上のshiftが常にM_Δを通るとは限らない。

```text
Music shift
  ≠ 必ず M_Δ
```

M_Δを使う場合は、どのHがどのθを超え、何を維持し、何を再構成するのかを明示する。

---

## ■ 9. ξ：有限Bに伴う未回収関係

ξは、有限境界Bを引いたことに伴ってなお残る未回収関係である。

```text
∀B_finite:
  ξ(B) ≠ 0
```

ξは、Probe対象物でも未知の貯蔵庫でもない。ξそのものを直接操作して消去したり、既知の内容として確定したりしない。

```text
ξ ≠ mistake
ξ ≠ noise
ξ ≠ known hidden object
ξ ≠ storage
ξ ≠ probe target
```

Bを変えれば、以前のBで未回収だった関係の一部を新しいSILN/W/M_B候補として記述できることはある。しかし、そのことはξの最終消去を意味しない。

```text
change B / change relation configuration
  ↓
Probe_B(interaction)
  ↓
{Δ}_B
with ξ'(B) ≠ 0
```

---

## ■ 10. 状態遷移

音楽変化を、検証用には次のように扱う。

```text
S_music(t)
  ↓ interaction / EFP change / B change / Γ change
Probe_B(interaction)
  ↓
{Δ}_B, E, H, update candidate, ξ(B)
  ↓
S_music(t+Δ)
```

ただし、これはT0へ新しい基底フローを追加するものではない。Music側で、対象側SILN、自己側M_B、検証側B/Γ/recordを混同しないための操作表記である。

---

## ■ 11. preserve()

特定の関係または構造を保存条件として指定する。

```text
preserve(W_interval)
preserve(W_motif)
preserve(B_meter)
preserve(harmonic_profile)
```

preserveは、対象側SILN/Wに対する保存条件である場合と、自己側M_Bが維持する解釈条件である場合を分けて書く。

---

## ■ 12. change()

指定した関係を変更する。

```text
change(pitch)
change(rhythm)
change(W_interval)
change(attack envelope)
```

基本的な変奏は、

\[
Variation
=
Preserve(X)
+
Change(Y)
\]

として記述できる。ただし、一次介入と派生変化を分ける。

```text
primary intervention
  ≠ derived / entailed relational changes
```

例：

```text
duration change
  -> gap / overlap change

return start change
  -> return gap / phase change

transient noise change
  -> total rendered spectrum change
```

---

## ■ 13. stabilize() / destabilize()

`stabilize()` は、指定したM_Bによる解釈・予測・応答が維持されやすい方向へ関係を操作する。

`destabilize()` は、M_Bをただちに破壊せず、維持の確実性を低下させる。

```text
stabilize(M_B^context)
destabilize(M_B^listener hypothesis)
```

具体的方法は各Moduleが定義する。

---

## ■ 14. shift()

`shift()` は、B、対象側SILN/W、または自己側M_Bのいずれが変わるのかを分けて記述する。

```text
shift(B_A -> B_B)
shift(SILN_music_A -> SILN_music_B)
shift(M_B^context_A -> M_B^context_B)
```

ただし、shiftは常にM_Δではない。M_Δを記述するのは、Hがθを超え、高負荷再編相として扱う場合に限る。

転調、再拍節化、和声再解釈、音色変化は、この操作の具体例になりうる。

---

## ■ 15. blur()

複数のB、SILN候補、またはM_B候補が競合し、単一解釈へ収束しにくい状態を作る。

```text
blur(B_A, B_B)
blur(M_B^analysis_A, M_B^analysis_B)
```

曖昧さ自体を操作対象として扱うが、実聴取で曖昧に聞こえたこととは分ける。

---

## ■ 16. break()

現在のB、SILN/W、またはM_Bの維持を意図的に破断させる。

```text
break(W_interval)
break(M_B^context)
break(B_meter)
```

ただし、

```text
break ≠ random
```

である。何を壊し、何を保存するかを同時に記述する。

---

## ■ 17. redistribute_relation_configuration()

旧Coreの `redistribute(ξ)` は廃止する。

ξは操作対象ではない。操作できるのは、B、対象側関係配置、提示条件、Γ、または自己側M_B候補である。

```text
redistribute_relation_configuration(B, W, presentation, Γ)
  ↓
Probe_B(interaction)
  ↓
その有限Bで残るξを記述
```

調律、タイミング、音高、配置などの変更は、ξを直接配分し直すのではなく、関係配置を変えた後に再観測する。

---

## ■ 18. 分析の最小問

```text
B:
どの有限境界で見ているか。

SILN_music / W_music:
対象側にはどの関係が提示されているか。

M_B:
どの自己側構造が解釈・予測・応答を拘束しているか。

EFP / F:
何が入力断面で、どのM_Bを通して何として読まれたか。

E / H:
どの差が出て、何が未吸収として残ったか。

θ / M_Δ:
高負荷再編相を起動するほどの未吸収差か。

ξ:
この有限Bに伴って、どの未回収関係を記述するか。
```

---

## ■ 19. 生成の最小問

```text
Goal:
どこへ動きたいか。

Preserve:
対象側の何を残したいか。
M_B側のどの解釈・予測を残したいか。

Change:
対象側の何を変えたいか。
どのM_Bによる読みを変えたいか。

Transition:
B / SILN / W / M_B のどれをどう動かすか。

Listening:
structural prediction / perceptual hypothesis / actual listening observation を分けたか。
```

---

## ■ 20. Coreに入れないもの

以下はCoreへ固定しない。

```text
12平均律
長調・短調
機能和声
コードネーム
モード
対位法
ジャズ理論
特定拍子
特定楽式
特定ジャンル
特定の楽器音色
```

これらはすべて、必要に応じて接続される対象側SILN/W、または自己側 `M_B^learned / M_B^analysis` の候補である。

---

## ■ 21. Coreの破断条件

次の場合、Coreを更新する。

- 特定音楽文化を前提としなければ動作しない
- 平均律を外すと成立しない
- 和声を使わない音楽を扱えない
- 時間構造を持つ音楽を記述できない
- 音色・attackなど音事象内部の形成関係を扱えない
- 分析はできるが生成に利用できない
- 生成はできるが保存構造を説明できない
- M_Bを対象側構造と自己側整合構造のどちらにも使ってしまう
- FをEFPや実際の発音そのものと混同してしまう
- HをEの単純な時間積分として扱ってしまう
- ξをProbe対象物、未知の貯蔵庫、または操作対象として扱ってしまう
- shiftを常にM_Δとして扱ってしまう

---

## ■ 22. 最短圧縮

```text
RDL Music Core v0.2

TARGET SIDE
  EFP
  SILN_music
  W_music

SELF SIDE
  M_B^device
  M_B^analysis
  M_B^listener
  M_B^learned
  M_B^context

INTERPRETATION
  F = interp(M_B, EFP)
  F' = interp(M_B, EFP')
  E = Δ(F, F')
  H = unresolved / accumulated / propagated part of E under current M_B
  H ≥ θ -> M_Δ only when high-load reorganization is invoked

FINITE B
  ξ(B) remains nonzero
  ξ is described, not directly operated on

OPERATIONS
  preserve()
  change()
  stabilize()
  destabilize()
  shift()
  blur()
  break()
  redistribute_relation_configuration()

ANALYSIS
  What is target-side relation?
  Which M_B reads it?
  What is EFP and what is F?
  What remains unresolved as H?
  Which unrecovered relation is described as ξ under this finite B?

GENERATION
  What target-side relation is preserved?
  What relation is changed?
  Which M_B reading is expected to remain or change?
  What is only structural prediction?
  What still awaits actual listening?

Core
≠ tuning
≠ harmony
≠ genre
≠ Western music
≠ T2 runtime extraction
```

---

*v0.2：新T0/T1に合わせ、対象側SILN/Wと自己側M_Bを分離。FをEFPそのものではなく `interp(M_B, EFP)` とし、Hを未吸収差の残存・蓄積・伝播へ修正。ξを操作対象・未知貯蔵庫として扱わず、有限Bに伴う未回収関係として再定義。M_Δを高負荷再編相に限定し、旧 `redistribute(ξ)` を廃止して関係配置の変更と再観測へ置換。*

*v0.1：初版。RDL音楽理論の最小共通文法として、音楽状態 \(S_t\) と基本操作群を定義。特定調律・和声・文化圏に依存する知識をCore外へ置き、分析と生成の双方から利用可能な最小構造として仮設。*
