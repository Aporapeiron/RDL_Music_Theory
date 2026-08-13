# リズム・拍節｜Module計画

*状態：DRAFT v0.1*

## 0. 目的

時間上の音・休符・長さ・拍節位置を、候補空間、制約、境界変更、履歴として扱うModule境界を定める。

このModuleは、拍節ラベルやグリッド位置から実際の演奏タイミング、アクセント、グルーヴを一意に導かない。リズムは、時間格子、候補語彙、拍節文脈、休符候補、境界再開、履歴を通して成立する候補Moduleとして扱う。

```text
time grid / meter context
  ↓
B_rhythm + Γ_rhythm_candidate
  ↓
rhythm candidate set
  ↓
constraint / selection / dynamic record
```

拍節やアクセントは、人間の知覚中心や身体同期の完成モデルではなく、現段階ではlearnedな記述候補として置く。

## 1. 参照する既知音楽理論

- `30_既知音楽理論参照/07_リズムと拍節.md`
- `10_検証/03_単純リズム_候補集合と制約.md`
- `10_検証/25_リズム候補Module_動態Adapter第二標本.md`
- `10_検証/26_リズム境界変更_候補空間再構成_最小実験.md`

既知音楽理論側では、次の語彙が参照される。

| 語彙 | このModuleでの扱い |
|---|---|
| pulse | 反復的な基準単位候補 |
| beat | 拍として数える単位候補 |
| meter | 拍のまとまりと強弱枠組み |
| accent | 強調位置の記述候補 |
| syncopation | 期待位置との差分記述候補 |
| rest | 休符・無音区間の候補 |

これらは記述体系であり、実際の演奏タイミングや身体的拍感そのものではない。

## 2. 既存検証との接続

主に接続する検証は次の通り。

| 検証 | 接続内容 |
|---|---|
| `03_単純リズム_候補集合と制約.md` | 表拍・裏拍だけの候補集合と三状態判定 |
| `25_リズム候補Module_動態Adapter第二標本.md` | observation / structural_transition / realized_transitionの第二標本 |
| `26_リズム境界変更_候補空間再構成_最小実験.md` | grid_open変更による休符候補の再構成 |
| `27〜41` | 音程Moduleとの横断不変条件、record、no_effect、再生成実行の分離 |

既存検証から受け取る最小構造は次の通り。

```text
B_4/4
  + candidate space = {表拍, 裏拍}
  + current / target condition
  ↓
candidate set
  ↓
|C| による状態判定
```

動態側は次の通り。

```text
target=休符
  ↓ closed gridではno_candidate
reopen_grid_boundary
  ↓ grid_open=True
candidate space再生成
  ↓
休符候補
```

## 3. B

このModuleの境界候補。

| 境界 | 役割 |
|---|---|
| `B_time_grid` | 時間格子、分割単位を指定する |
| `B_meter` | 4/4などの拍節枠を指定する |
| `B_candidate_vocab` | 表拍、裏拍、休符などの候補語彙を指定する |
| `B_grid_open` | 境界再開により候補語彙を拡張するかを保持する |
| `B_duration_unit` | 長さ候補を保持する |
| `B_accent_policy` | 強弱・アクセントを候補化するかを指定する |
| `B_history` | observation / structural / realized履歴を保持する |

`B_meter` と実際のアクセント、演奏タイミング、身体的拍感は同一ではない。

```text
meter
  ≠ accent
  ≠ performance timing
  ≠ groove
```

## 4. Γ

このModuleで使う候補生成・制約・投影規則。

| Γ | 入力 | 出力 |
|---|---|---|
| `Γ_rhythm_candidate` | time grid、candidate vocab | rhythm candidates |
| `Γ_change_current` | current候補、candidate set | current以外の候補 |
| `Γ_target_filter` | target条件、candidate set | 制約後候補 |
| `Γ_grid_reopen` | grid_open状態 | 境界変更record |
| `Γ_dynamic_candidate_space` | grid_open、candidate vocab | 再構成候補空間 |
| `Γ_event_projection` | Module固有record | GenericDynamicEvent |

`Γ_grid_reopen` は候補生成条件を変更しうる構造遷移であり、具体的なリズム候補採用ではない。

## 5. M_B候補

このModuleのM_B候補。

| M_B候補 | 内容 |
|---|---|
| `rhythm_candidate_set` | 現在境界内のリズム候補集合 |
| `metric_position_candidate` | 表拍・裏拍などの位置候補 |
| `rest_candidate` | 境界再開後に立ちうる休符候補 |
| `accent_candidate` | 強調位置候補 |
| `syncopation_candidate` | 期待位置との差分候補 |
| `rhythm_observation_record` | 候補評価の観測記録 |
| `rhythm_structural_transition_record` | grid reopenなどの構造遷移記録 |
| `rhythm_realized_transition_record` | 候補採用の具体遷移記録 |

休符が候補にない状態で `target=休符` が来た場合は、候補空間とtargetの衝突として扱う。

```text
target_rest no_candidate
  ≠ rest impossible
  ≠ rhythm failure
```

## 6. 候補生成・制約・選択

### 候補生成

- meterとgridから表拍・裏拍候補を生成する
- grid boundaryが開いた場合、休符などの候補を追加する
- duration候補を導入する場合は、位置候補と分けて生成する
- accent候補は位置候補とは別軸で生成する

### 制約

- current候補を変更する
- target条件を適用する
- 候補語彙に存在しないtargetはno_candidateとする
- grid reopenにより候補空間を再生成する
- 履歴をobservation / structural / realizedへ分けて保持する

### 選択

候補が一つに絞られた場合は `locally_resolved` とするが、音楽的唯一性とは読まない。

```text
|C| = 0 → no_candidate
|C| = 1 → locally_resolved
|C| > 1 → underdetermined
```

## 7. 破断条件

このModuleが破断する、または未解決ξを残す条件。

- targetが候補語彙に存在しない
- meterはあるがgrid分割が未指定である
- gridはあるがduration候補が未指定である
- 拍節位置とアクセントが一致しない
- 休符を音候補と同じ扱いにしてよいかが未確定である
- structural_transitionをrealized_transitionと混同する
- projection順を因果時系列と誤読する
- リズムModuleのgrid reopenを全Module共通fallbackにしてしまう

禁止する短絡は次の通り。

```text
meter = groove
beat = accent
rest target = no_candidateだから不可
grid reopen = concrete realization
event projection = causal sequence
rhythm adapter = Core共通controller
```

## 8. 未解決ξ

現時点で残す未解決領域。

- pulseやbeatの物理・身体的成立条件
- 演奏タイミング、揺れ、グルーヴ
- accentの生成・知覚条件
- syncopationの期待構造
- duration候補と位置候補の統合
- 休符targetの意味、無音と記譜休符の差
- 複数拍・複数小節の反復構造
- tempo変化とgridの再構成
- 動態Adapterの第三標本以降
- 因果時系列と履歴投影順の統合

これらは、旋律Module、形式Module、身体・基層仮説へ送る。

## 9. 次の最小検証

次に必要な最小検証は、リズム位置候補とduration候補を分け、同じ位置でも長さが異なる候補を扱えるかを確認することである。

```text
metric position
  ≠ duration
  ≠ accent
  ≠ rest
```

最小ケース。

| ケース | 検証したいこと |
|---|---|
| 表拍 + quarter duration | 位置と長さを別recordとして保持する |
| 表拍 + eighth duration | 同じ位置でもduration候補が分岐する |
| 裏拍 + accent | metric positionとaccentを分ける |
| rest + duration | 休符を位置・長さ・音響無音から分ける |

この検証により、リズムModuleが単なる表拍/裏拍の二候補ではなく、時間位置・長さ・アクセント・休符の束へ拡張できるかを確認する。

## 10. 現時点の短縮式

```text
リズム・拍節Moduleは、
拍節ラベルを演奏タイミングへ直結せず、
time grid・candidate vocab・境界変更・履歴を通して
リズム候補を扱う。

拍節、アクセント、グルーヴはまだ同一視しない。
```
