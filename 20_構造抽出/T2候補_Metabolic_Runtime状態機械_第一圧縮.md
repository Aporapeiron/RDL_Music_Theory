# T2候補 Metabolic Runtime状態機械 第一圧縮

## 位置づけ

`RDL_Music_Theory_既存検証_A_B_C分類_第一段階.md` のB分類を、工程番号列から切り離し、T2候補の最小状態機械として圧縮する。

これはRDL_Modulesへ正式移植する仕様ではない。

```text
Music起源のB分類
↓
反復する状態
↓
transition / guard / stop line
↓
T2候補骨格
```

## 抽出単位

```text
state
transition
guard
stop line
input
output
ξ
```

工程番号、音楽語彙、Module名は、ここではfixture由来の痕跡として扱い、状態機械のprimitiveにはしない。

## 第一圧縮状態列

```text
Input
↓
Bound
↓
Validated
↓
Candidate
↓
Evaluated
↓
Selected
↓
CommitmentReady
↓
CommitmentAttempted
↓
Committed
↓
Recorded
↓
AlternativeRetained
↓
Reactivated
↓
ConflictObserved
↓
Mediated
↓
OutcomeObserved
↓
ReentryReady
↓
NextInput
```

この列は3398工程から抜いた第一圧縮であり、最終的な最小状態機械ではない。

すべての実行で `commitment`、`conflict`、`mediation`、`alternative memory` が必須になるとは限らない。これらは主幹Runtimeに常時含まれるprimitiveではなく、必要時に接続されるMechanism branchとして再圧縮される可能性がある。

## 主幹候補と任意branch

現時点のより小さい主幹候補は以下である。

```text
Input
↓
Bound
↓
Validated
↓
Candidate
↓
Evaluated
↓
Recorded / Updated
↓
ReentryReady
↓
NextInput
```

必要時に接続されるbranch候補:

```text
Selection branch:
  Evaluated
  ↓
  Selected
  ↓
  CommitmentReady
  ↓
  CommitmentAttempted
  ↓
  Committed

Alternative branch:
  Candidate / Selected / Recorded
  ↓
  AlternativeRetained
  ↓
  Reactivated

Conflict mediation branch:
  Reactivated / Recorded
  ↓
  ConflictObserved
  ↓
  Mediated
  ↓
  OutcomeObserved
```

したがって第一圧縮状態列は、単線の実行命令ではなく、分岐、保留、非合流、再入を許す状態配置である。

## 遷移

```text
Input -> Bound
  input payloadが境界Bまたはcontractへ束縛される。

Bound -> Validated
  inputが現行境界で読めるかを検査する。

Validated -> Candidate
  処理対象を候補集合として生成する。

Candidate -> Evaluated
  候補が重み、優先度、条件、文脈圧によって評価される。

Evaluated -> Selected
  controllerが選択結果を作る。

Selected -> CommitmentReady
  選択結果がcommitment可能か検査される。

CommitmentReady -> CommitmentAttempted
  commitmentを試行するが、まだrecordやfinalではない。

CommitmentAttempted -> Committed
  採用が成立する。ただし未選択候補は消えない。

Committed -> Recorded
  commitmentの痕跡をrecord化する。

Recorded -> AlternativeRetained
  record後もalternative memoryを保持する。

AlternativeRetained -> Reactivated
  後続文脈により保持候補が再活性化される。

Reactivated -> ConflictObserved
  既存commitmentやrecordと衝突する場合、conflictとして観測する。

ConflictObserved -> Mediated
  conflictを即時resolutionにせず、mediationへ渡す。

Mediated -> OutcomeObserved
  mediationの結果を観測する。

OutcomeObserved -> ReentryReady
  次のinputまたはcycleへ戻れる形に束ねる。

ReentryReady -> NextInput
  next ξを保持して次の入口へ渡す。
```

## guard

各遷移は、少なくとも以下のguardを持つ。

```text
has_input
has_boundary
has_contract_if_required
validation_passed_or_failure_recorded
candidate_set_available_or_empty_recorded
evaluation_policy_available
selection_controller_available
commitment_readiness_confirmed
record_boundary_available
alternative_memory_policy_available
reactivation_context_available
conflict_detection_boundary_available
mediation_controller_available
outcome_observation_boundary_available
reentry_target_available
```

guardがない場合、遷移を実行せず、failureまたはpendingとして記録する。guard不足をそのままξへ同一視しない。停止状態を現在のBで記述してもなお未回収の関係が残る場合だけ、ξとして保持されうる。

## stop line

B分類から残る停止線は以下である。

```text
input ≠ validation
validation ≠ processing
candidate ≠ selected
selected ≠ committed
commitment attempt ≠ commitment record
committed ≠ recorded
recorded ≠ final
record ≠ rewrite
unselected ≠ deleted
alternative retained ≠ resolution
reactivated ≠ contradiction resolved
conflict observed ≠ conflict resolved
mediation ≠ closure
outcome observed ≠ final truth
diagnostic ≠ update
plan ≠ execution
handoff ≠ next execution
reentry ≠ terminal closure
```

## 入力と出力

```text
input:
  payload
  boundary B
  contract if required
  context
  prior record
  controller
  policy

output:
  state transition record
  selected item
  commitment trace
  record
  retained alternative memory
  conflict observation
  mediation outcome
  next ξ
```

## ξ

この状態機械では、ξを失敗やノイズとして扱わない。

```text
ξ =
  有限境界Bを引いたことに伴って残る未回収関係
```

guard不足、未選択候補、後続文脈待ちのalternative、conflict未解決成分、reentry先未確定成分は、それ自体が直ちにξではない。

```text
guard不足
↓
failure / pendingとして記録
↓
その停止状態を現在のBで記述してもなお未回収の関係が残る
↓
ξとして保持されうる
```

同様に、未選択候補そのものはξではない。未選択候補を現在の処理で回収しきれず、有限境界Bの外側または境界上に残る関係がある場合に、ξとして保持されうる。

ξは次の入力、別boundary、別controller、別fixtureで再回収されうるが、処理できなかったもの全体を入れる箱ではない。

## Music fixtureとの関係

この骨格はMusicから抽出されたが、Music固有理論ではない。

Music側に残るfixture:

```text
音程 target selection
voice leading
和声機能
拍節・リズム
調律から音程綴り
複数解釈保持
refrain / variation / memory
```

これらは、状態機械が対象固有性を潰さずに動くかを検査するために残す。

## 昇格前の破断条件

T2正式昇格前に、以下で壊れるか確認する。

```text
Music語彙を外すと状態が定義できない。
input / output が対象依存すぎて分離できない。
guardが音楽固有規則そのものになる。
stop lineがT1またはT0を再定義してしまう。
非Music対象で同型に動かない。
ξを残せず、全てをresolutionへ潰してしまう。
```

## 第一圧縮の結論

B分類は、現時点では以下のT2候補として読める。

```text
Metabolic Runtime =
  bounded input
  validation
  candidate lifecycle
  selection control
  commitment
  record
  alternative memory
  reactivation
  conflict mediation
  outcome observation
  reentry / handoff
```

次段階では、この骨格を非Music対象に食わせ、主幹として残る状態と、任意branchとしてのみ残るMechanismを分けて検査する。
