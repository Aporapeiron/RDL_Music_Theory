"""リフレイン同一性通過後のvariation lifecycleを検査する最小実験。"""

from dataclasses import dataclass

from refrain_identity_boundary_stress_1049_1098 import (
    RefrainIdentityBoundaryBundle,
    observe_refrain_identity_boundary,
)


@dataclass(frozen=True)
class RefrainVariationLifecycleStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class VariationMove:
    name: str
    source_cue: str
    preserves_anchor: bool
    changes_surface: bool
    changes_context: bool
    collapses_identity: bool
    status: str


@dataclass(frozen=True)
class RefrainVariationLifecycleRecord:
    refrain_label: str
    lifecycle_state: str
    identity_anchor: str
    variation_moves: tuple[VariationMove, ...]
    active_variations: tuple[str, ...]
    latent_variations: tuple[str, ...]
    compressed_variations: tuple[str, ...]
    preserves_same_with_difference: bool
    repeats_identically: bool
    becomes_new_object: bool
    deleted_variation: bool
    status: str


@dataclass(frozen=True)
class RefrainVariationLifecycleBundle:
    source_bundle: RefrainIdentityBoundaryBundle
    lifecycle_record: RefrainVariationLifecycleRecord
    stop_lines: tuple[str, ...]
    generated_identity_collapse: bool
    generated_new_object: bool
    generated_deletion: bool
    generated_final_form: bool
    status: str


@dataclass(frozen=True)
class RefrainVariationLifecycleObservation:
    source_status: str
    steps: tuple[RefrainVariationLifecycleStep, ...]
    bundle: RefrainVariationLifecycleBundle
    variation_preserves_identity_anchor: bool
    variation_is_not_identical_repetition: bool
    variation_is_not_new_object: bool
    lifecycle_keeps_active_and_latent: bool
    compression_is_not_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1099, "source_reentry", "reuse_1049_1098_refrain_identity_bundle", "refrain_identity_bundle_preserved"),
    (1100, "source_reentry", "next_xi_received", "refrain_variation_lifecycle_stress_received"),
    (1101, "source_reentry", "same_with_difference_recheck", "same_with_difference_available"),
    (1102, "variation_request", "variation_lifecycle_request", "variation_lifecycle_candidate"),
    (1103, "variation_request", "variation_not_repetition_guard", "variation_repetition_non_identity"),
    (1104, "variation_request", "variation_not_new_object_guard", "variation_new_object_non_identity"),
    (1105, "variation_request", "variation_not_identity_collapse_guard", "identity_collapse_blocked"),
    (1106, "move_layer", "surface_variation_move", "surface_variation_move_recorded"),
    (1107, "move_layer", "B_coloring_variation_move", "B_coloring_variation_move_recorded"),
    (1108, "move_layer", "cadential_position_variation_move", "cadential_position_variation_move_recorded"),
    (1109, "move_layer", "contextual_echo_variation_move", "contextual_echo_variation_move_recorded"),
    (1110, "move_guard", "move_preserves_anchor_check", "move_preserves_anchor_confirmed"),
    (1111, "move_guard", "move_changes_surface_check", "move_changes_surface_confirmed"),
    (1112, "move_guard", "move_does_not_collapse_identity", "move_identity_collapse_blocked"),
    (1113, "lifecycle_layer", "lifecycle_record_creation", "lifecycle_record_created"),
    (1114, "lifecycle_layer", "identity_anchor_carry", "identity_anchor_carried"),
    (1115, "lifecycle_layer", "active_variation_view", "active_variation_view_recorded"),
    (1116, "lifecycle_layer", "latent_variation_view", "latent_variation_view_recorded"),
    (1117, "lifecycle_layer", "compressed_variation_view", "compressed_variation_view_recorded"),
    (1118, "lifecycle_layer", "same_with_difference_carry", "same_with_difference_carried"),
    (1119, "lifecycle_layer", "identical_repetition_false_record", "identical_repetition_false_recorded"),
    (1120, "lifecycle_layer", "new_object_false_record", "new_object_false_recorded"),
    (1121, "lifecycle_layer", "deleted_variation_false_record", "deleted_variation_false_recorded"),
    (1122, "compression_view", "variation_compression_request", "variation_compression_candidate"),
    (1123, "compression_view", "compression_not_deletion_guard", "compression_deletion_non_identity"),
    (1124, "compression_view", "compressed_variation_keeps_anchor", "compressed_variation_anchor_preserved"),
    (1125, "compression_view", "compressed_variation_keeps_reentry", "compressed_variation_reentry_preserved"),
    (1126, "bundle", "variation_lifecycle_bundle_creation", "variation_lifecycle_bundle_created"),
    (1127, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1128, "bundle", "stop_lines_carry", "variation_lifecycle_stop_lines_carried"),
    (1129, "bundle", "generated_identity_collapse_false", "generated_identity_collapse_false_recorded"),
    (1130, "bundle", "generated_new_object_false", "generated_new_object_false_recorded"),
    (1131, "bundle", "generated_deletion_false", "generated_deletion_false_recorded"),
    (1132, "bundle", "generated_final_form_false", "generated_final_form_false_recorded"),
    (1133, "integrity", "anchor_preservation_check", "anchor_preservation_confirmed"),
    (1134, "integrity", "variation_repetition_split_check", "variation_repetition_split_confirmed"),
    (1135, "integrity", "variation_new_object_split_check", "variation_new_object_split_confirmed"),
    (1136, "integrity", "active_latent_lifecycle_check", "active_latent_lifecycle_confirmed"),
    (1137, "integrity", "compression_deletion_split_check", "compression_deletion_split_confirmed"),
    (1138, "non_identity", "variation_vs_repetition_split", "variation_repetition_non_identity_preserved"),
    (1139, "non_identity", "variation_vs_new_object_split", "variation_new_object_non_identity_preserved"),
    (1140, "non_identity", "lifecycle_vs_final_form_split", "lifecycle_final_form_non_identity"),
    (1141, "non_identity", "compression_vs_erasure_split", "compression_erasure_non_identity"),
    (1142, "music_subject", "variation_as_lived_refrain", "variation_as_lived_refrain_preserved"),
    (1143, "music_subject", "refrain_develops_without_losing_anchor", "refrain_development_anchor_preserved"),
    (1144, "music_subject", "memory_density_rebalanced", "memory_density_rebalanced"),
    (1145, "summary", "variation_lifecycle_summary", "variation_lifecycle_observed"),
    (1146, "summary", "no_final_form_summary", "no_final_form_confirmed"),
    (1147, "next_plan", "variation_sequence_boundary_next_candidate", "variation_sequence_boundary_next_candidate"),
    (1148, "next_plan", "next_xi_selection", "xi_variation_sequence_boundary_stress"),
)


def _build_steps() -> tuple[RefrainVariationLifecycleStep, ...]:
    previous = "refrain_identity_boundary_1049_1098"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            RefrainVariationLifecycleStep(
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


def build_refrain_variation_lifecycle_bundle(
    source: RefrainIdentityBoundaryBundle,
) -> RefrainVariationLifecycleBundle:
    evaluation = source.evaluation
    moves = (
        VariationMove(
            name="surface_variation",
            source_cue="surface_variation",
            preserves_anchor=True,
            changes_surface=True,
            changes_context=False,
            collapses_identity=False,
            status="variation_move_preserves_refrain_anchor",
        ),
        VariationMove(
            name="B_coloring_variation",
            source_cue="B_shift",
            preserves_anchor=True,
            changes_surface=False,
            changes_context=True,
            collapses_identity=False,
            status="variation_move_changes_context_without_new_object",
        ),
        VariationMove(
            name="cadential_position_variation",
            source_cue="cadential_position",
            preserves_anchor=True,
            changes_surface=True,
            changes_context=True,
            collapses_identity=False,
            status="variation_move_keeps_mixed_identity_difference",
        ),
        VariationMove(
            name="contextual_echo_variation",
            source_cue="contextual_difference",
            preserves_anchor=True,
            changes_surface=False,
            changes_context=True,
            collapses_identity=False,
            status="variation_move_retains_echo_as_memory",
        ),
    )
    lifecycle = RefrainVariationLifecycleRecord(
        refrain_label=evaluation.returned_label,
        lifecycle_state="variation_lifecycle_after_refrain_identity",
        identity_anchor="C_major_continuation_frame_anchor",
        variation_moves=moves,
        active_variations=("surface_variation", "cadential_position_variation"),
        latent_variations=("B_coloring_variation",),
        compressed_variations=("contextual_echo_variation",),
        preserves_same_with_difference=True,
        repeats_identically=False,
        becomes_new_object=False,
        deleted_variation=False,
        status="refrain_variation_lifecycle_recorded_without_identity_collapse",
    )
    return RefrainVariationLifecycleBundle(
        source_bundle=source,
        lifecycle_record=lifecycle,
        stop_lines=(
            "variation_not_repetition",
            "variation_not_new_object",
            "variation_not_identity_collapse",
            "compression_not_deletion",
            "lifecycle_not_final_form",
        ),
        generated_identity_collapse=False,
        generated_new_object=False,
        generated_deletion=False,
        generated_final_form=False,
        status="refrain_variation_lifecycle_bundle_1099_1148_built_without_final_form_or_erasure",
    )


def observe_refrain_variation_lifecycle() -> RefrainVariationLifecycleObservation:
    source = observe_refrain_identity_boundary()
    bundle = build_refrain_variation_lifecycle_bundle(source.bundle)
    lifecycle = bundle.lifecycle_record
    steps = _build_steps()

    return RefrainVariationLifecycleObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        variation_preserves_identity_anchor=(
            lifecycle.preserves_same_with_difference is True
            and all(move.preserves_anchor for move in lifecycle.variation_moves)
        ),
        variation_is_not_identical_repetition=(
            lifecycle.repeats_identically is False
            and bundle.generated_identity_collapse is False
        ),
        variation_is_not_new_object=(
            lifecycle.becomes_new_object is False
            and bundle.generated_new_object is False
        ),
        lifecycle_keeps_active_and_latent=(
            len(lifecycle.active_variations) == 2
            and len(lifecycle.latent_variations) == 1
            and len(lifecycle.compressed_variations) == 1
        ),
        compression_is_not_deletion=(
            lifecycle.deleted_variation is False
            and bundle.generated_deletion is False
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="refrain_variation_lifecycle_1099_1148_observed_without_final_form_or_erasure",
    )


def run_checks() -> None:
    observation = observe_refrain_variation_lifecycle()
    bundle = observation.bundle

    assert observation.source_status == (
        "refrain_identity_boundary_1049_1098_observed_as_same_with_difference"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1099
    assert observation.steps[-1].number == 1148
    assert observation.variation_preserves_identity_anchor is True
    assert observation.variation_is_not_identical_repetition is True
    assert observation.variation_is_not_new_object is True
    assert observation.lifecycle_keeps_active_and_latent is True
    assert observation.compression_is_not_deletion is True
    assert bundle.generated_identity_collapse is False
    assert bundle.generated_new_object is False
    assert bundle.generated_deletion is False
    assert bundle.generated_final_form is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_variation_sequence_boundary_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_refrain_variation_lifecycle().status)
