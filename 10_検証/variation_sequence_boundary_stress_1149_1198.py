"""variation move列の同一anchor保持と分岐境界を検査する最小実験。"""

from dataclasses import dataclass

from refrain_variation_lifecycle_stress_1099_1148 import (
    RefrainVariationLifecycleBundle,
    observe_refrain_variation_lifecycle,
)


@dataclass(frozen=True)
class VariationSequenceBoundaryStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class VariationSequenceEvent:
    index: int
    variation_name: str
    previous_event: str
    preserves_anchor: bool
    cumulative_anchor_strength: float
    opens_branch: bool
    branch_reason: str
    closes_sequence: bool
    status: str


@dataclass(frozen=True)
class VariationBranchCandidate:
    label: str
    source_event: str
    branch_kind: str
    shares_anchor: bool
    requires_new_sequence: bool
    deleted: bool
    status: str


@dataclass(frozen=True)
class VariationSequenceBoundaryBundle:
    source_bundle: RefrainVariationLifecycleBundle
    sequence_events: tuple[VariationSequenceEvent, ...]
    branch_candidates: tuple[VariationBranchCandidate, ...]
    retained_anchor: str
    sequence_threshold_rule: str
    stop_lines: tuple[str, ...]
    generated_final_sequence: bool
    generated_single_lineage: bool
    generated_deletion: bool
    status: str


@dataclass(frozen=True)
class VariationSequenceBoundaryObservation:
    source_status: str
    steps: tuple[VariationSequenceBoundaryStep, ...]
    bundle: VariationSequenceBoundaryBundle
    sequence_preserves_anchor_chain: bool
    branch_candidates_retained: bool
    sequence_is_not_final_form: bool
    sequence_is_not_single_lineage: bool
    branches_are_not_deletions: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1149, "source_reentry", "reuse_1099_1148_variation_lifecycle_bundle", "variation_lifecycle_bundle_preserved"),
    (1150, "source_reentry", "next_xi_received", "variation_sequence_boundary_stress_received"),
    (1151, "source_reentry", "variation_moves_recheck", "variation_moves_available"),
    (1152, "sequence_request", "variation_sequence_request", "variation_sequence_candidate"),
    (1153, "sequence_request", "sequence_not_final_form_guard", "sequence_final_form_non_identity"),
    (1154, "sequence_request", "sequence_not_single_lineage_guard", "single_lineage_blocked"),
    (1155, "sequence_request", "branch_not_deletion_guard", "branch_deletion_non_identity"),
    (1156, "sequence_layer", "surface_variation_event", "surface_variation_event_recorded"),
    (1157, "sequence_layer", "B_coloring_variation_event", "B_coloring_variation_event_recorded"),
    (1158, "sequence_layer", "cadential_position_variation_event", "cadential_position_variation_event_recorded"),
    (1159, "sequence_layer", "contextual_echo_variation_event", "contextual_echo_variation_event_recorded"),
    (1160, "sequence_layer", "cumulative_anchor_strength_record", "cumulative_anchor_strength_recorded"),
    (1161, "sequence_layer", "sequence_threshold_rule_record", "sequence_threshold_rule_recorded"),
    (1162, "sequence_guard", "anchor_chain_check", "anchor_chain_confirmed"),
    (1163, "sequence_guard", "sequence_closure_false_check", "sequence_closure_false_confirmed"),
    (1164, "sequence_guard", "sequence_variation_not_repetition", "sequence_variation_repetition_non_identity"),
    (1165, "branch_layer", "branch_candidate_request", "branch_candidate_created"),
    (1166, "branch_layer", "B_coloring_branch_candidate", "B_coloring_branch_candidate_recorded"),
    (1167, "branch_layer", "contextual_echo_branch_candidate", "contextual_echo_branch_candidate_recorded"),
    (1168, "branch_layer", "shared_anchor_branch_record", "shared_anchor_branch_recorded"),
    (1169, "branch_layer", "new_sequence_requirement_record", "new_sequence_requirement_recorded"),
    (1170, "branch_layer", "branch_deleted_false_record", "branch_deleted_false_recorded"),
    (1171, "branch_guard", "branch_not_error_check", "branch_error_non_identity"),
    (1172, "branch_guard", "branch_not_erasure_check", "branch_erasure_non_identity"),
    (1173, "branch_guard", "branch_not_final_split_check", "branch_final_split_confirmed"),
    (1174, "boundary_view", "sequence_boundary_creation", "sequence_boundary_created"),
    (1175, "boundary_view", "anchor_retention_view", "anchor_retention_view_created"),
    (1176, "boundary_view", "branch_retention_view", "branch_retention_view_created"),
    (1177, "boundary_view", "sequence_branch_non_confluence", "sequence_branch_non_confluence_recorded"),
    (1178, "bundle", "variation_sequence_boundary_bundle_creation", "variation_sequence_boundary_bundle_created"),
    (1179, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1180, "bundle", "stop_lines_carry", "variation_sequence_stop_lines_carried"),
    (1181, "bundle", "generated_final_sequence_false", "generated_final_sequence_false_recorded"),
    (1182, "bundle", "generated_single_lineage_false", "generated_single_lineage_false_recorded"),
    (1183, "bundle", "generated_deletion_false", "generated_deletion_false_recorded"),
    (1184, "integrity", "anchor_chain_preservation_check", "anchor_chain_preservation_confirmed"),
    (1185, "integrity", "branch_candidate_retention_check", "branch_candidate_retention_confirmed"),
    (1186, "integrity", "sequence_final_form_split_check", "sequence_final_form_split_confirmed"),
    (1187, "integrity", "single_lineage_split_check", "single_lineage_split_confirmed"),
    (1188, "integrity", "branch_deletion_split_check", "branch_deletion_split_confirmed"),
    (1189, "non_identity", "sequence_vs_final_form_split", "sequence_final_form_non_identity_preserved"),
    (1190, "non_identity", "sequence_vs_single_lineage_split", "sequence_single_lineage_non_identity"),
    (1191, "non_identity", "branch_vs_deletion_split", "branch_deletion_non_identity_preserved"),
    (1192, "non_identity", "branch_vs_error_split", "branch_error_non_identity_preserved"),
    (1193, "music_subject", "variation_sequence_as_development", "variation_sequence_development_preserved"),
    (1194, "music_subject", "branch_as_possible_derivation", "branch_possible_derivation_preserved"),
    (1195, "music_subject", "non_confluent_variation_memory", "non_confluent_variation_memory_preserved"),
    (1196, "summary", "variation_sequence_boundary_summary", "variation_sequence_boundary_observed"),
    (1197, "next_plan", "branch_reentry_policy_next_candidate", "branch_reentry_policy_next_candidate"),
    (1198, "next_plan", "next_xi_selection", "xi_branch_reentry_policy_stress"),
)


def _build_steps() -> tuple[VariationSequenceBoundaryStep, ...]:
    previous = "refrain_variation_lifecycle_1099_1148"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            VariationSequenceBoundaryStep(
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


def build_variation_sequence_boundary_bundle(
    source: RefrainVariationLifecycleBundle,
) -> VariationSequenceBoundaryBundle:
    lifecycle = source.lifecycle_record
    event_names = (
        "surface_variation",
        "B_coloring_variation",
        "cadential_position_variation",
        "contextual_echo_variation",
    )
    strengths = (0.94, 0.86, 0.81, 0.74)
    events = tuple(
        VariationSequenceEvent(
            index=index,
            variation_name=name,
            previous_event="sequence_start" if index == 1 else event_names[index - 2],
            preserves_anchor=True,
            cumulative_anchor_strength=strengths[index - 1],
            opens_branch=name in lifecycle.latent_variations + lifecycle.compressed_variations,
            branch_reason=(
                "latent_or_compressed_variation_can_open_derivative_sequence"
                if name in lifecycle.latent_variations + lifecycle.compressed_variations
                else "active_variation_continues_primary_sequence"
            ),
            closes_sequence=False,
            status="variation_sequence_event_recorded_without_closure",
        )
        for index, name in enumerate(event_names, start=1)
    )
    branches = (
        VariationBranchCandidate(
            label="B_coloring_derivative_sequence",
            source_event="B_coloring_variation",
            branch_kind="latent_context_branch",
            shares_anchor=True,
            requires_new_sequence=True,
            deleted=False,
            status="branch_candidate_retained_without_erasure",
        ),
        VariationBranchCandidate(
            label="contextual_echo_derivative_sequence",
            source_event="contextual_echo_variation",
            branch_kind="compressed_echo_branch",
            shares_anchor=True,
            requires_new_sequence=True,
            deleted=False,
            status="branch_candidate_retained_without_erasure",
        ),
    )
    return VariationSequenceBoundaryBundle(
        source_bundle=source,
        sequence_events=events,
        branch_candidates=branches,
        retained_anchor=lifecycle.identity_anchor,
        sequence_threshold_rule="anchor_strength_above_0_70_allows_sequence_continuity",
        stop_lines=(
            "sequence_not_final_form",
            "sequence_not_single_lineage",
            "branch_not_deletion",
            "branch_not_error",
            "non_confluent_variation_memory_retained",
        ),
        generated_final_sequence=False,
        generated_single_lineage=False,
        generated_deletion=False,
        status="variation_sequence_boundary_bundle_1149_1198_built_without_final_sequence_or_branch_erasure",
    )


def observe_variation_sequence_boundary() -> VariationSequenceBoundaryObservation:
    source = observe_refrain_variation_lifecycle()
    bundle = build_variation_sequence_boundary_bundle(source.bundle)
    steps = _build_steps()

    return VariationSequenceBoundaryObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        sequence_preserves_anchor_chain=(
            len(bundle.sequence_events) == 4
            and all(event.preserves_anchor for event in bundle.sequence_events)
            and min(event.cumulative_anchor_strength for event in bundle.sequence_events) > 0.70
        ),
        branch_candidates_retained=(
            len(bundle.branch_candidates) == 2
            and all(candidate.deleted is False for candidate in bundle.branch_candidates)
        ),
        sequence_is_not_final_form=bundle.generated_final_sequence is False,
        sequence_is_not_single_lineage=bundle.generated_single_lineage is False,
        branches_are_not_deletions=(
            bundle.generated_deletion is False
            and all(candidate.deleted is False for candidate in bundle.branch_candidates)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="variation_sequence_boundary_1149_1198_observed_without_final_sequence_or_branch_erasure",
    )


def run_checks() -> None:
    observation = observe_variation_sequence_boundary()
    bundle = observation.bundle

    assert observation.source_status == (
        "refrain_variation_lifecycle_1099_1148_observed_without_final_form_or_erasure"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1149
    assert observation.steps[-1].number == 1198
    assert observation.sequence_preserves_anchor_chain is True
    assert observation.branch_candidates_retained is True
    assert observation.sequence_is_not_final_form is True
    assert observation.sequence_is_not_single_lineage is True
    assert observation.branches_are_not_deletions is True
    assert len(bundle.sequence_events) == 4
    assert len(bundle.branch_candidates) == 2
    assert bundle.generated_final_sequence is False
    assert bundle.generated_single_lineage is False
    assert bundle.generated_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_branch_reentry_policy_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_variation_sequence_boundary().status)
