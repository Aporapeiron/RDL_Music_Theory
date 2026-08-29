"""reintegration context pressure境界を検査する最小実験。"""

from dataclasses import dataclass

from split_candidate_reintegration_stress_1699_1748 import (
    ReintegrationCandidate,
    SplitCandidateReintegrationBundle,
    observe_split_candidate_reintegration,
)


@dataclass(frozen=True)
class ReintegrationContextPressureStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ContextPressureCandidate:
    source_candidate: ReintegrationCandidate
    pressure_level: str
    pressure_source: str
    suggested_handling: str
    preserves_candidate_trace: bool
    preserves_context_trace: bool
    forces_reintegration: bool
    deletes_independent_path: bool
    status: str


@dataclass(frozen=True)
class ContextPressurePolicy:
    name: str
    accepts_weak_pressure: bool
    accepts_medium_pressure: bool
    accepts_strong_pressure: bool
    preserves_ambiguity_under_pressure: bool
    generates_forced_reintegration: bool
    status: str


@dataclass(frozen=True)
class ReintegrationContextPressureBundle:
    source_bundle: SplitCandidateReintegrationBundle
    policy: ContextPressurePolicy
    pressure_candidates: tuple[ContextPressureCandidate, ...]
    weak_pressure_paths: tuple[ContextPressureCandidate, ...]
    medium_pressure_paths: tuple[ContextPressureCandidate, ...]
    strong_pressure_paths: tuple[ContextPressureCandidate, ...]
    stop_lines: tuple[str, ...]
    generated_forced_reintegration: bool
    generated_independent_path_deletion: bool
    generated_context_truth: bool
    status: str


@dataclass(frozen=True)
class ReintegrationContextPressureObservation:
    source_status: str
    steps: tuple[ReintegrationContextPressureStep, ...]
    bundle: ReintegrationContextPressureBundle
    pressure_candidates_cover_reintegration_candidates: bool
    pressure_levels_preserved: bool
    candidate_and_context_traces_preserved: bool
    pressure_not_forced_reintegration: bool
    no_independent_path_deletion_or_context_truth: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1749, "source_reentry", "reuse_1699_1748_split_candidate_reintegration", "split_candidate_reintegration_preserved"),
    (1750, "source_reentry", "next_xi_received", "reintegration_context_pressure_stress_received"),
    (1751, "source_reentry", "reintegration_candidates_recheck", "reintegration_candidates_available"),
    (1752, "pressure_request", "reintegration_context_pressure_request", "reintegration_context_pressure_candidate"),
    (1753, "pressure_request", "pressure_not_forced_reintegration_guard", "forced_reintegration_blocked"),
    (1754, "pressure_request", "pressure_not_context_truth_guard", "context_truth_non_identity_preserved"),
    (1755, "pressure_request", "pressure_not_independent_deletion_guard", "independent_deletion_non_identity_preserved"),
    (1756, "policy_layer", "context_pressure_policy", "context_pressure_policy_recorded"),
    (1757, "policy_layer", "weak_pressure_acceptance_rule", "weak_pressure_acceptance_recorded"),
    (1758, "policy_layer", "medium_pressure_acceptance_rule", "medium_pressure_acceptance_recorded"),
    (1759, "policy_layer", "strong_pressure_acceptance_rule", "strong_pressure_acceptance_recorded"),
    (1760, "policy_layer", "ambiguity_under_pressure_preservation_rule", "ambiguity_under_pressure_preservation_recorded"),
    (1761, "pressure_layer", "contextual_reintegration_weak_pressure", "contextual_reintegration_weak_pressure_recorded"),
    (1762, "pressure_layer", "ambiguous_reintegration_medium_pressure", "ambiguous_reintegration_medium_pressure_recorded"),
    (1763, "pressure_layer", "independent_candidate_strong_pressure", "independent_candidate_strong_pressure_recorded"),
    (1764, "pressure_layer", "candidate_trace_carry", "candidate_trace_carried"),
    (1765, "pressure_layer", "context_trace_carry", "context_trace_carried"),
    (1766, "pressure_layer", "forced_reintegration_false_record", "forced_reintegration_false_recorded"),
    (1767, "pressure_layer", "independent_deletion_false_record", "independent_deletion_false_recorded"),
    (1768, "partition_layer", "weak_pressure_partition", "weak_pressure_partition_recorded"),
    (1769, "partition_layer", "medium_pressure_partition", "medium_pressure_partition_recorded"),
    (1770, "partition_layer", "strong_pressure_partition", "strong_pressure_partition_recorded"),
    (1771, "partition_layer", "partition_not_decision_guard", "partition_decision_non_identity"),
    (1772, "partition_layer", "strong_pressure_not_forced_merge_guard", "strong_pressure_forced_merge_non_identity"),
    (1773, "pressure_view", "context_pressure_view", "context_pressure_view_created"),
    (1774, "pressure_view", "weak_context_view", "weak_context_view_created"),
    (1775, "pressure_view", "medium_ambiguity_view", "medium_ambiguity_view_created"),
    (1776, "pressure_view", "strong_parallel_path_view", "strong_parallel_path_view_created"),
    (1777, "bundle", "reintegration_context_pressure_bundle_creation", "reintegration_context_pressure_bundle_created"),
    (1778, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1779, "bundle", "stop_lines_carry", "reintegration_context_pressure_stop_lines_carried"),
    (1780, "bundle", "generated_forced_reintegration_false", "generated_forced_reintegration_false_recorded"),
    (1781, "bundle", "generated_independent_path_deletion_false", "generated_independent_path_deletion_false_recorded"),
    (1782, "bundle", "generated_context_truth_false", "generated_context_truth_false_recorded"),
    (1783, "integrity", "pressure_candidates_cover_check", "pressure_candidates_cover_confirmed"),
    (1784, "integrity", "pressure_levels_preservation_check", "pressure_levels_preservation_confirmed"),
    (1785, "integrity", "candidate_context_trace_check", "candidate_context_trace_confirmed"),
    (1786, "integrity", "pressure_not_forced_reintegration_check", "pressure_not_forced_reintegration_confirmed"),
    (1787, "integrity", "no_deletion_context_truth_check", "no_deletion_context_truth_confirmed"),
    (1788, "non_identity", "pressure_vs_decision_split", "pressure_decision_non_identity"),
    (1789, "non_identity", "strong_pressure_vs_forced_merge_split", "strong_pressure_forced_merge_non_identity"),
    (1790, "non_identity", "context_trace_vs_truth_split", "context_trace_truth_non_identity"),
    (1791, "non_identity", "independent_path_vs_deletion_split", "independent_path_deletion_non_identity"),
    (1792, "music_subject", "pressure_as_contextual_pull", "contextual_pull_preserved"),
    (1793, "music_subject", "medium_pressure_as_ambiguous_hearing", "medium_pressure_ambiguous_hearing_preserved"),
    (1794, "music_subject", "strong_pressure_as_return_invitation", "strong_pressure_return_invitation_preserved"),
    (1795, "summary", "reintegration_context_pressure_summary", "reintegration_context_pressure_observed"),
    (1796, "summary", "pressure_without_forced_merge_summary", "pressure_without_forced_merge_confirmed"),
    (1797, "next_plan", "context_pressure_selection_delay_next_candidate", "context_pressure_selection_delay_next_candidate"),
    (1798, "next_plan", "next_xi_selection", "xi_context_pressure_selection_delay_stress"),
)


def _build_steps() -> tuple[ReintegrationContextPressureStep, ...]:
    previous = "split_candidate_reintegration_1699_1748"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            ReintegrationContextPressureStep(
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


def _pressure_candidate(candidate: ReintegrationCandidate) -> ContextPressureCandidate:
    if candidate.reintegrates_now:
        level = "weak"
        source = "identity_context_continuity"
        handling = "keep_as_contextual_reintegration_candidate"
    elif candidate.remains_independent:
        level = "strong"
        source = "parallel_path_recognition_pressure"
        handling = "invite_reintegration_without_forcing_merge"
    else:
        level = "medium"
        source = "ambiguous_later_context_pressure"
        handling = "delay_selection_and_preserve_ambiguity"

    return ContextPressureCandidate(
        source_candidate=candidate,
        pressure_level=level,
        pressure_source=source,
        suggested_handling=handling,
        preserves_candidate_trace=candidate.preserves_split_trace,
        preserves_context_trace=candidate.preserves_origin_trace,
        forces_reintegration=False,
        deletes_independent_path=False,
        status="context_pressure_candidate_recorded_without_forced_reintegration",
    )


def build_reintegration_context_pressure_bundle(
    source: SplitCandidateReintegrationBundle,
) -> ReintegrationContextPressureBundle:
    policy = ContextPressurePolicy(
        name="reintegration_context_pressure_policy",
        accepts_weak_pressure=True,
        accepts_medium_pressure=True,
        accepts_strong_pressure=True,
        preserves_ambiguity_under_pressure=True,
        generates_forced_reintegration=False,
        status="context_pressure_policy_preserves_pull_without_forced_merge",
    )
    candidates = tuple(
        _pressure_candidate(candidate)
        for candidate in source.reintegration_candidates
    )
    weak = tuple(candidate for candidate in candidates if candidate.pressure_level == "weak")
    medium = tuple(candidate for candidate in candidates if candidate.pressure_level == "medium")
    strong = tuple(candidate for candidate in candidates if candidate.pressure_level == "strong")
    return ReintegrationContextPressureBundle(
        source_bundle=source,
        policy=policy,
        pressure_candidates=candidates,
        weak_pressure_paths=weak,
        medium_pressure_paths=medium,
        strong_pressure_paths=strong,
        stop_lines=(
            "pressure_not_forced_reintegration",
            "pressure_not_context_truth",
            "pressure_not_independent_deletion",
            "strong_pressure_not_forced_merge",
            "context_trace_not_truth",
        ),
        generated_forced_reintegration=False,
        generated_independent_path_deletion=False,
        generated_context_truth=False,
        status="reintegration_context_pressure_bundle_1749_1798_built_without_forced_merge",
    )


def observe_reintegration_context_pressure() -> ReintegrationContextPressureObservation:
    source = observe_split_candidate_reintegration()
    bundle = build_reintegration_context_pressure_bundle(source.bundle)
    steps = _build_steps()

    return ReintegrationContextPressureObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        pressure_candidates_cover_reintegration_candidates=(
            len(bundle.pressure_candidates) == len(source.bundle.reintegration_candidates)
        ),
        pressure_levels_preserved=(
            len(bundle.weak_pressure_paths) == 1
            and len(bundle.medium_pressure_paths) == 1
            and len(bundle.strong_pressure_paths) == 1
        ),
        candidate_and_context_traces_preserved=all(
            candidate.preserves_candidate_trace and candidate.preserves_context_trace
            for candidate in bundle.pressure_candidates
        ),
        pressure_not_forced_reintegration=(
            bundle.policy.generates_forced_reintegration is False
            and bundle.generated_forced_reintegration is False
            and all(not candidate.forces_reintegration for candidate in bundle.pressure_candidates)
        ),
        no_independent_path_deletion_or_context_truth=(
            bundle.generated_independent_path_deletion is False
            and bundle.generated_context_truth is False
            and all(not candidate.deletes_independent_path for candidate in bundle.pressure_candidates)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="reintegration_context_pressure_1749_1798_observed_without_forced_merge_or_context_truth",
    )


def run_checks() -> None:
    observation = observe_reintegration_context_pressure()
    bundle = observation.bundle

    assert observation.source_status == (
        "split_candidate_reintegration_1699_1748_observed_without_forced_unification_or_rejection"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1749
    assert observation.steps[-1].number == 1798
    assert observation.pressure_candidates_cover_reintegration_candidates is True
    assert observation.pressure_levels_preserved is True
    assert observation.candidate_and_context_traces_preserved is True
    assert observation.pressure_not_forced_reintegration is True
    assert observation.no_independent_path_deletion_or_context_truth is True
    assert len(bundle.pressure_candidates) == 3
    assert len(bundle.weak_pressure_paths) == 1
    assert len(bundle.medium_pressure_paths) == 1
    assert len(bundle.strong_pressure_paths) == 1
    assert bundle.generated_forced_reintegration is False
    assert bundle.generated_independent_path_deletion is False
    assert bundle.generated_context_truth is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_context_pressure_selection_delay_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_reintegration_context_pressure().status)
