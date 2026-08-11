# RDL音楽_Core

*T4：応用層 / CREATE・MATH / DRAFT v0.1*  
*依存：RDL_Core / SILN_動態*  
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
何が保たれ
何が変わり
どこへ移るか
```

を扱う。

---

## ■ 1. 音楽状態

時刻 \(t\) における音楽状態を、

\[
S_t
=
\langle
B_t,
M_{B_t,t},
W_{B_t,t},
F_t,
E_{B_t,t},
H_{B_t,t},
\xi_{B_t,t}
\rangle
\]

と仮設する。

ここで、\(M\)、\(W\)、\(E\)、\(H\)、\(\xi\)は、現在の境界\(B_t\)に依存する。
以下では、B依存と時刻が文脈上自明な場合、記法を簡略化して\(M_B\)、\(W\)、\(E\)、\(H\)、\(\xi\)と書く。

---

## ■ 2. B：境界

\(B\) は、現在何を音楽的単位・基準として扱うかを決める。

例：

```text
B_tuning
B_pitch
B_key
B_meter
B_phrase
B_form
```

複数のBは同時に存在できる。

Bは固定されず、時間と目的によって変化する。

---

## ■ 3. M_B：安定構造

\(M_B\) は、現在のBにおいて同じものとして維持されている関係構造である。

例：

```text
M_tuning
M_key
M_chord
M_meter
M_motif
M_phrase
```

音そのものではなく、関係の維持を中心に見る。

---

## ■ 4. W_ij：関係

\(W_{ij}\) は、音楽要素間の関係を表す。

```text
W_pitch
W_interval
W_harmony
W_time
W_accent
W_motif
W_form
```

同じ要素でも、Bが変わればWの意味・重みは変わりうる。

---

## ■ 5. F：実際に現れた作用

\(F\) は、現在実際に観測された音楽作用である。

```text
発音
休止
音高変化
アクセント
音色変化
リズム変化
```

理論上予定された音ではなく、実際に現れたものを優先する。

---

## ■ 6. E：現在構造との差

\(E\) は、現在のM_Bから維持・予測される関係とFとの差である。

```text
predicted / inertial relation
          ↓
          E
          ↑
observed F
```

Eの存在を、直ちに誤りとはみなさない。

Eは変奏・逸脱・新構造形成の入口にもなる。

---

## ■ 7. H：蓄積

HはEの時間的蓄積として扱う。

ただし、

```text
H ≠ 音楽的緊張
H ≠ 不快
H ≠ 不協和
```

とする。

これらは必要なら別の音楽的派生量として定義する。

---

## ■ 8. ξ：未回収成分

ξは、現在のBとM_Bでは十分に記述できない成分である。

```text
ξ ≠ mistake
ξ ≠ noise
```

別のBを引いたとき、

```text
ξ
 ↓
new B
 ↓
new M_B
```

として安定構造になる可能性を常に残す。

---

## ■ 9. 状態遷移

音楽変化を、

\[
S_t
\rightarrow
\Delta
\rightarrow
S_{t+1}
\]

として扱う。

Δによって、

```text
B_t
M_{B_t,t}
W_{B_t,t}
F_t
E_{B_t,t}
H_{B_t,t}
ξ_{B_t,t}
```

の一部または複数が変化する。

---

## ■ 10. preserve()

特定の関係または構造を保存する。

```text
preserve(W_interval)
preserve(M_motif)
preserve(B_meter)
```

音楽的同一性を扱う基本操作である。

---

## ■ 11. change()

指定した関係を変更する。

```text
change(pitch)
change(rhythm)
change(W_interval)
change(orchestration)
```

基本的な変奏は、

\[
Variation
=
Preserve(X)
+
Change(Y)
\]

として記述できる。

---

## ■ 12. stabilize()

指定したM_Bが維持されやすい方向へ関係を操作する。

```text
stabilize(M_B)
```

反復、中心の強化、既知関係への回帰などが具体操作候補になりうる。

具体的方法は各モジュールが定義する。

---

## ■ 13. destabilize()

M_Bをただちに破壊せず、維持の確実性を低下させる。

```text
destabilize(M_B)
```

予測からの逸脱、中心の弱化、競合関係の導入などが候補になる。

具体的方法は各モジュールへ委ねる。

---

## ■ 14. shift()

現在のBまたはM_Bを、別の状態へ移行させる。

```text
shift(B_A → B_B)
```

概念的には、

```text
B_A ─────────→ B_B
 │               │
 M_{B_A} ─→ M_Δ ─→ M_{B_B}
```

となる。\(M_\Delta\)は、Bそのものではなく、現在の安定構造が再編される遷移相である。
したがって、Bの変更とMの相転移を同一視しない。

転調は、この操作の一例として扱える。

---

## ■ 15. blur()

複数のBまたはMが競合し、単一解釈へ収束しにくい状態を作る。

```text
blur(B_A, B_B)
```

曖昧さ自体を操作対象として扱う。

---

## ■ 16. break()

現在のBまたはM_Bの維持を意図的に破断させる。

```text
break(M)
break(B)
```

ただし、

```text
break ≠ random
```

である。

何を壊し、何を保存するかを同時に記述する。

---

## ■ 17. redistribute()

消去できない差異・ずれ・自由度の配置を変更する。

```text
redistribute(ξ)
```

調律、タイミング、音高、配置など複数領域への利用可能性を保持する。

---

## ■ 18. 分析の最小問

```text
B：
何を基準としているか。

M：
何が現在保たれているか。

W：
どの関係が重要か。

Δ：
何が変わったか。

Preserve：
何が変わらなかったか。

E/H：
現在構造とのずれはどう動いたか。

ξ：
現在の記述では何が残るか。
```

---

## ■ 19. 生成の最小問

```text
Goal：
どこへ動きたいか。

Preserve：
何を残したいか。

Change：
何を変えたいか。

Transition：
どのように移りたいか。

Target：
何を新たに安定させたいか。
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
```

これらはすべて、必要に応じて接続される音楽M_Bである。

---

## ■ 21. Coreの破断条件

次の場合、Coreを更新する。

- 特定音楽文化を前提としなければ動作しない
- 平均律を外すと成立しない
- 和声を使わない音楽を扱えない
- 時間構造を持つ音楽を記述できない
- 分析はできるが生成に利用できない
- 生成はできるが保存構造を説明できない
- 何でも説明できるだけで、操作上の差が出ない

---

## ■ 22. 最短圧縮

```text
RDL Music Core

STATE
S_t = <B_t,M_{B_t,t},W_{B_t,t},F_t,E_{B_t,t},H_{B_t,t},ξ_{B_t,t}>

FLOW
S_t → Δ → S_t+1

OPERATIONS
preserve()
change()
stabilize()
destabilize()
shift()
blur()
break()
redistribute()

ANALYSIS
What remains?
What changes?
Under which B?
What is ξ?

GENERATION
What to preserve?
What to change?
Where to move?

Core
≠ tuning
≠ harmony
≠ genre
≠ Western music
```

---

*v0.1：初版。RDL音楽理論の最小共通文法として、音楽状態 \(S_t\) と基本操作群を定義。特定調律・和声・文化圏に依存する知識をCore外へ置き、分析と生成の双方から利用可能な最小構造として仮設。*
