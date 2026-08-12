# RDL Music Theory

RDL音楽理論の検討・設計・検証を行うリポジトリ。

## 初期構成

```text
00_RDL音楽理論.md
    入口・全体構造・運用方針

01_RDL音楽_Core.md
    音楽領域で共通して使う最小の状態記述と操作

02_RDL音楽_文書地図.md
    文書の役割・依存関係・分岐条件

03_RDL音楽_全体設計方針.md
    物理・基層・中核・上層を接続する設計原則

10_検証/
    Coreを実例で検証する記録と実験用スクリプト
```

全体の設計方針は `03_RDL音楽_全体設計方針.md` に置く。具体的な調律・和声・旋律・リズム・楽式などは、Coreへ集積せず、必要になった時点で検証結果とともに分岐させる。`M_B`は現在のBで維持される関係構造として保ち、`M_B候補`はBとΓのもとで行う検証上の暫定判定として扱う。ΓはCoreの状態変数ではなく、Adapter・Module・検証系に置く。

## 現時点の検証対象

- C majorの候補集合と制約
- 単純リズムの候補集合と制約
- 音楽語彙を使わない候補集合の状態判定（現範囲の検証完了）
- 候補集合と制約の一般的な状態判定と、RDL固有の境界生成の分離
- Bと生成規則Γを分離した候補空間生成の最小実験
- 音名・コード・調性より下位の、2本の正弦波による波形関係抽出の最小実験
- 絶対周波数が変化する中で保存される比の、2成分波形による最小実験

現在の基礎検証：`10_検証/02_C_major_候補集合と制約.md`

実験用スクリプト：`10_検証/c_major_operations.py`

別領域の最小検証：`10_検証/03_単純リズム_候補集合と制約.md`

実験用スクリプト：`10_検証/rhythm_candidate_operations.py`

純粋な候補集合の検証（一般実験・現範囲で完了）：`10_検証/04_純粋候補集合_状態判定.md`

実験用スクリプト：`10_検証/generic_candidate_operations.py`

`B + M_B + Γ → C(B, M_B;Γ)`の音楽側固有部分の最小検証：`10_検証/05_Bから候補空間生成_最小実験.md`

実験用スクリプト：`10_検証/boundary_candidate_generation.py`

波形関係から`M_B`候補が立ち上がる条件の最小検証：`10_検証/06_波形関係_二正弦波_最小実験.md`

実験用スクリプト：`10_検証/two_sine_wave_relations.py`

時間変化する2成分の関係保存：`10_検証/07_波形関係_時間変化する二正弦波_最小実験.md`

実験用スクリプト：`10_検証/time_varying_two_sine_wave_relations.py`

短時間の関係破断と観測分解能：`10_検証/08_波形関係_短時間破断と観測分解能_最小実験.md`

実験用スクリプト：`10_検証/short_ratio_break_resolution.py`

観測格子の開始位相と破断検出：`10_検証/09_波形関係_観測格子位相と破断検出_最小実験.md`

実験用スクリプト：`10_検証/sampling_phase_ratio_break.py`

音程分解・周波数比から12TET半音数までの最小接続検査：`10_検証/10_音程分解_周波数比から12TET半音数_最小実験.md`

実験用スクリプト：`10_検証/interval_fifth_decomposition.py`

既知音楽理論を`M_B^learned`の観測資料として置き、純正五度と12TETの7半音を、周波数比・セント座標・12TETカテゴリーへ分解する最初の接続検査である。音程名への接続は扱わず、物理的に異なる比が同じ記述カテゴリーへ写ることを確認する。これを人間の知覚結果とは扱わない。

同一7半音と綴りによるP5／d6分岐：`10_検証/11_音程分解_同一7半音と綴り_P5_d6_最小実験.md`

実験用スクリプト：`10_検証/spelled_interval_divergence.py`

`C4 → G4`、`C♯4 → A♭4`、`C4 → A𝄫4`を比較し、同じ周波数比・cents・7半音が、音名上のgeneric intervalと音程品質によってP5／d6へ分岐することを検査する。特に`C4 → G4`と`C4 → A𝄫4`では物理音高対そのものを同一にし、音名・綴り情報を比較関係として保持するBの追加だけでラベルが分岐する。音程名を周波数比だけから導かず、音名・綴りをlearned側の追加構造として扱う。

同一トライトーンと綴りによる解決方向：`10_検証/12_音程分解_同一トライトーンと綴りによる解決方向_最小実験.md`

実験用スクリプト：`10_検証/tritone_spelling_resolution.py`

`F4 → B4`と`E♯4 → B4`を比較し、12TET物理モデル上の同一音高対・同じ6半音が、綴り情報によってA4／増四度とd5／減五度へ分岐することを検査する。さらに、learned側の代表的解決候補を外部から与え、そのtargetに対する二声部の移動を比較する。A4側は外へ開き、d5側は内へ狭まるが、これはラベルから自動的に導かれる法則ではない。綴りからtarget候補への対応と、targetからmotionへの記述を分離し、既知音楽理論を遷移`M_B`として読むための最小検証として閉じる。

解決候補の文脈分解：`10_検証/13_音程分解_解決候補の文脈分解_最小実験.md`

実験用スクリプト：`10_検証/contextual_resolution_candidate.py`

12で外部入力していたtarget候補を、文脈・音度役割・learned側の代表的進行規則・綴り付きの音高実現へ分解して保持する。`A4 / d5 → target`をラベル単独の規則として生成したものとは扱わず、既選択targetへ`M_B^context`と`M_B^learned`の注釈を対応させ、その後の`target → Γ_motion`を機械的に抽出する。機能和声全体、具体的targetの生成規則、候補選択確率、知覚モデル、文化横断的な法則は扱わず、Coreへ追加しない。

音度から具体音への実現：`10_検証/14_音程分解_音度から具体音への実現_最小実験.md`

実験用スクリプト：`10_検証/degree_to_pitch_realization.py`

13で未分解だった`目標音度 → 具体音`の間に、`B_realization`による候補オクターブ・声部範囲の境界、`Γ_spelling`による綴り付き候補生成、`B_range_projection`による範囲通過候補の抽出、`Γ_ordering`による上下関係を満たす候補対の構成、`Γ_select`による最小移動の選択を置く。`7→1`だけでは`F♯3 / F♯4 / F♯5`を区別できず、明示した実現規則によって`F♯4`が選ばれることを検査する。目標音度は13から引き継いだlearned tendencyの結果として扱い、14単独の新規検証とはしない。これは一つの限定的な実現規則であり、機能和声や人間の音楽的選択の一般モデルには拡張しない。

実現制約の競合と候補消滅：`10_検証/15_音程分解_実現制約の競合と候補消滅_最小実験.md`

実験用スクリプト：`10_検証/constraint_competition_observation.py`

14の実現段階で、候補がどこで消えるかを観測する。通常ケース、両声部には候補が残るが`Γ_ordering`で候補対が消えるケース、`B_range_projection`で片側候補が消えるケースを比較し、`generated / filtered / admissible / selected / failure_stage / status`を分けて保持する。空集合は、既知の制約診断である`constraint_no_candidate`または`no_admissible_candidate`として記録し、音楽一般の不可能性や、直ちにBを引き直す根拠とは扱わない。Bの引き直し・制約緩和・別の候補生成Γへの切替は未解決ξとして残す。

`10_検証/01_C6とAm7.md` は過去チャット由来の題材であり、履歴作用を含む後順位候補として保持する。

候補集合への制約適用は一般的な道具として切り分け、純粋候補集合の一般実験は現範囲で閉じる。RDL音楽側では、`F_wave → B → 複数の関係抽出 → 保存関係ごとのM_B候補群`と、`B + M_B + Γ → C(B, M_B;Γ)`、候補空間外の`ξ`、`B`の引き直しを検証対象とし、調性・和声Moduleは正式化しない。

空集合後の再探索分岐：`10_検証/16_音程分解_空集合後の再探索分岐_最小実験.md`

実験用スクリプト：`10_検証/reexploration_after_empty.py`

15で導入した`no_admissible_candidate`という診断形式を引き継ぐ初期空集合から、`B_change`・`Γ_change`・`upstream_target_change`を別分岐として適用する。14の既存`lower / upper`フィールドは16では声部IDの枠として扱い、物理的な上下は`pitch_ordering_rule`で分離する。B変更とΓ変更は実現層内の変更であり、B変更では候補オクターブ・声域を開き、Γ変更ではcrossed voice pitchesを比較対象へ含める。`upstream_target_change`は上流から与えられたtarget入力を差し替えて実現層を再実行する境界を観測する。各枝には`boundary_changed`・`relation_changed`・`upstream_target_changed`を`change_axes`として明示保持し、`branch_kind`から変更内容を逆算しない。各分岐が異なる候補集合と具体targetへ戻ることを確認するが、どの分岐を優先・採用すべきかは決めない。分岐の優先順位、採用条件、打ち切り条件は未解決ξとして残し、音楽一般の再探索順序やCoreの操作へ昇格させない。

再探索分岐の優先順位と採用条件：`10_検証/17_音程分解_再探索分岐の優先順位と採用条件_最小実験.md`

実験用スクリプト：`10_検証/reexploration_policy_comparison.py`

16で得られた三分岐へ、異なる保存条件と比較順を持つ探索方針を適用する。実音高移動量と、16から引き継いだ`change_axes`（境界変更・関係規則変更・上流target変更）を別軸で記録し、重み付き総合点へ潰さない。targetを維持する方針、厳密な実音高順序を維持する方針、即時移動量を最小にする方針が、それぞれ別の枝を採用することを検査する。これは採用条件がなければ空集合後の枝を一意に選べないことの最小検証であり、方針そのものの起源、履歴更新、打ち切り条件は未解決ξとして残す。

採用枝から次状態への履歴controller接続：`10_検証/18_音程分解_採用枝から次状態への履歴循環_最小実験.md`

実験用スクリプト：`10_検証/history_aware_reexploration_cycle.py`

17の採用枝を`StateTransition`として次状態へ反映し、履歴に保持した`change_axes`に応じて次回の`SearchPolicy`を選ぶ。直前に境界だけを変更した場合は厳密関係優先、上流targetだけを変更した場合は即時移動量優先という暫定controllerを明示する。ただし候補枝は初期seedから一度だけ作る固定メニューであり、18は履歴controllerの接続検査として二回の遷移後に閉じる。方針更新規則自体は音楽一般へ拡張せず、`M_B`と`Γ`を持つ検証Module内の仮設として保持する。

状態からの再探索枝再生成：`10_検証/19_音程分解_状態からの再探索枝再生成_最小実験.md`

実験用スクリプト：`10_検証/state_rebased_reexploration.py`

18の固定枝メニューを操作候補へ置き換え、`B・Γ・target`を含む現在状態へ毎回適用する。具体音の移動基準は`last_realized_pair`へ一本化し、初期seedの開始音を保持した後、採用された候補へ更新する。これは現在の`B`で有効なペアを保証する名前ではなく、最後に具体音として実現したペアを基準点として保持するための名称である。したがって次回の`Γ_select`も初期seedではなく`state_t`の最後に実現した音高を移動基準として読む。採用された具体音遷移は`realized_transition_history`へ記録し、操作観測とは分離する。適用後に候補を再生成し、状態差分から実際の`change_axes`を計算する。既にtargetが変更済みの状態へ同じ操作を適用した場合は`no_effect`として検出し、二重の変更履歴を記録しない。これは状態・操作・候補再生成・履歴を接続する検証であり、音楽固有の規則をCoreへ追加しない。

操作後も空集合を保持する観測：`10_検証/20_音程分解_操作後も空集合を保持する観測.md`

実験用スクリプト：`10_検証/empty_action_observation.py`

19の`ActionObservation`を空候補対応へ拡張し、操作が`applied`でも候補再生成後に
`constraint_no_candidate`となる観測を捨てずに保持する。空観測には`BranchEvaluation`を
作らず、選択された`DynamicStateTransition`と操作観測履歴を分離する。`B_tighten`で
範囲投影後も候補が空の状態を作り、`Γ_change`の空観測を履歴へ残しつつ、
`upstream_target_change`を採用して`E♯4–F♯4`へ復帰できることを確認する。
`empty`は既知の候補消滅診断、次の復旧操作・打ち切り条件は未解決ξとして別に保持する。Bが変化しても具体音の採用がなければ`realized_transition_history`は増えず、操作結果は`observation_history`へ残る。

列挙済みaction set枯渇後のfallback outcome観測：`10_検証/21_音程分解_全操作empty後のfallback観測_最小実験.md`

実験用スクリプト：`10_検証/exhaustion_fallback_observation.py`

20の空状態にvoice B側の境界閉鎖を加え、同一source stateから列挙した`B_change`・`Γ_change`・`upstream_target_change`の一手先枝がすべてemptyになる候補枯渇状態を作る。停止、voice B境界の再開、target破棄を`FallbackOutcomeObservation`として比較し、停止は具体音遷移を作らず、境界再開は候補空間だけを開き、target破棄は代替targetや具体音を捏造しないことを確認する。三fallbackは正式な次状態へまだ適用せず、選択controller、voice B境界を開く権限、target破棄後の代替targetは未解決ξとして保持する。

fallback採用後の実状態遷移：`10_検証/22_音程分解_fallback採用後の実状態遷移_最小実験.md`

実験用スクリプト：`10_検証/fallback_state_adoption.py`

21で観測に留めた`reopen_voice_B_boundary`を実際に適用し、`DynamicSearchState`を構成する。fallback自体は具体音を実現しないため、`FallbackStateTransition`を`fallback_transition_history`へ保存し、`realized_transition_history`とは分離する。境界再開後のS3から`upstream_target_change`、さらに`B_change`を通常の状態遷移として採用し、fallback後も探索が継続することを確認する。`stop_search`と`discard_target`は、状態表現が不足するため未解決ξとして残す。

10〜22の動態圧縮：`10_検証/23_音程分解_10〜22の動態圧縮_全体構造.md`

10〜17の関係観測・候補生成・実現・再探索枝・採用条件と、18〜22の状態・履歴・empty・action set枯渇・fallback・通常探索復帰を一枚の構造へ圧縮する。`observation_history`、`fallback_transition_history`、`realized_transition_history`を分離したまま、22で実状態化できた`reopen_voice_B_boundary`と、未解決ξとして残した`stop_search`・`discard_target`を区別して記録する。23は実験器やCore変数を追加しない。

音程分解・動態Adapterの最小境界：`10_検証/24_音程分解_動態Adapterの最小境界_検証.md`

23で圧縮した三履歴を、音楽固有の状態意味やcontrollerを一般化せず、`observation`・`structural_transition`・`realized_transition`の共通イベントへ投影する。empty観測、fallback構造遷移、具体音実現を別イベントとして保持できることだけを検証し、Module側の操作識別子は不透明な`operation_kind`として残す。Coreへ新しい状態変数は追加しない。

実験用スクリプト：`10_検証/dynamic_adapter_boundary.py`

## 状態

初期検証段階。文書ごとの状態は各ファイルに記録する。
