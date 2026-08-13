# 全Module横断レビュー｜破断と最小検証

*状態：DRAFT v0.1*

## 0. 目的

`40_中核音楽理論` の `01`〜`10` が一通り作成されたため、次段階としてModule間の重複、循環参照、責務漏れ、破断条件を横断的に見る。

本書は新しい音楽理論Moduleを増やすものではない。既存Module間の接続を、次の四つへ分解する。

```text
observation
generation
selection
controller
```

特に、既知音楽理論で相互説明になりやすい次の領域を主対象にする。

```text
音階・調
  ↔ 和音
  ↔ 和声機能
  ↔ 声部進行
```

## 1. 現在の全体段階

現在の段階は、Module候補を作る段階から、全Moduleを横断して破断を見る段階へ移った。

```text
30_既知音楽理論参照
        ↓
40_中核音楽理論
        ↓
10_検証
        ↓
20_構造抽出
        ↓
必要なら 01 Core / 03 全体設計へ戻す
```

`40_中核音楽理論` は、既知音楽理論の章立てではなく、各領域を次の共通書式で受けるためのModule計画である。

```text
B
Γ
M_B候補
候補生成
制約
選択
ξ
破断条件
```

## 2. 最重要循環候補

現在もっとも注意すべき循環は次である。

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

この流れは、既知音楽理論では自然に説明し合う。しかしRDL音楽では、どの段階が観測で、どの段階が候補生成で、どの段階が選択で、どの段階がcontrollerなのかを分けないと循環する。

## 3. 4領域の責務分割

### 3.1 音階・調Module

主責務は、音名・音高・綴りを `key context` と `scale degree role` へ写すことである。

```text
spelled pitch
  + key context
  ↓
scale degree role
```

ここで許されること。

- tonic候補を置く
- scale pattern候補を置く
- spelling policyを置く
- 音をscale degreeへ写す
- degree roleを注釈する

ここでしてはいけないこと。

- key contextから和音候補を自動確定する
- scale degreeからtargetを一意生成する
- tonicを人間の基層知覚中心として完成モデル化する

### 3.2 和音Module

主責務は、key contextやpitch collectionを受けて、和音候補集合を生成・保持することである。

```text
key context / pitch collection
  ↓
B_chord + Γ_chord_candidate
  ↓
chord candidate set
```

ここで許されること。

- pitch collectionから複数のroot候補を立てる
- bass、voicing、spelling、履歴を別軸として保持する
- `C6 / Am7` のような同一音集合の曖昧さを候補集合として残す
- `C(B, M_B; Γ)` として候補生成規則の依存性を記録する

ここでしてはいけないこと。

- pitch collectionを和音同一性とみなす
- chord labelからharmonic functionを確定する
- chord labelから次進行を生成する
- `Γ_chord_candidate` をCoreへ昇格する

### 3.3 和声機能Module

主責務は、和音候補にkey context、degree role、履歴を重ね、機能注釈候補を立てることである。

```text
chord candidate
  + key context
  + degree role
  + local history
  ↓
functional annotation候補
```

ここで許されること。

- same chord / different key context による機能分岐を記録する
- tonic / dominant / predominantをlearnedな機能注釈候補として置く
- cadence候補を前後関係込みで注釈する
- targetが外部から与えられた場合に注釈する

ここでしてはいけないこと。

- function labelをtarget生成器にする
- dominantをtonicへの必然的解決とみなす
- Hをharmonic tensionへ直結する
- tonicを基層知覚中心として完成モデル化する

### 3.4 声部進行Module

主責務は、既に与えられたtarget degree候補や和音候補を、具体音候補・制約・選択・履歴へ展開することである。

```text
target degree候補
  ↓
B_voice_realization + Γ_voice_candidate
  ↓
concrete voice candidates
  ↓
constraint / selection / history
```

ここで許されること。

- target degreeから複数の具体音候補を生成する
- voice range、ordering、spacingで候補を制約する
- `empty` を観測として記録する
- fallbackやboundary reopenを構造遷移として保持する
- `Γ_select` が明示された場合だけ具体実現を選ぶ

ここでしてはいけないこと。

- target degreeをconcrete pitchへ直結する
- leading toneを必ず解決させる
- minimum motionを普遍選択規則にする
- fallbackを正解にする
- GenericDynamicEventをstate復元命令にする

## 4. 観測・生成・選択・controllerの分離

### 4.1 observation

観測は、現在の境界で何が見えているかを記録する。

```text
pitch collection observed
key context observed / hypothesized
chord candidate observed
functional annotation observed
empty observed
motion observed
```

観測は、次の候補を選ぶ命令ではない。

### 4.2 generation

生成は、明示された `B / M_B / Γ` から候補集合を作る。

```text
B_key_scale + Γ_scale_degree
  → degree role candidates

B_chord + Γ_chord_candidate
  → chord candidate set

B_harmonic_function + Γ_function_annotation
  → function annotation candidates

B_voice_realization + Γ_voice_candidate
  → concrete voice candidates
```

生成は、候補を一つ選んだことを意味しない。

### 4.3 selection

選択は、候補集合に制約や選択規則を適用して採用候補を決める。

```text
candidate set
  + constraints
  + Γ_select
  ↓
selected candidate
```

`Γ_select` がない場合、候補集合は `underdetermined` として保持する。

### 4.4 controller

controllerは、どの境界を開くか、どのΓを使うか、empty後に何を緩和するかを決める。

現時点では、controllerはModule固有または未解決ξとして残す。

```text
controller未確定:
  tonic候補の選択
  chord root候補の選択
  function annotationの選択
  target候補の選択
  voice-leading制約緩和
  fallback採用
```

これらをCoreへ上げない。

## 5. 循環を切るための禁止線

次の短絡を禁止する。

```text
key context → chord candidateを一意生成
chord label → harmonic functionを一意生成
function label → targetを一意生成
target degree → concrete pitchを一意生成
voice leading result → next key contextを自動確定
```

許されるのは、各段階で候補を生成し、候補集合・制約・履歴・未解決ξを記録することだけである。

## 6. 最小横断検証候補

次の検証を優先候補とする。

### 6.1 same chord / different key context

```text
G-B-D
  + C major
  ↓
V / dominant候補

G-B-D
  + G major
  ↓
I / tonic候補
```

確認すること。

- 和音名だけでは機能が決まらない
- key contextがfunction annotationを分岐させる
- function annotationはtargetを自動生成しない

### 6.2 same pitch collection / different bass-context

```text
{C, E, G, A}
  + bass C
  ↓
C6候補

{C, E, G, A}
  + bass A
  ↓
Am7候補
```

確認すること。

- pitch collectionだけではchord identityが決まらない
- bass、context、historyがM_B候補を分岐させる
- C6 / Am7はfunctionへ直結しない

### 6.3 function annotation / target candidate分離

```text
dominant annotation候補
  ↓
target候補集合
  ↓
未選択ならunderdetermined
```

確認すること。

- dominantはtarget生成器ではない
- target候補が複数残る状態を保持できる
- selected targetがある場合だけ `Γ_motion` へ進む

### 6.4 target degree / concrete realization分離

```text
target degree
  ↓ B_voice_realization
candidate concrete pitches
  ↓ constraints
selected realization / empty
```

確認すること。

- target degreeは具体音ではない
- voice rangeやorderingでemptyが起きる
- emptyは失敗ではなく観測記録である

## 7. 横断レビューで見えた責務漏れ

現時点で明確に未回収な責務は次である。

| 未回収責務 | 現在位置 |
|---|---|
| tonic候補を選ぶcontroller | 音階・調Moduleのξ |
| chord root候補を選ぶcontroller | 和音Moduleのξ |
| function annotationを選ぶcontroller | 和声機能Moduleのξ |
| target候補を生成・選択するcontroller | 和声機能 / 声部進行Moduleの間のξ |
| empty後の緩和順序controller | 声部進行 / 動態Adapterのξ |
| next key contextを再解釈するcontroller | 音階・調 / 形式Moduleのξ |

これらは「不足」ではなく、現段階でCoreへ上げないために明示しておく未解決ξである。

## 8. 現時点の結論

`03_音階調`、`04_和音`、`05_和声機能`、`06_声部進行` は、次のように接続するのが安全である。

```text
音階・調:
  key context / scale degree roleを注釈する

和音:
  chord candidate setを生成・保持する

和声機能:
  function annotation候補を生成・保持する

声部進行:
  target degree候補を具体音候補・制約・履歴へ展開する
```

循環を閉じるのは、controllerを入れたときである。現段階ではcontrollerを未解決ξとして残し、候補生成・観測・選択・履歴の分離が保てるかを最小検証で確認する。

## 9. 作成済み検証と次候補

最初の横断検証として、次を作成した。

```text
42_和声機能_同一和音とkey_context分岐_最小実験.md
harmonic_function_key_context_branch.py
```

確認したこと。

```text
same chord candidate
  + different key context
  ↓
different degree annotation
  ↓
different function annotation
  ↓
targetは未生成のまま保持
```

この検証で、和音Moduleから和声機能Moduleへの接続は、循環せずに成立する最小例を得た。

次の横断検証として、次を作成した。

```text
43_和声機能_target候補集合と選択境界_最小実験.md
harmonic_function_target_candidate_boundary.py
```

確認したこと。

```text
function annotation candidate
  + externally supplied target candidate set
  ↓
target candidates observed
  ↓
Γ_context_selectionなし → underdetermined
Γ_selectあり → selected target
```

これにより、42〜43で次の三分離を確認した。

```text
function annotation
  ≠ target candidate generation
  ≠ target selection
```

次の接続検証として、次を作成した。

```text
44_声部進行_selected_targetから具体音実現境界_最小実験.md
voice_leading_selected_target_realization_boundary.py
```

確認したこと。

```text
selected target = C major
  ↓ external target degree plan
target degrees = 3 / 1
  ↓ existing 14 realization
selected concrete target = E4-C5
```

この接続は自動生成ではない。

```text
selected target
  ≠ target degree plan
  ≠ concrete pitch realization
```

これにより、42〜44で次の分離を確認した。

```text
function annotation
  ≠ target candidate generation
  ≠ target selection
  ≠ target degree planning
  ≠ concrete pitch realization
```

次の接続検証として、次を作成した。

```text
45_文脈解釈_voice_leading後のnext_key未確定_最小実験.md
next_key_context_after_voice_leading_boundary.py
```

確認したこと。

```text
voice leading result = E4-C5
  + externally supplied next context candidate set
  ↓
next context candidates observed
  ↓
Γ_context_selectionなし → underdetermined
Γ_context_selectionあり → selected next context
```

この接続は自動生成ではない。

```text
voice leading result
  ≠ next key/context interpretation
```

これにより、42〜45で次の分離を確認した。

```text
function annotation
  ≠ target candidate generation
  ≠ target selection
  ≠ target degree planning
  ≠ concrete pitch realization
  ≠ next key/context interpretation
```

42〜45の横断結果は、次の構造抽出版へ送った。

```text
20_構造抽出/中核音楽理論_42〜45循環分解_構造抽出版.md
```

この抽出版では、循環候補を因果列として閉じず、annotation、generation、observation、selection、planning、realization、reinterpretationの非同一性として整理する。
次のξ検証として、次を作成した。

```text
46_和声機能_function_annotationとtarget候補生成規則の分離_最小実験.md
harmonic_function_target_generation_rule_boundary.py
```

確認したこと。

```text
function annotation candidate
  + key context
  + Γ_target_candidate_generation_fixture
  ↓
generated target candidate set
```

ただし、この生成はfunction annotation candidate単独から生じたものではない。

```text
function annotation candidate
  ≠ Γ_target_candidate_generation_fixture
  ≠ generated target candidate set
```

また、生成済みcandidate setはselected targetではない。

```text
generated target candidate set
  ≠ selected target
```

46により、42〜45で空けていた `ξ_target_candidate_generation` へ限定fixtureを置いても、annotationとgenerationの分離が保てることを確認した。次候補は、生成規則を変えた場合に同じfunction annotation candidateから異なるtarget候補集合が生じるかを見る検証である。
次のξ検証として、次を作成した。

```text
47_和声機能_target候補生成規則差し替えによる候補集合分岐_最小実験.md
harmonic_function_generation_rule_variation.py
```

確認したこと。

```text
same function annotation candidate
  + same key context
  + different Γ_target_candidate_generation_fixture
  ↓
different generated target candidate sets
```

これにより、target候補集合はfunction annotation candidateの内在属性ではなく、annotation、context、生成規則の関係として生じることを確認した。

```text
generated target candidate set
  = C(function annotation candidate, key context; Γ_target_candidate_generation_fixture)
```

ただし、生成規則はfixtureであり、一般的・文脈依存な `ξ_target_candidate_generation` は未解決である。次候補は、同じfunction annotation candidateと同じ生成規則でも、key contextを変えると候補集合が変わるかを見る検証である。
次のξ検証として、次を作成した。

```text
48_和声機能_context差し替えによるtarget候補集合分岐_最小実験.md
harmonic_function_generation_context_variation.py
```

確認したこと。

```text
same function annotation label
  + different key context
  + same Γ_target_candidate_generation_fixture
  ↓
different generated target candidate sets
```

47では生成規則差し替えで候補集合が分岐した。48では生成規則を固定し、context差し替えで候補集合が分岐することを確認した。

```text
dominant_candidate + C major + Γ_context_sensitive_fixture
  → {C major, A minor}

dominant_candidate + G major + Γ_context_sensitive_fixture
  → {G major, E minor}
```

ただし、ここで固定したのはfunction annotation labelであり、同一のFunctionObservation objectではない。生成規則はfixtureであり、一般的・文脈依存な `ξ_target_candidate_generation` は未解決である。
46〜49の横断結果は、次の構造抽出版へ送った。

```text
20_構造抽出/和声機能_target候補生成_46〜49構造抽出版.md
```

この抽出版では、`ξ_target_candidate_generation` を完成規則としてではなく、function observation、Γ_target_candidate_generation、applicability check、generated target candidate set、selection boundaryの分離として整理する。
次のξ検証として、次を作成した。

```text
49_和声機能_history差し替えによるtarget候補集合分岐_最小実験.md
harmonic_function_generation_history_variation.py
```

確認したこと。

```text
same current function observation
  + same Γ_target_candidate_generation_fixture
  + different history
  ↓
different generated target candidate sets
```

46〜48ではannotation、context、Γ_generationの軸を見た。49ではhistoryを追加入力として置き、同じcurrent observationと同じΓでも候補集合が分岐することを確認した。

```text
dominant_candidate + C major + Γ_history_sensitive_fixture + ordinary_preparation
  → {C major}

dominant_candidate + C major + Γ_history_sensitive_fixture + deceptive_setup
  → {C major, A minor}
```

ただし、historyはfixtureであり、一般的・文脈依存な `ξ_history_sensitive_generation` は未解決である。selected targetは生成しない。
次のξ検証として、次を作成した。

```text
50_和声機能_同一history大分類内local_pattern差によるtarget候補集合分岐_最小実験.md
harmonic_function_generation_history_local_pattern.py
```

確認したこと。

```text
same current function observation
  + same Γ_target_candidate_generation_fixture
  + same history.broad_pattern
  + different history.local_pattern
  ↓
different generated target candidate sets
```

49ではhistory.local_patternがcandidate setへ影響しうることを確認した。50では、history大分類が同じでも、Γが読む局所粒度が異なればcandidate setが分岐することを確認した。

```text
broad_pattern = dominant_preparation
local_pattern = ordinary_preparation
  → {C major}

broad_pattern = dominant_preparation
local_pattern = deceptive_setup
  → {C major, A minor}
```

ただし、50は粒度そのものを切り替える検証ではない。同一broad_pattern内のlocal_pattern差が、今回のΓに読まれた場合にcandidate setへ影響することを確認した。selected targetは生成しない。
次のξ検証として、次を作成した。

```text
51_和声機能_B_history粒度差によるtarget候補集合分岐_最小実験.md
harmonic_function_generation_history_boundary_granularity.py
```

確認したこと。

```text
same underlying history
  + same current function observation
  + same Γ_target_candidate_generation_fixture
  + different history representation under B_history
  ↓
different generated target candidate sets
```

51では、同じunderlying historyを `B_history_coarse` と `B_history_fine` で異なるhistory representationへ投影し、Γが参照できるhistory featuresの違いによりcandidate setが分岐することを確認した。

```text
B_history_coarse → broad_pattern only → {C major}
B_history_fine   → broad_pattern + local_pattern → {C major, A minor}
```

ただし、B_historyの選択とhistory representation粒度はfixtureであり、一般的な `ξ_history_granularity` は未解決である。selected targetは生成しない。

