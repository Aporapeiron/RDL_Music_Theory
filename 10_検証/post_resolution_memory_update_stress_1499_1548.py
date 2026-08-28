"""resolution return後のmemory updateを検査する最小実験。"""

from dataclasses import dataclass

from resolution_return_boundary_stress_1449_1498 import (
    ResolutionReturnBoundaryBundle,
    ResolutionReturnDecision,
    observe_resolution_return_boundary,
)


@dataclass(frozen=True)
class PostResolutionMemoryUpdateStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class PostResolutionMemoryEntry:
    source_decision: ResolutionReturnDecision
    update_kind: str
    memory_state_after_update: str
    keeps_pre_return_trace: bool
    keeps_future_route: bool
    marks_complete: bool
    deletes_deferred_trace: bool
    status: str


@dataclass(frozen=True)
class PostResolutionUpdatePolicy:
    name: str
    update_scope: str
    preserves_partial_history: bool
    preserves_transformation_history: bool
    preserves_redeferred_history: bool
    closes_memory_record: bool
    status: str


@dataclass(frozen=True)
class PostResolutionMemoryUpdateBundle:
    source_bundle: ResolutionReturnBoundaryBundle
    policy: PostResolutionUpdatePolicy
    updated_entries: tuple[PostResolutionMemoryEntry, ...]
    returned_memory: tuple[PostResolutionMemoryEntry, ...]
    redeferred_memory: tuple[PostResolutionMemoryEntry, ...]
    stop_lines: tuple[str, ...]
    generated_completion_record: bool
    generated_trace_deletion: bool
    generated_final_resolution: bool
    status: str


@dataclass(frozen=True)
class PostResolutionMemoryUpdateObservation:
    source_status: str
    steps: tuple[PostResolutionMemoryUpdateStep, ...]
    bundle: PostResolutionMemoryUpdateBundle
    update_preserves_return_history: bool
    partial_and_transformed_memory_retained: bool
    redeferred_memory_retained: bool
    update_not_completion_or_final_resolution: bool
    no_trace_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1499, "source_reentry", "reuse_1449_1498_resolution_return_boundary", "resolution_return_boundary_preserved"),
    (1500, "source_reentry", "next_xi_received", "post_resolution_memory_update_stress_received"),
    (1501, "source_reentry", "return_decisions_recheck", "return_decisions_available"),
    (1502, "update_request", "post_resolution_memory_update_request", "post_resolution_memory_update_candidate"),
    (1503, "update_request", "update_not_completion_guard", "completion_record_blocked"),
    (1504, "update_request", "update_not_trace_deletion_guard", "trace_deletion_non_identity"),
    (1505, "update_request", "update_not_final_resolution_guard", "final_resolution_non_identity"),
    (1506, "policy_layer", "post_resolution_update_policy", "post_resolution_update_policy_recorded"),
    (1507, "policy_layer", "partial_history_preservation_rule", "partial_history_preservation_rule_recorded"),
    (1508, "policy_layer", "transformation_history_preservation_rule", "transformation_history_preservation_rule_recorded"),
    (1509, "policy_layer", "redeferred_history_preservation_rule", "redeferred_history_preservation_rule_recorded"),
    (1510, "policy_layer", "memory_record_closure_false", "memory_record_closure_false_recorded"),
    (1511, "entry_layer", "primary_post_resolution_entry", "primary_post_resolution_entry_recorded"),
    (1512, "entry_layer", "derivative_post_resolution_entry", "derivative_post_resolution_entry_recorded"),
    (1513, "entry_layer", "latent_post_resolution_entry", "latent_post_resolution_entry_recorded"),
    (1514, "entry_layer", "pre_return_trace_carry", "pre_return_trace_carried"),
    (1515, "entry_layer", "future_route_carry", "future_route_carried"),
    (1516, "entry_layer", "complete_false_record", "complete_false_recorded"),
    (1517, "entry_layer", "trace_deletion_false_record", "trace_deletion_false_recorded"),
    (1518, "partition_layer", "returned_memory_partition", "returned_memory_partition_recorded"),
    (1519, "partition_layer", "redeferred_memory_partition", "redeferred_memory_partition_recorded"),
    (1520, "partition_layer", "partition_not_erasure_guard", "partition_erasure_non_identity"),
    (1521, "partition_layer", "returned_not_closed_guard", "returned_closed_non_identity"),
    (1522, "partition_layer", "redeferred_not_failure_guard", "redeferred_failure_non_identity"),
    (1523, "update_view", "post_resolution_update_view", "post_resolution_update_view_created"),
    (1524, "update_view", "history_retention_view", "history_retention_view_created"),
    (1525, "update_view", "future_route_retention_view", "future_route_retention_view_created"),
    (1526, "update_view", "non_closed_memory_record_view", "non_closed_memory_record_view_created"),
    (1527, "bundle", "post_resolution_memory_update_bundle_creation", "post_resolution_memory_update_bundle_created"),
    (1528, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1529, "bundle", "stop_lines_carry", "post_resolution_update_stop_lines_carried"),
    (1530, "bundle", "generated_completion_record_false", "generated_completion_record_false_recorded"),
    (1531, "bundle", "generated_trace_deletion_false", "generated_trace_deletion_false_recorded"),
    (1532, "bundle", "generated_final_resolution_false", "generated_final_resolution_false_recorded"),
    (1533, "integrity", "return_history_preservation_check", "return_history_preservation_confirmed"),
    (1534, "integrity", "partial_transformed_memory_check", "partial_transformed_memory_confirmed"),
    (1535, "integrity", "redeferred_memory_check", "redeferred_memory_confirmed"),
    (1536, "integrity", "completion_final_resolution_split_check", "completion_final_resolution_split_confirmed"),
    (1537, "integrity", "trace_deletion_split_check", "trace_deletion_split_confirmed"),
    (1538, "non_identity", "update_vs_completion_split", "update_completion_non_identity"),
    (1539, "non_identity", "memory_update_vs_final_resolution_split", "memory_update_final_resolution_non_identity"),
    (1540, "non_identity", "returned_memory_vs_closed_memory_split", "returned_closed_memory_non_identity"),
    (1541, "non_identity", "redeferred_memory_vs_failure_split", "redeferred_failure_non_identity_preserved"),
    (1542, "music_subject", "post_resolution_memory_as_afterimage", "post_resolution_afterimage_preserved"),
    (1543, "music_subject", "transformed_resolution_memory_as_new_expectation", "transformed_resolution_expectation_preserved"),
    (1544, "music_subject", "redeferred_memory_as_continuing_line", "redeferred_continuing_line_preserved"),
    (1545, "summary", "post_resolution_memory_update_summary", "post_resolution_memory_update_observed"),
    (1546, "summary", "no_completion_no_deletion_summary", "no_completion_no_deletion_confirmed"),
    (1547, "next_plan", "post_resolution_reentry_cycle_next_candidate", "post_resolution_reentry_cycle_next_candidate"),
    (1548, "next_plan", "next_xi_selection", "xi_post_resolution_reentry_cycle_stress"),
)


def _build_steps() -> tuple[PostResolutionMemoryUpdateStep, ...]:
    previous = "resolution_return_boundary_1449_1498"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            PostResolutionMemoryUpdateStep(
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


def _memory_entry(decision: ResolutionReturnDecision) -> PostResolutionMemoryEntry:
    if decision.return_event.resolves_pressure_partially:
        update_kind = "returned_resolution_memory_update"
        state = "post_return_transformed_memory"
    else:
        update_kind = "redeferred_resolution_memory_update"
        state = "post_return_redeferred_memory"
    return PostResolutionMemoryEntry(
        source_decision=decision,
        update_kind=update_kind,
        memory_state_after_update=state,
        keeps_pre_return_trace=True,
        keeps_future_route=decision.keeps_future_route,
        marks_complete=False,
        deletes_deferred_trace=False,
        status="post_resolution_memory_entry_updated_without_completion_or_trace_deletion",
    )


def build_post_resolution_memory_update_bundle(
    source: ResolutionReturnBoundaryBundle,
) -> PostResolutionMemoryUpdateBundle:
    policy = PostResolutionUpdatePolicy(
        name="post_resolution_memory_update_policy",
        update_scope="partial_transformed_and_redeferred_resolution_memory",
        preserves_partial_history=True,
        preserves_transformation_history=True,
        preserves_redeferred_history=True,
        closes_memory_record=False,
        status="post_resolution_update_policy_preserves_open_memory_history",
    )
    entries = tuple(_memory_entry(decision) for decision in source.decisions)
    returned = tuple(entry for entry in entries if "returned" in entry.update_kind)
    redeferred = tuple(entry for entry in entries if "redeferred" in entry.update_kind)
    return PostResolutionMemoryUpdateBundle(
        source_bundle=source,
        policy=policy,
        updated_entries=entries,
        returned_memory=returned,
        redeferred_memory=redeferred,
        stop_lines=(
            "update_not_completion",
            "update_not_trace_deletion",
            "update_not_final_resolution",
            "returned_not_closed",
            "redeferred_not_failure",
        ),
        generated_completion_record=False,
        generated_trace_deletion=False,
        generated_final_resolution=False,
        status="post_resolution_memory_update_bundle_1499_1548_built_without_completion_or_trace_deletion",
    )


def observe_post_resolution_memory_update() -> PostResolutionMemoryUpdateObservation:
    source = observe_resolution_return_boundary()
    bundle = build_post_resolution_memory_update_bundle(source.bundle)
    steps = _build_steps()

    return PostResolutionMemoryUpdateObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        update_preserves_return_history=(
            len(bundle.updated_entries) == 3
            and all(entry.keeps_pre_return_trace for entry in bundle.updated_entries)
        ),
        partial_and_transformed_memory_retained=(
            len(bundle.returned_memory) == 2
            and all(entry.keeps_future_route for entry in bundle.returned_memory)
        ),
        redeferred_memory_retained=(
            len(bundle.redeferred_memory) == 1
            and bundle.redeferred_memory[0].keeps_future_route is True
        ),
        update_not_completion_or_final_resolution=(
            bundle.policy.closes_memory_record is False
            and bundle.generated_completion_record is False
            and bundle.generated_final_resolution is False
            and all(entry.marks_complete is False for entry in bundle.updated_entries)
        ),
        no_trace_deletion=(
            bundle.generated_trace_deletion is False
            and all(entry.deletes_deferred_trace is False for entry in bundle.updated_entries)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="post_resolution_memory_update_1499_1548_observed_without_completion_or_trace_deletion",
    )


def run_checks() -> None:
    observation = observe_post_resolution_memory_update()
    bundle = observation.bundle

    assert observation.source_status == (
        "resolution_return_boundary_1449_1498_observed_without_final_solve_or_closure"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1499
    assert observation.steps[-1].number == 1548
    assert observation.update_preserves_return_history is True
    assert observation.partial_and_transformed_memory_retained is True
    assert observation.redeferred_memory_retained is True
    assert observation.update_not_completion_or_final_resolution is True
    assert observation.no_trace_deletion is True
    assert len(bundle.updated_entries) == 3
    assert len(bundle.returned_memory) == 2
    assert len(bundle.redeferred_memory) == 1
    assert bundle.generated_completion_record is False
    assert bundle.generated_trace_deletion is False
    assert bundle.generated_final_resolution is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_post_resolution_reentry_cycle_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_post_resolution_memory_update().status)
