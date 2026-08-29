"""context pressure下のselection delay境界を検査する最小実験。"""

from dataclasses import dataclass

from reintegration_context_pressure_stress_1749_1798 import (
    ContextPressureCandidate,
    ReintegrationContextPressureBundle,
    observe_reintegration_context_pressure,
)


@dataclass(frozen=True)
class ContextPressureSelectionDelayStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class SelectionDelayCandidate:
    source_pressure: ContextPressureCandidate
    delay_kind: str
    delay_reason: str
    preserves_pressure_trace: bool
    preserves_candidate_route: bool
    selects_now: bool
    treats_delay_as_failure: bool
    status: str


@dataclass(frozen=True)
class SelectionDelayPolicy:
    name: str
    permits_delay_under_pressure: bool
    preserves_strong_pressure_without_selection: bool
    preserves_medium_ambiguity: bool
    rejects_failure_collapse: bool
    generates_immediate_selection: bool
    status: str


@dataclass(frozen=True)
class ContextPressureSelectionDelayBundle:
    source_bundle: ReintegrationContextPressureBundle
    policy: SelectionDelayPolicy
    delay_candidates: tuple[SelectionDelayCandidate, ...]
    immediate_selection_candidates: tuple[SelectionDelayCandidate, ...]
    delayed_candidates: tuple[SelectionDelayCandidate, ...]
    ambiguity_delays: tuple[SelectionDelayCandidate, ...]
    stop_lines: tuple[str, ...]
    generated_immediate_selection: bool
    generated_delay_failure: bool
    generated_pressure_erasure: bool
    status: str


@dataclass(frozen=True)
class ContextPressureSelectionDelayObservation:
    source_status: str
    steps: tuple[ContextPressureSelectionDelayStep, ...]
    bundle: ContextPressureSelectionDelayBundle
    delay_candidates_cover_pressure_candidates: bool
    immediate_and_delayed_paths_preserved: bool
    ambiguity_delay_preserved: bool
    delay_not_failure_or_pressure_erasure: bool
    pressure_selection_split_preserved: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1799, "source_reentry", "reuse_1749_1798_reintegration_context_pressure", "reintegration_context_pressure_preserved"),
    (1800, "source_reentry", "next_xi_received", "context_pressure_selection_delay_stress_received"),
    (1801, "source_reentry", "pressure_candidates_recheck", "pressure_candidates_available"),
    (1802, "delay_request", "context_pressure_selection_delay_request", "context_pressure_selection_delay_candidate"),
    (1803, "delay_request", "delay_not_failure_guard", "delay_failure_non_identity_preserved"),
    (1804, "delay_request", "delay_not_pressure_erasure_guard", "pressure_erasure_non_identity_preserved"),
    (1805, "delay_request", "pressure_not_selection_guard", "pressure_selection_non_identity_preserved"),
    (1806, "policy_layer", "selection_delay_policy", "selection_delay_policy_recorded"),
    (1807, "policy_layer", "delay_under_pressure_permission", "delay_under_pressure_permission_recorded"),
    (1808, "policy_layer", "strong_pressure_without_selection_rule", "strong_pressure_without_selection_recorded"),
    (1809, "policy_layer", "medium_ambiguity_preservation_rule", "medium_ambiguity_preservation_recorded"),
    (1810, "policy_layer", "failure_collapse_rejection_rule", "failure_collapse_rejection_recorded"),
    (1811, "delay_layer", "weak_pressure_immediate_candidate", "weak_pressure_immediate_candidate_recorded"),
    (1812, "delay_layer", "medium_pressure_ambiguity_delay_candidate", "medium_pressure_ambiguity_delay_recorded"),
    (1813, "delay_layer", "strong_pressure_selection_delay_candidate", "strong_pressure_selection_delay_recorded"),
    (1814, "delay_layer", "pressure_trace_carry", "pressure_trace_carried"),
    (1815, "delay_layer", "candidate_route_carry", "candidate_route_carried"),
    (1816, "delay_layer", "selects_now_false_record_for_delays", "selects_now_false_recorded_for_delays"),
    (1817, "delay_layer", "delay_failure_false_record", "delay_failure_false_recorded"),
    (1818, "partition_layer", "immediate_selection_partition", "immediate_selection_partition_recorded"),
    (1819, "partition_layer", "delayed_candidate_partition", "delayed_candidate_partition_recorded"),
    (1820, "partition_layer", "ambiguity_delay_partition", "ambiguity_delay_partition_recorded"),
    (1821, "partition_layer", "partition_not_final_decision_guard", "partition_final_decision_non_identity"),
    (1822, "partition_layer", "delay_not_rejection_guard", "delay_rejection_non_identity"),
    (1823, "delay_view", "selection_delay_view", "selection_delay_view_created"),
    (1824, "delay_view", "pressure_trace_view", "pressure_trace_view_created"),
    (1825, "delay_view", "delayed_route_view", "delayed_route_view_created"),
    (1826, "delay_view", "ambiguity_delay_view", "ambiguity_delay_view_created"),
    (1827, "bundle", "context_pressure_selection_delay_bundle_creation", "context_pressure_selection_delay_bundle_created"),
    (1828, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1829, "bundle", "stop_lines_carry", "context_pressure_selection_delay_stop_lines_carried"),
    (1830, "bundle", "generated_immediate_selection_false", "generated_immediate_selection_false_recorded"),
    (1831, "bundle", "generated_delay_failure_false", "generated_delay_failure_false_recorded"),
    (1832, "bundle", "generated_pressure_erasure_false", "generated_pressure_erasure_false_recorded"),
    (1833, "integrity", "delay_candidates_cover_pressure_candidates_check", "delay_candidates_cover_pressure_candidates_confirmed"),
    (1834, "integrity", "immediate_delayed_paths_check", "immediate_delayed_paths_confirmed"),
    (1835, "integrity", "ambiguity_delay_preservation_check", "ambiguity_delay_preservation_confirmed"),
    (1836, "integrity", "delay_not_failure_erasure_check", "delay_not_failure_erasure_confirmed"),
    (1837, "integrity", "pressure_selection_split_check", "pressure_selection_split_confirmed"),
    (1838, "non_identity", "delay_vs_failure_split", "delay_failure_non_identity"),
    (1839, "non_identity", "pressure_vs_selection_split", "pressure_selection_non_identity"),
    (1840, "non_identity", "strong_pressure_vs_immediate_selection_split", "strong_pressure_immediate_selection_non_identity"),
    (1841, "non_identity", "delay_vs_rejection_split", "delay_rejection_non_identity"),
    (1842, "music_subject", "delay_as_hearing_maturation", "hearing_maturation_preserved"),
    (1843, "music_subject", "medium_delay_as_suspended_reading", "medium_delay_suspended_reading_preserved"),
    (1844, "music_subject", "strong_delay_as_unresolved_pull", "strong_delay_unresolved_pull_preserved"),
    (1845, "summary", "context_pressure_selection_delay_summary", "context_pressure_selection_delay_observed"),
    (1846, "summary", "delay_without_failure_or_selection_summary", "delay_without_failure_or_selection_confirmed"),
    (1847, "next_plan", "delayed_selection_reactivation_next_candidate", "delayed_selection_reactivation_next_candidate"),
    (1848, "next_plan", "next_xi_selection", "xi_delayed_selection_reactivation_stress"),
)


def _build_steps() -> tuple[ContextPressureSelectionDelayStep, ...]:
    previous = "reintegration_context_pressure_1749_1798"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            ContextPressureSelectionDelayStep(
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


def _delay_candidate(pressure: ContextPressureCandidate) -> SelectionDelayCandidate:
    if pressure.pressure_level == "weak":
        kind = "weak_pressure_immediate_selection_candidate"
        reason = "already_stable_contextual_continuity"
        selects_now = True
    elif pressure.pressure_level == "medium":
        kind = "medium_pressure_ambiguity_delay_candidate"
        reason = "ambiguous_hearing_requires_later_context"
        selects_now = False
    else:
        kind = "strong_pressure_selection_delay_candidate"
        reason = "strong_pull_preserved_until_route_matures"
        selects_now = False

    return SelectionDelayCandidate(
        source_pressure=pressure,
        delay_kind=kind,
        delay_reason=reason,
        preserves_pressure_trace=True,
        preserves_candidate_route=pressure.preserves_candidate_trace,
        selects_now=selects_now,
        treats_delay_as_failure=False,
        status="context_pressure_selection_delay_candidate_recorded_without_failure",
    )


def build_context_pressure_selection_delay_bundle(
    source: ReintegrationContextPressureBundle,
) -> ContextPressureSelectionDelayBundle:
    policy = SelectionDelayPolicy(
        name="context_pressure_selection_delay_policy",
        permits_delay_under_pressure=True,
        preserves_strong_pressure_without_selection=True,
        preserves_medium_ambiguity=True,
        rejects_failure_collapse=True,
        generates_immediate_selection=False,
        status="selection_delay_policy_preserves_pressure_without_forced_choice",
    )
    candidates = tuple(
        _delay_candidate(pressure)
        for pressure in source.pressure_candidates
    )
    immediate = tuple(candidate for candidate in candidates if candidate.selects_now)
    delayed = tuple(candidate for candidate in candidates if not candidate.selects_now)
    ambiguity = tuple(candidate for candidate in delayed if "ambiguity" in candidate.delay_kind)
    return ContextPressureSelectionDelayBundle(
        source_bundle=source,
        policy=policy,
        delay_candidates=candidates,
        immediate_selection_candidates=immediate,
        delayed_candidates=delayed,
        ambiguity_delays=ambiguity,
        stop_lines=(
            "delay_not_failure",
            "delay_not_pressure_erasure",
            "pressure_not_selection",
            "strong_pressure_not_immediate_selection",
            "delay_not_rejection",
        ),
        generated_immediate_selection=False,
        generated_delay_failure=False,
        generated_pressure_erasure=False,
        status="context_pressure_selection_delay_bundle_1799_1848_built_without_forced_selection",
    )


def observe_context_pressure_selection_delay() -> ContextPressureSelectionDelayObservation:
    source = observe_reintegration_context_pressure()
    bundle = build_context_pressure_selection_delay_bundle(source.bundle)
    steps = _build_steps()

    return ContextPressureSelectionDelayObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        delay_candidates_cover_pressure_candidates=(
            len(bundle.delay_candidates) == len(source.bundle.pressure_candidates)
        ),
        immediate_and_delayed_paths_preserved=(
            len(bundle.immediate_selection_candidates) == 1
            and len(bundle.delayed_candidates) == 2
        ),
        ambiguity_delay_preserved=(
            len(bundle.ambiguity_delays) == 1
            and bundle.policy.preserves_medium_ambiguity is True
        ),
        delay_not_failure_or_pressure_erasure=(
            bundle.generated_delay_failure is False
            and bundle.generated_pressure_erasure is False
            and all(not candidate.treats_delay_as_failure for candidate in bundle.delay_candidates)
        ),
        pressure_selection_split_preserved=(
            bundle.policy.permits_delay_under_pressure is True
            and bundle.policy.preserves_strong_pressure_without_selection is True
            and bundle.generated_immediate_selection is False
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="context_pressure_selection_delay_1799_1848_observed_without_failure_or_forced_selection",
    )


def run_checks() -> None:
    observation = observe_context_pressure_selection_delay()
    bundle = observation.bundle

    assert observation.source_status == (
        "reintegration_context_pressure_1749_1798_observed_without_forced_merge_or_context_truth"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1799
    assert observation.steps[-1].number == 1848
    assert observation.delay_candidates_cover_pressure_candidates is True
    assert observation.immediate_and_delayed_paths_preserved is True
    assert observation.ambiguity_delay_preserved is True
    assert observation.delay_not_failure_or_pressure_erasure is True
    assert observation.pressure_selection_split_preserved is True
    assert len(bundle.delay_candidates) == 3
    assert len(bundle.immediate_selection_candidates) == 1
    assert len(bundle.delayed_candidates) == 2
    assert len(bundle.ambiguity_delays) == 1
    assert bundle.generated_immediate_selection is False
    assert bundle.generated_delay_failure is False
    assert bundle.generated_pressure_erasure is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_delayed_selection_reactivation_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_context_pressure_selection_delay().status)
