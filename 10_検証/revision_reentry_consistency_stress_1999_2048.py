"""revision memory再入時のconsistency境界を検査する最小実験。"""

from dataclasses import dataclass

from commitment_revision_memory_stress_1949_1998 import (
    CommitmentRevisionMemoryBundle,
    RevisionMemoryEntry,
    observe_commitment_revision_memory,
)


@dataclass(frozen=True)
class RevisionReentryConsistencyStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class RevisionReentryLink:
    source_revision: RevisionMemoryEntry
    link_kind: str
    consistency_relation: str
    preserves_revision_trace: bool
    preserves_commitment_trace: bool
    rewrites_original_commitment: bool
    forces_consistency_by_deletion: bool
    status: str


@dataclass(frozen=True)
class RevisionReentryConsistencyPolicy:
    name: str
    accepts_revision_reentry: bool
    preserves_original_commitment: bool
    permits_nonidentical_consistency: bool
    rejects_deletion_based_consistency: bool
    generates_history_rewrite: bool
    status: str


@dataclass(frozen=True)
class RevisionReentryConsistencyBundle:
    source_bundle: CommitmentRevisionMemoryBundle
    policy: RevisionReentryConsistencyPolicy
    consistency_links: tuple[RevisionReentryLink, ...]
    committed_consistency_links: tuple[RevisionReentryLink, ...]
    boundary_consistency_links: tuple[RevisionReentryLink, ...]
    stop_lines: tuple[str, ...]
    generated_history_rewrite: bool
    generated_deletion_based_consistency: bool
    generated_commitment_overwrite: bool
    status: str


@dataclass(frozen=True)
class RevisionReentryConsistencyObservation:
    source_status: str
    steps: tuple[RevisionReentryConsistencyStep, ...]
    bundle: RevisionReentryConsistencyBundle
    revision_entries_reentered_as_links: bool
    committed_and_boundary_links_preserved: bool
    revision_and_commitment_traces_preserved: bool
    consistency_without_rewrite_or_deletion: bool
    original_commitment_not_overwritten: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (1999, "source_reentry", "reuse_1949_1998_commitment_revision_memory", "commitment_revision_memory_preserved"),
    (2000, "source_reentry", "next_xi_received", "revision_reentry_consistency_stress_received"),
    (2001, "source_reentry", "revision_entries_recheck", "revision_entries_available"),
    (2002, "consistency_request", "revision_reentry_consistency_request", "revision_reentry_consistency_candidate"),
    (2003, "consistency_request", "consistency_not_history_rewrite_guard", "history_rewrite_non_identity_preserved"),
    (2004, "consistency_request", "consistency_not_deletion_guard", "deletion_based_consistency_blocked"),
    (2005, "consistency_request", "consistency_not_commitment_overwrite_guard", "commitment_overwrite_non_identity_preserved"),
    (2006, "policy_layer", "revision_reentry_consistency_policy", "revision_reentry_consistency_policy_recorded"),
    (2007, "policy_layer", "revision_reentry_acceptance_rule", "revision_reentry_acceptance_recorded"),
    (2008, "policy_layer", "original_commitment_preservation_rule", "original_commitment_preservation_recorded"),
    (2009, "policy_layer", "nonidentical_consistency_permission", "nonidentical_consistency_permission_recorded"),
    (2010, "policy_layer", "deletion_based_consistency_rejection_rule", "deletion_based_consistency_rejection_recorded"),
    (2011, "link_layer", "reference_revision_consistency_link", "reference_revision_consistency_link_recorded"),
    (2012, "link_layer", "boundary_revision_consistency_link", "boundary_revision_consistency_link_recorded"),
    (2013, "link_layer", "active_pull_revision_consistency_link", "active_pull_revision_consistency_link_recorded"),
    (2014, "link_layer", "revision_trace_carry", "revision_trace_carried"),
    (2015, "link_layer", "commitment_trace_carry", "commitment_trace_carried"),
    (2016, "link_layer", "history_rewrite_false_record", "history_rewrite_false_recorded"),
    (2017, "link_layer", "commitment_overwrite_false_record", "commitment_overwrite_false_recorded"),
    (2018, "partition_layer", "committed_consistency_partition", "committed_consistency_partition_recorded"),
    (2019, "partition_layer", "boundary_consistency_partition", "boundary_consistency_partition_recorded"),
    (2020, "partition_layer", "consistency_link_partition", "consistency_link_partition_recorded"),
    (2021, "partition_layer", "partition_not_correction_guard", "partition_correction_non_identity"),
    (2022, "partition_layer", "boundary_link_not_failure_guard", "boundary_link_failure_non_identity"),
    (2023, "consistency_view", "revision_reentry_consistency_view", "revision_reentry_consistency_view_created"),
    (2024, "consistency_view", "original_commitment_view", "original_commitment_view_created"),
    (2025, "consistency_view", "nonidentical_consistency_view", "nonidentical_consistency_view_created"),
    (2026, "consistency_view", "trace_preservation_view", "trace_preservation_view_created"),
    (2027, "bundle", "revision_reentry_consistency_bundle_creation", "revision_reentry_consistency_bundle_created"),
    (2028, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2029, "bundle", "stop_lines_carry", "revision_reentry_consistency_stop_lines_carried"),
    (2030, "bundle", "generated_history_rewrite_false", "generated_history_rewrite_false_recorded"),
    (2031, "bundle", "generated_deletion_based_consistency_false", "generated_deletion_based_consistency_false_recorded"),
    (2032, "bundle", "generated_commitment_overwrite_false", "generated_commitment_overwrite_false_recorded"),
    (2033, "integrity", "revision_entries_reentered_as_links_check", "revision_entries_reentered_as_links_confirmed"),
    (2034, "integrity", "committed_boundary_links_check", "committed_boundary_links_confirmed"),
    (2035, "integrity", "revision_commitment_trace_check", "revision_commitment_trace_confirmed"),
    (2036, "integrity", "consistency_without_rewrite_deletion_check", "consistency_without_rewrite_deletion_confirmed"),
    (2037, "integrity", "original_commitment_not_overwritten_check", "original_commitment_not_overwritten_confirmed"),
    (2038, "non_identity", "consistency_vs_history_rewrite_split", "consistency_history_rewrite_non_identity"),
    (2039, "non_identity", "consistency_vs_deletion_split", "consistency_deletion_non_identity"),
    (2040, "non_identity", "revision_reentry_vs_correction_split", "revision_reentry_correction_non_identity"),
    (2041, "non_identity", "boundary_consistency_vs_failure_split", "boundary_consistency_failure_non_identity"),
    (2042, "music_subject", "consistency_as_traceable_rehearing", "traceable_rehearing_preserved"),
    (2043, "music_subject", "nonidentical_consistency_as_living_reading", "living_reading_preserved"),
    (2044, "music_subject", "boundary_link_as_open_interpretive_memory", "open_interpretive_memory_preserved"),
    (2045, "summary", "revision_reentry_consistency_summary", "revision_reentry_consistency_observed"),
    (2046, "summary", "consistency_without_rewrite_or_deletion_summary", "consistency_without_rewrite_or_deletion_confirmed"),
    (2047, "next_plan", "revision_conflict_detection_next_candidate", "revision_conflict_detection_next_candidate"),
    (2048, "next_plan", "next_xi_selection", "xi_revision_conflict_detection_stress"),
)


def _build_steps() -> tuple[RevisionReentryConsistencyStep, ...]:
    previous = "commitment_revision_memory_1949_1998"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            RevisionReentryConsistencyStep(
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


def _consistency_link(revision: RevisionMemoryEntry) -> RevisionReentryLink:
    if revision.source_commitment.enters_commitment:
        kind = "committed_revision_consistency_link"
        relation = "reheard_commitment_consistent_with_original_weight"
    else:
        kind = "boundary_revision_consistency_link"
        relation = "open_responsibility_consistent_with_noncommitment_trace"

    return RevisionReentryLink(
        source_revision=revision,
        link_kind=kind,
        consistency_relation=relation,
        preserves_revision_trace=True,
        preserves_commitment_trace=revision.preserves_commitment_trace,
        rewrites_original_commitment=False,
        forces_consistency_by_deletion=False,
        status="revision_reentry_consistency_link_recorded_without_rewrite_or_deletion",
    )


def build_revision_reentry_consistency_bundle(
    source: CommitmentRevisionMemoryBundle,
) -> RevisionReentryConsistencyBundle:
    policy = RevisionReentryConsistencyPolicy(
        name="revision_reentry_consistency_policy",
        accepts_revision_reentry=True,
        preserves_original_commitment=True,
        permits_nonidentical_consistency=True,
        rejects_deletion_based_consistency=True,
        generates_history_rewrite=False,
        status="revision_reentry_policy_preserves_consistency_without_history_rewrite",
    )
    links = tuple(_consistency_link(entry) for entry in source.revision_entries)
    committed = tuple(link for link in links if "committed" in link.link_kind)
    boundary = tuple(link for link in links if "boundary" in link.link_kind)
    return RevisionReentryConsistencyBundle(
        source_bundle=source,
        policy=policy,
        consistency_links=links,
        committed_consistency_links=committed,
        boundary_consistency_links=boundary,
        stop_lines=(
            "consistency_not_history_rewrite",
            "consistency_not_deletion_based",
            "consistency_not_commitment_overwrite",
            "revision_reentry_not_correction_only",
            "boundary_link_not_failure",
        ),
        generated_history_rewrite=False,
        generated_deletion_based_consistency=False,
        generated_commitment_overwrite=False,
        status="revision_reentry_consistency_bundle_1999_2048_built_without_rewrite_or_deletion",
    )


def observe_revision_reentry_consistency() -> RevisionReentryConsistencyObservation:
    source = observe_commitment_revision_memory()
    bundle = build_revision_reentry_consistency_bundle(source.bundle)
    steps = _build_steps()

    return RevisionReentryConsistencyObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        revision_entries_reentered_as_links=(
            len(bundle.consistency_links) == len(source.bundle.revision_entries)
        ),
        committed_and_boundary_links_preserved=(
            len(bundle.committed_consistency_links) == 2
            and len(bundle.boundary_consistency_links) == 1
        ),
        revision_and_commitment_traces_preserved=(
            bundle.policy.preserves_original_commitment is True
            and all(
                link.preserves_revision_trace and link.preserves_commitment_trace
                for link in bundle.consistency_links
            )
        ),
        consistency_without_rewrite_or_deletion=(
            bundle.generated_history_rewrite is False
            and bundle.generated_deletion_based_consistency is False
            and all(
                not link.rewrites_original_commitment
                and not link.forces_consistency_by_deletion
                for link in bundle.consistency_links
            )
        ),
        original_commitment_not_overwritten=bundle.generated_commitment_overwrite is False,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="revision_reentry_consistency_1999_2048_observed_without_rewrite_or_deletion",
    )


def run_checks() -> None:
    observation = observe_revision_reentry_consistency()
    bundle = observation.bundle

    assert observation.source_status == (
        "commitment_revision_memory_1949_1998_observed_without_past_rewrite_or_deletion"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 1999
    assert observation.steps[-1].number == 2048
    assert observation.revision_entries_reentered_as_links is True
    assert observation.committed_and_boundary_links_preserved is True
    assert observation.revision_and_commitment_traces_preserved is True
    assert observation.consistency_without_rewrite_or_deletion is True
    assert observation.original_commitment_not_overwritten is True
    assert len(bundle.consistency_links) == 3
    assert len(bundle.committed_consistency_links) == 2
    assert len(bundle.boundary_consistency_links) == 1
    assert bundle.generated_history_rewrite is False
    assert bundle.generated_deletion_based_consistency is False
    assert bundle.generated_commitment_overwrite is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_revision_conflict_detection_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_revision_reentry_consistency().status)
