# RDL音楽理論｜文書地図

*RDL音楽理論の文書配置と依存関係を記録する。*

## ■ 1. 現在の構成

```text
RDL音楽理論/
├─ 00_RDL音楽理論.md
├─ 01_RDL音楽_Core.md
├─ 02_RDL音楽_文書地図.md
├─ 03_RDL音楽_全体設計方針.md
├─ 10_検証/
│  ├─ 01_C6とAm7.md
│  ├─ 02_C_major_候補集合と制約.md
│  ├─ 03_単純リズム_候補集合と制約.md
│  ├─ 04_純粋候補集合_状態判定.md
│  ├─ 05_Bから候補空間生成_最小実験.md
│  ├─ 06_波形関係_二正弦波_最小実験.md
│  ├─ 07_波形関係_時間変化する二正弦波_最小実験.md
│  ├─ 08_波形関係_短時間破断と観測分解能_最小実験.md
│  ├─ 09_波形関係_観測格子位相と破断検出_最小実験.md
│  ├─ 10_音程分解_周波数比から12TET半音数_最小実験.md
│  ├─ 11_音程分解_同一7半音と綴り_P5_d6_最小実験.md
│  ├─ 12_音程分解_同一トライトーンと綴りによる解決方向_最小実験.md
│  ├─ 13_音程分解_解決候補の文脈分解_最小実験.md
│  ├─ 14_音程分解_音度から具体音への実現_最小実験.md
│  ├─ 15_音程分解_実現制約の競合と候補消滅_最小実験.md
│  ├─ 16_音程分解_空集合後の再探索分岐_最小実験.md
│  ├─ 17_音程分解_再探索分岐の優先順位と採用条件_最小実験.md
│  ├─ 18_音程分解_採用枝から次状態への履歴循環_最小実験.md
│  ├─ 19_音程分解_状態からの再探索枝再生成_最小実験.md
│  ├─ 20_音程分解_操作後も空集合を保持する観測.md
│  ├─ 21_音程分解_全操作empty後のfallback観測_最小実験.md
│  ├─ 22_音程分解_fallback採用後の実状態遷移_最小実験.md
│  ├─ 23_音程分解_10〜22の動態圧縮_全体構造.md
│  ├─ 24_音程分解_動態Adapterの最小境界_検証.md
│  ├─ 25_リズム候補Module_動態Adapter第二標本.md
│  ├─ 26_リズム境界変更_候補空間再構成_最小実験.md
│  ├─ 27_二標本_動態境界の横断不変条件.md
│  ├─ 28_同一BoundaryTransition_投影と候補再構成_最小実験.md
│  ├─ 29_動態Adapter候補_二標本と一標本の圧縮.md
│  ├─ 30_同一音程fallback遷移_投影と候補再構成_最小実験.md
│  ├─ 31_二標本_構造遷移record接続の横断検査.md
│  ├─ 32_同一音程fallback遷移_空の候補再生成_最小実験.md
│  ├─ 33_同一リズム境界遷移_空の候補再生成_最小実験.md
│  ├─ 34_二標本_空結果のModule固有位置_横断観測.md
│  ├─ 35_リズム_no_effect境界recordと候補再生成_最小実験.md
│  ├─ 36_音程_no_effectfallback_recordと候補再生成_最小実験.md
│  ├─ 37_音程_no_effectrecordの候補再構成とcontroller境界_最小実験.md
│  ├─ 38_状態signature三断面_最小観測.md
│  ├─ 39_用途別状態同一性_最小検査.md
│  ├─ 40_候補再構成呼出し側の用途別同一性_最小検査.md
│  ├─ 41_候補生成同一性と再生成実行の分離_最小検査.md
│  ├─ 42_和声機能_同一和音とkey_context分岐_最小実験.md
│  ├─ 43_和声機能_target候補集合と選択境界_最小実験.md
│  ├─ 44_声部進行_selected_targetから具体音実現境界_最小実験.md
│  ├─ 45_文脈解釈_voice_leading後のnext_key未確定_最小実験.md
│  ├─ 46_和声機能_function_annotationとtarget候補生成規則の分離_最小実験.md
│  ├─ 47_和声機能_target候補生成規則差し替えによる候補集合分岐_最小実験.md
│  ├─ 48_和声機能_context差し替えによるtarget候補集合分岐_最小実験.md
│  ├─ 49_和声機能_history差し替えによるtarget候補集合分岐_最小実験.md
│  ├─ 50_和声機能_同一history大分類内local_pattern差によるtarget候補集合分岐_最小実験.md
│  ├─ 51_和声機能_B_history粒度差によるtarget候補集合分岐_最小実験.md
│  ├─ c_major_operations.py
│  ├─ rhythm_candidate_operations.py
│  ├─ generic_candidate_operations.py
│  ├─ boundary_candidate_generation.py
│  ├─ two_sine_wave_relations.py
│  ├─ time_varying_two_sine_wave_relations.py
│  ├─ short_ratio_break_resolution.py
│  ├─ sampling_phase_ratio_break.py
│  ├─ interval_fifth_decomposition.py
│  ├─ spelled_interval_divergence.py
│  ├─ tritone_spelling_resolution.py
│  ├─ contextual_resolution_candidate.py
│  ├─ degree_to_pitch_realization.py
│  ├─ constraint_competition_observation.py
│  ├─ reexploration_after_empty.py
│  ├─ reexploration_policy_comparison.py
│  ├─ history_aware_reexploration_cycle.py
│  ├─ state_rebased_reexploration.py
│  ├─ empty_action_observation.py
│  ├─ exhaustion_fallback_observation.py
│  ├─ fallback_state_adoption.py
│  ├─ dynamic_adapter_boundary.py
│  ├─ rhythm_dynamic_adapter.py
│  ├─ rhythm_boundary_reconstruction.py
│  ├─ rhythm_transition_projection_reconstruction.py
│  ├─ pitch_transition_projection_reconstruction.py
│  ├─ cross_module_transition_connection.py
│  ├─ pitch_transition_projection_empty_regeneration.py
│  ├─ rhythm_transition_projection_empty_regeneration.py
│  ├─ cross_module_empty_result_locations.py
│  ├─ rhythm_no_effect_transition_regeneration.py
│  ├─ pitch_no_effect_transition_regeneration.py
│  ├─ pitch_no_effect_controller_boundary.py
│  ├─ cross_module_dynamic_invariants.py
│  ├─ state_signature_observation.py
│  ├─ state_signature_views.py
│  ├─ harmonic_function_key_context_branch.py
│  ├─ harmonic_function_target_candidate_boundary.py
│  ├─ voice_leading_selected_target_realization_boundary.py
│  ├─ next_key_context_after_voice_leading_boundary.py
│  ├─ harmonic_function_target_generation_rule_boundary.py
│  ├─ harmonic_function_generation_rule_variation.py
│  ├─ harmonic_function_generation_context_variation.py
│  ├─ harmonic_function_generation_history_variation.py
│  ├─ harmonic_function_generation_history_local_pattern.py
│  └─ harmonic_function_generation_history_boundary_granularity.py
├─ 20_構造抽出/
│  └─ 動態Adapter候補_構造抽出版.md
│  └─ 音程実現_候補生成と制約の構造抽出版.md
│  └─ empty後再探索_観測fallback履歴の構造抽出版.md
│  └─ 物理音高から音楽ラベルへの分岐構造抽出版.md
│  └─ 音程Module構造地図.md
│  └─ 中核音楽理論_42〜45循環分解_構造抽出版.md
│  └─ 和声機能_target候補生成_46〜49構造抽出版.md
├─ 30_既知音楽理論参照/
│  ├─ 00_既知音楽理論参照_地図.md
│  └─ 01_音程.md
│  ├─ 02_音高と調律.md
│  ├─ 03_音階と調.md
│  ├─ 04_和音.md
│  ├─ 05_和声機能.md
│  ├─ 06_声部進行.md
│  ├─ 07_リズムと拍節.md
│  ├─ 08_旋律.md
│  ├─ 09_形式.md
│  └─ 10_記譜と綴り.md
├─ 40_中核音楽理論/
│  ├─ 00_中核音楽理論_計画表.md
│  ├─ 01_音高調律_Module計画.md
│  ├─ 02_音程_Module計画.md
│  ├─ 03_音階調_Module計画.md
│  ├─ 04_和音_Module計画.md
│  ├─ 05_和声機能_Module計画.md
│  ├─ 06_声部進行_Module計画.md
│  ├─ 07_リズム拍節_Module計画.md
│  ├─ 08_旋律_Module計画.md
│  ├─ 09_形式_Module計画.md
│  ├─ 10_記譜綴り_Module計画.md
│  └─ 11_全Module横断レビュー_破断と最小検証.md
```

## ■ 2. 各文書の役割

### 00_RDL音楽理論.md

RDL音楽理論の入口・全体構造を示す。

- 理論の目的
- 基本姿勢
- 分析と生成の方向
- 既存音楽理論との接続方針
- 将来モジュールの予定地
- 検証条件と破断条件
- 文書運用方針

本文書へ具体理論を集積し続けない。

### 01_RDL音楽_Core.md

音楽領域で共通して使用する最小の状態記述と操作を定める。

```text
S_t = <B_t, M_{B_t,t}, W_{B_t,t}, F_t, E_{B_t,t}, H_{B_t,t}, ξ_{B_t,t}>
S_t → Δ → S_t+1
```

### 20_構造抽出/動態Adapter候補_構造抽出版.md

24〜41の検証列から、Module固有状態の用途別projection、Module固有recordからGeneric eventと候補再生成への二経路、再探索の動態、保持すべき非同一性を抽出して配置する。29の証拠圧縮とは別に、確定接続・未解決ξ・禁止補完を一枚で読むための設計文書である。

### 20_構造抽出/音程実現_候補生成と制約の構造抽出版.md

13〜15から、文脈・役割・learned tendencyによるtarget注釈と、目標音度から具体音への実現を分けて配置する。候補生成、声域投影、声部関係、選択、候補消滅位置を音程Module固有構造として抽出する。

### 20_構造抽出/empty後再探索_観測fallback履歴の構造抽出版.md

16〜22から、empty観測、再探索action、列挙済みaction setの枯渇、fallback outcome、境界再開の採用、通常探索への復帰、三種類の履歴を抽出する。fallback選択原理と上位controllerは未解決ξとして残す。

### 20_構造抽出/物理音高から音楽ラベルへの分岐構造抽出版.md

10〜13から、周波数比・連続座標・12TETカテゴリー・綴り・音程ラベル・文脈的targetを分離する。物理的に同じ音高関係でも綴りにより音程ラベルが分岐する構造と、labelからtargetを自動生成しない境界を抽出する。

### 20_構造抽出/音程Module構造地図.md

四つの抽出版を、物理関係・音楽ラベル・`ξ_target_selection`・選択済みtarget・具体音実現・empty後再探索・Generic event投影として接続する。検証番号を横断する入口であり、新たな因果規則や共通controllerは追加しない。

### 20_構造抽出/中核音楽理論_42〜45循環分解_構造抽出版.md

42〜45の横断検証から、`key context → chord candidate → function annotation → target → voice leading → next key/context` の循環候補を分解する。function annotation、target候補生成、target選択、target degree planning、具体音実現、next context候補生成、next context選択を非同一の責務として保持し、残るξと禁止補完を整理する。

### 20_構造抽出/和声機能_target候補生成_46〜49構造抽出版.md

46〜49の横断検証から、`ξ_target_candidate_generation` とhistory入力の現在地を抽出する。function annotation、target候補生成規則、規則の適用可否、history fixture、生成済み候補集合、selected targetを非同一として保持し、candidate setが `C(function observation, history fixture; Γ_target_candidate_generation)` としてfixture上で現れることを整理する。

### 30_既知音楽理論参照/

既存の音楽理論を、物理法則・普遍知覚・RDL Core・RDL検証結論と同一視せず、参照用の構造化辞書として置く。最初は音程の分類と綴りによる分岐だけを収録し、検証・構造抽出へのリンクで接続する。

B依存と時刻が自明な場合は、\(M_B\)、\(W\)、\(E\)、\(H\)、\(ξ\)へ省略する。

具体的な調律・和声・旋律・リズム・楽式・ジャンルの知識は、必要な場合に別モジュールへ接続する。

### 40_中核音楽理論/

物理側の観測層と`30_既知音楽理論参照`を受け取り、RDL音楽として何をModule化し、どの順で検証するかを管理する。

`30_既知音楽理論参照`は既存体系の辞書であり、`40_中核音楽理論`はRDL音楽側のModule計画である。中核音楽理論は基層知覚を直接モデル化せず、物理層とlearned層を詰めた後、その間に残る写像・破断・残差から`B_base / Γ_base / M_B^base候補`を仮設する。

現在の入口：`40_中核音楽理論/00_中核音楽理論_計画表.md` / Module計画作成済み：`01_音高調律`〜`10_記譜綴り` / 横断レビュー：`40_中核音楽理論/11_全Module横断レビュー_破断と最小検証.md` / 作成済み検証：`10_検証/42_和声機能_同一和音とkey_context分岐_最小実験.md`〜`10_検証/51_和声機能_B_history粒度差によるtarget候補集合分岐_最小実験.md` / 構造抽出：`20_構造抽出/中核音楽理論_42〜45循環分解_構造抽出版.md` / `20_構造抽出/和声機能_target候補生成_46〜49構造抽出版.md`

### 02_RDL音楽_文書地図.md

各文書の役割、依存関係、分岐条件を管理する。

### 03_RDL音楽_全体設計方針.md

物理側の観測層から、基層・中核・上層の知覚・音楽構造・意味層へ進むための設計原則を定める。

- 硬い対象から積み上げるが、硬さを絶対真理とは扱わない
- 対象、B、Γを分離する
- M_Bそのものと、B・Γのもとで検証されるM_B候補を分ける
- ΓをCoreの状態変数ではなく、Adapter・Module・検証系の規則として扱う
- Bに身体・装置・環境によって事実上課される境界も含める
- 物理的変化、観測された変化、知覚上の破断を分離する
- Coreと検証・Moduleの境界を維持する

入口文書が「何を目指すか」、Coreが「何を共通文法とするか」を示すのに対し、本方針は「どの順序と境界で全体を構築するか」を示す。

## ■ 3. 依存関係

厳密な一方向の依存ではなく、次の役割関係として扱う。

```text
                 00 入口・全体構造
                         │
03 全体設計方針 ──────────┼────────→ 設計・検証・各論
                         │
RDL_Core / SILN ───→ 01 Core ────────┘
```

入口文書とCoreと全体設計方針は役割が異なる。入口は目的と全体像、Coreは共通文法、全体設計方針は層・検証順序・昇格境界を定める。

### 23_音程分解_10〜22の動態圧縮_全体構造.md

10〜22で確認した音程分解Moduleの動態を、関係観測・候補生成・実現・再探索・empty・action set枯渇・fallback・通常探索復帰の一枚の構造へ圧縮する。

`observation_history`、`fallback_transition_history`、`realized_transition_history`を分離したまま、22で実状態化できた`reopen_voice_B_boundary`と、未解決ξとして残した`stop_search`・`discard_target`を同じ意味へ潰さずに記録する。新しいCore変数や音楽一般の規則は追加しない。

### 24_音程分解_動態Adapterの最小境界_検証.md

23で圧縮した音程Moduleの三履歴を、`observation`・`structural_transition`・`realized_transition`という音楽語彙を含まない最小イベントへ投影する。empty観測、fallbackを適用した構造遷移、ordinary actionによる具体音実現を別履歴のまま保持し、Module側の操作識別子を不透明な`operation_kind`として残せることを確認する。`event_kind`は履歴・操作系統の分類であり、実効果は`operation_status`と`change_axes`、具体実現は`realization_status`から別に読む。Adapterは状態意味・controller・fallback選択を一般化せず、Coreへ新しい状態変数を追加しない。

### 29_動態Adapter候補_二標本と一標本の圧縮.md

24〜41で確認した動態Adapter候補を圧縮する。二標本の横断契約、fixtureで確認した非空・空の結果分岐、`event_kind`と実差分の分離、Module固有に残す空位置を区別する。37〜41では、用途別状態同一性と候補生成同一性、再生成実行の非同一性も音程一標本で観測する。候補生成規則と状態意味はModule固有のまま保持し、state identity・no_effect履歴圧縮は未解決とし、共通projector・共通状態・共通empty分類・共通候補生成器・共通controller・因果順序を追加しない。

### 30_同一音程fallback遷移_投影と候補再構成_最小実験.md

22の`FallbackStateTransition`を同一recordのまま24の`project_fallback`と19の`observe_actions()`へ接続する。recordに保存したsource／resulting voice B境界の実差分を読み、構造遷移イベントへの投影と、`B_change`・`upstream_target_change`の有効枝再観測を分離して確認する。これは28のリズムModuleと比較可能な第二標本であり、共通状態・共通候補生成器・因果順序を追加しない。

### 31_二標本_構造遷移record接続の横断検査.md

28のリズムModuleと30の音程Moduleを個別に実行し、Module固有の構造遷移recordが`structural_transition / not_realized`への投影と、record由来の候補再生成の双方へ接続する限定形式を検査する。候補語彙、状態内容、`change_axes`名、状態復元手順、候補生成規則、因果順序は比較・共通化しない。

### 32_同一音程fallback遷移_空の候補再生成_最小実験.md

実差分を持つ音程Module固有`FallbackStateTransition`を、`structural_transition`への投影とrecord由来の候補再生成へ接続する。ただし結果は空のまま残す。構造遷移後の再生成接続と候補非空性を分離し、空観測を候補消滅の診断として保持する。共通Adapter・共通状態・共通候補生成器・共通controllerは追加しない。

### 33_同一リズム境界遷移_空の候補再生成_最小実験.md

実差分を持つリズムModule固有`BoundaryTransition`を、`structural_transition`への投影とrecord由来の候補再生成へ接続する。候補空間自体は開くが、現在値除外とtarget条件の交差によって制約後の候補は空となる。03の静的候補生成器、共通Adapter・共通状態・共通候補生成器・共通controllerは変更しない。

### 34_二標本_空結果のModule固有位置_横断観測.md

32の音程Moduleと33のリズムModuleを比較し、両者の生候補と最終空結果の間にあるModule固有段階を記録する。音程は`B_range_projection`、リズムは現在値除外とtarget制約の交差で空になる。共通empty分類・共通状態・共通候補生成器・共通controllerは追加しない。

### 35_リズム_no_effect境界recordと候補再生成_最小実験.md

実差分のないリズムModule固有`BoundaryTransition`を投影と再生成へ接続する。eventの履歴分類は`structural_transition`のままでも、`operation_status=no_effect`と空の変更軸から構造条件が変わっていないことを読む。source／resulting候補条件は同じである。03の静的候補生成器、共通Adapter・共通状態・共通controllerは変更しない。

### 36_音程_no_effectfallback_recordと候補再生成_最小実験.md

実差分のない音程Module固有`FallbackStateTransition`を投影と再生成へ接続する。`event_kind=structural_transition`はfallback transition historyの分類を示し、実効果は`operation_status=no_effect`と空の変更軸から別に読む。source／resulting候補結果の一致は今回fixtureとして確認し、共通Adapter・共通状態・共通controller・因果順序は追加しない。

### 37_音程_no_effectrecordの候補再構成とcontroller境界_最小実験.md

実差分のない音程`FallbackStateTransition`をcandidate再構成へ通し、候補生成入力が不変でも`last_change_axes`を読む既存controllerのpolicyは変わり得ることを観測する。`state_after_transition()`はrecord採用履歴を追加しない候補再構成用ヘルパーであり、state identity・no_effect後のcontroller規則・履歴保存規則は決定しない。

## ■ 4. 将来の分岐候補

以下は予定地であり、現時点での作成を要求しない。

```text
調律
音高・音程
音階・モード
調性・和声
旋律・モチーフ
リズム・拍子
グルーヴ
対位法
楽式
分析・作曲実例
```

分岐は、次のいずれかが生じた時点で検討する。

- Coreや入口文書に具体領域の知識が蓄積し始めた
- 独立した検証条件を持つ領域が現れた
- 複数の文書から参照される共通領域になった
- 既存理論との接続を個別に記録する必要が生じた

## ■ 5. 現時点の検証対象

まずは、Coreが実際の音楽関係を記述できるかを確認する。

### 5.1 基礎検証：C majorの候補集合と制約

記録：`10_検証/02_C_major_候補集合と制約.md`

現在の主検証対象。C majorを実験用の境界として置き、候補空間、保存条件、現在候補の変更、目標条件が候補集合へどう作用するかを確認する。

実装：`10_検証/c_major_operations.py`

この段階では、`stabilize / destabilize` の具体化や、安定度・緊張度の順位付けを行わない。C majorで規則を定義した結果を、Coreの操作が自然に導いたものとも扱わない。

### 5.2 履歴由来の候補：C6とAm7

同じ音集合が、低音・配置・履歴・後続関係によって別のM_Bとして安定しうるかを確認する。

記録：`10_検証/01_C6とAm7.md`

この検証は過去チャット由来の題材であり、現行Coreから最初に導いた検証ではない。履歴作用を含む後順位候補として保持する。

初期の観察結果：

```text
同じ音集合 ≠ 同じM_B
低音関係は、音集合とは別の強い境界になりうる
一時的な低音変更と、持続する構造変更は区別が必要
曖昧さは、必ずしも大きなEではない
```

この検証では、Eを数値化せず、関係のどの層に差が現れたかを記録した。

### 5.3 Bから候補空間を生成する最小実験

記録：`10_検証/05_Bから候補空間生成_最小実験.md`

実装：`10_検証/boundary_candidate_generation.py`

`B`と`M_B`だけでは候補集合が決まらず、候補生成規則`Γ`を接続したときに`C(B, M_B;Γ)`が生成されることを、C majorを参照例として確認する。

この実験では、候補生成と生成後の制約処理を分離し、同じ`B`・`M_B`でも`Γ`が変われば候補空間が変わることを記録する。

### 5.4 次段階の検証候補

```text
候補空間の生成方法
制約の追加と解除
同一事象の反復
反復間の差
順序による候補集合の変化
```

純粋候補集合の検証で、候補数による状態判定が音楽語彙から独立して記述できることを確認した。これはRDL音楽固有の法則ではなく、`C → 制約 R → C'` という一般的な道具として分離し、現範囲の一般実験は閉じる。

したがって、一般側の候補集合実験を増やすより、音名・コードより下位の波形関係を確認し、その後に音楽において `B`・`M_B`と生成規則`Γ`から `C(B, M_B;Γ)` がどう生成されるか、候補空間外の `ξ` をどう残すか、いつ `B` を引き直すかへ戻る。転回形・七の和音・持続・反復などの具体的拡張は、この境界生成を確認した後に検討する。

### 5.5 波形関係からM_B候補を立ち上げる最小実験

記録：`10_検証/06_波形関係_二正弦波_最小実験.md`

実装：`10_検証/two_sine_wave_relations.py`

2本の正弦波を既知成分として与え、周波数比・有理近似・共通周期・反復性を観測境界内で抽出する。`ratio_preserved`と`short_recurrence_candidate`を別軸に分け、実サンプル列から得る`recurrence_error`は補助観測として扱う。これは未知波形のスペクトル分解や知覚モデルではなく、音名・コード・調性を使わない波形関係の最初の足場である。保存関係ごとの`M_B候補群`は境界依存の暫定状態として扱い、Coreへ追加しない。

### 5.6 時間変化の中で保存される波形関係

記録：`10_検証/07_波形関係_時間変化する二正弦波_最小実験.md`

実装：`10_検証/time_varying_two_sine_wave_relations.py`

既知の時間変化する周波数軌道`f1(t)`・`f2(t)`から、各成分の絶対値保存と比の保存を分離して観測する。特に、絶対周波数がともに変化しても`f2(t)/f1(t)`が保存されるケースと、一方の成分だけが変化して比が崩れるケースを比較する。波形は積分位相から生成するが、未知波形からの周波数推定や短周期再帰の候補化は扱わない。`M_B候補 = B内で保存される関係の束`という仮説を検証層で確認するための実験であり、Coreへ追加しない。

### 5.7 短時間の関係破断と観測分解能

記録：`10_検証/08_波形関係_短時間破断と観測分解能_最小実験.md`

実装：`10_検証/short_ratio_break_resolution.py`

既知の連続時間モデルに0.5 msだけ比が`1.5`から`1.6`へ移動する区間を置き、10 kHzと1 kHzのサンプル境界で破断が検出されるかを比較する。連続モデル上の破断、Bのサンプル点で検出された破断、観測上の比保存を別軸で記録する。粗いBで破断を検出しなかったことを、連続時間で比が保存されたこととは解釈しない。未知波形からの関係推定、破断の補間、知覚可能性は扱わず、Coreへ追加しない。

### 5.8 観測格子の開始位相と破断検出

記録：`10_検証/09_波形関係_観測格子位相と破断検出_最小実験.md`

実装：`10_検証/sampling_phase_ratio_break.py`

08と同じ既知モデル・同じ観測時間・同じsample_rate・同じ`Γ_point_ratio`を使い、`sampling_phase_s`だけを0 msと0.5 msで切り替える。分解能が同じでも観測格子の配置によって破断検出が変わることを、独立した`run_checks()`と`main()`出力で確認する。`model_ratio_break_present`、観測時間窓との交差、サンプル点での破断検出、観測上の比保存を分離し、08のコードを拡張するのではなく09専用実験として管理する。未観測領域の内容を直接確定せず、Coreへ追加しない。

### 5.9 音程分解・周波数比から12TET半音数までの最小接続検査

記録：`10_検証/10_音程分解_周波数比から12TET半音数_最小実験.md`

実装：`10_検証/interval_fifth_decomposition.py`

既知音楽理論を、長期的に形成された`M_B^learned`の観測資料として扱い、純正五度の代表比と12TETの7半音を下位の関係へ逆分解する。純正比`3:2`と12TETの`2^(7/12)`を比較し、次を分離する。

```text
周波数比
→ セント座標
→ 12TET上の半音数
```

純正五度の代表比と12TETの7半音は物理比として異なるが、`Γ_12TET_round`ではともに7半音へ写る。この結果は、物理関係が同一であることではなく、既知の記述規則によるカテゴリー圧縮を示す。音名・綴りを必要とする音程名、人間の基層知覚、五度の協和・和声機能はこの検証の範囲外に残す。

### 5.10 音程分解・同一7半音と綴りによるP5／d6分岐

記録：`10_検証/11_音程分解_同一7半音と綴り_P5_d6_最小実験.md`

実装：`10_検証/spelled_interval_divergence.py`

`C4 → G4`、`C♯4 → A♭4`、`C4 → A𝄫4`を比較し、同じ7半音・同じ周波数比が音名上のgeneric intervalと音程品質によってP5／完全五度とd6／減六度へ分岐することを検査する。特に`C4 → G4`と`C4 → A𝄫4`では下音・上音の絶対音高まで同一にし、音名・綴り情報を比較関係として保持するBの追加による分岐を確認する。これは、音程名が周波数比だけでなく、`M_B^learned`側の追加構造を必要とすることを示す。ただし、記述上の分岐を心理実験としての知覚差とは扱わず、Coreへ追加しない。

### 5.11 音程分解・同一トライトーンと綴りによる解決方向

記録：`10_検証/12_音程分解_同一トライトーンと綴りによる解決方向_最小実験.md`

実装：`10_検証/tritone_spelling_resolution.py`

`F4 → B4`と`E♯4 → B4`を比較し、12TET物理モデル上の同一音高対・同じ6半音が、綴り情報を比較関係として保持するBによってA4／増四度とd5／減五度へ分岐することを検査する。さらに、learned側の代表的解決候補として`F4 → E4, B4 → C5`と`E♯4 → F♯4, B4 → A♯4`を外部から与え、前者が外へ開き、後者が内へ狭まるという声部移動を`Γ_motion`で記述する。これはA4/d5からtargetを自動生成する実験でも、解決感や機能和声の普遍性を検証するものでもない。`A4 / d5 → target候補`というlearned側の遷移`M_B`と、`target → motion`という機械的な関係抽出を分けて保持する最小例であり、Coreへ追加しない。

### 5.12 音程分解・解決候補の文脈分解

記録：`10_検証/13_音程分解_解決候補の文脈分解_最小実験.md`

実装：`10_検証/contextual_resolution_candidate.py`

12で外部から与えていた`target`を、次の部品へ分解して保持する。

```text
既選択target
  + 文脈
  + 開始音度・目標音度
  + learned側の代表的な進行規則
  + 綴り付きの音高実現
  ↓
target候補の分解・整合確認
  ↓ Γ_motion
声部運動
```

`F4–B4 / A4`はC major内の`4→3`と`7→1`、`E♯4–B4 / d5`はF♯ major内の`7→1`と`4→3`として、既に選択された具体的targetへ注釈される。これはA4/d5というラベルや`7→1`・`4→3`からtargetを生成する規則ではなく、`M_B^context`と`M_B^learned`がtargetへどう対応づけられているかを確認する検証用の分解である。代表例以外の候補、具体化規則、様式差、知覚差、機能和声全体は扱わず、Coreへ追加しない。

### 5.13 音程分解・音度から具体音への実現

記録：`10_検証/14_音程分解_音度から具体音への実現_最小実験.md`

実装：`10_検証/degree_to_pitch_realization.py`

13で既選択targetとして与えていた具体音について、13から引き継いだlearned tendencyによる目標音度の後段を検証する。`B_realization`で候補オクターブと声部範囲を境界として置き、`Γ_spelling`で複数の綴り付き候補を生成し、`B_range_projection`で声域範囲を通過した候補へ絞り、`Γ_ordering`で上下関係を満たす候補対を構成し、`Γ_select`で開始音からの最小移動を適用して候補の一つを選択する。`7→1`だけでは`F♯3 / F♯4 / F♯5`を区別できず、`F♯4`の具体化には別の境界と規則が必要であることを検査する。これは一つの12TET長音階モデルと選択規則の限定実験であり、音度遷移から具体音が常に一意に決まること、機能和声や人間の音楽的選択を一般化することは扱わない。

### 5.14 音程分解・実現制約の競合と候補消滅

記録：`10_検証/15_音程分解_実現制約の競合と候補消滅_最小実験.md`

実装：`10_検証/constraint_competition_observation.py`

14で分離した候補生成・`B_range_projection`・`Γ_ordering`・選択の各段階について、候補が消える位置を観測する。`Γ_spelling`直後の生成候補が同じでも、`B_realization`の声部範囲による投影で片側候補が空になる場合と、投影後の候補が`Γ_ordering`で候補対を作れない場合へ分岐する。前者は`status = constraint_no_candidate`、後者は`status = no_admissible_candidate`として、`selected`を空にし、`failure_stage`と理由を保持する。これは境界競合の既知の診断であり、音域・上下関係を音楽一般の普遍的制約、空集合を実際の不可能性、候補消滅を直ちにB引き直しの根拠とは扱わない。Bの引き直し・制約緩和・別の候補生成Γへの切替は未解決ξとして残す。

### 5.15 音程分解・空集合後の再探索分岐

記録：`10_検証/16_音程分解_空集合後の再探索分岐_最小実験.md`

実装：`10_検証/reexploration_after_empty.py`

15で導入した`no_admissible_candidate`という診断形式を引き継ぐ初期空集合から、`B_change`・`Γ_change`・`upstream_target_change`を別分岐として適用する。14の既存`lower / upper`フィールドは16では声部IDの枠として扱い、物理的な上下は`pitch_ordering_rule`で分離する。B変更とΓ変更は実現層内の変更であり、B変更では候補オクターブ・声域を開き、Γ変更ではcrossed voice pitchesを比較対象へ含める。`upstream_target_change`は上流から与えられたtarget入力を差し替えて実現層を再実行する境界を観測する。各分岐の`change_axes`（`boundary_changed`・`relation_changed`・`upstream_target_changed`）と`generated_voice_A / generated_voice_B / filtered_voice_A / filtered_voice_B / admissible_voice_pairs / selected / pitch_ordering_rule`を保持し、`branch_kind`から変更内容を逆算しない。空集合後の再探索が一つの復旧操作へ縮約できないことを検査する。分岐の優先順位、採用条件、打ち切り条件は未解決ξとして残し、音楽一般の再探索順序やCoreの操作へ昇格させない。

### 5.16 音程分解・再探索分岐の優先順位と採用条件

記録：`10_検証/17_音程分解_再探索分岐の優先順位と採用条件_最小実験.md`

実装：`10_検証/reexploration_policy_comparison.py`

16で得られた三つの再探索枝を、`change_axes`から投影した`motion_cost`、`boundary_change_cost`、`relation_change_cost`、`upstream_target_change_cost`、保存条件の別軸へ分解する。重み付き総合点は置かず、target維持・厳密な実音高順序の維持・即時移動量の最小化という明示的な方針を適用し、同じ枝集合でも採用結果が変わることを検証する。これは採用方針を一意化するものではなく、保存条件と比較順が必要であることを示す比較実験である。方針の起源、複数条件の競合、履歴による更新、打ち切り条件は未解決ξとして残し、Coreへ昇格させない。

### 5.17 音程分解・採用枝から次状態への履歴controller接続

記録：`10_検証/18_音程分解_採用枝から次状態への履歴循環_最小実験.md`

実装：`10_検証/history_aware_reexploration_cycle.py`

17の`BranchEvaluation`と`SearchPolicy`を引き継ぎ、採用枝を`StateTransition`として次状態へ記録する。次状態の`selected_pair`を次回の即時移動量の基準へ再投影し、履歴に保持した`change_axes`をcontrollerへ渡して次の方針を選ぶ。履歴なし→`target_continuity_then_relation`、直前の`change_axes`が`boundary_changed`のみ→`strict_relation_then_boundary`、直前の`change_axes`が`upstream_target_changed`のみ→`minimum_immediate_motion`という暫定写像を二回の遷移で実行し、S2で次方針を得たところで停止する。候補枝は初期seedから一度だけ作る固定メニューであるため、現在状態からのB・Γ・target差分の再計算は19へ送る。`branch_kind`は表示・追跡用に留め、性質の推定には使わない。これは履歴controllerの接続検査であり、controllerの写像、履歴保持長、Γ_change後の規則、打ち切り条件は未解決ξとして残す。12平均律・長音階・音度・声部順序は引き続きModule固有の`M_B`と`Γ`に留め、Coreへ昇格させない。

### 5.18 音程分解・状態からの再探索枝再生成

記録：`10_検証/19_音程分解_状態からの再探索枝再生成_最小実験.md`

実装：`10_検証/state_rebased_reexploration.py`

18の固定枝メニューを、現在状態へ適用する操作候補へ置き換える。`B`を候補オクターブ・声域、`Γ`を実音高ordering rule、`target`をvoiceごとのtarget degreeとして`DynamicSearchState`へ保持し、`B_change`・`Γ_change`・`upstream_target_change`を状態へ適用する。具体音の移動基準は`last_realized_pair`へ一本化し、初期seedの開始音から採用候補へ遷移ごとに更新する。これは現在の`B`で有効なペアを保証する名前ではなく、最後に具体音として実現したペアを基準点として保持するための名称である。これにより、次回の`Γ_select`は`state_0`の開始音ではなく`state_t`の最後に実現した音高を移動基準として読む。S1の`A♯3–F♯4`からtarget変更を適用した場合、`E♯3`と`E♯4`の移動量はそれぞれ5半音と7半音となり、`E♯3–F♯4`が選ばれる。適用後に候補を再生成し、適用前後の状態差分から実際の`change_axes`を計算するため、枝名から性質を逆算しない。既にtargetが変更済みの状態へ同じ操作を適用すると`no_effect`として検出され、`upstream_target_changed = false`のまま保持される。`no_effect`は観測には残すが、今回の比較では採用対象から除外する。採用された具体音遷移は`realized_transition_history`へ記録し、各操作の観測は`observation_history`へ分離する。これは状態・操作・候補再生成・履歴を接続する検証であり、Coreへ音楽固有のB・Γ・targetを追加しない。候補再生成後もemptyになる場合の復帰、複合変更、操作controllerの更新は未解決ξとして残す。

### 5.19 音程分解・操作後も空集合を保持する観測

記録：`10_検証/20_音程分解_操作後も空集合を保持する観測.md`

実装：`10_検証/empty_action_observation.py`

19の`ActionObservation`を空候補対応へ拡張し、操作後に`selected = None`となっても
`ReexplorationObservation.status`、`failure_stage`、`failure_reason`を保持する。空観測には
`BranchEvaluation`を作らず、採用された`DynamicStateTransition`と、各操作を試した
`realized_transition_history`と`observation_history`を分離する。`B_tighten`で`B_range_projection`後の
`constraint_no_candidate`を作り、空状態を通常の遷移と混同せず保持する。同じ空状態から
`Γ_change`がなおemptyになる観測も履歴へ残し、`strict_relation_then_boundary`の比較では
空枝を除外して`upstream_target_change`を採用し、`E♯4–F♯4`へ戻ることを確認する。
`empty`は既知の診断、復旧方針・打ち切り条件・空状態での`last_realized_pair`の意味は未解決ξとして
分離する。Coreへ音楽固有のB・Γ・targetを追加しない。

### 5.20 音程分解・列挙済みaction set枯渇後のfallback outcome観測

記録：`10_検証/21_音程分解_全操作empty後のfallback観測_最小実験.md`

実装：`10_検証/exhaustion_fallback_observation.py`

20の空状態にvoice B側の境界閉鎖を加え、同一source stateから列挙した
`B_change`・`Γ_change`・`upstream_target_change`の一手先枝を独立に評価する。
列挙済みaction setの全枝がemptyになった場合を、可能な操作全体の消滅とは呼ばず、
action-set exhaustionとして記録する。その後の`stop_search`、
`reopen_voice_B_boundary`、`discard_target`を`FallbackOutcomeObservation`として比較し、
いずれも正式な`DynamicSearchState`の次状態へはまだ昇格させない。voice B境界の局所的な
再開は、上位層のBへの退避とは区別する。fallback選択controller、境界再開の権限、target破棄後の
代替target、fallback履歴の形式は未解決ξとして保持し、Coreへ昇格させない。

### 5.21 音程分解・fallback採用後の実状態遷移

記録：`10_検証/22_音程分解_fallback採用後の実状態遷移_最小実験.md`

実装：`10_検証/fallback_state_adoption.py`

21で`FallbackOutcomeObservation`に留めた`reopen_voice_B_boundary`を実際に
`DynamicSearchState`へ適用し、`S_t → Δ → S_t+1`を構成する。fallbackはvoice Bの
境界を変えるが、具体音をまだ採用しないため、`FallbackStateTransition`を
`fallback_transition_history`へ記録し、`realized_transition_history`へ混ぜない。
境界再開後の状態から`upstream_target_change`を採用し、その後
`minimum_immediate_motion`で`B_change`を採用して、fallback後も通常探索が続くことを
確認する。`stop_search`と`discard_target`は正式な次状態へ変換せず、停止後のcontroller接続と
target破棄後の状態表現を未解決ξとして保持する。Coreへ音楽固有のB・Γ・targetを追加しない。

### 5.22 音程分解・10〜22の動態圧縮

記録：`10_検証/23_音程分解_10〜22の動態圧縮_全体構造.md`

10〜17の関係観測・候補生成・実現・再探索枝・採用条件と、18〜22の状態・履歴・empty・action set枯渇・fallback・通常探索復帰を一枚の構造へ圧縮する。候補生成は`physical relation → 12TET coordinate/category → learned description → contextual role / target → realization candidate generation`の層を保ち、現在状態の`B / Γ / target`から候補が生成される入口と混同しない。

`observation_history`、`fallback_transition_history`、`realized_transition_history`を分離したまま、22で実状態化できた`reopen_voice_B_boundary`と、既知のfallback outcome後に未解決として残る接続・状態表現を区別して記録する。23は実験器やCore変数を追加しない。

### 5.23 音程分解・動態Adapterの最小境界

記録：`10_検証/24_音程分解_動態Adapterの最小境界_検証.md`

実装：`10_検証/dynamic_adapter_boundary.py`

23で圧縮した音程Moduleの三履歴を、`observation`・`structural_transition`・`realized_transition`の共通イベントへ投影する。empty観測、fallback構造遷移、具体音実現を別イベントとして保持し、`branch_kind`・`fallback_kind`・`selected_branch_kind`に由来するModule識別子を不透明な`operation_kind`として保存する。`project_state()`の出力は履歴チャンネル別の投影順であり、因果・時系列順を再構成しない。Adapterは状態意味・controller・fallback選択を一般化せず、Coreへ新しい状態変数を追加しない。

### 5.24 リズム候補Module・動態Adapter第二標本

記録：`10_検証/25_リズム候補Module_動態Adapter第二標本.md`

実装：`10_検証/rhythm_dynamic_adapter.py`

表拍・裏拍だけを候補とする既存の単純リズムModuleへ、音程Moduleとは別形式の操作観測・構造遷移・具体実現記録を置き、同じ`observation`・`structural_transition`・`realized_transition`へ投影できるかを検証する。`target_rest`による既知の空候補、`reopen_grid_boundary`によるfallback構造遷移、`select_offbeat`による具体実現を分離し、Module側の識別子を不透明な`operation_kind`として保持する。二標本で共通境界の候補を得たが、Coreへの昇格、候補選択原理、因果順序の再構成は行わない。

### 5.25 リズム境界変更・候補空間再構成

記録：`10_検証/26_リズム境界変更_候補空間再構成_最小実験.md`

実装：`10_検証/rhythm_boundary_reconstruction.py`

25で記録した`reopen_grid_boundary`を、25で使った候補語彙と制約器を再利用する26専用の境界依存候補生成器へ接続する。閉じた境界では空候補になる`target=休符`を、構造遷移後の`grid_open=True`で再評価し、`休符`が候補空間へ追加されることを確認する。03の静的`candidate_space`は変更しない。`structural_transition`が後続の候補生成条件を変更し得ることを示すが、共通projector、共通状態、controller、因果順序は導入しない。

### 5.26 二標本・動態境界の横断契約候補

記録：`10_検証/27_二標本_動態境界の横断不変条件.md`

実装：`10_検証/cross_module_dynamic_invariants.py`

24の音程Moduleと25・26のリズムModuleを個別の既存検証器のまま実行し、`observation`・`structural_transition`・`realized_transition`の三分類、`operation_kind`の保持、実現状態の分離を横断契約候補として再確認する。三分類すべての出現はfixture coverageへ分離し、26の候補空間再構成は別実験として再検査する。共通projector・共通状態・共通controller・因果順序への昇格は行わない。

### 5.27 同一リズム境界遷移の投影・候補再構成

記録：`10_検証/28_同一BoundaryTransition_投影と候補再構成_最小実験.md`

実装：`10_検証/rhythm_transition_projection_reconstruction.py`

26が生成した同じ`BoundaryTransition`を、`structural_transition`のGenericイベントへ投影し、そのrecordが持つ`resulting_grid_open`を26専用の動的候補生成器へ渡す。投影用recordと候補再構成用recordを分けず、同一境界遷移が両方の経路へ接続されることを検証する。03の静的`candidate_space`、共通Adapter、因果順序は変更しない。

### 5.28 動態Adapter候補・二標本横断契約とModule固有結果の圧縮

記録：`10_検証/29_動態Adapter候補_二標本と一標本の圧縮.md`

24〜41を圧縮し、二標本で確認した三イベント分類・不透明な`operation_kind`保持・`realization_status`分離・`event_kind`と実差分の分離、およびModule固有の構造遷移recordからの投影・再生成処理接続を記録する。37〜41の音程一標本では候補再構成、controller入力、用途別状態同一性、候補生成同一性、再生成実行を分離する。非空・空はfixture結果、空位置はModule固有観測、state identity・no_effect履歴圧縮は未解決として分離し、共通projector・共通状態・共通empty分類・共通controller・因果順序は追加しない。

### 5.29 同一音程fallback遷移の投影・候補再構成

記録：`10_検証/30_同一音程fallback遷移_投影と候補再構成_最小実験.md`

実装：`10_検証/pitch_transition_projection_reconstruction.py`

22の同じ`FallbackStateTransition`を24の`project_fallback`へ投影し、recordが持つsource／resulting voice B境界差分を19の候補生成器へ反映する。`structural_transition`への投影と、`B_change`・`upstream_target_change`が有効枝として再観測されることを確認する。28のリズムModuleと同じ接続形式を二標本で比較するが、候補生成規則・境界意味・共通状態・因果順序は統一しない。

## ■ 6. 運用原則

- GitHubリポジトリを保存・版管理の基準とする
- ローカル作業領域で編集・検証し、確定した変更をコミットする
- 原文版を先に固定し、更新時は構造差分を確認する
- Coreへ特定文化圏・調律・ジャンルの前提を持ち込まない
- Eの定義は実例から抽出し、先に過度な数式固定を行わない
- モジュール分割そのものを目的にしない
- 物理側の検証結果を、そのまま知覚上の結論へ拡張しない
- 既知の信号処理とRDLによる構造記述を分ける
- B・Γ・M_Bを省略せず、保存・破断の判定条件を記録する
- 下位層の条件を固定してから上位層へ進む

## ■ 7. 状態

```text
入口文書       v0.1 / DRAFT
Core           v0.1 / DRAFT
文書地図       v0.2 / 更新
全体設計方針   v0.1 / DRAFT
調性・和声Module 未作成 / `B + M_B + Γ → C(B, M_B;Γ)`の検証中
C major候補集合と制約 v0.2 / 検証中
Bから候補空間生成 v0.1 / 実験中
波形関係・二正弦波 v0.1 / 実験中
時間変化する波形関係 v0.1 / 実験中
短時間破断と観測分解能 v0.1 / 実験中
観測格子の開始位相と破断検出 v0.1 / 実験中
音程分解・周波数比から12TET半音数 v0.2 / Module候補・最小接続検査
同一7半音と綴りによるP5／d6 v0.2 / Module候補・最小接続検査
同一トライトーンと綴りによる解決方向 v0.1 / Module候補・最小接続検査
解決候補の文脈分解 v0.1 / Module候補・最小接続検査
音度から具体音への実現 v0.1 / Module候補・最小接続検査
実現制約の競合と候補消滅 v0.1 / Module候補・最小接続検査
空集合後の再探索分岐 v0.1 / Module候補・最小接続検査
再探索分岐の優先順位と採用条件 v0.1 / Module候補・最小接続検査
採用枝から次状態への履歴controller接続 v0.1 / Module候補・最小接続検査
状態からの再探索枝再生成 v0.1 / Module候補・最小接続検査
列挙済みaction set枯渇後のfallback outcome観測 v0.1 / Module候補・最小接続検査
fallback採用後の実状態遷移 v0.1 / Module候補・最小接続検査
音程分解・10〜22の動態圧縮 v0.1 / Module候補・動態圧縮
音程分解・動態Adapterの最小境界 v0.1 / Adapter候補・最小接続検査
リズム候補Module・動態Adapter第二標本 v0.1 / Adapter候補・第二標本検証
動態Adapter候補・二標本横断契約とModule固有結果の圧縮 v0.5 / Adapter候補・証拠範囲圧縮
同一音程fallback遷移の投影・候補再構成 v0.1 / Module候補・最小接続検査
C6とAm7 v0.1 / 履歴由来・後順位候補
```























