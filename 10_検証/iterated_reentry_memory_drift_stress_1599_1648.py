"""reentry反復後のmemory driftを検査する最小実験。"""

from dataclasses import dataclass

from post_resolution_reentry_cycle_stress_1549_1598 import (
    PostResolutionReentryCandidate,
    PostResolutionReentryCycleBundle,
    observe_post_resolution_reentry_cycle,
)


@dataclass(frozen=True)
class IteratedReentryMemoryDriftStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class MemoryDriftCandidate:
    source_reentry: PostResolutionReentryCandidate
    drift_kind: str
    identity_anchor: str
    drift_vector: str
    preserves_origin_trace: bool
    preserves_reentry_route: bool
    treats_drift_as_error: bool
    collapses_to_identical_memory: bool
    status: str


@dataclass(frozen=True)
class IteratedReentryDriftPolicy:
    name: str
    permits_nonidentical_reentry: bool
    preserves_identity_anchor: bool
    rejects_error_collapse: bool
    rejects_identity_collapse: bool
    generates_memory_reset: bool
    status: str


@dataclass(frozen=True)
class IteratedReentryMemoryDriftBundle:
    source_bundle: PostResolutionReentryCycleBundle
    policy: IteratedReentryDriftPolicy
    drift_candidates: tuple[MemoryDriftCandidate, ...]
    returned_drifts: tuple[MemoryDriftCandidate, ...]
    redeferred_drifts: tuple[MemoryDriftCandidate, ...]
    stop_lines: tuple[str, ...]
    generated_identity_collapse: bool
    generated_error_collapse: bool
    generated_memory_reset: bool
    status: str


@dataclass(frozen=True)
class IteratedReentryMemoryDriftObservation:
    source_status: str
    steps: tuple[IteratedReentryMemoryDriftStep, ...]
    bundle: IteratedReentryMemoryDriftBundle
    all_reentries_generate_drift_candidates: bool
    origin_trace_and_route_preserved: bool
    drift_without_identity_collapse: bool
    drift_not_error_or_memory_reset: bool
    returned_and_redeferred_drifts_preserved: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1599, "source_reentry", "reuse_1549_1598_post_resolution_reentry_cycle", "post_resolution_reentry_cycle_preserved"),
    (1600, "source_reentry", "next_xi_received", "iterated_reentry_memory_drift_stress_received"),
    (1601, "source_reentry", "reentry_candidates_recheck", "reentry_candidates_available"),
    (1602, "iteration_request", "iterated_reentry_request", "iterated_reentry_candidate"),
    (1603, "iteration_request", "drift_not_error_guard", "drift_error_non_identity_preserved"),
    (1604, "iteration_request", "drift_not_identity_collapse_guard", "identity_collapse_blocked"),
    (1605, "iteration_request", "drift_not_memory_reset_guard", "memory_reset_non_identity_preserved"),
    (1606, "policy_layer", "iterated_reentry_drift_policy", "iterated_reentry_drift_policy_recorded"),
    (1607, "policy_layer", "nonidentical_reentry_permission", "nonidentical_reentry_permission_recorded"),
    (1608, "policy_layer", "identity_anchor_preservation_rule", "identity_anchor_preservation_recorded"),
    (1609, "policy_layer", "error_collapse_rejection_rule", "error_collapse_rejection_recorded"),
    (1610, "policy_layer", "identity_collapse_rejection_rule", "identity_collapse_rejection_recorded"),
    (1611, "drift_layer", "primary_returned_memory_drift", "primary_returned_memory_drift_recorded"),
    (1612, "drift_layer", "derivative_returned_memory_drift", "derivative_returned_memory_drift_recorded"),
    (1613, "drift_layer", "latent_redeferred_memory_drift", "latent_redeferred_memory_drift_recorded"),
    (1614, "drift_layer", "origin_trace_anchor_carry", "origin_trace_anchor_carried"),
    (1615, "drift_layer", "reentry_route_carry", "reentry_route_carried"),
    (1616, "drift_layer", "error_false_record", "error_false_recorded"),
    (1617, "drift_layer", "identity_collapse_false_record", "identity_collapse_false_recorded"),
    (1618, "drift_partition", "returned_drift_partition", "returned_drift_partition_recorded"),
    (1619, "drift_partition", "redeferred_drift_partition", "redeferred_drift_partition_recorded"),
    (1620, "drift_partition", "partition_not_ranking_guard", "partition_ranking_non_identity"),
    (1621, "drift_partition", "drift_not_degradation_guard", "drift_degradation_non_identity"),
    (1622, "drift_partition", "redeferred_drift_not_failure_guard", "redeferred_drift_failure_non_identity"),
    (1623, "drift_view", "iterated_reentry_drift_view", "iterated_reentry_drift_view_created"),
    (1624, "drift_view", "identity_anchor_view", "identity_anchor_view_created"),
    (1625, "drift_view", "route_preservation_view", "route_preservation_view_created"),
    (1626, "drift_view", "nonidentical_memory_view", "nonidentical_memory_view_created"),
    (1627, "bundle", "iterated_reentry_memory_drift_bundle_creation", "iterated_reentry_memory_drift_bundle_created"),
    (1628, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1629, "bundle", "stop_lines_carry", "iterated_reentry_drift_stop_lines_carried"),
    (1630, "bundle", "generated_identity_collapse_false", "generated_identity_collapse_false_recorded"),
    (1631, "bundle", "generated_error_collapse_false", "generated_error_collapse_false_recorded"),
    (1632, "bundle", "generated_memory_reset_false", "generated_memory_reset_false_recorded"),
    (1633, "integrity", "all_reentries_generate_drift_candidates_check", "all_reentries_generate_drift_candidates_confirmed"),
    (1634, "integrity", "origin_trace_route_preservation_check", "origin_trace_route_preservation_confirmed"),
    (1635, "integrity", "identity_anchor_preservation_check", "identity_anchor_preservation_confirmed"),
    (1636, "integrity", "drift_without_identity_collapse_check", "drift_without_identity_collapse_confirmed"),
    (1637, "integrity", "drift_not_error_reset_check", "drift_not_error_reset_confirmed"),
    (1638, "non_identity", "drift_vs_error_split", "drift_error_non_identity"),
    (1639, "non_identity", "drift_vs_identical_memory_split", "drift_identical_memory_non_identity"),
    (1640, "non_identity", "iteration_vs_reset_split", "iteration_reset_non_identity"),
    (1641, "non_identity", "redeferred_drift_vs_failure_split", "redeferred_drift_failure_non_identity"),
    (1642, "music_subject", "drift_as_reheard_difference", "drift_reheard_difference_preserved"),
    (1643, "music_subject", "returned_drift_as_changed_expectation", "returned_drift_changed_expectation_preserved"),
    (1644, "music_subject", "redeferred_drift_as_suspended_continuity", "redeferred_drift_suspended_continuity_preserved"),
    (1645, "summary", "iterated_reentry_memory_drift_summary", "iterated_reentry_memory_drift_observed"),
    (1646, "summary", "nonidentical_memory_no_error_summary", "nonidentical_memory_no_error_confirmed"),
    (1647, "next_plan", "drift_accumulation_threshold_next_candidate", "drift_accumulation_threshold_next_candidate"),
    (1648, "next_plan", "next_xi_selection", "xi_drift_accumulation_threshold_stress"),
)


def _build_steps() -> tuple[IteratedReentryMemoryDriftStep, ...]:
    previous = "post_resolution_reentry_cycle_1549_1598"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            IteratedReentryMemoryDriftStep(
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


def _drift_candidate(reentry: PostResolutionReentryCandidate) -> MemoryDriftCandidate:
    if reentry.reentry_kind == "returned_memory_reentry_candidate":
        drift_kind = "returned_memory_rehearing_drift"
        drift_vector = "changed_expectation_after_return"
    else:
        drift_kind = "redeferred_memory_continuation_drift"
        drift_vector = "suspended_continuity_after_reentry"

    return MemoryDriftCandidate(
        source_reentry=reentry,
        drift_kind=drift_kind,
        identity_anchor=reentry.cycle_position,
        drift_vector=drift_vector,
        preserves_origin_trace=reentry.keeps_return_history,
        preserves_reentry_route=reentry.keeps_future_route,
        treats_drift_as_error=False,
        collapses_to_identical_memory=False,
        status="iterated_reentry_memory_drift_recorded_without_error_or_identity_collapse",
    )


def build_iterated_reentry_memory_drift_bundle(
    source: PostResolutionReentryCycleBundle,
) -> IteratedReentryMemoryDriftBundle:
    policy = IteratedReentryDriftPolicy(
        name="iterated_reentry_memory_drift_policy",
        permits_nonidentical_reentry=True,
        preserves_identity_anchor=True,
        rejects_error_collapse=True,
        rejects_identity_collapse=True,
        generates_memory_reset=False,
        status="iterated_reentry_policy_preserves_drift_without_collapse",
    )
    candidates = tuple(_drift_candidate(candidate) for candidate in source.candidates)
    returned = tuple(candidate for candidate in candidates if "returned" in candidate.drift_kind)
    redeferred = tuple(candidate for candidate in candidates if "redeferred" in candidate.drift_kind)
    return IteratedReentryMemoryDriftBundle(
        source_bundle=source,
        policy=policy,
        drift_candidates=candidates,
        returned_drifts=returned,
        redeferred_drifts=redeferred,
        stop_lines=(
            "drift_not_error",
            "drift_not_identity_collapse",
            "drift_not_memory_reset",
            "iteration_not_reset",
            "redeferred_drift_not_failure",
        ),
        generated_identity_collapse=False,
        generated_error_collapse=False,
        generated_memory_reset=False,
        status="iterated_reentry_memory_drift_bundle_1599_1648_built_without_collapse",
    )


def observe_iterated_reentry_memory_drift() -> IteratedReentryMemoryDriftObservation:
    source = observe_post_resolution_reentry_cycle()
    bundle = build_iterated_reentry_memory_drift_bundle(source.bundle)
    steps = _build_steps()

    return IteratedReentryMemoryDriftObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        all_reentries_generate_drift_candidates=(
            len(bundle.drift_candidates) == len(source.bundle.candidates)
        ),
        origin_trace_and_route_preserved=all(
            candidate.preserves_origin_trace and candidate.preserves_reentry_route
            for candidate in bundle.drift_candidates
        ),
        drift_without_identity_collapse=(
            bundle.policy.preserves_identity_anchor is True
            and bundle.generated_identity_collapse is False
            and all(not candidate.collapses_to_identical_memory for candidate in bundle.drift_candidates)
        ),
        drift_not_error_or_memory_reset=(
            bundle.policy.rejects_error_collapse is True
            and bundle.generated_error_collapse is False
            and bundle.generated_memory_reset is False
            and all(not candidate.treats_drift_as_error for candidate in bundle.drift_candidates)
        ),
        returned_and_redeferred_drifts_preserved=(
            len(bundle.returned_drifts) == 2 and len(bundle.redeferred_drifts) == 1
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="iterated_reentry_memory_drift_1599_1648_observed_without_error_or_identity_collapse",
    )


def run_checks() -> None:
    observation = observe_iterated_reentry_memory_drift()
    bundle = observation.bundle

    assert observation.source_status == (
        "post_resolution_reentry_cycle_1549_1598_observed_without_closure_or_final_answer"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1599
    assert observation.steps[-1].number == 1648
    assert observation.all_reentries_generate_drift_candidates is True
    assert observation.origin_trace_and_route_preserved is True
    assert observation.drift_without_identity_collapse is True
    assert observation.drift_not_error_or_memory_reset is True
    assert observation.returned_and_redeferred_drifts_preserved is True
    assert len(bundle.drift_candidates) == 3
    assert len(bundle.returned_drifts) == 2
    assert len(bundle.redeferred_drifts) == 1
    assert bundle.generated_identity_collapse is False
    assert bundle.generated_error_collapse is False
    assert bundle.generated_memory_reset is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_drift_accumulation_threshold_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_iterated_reentry_memory_drift().status)
