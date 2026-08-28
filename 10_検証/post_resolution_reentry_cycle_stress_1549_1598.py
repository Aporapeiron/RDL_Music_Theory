"""post-resolution memory update後のreentry cycleを検査する最小実験。"""

from dataclasses import dataclass

from post_resolution_memory_update_stress_1499_1548 import (
    PostResolutionMemoryEntry,
    PostResolutionMemoryUpdateBundle,
    observe_post_resolution_memory_update,
)


@dataclass(frozen=True)
class PostResolutionReentryCycleStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class PostResolutionReentryCandidate:
    source_entry: PostResolutionMemoryEntry
    reentry_kind: str
    cycle_position: str
    keeps_return_history: bool
    keeps_future_route: bool
    creates_new_final_answer: bool
    closes_cycle: bool
    status: str


@dataclass(frozen=True)
class PostResolutionReentryPolicy:
    name: str
    accepts_returned_memory: bool
    accepts_redeferred_memory: bool
    preserves_memory_trace: bool
    permits_reentry_without_closure: bool
    generates_completion: bool
    status: str


@dataclass(frozen=True)
class PostResolutionReentryCycleBundle:
    source_bundle: PostResolutionMemoryUpdateBundle
    policy: PostResolutionReentryPolicy
    candidates: tuple[PostResolutionReentryCandidate, ...]
    returned_reentries: tuple[PostResolutionReentryCandidate, ...]
    redeferred_reentries: tuple[PostResolutionReentryCandidate, ...]
    stop_lines: tuple[str, ...]
    generated_cycle_closure: bool
    generated_final_answer: bool
    generated_trace_erasure: bool
    status: str


@dataclass(frozen=True)
class PostResolutionReentryCycleObservation:
    source_status: str
    steps: tuple[PostResolutionReentryCycleStep, ...]
    bundle: PostResolutionReentryCycleBundle
    all_memory_entries_reenterable: bool
    returned_and_redeferred_paths_preserved: bool
    reentry_keeps_memory_trace: bool
    reentry_without_cycle_closure: bool
    no_final_answer_or_trace_erasure: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1549, "source_reentry", "reuse_1499_1548_post_resolution_memory_update", "post_resolution_memory_update_preserved"),
    (1550, "source_reentry", "next_xi_received", "post_resolution_reentry_cycle_stress_received"),
    (1551, "source_reentry", "updated_memory_entries_recheck", "updated_memory_entries_available"),
    (1552, "reentry_request", "post_resolution_reentry_request", "post_resolution_reentry_candidate"),
    (1553, "reentry_request", "reentry_not_completion_guard", "completion_non_identity_preserved"),
    (1554, "reentry_request", "reentry_not_final_answer_guard", "final_answer_non_identity_preserved"),
    (1555, "reentry_request", "reentry_not_trace_erasure_guard", "trace_erasure_non_identity_preserved"),
    (1556, "policy_layer", "post_resolution_reentry_policy", "post_resolution_reentry_policy_recorded"),
    (1557, "policy_layer", "returned_memory_acceptance_rule", "returned_memory_acceptance_recorded"),
    (1558, "policy_layer", "redeferred_memory_acceptance_rule", "redeferred_memory_acceptance_recorded"),
    (1559, "policy_layer", "memory_trace_preservation_rule", "memory_trace_preservation_recorded"),
    (1560, "policy_layer", "cycle_closure_false_rule", "cycle_closure_false_recorded"),
    (1561, "candidate_layer", "primary_returned_reentry_candidate", "primary_returned_reentry_recorded"),
    (1562, "candidate_layer", "derivative_returned_reentry_candidate", "derivative_returned_reentry_recorded"),
    (1563, "candidate_layer", "latent_redeferred_reentry_candidate", "latent_redeferred_reentry_recorded"),
    (1564, "candidate_layer", "return_history_carry", "return_history_carried"),
    (1565, "candidate_layer", "future_route_carry", "future_route_carried"),
    (1566, "candidate_layer", "final_answer_false_record", "final_answer_false_recorded"),
    (1567, "candidate_layer", "cycle_closure_false_record", "cycle_closure_false_recorded"),
    (1568, "cycle_partition", "returned_reentry_partition", "returned_reentry_partition_recorded"),
    (1569, "cycle_partition", "redeferred_reentry_partition", "redeferred_reentry_partition_recorded"),
    (1570, "cycle_partition", "partition_not_selection_guard", "partition_selection_non_identity"),
    (1571, "cycle_partition", "returned_not_resolved_guard", "returned_resolved_non_identity"),
    (1572, "cycle_partition", "redeferred_not_failed_guard", "redeferred_failed_non_identity"),
    (1573, "cycle_view", "post_resolution_reentry_view", "post_resolution_reentry_view_created"),
    (1574, "cycle_view", "memory_trace_reentry_view", "memory_trace_reentry_view_created"),
    (1575, "cycle_view", "future_route_reentry_view", "future_route_reentry_view_created"),
    (1576, "cycle_view", "open_cycle_view", "open_cycle_view_created"),
    (1577, "bundle", "post_resolution_reentry_cycle_bundle_creation", "post_resolution_reentry_cycle_bundle_created"),
    (1578, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1579, "bundle", "stop_lines_carry", "post_resolution_reentry_stop_lines_carried"),
    (1580, "bundle", "generated_cycle_closure_false", "generated_cycle_closure_false_recorded"),
    (1581, "bundle", "generated_final_answer_false", "generated_final_answer_false_recorded"),
    (1582, "bundle", "generated_trace_erasure_false", "generated_trace_erasure_false_recorded"),
    (1583, "integrity", "all_memory_entries_reenterable_check", "all_memory_entries_reenterable_confirmed"),
    (1584, "integrity", "returned_redeferred_path_preservation_check", "returned_redeferred_path_preservation_confirmed"),
    (1585, "integrity", "memory_trace_preservation_check", "memory_trace_preservation_confirmed"),
    (1586, "integrity", "open_cycle_check", "open_cycle_confirmed"),
    (1587, "integrity", "no_final_answer_trace_erasure_check", "no_final_answer_trace_erasure_confirmed"),
    (1588, "non_identity", "reentry_vs_completion_split", "reentry_completion_non_identity"),
    (1589, "non_identity", "reentry_vs_final_answer_split", "reentry_final_answer_non_identity"),
    (1590, "non_identity", "cycle_vs_closure_split", "cycle_closure_non_identity"),
    (1591, "non_identity", "redeferred_reentry_vs_failure_split", "redeferred_reentry_failure_non_identity"),
    (1592, "music_subject", "returned_memory_as_new_listening_entry", "returned_memory_new_listening_entry_preserved"),
    (1593, "music_subject", "transformed_memory_as_reheard_expectation", "transformed_memory_reheard_expectation_preserved"),
    (1594, "music_subject", "redeferred_memory_as_unfinished_continuation", "redeferred_memory_unfinished_continuation_preserved"),
    (1595, "summary", "post_resolution_reentry_cycle_summary", "post_resolution_reentry_cycle_observed"),
    (1596, "summary", "open_reentry_no_closure_summary", "open_reentry_no_closure_confirmed"),
    (1597, "next_plan", "iterated_reentry_memory_drift_next_candidate", "iterated_reentry_memory_drift_next_candidate"),
    (1598, "next_plan", "next_xi_selection", "xi_iterated_reentry_memory_drift_stress"),
)


def _build_steps() -> tuple[PostResolutionReentryCycleStep, ...]:
    previous = "post_resolution_memory_update_1499_1548"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            PostResolutionReentryCycleStep(
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


def _reentry_candidate(entry: PostResolutionMemoryEntry) -> PostResolutionReentryCandidate:
    if entry.update_kind == "returned_resolution_memory_update":
        reentry_kind = "returned_memory_reentry_candidate"
        cycle_position = "reheard_post_return_entry"
    else:
        reentry_kind = "redeferred_memory_reentry_candidate"
        cycle_position = "unfinished_post_return_entry"

    return PostResolutionReentryCandidate(
        source_entry=entry,
        reentry_kind=reentry_kind,
        cycle_position=cycle_position,
        keeps_return_history=entry.keeps_pre_return_trace,
        keeps_future_route=entry.keeps_future_route,
        creates_new_final_answer=False,
        closes_cycle=False,
        status="post_resolution_memory_reentry_candidate_recorded_without_closure",
    )


def build_post_resolution_reentry_cycle_bundle(
    source: PostResolutionMemoryUpdateBundle,
) -> PostResolutionReentryCycleBundle:
    policy = PostResolutionReentryPolicy(
        name="post_resolution_reentry_cycle_policy",
        accepts_returned_memory=True,
        accepts_redeferred_memory=True,
        preserves_memory_trace=True,
        permits_reentry_without_closure=True,
        generates_completion=False,
        status="post_resolution_reentry_policy_keeps_open_cycle",
    )
    candidates = tuple(_reentry_candidate(entry) for entry in source.updated_entries)
    returned = tuple(candidate for candidate in candidates if "returned" in candidate.reentry_kind)
    redeferred = tuple(candidate for candidate in candidates if "redeferred" in candidate.reentry_kind)
    return PostResolutionReentryCycleBundle(
        source_bundle=source,
        policy=policy,
        candidates=candidates,
        returned_reentries=returned,
        redeferred_reentries=redeferred,
        stop_lines=(
            "reentry_not_completion",
            "reentry_not_final_answer",
            "reentry_not_trace_erasure",
            "cycle_not_closure",
            "redeferred_reentry_not_failure",
        ),
        generated_cycle_closure=False,
        generated_final_answer=False,
        generated_trace_erasure=False,
        status="post_resolution_reentry_cycle_bundle_1549_1598_built_without_closure",
    )


def observe_post_resolution_reentry_cycle() -> PostResolutionReentryCycleObservation:
    source = observe_post_resolution_memory_update()
    bundle = build_post_resolution_reentry_cycle_bundle(source.bundle)
    steps = _build_steps()

    return PostResolutionReentryCycleObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        all_memory_entries_reenterable=(
            len(bundle.candidates) == len(source.bundle.updated_entries)
            and all(candidate.keeps_future_route for candidate in bundle.candidates)
        ),
        returned_and_redeferred_paths_preserved=(
            len(bundle.returned_reentries) == 2 and len(bundle.redeferred_reentries) == 1
        ),
        reentry_keeps_memory_trace=(
            bundle.policy.preserves_memory_trace is True
            and all(candidate.keeps_return_history for candidate in bundle.candidates)
        ),
        reentry_without_cycle_closure=(
            bundle.policy.permits_reentry_without_closure is True
            and bundle.generated_cycle_closure is False
            and all(candidate.closes_cycle is False for candidate in bundle.candidates)
        ),
        no_final_answer_or_trace_erasure=(
            bundle.generated_final_answer is False
            and bundle.generated_trace_erasure is False
            and all(candidate.creates_new_final_answer is False for candidate in bundle.candidates)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="post_resolution_reentry_cycle_1549_1598_observed_without_closure_or_final_answer",
    )


def run_checks() -> None:
    observation = observe_post_resolution_reentry_cycle()
    bundle = observation.bundle

    assert observation.source_status == (
        "post_resolution_memory_update_1499_1548_observed_without_completion_or_trace_deletion"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1549
    assert observation.steps[-1].number == 1598
    assert observation.all_memory_entries_reenterable is True
    assert observation.returned_and_redeferred_paths_preserved is True
    assert observation.reentry_keeps_memory_trace is True
    assert observation.reentry_without_cycle_closure is True
    assert observation.no_final_answer_or_trace_erasure is True
    assert len(bundle.candidates) == 3
    assert len(bundle.returned_reentries) == 2
    assert len(bundle.redeferred_reentries) == 1
    assert bundle.generated_cycle_closure is False
    assert bundle.generated_final_answer is False
    assert bundle.generated_trace_erasure is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_iterated_reentry_memory_drift_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_post_resolution_reentry_cycle().status)
