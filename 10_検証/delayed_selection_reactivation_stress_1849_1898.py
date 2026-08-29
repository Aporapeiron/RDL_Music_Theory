"""delayed selectionのreactivation境界を検査する最小実験。"""

from dataclasses import dataclass

from context_pressure_selection_delay_stress_1799_1848 import (
    ContextPressureSelectionDelayBundle,
    SelectionDelayCandidate,
    observe_context_pressure_selection_delay,
)


@dataclass(frozen=True)
class DelayedSelectionReactivationStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ReactivatedSelectionCandidate:
    source_delay: SelectionDelayCandidate
    reactivation_kind: str
    reactivation_trigger: str
    preserves_delay_trace: bool
    preserves_pressure_trace: bool
    selects_now: bool
    clears_delay_record: bool
    status: str


@dataclass(frozen=True)
class DelayedSelectionReactivationPolicy:
    name: str
    accepts_delayed_candidates: bool
    permits_reactivation_without_selection: bool
    preserves_delay_trace: bool
    rejects_delay_clearance: bool
    generates_immediate_adoption: bool
    status: str


@dataclass(frozen=True)
class DelayedSelectionReactivationBundle:
    source_bundle: ContextPressureSelectionDelayBundle
    policy: DelayedSelectionReactivationPolicy
    reactivated_candidates: tuple[ReactivatedSelectionCandidate, ...]
    reactivated_without_selection: tuple[ReactivatedSelectionCandidate, ...]
    reactivated_with_immediate_selection: tuple[ReactivatedSelectionCandidate, ...]
    still_delayed_candidates: tuple[ReactivatedSelectionCandidate, ...]
    stop_lines: tuple[str, ...]
    generated_immediate_adoption: bool
    generated_delay_clearance: bool
    generated_pressure_trace_deletion: bool
    status: str


@dataclass(frozen=True)
class DelayedSelectionReactivationObservation:
    source_status: str
    steps: tuple[DelayedSelectionReactivationStep, ...]
    bundle: DelayedSelectionReactivationBundle
    delayed_candidates_reactivated: bool
    selection_and_nonselection_paths_preserved: bool
    delay_and_pressure_traces_preserved: bool
    reactivation_not_immediate_adoption: bool
    no_delay_clearance_or_trace_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1849, "source_reentry", "reuse_1799_1848_context_pressure_selection_delay", "context_pressure_selection_delay_preserved"),
    (1850, "source_reentry", "next_xi_received", "delayed_selection_reactivation_stress_received"),
    (1851, "source_reentry", "delay_candidates_recheck", "delay_candidates_available"),
    (1852, "reactivation_request", "delayed_selection_reactivation_request", "delayed_selection_reactivation_candidate"),
    (1853, "reactivation_request", "reactivation_not_immediate_adoption_guard", "immediate_adoption_non_identity_preserved"),
    (1854, "reactivation_request", "reactivation_not_delay_clearance_guard", "delay_clearance_blocked"),
    (1855, "reactivation_request", "reactivation_not_pressure_trace_deletion_guard", "pressure_trace_deletion_non_identity_preserved"),
    (1856, "policy_layer", "delayed_selection_reactivation_policy", "delayed_selection_reactivation_policy_recorded"),
    (1857, "policy_layer", "delayed_candidate_acceptance_rule", "delayed_candidate_acceptance_recorded"),
    (1858, "policy_layer", "reactivation_without_selection_permission", "reactivation_without_selection_permission_recorded"),
    (1859, "policy_layer", "delay_trace_preservation_rule", "delay_trace_preservation_recorded"),
    (1860, "policy_layer", "delay_clearance_rejection_rule", "delay_clearance_rejection_recorded"),
    (1861, "reactivation_layer", "weak_immediate_candidate_reactivation", "weak_immediate_candidate_reactivation_recorded"),
    (1862, "reactivation_layer", "medium_delayed_candidate_reactivation", "medium_delayed_candidate_reactivation_recorded"),
    (1863, "reactivation_layer", "strong_delayed_candidate_reactivation", "strong_delayed_candidate_reactivation_recorded"),
    (1864, "reactivation_layer", "delay_trace_carry", "delay_trace_carried"),
    (1865, "reactivation_layer", "pressure_trace_carry", "pressure_trace_carried"),
    (1866, "reactivation_layer", "immediate_adoption_false_record", "immediate_adoption_false_recorded"),
    (1867, "reactivation_layer", "delay_clearance_false_record", "delay_clearance_false_recorded"),
    (1868, "partition_layer", "reactivated_without_selection_partition", "reactivated_without_selection_partition_recorded"),
    (1869, "partition_layer", "reactivated_with_immediate_selection_partition", "reactivated_with_immediate_selection_partition_recorded"),
    (1870, "partition_layer", "still_delayed_partition", "still_delayed_partition_recorded"),
    (1871, "partition_layer", "partition_not_resolution_guard", "partition_resolution_non_identity"),
    (1872, "partition_layer", "still_delayed_not_failure_guard", "still_delayed_failure_non_identity"),
    (1873, "reactivation_view", "delayed_selection_reactivation_view", "delayed_selection_reactivation_view_created"),
    (1874, "reactivation_view", "delay_trace_view", "delay_trace_view_created"),
    (1875, "reactivation_view", "pressure_trace_view", "pressure_trace_view_created"),
    (1876, "reactivation_view", "reactivated_nonselection_view", "reactivated_nonselection_view_created"),
    (1877, "bundle", "delayed_selection_reactivation_bundle_creation", "delayed_selection_reactivation_bundle_created"),
    (1878, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1879, "bundle", "stop_lines_carry", "delayed_selection_reactivation_stop_lines_carried"),
    (1880, "bundle", "generated_immediate_adoption_false", "generated_immediate_adoption_false_recorded"),
    (1881, "bundle", "generated_delay_clearance_false", "generated_delay_clearance_false_recorded"),
    (1882, "bundle", "generated_pressure_trace_deletion_false", "generated_pressure_trace_deletion_false_recorded"),
    (1883, "integrity", "delayed_candidates_reactivated_check", "delayed_candidates_reactivated_confirmed"),
    (1884, "integrity", "selection_nonselection_paths_check", "selection_nonselection_paths_confirmed"),
    (1885, "integrity", "delay_pressure_traces_check", "delay_pressure_traces_confirmed"),
    (1886, "integrity", "reactivation_not_adoption_check", "reactivation_not_adoption_confirmed"),
    (1887, "integrity", "no_clearance_trace_deletion_check", "no_clearance_trace_deletion_confirmed"),
    (1888, "non_identity", "reactivation_vs_immediate_adoption_split", "reactivation_immediate_adoption_non_identity"),
    (1889, "non_identity", "reactivation_vs_delay_clearance_split", "reactivation_delay_clearance_non_identity"),
    (1890, "non_identity", "still_delayed_vs_failure_split", "still_delayed_failure_non_identity"),
    (1891, "non_identity", "reactivation_vs_resolution_split", "reactivation_resolution_non_identity"),
    (1892, "music_subject", "reactivation_as_returned_attention", "returned_attention_preserved"),
    (1893, "music_subject", "medium_reactivation_as_reopened_reading", "medium_reactivation_reopened_reading_preserved"),
    (1894, "music_subject", "strong_reactivation_as_active_pull", "strong_reactivation_active_pull_preserved"),
    (1895, "summary", "delayed_selection_reactivation_summary", "delayed_selection_reactivation_observed"),
    (1896, "summary", "reactivation_without_adoption_or_clearance_summary", "reactivation_without_adoption_or_clearance_confirmed"),
    (1897, "next_plan", "reactivated_selection_commitment_boundary_next_candidate", "reactivated_selection_commitment_boundary_next_candidate"),
    (1898, "next_plan", "next_xi_selection", "xi_reactivated_selection_commitment_boundary_stress"),
)


def _build_steps() -> tuple[DelayedSelectionReactivationStep, ...]:
    previous = "context_pressure_selection_delay_1799_1848"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            DelayedSelectionReactivationStep(
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


def _reactivation_candidate(delay: SelectionDelayCandidate) -> ReactivatedSelectionCandidate:
    if delay.selects_now:
        kind = "immediate_candidate_reactivation_record"
        trigger = "stable_context_returns_as_reference"
        selects_now = True
    elif "ambiguity" in delay.delay_kind:
        kind = "ambiguous_delay_reactivation_candidate"
        trigger = "later_context_reopens_suspended_reading"
        selects_now = False
    else:
        kind = "strong_delay_reactivation_candidate"
        trigger = "unresolved_pull_becomes_active_again"
        selects_now = False

    return ReactivatedSelectionCandidate(
        source_delay=delay,
        reactivation_kind=kind,
        reactivation_trigger=trigger,
        preserves_delay_trace=True,
        preserves_pressure_trace=delay.preserves_pressure_trace,
        selects_now=selects_now,
        clears_delay_record=False,
        status="delayed_selection_reactivation_recorded_without_adoption_or_clearance",
    )


def build_delayed_selection_reactivation_bundle(
    source: ContextPressureSelectionDelayBundle,
) -> DelayedSelectionReactivationBundle:
    policy = DelayedSelectionReactivationPolicy(
        name="delayed_selection_reactivation_policy",
        accepts_delayed_candidates=True,
        permits_reactivation_without_selection=True,
        preserves_delay_trace=True,
        rejects_delay_clearance=True,
        generates_immediate_adoption=False,
        status="delayed_selection_reactivation_policy_preserves_open_reactivation",
    )
    candidates = tuple(
        _reactivation_candidate(delay)
        for delay in source.delay_candidates
    )
    without_selection = tuple(candidate for candidate in candidates if not candidate.selects_now)
    with_selection = tuple(candidate for candidate in candidates if candidate.selects_now)
    still_delayed = tuple(
        candidate for candidate in without_selection if "delay" in candidate.reactivation_kind
    )
    return DelayedSelectionReactivationBundle(
        source_bundle=source,
        policy=policy,
        reactivated_candidates=candidates,
        reactivated_without_selection=without_selection,
        reactivated_with_immediate_selection=with_selection,
        still_delayed_candidates=still_delayed,
        stop_lines=(
            "reactivation_not_immediate_adoption",
            "reactivation_not_delay_clearance",
            "reactivation_not_pressure_trace_deletion",
            "still_delayed_not_failure",
            "reactivation_not_resolution",
        ),
        generated_immediate_adoption=False,
        generated_delay_clearance=False,
        generated_pressure_trace_deletion=False,
        status="delayed_selection_reactivation_bundle_1849_1898_built_without_adoption_or_clearance",
    )


def observe_delayed_selection_reactivation() -> DelayedSelectionReactivationObservation:
    source = observe_context_pressure_selection_delay()
    bundle = build_delayed_selection_reactivation_bundle(source.bundle)
    steps = _build_steps()

    return DelayedSelectionReactivationObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        delayed_candidates_reactivated=(
            len(bundle.reactivated_candidates) == len(source.bundle.delay_candidates)
            and len(bundle.reactivated_without_selection) == 2
        ),
        selection_and_nonselection_paths_preserved=(
            len(bundle.reactivated_with_immediate_selection) == 1
            and len(bundle.reactivated_without_selection) == 2
        ),
        delay_and_pressure_traces_preserved=(
            bundle.policy.preserves_delay_trace is True
            and all(
                candidate.preserves_delay_trace and candidate.preserves_pressure_trace
                for candidate in bundle.reactivated_candidates
            )
        ),
        reactivation_not_immediate_adoption=(
            bundle.policy.generates_immediate_adoption is False
            and bundle.generated_immediate_adoption is False
        ),
        no_delay_clearance_or_trace_deletion=(
            bundle.generated_delay_clearance is False
            and bundle.generated_pressure_trace_deletion is False
            and all(not candidate.clears_delay_record for candidate in bundle.reactivated_candidates)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="delayed_selection_reactivation_1849_1898_observed_without_adoption_or_delay_clearance",
    )


def run_checks() -> None:
    observation = observe_delayed_selection_reactivation()
    bundle = observation.bundle

    assert observation.source_status == (
        "context_pressure_selection_delay_1799_1848_observed_without_failure_or_forced_selection"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1849
    assert observation.steps[-1].number == 1898
    assert observation.delayed_candidates_reactivated is True
    assert observation.selection_and_nonselection_paths_preserved is True
    assert observation.delay_and_pressure_traces_preserved is True
    assert observation.reactivation_not_immediate_adoption is True
    assert observation.no_delay_clearance_or_trace_deletion is True
    assert len(bundle.reactivated_candidates) == 3
    assert len(bundle.reactivated_without_selection) == 2
    assert len(bundle.reactivated_with_immediate_selection) == 1
    assert len(bundle.still_delayed_candidates) == 2
    assert bundle.generated_immediate_adoption is False
    assert bundle.generated_delay_clearance is False
    assert bundle.generated_pressure_trace_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_reactivated_selection_commitment_boundary_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_delayed_selection_reactivation().status)
