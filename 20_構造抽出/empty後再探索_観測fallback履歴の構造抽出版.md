# empty後再探索｜観測・fallback・履歴の構造抽出版

*対象：音程Moduleの16〜22で観測した、empty後の再探索経路*  
*状態：DRAFT v0.1 / 音程Module固有の動態構造*

## ■ 0. 位置づけ

本書は、候補が空になった後の操作候補、枯渇診断、fallback、通常探索への復帰を抽出する。fallbackの選択原理や動態Adapterへの投影は扱わない。

## ■ 1. emptyから再探索まで

```text
current state
  ↓ current action setを列挙
各actionを同じsource stateから独立評価
  ├─ candidateあり
  │    → evaluation / policy
  │    → 採用された場合のみ concrete realization
  └─ empty
       → observation history
       → 別actionを評価
```

`B_change`、`Γ_change`、`upstream_target_change`は、候補空間を一つに復旧する同義操作ではない。実際の変更軸は操作名ではなく状態差分から読む。

```text
操作した ≠ 候補が生まれた ≠ 比較可能 ≠ 採用された
```

## ■ 2. 枯渇とfallback

```text
列挙済みaction set
  └─ 一手先の全枝がempty
       → action_set_exhausted
       → fallback outcomeを比較観測
            ├─ stop_search
            ├─ reopen_voice_B_boundary
            └─ discard_target
```

これは可能な操作全体の消滅ではない。同じsource stateから列挙した、現在のaction setに限る枯渇診断である。

fallback outcomeは直ちに正式な次状態ではない。`stop_search`と`discard_target`は観測として残り、`reopen_voice_B_boundary`だけが次節の限定例で実状態へ採用される。

## ■ 3. fallback採用と通常探索への復帰

```text
S_empty
  ↓ reopen_voice_B_boundary
S_boundary_reopened
  ├─ fallback_transition_history +1
  └─ realized_transition_history +0
       ↓ 新しいstateからaction setを再生成
       ↓ ordinary actionを採用
S_realized
  └─ realized_transition_history +1
```

境界再開は具体音の実現ではない。候補生成条件を変える構造状態の更新であり、具体音を採用した後の履歴とは分ける。

## ■ 4. 履歴の三断面

```text
observation_history
  actionを評価した観測（emptyを含む）

fallback_transition_history
  fallbackを採用して構造条件だけを変えた記録

realized_transition_history
  ordinary actionを採用して具体音まで実現した記録
```

```text
候補を見た ≠ 構造状態を変更した ≠ 具体音を実現した
```

## ■ 5. 確定接続・ξ・禁止補完

**確定接続**：empty観測を残したまま、列挙済みaction setの枯渇を診断し、境界再開fallbackを実状態へ採用して通常探索へ戻せる。

**未解決ξ**：fallbackを選ぶcontroller、停止後の接続、target破棄後の状態と次target、制約緩和順序、探索終端。

**禁止補完**：emptyを全操作失敗と読まない。fallbackを自動的な正解としない。fallback採用を具体音実現と混同しない。音程Module固有のaction集合と履歴をCoreへ上げない。
