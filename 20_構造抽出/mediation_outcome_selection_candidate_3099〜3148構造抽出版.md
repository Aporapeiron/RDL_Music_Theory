# mediation outcome selection candidate 3099〜3148 構造抽出版

## 抽出対象

`10_検証/3099〜3148_mediation_outcome_selection_candidate_stress_test_50工程_最小実験.md`

## 位相

```text
source_reentry
→ candidate_request
→ candidate_layer
→ candidate_basis_layer
→ partition_layer
→ candidate_view
→ bundle
→ integrity
→ non_identity
→ music_subject
→ summary
→ next_plan
```

## source_reentry

3049〜3098のmediation selection controller resultを再入する。

```text
selection controller boundary
→ selection controller result
→ outcome selection candidate
```

controller resultは、まだselection、commitment、resolutionへ進んでいない比較結果である。

## candidate_request

controller resultをselection candidateへ渡すrequestを生成する。

ただしrequestは、selected outcomeやcommitmentそのものではない。

## candidate_layer

controller result種別ごとにselection candidateを分ける。

```text
contextual controller result
→ contextual selection candidate

hearing shift controller result
→ hearing shift selection candidate

reference controller result
→ reference selection candidate
```

## candidate_basis_layer

candidateは、比較結果から生じた選択可能性として保持される。

```text
phrase trace candidate
weight trace candidate
reference trace candidate
```

## partition_layer

candidateは三つの経路に分割される。

```text
contextual_candidate
hearing_shift_candidate
reference_candidate
```

分割はsolutionではない。

## candidate_view

candidate viewは、後続selected outcome boundaryへ渡すための可視境界である。

ここでは、まだselected outcomeもcommitmentも生成しない。

## bundle

bundleは以下を保持する。

```text
source_bundle
candidate_routes
contextual_candidates
hearing_shift_candidates
reference_candidates
stop_lines
```

## integrity

確認する条件:

```text
every result gets candidate route
candidate variety preserved
result controller record traces preserved
candidate generated without selection
no commitment rewrite or resolution
```

## non_identity

```text
selection candidate ≠ selected outcome
selection candidate ≠ outcome commitment
selection candidate ≠ resolution
```

この非同一性により、選択可能性を即時採用や解決へ潰さない。

## music_subject

音楽的には、これは「戻ってきた聞こえの比較結果が、採用可能性として浮上する」段階である。

文脈上の戻り、聞こえの重みの再聴取、参照軸の開放性が、それぞれ別のselection candidateとして保持される。

## summary

3099〜3148では、

```text
controller result
→ selection candidate
→ selected outcome boundary
```

のうち、selection candidateまでを検証した。

## next_plan

次のξ:

```text
mediation_selected_outcome_boundary_stress
```
