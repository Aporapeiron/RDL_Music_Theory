# 検証記録：和声機能・同一和音とkey context分岐

*対象：同じ和音候補が、異なるkey contextで別の和声機能候補へ分岐する条件*  
*状態：DRAFT v0.1 / 中核音楽理論Module横断レビュー後の最小検証*  
*実装：`10_検証/harmonic_function_key_context_branch.py`*

---

## ■ 0. 検証目的

`40_中核音楽理論/11_全Module横断レビュー_破断と最小検証.md` では、次の循環候補を最重要課題として置いた。

```text
key context
  ↓
chord candidate
  ↓
harmonic function
  ↓
target
  ↓
voice leading
  ↓
next key/context interpretation
```

今回の検証では、この循環を閉じない。

同じ和音候補に異なるkey contextを接続したとき、degree annotationとfunction annotationが分岐することだけを確認する。

```text
same chord candidate
  + different key context
  ↓
different degree annotation
  ↓
different function annotation candidate
  ↓
targetは未生成のまま保持
```

ここで確認するのは、和音Moduleから和声機能Moduleへの接続である。function labelからtargetや声部進行を自動生成しない。

---

## ■ 1. 固定する最小入力

### 1.1 和音候補

和音候補を次に固定する。

```text
chord candidate:
  label = G major triad
  root = G
  quality = major
  pitch_classes = {G, B, D}
```

これはrooted chord candidateであり、音響実測やvoicing、bass、履歴は扱わない。

### 1.2 key context

同じ和音候補に、二つのkey contextを接続する。

```text
Context A:
  C major

Context B:
  G major
```

key contextは観測・仮説として与える。今回のコードは、和音候補からkey contextを推定しない。

---

## ■ 2. BとΓ

今回の境界は次の通り。

```text
B_harmonic_function:
  chord candidate
  key context
  function vocabulary
```

使うΓは二段階に分ける。

```text
Γ_degree_annotation:
  chord root + key context
  → root degree

Γ_function_annotation:
  root degree + function vocabulary
  → function annotation candidate
```

ここで重要なのは、次を置かないことである。

```text
Γ_target_generation
Γ_voice_leading_generation
Γ_next_key_interpretation
```

したがって、function annotationはtarget生成器ではない。

---

## ■ 3. 最小ケースの比較

### 3.1 `G-B-D` in C major

```text
G major triad
  + C major key context
  ↓
root degree = 5
  ↓
function annotation = dominant_candidate
```

この結果は、C major内でG major triadをV候補として注釈できることを示す。

ただし、ここからtonicへのtargetは生成しない。

### 3.2 `G-B-D` in G major

```text
G major triad
  + G major key context
  ↓
root degree = 1
  ↓
function annotation = tonic_candidate
```

同じ和音候補でも、key contextが変わるとroot degreeとfunction annotationが分岐する。

---

## ■ 4. 観測結果

| chord candidate | key context | root degree | function annotation | generated target |
|---|---|---:|---|---|
| `G-B-D` | C major | 5 | `dominant_candidate` | `None` |
| `G-B-D` | G major | 1 | `tonic_candidate` | `None` |

確認できたこと。

```text
same chord candidate
  ≠ same degree annotation
  ≠ same function annotation
```

さらに、両方ともtargetは未生成である。

```text
function annotation
  ≠ target generation
```

---

## ■ 5. Module責務の確認

今回の接続は、次のように分かれる。

```text
和音Module:
  G major triadというchord candidateを渡す

音階・調Module:
  C major / G majorというkey contextを渡す

和声機能Module:
  root degreeとfunction annotation候補を生成する

声部進行Module:
  今回は未接続
```

したがって、和声機能Moduleは、声部進行Moduleの入力を自動生成していない。

---

## ■ 6. まだ言えないこと

今回の検証から、次は言えない。

```text
dominant_candidateが必ずtonicへ解決すること
tonic_candidateが聴取上の安定を意味すること
G major triadからkey contextを一意推定できること
function annotationからtarget候補集合を生成できること
target候補をどのcontrollerが選ぶか
voice leading後にnext key contextが自動確定すること
```

加えて、今回の`FUNCTION_BY_MAJOR_DEGREE`はfixture用の限定Γであり、quality、spelling、bass、履歴、前後関係を含む一般的な和声機能規則ではない。

これらは未解決ξとして残す。

---

## ■ 7. 暫定結論

今回固定したfixtureでは、同じ和音候補に異なるkey contextを与えることでdegree annotationが分岐し、現在の限定的な`Γ_function_annotation`に従ってfunction annotation候補も分岐した。

```text
G major triad
  + C major
  → degree 5
  → Γ_function_annotation（限定表）
  → dominant_candidate

G major triad
  + G major
  → degree 1
  → Γ_function_annotation（限定表）
  → tonic_candidate
```

ただし、この分岐は一般的な和声機能規則の完成でも、target生成や声部進行生成でもない。

```text
function annotation candidate
  ↓
target未生成
```

したがって、今回の検証は、和音Moduleから和声機能Moduleへの接続を、循環させずに閉じる最小例である。

次の検証では、`dominant_candidate` からtargetを直接生成せず、target候補集合を外部または別Moduleから与えた場合に、どの時点で `underdetermined` と `selected target` が分かれるかを見る。


