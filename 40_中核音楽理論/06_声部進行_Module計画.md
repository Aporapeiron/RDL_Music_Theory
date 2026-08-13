# 声部進行｜Module計画

*状態：DRAFT v0.1*

## 0. 目的

和声機能Moduleや音階・調Moduleから渡されたtarget degree候補、和音Moduleから渡された和音候補を受け取り、複数声部の具体的な時間遷移を候補生成・制約・選択・履歴として整理する。

このModuleは、音程ラベルや機能ラベルから具体的声部進行を一意に導かない。声部進行は、target候補、声域、上下関係、配置、履歴、様式制約、選択規則が接続された後に成立する実現層として扱う。

```text
target degree候補
  ↓
B_voice_realization + Γ_voice_candidate
  ↓
concrete voice candidates
  ↓
constraint / selection / history
```

ここでは、最小移動、声部交差禁止、leading tone解決などを普遍規則としてCoreへ上げない。

## 1. 参照する既知音楽理論

- `30_既知音楽理論参照/06_声部進行.md`
- `20_構造抽出/音程実現_候補生成と制約の構造抽出版.md`
- `20_構造抽出/empty後再探索_観測fallback履歴の構造抽出版.md`
- `20_構造抽出/動態Adapter候補_構造抽出版.md`

既知音楽理論側では、次の語彙が参照される。

| 語彙 | このModuleでの扱い |
|---|---|
| contrary / similar / parallel / oblique motion | 声部間の相対運動ラベル |
| tendency tone | learnedな進行傾向候補 |
| leading tone | key context内の第7音に対する役割注釈候補 |
| voice crossing | 声部上下関係の破断候補 |
| spacing / range | 候補空間の境界・制約 |

これらは様式依存の記述体系であり、人間の選択原理そのものではない。

## 2. 既存検証との接続

主に接続する検証・構造抽出は次の通り。

| 検証・構造 | 接続内容 |
|---|---|
| `14_音程分解_音度から具体音への実現_最小実験.md` | target degreeから具体音候補へ至る実現境界 |
| `15_音程分解_実現制約の競合と候補消滅_最小実験.md` | 声域・上下関係制約による候補消滅 |
| `16〜22` | empty後の再探索、fallback、履歴分離 |
| `24〜41` | 動態Adapter候補、record/event、用途別state同一性 |
| `20_構造抽出/音程実現_候補生成と制約の構造抽出版.md` | target degreeとconcrete pitchの非同一性 |
| `20_構造抽出/empty後再探索_観測fallback履歴の構造抽出版.md` | empty観測・fallback採用・履歴の三断面 |

既存検証から受け取る最小構造は次の通り。

```text
target degree
  ↓ B_realization
candidate octaves / voice range
  ↓ Γ_spelling
generated spelled candidates
  ↓ B_range_projection
filtered candidates
  ↓ Γ_ordering
admissible voice pairs
  ↓ Γ_select
concrete target
```

empty後の構造は次の通り。

```text
candidate empty
  ↓ observation history
action set evaluation
  ↓
fallback / boundary reopen / target discard
  ↓
state reconstruction
```

## 3. B

このModuleの境界候補。

| 境界 | 役割 |
|---|---|
| `B_voice_count` | 声部数を指定する |
| `B_voice_range` | 各声部の音域を指定する |
| `B_candidate_octaves` | target degreeから候補化するオクターブ範囲 |
| `B_voice_ordering` | 上下関係・交差許容を指定する |
| `B_spacing` | 声部間隔・密集/開離配置を扱う |
| `B_motion_policy` | 最小移動などの選択規則を指定する |
| `B_style_constraint` | 様式固有制約を注釈する |
| `B_history` | observation / fallback / realized履歴を保持する |

`B_motion_policy` は選択規則であり、声部進行の普遍法則ではない。

```text
minimum motion
  ≠ human choice
  ≠ musical correctness
```

## 4. Γ

このModuleで使う候補生成・制約・記述規則。

| Γ | 入力 | 出力 |
|---|---|---|
| `Γ_degree_to_voice_candidates` | target degree、candidate octaves | 綴り付き候補 |
| `Γ_range_projection` | candidates、voice range | 範囲通過候補 |
| `Γ_ordering` | filtered candidates | 許容声部組 |
| `Γ_motion_measure` | current、candidate target | 移動量・方向 |
| `Γ_select` | admissible pairs、selection policy | selected target |
| `Γ_motion_label` | voice motions | contrary / parallel等の運動ラベル |
| `Γ_reexplore` | empty record、action set | 再探索候補 |
| `Γ_event_projection` | Module固有record | GenericDynamicEvent |

`Γ_event_projection` は抽象観測であり、Module固有stateを復元する命令ではない。

## 5. M_B候補

このModuleのM_B候補。

| M_B候補 | 内容 |
|---|---|
| `voice_candidate_set` | 声部ごとの具体音候補集合 |
| `range_filtered_candidate_set` | 声域制約を通過した候補 |
| `admissible_voice_pair_set` | 上下関係や交差条件を満たす候補組 |
| `selected_voice_realization` | 選択規則により採用された具体音 |
| `motion_description_record` | 各声部の移動量・方向ラベル |
| `empty_observation_record` | 候補消滅の観測記録 |
| `fallback_transition_record` | 境界再開などの構造状態変更 |
| `realized_transition_record` | 具体音まで実現した遷移記録 |

候補が空になった場合も、実現器全体の失敗とは読まない。

```text
empty
  ≠ target一般の不在
  ≠ 全操作失敗
  ≠ Core破断
```

## 6. 候補生成・制約・選択

### 候補生成

- target degreeから候補オクターブ上の具体音候補を生成する
- voice rangeで候補を投影する
- 声部上下関係を満たす組を生成する
- current stateとの差分から移動量候補を生成する
- motion labelを抽出する

### 制約

- 声域制約
- 声部交差の許容/禁止
- spacing制約
- 最小移動などの選択規則
- 様式固有の禁止・優先条件
- targetを維持するか、破棄するか
- boundaryを再開するか

### 選択

選択はModule内で可能だが、選択規則を明示した場合に限る。

```text
admissible candidates
  + Γ_select
  ↓
selected realization
```

`Γ_select` がない場合は、候補集合を保持して `underdetermined` とする。

## 7. 破断条件

このModuleが破断する、または未解決ξを残す条件。

- 声域投影で片側候補が空になる
- 両側候補は残るが、上下関係で候補対が空になる
- target degreeはあるが、具体音の候補範囲が未指定である
- 最小移動と声部交差禁止などの制約が競合する
- empty後にどの境界を緩和するか決まらない
- fallbackを採用するcontrollerが未定である
- `no_effect` recordを全体無変化と誤読する
- selected realizationを人間の選択と同一視する

禁止する短絡は次の通り。

```text
target degree = concrete pitch
leading tone = always resolves
voice crossing = universally forbidden
minimum motion = universal selection rule
fallback = correct answer
GenericDynamicEvent = state復元命令
```

## 8. 未解決ξ

現時点で残す未解決領域。

- 妥当な声域・spacingの設定
- 制約の優先順位
- candidate empty後の緩和順序
- fallbackを選ぶcontroller
- stop_search / discard_targetの後続接続
- 様式・編成・楽器による声部制約
- 人間の聴取・作曲上の選択原理
- 動態AdapterをどこまでModule横断化できるか
- state同一性をどのviewで比較するか

これらは、動態Adapter検証、形式Module、基層仮説へ送る。

## 9. 次の最小検証

次に必要な最小検証は、声部進行ModuleをリズムModuleと比較し、動態Adapterの第三標本または横断条件を増やすことである。

```text
voice-leading empty
  ↓
fallback / record / regeneration

rhythm boundary empty
  ↓
fallback / record / regeneration
```

最小ケース。

| ケース | 検証したいこと |
|---|---|
| 声域制約で片側候補が空 | empty位置とfallback候補を記録する |
| 声部交差制約で候補対が空 | range emptyとordering emptyを分ける |
| 境界再開fallback | concrete realizationではなく構造状態変更として記録する |
| no_effect record | 候補再生成は実行されても結果非空とは限らない |

この検証により、声部進行固有の実現構造と、Module横断の動態recordを混同しないことを確認する。

## 10. 現時点の短縮式

```text
声部進行Moduleは、
target degreeを具体音へ直結せず、
声域・配置・上下関係・選択規則・履歴を通して
具体的な声部遷移候補を扱う。

emptyやfallbackは失敗ではなく、
動態記録として保持する。
```
