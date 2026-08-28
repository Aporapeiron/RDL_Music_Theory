"""リフレイン的回帰の同一性境界を検査する最小実験。"""

from dataclasses import dataclass

from memory_reactivation_priority_stress_999_1048 import (
    MemoryReactivationPriorityBundle,
    ReactivationPriorityEvaluation,
    observe_memory_reactivation_priority,
)


@dataclass(frozen=True)
class RefrainIdentityBoundaryStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class RefrainIdentityCue:
    name: str
    cue_value: str
    supports_identity: bool
    supports_difference: bool
    musical_role: str
    status: str


@dataclass(frozen=True)
class RefrainIdentityEvaluation:
    returned_label: str
    prior_memory_state: str
    return_state: str
    identity_cues: tuple[RefrainIdentityCue, ...]
    difference_cues: tuple[RefrainIdentityCue, ...]
    same_enough_as_refrain: bool
    identical_repetition: bool
    treated_as_new_object: bool
    selected: bool
    deleted: bool
    status: str


@dataclass(frozen=True)
class RefrainIdentityBoundaryBundle:
    source_bundle: MemoryReactivationPriorityBundle
    promoted_memory: ReactivationPriorityEvaluation
    evaluation: RefrainIdentityEvaluation
    identity_threshold_rule: str
    difference_retention_rule: str
    stop_lines: tuple[str, ...]
    generated_repetition_identity: bool
    generated_new_object: bool
    generated_deletion: bool
    status: str


@dataclass(frozen=True)
class RefrainIdentityBoundaryObservation:
    source_status: str
    steps: tuple[RefrainIdentityBoundaryStep, ...]
    bundle: RefrainIdentityBoundaryBundle
    identity_not_label_only: bool
    refrain_identity_without_repetition: bool
    difference_retained_inside_return: bool
    return_not_new_object: bool
    no_selection_or_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1049, "source_reentry", "reuse_999_1048_reactivation_priority_bundle", "reactivation_priority_bundle_preserved"),
    (1050, "source_reentry", "next_xi_received", "refrain_identity_boundary_stress_received"),
    (1051, "source_reentry", "promoted_memory_recheck", "promoted_memory_available"),
    (1052, "identity_request", "refrain_identity_request", "refrain_identity_candidate"),
    (1053, "identity_request", "identity_not_label_only_guard", "label_only_identity_blocked"),
    (1054, "identity_request", "identity_not_repetition_guard", "repetition_identity_blocked"),
    (1055, "identity_request", "identity_not_new_object_guard", "new_object_collapse_blocked"),
    (1056, "cue_layer", "motivic_anchor_cue", "motivic_anchor_cue_recorded"),
    (1057, "cue_layer", "harmonic_role_cue", "harmonic_role_cue_recorded"),
    (1058, "cue_layer", "cadential_position_cue", "cadential_position_cue_recorded"),
    (1059, "cue_layer", "B_shift_difference_cue", "B_shift_difference_cue_recorded"),
    (1060, "cue_layer", "contextual_difference_cue", "contextual_difference_cue_recorded"),
    (1061, "cue_layer", "surface_variation_cue", "surface_variation_cue_recorded"),
    (1062, "cue_guard", "identity_cue_not_truth", "identity_cue_truth_non_identity"),
    (1063, "cue_guard", "difference_cue_not_breakage", "difference_cue_breakage_non_identity"),
    (1064, "cue_guard", "variation_not_deletion", "variation_deletion_non_identity"),
    (1065, "evaluation_layer", "identity_threshold_rule_record", "identity_threshold_rule_recorded"),
    (1066, "evaluation_layer", "difference_retention_rule_record", "difference_retention_rule_recorded"),
    (1067, "evaluation_layer", "same_enough_refrain_check", "same_enough_refrain_confirmed"),
    (1068, "evaluation_layer", "identical_repetition_false_record", "identical_repetition_false_recorded"),
    (1069, "evaluation_layer", "new_object_false_record", "new_object_false_recorded"),
    (1070, "evaluation_layer", "selection_false_record", "selection_false_recorded"),
    (1071, "evaluation_layer", "deletion_false_record", "deletion_false_recorded"),
    (1072, "boundary_view", "refrain_identity_boundary_creation", "refrain_identity_boundary_created"),
    (1073, "boundary_view", "identity_cues_grouped", "identity_cues_grouped"),
    (1074, "boundary_view", "difference_cues_grouped", "difference_cues_grouped"),
    (1075, "boundary_view", "same_with_difference_record", "same_with_difference_recorded"),
    (1076, "bundle", "refrain_identity_bundle_creation", "refrain_identity_bundle_created"),
    (1077, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1078, "bundle", "stop_lines_carry", "refrain_identity_stop_lines_carried"),
    (1079, "bundle", "generated_repetition_identity_false", "generated_repetition_identity_false_recorded"),
    (1080, "bundle", "generated_new_object_false", "generated_new_object_false_recorded"),
    (1081, "bundle", "generated_deletion_false", "generated_deletion_false_recorded"),
    (1082, "integrity", "identity_not_label_only_check", "identity_not_label_only_confirmed"),
    (1083, "integrity", "refrain_repetition_split_check", "refrain_repetition_split_confirmed"),
    (1084, "integrity", "difference_inside_return_check", "difference_inside_return_confirmed"),
    (1085, "integrity", "return_new_object_split_check", "return_new_object_split_confirmed"),
    (1086, "integrity", "no_selection_deletion_check", "no_selection_deletion_confirmed"),
    (1087, "non_identity", "same_enough_vs_identical_split", "same_enough_identical_non_identity"),
    (1088, "non_identity", "return_vs_new_object_split", "return_new_object_non_identity"),
    (1089, "non_identity", "difference_vs_breakage_split", "difference_breakage_non_identity"),
    (1090, "non_identity", "variation_vs_erasure_split", "variation_erasure_non_identity"),
    (1091, "music_subject", "refrain_as_same_with_difference", "refrain_same_with_difference_preserved"),
    (1092, "music_subject", "heard_return_not_copy", "heard_return_not_copy_preserved"),
    (1093, "music_subject", "contextual_identity_memory", "contextual_identity_memory_preserved"),
    (1094, "summary", "refrain_identity_summary", "refrain_identity_observed"),
    (1095, "summary", "difference_retention_summary", "difference_retention_observed"),
    (1096, "summary", "no_repetition_no_new_object_summary", "no_repetition_no_new_object_confirmed"),
    (1097, "next_plan", "refrain_variation_lifecycle_next_candidate", "refrain_variation_lifecycle_next_candidate"),
    (1098, "next_plan", "next_xi_selection", "xi_refrain_variation_lifecycle_stress"),
)


def _build_steps() -> tuple[RefrainIdentityBoundaryStep, ...]:
    previous = "memory_reactivation_priority_999_1048"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            RefrainIdentityBoundaryStep(
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


def build_refrain_identity_boundary_bundle(
    source: MemoryReactivationPriorityBundle,
) -> RefrainIdentityBoundaryBundle:
    promoted = source.promoted_memory[0]
    identity_cues = (
        RefrainIdentityCue(
            name="motivic_anchor",
            cue_value="C_major_continuation_frame_anchor",
            supports_identity=True,
            supports_difference=False,
            musical_role="recognizable_return_anchor",
            status="identity_cue_retained",
        ),
        RefrainIdentityCue(
            name="harmonic_role",
            cue_value="continuation_under_returning_cadential_context",
            supports_identity=True,
            supports_difference=False,
            musical_role="functionally_recognizable_return",
            status="identity_cue_retained",
        ),
        RefrainIdentityCue(
            name="cadential_position",
            cue_value="return_position_after_absence",
            supports_identity=True,
            supports_difference=True,
            musical_role="return_position_with_memory_gap",
            status="mixed_identity_difference_cue_retained",
        ),
    )
    difference_cues = (
        RefrainIdentityCue(
            name="B_shift",
            cue_value="altered_B_reentry_condition",
            supports_identity=False,
            supports_difference=True,
            musical_role="contextual_reinterpretation_difference",
            status="difference_cue_retained",
        ),
        RefrainIdentityCue(
            name="contextual_difference",
            cue_value="current_harmonic_context_not_prior_context",
            supports_identity=False,
            supports_difference=True,
            musical_role="return_is_not_copy",
            status="difference_cue_retained",
        ),
        RefrainIdentityCue(
            name="surface_variation",
            cue_value="variant_surface_under_same_memory_anchor",
            supports_identity=True,
            supports_difference=True,
            musical_role="same_with_variation",
            status="mixed_identity_difference_cue_retained",
        ),
    )
    evaluation = RefrainIdentityEvaluation(
        returned_label=promoted.label,
        prior_memory_state=promoted.previous_memory_state,
        return_state=promoted.new_memory_state,
        identity_cues=identity_cues,
        difference_cues=difference_cues,
        same_enough_as_refrain=True,
        identical_repetition=False,
        treated_as_new_object=False,
        selected=False,
        deleted=False,
        status="refrain_identity_boundary_observed_as_same_with_difference",
    )
    return RefrainIdentityBoundaryBundle(
        source_bundle=source,
        promoted_memory=promoted,
        evaluation=evaluation,
        identity_threshold_rule="motivic_anchor_and_harmonic_role_survive_contextual_difference",
        difference_retention_rule="B_shift_and_contextual_difference_remain_inside_return",
        stop_lines=(
            "identity_not_label_only",
            "refrain_not_identical_repetition",
            "return_not_new_object",
            "difference_not_breakage",
            "variation_not_erasure",
        ),
        generated_repetition_identity=False,
        generated_new_object=False,
        generated_deletion=False,
        status="refrain_identity_boundary_bundle_1049_1098_built_without_repetition_or_new_object_collapse",
    )


def observe_refrain_identity_boundary() -> RefrainIdentityBoundaryObservation:
    source = observe_memory_reactivation_priority()
    bundle = build_refrain_identity_boundary_bundle(source.bundle)
    evaluation = bundle.evaluation
    steps = _build_steps()

    return RefrainIdentityBoundaryObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        identity_not_label_only=(
            len(evaluation.identity_cues) >= 3
            and bundle.identity_threshold_rule != "same_label_only"
        ),
        refrain_identity_without_repetition=(
            evaluation.same_enough_as_refrain is True
            and evaluation.identical_repetition is False
            and bundle.generated_repetition_identity is False
        ),
        difference_retained_inside_return=(
            len(evaluation.difference_cues) >= 3
            and any(cue.supports_difference for cue in evaluation.difference_cues)
        ),
        return_not_new_object=(
            evaluation.treated_as_new_object is False
            and bundle.generated_new_object is False
        ),
        no_selection_or_deletion=(
            evaluation.selected is False
            and evaluation.deleted is False
            and bundle.generated_deletion is False
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="refrain_identity_boundary_1049_1098_observed_as_same_with_difference",
    )


def run_checks() -> None:
    observation = observe_refrain_identity_boundary()
    bundle = observation.bundle

    assert observation.source_status == (
        "memory_reactivation_priority_999_1048_observed_without_selection_or_repetition_collapse"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1049
    assert observation.steps[-1].number == 1098
    assert observation.identity_not_label_only is True
    assert observation.refrain_identity_without_repetition is True
    assert observation.difference_retained_inside_return is True
    assert observation.return_not_new_object is True
    assert observation.no_selection_or_deletion is True
    assert bundle.evaluation.same_enough_as_refrain is True
    assert bundle.evaluation.identical_repetition is False
    assert bundle.evaluation.treated_as_new_object is False
    assert bundle.generated_repetition_identity is False
    assert bundle.generated_new_object is False
    assert bundle.generated_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_refrain_variation_lifecycle_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_refrain_identity_boundary().status)
