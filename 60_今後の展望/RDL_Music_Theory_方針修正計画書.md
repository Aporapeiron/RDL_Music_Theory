# RDL_Music_Theory 方針修正計画書

**状態：DRAFT v0.1**
**対象：RDL_Music_Theory**
**目的：音楽固有理論と、T1代謝を実行する汎用機構の責務を分離する**

---

## 0. 方針修正の要旨

RDL_Music_Theory は現在、

1. 音楽を関係構造として分析・生成する **T3音楽応用系**
2. T1の基本代謝を有限な処理列として実際に回す **汎用実行機構の実験系**

の二つを同時に育てている。

当初の音楽理論側の目的は、

```text
関係を見る
↓
状態を記述する
↓
変化を操作する
```

ことであり、既存音楽理論のRDL語への単純翻訳ではない。

一方、検証の進行によって、

```text
candidate
selection
commitment
record
alternative retention
reactivation
handoff
```

など、音楽対象そのものに依存しない処理位相が大量に抽出されてきた。

これらは、RDL_Modules が定義する

```text
T1 の各プロセスを実際にどう動かすか
```

というT2の責務と一致する。

したがって今後は、

> **音楽を検証場として発見された汎用代謝実行機構をT2候補として抽出し、Musicを再び音楽固有のT3応用へ集中させる。**

ことを基本方針とする。

---

# 1. 修正後の基本配置

```text
T0
基底仮設・最低動作仕様
B / ξ / M_B / E / H / θ
        ↓

T1
基本代謝
SILN展開
↓
検査・選別
↓
再構成
↺
        ↓

T2
代謝実行機構
T1循環を有限な状態遷移として実行する
        ↓

T3
対象別応用
Music / Human / その他
```

T2はT1を再定義しない。

RDL_Modulesの既存方針でも、T2はT1代謝そのものではなく、その代謝を「実際にどう動かすか」を扱う。

今回Musicから抽出するものは、このT2側の **Mechanism候補** とする。

---

# 2. Musicに残すもの

Musicには、対象が音楽でなければ成立しない構造を残す。

例：

```text
音高
音程
調律
音階
調性
和音
和声機能
声部進行
リズム
拍節
グルーヴ
旋律
モチーフ
楽式
音楽的曖昧性
聴取上の複数解釈
物理入力と知覚の写像
```

また、

```text
preserve()
change()
stabilize()
destabilize()
shift()
blur()
break()
redistribute()
```

など、音楽分析・生成に直接用いる共通操作については、Music Coreに保持する余地がある。

ただし、その内部で使用される汎用的な候補管理・選択・記録機構はT2側へ委譲する。

---

# 3. T2抽出候補

次のような構造は、音楽固有知識ではなく、代謝処理の状態遷移として扱う。

```text
candidate generation
candidate retention
candidate lifecycle

weighting
priority
threshold
selection controller
selection

commitment
commitment attempt
commitment boundary

record
trace
alternative memory

reactivation
reentry

handoff
execution readiness
update review
promotion diagnostic
```

特に次の非同一性は汎用性が高い。

```text
candidate ≠ selected

selected ≠ committed

committed ≠ recorded

recorded ≠ final

unselected ≠ deleted

alternative retained ≠ resolution

diagnostic ≠ update

plan ≠ execution

handoff ≠ next execution
```

現在の汎用分解再結晶化方法論でも、

```text
候補 ≠ 確定
診断 ≠ 更新
record ≠ Core
計画候補 ≠ 実行
handoff ≠ 次作業開始
```

という分離が既に抽出されている。

---

# 4. 抽出物の暫定的な立ち位置

現段階では新たな基底層やT1を追加しない。

暫定配置：

```text
RDL_Modules
└─ Metabolic_Runtime / 仮称
   ├─ README.md
   ├─ Candidate_State_Transition
   ├─ Selection_Control
   ├─ Record_and_Alternative_Memory
   └─ Reentry_and_Handoff
```

ただし、このディレクトリ構成は確定しない。

RDL_Modules自身の原則、

```text
候補
↓
実運用
↓
複数対象で再使用
↓
有効範囲を確認
↓
正式モジュールへ昇格
```

に従う。

したがって最初から多数の正式Moduleへ分割しない。

---

# 5. 第一段階：Music内での分類

既存文書を削除・移動する前に、まず全検証を三分類する。

### A. Music固有

```text
音高
音程
和音
和声
リズム
拍節
音楽知覚
音楽文脈
音楽的複数解釈
```

Musicへ残す。

### B. Music起源だが汎用化候補

```text
candidate lifecycle
selection
commitment
record
alternative retention
reactivation
reentry
handoff
```

T2昇格候補としてマークする。

### C. 両者の接続検証

```text
音楽的入力
↓
汎用処理機構
↓
音楽的出力
```

Music側に実例として残すか、T2側のfixture / stress testとして複製・再構成する。

---

# 6. 第二段階：最小骨格の抽出

3398工程等の検証列を、そのままT2へ移植しない。

先に圧縮する。

例：

```text
大量の個別工程
↓
反復する状態
↓
状態間の禁止接続
↓
最小遷移機構
```

抽出対象は「工程番号」ではなく、

```text
state
transition
guard
stop line
input
output
ξ
```

とする。

---

# 7. 第三段階：Music以外で耐久検査

T2候補へ昇格させる前に、少なくとも一つ以上の非Music対象で再使用する。

候補例：

```text
RDL_Human
概念耐久検査
文書編集
理論比較
設計判断
```

音楽入力を外した途端に成立しなくなるなら、Music固有構造として戻す。

複数対象で同じ状態遷移・停止線が残るなら、T2 Mechanism候補として強度が上がる。

---

# 8. 第四段階：Music Coreの再圧縮

汎用処理を外したあと、Music Coreを再検査する。

Music Coreに最低限残す問いは、

```text
何を音楽的境界としているか。

何が保存されているか。

何が変化したか。

どの関係が変化を支配したか。

何が別状態へ移行したか。

何を保存し、何を変えると、
目的とする音楽変化を生成できるか。
```

とする。

Music Coreの破断条件として既に、

```text
分析はできるが生成に利用できない
生成はできるが保存構造を説明できない
```

等が置かれているため、再圧縮後もこれを維持する。

---

# 9. T0整合修正

抽出作業と並行して、Music CoreのT0整合を修正する。

## 9.1 E

現行Music Core：

```text
E
=
現在のM_Bから維持・予測される関係
と
F
との差
```

を、現行T0 SPECに合わせ、

```text
F(t)
=
interp(M_B, EFP(t))

F'(t+Δ)
=
interp(M_B, EFP(t+Δ))

E(t+Δ)
=
Δ(F, F')
```

へ整理する。

F'には更新後のM_B'を使わず、同一の更新前M_Bを用いる。これは現行SPECの明示要件である。

## 9.2 ξ

Music側でξを単なる「記述不能成分」とせず、

> **有限境界Bを引いたことに伴って残る未回収関係**

としてT0定義を継承する。

---

# 10. 汎用分解再結晶化方法論の扱い

`04_汎用分解再結晶化方法論.md` は削除しない。

これはMusic内部で発見された第二成果を保持している。

ただし位置づけを、

```text
Music固有理論
```

から、

```text
Musicを第一検証場として得られた
T2方法論候補
```

へ変更する。

将来的にT2へ正式移植された場合、Music側には、

```text
この方法論がMusicでどのように発生したか
```

を示す参照文書だけを残してよい。

---

# 11. 直ちに行わないこと

今回の修正では次を行わない。

```text
T1の基本代謝定義を変更しない。

T0へ新しい基底変数を追加しない。

candidate / controller / record 等を
Core Primitiveへ昇格しない。

3398工程をそのまま正式仕様にしない。

既存検証文書を大量削除しない。

Musicから検証履歴を消さない。

先に巨大なT2階層を設計しない。
```

---

# 12. 昇格条件

Music由来の構造をT2 Mechanismとして正式昇格させるには、最低限次を満たす。

```text
1. 音楽固有語彙を除いて記述できる。

2. T1のどの局面を実行する機構か明示できる。

3. input / output が定義できる。

4. 状態遷移が明示できる。

5. 禁止接続・停止線が明示できる。

6. 破断条件が存在する。

7. ξとして未回収部分を残せる。

8. Music以外の対象でも再利用できる。

9. T1そのものを再定義していない。

10. T0のB-ξおよび更新仕様に反しない。
```

---

# 13. 方針修正後の期待構造

```text
RDL_Music_Theory

00_RDL音楽理論
01_RDL音楽_Core
03_全体設計方針

10_検証
├─ 音楽固有検証
├─ T2抽出元検証
└─ 接続検証

20_構造抽出
├─ 音楽固有構造
└─ T2昇格候補

30_既知音楽理論参照

40_中核音楽理論

50_既知基層解釈参照
```

T2へ移す候補についても、元の検証履歴との参照関係を保持する。

---

# 14. 方針の圧縮

```text
Musicで育ったものを、
全部Musicの理論とはみなさない。

音楽固有の関係はMusicへ残す。

対象に依存せず、
T1循環を実際に回していた機構は、
T2候補として抽出する。

ただし、
抽出しただけでT2へ確定しない。

圧縮し、
別対象へ食わせ、
壊し、
残ったものだけを昇格する。
```

---

## 最終方針

> **RDL_Music_Theoryを縮小することが目的ではない。音楽を検証場として発見された汎用機構を適切な層へ戻すことで、Musicの音楽固有性と、RDL全体系の代謝実行能力を同時に明確化する。**

> **T1は代謝の基本循環を定める。Musicから抽出される候補は、その循環を現実の有限処理として成立させるT2代謝実行機構として検査する。**
