"""再探索分岐の優先順位と採用条件を比較する最小検証。

16では、同じ空集合からB_change・Γ_change・upstream_target_changeへ
分岐できることを確認した。
17では、各分岐を一つの総合点へ潰さず、変更軸を分けたまま明示的な
探索方針を適用する。方針ごとに採用枝が変わることを観測し、どの方針が
音楽一般に正しいかは決めない。
"""

from dataclasses import dataclass, replace

from reexploration_after_empty import (
    ChangeAxes,
    ReexplorationObservation,
    build_reexploration_observations,
)


@dataclass(frozen=True)
class BranchEvaluation:
    """再探索枝を比較するための分離された観測軸。"""

    branch_kind: str
    change_layer: str
    change_axes: ChangeAxes
    status: str
    selected_pair: tuple[str, str]
    motion_cost: int
    boundary_change_cost: int
    relation_change_cost: int
    upstream_target_change_cost: int
    preserves_strict_ordering: bool
    preserves_original_target: bool
    admissible_pair_count: int


@dataclass(frozen=True)
class SearchPolicy:
    """再探索枝を採用するための明示的な条件と比較順。"""

    name: str
    description: str
    require_strict_ordering: bool | None
    require_original_target: bool | None
    ranking: tuple[str, ...]


@dataclass(frozen=True)
class PolicyDecision:
    """一つの方針を枝集合へ適用した結果。"""

    policy_name: str
    considered_branch_kinds: tuple[str, ...]
    rejected_branch_kinds: tuple[str, ...]
    ranked_branch_kinds: tuple[str, ...]
    selected_branch_kind: str


def evaluate_branch(observation: ReexplorationObservation) -> BranchEvaluation:
    """16の選択済み枝を、比較軸を混ぜずに評価する。"""

    if observation.selected is None:
        raise ValueError("cannot score an empty reexploration branch")

    selected_a, selected_b = observation.selected
    start_a = observation.request.lower.start
    start_b = observation.request.upper.start
    motion_cost = abs(selected_a.chromatic_index - start_a.chromatic_index) + abs(
        selected_b.chromatic_index - start_b.chromatic_index
    )

    # ここでの変更コストは、音楽一般の重みではなく、この最小実験で
    # 実際にどの軸を変更したかを示す分類値である。枝名から逆算しない。
    change_axes = observation.change_axes
    boundary_change_cost = int(change_axes.boundary_changed)
    relation_change_cost = int(change_axes.relation_changed)
    upstream_target_change_cost = int(change_axes.upstream_target_changed)

    return BranchEvaluation(
        branch_kind=observation.branch_kind,
        change_layer=observation.change_layer,
        change_axes=change_axes,
        status=observation.status,
        selected_pair=(selected_a.text, selected_b.text),
        motion_cost=motion_cost,
        boundary_change_cost=boundary_change_cost,
        relation_change_cost=relation_change_cost,
        upstream_target_change_cost=upstream_target_change_cost,
        preserves_strict_ordering=(
            observation.pitch_ordering_rule == "strict_voice_a_pitch_lt_voice_b_pitch"
        ),
        preserves_original_target=(
            not change_axes.upstream_target_changed
        ),
        admissible_pair_count=len(observation.admissible_voice_pairs),
    )


def build_branch_evaluations() -> tuple[BranchEvaluation, ...]:
    """16の三つの選択済み再探索枝を比較軸へ写す。"""

    initial, b_branch, gamma_branch, target_branch = (
        build_reexploration_observations()
    )
    assert initial.status == "no_admissible_candidate"
    return tuple(
        evaluate_branch(observation)
        for observation in (b_branch, gamma_branch, target_branch)
    )


def _matches_policy(
    branch: BranchEvaluation,
    policy: SearchPolicy,
) -> bool:
    if (
        policy.require_strict_ordering is not None
        and branch.preserves_strict_ordering != policy.require_strict_ordering
    ):
        return False
    if (
        policy.require_original_target is not None
        and branch.preserves_original_target != policy.require_original_target
    ):
        return False
    return True


def _ranking_key(
    branch: BranchEvaluation,
    policy: SearchPolicy,
) -> tuple[int, ...]:
    return tuple(getattr(branch, field_name) for field_name in policy.ranking)


def apply_policy(
    policy: SearchPolicy,
    branches: tuple[BranchEvaluation, ...],
) -> PolicyDecision:
    """方針を枝へ適用し、辞書式比較の結果だけを返す。"""

    considered = tuple(branch for branch in branches if _matches_policy(branch, policy))
    rejected = tuple(branch for branch in branches if branch not in considered)
    if not considered:
        raise ValueError(f"policy has no admissible reexploration branch: {policy.name}")

    ranked = tuple(
        sorted(
            considered,
            key=lambda branch: (_ranking_key(branch, policy), branch.branch_kind),
        )
    )
    return PolicyDecision(
        policy_name=policy.name,
        considered_branch_kinds=tuple(branch.branch_kind for branch in considered),
        rejected_branch_kinds=tuple(branch.branch_kind for branch in rejected),
        ranked_branch_kinds=tuple(branch.branch_kind for branch in ranked),
        selected_branch_kind=ranked[0].branch_kind,
    )


POLICIES = (
    SearchPolicy(
        name="target_continuity_then_relation",
        description="上流targetを維持し、次にΓの厳密性を維持する",
        require_strict_ordering=None,
        require_original_target=True,
        ranking=("relation_change_cost", "motion_cost", "boundary_change_cost"),
    ),
    SearchPolicy(
        name="strict_relation_then_boundary",
        description="厳密な実音高順序を維持し、境界変更の小さい枝を選ぶ",
        require_strict_ordering=True,
        require_original_target=None,
        ranking=(
            "boundary_change_cost",
            "motion_cost",
            "upstream_target_change_cost",
        ),
    ),
    SearchPolicy(
        name="minimum_immediate_motion",
        description="今回の実音高移動量を最小にする",
        require_strict_ordering=None,
        require_original_target=None,
        ranking=(
            "motion_cost",
            "relation_change_cost",
            "upstream_target_change_cost",
            "boundary_change_cost",
        ),
    ),
)


def build_policy_decisions(
    branches: tuple[BranchEvaluation, ...] | None = None,
) -> tuple[PolicyDecision, ...]:
    if branches is None:
        branches = build_branch_evaluations()
    return tuple(apply_policy(policy, branches) for policy in POLICIES)


def run_checks() -> None:
    branches = build_branch_evaluations()
    by_kind = {branch.branch_kind: branch for branch in branches}

    assert by_kind["B_change"].motion_cost == 12
    assert by_kind["B_change"].boundary_change_cost == 1
    assert by_kind["B_change"].relation_change_cost == 0
    assert by_kind["B_change"].preserves_strict_ordering is True
    assert by_kind["B_change"].preserves_original_target is True
    assert by_kind["B_change"].selected_pair == ("A♯3", "F♯4")

    assert by_kind["Γ_change"].motion_cost == 0
    assert by_kind["Γ_change"].boundary_change_cost == 0
    assert by_kind["Γ_change"].relation_change_cost == 1
    assert by_kind["Γ_change"].preserves_strict_ordering is False
    assert by_kind["Γ_change"].preserves_original_target is True
    assert by_kind["Γ_change"].selected_pair == ("A♯4", "F♯4")

    assert by_kind["upstream_target_change"].motion_cost == 5
    assert by_kind["upstream_target_change"].boundary_change_cost == 0
    assert by_kind["upstream_target_change"].relation_change_cost == 0
    assert by_kind["upstream_target_change"].upstream_target_change_cost == 1
    assert by_kind["upstream_target_change"].preserves_strict_ordering is True
    assert by_kind["upstream_target_change"].preserves_original_target is False
    assert by_kind["upstream_target_change"].selected_pair == ("E♯4", "F♯4")

    # 枝名は表示ラベルにすぎず、複合変更も軸の組合せとして保持できる。
    _, b_branch, _, _ = build_reexploration_observations()
    combined_branch = replace(
        b_branch,
        branch_kind="combined_change",
        change_axes=ChangeAxes(boundary_changed=True, relation_changed=True),
    )
    combined = evaluate_branch(combined_branch)
    assert combined.boundary_change_cost == 1
    assert combined.relation_change_cost == 1
    assert combined.upstream_target_change_cost == 0
    assert combined.change_axes == ChangeAxes(
        boundary_changed=True,
        relation_changed=True,
    )

    decisions = build_policy_decisions(branches)
    assert tuple(decision.selected_branch_kind for decision in decisions) == (
        "B_change",
        "upstream_target_change",
        "Γ_change",
    )
    assert decisions[0].rejected_branch_kinds == ("upstream_target_change",)
    assert decisions[1].rejected_branch_kinds == ("Γ_change",)
    assert decisions[2].rejected_branch_kinds == ()


def print_observation(branch: BranchEvaluation) -> None:
    print(
        f"[{branch.branch_kind}] selected={branch.selected_pair[0]}-"
        f"{branch.selected_pair[1]}"
    )
    print(
        f"  motion={branch.motion_cost} / boundary={branch.boundary_change_cost}"
        f" / relation={branch.relation_change_cost}"
        f" / upstream_target={branch.upstream_target_change_cost}"
    )
    print(
        f"  preserves_strict_ordering={branch.preserves_strict_ordering}"
        f" / preserves_original_target={branch.preserves_original_target}"
    )


def main() -> None:
    run_checks()
    branches = build_branch_evaluations()
    print("[branch evaluations]")
    for branch in branches:
        print_observation(branch)
    print("[policy decisions]")
    for policy, decision in zip(POLICIES, build_policy_decisions(branches)):
        print(f"[{policy.name}] {policy.description}")
        print(f"  considered={decision.considered_branch_kinds}")
        print(f"  rejected={decision.rejected_branch_kinds}")
        print(f"  ranking={decision.ranked_branch_kinds}")
        print(f"  selected={decision.selected_branch_kind}")


if __name__ == "__main__":
    main()
