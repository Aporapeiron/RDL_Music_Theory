"""reactivated selectionのcommitment境界を検査する最小実験。"""

from dataclasses import dataclass

from delayed_selection_reactivation_stress_1849_1898 import (
    DelayedSelectionReactivationBundle,
    ReactivatedSelectionCandidate,
    observe_delayed_selection_reactivation,
)


@dataclass(frozen=True)
class ReactivatedSelectionCommitmentStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class CommitmentCandidate:
    source_reactivation: ReactivatedSelectionCandidate
    commitment_kind: str
    commitment_reason: str
    preserves_reactivation_trace: bool
    preserves_delay_trace: bool
    enters_commitment: bool
    becomes_final_truth: bool
    becomes_resolution: bool
    status: str


@dataclass(frozen=True)
class CommitmentBoundaryPolicy:
    name: str
    permits_commitment_after_reactivation: bool
    permits_noncommitment_retention: bool
    preserves_precommitment_trace: bool
    rejects_final_truth_collapse: bool
    rejects_resolution_collapse: bool
    status: str


@dataclass(frozen=True)
class ReactivatedSelectionCommitmentBundle:
    source_bundle: DelayedSelectionReactivationBundle
    policy: CommitmentBoundaryPolicy
    commitment_candidates: tuple[CommitmentCandidate, ...]
    committed_candidates: tuple[CommitmentCandidate, ...]
    retained_noncommitment_candidates: tuple[CommitmentCandidate, ...]
    boundary_commitment_candidates: tuple[CommitmentCandidate, ...]
    stop_lines: tuple[str, ...]
    generated_final_truth: bool
    generated_resolution: bool
    generated_irreversible_fixation: bool
    status: str


@dataclass(frozen=True)
class ReactivatedSelectionCommitmentObservation:
    source_status: str
    steps: tuple[ReactivatedSelectionCommitmentStep, ...]
    bundle: ReactivatedSelectionCommitmentBundle
    reactivated_candidates_cover_commitment_candidates: bool
    committed_and_retained_paths_preserved: bool
    precommitment_traces_preserved: bool
    commitment_not_truth_or_resolution: bool
    no_irreversible_fixation: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1899, "source_reentry", "reuse_1849_1898_delayed_selection_reactivation", "delayed_selection_reactivation_preserved"),
    (1900, "source_reentry", "next_xi_received", "reactivated_selection_commitment_boundary_stress_received"),
    (1901, "source_reentry", "reactivated_candidates_recheck", "reactivated_candidates_available"),
    (1902, "commitment_request", "reactivated_selection_commitment_request", "reactivated_selection_commitment_candidate"),
    (1903, "commitment_request", "commitment_not_final_truth_guard", "final_truth_non_identity_preserved"),
    (1904, "commitment_request", "commitment_not_resolution_guard", "resolution_non_identity_preserved"),
    (1905, "commitment_request", "commitment_not_irreversible_fixation_guard", "irreversible_fixation_blocked"),
    (1906, "policy_layer", "commitment_boundary_policy", "commitment_boundary_policy_recorded"),
    (1907, "policy_layer", "commitment_after_reactivation_permission", "commitment_after_reactivation_permission_recorded"),
    (1908, "policy_layer", "noncommitment_retention_permission", "noncommitment_retention_permission_recorded"),
    (1909, "policy_layer", "precommitment_trace_preservation_rule", "precommitment_trace_preservation_recorded"),
    (1910, "policy_layer", "truth_resolution_collapse_rejection_rule", "truth_resolution_collapse_rejection_recorded"),
    (1911, "commitment_layer", "weak_reference_commitment_candidate", "weak_reference_commitment_candidate_recorded"),
    (1912, "commitment_layer", "medium_reopened_reading_boundary_candidate", "medium_reopened_reading_boundary_recorded"),
    (1913, "commitment_layer", "strong_active_pull_commitment_candidate", "strong_active_pull_commitment_recorded"),
    (1914, "commitment_layer", "reactivation_trace_carry", "reactivation_trace_carried"),
    (1915, "commitment_layer", "delay_trace_carry", "delay_trace_carried"),
    (1916, "commitment_layer", "final_truth_false_record", "final_truth_false_recorded"),
    (1917, "commitment_layer", "resolution_false_record", "resolution_false_recorded"),
    (1918, "partition_layer", "committed_candidate_partition", "committed_candidate_partition_recorded"),
    (1919, "partition_layer", "retained_noncommitment_partition", "retained_noncommitment_partition_recorded"),
    (1920, "partition_layer", "boundary_commitment_partition", "boundary_commitment_partition_recorded"),
    (1921, "partition_layer", "partition_not_final_ranking_guard", "partition_final_ranking_non_identity"),
    (1922, "partition_layer", "retained_noncommitment_not_failure_guard", "retained_noncommitment_failure_non_identity"),
    (1923, "commitment_view", "reactivated_commitment_view", "reactivated_commitment_view_created"),
    (1924, "commitment_view", "precommitment_trace_view", "precommitment_trace_view_created"),
    (1925, "commitment_view", "committed_candidate_view", "committed_candidate_view_created"),
    (1926, "commitment_view", "noncommitment_retention_view", "noncommitment_retention_view_created"),
    (1927, "bundle", "reactivated_selection_commitment_bundle_creation", "reactivated_selection_commitment_bundle_created"),
    (1928, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1929, "bundle", "stop_lines_carry", "reactivated_commitment_stop_lines_carried"),
    (1930, "bundle", "generated_final_truth_false", "generated_final_truth_false_recorded"),
    (1931, "bundle", "generated_resolution_false", "generated_resolution_false_recorded"),
    (1932, "bundle", "generated_irreversible_fixation_false", "generated_irreversible_fixation_false_recorded"),
    (1933, "integrity", "reactivated_candidates_cover_commitment_candidates_check", "reactivated_candidates_cover_commitment_candidates_confirmed"),
    (1934, "integrity", "committed_retained_paths_check", "committed_retained_paths_confirmed"),
    (1935, "integrity", "precommitment_trace_preservation_check", "precommitment_trace_preservation_confirmed"),
    (1936, "integrity", "commitment_not_truth_resolution_check", "commitment_not_truth_resolution_confirmed"),
    (1937, "integrity", "no_irreversible_fixation_check", "no_irreversible_fixation_confirmed"),
    (1938, "non_identity", "commitment_vs_final_truth_split", "commitment_final_truth_non_identity"),
    (1939, "non_identity", "commitment_vs_resolution_split", "commitment_resolution_non_identity"),
    (1940, "non_identity", "commitment_vs_irreversible_fixation_split", "commitment_irreversible_fixation_non_identity"),
    (1941, "non_identity", "noncommitment_retention_vs_failure_split", "noncommitment_retention_failure_non_identity"),
    (1942, "music_subject", "commitment_as_interpretive_weight", "interpretive_weight_preserved"),
    (1943, "music_subject", "boundary_commitment_as_suspended_responsibility", "suspended_responsibility_preserved"),
    (1944, "music_subject", "strong_commitment_as_active_musical_reading", "active_musical_reading_preserved"),
    (1945, "summary", "reactivated_selection_commitment_summary", "reactivated_selection_commitment_observed"),
    (1946, "summary", "commitment_without_truth_resolution_summary", "commitment_without_truth_resolution_confirmed"),
    (1947, "next_plan", "commitment_revision_memory_next_candidate", "commitment_revision_memory_next_candidate"),
    (1948, "next_plan", "next_xi_selection", "xi_commitment_revision_memory_stress"),
)


def _build_steps() -> tuple[ReactivatedSelectionCommitmentStep, ...]:
    previous = "delayed_selection_reactivation_1849_1898"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            ReactivatedSelectionCommitmentStep(
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


def _commitment_candidate(
    reactivation: ReactivatedSelectionCandidate,
) -> CommitmentCandidate:
    if reactivation.selects_now:
        kind = "reference_commitment_candidate"
        reason = "stable_reference_can_receive_interpretive_weight"
        enters_commitment = True
    elif "ambiguous" in reactivation.reactivation_kind:
        kind = "boundary_commitment_candidate"
        reason = "reopened_reading_needs_suspended_responsibility"
        enters_commitment = False
    else:
        kind = "active_pull_commitment_candidate"
        reason = "strong_reactivation_can_receive_provisional_weight"
        enters_commitment = True

    return CommitmentCandidate(
        source_reactivation=reactivation,
        commitment_kind=kind,
        commitment_reason=reason,
        preserves_reactivation_trace=True,
        preserves_delay_trace=reactivation.preserves_delay_trace,
        enters_commitment=enters_commitment,
        becomes_final_truth=False,
        becomes_resolution=False,
        status="reactivated_selection_commitment_candidate_recorded_without_truth_or_resolution",
    )


def build_reactivated_selection_commitment_bundle(
    source: DelayedSelectionReactivationBundle,
) -> ReactivatedSelectionCommitmentBundle:
    policy = CommitmentBoundaryPolicy(
        name="reactivated_selection_commitment_boundary_policy",
        permits_commitment_after_reactivation=True,
        permits_noncommitment_retention=True,
        preserves_precommitment_trace=True,
        rejects_final_truth_collapse=True,
        rejects_resolution_collapse=True,
        status="commitment_boundary_policy_preserves_weight_without_finality",
    )
    candidates = tuple(
        _commitment_candidate(reactivation)
        for reactivation in source.reactivated_candidates
    )
    committed = tuple(candidate for candidate in candidates if candidate.enters_commitment)
    retained = tuple(candidate for candidate in candidates if not candidate.enters_commitment)
    boundary = tuple(candidate for candidate in retained if "boundary" in candidate.commitment_kind)
    return ReactivatedSelectionCommitmentBundle(
        source_bundle=source,
        policy=policy,
        commitment_candidates=candidates,
        committed_candidates=committed,
        retained_noncommitment_candidates=retained,
        boundary_commitment_candidates=boundary,
        stop_lines=(
            "commitment_not_final_truth",
            "commitment_not_resolution",
            "commitment_not_irreversible_fixation",
            "retained_noncommitment_not_failure",
            "partition_not_final_ranking",
        ),
        generated_final_truth=False,
        generated_resolution=False,
        generated_irreversible_fixation=False,
        status="reactivated_selection_commitment_bundle_1899_1948_built_without_truth_or_resolution",
    )


def observe_reactivated_selection_commitment() -> ReactivatedSelectionCommitmentObservation:
    source = observe_delayed_selection_reactivation()
    bundle = build_reactivated_selection_commitment_bundle(source.bundle)
    steps = _build_steps()

    return ReactivatedSelectionCommitmentObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        reactivated_candidates_cover_commitment_candidates=(
            len(bundle.commitment_candidates) == len(source.bundle.reactivated_candidates)
        ),
        committed_and_retained_paths_preserved=(
            len(bundle.committed_candidates) == 2
            and len(bundle.retained_noncommitment_candidates) == 1
        ),
        precommitment_traces_preserved=(
            bundle.policy.preserves_precommitment_trace is True
            and all(
                candidate.preserves_reactivation_trace and candidate.preserves_delay_trace
                for candidate in bundle.commitment_candidates
            )
        ),
        commitment_not_truth_or_resolution=(
            bundle.generated_final_truth is False
            and bundle.generated_resolution is False
            and all(
                not candidate.becomes_final_truth and not candidate.becomes_resolution
                for candidate in bundle.commitment_candidates
            )
        ),
        no_irreversible_fixation=bundle.generated_irreversible_fixation is False,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="reactivated_selection_commitment_1899_1948_observed_without_truth_or_resolution",
    )


def run_checks() -> None:
    observation = observe_reactivated_selection_commitment()
    bundle = observation.bundle

    assert observation.source_status == (
        "delayed_selection_reactivation_1849_1898_observed_without_adoption_or_delay_clearance"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1899
    assert observation.steps[-1].number == 1948
    assert observation.reactivated_candidates_cover_commitment_candidates is True
    assert observation.committed_and_retained_paths_preserved is True
    assert observation.precommitment_traces_preserved is True
    assert observation.commitment_not_truth_or_resolution is True
    assert observation.no_irreversible_fixation is True
    assert len(bundle.commitment_candidates) == 3
    assert len(bundle.committed_candidates) == 2
    assert len(bundle.retained_noncommitment_candidates) == 1
    assert len(bundle.boundary_commitment_candidates) == 1
    assert bundle.generated_final_truth is False
    assert bundle.generated_resolution is False
    assert bundle.generated_irreversible_fixation is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_commitment_revision_memory_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_reactivated_selection_commitment().status)
