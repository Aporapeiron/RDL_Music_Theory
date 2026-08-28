"""主系列と派生系列の並行variation memoryを検査する最小実験。"""

from dataclasses import dataclass

from branch_reentry_policy_stress_1199_1248 import (
    BranchReentryPolicyBundle,
    observe_branch_reentry_policy,
)


@dataclass(frozen=True)
class ParallelVariationMemoryStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ParallelMemoryTrack:
    name: str
    track_kind: str
    shared_anchor: str
    local_memory: tuple[str, ...]
    can_exchange_cues: bool
    merged_into_other_track: bool
    deleted: bool
    status: str


@dataclass(frozen=True)
class MemoryExchangeBoundary:
    shared_item: str
    source_track: str
    target_track: str
    exchange_kind: str
    permits_transfer: bool
    forces_merge: bool
    asserts_equivalence: bool
    status: str


@dataclass(frozen=True)
class ParallelVariationMemoryBundle:
    source_bundle: BranchReentryPolicyBundle
    tracks: tuple[ParallelMemoryTrack, ...]
    exchanges: tuple[MemoryExchangeBoundary, ...]
    shared_memory: tuple[str, ...]
    separated_memory: tuple[str, ...]
    stop_lines: tuple[str, ...]
    generated_track_merge: bool
    generated_equivalence: bool
    generated_deletion: bool
    status: str


@dataclass(frozen=True)
class ParallelVariationMemoryObservation:
    source_status: str
    steps: tuple[ParallelVariationMemoryStep, ...]
    bundle: ParallelVariationMemoryBundle
    parallel_tracks_preserved: bool
    shared_anchor_without_merge: bool
    local_memory_separated: bool
    exchange_without_equivalence: bool
    latent_branch_memory_preserved: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1249, "source_reentry", "reuse_1199_1248_branch_reentry_policy", "branch_reentry_policy_preserved"),
    (1250, "source_reentry", "next_xi_received", "parallel_variation_memory_stress_received"),
    (1251, "source_reentry", "reentry_and_latent_branches_recheck", "reentry_and_latent_branches_available"),
    (1252, "parallel_request", "parallel_memory_request", "parallel_memory_candidate"),
    (1253, "parallel_request", "parallel_not_merge_guard", "parallel_merge_non_identity"),
    (1254, "parallel_request", "shared_anchor_not_equivalence_guard", "shared_anchor_equivalence_blocked"),
    (1255, "parallel_request", "local_memory_not_deletion_guard", "local_memory_deletion_non_identity"),
    (1256, "track_layer", "primary_track_creation", "primary_track_created"),
    (1257, "track_layer", "derivative_track_creation", "derivative_track_created"),
    (1258, "track_layer", "latent_track_creation", "latent_track_created"),
    (1259, "track_layer", "shared_anchor_record", "shared_anchor_recorded"),
    (1260, "track_layer", "track_local_memory_record", "track_local_memory_recorded"),
    (1261, "track_layer", "track_exchange_permission_record", "track_exchange_permission_recorded"),
    (1262, "track_guard", "track_merge_false_check", "track_merge_false_confirmed"),
    (1263, "track_guard", "track_deletion_false_check", "track_deletion_false_confirmed"),
    (1264, "track_guard", "parallel_tracks_non_confluent", "parallel_tracks_non_confluent_recorded"),
    (1265, "exchange_layer", "anchor_exchange_boundary", "anchor_exchange_boundary_recorded"),
    (1266, "exchange_layer", "cadential_cue_exchange_boundary", "cadential_cue_exchange_boundary_recorded"),
    (1267, "exchange_layer", "B_coloring_exchange_boundary", "B_coloring_exchange_boundary_recorded"),
    (1268, "exchange_layer", "echo_memory_exchange_boundary", "echo_memory_exchange_boundary_recorded"),
    (1269, "exchange_guard", "exchange_not_merge_check", "exchange_merge_non_identity"),
    (1270, "exchange_guard", "exchange_not_equivalence_check", "exchange_equivalence_non_identity"),
    (1271, "exchange_guard", "exchange_not_truth_check", "exchange_truth_non_identity"),
    (1272, "memory_partition", "shared_memory_partition", "shared_memory_partition_recorded"),
    (1273, "memory_partition", "separated_memory_partition", "separated_memory_partition_recorded"),
    (1274, "memory_partition", "latent_branch_memory_partition", "latent_branch_memory_partition_recorded"),
    (1275, "memory_partition", "partition_not_erasure_guard", "partition_erasure_non_identity"),
    (1276, "bundle", "parallel_memory_bundle_creation", "parallel_memory_bundle_created"),
    (1277, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1278, "bundle", "stop_lines_carry", "parallel_memory_stop_lines_carried"),
    (1279, "bundle", "generated_track_merge_false", "generated_track_merge_false_recorded"),
    (1280, "bundle", "generated_equivalence_false", "generated_equivalence_false_recorded"),
    (1281, "bundle", "generated_deletion_false", "generated_deletion_false_recorded"),
    (1282, "integrity", "parallel_track_preservation_check", "parallel_track_preservation_confirmed"),
    (1283, "integrity", "shared_anchor_without_merge_check", "shared_anchor_without_merge_confirmed"),
    (1284, "integrity", "local_memory_separation_check", "local_memory_separation_confirmed"),
    (1285, "integrity", "exchange_without_equivalence_check", "exchange_without_equivalence_confirmed"),
    (1286, "integrity", "latent_branch_memory_check", "latent_branch_memory_confirmed"),
    (1287, "non_identity", "parallel_vs_merge_split", "parallel_merge_non_identity_preserved"),
    (1288, "non_identity", "shared_anchor_vs_equivalence_split", "shared_anchor_equivalence_non_identity"),
    (1289, "non_identity", "exchange_vs_truth_split", "exchange_truth_non_identity_preserved"),
    (1290, "non_identity", "separation_vs_deletion_split", "separation_deletion_non_identity"),
    (1291, "music_subject", "parallel_variation_as_polyphonic_memory", "parallel_variation_polyphonic_memory_preserved"),
    (1292, "music_subject", "shared_anchor_with_track_difference", "shared_anchor_track_difference_preserved"),
    (1293, "music_subject", "latent_branch_as_background_continuity", "latent_branch_background_continuity_preserved"),
    (1294, "summary", "parallel_variation_memory_summary", "parallel_variation_memory_observed"),
    (1295, "summary", "shared_separated_memory_summary", "shared_separated_memory_observed"),
    (1296, "summary", "no_merge_no_deletion_summary", "no_merge_no_deletion_confirmed"),
    (1297, "next_plan", "polyphonic_memory_coordination_next_candidate", "polyphonic_memory_coordination_next_candidate"),
    (1298, "next_plan", "next_xi_selection", "xi_polyphonic_memory_coordination_stress"),
)


def _build_steps() -> tuple[ParallelVariationMemoryStep, ...]:
    previous = "branch_reentry_policy_1199_1248"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            ParallelVariationMemoryStep(
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


def build_parallel_variation_memory_bundle(
    source: BranchReentryPolicyBundle,
) -> ParallelVariationMemoryBundle:
    anchor = source.source_bundle.retained_anchor
    tracks = (
        ParallelMemoryTrack(
            name="primary_variation_sequence",
            track_kind="primary",
            shared_anchor=anchor,
            local_memory=("surface_variation", "cadential_position_variation"),
            can_exchange_cues=True,
            merged_into_other_track=False,
            deleted=False,
            status="primary_track_retained_without_merge",
        ),
        ParallelMemoryTrack(
            name=source.reentry_candidates[0].branch.label,
            track_kind="derivative",
            shared_anchor=anchor,
            local_memory=("B_coloring_derivative_return",),
            can_exchange_cues=True,
            merged_into_other_track=False,
            deleted=False,
            status="derivative_track_retained_without_primary_confluence",
        ),
        ParallelMemoryTrack(
            name=source.latent_branches[0].branch.label,
            track_kind="latent",
            shared_anchor=anchor,
            local_memory=("contextual_echo_unheard_option",),
            can_exchange_cues=False,
            merged_into_other_track=False,
            deleted=False,
            status="latent_track_retained_as_background_continuity",
        ),
    )
    exchanges = (
        MemoryExchangeBoundary(
            shared_item=anchor,
            source_track="primary_variation_sequence",
            target_track=source.reentry_candidates[0].branch.label,
            exchange_kind="anchor_reference",
            permits_transfer=True,
            forces_merge=False,
            asserts_equivalence=False,
            status="anchor_exchange_permitted_without_track_merge",
        ),
        MemoryExchangeBoundary(
            shared_item="cadential_position_cue",
            source_track="primary_variation_sequence",
            target_track=source.reentry_candidates[0].branch.label,
            exchange_kind="cadential_cue_reference",
            permits_transfer=True,
            forces_merge=False,
            asserts_equivalence=False,
            status="cadential_cue_exchange_permitted_without_equivalence",
        ),
        MemoryExchangeBoundary(
            shared_item="B_coloring_memory",
            source_track=source.reentry_candidates[0].branch.label,
            target_track="primary_variation_sequence",
            exchange_kind="coloring_feedback",
            permits_transfer=True,
            forces_merge=False,
            asserts_equivalence=False,
            status="B_coloring_feedback_permitted_without_truth_claim",
        ),
        MemoryExchangeBoundary(
            shared_item="contextual_echo_memory",
            source_track=source.latent_branches[0].branch.label,
            target_track="primary_variation_sequence",
            exchange_kind="latent_reference",
            permits_transfer=False,
            forces_merge=False,
            asserts_equivalence=False,
            status="echo_memory_retained_without_exchange",
        ),
    )
    return ParallelVariationMemoryBundle(
        source_bundle=source,
        tracks=tracks,
        exchanges=exchanges,
        shared_memory=(anchor, "cadential_position_cue"),
        separated_memory=(
            "surface_variation",
            "B_coloring_derivative_return",
            "contextual_echo_unheard_option",
        ),
        stop_lines=(
            "parallel_not_merge",
            "shared_anchor_not_equivalence",
            "exchange_not_truth",
            "local_memory_not_deletion",
            "latent_track_not_erasure",
        ),
        generated_track_merge=False,
        generated_equivalence=False,
        generated_deletion=False,
        status="parallel_variation_memory_bundle_1249_1298_built_without_track_merge_or_memory_erasure",
    )


def observe_parallel_variation_memory() -> ParallelVariationMemoryObservation:
    source = observe_branch_reentry_policy()
    bundle = build_parallel_variation_memory_bundle(source.bundle)
    steps = _build_steps()

    return ParallelVariationMemoryObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        parallel_tracks_preserved=(
            len(bundle.tracks) == 3
            and all(track.merged_into_other_track is False for track in bundle.tracks)
        ),
        shared_anchor_without_merge=(
            bundle.generated_track_merge is False
            and all(exchange.forces_merge is False for exchange in bundle.exchanges)
        ),
        local_memory_separated=len(bundle.separated_memory) == 3,
        exchange_without_equivalence=(
            bundle.generated_equivalence is False
            and all(exchange.asserts_equivalence is False for exchange in bundle.exchanges)
        ),
        latent_branch_memory_preserved=(
            bundle.tracks[2].track_kind == "latent"
            and bundle.tracks[2].deleted is False
            and bundle.generated_deletion is False
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="parallel_variation_memory_1249_1298_observed_without_track_merge_or_memory_erasure",
    )


def run_checks() -> None:
    observation = observe_parallel_variation_memory()
    bundle = observation.bundle

    assert observation.source_status == (
        "branch_reentry_policy_1199_1248_observed_without_primary_merge_or_deletion"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1249
    assert observation.steps[-1].number == 1298
    assert observation.parallel_tracks_preserved is True
    assert observation.shared_anchor_without_merge is True
    assert observation.local_memory_separated is True
    assert observation.exchange_without_equivalence is True
    assert observation.latent_branch_memory_preserved is True
    assert len(bundle.tracks) == 3
    assert len(bundle.exchanges) == 4
    assert bundle.generated_track_merge is False
    assert bundle.generated_equivalence is False
    assert bundle.generated_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_polyphonic_memory_coordination_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_parallel_variation_memory().status)
