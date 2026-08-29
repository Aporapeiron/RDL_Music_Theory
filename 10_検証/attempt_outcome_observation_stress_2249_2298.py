"""policy execution attemptのoutcome observation境界を検査する最小実験。"""

from dataclasses import dataclass

from policy_execution_attempt_boundary_stress_2199_2248 import (
    PolicyExecutionAttempt,
    PolicyExecutionAttemptBundle,
    observe_policy_execution_attempt,
)


@dataclass(frozen=True)
class AttemptOutcomeObservationStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class AttemptOutcomeSignal:
    source_attempt: PolicyExecutionAttempt
    signal_kind: str
    observed_signal: str
    preserves_attempt_trace: bool
    preserves_conflict_trace: bool
    records_observation: bool
    commits_success_failure: bool
    resolves_conflict: bool
    status: str


@dataclass(frozen=True)
class AttemptOutcomeObservationBundle:
    source_bundle: PolicyExecutionAttemptBundle
    outcome_signals: tuple[AttemptOutcomeSignal, ...]
    deferred_outcome_signals: tuple[AttemptOutcomeSignal, ...]
    weight_outcome_signals: tuple[AttemptOutcomeSignal, ...]
    recheck_outcome_signals: tuple[AttemptOutcomeSignal, ...]
    stop_lines: tuple[str, ...]
    generated_outcome_observation: bool
    generated_resolution: bool
    generated_success_failure_verdict: bool
    generated_conflict_deletion: bool
    status: str


@dataclass(frozen=True)
class AttemptOutcomeObservation:
    source_status: str
    steps: tuple[AttemptOutcomeObservationStep, ...]
    bundle: AttemptOutcomeObservationBundle
    every_attempt_gets_outcome_signal: bool
    outcome_variety_preserved: bool
    attempt_and_conflict_traces_preserved: bool
    outcome_observed_without_resolution: bool
    no_success_failure_verdict: bool
    no_conflict_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2249, "source_reentry", "reuse_2199_2248_policy_execution_attempt", "policy_execution_attempt_preserved"),
    (2250, "source_reentry", "next_xi_received", "attempt_outcome_observation_stress_received"),
    (2251, "source_reentry", "execution_attempts_recheck", "execution_attempts_available"),
    (2252, "observation_request", "attempt_outcome_observation_request", "attempt_outcome_observation_candidate"),
    (2253, "observation_request", "outcome_observation_not_resolution_guard", "outcome_resolution_non_identity_preserved"),
    (2254, "observation_request", "outcome_observation_not_success_failure_guard", "success_failure_verdict_blocked"),
    (2255, "observation_request", "outcome_observation_not_conflict_deletion_guard", "conflict_deletion_blocked"),
    (2256, "outcome_signal_layer", "outcome_signal_generation", "outcome_signals_recorded"),
    (2257, "outcome_signal_layer", "deferred_context_probe_signal", "deferred_context_probe_signal_recorded"),
    (2258, "outcome_signal_layer", "hearing_rebalance_signal", "hearing_rebalance_signal_recorded"),
    (2259, "outcome_signal_layer", "reference_stability_signal", "reference_stability_signal_recorded"),
    (2260, "outcome_signal_layer", "records_observation_true", "records_observation_true_recorded"),
    (2261, "outcome_signal_layer", "commits_success_failure_false", "commits_success_failure_false_recorded"),
    (2262, "outcome_signal_layer", "resolves_conflict_false", "resolves_conflict_false_recorded"),
    (2263, "observation_content_layer", "later_context_signal_content", "later_context_signal_content_recorded"),
    (2264, "observation_content_layer", "hearing_priority_signal_content", "hearing_priority_signal_content_recorded"),
    (2265, "observation_content_layer", "reference_stability_signal_content", "reference_stability_signal_content_recorded"),
    (2266, "observation_content_layer", "attempt_trace_carry", "attempt_trace_carried"),
    (2267, "observation_content_layer", "conflict_trace_carry", "conflict_trace_carried"),
    (2268, "observation_content_layer", "readiness_trace_carry", "readiness_trace_carried"),
    (2269, "partition_layer", "deferred_outcome_signal_partition", "deferred_outcome_signal_partition_recorded"),
    (2270, "partition_layer", "weight_outcome_signal_partition", "weight_outcome_signal_partition_recorded"),
    (2271, "partition_layer", "recheck_outcome_signal_partition", "recheck_outcome_signal_partition_recorded"),
    (2272, "partition_layer", "outcome_signal_partition_not_verdict_guard", "partition_verdict_non_identity"),
    (2273, "partition_layer", "outcome_signal_partition_not_solution_guard", "partition_solution_non_identity"),
    (2274, "observation_view", "attempt_outcome_observation_view", "attempt_outcome_observation_view_created"),
    (2275, "observation_view", "deferred_outcome_signal_view", "deferred_outcome_signal_view_created"),
    (2276, "observation_view", "weight_outcome_signal_view", "weight_outcome_signal_view_created"),
    (2277, "observation_view", "recheck_outcome_signal_view", "recheck_outcome_signal_view_created"),
    (2278, "bundle", "attempt_outcome_observation_bundle_creation", "attempt_outcome_observation_bundle_created"),
    (2279, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2280, "bundle", "stop_lines_carry", "attempt_outcome_observation_stop_lines_carried"),
    (2281, "bundle", "generated_outcome_observation_true", "generated_outcome_observation_true_recorded"),
    (2282, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (2283, "bundle", "generated_success_failure_verdict_false", "generated_success_failure_verdict_false_recorded"),
    (2284, "bundle", "generated_conflict_deletion_false", "generated_conflict_deletion_false_recorded"),
    (2285, "integrity", "every_attempt_gets_outcome_signal_check", "every_attempt_gets_outcome_signal_confirmed"),
    (2286, "integrity", "outcome_variety_preservation_check", "outcome_variety_preservation_confirmed"),
    (2287, "integrity", "attempt_conflict_trace_check", "attempt_conflict_trace_confirmed"),
    (2288, "integrity", "outcome_observed_without_resolution_check", "outcome_observed_without_resolution_confirmed"),
    (2289, "integrity", "no_success_failure_verdict_check", "no_success_failure_verdict_confirmed"),
    (2290, "integrity", "no_conflict_deletion_check", "no_conflict_deletion_confirmed"),
    (2291, "non_identity", "outcome_observation_vs_resolution_split", "outcome_observation_resolution_non_identity"),
    (2292, "non_identity", "outcome_observation_vs_verdict_split", "outcome_observation_verdict_non_identity"),
    (2293, "non_identity", "signal_vs_solution_split", "signal_solution_non_identity"),
    (2294, "music_subject", "outcome_signal_as_heard_response", "heard_response_preserved"),
    (2295, "music_subject", "deferred_signal_as_contextual_hint", "contextual_hint_preserved"),
    (2296, "music_subject", "weight_signal_as_hearing_shift_hint", "hearing_shift_hint_preserved"),
    (2297, "summary", "attempt_outcome_observation_summary", "attempt_outcome_observation_observed"),
    (2298, "next_plan", "next_xi_selection", "xi_outcome_interpretation_boundary_stress"),
)


def _build_steps() -> tuple[AttemptOutcomeObservationStep, ...]:
    previous = "policy_execution_attempt_2199_2248"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            AttemptOutcomeObservationStep(
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


def _outcome_signal(attempt: PolicyExecutionAttempt) -> AttemptOutcomeSignal:
    if attempt.attempt_kind == "deferred_context_probe_attempt":
        kind = "deferred_context_probe_signal"
        signal = "later_context_hint_observed_without_resolution"
    elif attempt.attempt_kind == "weight_priority_adjustment_attempt":
        kind = "hearing_rebalance_signal"
        signal = "hearing_priority_shift_observed_without_verdict"
    else:
        kind = "reference_stability_signal"
        signal = "reference_stability_observed_without_deleting_alternatives"

    return AttemptOutcomeSignal(
        source_attempt=attempt,
        signal_kind=kind,
        observed_signal=signal,
        preserves_attempt_trace=True,
        preserves_conflict_trace=attempt.preserves_conflict_trace,
        records_observation=True,
        commits_success_failure=False,
        resolves_conflict=False,
        status="attempt_outcome_signal_recorded_without_verdict",
    )


def build_attempt_outcome_observation_bundle(
    source: PolicyExecutionAttemptBundle,
) -> AttemptOutcomeObservationBundle:
    signals = tuple(_outcome_signal(attempt) for attempt in source.attempts)
    deferred = tuple(signal for signal in signals if signal.signal_kind == "deferred_context_probe_signal")
    weight = tuple(signal for signal in signals if signal.signal_kind == "hearing_rebalance_signal")
    recheck = tuple(signal for signal in signals if signal.signal_kind == "reference_stability_signal")
    return AttemptOutcomeObservationBundle(
        source_bundle=source,
        outcome_signals=signals,
        deferred_outcome_signals=deferred,
        weight_outcome_signals=weight,
        recheck_outcome_signals=recheck,
        stop_lines=(
            "outcome_observation_not_resolution",
            "outcome_observation_not_success_failure_verdict",
            "outcome_observation_not_conflict_deletion",
            "outcome_signal_partition_not_verdict",
            "outcome_signal_partition_not_solution",
        ),
        generated_outcome_observation=True,
        generated_resolution=False,
        generated_success_failure_verdict=False,
        generated_conflict_deletion=False,
        status="attempt_outcome_observation_bundle_2249_2298_built_without_verdict",
    )


def observe_attempt_outcome_observation() -> AttemptOutcomeObservation:
    source = observe_policy_execution_attempt()
    bundle = build_attempt_outcome_observation_bundle(source.bundle)
    steps = _build_steps()

    return AttemptOutcomeObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        every_attempt_gets_outcome_signal=(
            len(bundle.outcome_signals) == len(source.bundle.attempts)
        ),
        outcome_variety_preserved=(
            len(bundle.deferred_outcome_signals) == 1
            and len(bundle.weight_outcome_signals) == 1
            and len(bundle.recheck_outcome_signals) == 1
        ),
        attempt_and_conflict_traces_preserved=all(
            signal.preserves_attempt_trace and signal.preserves_conflict_trace
            for signal in bundle.outcome_signals
        ),
        outcome_observed_without_resolution=(
            bundle.generated_outcome_observation is True
            and bundle.generated_resolution is False
            and all(signal.records_observation and not signal.resolves_conflict for signal in bundle.outcome_signals)
        ),
        no_success_failure_verdict=(
            bundle.generated_success_failure_verdict is False
            and all(not signal.commits_success_failure for signal in bundle.outcome_signals)
        ),
        no_conflict_deletion=(
            bundle.generated_conflict_deletion is False
            and all(not signal.source_attempt.source_readiness.source_route.deletes_conflict for signal in bundle.outcome_signals)
        ),
        generated_mutation=any(step.generated_mutation for step in steps),
        status="attempt_outcome_observation_2249_2298_observed_without_resolution_or_verdict",
    )


def run_checks() -> None:
    observation = observe_attempt_outcome_observation()
    bundle = observation.bundle

    assert observation.source_status == (
        "policy_execution_attempt_2199_2248_observed_without_resolution_or_outcome"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2249
    assert observation.steps[-1].number == 2298
    assert observation.every_attempt_gets_outcome_signal is True
    assert observation.outcome_variety_preserved is True
    assert observation.attempt_and_conflict_traces_preserved is True
    assert observation.outcome_observed_without_resolution is True
    assert observation.no_success_failure_verdict is True
    assert observation.no_conflict_deletion is True
    assert len(bundle.outcome_signals) == 3
    assert len(bundle.deferred_outcome_signals) == 1
    assert len(bundle.weight_outcome_signals) == 1
    assert len(bundle.recheck_outcome_signals) == 1
    assert bundle.generated_outcome_observation is True
    assert bundle.generated_resolution is False
    assert bundle.generated_success_failure_verdict is False
    assert bundle.generated_conflict_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_outcome_interpretation_boundary_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_attempt_outcome_observation().status)
