"""split candidateのreintegration境界を検査する最小実験。"""

from dataclasses import dataclass

from drift_accumulation_threshold_stress_1649_1698 import (
    DriftAccumulationThresholdBundle,
    DriftThresholdCandidate,
    observe_drift_accumulation_threshold,
)


@dataclass(frozen=True)
class SplitCandidateReintegrationStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ReintegrationCandidate:
    source_threshold: DriftThresholdCandidate
    reintegration_kind: str
    context_relation: str
    preserves_split_trace: bool
    preserves_origin_trace: bool
    reintegrates_now: bool
    remains_independent: bool
    forces_unification: bool
    status: str


@dataclass(frozen=True)
class SplitReintegrationPolicy:
    name: str
    accepts_split_candidate: bool
    permits_contextual_reintegration: bool
    permits_independent_retention: bool
    preserves_boundary_ambiguity: bool
    generates_forced_unification: bool
    status: str


@dataclass(frozen=True)
class SplitCandidateReintegrationBundle:
    source_bundle: DriftAccumulationThresholdBundle
    policy: SplitReintegrationPolicy
    reintegration_candidates: tuple[ReintegrationCandidate, ...]
    contextual_reintegrations: tuple[ReintegrationCandidate, ...]
    independent_retentions: tuple[ReintegrationCandidate, ...]
    ambiguous_reintegrations: tuple[ReintegrationCandidate, ...]
    stop_lines: tuple[str, ...]
    generated_forced_unification: bool
    generated_split_rejection: bool
    generated_origin_deletion: bool
    status: str


@dataclass(frozen=True)
class SplitCandidateReintegrationObservation:
    source_status: str
    steps: tuple[SplitCandidateReintegrationStep, ...]
    bundle: SplitCandidateReintegrationBundle
    split_and_retained_candidates_carried: bool
    contextual_and_independent_paths_preserved: bool
    split_trace_preserved: bool
    reintegration_not_forced_unification: bool
    no_split_rejection_or_origin_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1699, "source_reentry", "reuse_1649_1698_drift_accumulation_threshold", "drift_accumulation_threshold_preserved"),
    (1700, "source_reentry", "next_xi_received", "split_candidate_reintegration_stress_received"),
    (1701, "source_reentry", "threshold_candidates_recheck", "threshold_candidates_available"),
    (1702, "reintegration_request", "split_candidate_reintegration_request", "split_candidate_reintegration_candidate"),
    (1703, "reintegration_request", "reintegration_not_rejection_guard", "split_rejection_non_identity_preserved"),
    (1704, "reintegration_request", "reintegration_not_forced_unification_guard", "forced_unification_blocked"),
    (1705, "reintegration_request", "reintegration_not_origin_deletion_guard", "origin_deletion_non_identity_preserved"),
    (1706, "policy_layer", "split_reintegration_policy", "split_reintegration_policy_recorded"),
    (1707, "policy_layer", "split_candidate_acceptance_rule", "split_candidate_acceptance_recorded"),
    (1708, "policy_layer", "contextual_reintegration_permission", "contextual_reintegration_permission_recorded"),
    (1709, "policy_layer", "independent_retention_permission", "independent_retention_permission_recorded"),
    (1710, "policy_layer", "boundary_ambiguity_preservation_rule", "boundary_ambiguity_preservation_recorded"),
    (1711, "candidate_layer", "below_threshold_reintegration_candidate", "below_threshold_reintegration_candidate_recorded"),
    (1712, "candidate_layer", "boundary_zone_reintegration_candidate", "boundary_zone_reintegration_candidate_recorded"),
    (1713, "candidate_layer", "split_zone_reintegration_candidate", "split_zone_reintegration_candidate_recorded"),
    (1714, "candidate_layer", "split_trace_carry", "split_trace_carried"),
    (1715, "candidate_layer", "origin_trace_carry", "origin_trace_carried"),
    (1716, "candidate_layer", "forced_unification_false_record", "forced_unification_false_recorded"),
    (1717, "candidate_layer", "split_rejection_false_record", "split_rejection_false_recorded"),
    (1718, "partition_layer", "contextual_reintegration_partition", "contextual_reintegration_partition_recorded"),
    (1719, "partition_layer", "independent_retention_partition", "independent_retention_partition_recorded"),
    (1720, "partition_layer", "ambiguous_reintegration_partition", "ambiguous_reintegration_partition_recorded"),
    (1721, "partition_layer", "partition_not_final_merge_guard", "partition_final_merge_non_identity"),
    (1722, "partition_layer", "independent_retention_not_failure_guard", "independent_retention_failure_non_identity"),
    (1723, "reintegration_view", "split_candidate_reintegration_view", "split_candidate_reintegration_view_created"),
    (1724, "reintegration_view", "contextual_merge_view", "contextual_merge_view_created"),
    (1725, "reintegration_view", "independent_candidate_view", "independent_candidate_view_created"),
    (1726, "reintegration_view", "ambiguous_reintegration_view", "ambiguous_reintegration_view_created"),
    (1727, "bundle", "split_candidate_reintegration_bundle_creation", "split_candidate_reintegration_bundle_created"),
    (1728, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1729, "bundle", "stop_lines_carry", "split_candidate_reintegration_stop_lines_carried"),
    (1730, "bundle", "generated_forced_unification_false", "generated_forced_unification_false_recorded"),
    (1731, "bundle", "generated_split_rejection_false", "generated_split_rejection_false_recorded"),
    (1732, "bundle", "generated_origin_deletion_false", "generated_origin_deletion_false_recorded"),
    (1733, "integrity", "split_and_retained_candidates_carried_check", "split_and_retained_candidates_carried_confirmed"),
    (1734, "integrity", "contextual_independent_paths_check", "contextual_independent_paths_confirmed"),
    (1735, "integrity", "split_trace_preservation_check", "split_trace_preservation_confirmed"),
    (1736, "integrity", "reintegration_not_forced_unification_check", "reintegration_not_forced_unification_confirmed"),
    (1737, "integrity", "no_rejection_origin_deletion_check", "no_rejection_origin_deletion_confirmed"),
    (1738, "non_identity", "reintegration_vs_forced_unification_split", "reintegration_forced_unification_non_identity"),
    (1739, "non_identity", "split_candidate_vs_rejection_split", "split_candidate_rejection_non_identity"),
    (1740, "non_identity", "independent_retention_vs_failure_split", "independent_retention_failure_non_identity"),
    (1741, "non_identity", "contextual_merge_vs_final_merge_split", "contextual_merge_final_merge_non_identity"),
    (1742, "music_subject", "reintegration_as_later_context_recognition", "later_context_recognition_preserved"),
    (1743, "music_subject", "split_candidate_as_returnable_motif", "split_candidate_returnable_motif_preserved"),
    (1744, "music_subject", "independent_candidate_as_parallel_memory", "independent_candidate_parallel_memory_preserved"),
    (1745, "summary", "split_candidate_reintegration_summary", "split_candidate_reintegration_observed"),
    (1746, "summary", "no_forced_unification_no_rejection_summary", "no_forced_unification_no_rejection_confirmed"),
    (1747, "next_plan", "reintegration_context_pressure_next_candidate", "reintegration_context_pressure_next_candidate"),
    (1748, "next_plan", "next_xi_selection", "xi_reintegration_context_pressure_stress"),
)


def _build_steps() -> tuple[SplitCandidateReintegrationStep, ...]:
    previous = "drift_accumulation_threshold_1649_1698"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            SplitCandidateReintegrationStep(
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


def _reintegration_candidate(
    threshold: DriftThresholdCandidate,
) -> ReintegrationCandidate:
    if threshold.threshold_zone == "below_soft_threshold":
        kind = "same_memory_reintegration_candidate"
        relation = "already_within_identity_context"
        reintegrates_now = True
        remains_independent = False
    elif threshold.threshold_zone == "boundary_ambiguity_zone":
        kind = "ambiguous_reintegration_candidate"
        relation = "waits_for_later_context"
        reintegrates_now = False
        remains_independent = False
    else:
        kind = "split_candidate_reintegration_candidate"
        relation = "parallel_candidate_with_origin_trace"
        reintegrates_now = False
        remains_independent = True

    return ReintegrationCandidate(
        source_threshold=threshold,
        reintegration_kind=kind,
        context_relation=relation,
        preserves_split_trace=True,
        preserves_origin_trace=threshold.preserves_origin_trace,
        reintegrates_now=reintegrates_now,
        remains_independent=remains_independent,
        forces_unification=False,
        status="split_candidate_reintegration_recorded_without_forced_unification",
    )


def build_split_candidate_reintegration_bundle(
    source: DriftAccumulationThresholdBundle,
) -> SplitCandidateReintegrationBundle:
    policy = SplitReintegrationPolicy(
        name="split_candidate_reintegration_policy",
        accepts_split_candidate=True,
        permits_contextual_reintegration=True,
        permits_independent_retention=True,
        preserves_boundary_ambiguity=True,
        generates_forced_unification=False,
        status="split_reintegration_policy_preserves_reintegrable_difference",
    )
    candidates = tuple(
        _reintegration_candidate(threshold)
        for threshold in source.threshold_candidates
    )
    contextual = tuple(candidate for candidate in candidates if candidate.reintegrates_now)
    independent = tuple(candidate for candidate in candidates if candidate.remains_independent)
    ambiguous = tuple(
        candidate
        for candidate in candidates
        if not candidate.reintegrates_now and not candidate.remains_independent
    )
    return SplitCandidateReintegrationBundle(
        source_bundle=source,
        policy=policy,
        reintegration_candidates=candidates,
        contextual_reintegrations=contextual,
        independent_retentions=independent,
        ambiguous_reintegrations=ambiguous,
        stop_lines=(
            "reintegration_not_rejection",
            "reintegration_not_forced_unification",
            "reintegration_not_origin_deletion",
            "independent_retention_not_failure",
            "contextual_merge_not_final_merge",
        ),
        generated_forced_unification=False,
        generated_split_rejection=False,
        generated_origin_deletion=False,
        status="split_candidate_reintegration_bundle_1699_1748_built_without_forced_unification",
    )


def observe_split_candidate_reintegration() -> SplitCandidateReintegrationObservation:
    source = observe_drift_accumulation_threshold()
    bundle = build_split_candidate_reintegration_bundle(source.bundle)
    steps = _build_steps()

    return SplitCandidateReintegrationObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        split_and_retained_candidates_carried=(
            len(bundle.reintegration_candidates) == len(source.bundle.threshold_candidates)
        ),
        contextual_and_independent_paths_preserved=(
            len(bundle.contextual_reintegrations) == 1
            and len(bundle.independent_retentions) == 1
            and len(bundle.ambiguous_reintegrations) == 1
        ),
        split_trace_preserved=all(
            candidate.preserves_split_trace and candidate.preserves_origin_trace
            for candidate in bundle.reintegration_candidates
        ),
        reintegration_not_forced_unification=(
            bundle.policy.generates_forced_unification is False
            and bundle.generated_forced_unification is False
            and all(not candidate.forces_unification for candidate in bundle.reintegration_candidates)
        ),
        no_split_rejection_or_origin_deletion=(
            bundle.generated_split_rejection is False
            and bundle.generated_origin_deletion is False
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="split_candidate_reintegration_1699_1748_observed_without_forced_unification_or_rejection",
    )


def run_checks() -> None:
    observation = observe_split_candidate_reintegration()
    bundle = observation.bundle

    assert observation.source_status == (
        "drift_accumulation_threshold_1649_1698_observed_without_truth_or_forced_selection"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1699
    assert observation.steps[-1].number == 1748
    assert observation.split_and_retained_candidates_carried is True
    assert observation.contextual_and_independent_paths_preserved is True
    assert observation.split_trace_preserved is True
    assert observation.reintegration_not_forced_unification is True
    assert observation.no_split_rejection_or_origin_deletion is True
    assert len(bundle.reintegration_candidates) == 3
    assert len(bundle.contextual_reintegrations) == 1
    assert len(bundle.independent_retentions) == 1
    assert len(bundle.ambiguous_reintegrations) == 1
    assert bundle.generated_forced_unification is False
    assert bundle.generated_split_rejection is False
    assert bundle.generated_origin_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_reintegration_context_pressure_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_split_candidate_reintegration().status)
