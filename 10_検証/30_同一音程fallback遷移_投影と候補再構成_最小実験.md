# 検証記録：同一音程fallback遷移の投影と候補再構成

*対象：22の`FallbackStateTransition`を、24の投影と19の候補再生成へ同一recordとして接続する*
*状態：DRAFT v0.1 / 音程Module候補・最小接続検査*
*実装：`10_検証/pitch_transition_projection_reconstruction.py`*

---

## ■ 0. 目的と範囲

28ではリズムModuleで、同一の`BoundaryTransition`を構造遷移イベントへの投影と候補再構成へ通した。

30は、音程Moduleでも同じ**形式**を比較できるかを検査する。ただし、境界の意味・候補生成器・候補の形はリズムModuleと統一しない。

```text
音程Moduleの同一 FallbackStateTransition
  ├─ 24の project_fallback
  │    → structural_transition event
  └─ recordが保存した voice B 境界の実差分
       → 19の候補再生成器
       → 次の有効枝の再観測
```

共通Adapter、共通状態、共通候補生成器、fallback選択controller、Module間の因果順序は追加しない。

## ■ 1. recordを候補生成条件として読めるようにする最小補足

22の`FallbackStateTransition`は、従来は再開後のvoice B境界を表示文字列として記録していた。30では、候補生成条件としても読めるよう、Module固有の前後境界をそのまま保持する。

```text
source_voice_b_boundary
resulting_voice_b_boundary
```

これは状態意味をAdapterへ移したものではない。`RealizationBoundary`は音程Module側のままであり、30の再生成器も音程Moduleの`observe_actions()`を使う。

## ■ 2. 同一recordの二経路

22の枯渇状態から採用されるrecordは、次を持つ。

```text
fallback_kind = reopen_voice_B_boundary
operation_status = applied
source voice B boundary = F4–F4
resulting voice B boundary = F♯4–F♯4
change_axes.boundary_changed = True
```

30はこの一件を一度だけ取得する。

```text
FallbackStateTransition
  ├─ project_fallback
  │    → event_kind = structural_transition
  │    → operation_kind = reopen_voice_B_boundary
  │    → realization_status = not_realized
  └─ source stateへrecordのresulting_voice_b_boundaryを反映
       → observe_actions
       → B_change / upstream_target_change が有効枝として再出現
```

後者では、操作名から再開を推定しない。source state IDとsource境界がrecordと一致することを検査したうえで、recordの`resulting_voice_b_boundary`だけを反映する。

## ■ 3. 実測

再観測された有効枝と具体候補は次のとおりである。

| 有効枝 | 具体候補 |
|---|---|
| `B_change` | `A♯3–F♯4` |
| `upstream_target_change` | `E♯4–F♯4` |

`Γ_change`は候補を得ないままである。この差は、voice B境界の再開だけで全操作が実現可能になったことを意味しない。

## ■ 4. ここで閉じたこと

今回、音程Moduleでは次の限定命題が成立した。

```text
一つのFallbackStateTransition recordは、
構造遷移イベントへの投影と、
そのrecordが持つ実境界差分による後続候補再生成の双方へ接続できる。
```

28のリズムModuleと合わせ、次の形式は二標本で比較できる。

```text
Module固有の構造遷移record
  → Module固有projectorによる structural_transition
  → recordのresulting conditionを使うModule固有候補生成
```

## ■ 5. 導かれないこと

30は次を示さない。

```text
音程とリズムが同じ境界を持つこと
候補生成規則や候補集合が同じこと
structural_transition一般が必ず候補空間を変えること
共通projector・共通状態・共通候補生成器を実装できること
fallbackの選択理由や、二経路の因果順序
```

具体音をこのfallback自身が実現したわけでもない。`realization_status = not_realized`のまま、後続候補の条件だけを変えた構造遷移として保存する。

## ■ 6. 未解決ξ

```text
recordが表せない複合状態差分をどう扱うか
複数の構造遷移recordをどの順序で適用するか
候補再生成後の有効枝から何を採用するか
共通形式に必要な入出力契約と許容差分
```

30は、二標本で同じ分類契約と接続形式を観測した段階に留める。
