"""conflict resolution policyのexecution readiness境界を検査する最小実験。"""

from dataclasses import dataclass

from conflict_resolution_policy_stress_2099_2148 import (
    ConflictResolutionPolicyBundle,
    ConflictResolutionRoute,
    observe_conflict_resolution_policy,
)


@dataclass(frozen=True)
class PolicyExecutionReadinessStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class PolicyExecutionReadinessItem:
    source_route: ConflictResolutionRoute
    readiness_kind: str
    required_condition: str
    preserves_route_partition: bool
    preserves_conflict_trace: bool
    permits_later_execution: bool
    executes_now: bool
    resolves_now: bool
    status: str


@dataclass(frozen=True)
class PolicyExecutionReadinessBundle:
    source_bundle: ConflictResolutionPolicyBundle
    readiness_items: tuple[PolicyExecutionReadinessItem, ...]
    deferred_ready_items: tuple[PolicyExecutionReadinessItem, ...]
    weight_ready_items: tuple[PolicyExecutionReadinessItem, ...]
    recheck_ready_items: tuple[PolicyExecutionReadinessItem, ...]
    stop_lines: tuple[str, ...]
    generated_policy_execution: bool
    generated_resolution: bool
    generated_conflict_deletion: bool
    status: str


@dataclass(frozen=True)
class PolicyExecutionReadinessObservation:
    source_status: str
    steps: tuple[PolicyExecutionReadinessStep, ...]
    bundle: PolicyExecutionReadinessBundle
    every_route_gets_readiness_item: bool
    readiness_variety_preserved: bool
    route_and_conflict_traces_preserved: bool
    readiness_not_execution_or_resolution: bool
    no_conflict_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2149, "source_reentry", "reuse_2099_2148_conflict_resolution_policy", "conflict_resolution_policy_preserved"),
    (2150, "source_reentry", "next_xi_received", "policy_execution_readiness_stress_received"),
    (2151, "source_reentry", "resolution_routes_recheck", "resolution_routes_available"),
    (2152, "readiness_request", "policy_execution_readiness_request", "policy_execution_readiness_candidate"),
    (2153, "readiness_request", "readiness_not_execution_guard", "execution_non_identity_preserved"),
    (2154, "readiness_request", "readiness_not_resolution_guard", "resolution_non_identity_preserved"),
    (2155, "readiness_request", "readiness_not_conflict_deletion_guard", "conflict_deletion_blocked"),
    (2156, "readiness_layer", "readiness_item_generation", "readiness_items_recorded"),
    (2157, "readiness_layer", "deferred_route_readiness", "deferred_route_readiness_recorded"),
    (2158, "readiness_layer", "weight_revision_route_readiness", "weight_revision_route_readiness_recorded"),
    (2159, "readiness_layer", "recheck_route_readiness", "recheck_route_readiness_recorded"),
    (2160, "readiness_layer", "later_execution_permission", "later_execution_permission_recorded"),
    (2161, "readiness_layer", "executes_now_false_record", "executes_now_false_recorded"),
    (2162, "readiness_layer", "resolves_now_false_record", "resolves_now_false_recorded"),
    (2163, "precondition_layer", "later_context_requirement", "later_context_requirement_recorded"),
    (2164, "precondition_layer", "changed_priority_requirement", "changed_priority_requirement_recorded"),
    (2165, "precondition_layer", "periodic_recheck_requirement", "periodic_recheck_requirement_recorded"),
    (2166, "precondition_layer", "route_partition_carry", "route_partition_carried"),
    (2167, "precondition_layer", "conflict_trace_carry", "conflict_trace_carried"),
    (2168, "precondition_layer", "revision_trace_carry", "revision_trace_carried"),
    (2169, "partition_layer", "deferred_ready_partition", "deferred_ready_partition_recorded"),
    (2170, "partition_layer", "weight_ready_partition", "weight_ready_partition_recorded"),
    (2171, "partition_layer", "recheck_ready_partition", "recheck_ready_partition_recorded"),
    (2172, "partition_layer", "readiness_partition_not_execution_guard", "partition_execution_non_identity"),
    (2173, "partition_layer", "readiness_partition_not_solution_guard", "partition_solution_non_identity"),
    (2174, "readiness_view", "policy_execution_readiness_view", "policy_execution_readiness_view_created"),
    (2175, "readiness_view", "deferred_execution_readiness_view", "deferred_execution_readiness_view_created"),
    (2176, "readiness_view", "weight_revision_readiness_view", "weight_revision_readiness_view_created"),
    (2177, "readiness_view", "recheck_readiness_view", "recheck_readiness_view_created"),
    (2178, "bundle", "policy_execution_readiness_bundle_creation", "policy_execution_readiness_bundle_created"),
    (2179, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2180, "bundle", "stop_lines_carry", "policy_execution_readiness_stop_lines_carried"),
    (2181, "bundle", "generated_policy_execution_false", "generated_policy_execution_false_recorded"),
    (2182, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (2183, "bundle", "generated_conflict_deletion_false", "generated_conflict_deletion_false_recorded"),
    (2184, "integrity", "every_route_gets_readiness_item_check", "every_route_gets_readiness_item_confirmed"),
    (2185, "integrity", "readiness_variety_preservation_check", "readiness_variety_preservation_confirmed"),
    (2186, "integrity", "route_conflict_trace_check", "route_conflict_trace_confirmed"),
    (2187, "integrity", "readiness_not_execution_check", "readiness_not_execution_confirmed"),
    (2188, "integrity", "readiness_not_resolution_check", "readiness_not_resolution_confirmed"),
    (2189, "integrity", "no_conflict_deletion_check", "no_conflict_deletion_confirmed"),
    (2190, "non_identity", "readiness_vs_execution_split", "readiness_execution_non_identity"),
    (2191, "non_identity", "readiness_vs_resolution_split", "readiness_resolution_non_identity"),
    (2192, "non_identity", "execution_readiness_vs_final_verdict_split", "execution_readiness_final_verdict_non_identity"),
    (2193, "music_subject", "readiness_as_performance_entry_condition", "performance_entry_condition_preserved"),
    (2194, "music_subject", "deferred_readiness_as_waiting_context", "waiting_context_preserved"),
    (2195, "music_subject", "weight_readiness_as_hearing_priority_preparation", "hearing_priority_preparation_preserved"),
    (2196, "summary", "policy_execution_readiness_summary", "policy_execution_readiness_observed"),
    (2197, "summary", "readiness_without_execution_summary", "readiness_without_execution_confirmed"),
    (2198, "next_plan", "next_xi_selection", "xi_policy_execution_attempt_boundary_stress"),
)


def _build_steps() -> tuple[PolicyExecutionReadinessStep, ...]:
    previous = "conflict_resolution_policy_2099_2148"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            PolicyExecutionReadinessStep(
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


def _readiness_item(route: ConflictResolutionRoute) -> PolicyExecutionReadinessItem:
    if route.route_kind == "deferred_resolution_route":
        kind = "deferred_execution_readiness"
        condition = "later_context_must_arrive_before_execution"
    elif route.route_kind == "weight_revision_route":
        kind = "weight_revision_execution_readiness"
        condition = "changed_hearing_priority_must_be_available"
    else:
        kind = "recheck_execution_readiness"
        condition = "reference_state_must_be_periodically_rechecked"

    return PolicyExecutionReadinessItem(
        source_route=route,
        readiness_kind=kind,
        required_condition=condition,
        preserves_route_partition=True,
        preserves_conflict_trace=route.preserves_conflict_trace,
        permits_later_execution=True,
        executes_now=False,
        resolves_now=False,
        status="policy_execution_readiness_item_recorded_without_execution",
    )


def build_policy_execution_readiness_bundle(
    source: ConflictResolutionPolicyBundle,
) -> PolicyExecutionReadinessBundle:
    items = tuple(_readiness_item(route) for route in source.resolution_routes)
    deferred = tuple(item for item in items if item.readiness_kind == "deferred_execution_readiness")
    weight = tuple(item for item in items if item.readiness_kind == "weight_revision_execution_readiness")
    recheck = tuple(item for item in items if item.readiness_kind == "recheck_execution_readiness")
    return PolicyExecutionReadinessBundle(
        source_bundle=source,
        readiness_items=items,
        deferred_ready_items=deferred,
        weight_ready_items=weight,
        recheck_ready_items=recheck,
        stop_lines=(
            "readiness_not_execution",
            "readiness_not_resolution",
            "readiness_not_conflict_deletion",
            "readiness_partition_not_solution",
            "readiness_not_final_verdict",
        ),
        generated_policy_execution=False,
        generated_resolution=False,
        generated_conflict_deletion=False,
        status="policy_execution_readiness_bundle_2149_2198_built_without_execution",
    )


def observe_policy_execution_readiness() -> PolicyExecutionReadinessObservation:
    source = observe_conflict_resolution_policy()
    bundle = build_policy_execution_readiness_bundle(source.bundle)
    steps = _build_steps()

    return PolicyExecutionReadinessObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_route_gets_readiness_item=(
            len(bundle.readiness_items) == len(source.bundle.resolution_routes)
        ),
        readiness_variety_preserved=(
            len(bundle.deferred_ready_items) == 1
            and len(bundle.weight_ready_items) == 1
            and len(bundle.recheck_ready_items) == 1
        ),
        route_and_conflict_traces_preserved=all(
            item.preserves_route_partition and item.preserves_conflict_trace
            for item in bundle.readiness_items
        ),
        readiness_not_execution_or_resolution=(
            bundle.generated_policy_execution is False
            and bundle.generated_resolution is False
            and all(not item.executes_now and not item.resolves_now for item in bundle.readiness_items)
        ),
        no_conflict_deletion=(
            bundle.generated_conflict_deletion is False
            and all(not item.source_route.deletes_conflict for item in bundle.readiness_items)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="policy_execution_readiness_2149_2198_observed_without_execution_or_resolution",
    )


def run_checks() -> None:
    observation = observe_policy_execution_readiness()
    bundle = observation.bundle

    assert observation.source_status == (
        "conflict_resolution_policy_2099_2148_observed_without_forced_resolution_or_deletion"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2149
    assert observation.steps[-1].number == 2198
    assert observation.every_route_gets_readiness_item is True
    assert observation.readiness_variety_preserved is True
    assert observation.route_and_conflict_traces_preserved is True
    assert observation.readiness_not_execution_or_resolution is True
    assert observation.no_conflict_deletion is True
    assert len(bundle.readiness_items) == 3
    assert len(bundle.deferred_ready_items) == 1
    assert len(bundle.weight_ready_items) == 1
    assert len(bundle.recheck_ready_items) == 1
    assert bundle.generated_policy_execution is False
    assert bundle.generated_resolution is False
    assert bundle.generated_conflict_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_policy_execution_attempt_boundary_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_policy_execution_readiness().status)
