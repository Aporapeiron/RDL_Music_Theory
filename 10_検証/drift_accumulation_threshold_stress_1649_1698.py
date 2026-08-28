"""memory drift蓄積のthreshold境界を検査する最小実験。"""

from dataclasses import dataclass

from iterated_reentry_memory_drift_stress_1599_1648 import (
    IteratedReentryMemoryDriftBundle,
    MemoryDriftCandidate,
    observe_iterated_reentry_memory_drift,
)


@dataclass(frozen=True)
class DriftAccumulationThresholdStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class DriftThresholdCandidate:
    source_drift: MemoryDriftCandidate
    accumulation_level: int
    threshold_zone: str
    handling_kind: str
    keeps_identity_anchor: bool
    preserves_origin_trace: bool
    splits_to_new_candidate: bool
    treats_threshold_as_truth: bool
    status: str


@dataclass(frozen=True)
class DriftThresholdPolicy:
    name: str
    soft_threshold: int
    split_threshold: int
    permits_below_threshold_drift: bool
    preserves_boundary_ambiguity: bool
    treats_threshold_as_final_truth: bool
    generates_forced_selection: bool
    status: str


@dataclass(frozen=True)
class DriftAccumulationThresholdBundle:
    source_bundle: IteratedReentryMemoryDriftBundle
    policy: DriftThresholdPolicy
    threshold_candidates: tuple[DriftThresholdCandidate, ...]
    retained_identity_drifts: tuple[DriftThresholdCandidate, ...]
    split_candidate_drifts: tuple[DriftThresholdCandidate, ...]
    boundary_zone_drifts: tuple[DriftThresholdCandidate, ...]
    stop_lines: tuple[str, ...]
    generated_forced_selection: bool
    generated_final_truth: bool
    generated_origin_deletion: bool
    status: str


@dataclass(frozen=True)
class DriftAccumulationThresholdObservation:
    source_status: str
    steps: tuple[DriftAccumulationThresholdStep, ...]
    bundle: DriftAccumulationThresholdBundle
    threshold_candidates_cover_source_drifts: bool
    retained_and_split_paths_preserved: bool
    boundary_zone_preserved: bool
    threshold_not_truth_or_forced_selection: bool
    origin_trace_preserved_across_split: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1649, "source_reentry", "reuse_1599_1648_iterated_reentry_memory_drift", "iterated_reentry_memory_drift_preserved"),
    (1650, "source_reentry", "next_xi_received", "drift_accumulation_threshold_stress_received"),
    (1651, "source_reentry", "drift_candidates_recheck", "drift_candidates_available"),
    (1652, "threshold_request", "drift_accumulation_threshold_request", "drift_accumulation_threshold_candidate"),
    (1653, "threshold_request", "threshold_not_truth_guard", "threshold_truth_non_identity_preserved"),
    (1654, "threshold_request", "threshold_not_forced_selection_guard", "forced_selection_blocked"),
    (1655, "threshold_request", "threshold_not_origin_deletion_guard", "origin_deletion_non_identity_preserved"),
    (1656, "policy_layer", "drift_threshold_policy", "drift_threshold_policy_recorded"),
    (1657, "policy_layer", "soft_threshold_rule", "soft_threshold_rule_recorded"),
    (1658, "policy_layer", "split_threshold_rule", "split_threshold_rule_recorded"),
    (1659, "policy_layer", "boundary_ambiguity_preservation_rule", "boundary_ambiguity_preservation_recorded"),
    (1660, "policy_layer", "forced_selection_false_rule", "forced_selection_false_recorded"),
    (1661, "threshold_layer", "primary_returned_below_threshold", "primary_returned_below_threshold_recorded"),
    (1662, "threshold_layer", "derivative_returned_boundary_zone", "derivative_returned_boundary_zone_recorded"),
    (1663, "threshold_layer", "latent_redeferred_split_zone", "latent_redeferred_split_zone_recorded"),
    (1664, "threshold_layer", "identity_anchor_carry", "identity_anchor_carried"),
    (1665, "threshold_layer", "origin_trace_carry", "origin_trace_carried"),
    (1666, "threshold_layer", "truth_false_record", "truth_false_recorded"),
    (1667, "threshold_layer", "forced_selection_false_record", "forced_selection_false_recorded"),
    (1668, "partition_layer", "retained_identity_drift_partition", "retained_identity_drift_partition_recorded"),
    (1669, "partition_layer", "split_candidate_drift_partition", "split_candidate_drift_partition_recorded"),
    (1670, "partition_layer", "boundary_zone_drift_partition", "boundary_zone_drift_partition_recorded"),
    (1671, "partition_layer", "partition_not_deletion_guard", "partition_deletion_non_identity"),
    (1672, "partition_layer", "split_not_rejection_guard", "split_rejection_non_identity"),
    (1673, "threshold_view", "accumulation_threshold_view", "accumulation_threshold_view_created"),
    (1674, "threshold_view", "identity_retention_view", "identity_retention_view_created"),
    (1675, "threshold_view", "candidate_split_view", "candidate_split_view_created"),
    (1676, "threshold_view", "boundary_ambiguity_view", "boundary_ambiguity_view_created"),
    (1677, "bundle", "drift_accumulation_threshold_bundle_creation", "drift_accumulation_threshold_bundle_created"),
    (1678, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1679, "bundle", "stop_lines_carry", "drift_accumulation_threshold_stop_lines_carried"),
    (1680, "bundle", "generated_forced_selection_false", "generated_forced_selection_false_recorded"),
    (1681, "bundle", "generated_final_truth_false", "generated_final_truth_false_recorded"),
    (1682, "bundle", "generated_origin_deletion_false", "generated_origin_deletion_false_recorded"),
    (1683, "integrity", "threshold_candidates_cover_source_drifts_check", "threshold_candidates_cover_source_drifts_confirmed"),
    (1684, "integrity", "retained_split_paths_check", "retained_split_paths_confirmed"),
    (1685, "integrity", "boundary_zone_preservation_check", "boundary_zone_preservation_confirmed"),
    (1686, "integrity", "threshold_not_truth_selection_check", "threshold_not_truth_selection_confirmed"),
    (1687, "integrity", "origin_trace_across_split_check", "origin_trace_across_split_confirmed"),
    (1688, "non_identity", "threshold_vs_truth_split", "threshold_truth_non_identity"),
    (1689, "non_identity", "split_vs_rejection_split", "split_rejection_non_identity"),
    (1690, "non_identity", "boundary_zone_vs_decision_split", "boundary_zone_decision_non_identity"),
    (1691, "non_identity", "accumulation_vs_reset_split", "accumulation_reset_non_identity"),
    (1692, "music_subject", "threshold_as_recognition_pressure", "threshold_recognition_pressure_preserved"),
    (1693, "music_subject", "below_threshold_as_same_memory_variation", "below_threshold_same_memory_variation_preserved"),
    (1694, "music_subject", "split_zone_as_new_musical_candidate", "split_zone_new_musical_candidate_preserved"),
    (1695, "summary", "drift_accumulation_threshold_summary", "drift_accumulation_threshold_observed"),
    (1696, "summary", "threshold_without_truth_or_forced_selection_summary", "threshold_without_truth_or_forced_selection_confirmed"),
    (1697, "next_plan", "split_candidate_reintegration_next_candidate", "split_candidate_reintegration_next_candidate"),
    (1698, "next_plan", "next_xi_selection", "xi_split_candidate_reintegration_stress"),
)


def _build_steps() -> tuple[DriftAccumulationThresholdStep, ...]:
    previous = "iterated_reentry_memory_drift_1599_1648"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            DriftAccumulationThresholdStep(
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


def _threshold_candidate(
    drift: MemoryDriftCandidate,
    index: int,
) -> DriftThresholdCandidate:
    levels = (1, 2, 3)
    level = levels[index]
    if level == 1:
        zone = "below_soft_threshold"
        handling = "same_memory_variation"
        split = False
    elif level == 2:
        zone = "boundary_ambiguity_zone"
        handling = "ambiguous_identity_drift"
        split = False
    else:
        zone = "split_threshold_zone"
        handling = "new_candidate_with_origin_trace"
        split = True

    return DriftThresholdCandidate(
        source_drift=drift,
        accumulation_level=level,
        threshold_zone=zone,
        handling_kind=handling,
        keeps_identity_anchor=level < 3,
        preserves_origin_trace=drift.preserves_origin_trace,
        splits_to_new_candidate=split,
        treats_threshold_as_truth=False,
        status="drift_threshold_candidate_recorded_without_truth_or_forced_selection",
    )


def build_drift_accumulation_threshold_bundle(
    source: IteratedReentryMemoryDriftBundle,
) -> DriftAccumulationThresholdBundle:
    policy = DriftThresholdPolicy(
        name="drift_accumulation_threshold_policy",
        soft_threshold=2,
        split_threshold=3,
        permits_below_threshold_drift=True,
        preserves_boundary_ambiguity=True,
        treats_threshold_as_final_truth=False,
        generates_forced_selection=False,
        status="drift_threshold_policy_preserves_ambiguous_boundary_without_truth",
    )
    candidates = tuple(
        _threshold_candidate(drift, index)
        for index, drift in enumerate(source.drift_candidates)
    )
    retained = tuple(candidate for candidate in candidates if not candidate.splits_to_new_candidate)
    split = tuple(candidate for candidate in candidates if candidate.splits_to_new_candidate)
    boundary = tuple(
        candidate for candidate in candidates if candidate.threshold_zone == "boundary_ambiguity_zone"
    )
    return DriftAccumulationThresholdBundle(
        source_bundle=source,
        policy=policy,
        threshold_candidates=candidates,
        retained_identity_drifts=retained,
        split_candidate_drifts=split,
        boundary_zone_drifts=boundary,
        stop_lines=(
            "threshold_not_truth",
            "threshold_not_forced_selection",
            "threshold_not_origin_deletion",
            "split_not_rejection",
            "boundary_zone_not_decision",
        ),
        generated_forced_selection=False,
        generated_final_truth=False,
        generated_origin_deletion=False,
        status="drift_accumulation_threshold_bundle_1649_1698_built_without_truth_or_forced_selection",
    )


def observe_drift_accumulation_threshold() -> DriftAccumulationThresholdObservation:
    source = observe_iterated_reentry_memory_drift()
    bundle = build_drift_accumulation_threshold_bundle(source.bundle)
    steps = _build_steps()

    return DriftAccumulationThresholdObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        threshold_candidates_cover_source_drifts=(
            len(bundle.threshold_candidates) == len(source.bundle.drift_candidates)
        ),
        retained_and_split_paths_preserved=(
            len(bundle.retained_identity_drifts) == 2
            and len(bundle.split_candidate_drifts) == 1
        ),
        boundary_zone_preserved=(
            len(bundle.boundary_zone_drifts) == 1
            and bundle.policy.preserves_boundary_ambiguity is True
        ),
        threshold_not_truth_or_forced_selection=(
            bundle.policy.treats_threshold_as_final_truth is False
            and bundle.policy.generates_forced_selection is False
            and bundle.generated_final_truth is False
            and bundle.generated_forced_selection is False
            and all(not candidate.treats_threshold_as_truth for candidate in bundle.threshold_candidates)
        ),
        origin_trace_preserved_across_split=(
            bundle.generated_origin_deletion is False
            and all(candidate.preserves_origin_trace for candidate in bundle.threshold_candidates)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="drift_accumulation_threshold_1649_1698_observed_without_truth_or_forced_selection",
    )


def run_checks() -> None:
    observation = observe_drift_accumulation_threshold()
    bundle = observation.bundle

    assert observation.source_status == (
        "iterated_reentry_memory_drift_1599_1648_observed_without_error_or_identity_collapse"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1649
    assert observation.steps[-1].number == 1698
    assert observation.threshold_candidates_cover_source_drifts is True
    assert observation.retained_and_split_paths_preserved is True
    assert observation.boundary_zone_preserved is True
    assert observation.threshold_not_truth_or_forced_selection is True
    assert observation.origin_trace_preserved_across_split is True
    assert len(bundle.threshold_candidates) == 3
    assert len(bundle.retained_identity_drifts) == 2
    assert len(bundle.split_candidate_drifts) == 1
    assert len(bundle.boundary_zone_drifts) == 1
    assert bundle.generated_forced_selection is False
    assert bundle.generated_final_truth is False
    assert bundle.generated_origin_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_split_candidate_reintegration_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_drift_accumulation_threshold().status)
