# 検証記録：同一音程fallback遷移と空の候補再生成

*対象：音程Moduleの`FallbackStateTransition`*  
*状態：DRAFT v0.1 / 構造遷移後の空再生成検証*

---

## ■ 0. 目的

31では、構造遷移recordから再生成処理へ接続できることと、候補が非空になることを分離した。

32では、実際に状態条件を変える同一`FallbackStateTransition`を、イベント投影と候補再生成へ通す。ただし再生成結果は空のまま残す。

```text
FallbackStateTransition
  voice B boundary: F4–F4 → G4–G4
  ├─ project_fallback
  │    → structural_transition / not_realized
  └─ state_after_transition
       → observe_actions
       → empty
```

## ■ 1. 実差分

recordは`source_voice_b_boundary`と`resulting_voice_b_boundary`を実体として保持する。

```text
source    F4–F4
resulting G4–G4
```

したがって、操作は`applied`であり、`boundary_changed`が記録される。`shift_voice_B_boundary_to_G4`という操作名から変更内容を推定せず、recordの前後境界を`state_after_transition()`へ渡す。

## ■ 2. 再生成結果

結果状態で既存の三操作を再観測する。

| 枝 | 観測結果 |
|---|---|
| `B_change` | `constraint_no_candidate` |
| `Γ_change` | `constraint_no_candidate` |
| `upstream_target_change` | `constraint_no_candidate` |

`regeneration_status=executed`、`regenerated_count=0`である。空観測は評価・具体実現へ進まず、20〜21と同様に候補消滅の診断として残る。

## ■ 3. 確定範囲

```text
構造遷移recordの実差分
  → structural_transitionへの投影
  → record由来の再生成処理
  → empty
```

ここで確認したのは、構造遷移後も候補が必ず復帰するわけではないことだけである。空結果は接続の失敗、操作の`no_effect`、またはGenericDynamicEventによる候補生成を意味しない。

## ■ 4. 未解決ξ

- 空の構造遷移後にどのfallbackを選ぶか
- G4境界を採用しうる上位条件
- 複数条件の同時差分をどこまでrecordへ保存するか
- 空結果を含む第三標本での接続形式の再現

共通Adapter・共通状態・共通候補生成器・共通controllerは追加しない。
