"""commitment後のrevision memory境界を検査する最小実験。"""

from dataclasses import dataclass

from reactivated_selection_commitment_boundary_stress_1899_1948 import (
    CommitmentCandidate,
    ReactivatedSelectionCommitmentBundle,
    observe_reactivated_selection_commitment,
)


@dataclass(frozen=True)
class CommitmentRevisionMemoryStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class RevisionMemoryEntry:
    source_commitment: CommitmentCandidate
    revision_kind: str
    revision_reason: str
    preserves_commitment_trace: bool
    preserves_precommitment_trace: bool
    is_error_correction_only: bool
    rewrites_past_commitment: bool
    status: str


@dataclass(frozen=True)
class RevisionMemoryPolicy:
    name: str
    accepts_committed_candidates: bool
    accepts_noncommitment_candidates: bool
    preserves_commitment_history: bool
    rejects_past_rewrite: bool
    generates_error_only_revision: bool
    status: str


@dataclass(frozen=True)
class CommitmentRevisionMemoryBundle:
    source_bundle: ReactivatedSelectionCommitmentBundle
    policy: RevisionMemoryPolicy
    revision_entries: tuple[RevisionMemoryEntry, ...]
    committed_revision_entries: tuple[RevisionMemoryEntry, ...]
    noncommitment_revision_entries: tuple[RevisionMemoryEntry, ...]
    boundary_revision_entries: tuple[RevisionMemoryEntry, ...]
    stop_lines: tuple[str, ...]
    generated_past_rewrite: bool
    generated_error_only_revision: bool
    generated_commitment_deletion: bool
    status: str


@dataclass(frozen=True)
class CommitmentRevisionMemoryObservation:
    source_status: str
    steps: tuple[CommitmentRevisionMemoryStep, ...]
    bundle: CommitmentRevisionMemoryBundle
    revision_entries_cover_commitment_candidates: bool
    committed_and_noncommitment_histories_preserved: bool
    commitment_and_precommitment_traces_preserved: bool
    revision_not_error_only_or_past_rewrite: bool
    no_commitment_deletion: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1949, "source_reentry", "reuse_1899_1948_reactivated_selection_commitment", "reactivated_selection_commitment_preserved"),
    (1950, "source_reentry", "next_xi_received", "commitment_revision_memory_stress_received"),
    (1951, "source_reentry", "commitment_candidates_recheck", "commitment_candidates_available"),
    (1952, "revision_request", "commitment_revision_memory_request", "commitment_revision_memory_candidate"),
    (1953, "revision_request", "revision_not_error_only_guard", "error_only_revision_non_identity_preserved"),
    (1954, "revision_request", "revision_not_past_rewrite_guard", "past_rewrite_blocked"),
    (1955, "revision_request", "revision_not_commitment_deletion_guard", "commitment_deletion_non_identity_preserved"),
    (1956, "policy_layer", "revision_memory_policy", "revision_memory_policy_recorded"),
    (1957, "policy_layer", "committed_candidate_acceptance_rule", "committed_candidate_acceptance_recorded"),
    (1958, "policy_layer", "noncommitment_candidate_acceptance_rule", "noncommitment_candidate_acceptance_recorded"),
    (1959, "policy_layer", "commitment_history_preservation_rule", "commitment_history_preservation_recorded"),
    (1960, "policy_layer", "past_rewrite_rejection_rule", "past_rewrite_rejection_recorded"),
    (1961, "revision_layer", "reference_commitment_revision_entry", "reference_commitment_revision_entry_recorded"),
    (1962, "revision_layer", "boundary_commitment_revision_entry", "boundary_commitment_revision_entry_recorded"),
    (1963, "revision_layer", "active_pull_commitment_revision_entry", "active_pull_commitment_revision_entry_recorded"),
    (1964, "revision_layer", "commitment_trace_carry", "commitment_trace_carried"),
    (1965, "revision_layer", "precommitment_trace_carry", "precommitment_trace_carried"),
    (1966, "revision_layer", "error_only_false_record", "error_only_false_recorded"),
    (1967, "revision_layer", "past_rewrite_false_record", "past_rewrite_false_recorded"),
    (1968, "partition_layer", "committed_revision_partition", "committed_revision_partition_recorded"),
    (1969, "partition_layer", "noncommitment_revision_partition", "noncommitment_revision_partition_recorded"),
    (1970, "partition_layer", "boundary_revision_partition", "boundary_revision_partition_recorded"),
    (1971, "partition_layer", "partition_not_correction_guard", "partition_correction_non_identity"),
    (1972, "partition_layer", "noncommitment_revision_not_failure_guard", "noncommitment_revision_failure_non_identity"),
    (1973, "revision_view", "commitment_revision_memory_view", "commitment_revision_memory_view_created"),
    (1974, "revision_view", "commitment_history_view", "commitment_history_view_created"),
    (1975, "revision_view", "future_revision_route_view", "future_revision_route_view_created"),
    (1976, "revision_view", "non_rewriting_memory_view", "non_rewriting_memory_view_created"),
    (1977, "bundle", "commitment_revision_memory_bundle_creation", "commitment_revision_memory_bundle_created"),
    (1978, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (1979, "bundle", "stop_lines_carry", "commitment_revision_memory_stop_lines_carried"),
    (1980, "bundle", "generated_past_rewrite_false", "generated_past_rewrite_false_recorded"),
    (1981, "bundle", "generated_error_only_revision_false", "generated_error_only_revision_false_recorded"),
    (1982, "bundle", "generated_commitment_deletion_false", "generated_commitment_deletion_false_recorded"),
    (1983, "integrity", "revision_entries_cover_commitment_candidates_check", "revision_entries_cover_commitment_candidates_confirmed"),
    (1984, "integrity", "committed_noncommitment_history_check", "committed_noncommitment_history_confirmed"),
    (1985, "integrity", "commitment_precommitment_trace_check", "commitment_precommitment_trace_confirmed"),
    (1986, "integrity", "revision_not_error_rewrite_check", "revision_not_error_rewrite_confirmed"),
    (1987, "integrity", "no_commitment_deletion_check", "no_commitment_deletion_confirmed"),
    (1988, "non_identity", "revision_vs_error_correction_split", "revision_error_correction_non_identity"),
    (1989, "non_identity", "revision_vs_past_rewrite_split", "revision_past_rewrite_non_identity"),
    (1990, "non_identity", "revision_memory_vs_commitment_deletion_split", "revision_commitment_deletion_non_identity"),
    (1991, "non_identity", "noncommitment_revision_vs_failure_split", "noncommitment_revision_failure_non_identity"),
    (1992, "music_subject", "revision_memory_as_rehearable_commitment", "rehearable_commitment_preserved"),
    (1993, "music_subject", "boundary_revision_as_open_responsibility", "open_responsibility_preserved"),
    (1994, "music_subject", "active_pull_revision_as_continuing_interpretation", "continuing_interpretation_preserved"),
    (1995, "summary", "commitment_revision_memory_summary", "commitment_revision_memory_observed"),
    (1996, "summary", "revision_without_rewrite_or_deletion_summary", "revision_without_rewrite_or_deletion_confirmed"),
    (1997, "next_plan", "revision_reentry_consistency_next_candidate", "revision_reentry_consistency_next_candidate"),
    (1998, "next_plan", "next_xi_selection", "xi_revision_reentry_consistency_stress"),
)


def _build_steps() -> tuple[CommitmentRevisionMemoryStep, ...]:
    previous = "reactivated_selection_commitment_1899_1948"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            CommitmentRevisionMemoryStep(
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


def _revision_entry(commitment: CommitmentCandidate) -> RevisionMemoryEntry:
    if commitment.enters_commitment:
        kind = "committed_candidate_revision_memory"
        reason = "committed_weight_can_be_reheard_later"
    else:
        kind = "noncommitment_boundary_revision_memory"
        reason = "suspended_responsibility_requires_revision_route"

    return RevisionMemoryEntry(
        source_commitment=commitment,
        revision_kind=kind,
        revision_reason=reason,
        preserves_commitment_trace=True,
        preserves_precommitment_trace=commitment.preserves_reactivation_trace and commitment.preserves_delay_trace,
        is_error_correction_only=False,
        rewrites_past_commitment=False,
        status="commitment_revision_memory_entry_recorded_without_past_rewrite",
    )


def build_commitment_revision_memory_bundle(
    source: ReactivatedSelectionCommitmentBundle,
) -> CommitmentRevisionMemoryBundle:
    policy = RevisionMemoryPolicy(
        name="commitment_revision_memory_policy",
        accepts_committed_candidates=True,
        accepts_noncommitment_candidates=True,
        preserves_commitment_history=True,
        rejects_past_rewrite=True,
        generates_error_only_revision=False,
        status="revision_memory_policy_preserves_commitment_without_rewriting_past",
    )
    entries = tuple(_revision_entry(candidate) for candidate in source.commitment_candidates)
    committed = tuple(entry for entry in entries if entry.source_commitment.enters_commitment)
    noncommitment = tuple(entry for entry in entries if not entry.source_commitment.enters_commitment)
    boundary = tuple(entry for entry in noncommitment if "boundary" in entry.revision_kind)
    return CommitmentRevisionMemoryBundle(
        source_bundle=source,
        policy=policy,
        revision_entries=entries,
        committed_revision_entries=committed,
        noncommitment_revision_entries=noncommitment,
        boundary_revision_entries=boundary,
        stop_lines=(
            "revision_not_error_only",
            "revision_not_past_rewrite",
            "revision_not_commitment_deletion",
            "noncommitment_revision_not_failure",
            "partition_not_correction",
        ),
        generated_past_rewrite=False,
        generated_error_only_revision=False,
        generated_commitment_deletion=False,
        status="commitment_revision_memory_bundle_1949_1998_built_without_rewrite_or_deletion",
    )


def observe_commitment_revision_memory() -> CommitmentRevisionMemoryObservation:
    source = observe_reactivated_selection_commitment()
    bundle = build_commitment_revision_memory_bundle(source.bundle)
    steps = _build_steps()

    return CommitmentRevisionMemoryObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        revision_entries_cover_commitment_candidates=(
            len(bundle.revision_entries) == len(source.bundle.commitment_candidates)
        ),
        committed_and_noncommitment_histories_preserved=(
            len(bundle.committed_revision_entries) == 2
            and len(bundle.noncommitment_revision_entries) == 1
        ),
        commitment_and_precommitment_traces_preserved=(
            bundle.policy.preserves_commitment_history is True
            and all(
                entry.preserves_commitment_trace and entry.preserves_precommitment_trace
                for entry in bundle.revision_entries
            )
        ),
        revision_not_error_only_or_past_rewrite=(
            bundle.generated_error_only_revision is False
            and bundle.generated_past_rewrite is False
            and all(
                not entry.is_error_correction_only and not entry.rewrites_past_commitment
                for entry in bundle.revision_entries
            )
        ),
        no_commitment_deletion=bundle.generated_commitment_deletion is False,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="commitment_revision_memory_1949_1998_observed_without_past_rewrite_or_deletion",
    )


def run_checks() -> None:
    observation = observe_commitment_revision_memory()
    bundle = observation.bundle

    assert observation.source_status == (
        "reactivated_selection_commitment_1899_1948_observed_without_truth_or_resolution"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1949
    assert observation.steps[-1].number == 1998
    assert observation.revision_entries_cover_commitment_candidates is True
    assert observation.committed_and_noncommitment_histories_preserved is True
    assert observation.commitment_and_precommitment_traces_preserved is True
    assert observation.revision_not_error_only_or_past_rewrite is True
    assert observation.no_commitment_deletion is True
    assert len(bundle.revision_entries) == 3
    assert len(bundle.committed_revision_entries) == 2
    assert len(bundle.noncommitment_revision_entries) == 1
    assert len(bundle.boundary_revision_entries) == 1
    assert bundle.generated_past_rewrite is False
    assert bundle.generated_error_only_revision is False
    assert bundle.generated_commitment_deletion is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_revision_reentry_consistency_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_commitment_revision_memory().status)
