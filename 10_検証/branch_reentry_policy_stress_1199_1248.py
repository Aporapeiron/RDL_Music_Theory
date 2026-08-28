"""variation branch candidateの再入policyを検査する最小実験。"""

from dataclasses import dataclass

from variation_sequence_boundary_stress_1149_1198 import (
    VariationBranchCandidate,
    VariationSequenceBoundaryBundle,
    observe_variation_sequence_boundary,
)


@dataclass(frozen=True)
class BranchReentryPolicyStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class BranchReentryCondition:
    name: str
    condition_source: str
    target_branch: str
    permits_reentry: bool
    keeps_latent_if_unmet: bool
    musical_reason: str
    status: str


@dataclass(frozen=True)
class BranchReentryDecision:
    branch: VariationBranchCandidate
    condition: BranchReentryCondition
    reentry_state: str
    enters_primary_sequence: bool
    starts_derivative_sequence: bool
    remains_latent: bool
    selected_as_final: bool
    deleted: bool
    status: str


@dataclass(frozen=True)
class BranchReentryPolicyBundle:
    source_bundle: VariationSequenceBoundaryBundle
    conditions: tuple[BranchReentryCondition, ...]
    decisions: tuple[BranchReentryDecision, ...]
    reentry_candidates: tuple[BranchReentryDecision, ...]
    latent_branches: tuple[BranchReentryDecision, ...]
    stop_lines: tuple[str, ...]
    generated_primary_confluence: bool
    generated_final_selection: bool
    generated_deletion: bool
    status: str


@dataclass(frozen=True)
class BranchReentryPolicyObservation:
    source_status: str
    steps: tuple[BranchReentryPolicyStep, ...]
    bundle: BranchReentryPolicyBundle
    reentry_policy_distinguishes_conditions: bool
    permitted_branch_starts_derivative_sequence: bool
    latent_branch_retained: bool
    reentry_not_primary_confluence: bool
    reentry_not_final_selection_or_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1199, "source_reentry", "reuse_1149_1198_variation_sequence_boundary", "variation_sequence_boundary_preserved"),
    (1200, "source_reentry", "next_xi_received", "branch_reentry_policy_stress_received"),
    (1201, "source_reentry", "branch_candidates_recheck", "branch_candidates_available"),
    (1202, "policy_request", "branch_reentry_policy_request", "branch_reentry_policy_candidate"),
    (1203, "policy_request", "reentry_not_primary_confluence_guard", "primary_confluence_blocked"),
    (1204, "policy_request", "reentry_not_final_selection_guard", "final_selection_blocked"),
    (1205, "policy_request", "latent_not_deletion_guard", "latent_deletion_non_identity"),
    (1206, "condition_layer", "B_coloring_reentry_condition", "B_coloring_reentry_condition_recorded"),
    (1207, "condition_layer", "contextual_echo_reentry_condition", "contextual_echo_reentry_condition_recorded"),
    (1208, "condition_layer", "condition_source_record", "condition_source_recorded"),
    (1209, "condition_layer", "musical_reason_record", "musical_reason_recorded"),
    (1210, "condition_guard", "condition_not_truth_guard", "condition_truth_non_identity"),
    (1211, "condition_guard", "condition_not_selection_guard", "condition_selection_non_identity"),
    (1212, "condition_guard", "unmet_condition_keeps_latent", "unmet_condition_latent_retention_recorded"),
    (1213, "decision_layer", "B_coloring_branch_decision", "B_coloring_branch_decision_recorded"),
    (1214, "decision_layer", "contextual_echo_branch_decision", "contextual_echo_branch_decision_recorded"),
    (1215, "decision_layer", "reentry_state_record", "reentry_state_recorded"),
    (1216, "decision_layer", "derivative_sequence_flag_record", "derivative_sequence_flag_recorded"),
    (1217, "decision_layer", "primary_sequence_false_record", "primary_sequence_false_recorded"),
    (1218, "decision_layer", "final_selection_false_record", "final_selection_false_recorded"),
    (1219, "decision_layer", "deletion_false_record", "deletion_false_recorded"),
    (1220, "reentry_view", "reentry_candidate_view_creation", "reentry_candidate_view_created"),
    (1221, "reentry_view", "latent_branch_view_creation", "latent_branch_view_created"),
    (1222, "reentry_view", "branch_policy_non_confluence", "branch_policy_non_confluence_recorded"),
    (1223, "reentry_view", "reentry_without_main_sequence_merge", "reentry_without_main_sequence_merge_recorded"),
    (1224, "bundle", "branch_reentry_policy_bundle_creation", "branch_reentry_policy_bundle_created"),
    (1225, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1226, "bundle", "stop_lines_carry", "branch_reentry_stop_lines_carried"),
    (1227, "bundle", "generated_primary_confluence_false", "generated_primary_confluence_false_recorded"),
    (1228, "bundle", "generated_final_selection_false", "generated_final_selection_false_recorded"),
    (1229, "bundle", "generated_deletion_false", "generated_deletion_false_recorded"),
    (1230, "integrity", "condition_distinction_check", "condition_distinction_confirmed"),
    (1231, "integrity", "derivative_sequence_check", "derivative_sequence_confirmed"),
    (1232, "integrity", "latent_branch_retention_check", "latent_branch_retention_confirmed"),
    (1233, "integrity", "primary_confluence_split_check", "primary_confluence_split_confirmed"),
    (1234, "integrity", "final_selection_deletion_split_check", "final_selection_deletion_split_confirmed"),
    (1235, "non_identity", "reentry_vs_primary_merge_split", "reentry_primary_merge_non_identity"),
    (1236, "non_identity", "reentry_vs_final_selection_split", "reentry_final_selection_non_identity"),
    (1237, "non_identity", "latent_vs_deletion_split", "latent_deletion_non_identity_preserved"),
    (1238, "non_identity", "policy_vs_truth_split", "policy_truth_non_identity"),
    (1239, "music_subject", "branch_reentry_as_derivative_return", "branch_reentry_derivative_return_preserved"),
    (1240, "music_subject", "latent_branch_as_unheard_option", "latent_branch_unheard_option_preserved"),
    (1241, "music_subject", "parallel_development_memory", "parallel_development_memory_preserved"),
    (1242, "summary", "branch_reentry_policy_summary", "branch_reentry_policy_observed"),
    (1243, "summary", "latent_retention_summary", "latent_retention_observed"),
    (1244, "summary", "non_confluence_summary", "non_confluence_confirmed"),
    (1245, "summary", "no_selection_no_deletion_summary", "no_selection_no_deletion_confirmed"),
    (1246, "summary", "no_mutation_summary", "no_mutation_confirmed"),
    (1247, "next_plan", "parallel_variation_memory_next_candidate", "parallel_variation_memory_next_candidate"),
    (1248, "next_plan", "next_xi_selection", "xi_parallel_variation_memory_stress"),
)


def _build_steps() -> tuple[BranchReentryPolicyStep, ...]:
    previous = "variation_sequence_boundary_1149_1198"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            BranchReentryPolicyStep(
                number=number,
                phase=phase,
                name=name,
                source=previous,
                result=result,
                generated_mutation=False,
            )
        )
        previous = result
    return tuple(steps)


def build_branch_reentry_policy_bundle(
    source: VariationSequenceBoundaryBundle,
) -> BranchReentryPolicyBundle:
    b_branch, echo_branch = source.branch_candidates
    b_condition = BranchReentryCondition(
        name="B_context_returns_with_anchor_strength",
        condition_source="B_coloring_variation_and_anchor_chain",
        target_branch=b_branch.label,
        permits_reentry=True,
        keeps_latent_if_unmet=True,
        musical_reason="B_coloring_can_start_derivative_sequence_without_merging_primary_sequence",
        status="branch_reentry_condition_permits_derivative_sequence",
    )
    echo_condition = BranchReentryCondition(
        name="echo_context_remains_below_reentry_threshold",
        condition_source="contextual_echo_variation_and_memory_density",
        target_branch=echo_branch.label,
        permits_reentry=False,
        keeps_latent_if_unmet=True,
        musical_reason="echo_branch_remains_available_as_unheard_option",
        status="branch_reentry_condition_keeps_branch_latent",
    )
    decisions = (
        BranchReentryDecision(
            branch=b_branch,
            condition=b_condition,
            reentry_state="derivative_sequence_reentry_candidate",
            enters_primary_sequence=False,
            starts_derivative_sequence=True,
            remains_latent=False,
            selected_as_final=False,
            deleted=False,
            status="branch_reentry_allowed_without_primary_confluence",
        ),
        BranchReentryDecision(
            branch=echo_branch,
            condition=echo_condition,
            reentry_state="latent_branch_retained",
            enters_primary_sequence=False,
            starts_derivative_sequence=False,
            remains_latent=True,
            selected_as_final=False,
            deleted=False,
            status="branch_reentry_deferred_without_deletion",
        ),
    )
    reentry_candidates = tuple(item for item in decisions if item.starts_derivative_sequence)
    latent_branches = tuple(item for item in decisions if item.remains_latent)
    return BranchReentryPolicyBundle(
        source_bundle=source,
        conditions=(b_condition, echo_condition),
        decisions=decisions,
        reentry_candidates=reentry_candidates,
        latent_branches=latent_branches,
        stop_lines=(
            "reentry_not_primary_confluence",
            "reentry_not_final_selection",
            "latent_not_deletion",
            "condition_not_truth",
            "policy_not_single_lineage",
        ),
        generated_primary_confluence=False,
        generated_final_selection=False,
        generated_deletion=False,
        status="branch_reentry_policy_bundle_1199_1248_built_without_primary_merge_or_deletion",
    )


def observe_branch_reentry_policy() -> BranchReentryPolicyObservation:
    source = observe_variation_sequence_boundary()
    bundle = build_branch_reentry_policy_bundle(source.bundle)
    steps = _build_steps()

    return BranchReentryPolicyObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        reentry_policy_distinguishes_conditions=(
            len(bundle.conditions) == 2
            and bundle.conditions[0].permits_reentry != bundle.conditions[1].permits_reentry
        ),
        permitted_branch_starts_derivative_sequence=(
            len(bundle.reentry_candidates) == 1
            and bundle.reentry_candidates[0].starts_derivative_sequence is True
            and bundle.reentry_candidates[0].enters_primary_sequence is False
        ),
        latent_branch_retained=(
            len(bundle.latent_branches) == 1
            and bundle.latent_branches[0].deleted is False
        ),
        reentry_not_primary_confluence=bundle.generated_primary_confluence is False,
        reentry_not_final_selection_or_deletion=(
            bundle.generated_final_selection is False
            and bundle.generated_deletion is False
            and all(decision.selected_as_final is False for decision in bundle.decisions)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="branch_reentry_policy_1199_1248_observed_without_primary_merge_or_deletion",
    )


def run_checks() -> None:
    observation = observe_branch_reentry_policy()
    bundle = observation.bundle

    assert observation.source_status == (
        "variation_sequence_boundary_1149_1198_observed_without_final_sequence_or_branch_erasure"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1199
    assert observation.steps[-1].number == 1248
    assert observation.reentry_policy_distinguishes_conditions is True
    assert observation.permitted_branch_starts_derivative_sequence is True
    assert observation.latent_branch_retained is True
    assert observation.reentry_not_primary_confluence is True
    assert observation.reentry_not_final_selection_or_deletion is True
    assert len(bundle.reentry_candidates) == 1
    assert len(bundle.latent_branches) == 1
    assert bundle.generated_primary_confluence is False
    assert bundle.generated_final_selection is False
    assert bundle.generated_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_parallel_variation_memory_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_branch_reentry_policy().status)
