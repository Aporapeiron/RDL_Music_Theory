# 検証記録：二標本における空結果のModule固有位置

*対象：32の音程Module、33のリズムModule*  
*状態：DRAFT v0.1 / 空結果位置の横断観測*

---

## ■ 0. 目的

32・33はいずれも、構造遷移record由来の再生成処理を実行した後に最終結果が空となる標本である。

34は、両者を単一の`empty`原因へ潰さず、実際にどのModule固有段階で空になったかを比較する。

## ■ 1. 実測

| Module | 生候補 | 最終候補 | Module側から直接読む根拠 |
|---|---:|---:|---|
| 音程 | 各再探索枝で音候補を生成 | 0 | `B_range_projection` |
| リズム | `raw_candidate_space_count=3` | 0 | 現在値`休符`の除外と`target=休符`の制約交差 |

音程32では、各`ActionObservation.observation.failure_stage`から`B_range_projection`を直接読む。voice Bの生成候補`F♯4`は存在するが、G4–G4というresulting boundaryの範囲投影で除外される。リズム33では、実行recordが保持する`current=休符`、`change_current=True`、`target=休符`と、構造遷移後の候補空間`(表拍, 裏拍, 休符)`および制約後の空候補を読む。

```text
pitch
  generated pitch candidates
  → B_range_projection
  → empty

rhythm
  raw candidate space
  → current exclusion + target constraint
  → empty
```

## ■ 2. 確定範囲

二標本で確認したのは、次の観測である。

```text
再生成処理はexecutedであり、
生候補が存在しても、Module固有の後続段階で最終結果はemptyになり得る。
```

ここから共通の`generation_empty`、`constraint_empty`、`selection_empty`を定義しない。34が保持するのは、各Module側の直接観測と入力条件であり、音程の`B_range_projection`とリズムの制約交差は同じ内部段階であることを確認していない。

## ■ 3. 未解決ξ

- 生候補そのものが空となる構造遷移標本
- 音程の`Γ_ordering`で空となる構造遷移標本
- 各Module固有の空位置を比較するために必要な最小投影境界
- 空位置の共通語彙が必要になる反例の数

共通状態・共通候補生成器・共通empty分類・共通controllerは追加しない。
