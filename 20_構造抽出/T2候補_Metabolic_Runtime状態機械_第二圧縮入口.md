# T2候補 Metabolic Runtime状態機械 第二圧縮入口

## 位置づけ

`T2候補_Metabolic_Runtime状態機械_第一圧縮.md` をさらに削り、T1に近すぎる主幹と、T2固有の実行機構を分ける。

第二圧縮では、第一圧縮で主幹候補に残っていた以下を優先的に壊す。

```text
Input -> Bound
Validation
Record / Update
```

## 破断対象1: Input -> Bound

第一圧縮:

```text
Input
↓
Bound
```

第二圧縮では、Bなしのinputが先に成立するとは扱わない。

T0では、観測・記述・操作そのものが有限境界Bを必要とする。したがって、Runtimeの入口は以下へ圧縮する。

```text
B + incoming relation / signal / request
↓
BoundedInput
```

または、

```text
BoundedInput
```

として扱う。

`Bound` は独立した後続stateというより、Runtime成立条件に近い。

## 破断対象2: Validation

第一圧縮:

```text
BoundedInput
↓
Validated
↓
Processable State
```

第二圧縮では、validationを必須stateではなく、transition guardまたはdiagnosticへ落とせるかを検査する。

T1/T0では、必ずしも入力をvalid / invalidへ先に分けない。

```text
BoundedInput
↓
State Formation / Interpretation
```

として、読める、読みにくい、読めない、差分が出る、破断する、という結果を状態形成側で保持できるかを確認する。

```text
validation
≠ Runtime trunk state確定
validation
= guard / diagnostic / failure record候補
```

## 破断対象3: Record / Update

第一圧縮:

```text
Test / Compare
↓
Recorded / Updated
```

第二圧縮では、recordとupdateを同一stateに置かない。

```text
Test / Compare
      ↓
 ┌────┴────┐
Maintain   Update / Reconstruct
      │       │
      └──┬────┘
         ↓
       Reentry

Record
= transition trace / observation history
```

recordは代謝そのものではなく、代謝を保持する観測・履歴機構である可能性が高い。

したがって、第二圧縮では以下を分ける。

```text
Maintain
  現行構造を維持する。

Update / Reconstruct
  現行構造を変える。

Record
  維持または更新の痕跡を保持する。
```

## 第二圧縮主幹候補

現時点でより硬い主幹候補:

```text
BoundedInput
↓
StateFormation / Interpretation
↓
Test / Compare
↓
Maintain / Reconstruct
↓
Reentry
```

これはT1の以下に近い。

```text
SILN展開
↓
検査・選別
↓
再構成
↺
```

ただし、T2 RuntimeはT1を再定義しない。

T2は、この主幹を有限実行可能にするために、どのtransitionでどのMechanismを接続するかを扱う。

## T2 Mechanism候補

主幹に常時含めない候補:

```text
contract
validation diagnostic
candidate lifecycle
selection controller
commitment
record trace
alternative memory
reactivation
conflict detection
mediation
outcome observation
handoff protocol
```

これらは、対象や状況に応じてtransitionへ接続される交換可能Mechanismとして扱う。

## 第二圧縮の検査問い

非Music耐久検査では、まず以下を壊す。

```text
1. BoundedInputだけで入口を定義できるか。

2. Validationをstateではなくguard / diagnosticへ落とせるか。

3. CandidateをProcessableStateへ圧縮できるか。

4. EvaluatedをTest / Compareへ圧縮できるか。

5. RecordをMaintain / Reconstructから分離し、trace mechanismへ落とせるか。

6. Selection / Commitmentなしでも主幹が回るか。

7. Alternative Memory / Reactivation / Mediationなしでも主幹が回るか。

8. それらが必要な対象では、branch mechanismとして後付けできるか。
```

## ξの扱い

第二圧縮でも、ξは処理不能一般ではない。

```text
ξ =
  有限境界Bを引いたことに伴って残る未回収関係
```

次をξへ直結しない。

```text
guard不足
invalid
unselected
pending
unresolved
unrecorded
```

これらはまずruntime state、diagnostic、trace、pendingとして扱う。

その上で、現在のBで記述しても未回収の関係が残る場合だけ、ξとして保持されうる。

## 結論

第一圧縮は3398工程からT2候補を剥がした段階だった。

第二圧縮入口では、さらにMusic履歴由来のstateを削り、以下の区別を前面に出す。

```text
T1
  循環の位相構造

T2 Runtime trunk
  T1位相を有限実行可能にする最小骨格

T2 Mechanisms
  transitionごとに必要時接続される実行機構
```

次段階では、この第二圧縮主幹を非Music対象へ適用し、何が主幹として残り、何がMechanism branchへ落ちるかを検査する。
