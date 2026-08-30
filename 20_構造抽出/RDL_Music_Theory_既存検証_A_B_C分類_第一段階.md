# RDL_Music_Theory 既存検証 A/B/C分類 第一段階

## 位置づけ

`60_今後の展望/RDL_Music_Theory_方針修正計画書.md` の第一段階に従い、既存検証を削除・移動せず、主対象によって暫定分類する。

この分類は正式移管ではない。

また、A/B/Cは完全な排他分類ではない。各範囲には主分類を一つ置き、必要に応じて補助タグを付ける。

```text
primary = A / B / C
secondary tags = Music-specific / T2-candidate / fixture
```

```text
分類
↓
圧縮
↓
非Music対象で再使用
↓
T2昇格判定
```

## 分類基準

```text
A Music固有
  音楽対象がなければ成立しない検証。

B Music起源だが汎用化候補
  candidate / selection / commitment / record / retention / reactivation / handoff など、
  音楽語彙を外しても状態遷移として残る検証。

C 両者の接続検証
  音楽的入力・出力と、汎用処理機構の境界接続を同時に扱う検証。
```

## A. Music固有

Music側へ残す主領域。

```text
01〜04
  primary = A
  secondary = Music-specific
  C6 / Am7、C major、単純リズム、純粋候補集合の初期観測。

06〜15
  primary = A
  secondary = Music-specific
  波形関係、周波数比、12TET半音数、音程綴り、トライトーン解決方向、音度から具体音への実現。

42〜53
  primary = A
  secondary = Music-specific
  和声機能、key context、function annotation、target候補、voice leading、next context。

54〜68
  primary = A
  secondary = Music-specific / fixture
  基層解釈、frequency response、temporal integration、learned bridge、音楽的解釈から中核Module入力への接続。

69〜85
  primary = A
  secondary = Music-specific / fixture
  音程Moduleの入力、generic interval、quality、interval label、contextual role、target、voice leading、harmonic bridge、next context。
```

保持理由:

```text
音高
音程
調律
和声機能
声部進行
リズム
拍節
音楽的文脈
知覚入力と音楽ラベルの写像
```

これらは、抽象化してもMusic側の対象構造を消さない範囲で扱う。

## B. Music起源だが汎用化候補

T2 Mechanism候補としてマークする主領域。

```text
86〜127
  primary = B
  secondary = T2-candidate / fixture
  state record、validation、M_B候補、Core整合候補、adoption、plan、execution readiness、update review、push readiness、handoff、contract generalization、input contract、payload binding、activation bridge。

179〜228
  primary = B
  secondary = T2-candidate
  螺旋型再入循環。T1代謝を連続運用すると現れるT2実行パターン候補。

399〜998
  primary = B
  secondary = T2-candidate / fixture
  policy、multiple interpretation record schema、B依存選択、weighting、threshold、candidate lifecycle、selection controller、post selection lifecycle、alternative memory、memory limit。

999〜1598
  primary = B
  secondary = T2-candidate
  memory reactivation、refrain identity、variation lifecycle、variation sequence、branch reentry、parallel variation memory、polyphonic memory coordination、deferred resolution、resolution return、post resolution memory update、post resolution reentry。

1599〜2598
  primary = B
  secondary = T2-candidate
  drift、threshold、split candidate reintegration、context pressure、delayed selection、commitment、revision memory、conflict detection、policy execution、attempt outcome、interpretation commitment、record、trace update、post commitment alternative retention。

2599〜3398
  primary = B
  secondary = T2-candidate / fixture
  alternative reactivation after commitment、commitment conflict、conflict mediation、mediation outcome readiness、attempt、observation、record boundary、selection readiness、selection controller、selected outcome、commitment readiness、commitment attempt、commitment record、post commitment alternative retention。
```

抽出単位:

```text
state
transition
guard
stop line
input
output
ξ
```

保持する非同一性:

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

## C. 両者の接続検証

Music側のfixtureとして残しつつ、T2候補抽出の入口にもなる領域。

```text
05
  primary = C
  secondary = Music-specific / T2-candidate / fixture
  Bから候補空間生成。Music固有の候補生成でありつつ、candidate generation一般化の入口でもある。

16〜41
  primary = C
  secondary = Music-specific / T2-candidate / fixture
  empty、fallback、再探索、動態Adapter、二標本横断、不変条件、no_effect、状態signature、候補再生成。

74〜85
  primary = C
  secondary = Music-specific / fixture
  音程Moduleのtarget selectionからvoice leading、harmonic bridge、state recordへ至る接続。

128〜178
  primary = C
  secondary = Music-specific / T2-candidate / fixture
  音程Module reentry列。音程固有処理へ戻りつつ、契約・実行境界・再入パターンを観測する。

229〜268
  primary = C
  secondary = Music-specific / T2-candidate / fixture
  和声機能、リズム拍節、音高調律への螺旋型再入循環移植と四Module差異抽出。

269〜398
  primary = C
  secondary = Music-specific / T2-candidate / fixture
  四Module音楽的固有性、相互作用面、音高調律から音程綴り境界、予測分岐と複数解釈保持。
```

Cは、A/Bのどちらかへ即時吸収しない。

```text
音楽的入力
↓
汎用処理機構
↓
音楽的出力
```

のfixtureとして残す。

## 第一段階の結論

現時点では、3398工程までの巨大列をそのままT2仕様へ移植しない。

```text
A = Music固有の対象構造
B = T2候補の状態遷移機構
C = Music fixtureを持つ接続検証
```

として分け、次段階ではBを中心に最小骨格へ圧縮する。

## 次段階

```text
B分類範囲
↓
反復する状態名の抽出
↓
transition / guard / stop line の圧縮
↓
Music語彙を外したT2候補骨格
↓
C分類からfixture候補を選ぶ
```

ただし、Music固有差分を消さない。
