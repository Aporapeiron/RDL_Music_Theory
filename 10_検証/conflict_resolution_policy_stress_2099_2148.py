"""detected conflictのresolution policy境界を検査する最小実験。"""

from dataclasses import dataclass

from revision_conflict_detection_stress_2049_2098 import (
    RevisionConflictCandidate,
    RevisionConflictDetectionBundle,
    observe_revision_conflict_detection,
)


@dataclass(frozen=True)
class ConflictResolutionPolicyStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ConflictResolutionRoute:
    source_conflict: RevisionConflictCandidate
    route_kind: str
    policy_reason: str
    preserves_conflict_trace: bool
    preserves_revision_trace: bool
    resolves_now: bool
    deletes_conflict: bool
    status: str


@dataclass(frozen=True)
class ConflictResolutionPolicy:
    name: str
    accepts_detected_conflicts: bool
    permits_deferred_resolution: bool
    permits_weight_revision: bool
    permits_recheck_route: bool
    generates_forced_resolution: bool
    status: str


@dataclass(frozen=True)
class ConflictResolutionPolicyBundle:
    source_bundle: RevisionConflictDetectionBundle
    policy: ConflictResolutionPolicy
    resolution_routes: tuple[ConflictResolutionRoute, ...]
    deferred_resolution_routes: tuple[ConflictResolutionRoute, ...]
    weight_revision_routes: tuple[ConflictResolutionRoute, ...]
    recheck_routes: tuple[ConflictResolutionRoute, ...]
    stop_lines: tuple[str, ...]
    generated_forced_resolution: bool
    generated_conflict_deletion: bool
    generated_final_verdict: bool
    status: str


@dataclass(frozen=True)
class ConflictResolutionPolicyObservation:
    source_status: str
    steps: tuple[ConflictResolutionPolicyStep, ...]
    bundle: ConflictResolutionPolicyBundle
    detected_conflicts_receive_routes: bool
    route_variety_preserved: bool
    conflict_and_revision_traces_preserved: bool
    policy_not_forced_resolution_or_verdict: bool
    no_conflict_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2099, "source_reentry", "reuse_2049_2098_revision_conflict_detection", "revision_conflict_detection_preserved"),
    (2100, "source_reentry", "next_xi_received", "conflict_resolution_policy_stress_received"),
    (2101, "source_reentry", "detected_conflicts_recheck", "detected_conflicts_available"),
    (2102, "policy_request", "conflict_resolution_policy_request", "conflict_resolution_policy_candidate"),
    (2103, "policy_request", "policy_not_forced_resolution_guard", "forced_resolution_non_identity_preserved"),
    (2104, "policy_request", "policy_not_conflict_deletion_guard", "conflict_deletion_blocked"),
    (2105, "policy_request", "policy_not_final_verdict_guard", "final_verdict_non_identity_preserved"),
    (2106, "policy_layer", "conflict_resolution_policy", "conflict_resolution_policy_recorded"),
    (2107, "policy_layer", "detected_conflict_acceptance_rule", "detected_conflict_acceptance_recorded"),
    (2108, "policy_layer", "deferred_resolution_permission", "deferred_resolution_permission_recorded"),
    (2109, "policy_layer", "weight_revision_permission", "weight_revision_permission_recorded"),
    (2110, "policy_layer", "recheck_route_permission", "recheck_route_permission_recorded"),
    (2111, "route_layer", "reference_nonconflict_recheck_route", "reference_nonconflict_recheck_route_recorded"),
    (2112, "route_layer", "boundary_conflict_deferred_resolution_route", "boundary_conflict_deferred_resolution_route_recorded"),
    (2113, "route_layer", "committed_tension_weight_revision_route", "committed_tension_weight_revision_route_recorded"),
    (2114, "route_layer", "conflict_trace_carry", "conflict_trace_carried"),
    (2115, "route_layer", "revision_trace_carry", "revision_trace_carried"),
    (2116, "route_layer", "forced_resolution_false_record", "forced_resolution_false_recorded"),
    (2117, "route_layer", "conflict_deletion_false_record", "conflict_deletion_false_recorded"),
    (2118, "partition_layer", "deferred_resolution_route_partition", "deferred_resolution_route_partition_recorded"),
    (2119, "partition_layer", "weight_revision_route_partition", "weight_revision_route_partition_recorded"),
    (2120, "partition_layer", "recheck_route_partition", "recheck_route_partition_recorded"),
    (2121, "partition_layer", "partition_not_solution_guard", "partition_solution_non_identity"),
    (2122, "partition_layer", "deferred_resolution_not_failure_guard", "deferred_resolution_failure_non_identity"),
    (2123, "policy_view", "conflict_resolution_policy_view", "conflict_resolution_policy_view_created"),
    (2124, "policy_view", "deferred_resolution_view", "deferred_resolution_view_created"),
    (2125, "policy_view", "weight_revision_view", "weight_revision_view_created"),
    (2126, "policy_view", "recheck_route_view", "recheck_route_view_created"),
    (2127, "bundle", "conflict_resolution_policy_bundle_creation", "conflict_resolution_policy_bundle_created"),
    (2128, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2129, "bundle", "stop_lines_carry", "conflict_resolution_policy_stop_lines_carried"),
    (2130, "bundle", "generated_forced_resolution_false", "generated_forced_resolution_false_recorded"),
    (2131, "bundle", "generated_conflict_deletion_false", "generated_conflict_deletion_false_recorded"),
    (2132, "bundle", "generated_final_verdict_false", "generated_final_verdict_false_recorded"),
    (2133, "integrity", "detected_conflicts_receive_routes_check", "detected_conflicts_receive_routes_confirmed"),
    (2134, "integrity", "route_variety_preservation_check", "route_variety_preservation_confirmed"),
    (2135, "integrity", "conflict_revision_trace_check", "conflict_revision_trace_confirmed"),
    (2136, "integrity", "policy_not_resolution_verdict_check", "policy_not_resolution_verdict_confirmed"),
    (2137, "integrity", "no_conflict_deletion_check", "no_conflict_deletion_confirmed"),
    (2138, "non_identity", "policy_vs_resolution_split", "policy_resolution_non_identity"),
    (2139, "non_identity", "resolution_policy_vs_final_verdict_split", "resolution_policy_final_verdict_non_identity"),
    (2140, "non_identity", "deferred_resolution_vs_failure_split", "deferred_resolution_failure_non_identity"),
    (2141, "non_identity", "weight_revision_vs_conflict_deletion_split", "weight_revision_conflict_deletion_non_identity"),
    (2142, "music_subject", "policy_as_response_shape", "response_shape_preserved"),
    (2143, "music_subject", "deferred_resolution_as_sustained_tension", "sustained_tension_preserved"),
    (2144, "music_subject", "weight_revision_as_changed_hearing_priority", "changed_hearing_priority_preserved"),
    (2145, "summary", "conflict_resolution_policy_summary", "conflict_resolution_policy_observed"),
    (2146, "summary", "policy_without_forced_resolution_summary", "policy_without_forced_resolution_confirmed"),
    (2147, "next_plan", "policy_execution_readiness_next_candidate", "policy_execution_readiness_next_candidate"),
    (2148, "next_plan", "next_xi_selection", "xi_policy_execution_readiness_stress"),
)


def _build_steps() -> tuple[ConflictResolutionPolicyStep, ...]:
    previous = "revision_conflict_detection_2049_2098"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            ConflictResolutionPolicyStep(
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


def _resolution_route(conflict: RevisionConflictCandidate) -> ConflictResolutionRoute:
    if not conflict.detects_conflict:
        kind = "nonconflict_recheck_route"
        reason = "stable_reference_requires_periodic_recheck"
        resolves_now = False
    elif "boundary" in conflict.conflict_kind:
        kind = "deferred_resolution_route"
        reason = "open_reading_pressure_requires_later_context"
        resolves_now = False
    else:
        kind = "weight_revision_route"
        reason = "interpretive_friction_requires_changed_priority"
        resolves_now = False

    return ConflictResolutionRoute(
        source_conflict=conflict,
        route_kind=kind,
        policy_reason=reason,
        preserves_conflict_trace=True,
        preserves_revision_trace=conflict.preserves_revision_trace,
        resolves_now=resolves_now,
        deletes_conflict=False,
        status="conflict_resolution_route_recorded_without_forced_resolution",
    )


def build_conflict_resolution_policy_bundle(
    source: RevisionConflictDetectionBundle,
) -> ConflictResolutionPolicyBundle:
    policy = ConflictResolutionPolicy(
        name="conflict_resolution_policy",
        accepts_detected_conflicts=True,
        permits_deferred_resolution=True,
        permits_weight_revision=True,
        permits_recheck_route=True,
        generates_forced_resolution=False,
        status="conflict_resolution_policy_preserves_routes_without_forced_solution",
    )
    routes = tuple(_resolution_route(conflict) for conflict in source.conflict_candidates)
    deferred = tuple(route for route in routes if route.route_kind == "deferred_resolution_route")
    weight = tuple(route for route in routes if route.route_kind == "weight_revision_route")
    recheck = tuple(route for route in routes if route.route_kind == "nonconflict_recheck_route")
    return ConflictResolutionPolicyBundle(
        source_bundle=source,
        policy=policy,
        resolution_routes=routes,
        deferred_resolution_routes=deferred,
        weight_revision_routes=weight,
        recheck_routes=recheck,
        stop_lines=(
            "policy_not_forced_resolution",
            "policy_not_conflict_deletion",
            "policy_not_final_verdict",
            "deferred_resolution_not_failure",
            "partition_not_solution",
        ),
        generated_forced_resolution=False,
        generated_conflict_deletion=False,
        generated_final_verdict=False,
        status="conflict_resolution_policy_bundle_2099_2148_built_without_forced_resolution",
    )


def observe_conflict_resolution_policy() -> ConflictResolutionPolicyObservation:
    source = observe_revision_conflict_detection()
    bundle = build_conflict_resolution_policy_bundle(source.bundle)
    steps = _build_steps()

    return ConflictResolutionPolicyObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        detected_conflicts_receive_routes=(
            len(bundle.resolution_routes) == len(source.bundle.conflict_candidates)
            and len(bundle.deferred_resolution_routes) == 1
            and len(bundle.weight_revision_routes) == 1
        ),
        route_variety_preserved=(
            len(bundle.deferred_resolution_routes) == 1
            and len(bundle.weight_revision_routes) == 1
            and len(bundle.recheck_routes) == 1
        ),
        conflict_and_revision_traces_preserved=all(
            route.preserves_conflict_trace and route.preserves_revision_trace
            for route in bundle.resolution_routes
        ),
        policy_not_forced_resolution_or_verdict=(
            bundle.policy.generates_forced_resolution is False
            and bundle.generated_forced_resolution is False
            and bundle.generated_final_verdict is False
            and all(not route.resolves_now for route in bundle.resolution_routes)
        ),
        no_conflict_deletion=(
            bundle.generated_conflict_deletion is False
            and all(not route.deletes_conflict for route in bundle.resolution_routes)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="conflict_resolution_policy_2099_2148_observed_without_forced_resolution_or_deletion",
    )


def run_checks() -> None:
    observation = observe_conflict_resolution_policy()
    bundle = observation.bundle

    assert observation.source_status == (
        "revision_conflict_detection_2049_2098_observed_without_resolution_or_deletion"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2099
    assert observation.steps[-1].number == 2148
    assert observation.detected_conflicts_receive_routes is True
    assert observation.route_variety_preserved is True
    assert observation.conflict_and_revision_traces_preserved is True
    assert observation.policy_not_forced_resolution_or_verdict is True
    assert observation.no_conflict_deletion is True
    assert len(bundle.resolution_routes) == 3
    assert len(bundle.deferred_resolution_routes) == 1
    assert len(bundle.weight_revision_routes) == 1
    assert len(bundle.recheck_routes) == 1
    assert bundle.generated_forced_resolution is False
    assert bundle.generated_conflict_deletion is False
    assert bundle.generated_final_verdict is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_policy_execution_readiness_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_conflict_resolution_policy().status)
