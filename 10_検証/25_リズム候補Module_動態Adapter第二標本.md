# 検証記録：リズム候補Moduleの動態Adapter第二標本

*対象：表拍・裏拍だけを持つ単純リズム候補Module*  
*状態：DRAFT v0.1 / Adapter横断候補の検証*  
*実装：\`10_検証/rhythm_dynamic_adapter.py\`*

---

## ■ 0. 検証目的

24で音程Moduleから抽出した、次の三つの共通イベント境界が、別の候補Moduleでも成立するかを確認する。

\`\`\`
observation
structural_transition
realized_transition
\`\`\`

今回のリズム側は、4/4・一定グリッド上の\`表拍 / 裏拍\`だけを候補とする。既存の候補集合実験を動態化するが、音程Moduleの\`B\`・\`Γ\`・音度・声部・状態意味は導入しない。

目的は、リズム理論を新設することでも、音程Moduleと同じ内部状態を作ることでもない。Module側の異なる記録を、共通イベント境界へ投影できるかを検査することである。

---

## ■ 1. リズム側の最小記録

リズム側では、次の三種類の記録を用意した。

\`\`\`
RhythmActionAttemptRecord
  → 操作を評価・観測した記録

RhythmStructuralTransition
  → fallbackでグリッド境界を変更した記録

RhythmRealizedTransition
  → 候補を具体的に採用した記録
\`\`\`

操作名はリズムModule内の識別子であり、Adapterは意味を解釈しない。操作名は共通イベントの\`operation_kind\`へ不透明値として保存される。

\`\`\`
change_current
target_rest
reopen_grid_boundary
select_offbeat
\`\`\`

---

## ■ 2. 検証経路

\`\`\`
R0
  → change_current を観測
  → 裏拍を具体実現
  → R1
  → target=休符で空候補を観測
  → reopen_grid_boundary
  → R2
\`\`\`

\`target=休符\`は候補空間に存在しないため、既知の\`no_candidate\`観測になる。空候補そのものを未解決ξとは扱わず、その後のfallback採用を別記録にする。

fallbackはグリッド境界の変更だけで、具体候補の実現ではない。したがって、\`structural_transition\`へ入り、\`realized_transition\`へは入らない。具体候補の採用記録は別の\`realized_transition\`として保持する。

---

## ■ 3. 共通イベントへの投影

| リズム側の記録 | 共通イベント | 保持するModule情報 |
|---|---|---|
| \`RhythmActionAttemptRecord\` | \`observation\` | \`branch_kind → operation_kind\` |
| \`RhythmStructuralTransition\` | \`structural_transition\` | \`fallback_kind → operation_kind\` |
| \`RhythmRealizedTransition\` | \`realized_transition\` | \`selected_branch_kind → operation_kind\` |

共通化されたのはイベントの境界だけである。候補の意味、fallbackの権限、次の操作、状態の意味は共通化していない。

\`\`\`
共通化したもの
  何を記録の種類として扱うか

共通化していないもの
  なぜその操作を選ぶか
  状態が何を意味するか
  次に何を選ぶか
  Module間の因果順序
\`\`\`

---

## ■ 4. 実測結果

\`rhythm_dynamic_adapter.py\`の検査では、次を確認した。

\`\`\`
observation             2
structural_transition   1
realized_transition     1
\`\`\`

また、次の\`operation_kind\`が消失せず保持される。

\`\`\`
change_current
target_rest
reopen_grid_boundary
select_offbeat
\`\`\`

\`target_rest\`による空候補観測は\`observation\`として残り、\`reopen_grid_boundary\`は\`structural_transition\`として残る。両者を一つの「失敗」へ潰していない。

ただし、この検証での\`reopen_grid_boundary\`は構造遷移の記録を作った段階に留まり、候補生成器へ境界変更を接続していない。したがって、\`structural_transition\`が実際に候補空間を再構成することまでは検証していない。

---

## ■ 5. 投影順と時系列

\`project_state()\`の出力は、音程Moduleと同じく、

\`\`\`
observation_history
↓
fallback_transition_history
↓
realized_transition_history
\`\`\`

という履歴チャンネル別の投影順である。これは実際の因果・時系列順を意味しない。

したがって、この第二標本だけから次を導入しない。

\`\`\`
sequence_id
event_id
caused_by
\`\`\`

Module間の時系列再構成は、別の検証対象として未解決ξへ残す。

---

## ■ 6. 暫定結論

表拍・裏拍だけのリズム候補Moduleでも、24の三分類、すなわち

\`\`\`
observation
structural_transition
realized_transition
\`\`\`

を、音程Moduleの内部状態を導入せずに再現できた。

よって、現時点ではこの三分類を**Module横断Adapterの候補境界**として扱える。ただし証拠は音程Moduleと単純リズムModuleの二標本に限られる。AdapterをCoreへ昇格させず、第三のModule、または異なる履歴形式による反例検証を残す。

この検証はイベント境界の再現を示すだけであり、音楽一般の動態法則、候補選択の共通原理、因果順序の再構成を示さない。
