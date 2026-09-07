# 旧B分類 第一再分類表

*状態：DRAFT v0.1 / 新T0/T1基準での旧B分類再読*
*依存：旧T2候補_新T0T1基準_再分類入口.md / RDL_Music_Theory_既存検証_A_B_C分類_第一段階.md*

---

## 0. 目的

本書は、旧A/B/C分類で `B = Music起源だが汎用化候補` とされた工程帯を、新T0/T1基準で最初にほどくための再分類表である。

ここでの分類は正式移管ではない。旧3398工程の履歴価値を保存しつつ、現在のMusic本線とT1/T2責務が混線しないようにするための作業台である。

---

## 1. 再分類カテゴリ

```text
T1工程
  Probe / Expansion / Inspection / Selection / Reconstruction に属する形成経路

T2汎用検査道具
  SelectionやInspectionに使える交換可能な検査・評価・比較道具

Music固有Selection基準
  音楽対象を読むための判断基準・許容損失・聴取停止線

Music↔汎用fixture
  Music入力・Music出力と汎用道具候補を接続する検証足場

historical evidence
  工程番号列、旧分類名、発見順序、当時の抽出経路
```

---

## 2. 工程帯別の第一再分類

| 旧範囲 | 旧主題 | 第一再分類 | 理由 | 保留点 |
|---|---|---|---|---|
| 86〜127 | state record、validation、adoption、plan、execution readiness、contract、payload binding、activation bridge | T1工程 / Music↔汎用fixture / historical evidence | 入力をBとΓで切り出し、既存Music Moduleへ渡す接続形成が主である。contractやbindingはT2本体ではなく、Probeから既存処理へ入るためのfixtureとして読む。 | validationがT2汎用検査道具になる部分と、単なるguardになる部分の分離。 |
| 179〜228 | 螺旋型再入循環、closed reentry cycle | T1工程 / historical evidence | inputからreentryまでの循環は、T1のProbe→展開→検査→再構成に近すぎる。Runtime全体をT2へ上げない。 | 各遷移で使われた検査関数だけをT2道具候補として抜けるか。 |
| 399〜998 | policy、multiple interpretation、B依存選択、weighting、threshold、candidate lifecycle、selection controller、alternative memory、memory limit | T2汎用検査道具 / Music固有Selection基準 / Music↔汎用fixture / historical evidence | 比較・重み・閾値・memory limitは道具候補になりうる。一方、何を保存・優先・保留するかはMusic固有Selection基準を含む。 | `selection controller` をT2道具とMusic基準に分解する必要がある。 |
| 999〜1598 | memory reactivation、refrain identity、variation lifecycle、branch reentry、polyphonic memory、deferred resolution | T1工程 / Music固有Selection基準 / Music↔汎用fixture | 記憶・回帰・変奏・解決はMusic固有の時間関係を多く含む。再活性化やbranch reentryはT1形成経路として読む。 | refrain / variation / resolution の音楽固有条件を汎用memory mechanismから切り分ける。 |
| 1599〜2598 | drift、threshold、split reintegration、context pressure、delayed selection、commitment、conflict、policy execution、trace update | T2汎用検査道具 / T1工程 / historical evidence | drift検査、threshold、conflict検出、policy executionはT2道具候補になりうる。commitmentやtraceはT1再構成・履歴機構に近い。 | commitmentをMusic固有採用、T1再構成、trace mechanismへ分ける。 |
| 2599〜3398 | alternative reactivation after commitment、commitment conflict、mediation、outcome readiness、selection readiness、commitment record | T1工程 / T2汎用検査道具 / historical evidence | mediationやoutcome比較は道具候補を含むが、post-commitment lifecycle全体はT1形成経路と履歴資料として読む。 | mediation selection controllerを、汎用比較道具・Music基準・fixtureへ三分する。 |

---

## 3. 旧語彙の読み替え

```text
candidate lifecycle
  -> T1形成経路の履歴記述
  -> 必要に応じてtrace mechanism候補を抽出

selection controller
  -> T1 Selectionで使われるcontroller候補
  -> T2汎用検査道具かMusic固有Selection基準かを再判定

commitment
  -> T1 Reconstruction / Music固有採用基準 / historical eventに分解

record
  -> 代謝そのものではなくtrace / observation / fixture recordとして再読

alternative memory
  -> Music固有の複数解釈・記憶条件
  -> 汎用memory limit tool候補
  -> historical evidenceに分解

mediation
  -> conflict比較道具候補
  -> Music固有の解釈調停基準
  -> fixture上の接続手順に分解
```

---

## 4. T2候補として残す最小対象

旧B分類から、現時点でT2汎用検査道具候補として残せる可能性が比較的高いものは次である。

```text
consistency check
loss criterion evaluator
threshold comparator
conflict detector
memory pressure / limit evaluator
reactivation eligibility check
mediation comparison metric
trace integrity check
stress test harness
```

これらも正式T2ではない。非Music対象で再使用し、SelectionやInspectionの道具として働くかを確認するまで候補に留める。

---

## 5. Music側へ戻す対象

旧B分類から、Music本線へ戻すべきものは次である。

```text
multiple interpretationの音楽的条件
refrain / motif memory
variation identity
polyphonic memory coordination
resolution expectation
context pressure as musical context
actual listening保留線
F_device / F_listener / F_analysisの分離
```

これらは汎用Runtimeへ吸い上げすぎず、Music Core v0.2の実験系列へ戻す。

---

## 6. 第一結論

旧B分類は、もはや一枚の `T2 Mechanism候補` ではない。

```text
旧B分類
=
T1形成経路
+ T2汎用検査道具候補
+ Music固有Selection基準
+ fixture
+ historical evidence
```

として読む。

次に進む場合は、`selection controller` を最初の分解対象にする。理由は、旧分類ではT2候補として肥大化しやすく、新T1/T2では `Selection ≠ T2` の境界が最も露出するためである。
