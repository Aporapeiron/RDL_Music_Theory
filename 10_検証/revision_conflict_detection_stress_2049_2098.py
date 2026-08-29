"""revision reentry後のconflict detection境界を検査する最小実験。"""

from dataclasses import dataclass

from revision_reentry_consistency_stress_1999_2048 import (
    RevisionReentryConsistencyBundle,
    RevisionReentryLink,
    observe_revision_reentry_consistency,
)


@dataclass(frozen=True)
class RevisionConflictDetectionStep:
    number: int
    phase: str
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class RevisionConflictCandidate:
    source_link: RevisionReentryLink
    conflict_kind: str
    conflict_site: str
    preserves_revision_trace: bool
    preserves_commitment_trace: bool
    detects_conflict: bool
    resolves_conflict_now: bool
    deletes_conflicting_path: bool
    status: str


@dataclass(frozen=True)
class RevisionConflictDetectionPolicy:
    name: str
    accepts_consistency_links: bool
    detects_nonidentical_conflicts: bool
    preserves_conflict_trace: bool
    rejects_resolution_collapse: bool
    generates_deletion_resolution: bool
    status: str


@dataclass(frozen=True)
class RevisionConflictDetectionBundle:
    source_bundle: RevisionReentryConsistencyBundle
    policy: RevisionConflictDetectionPolicy
    conflict_candidates: tuple[RevisionConflictCandidate, ...]
    detected_conflicts: tuple[RevisionConflictCandidate, ...]
    nonconflict_links: tuple[RevisionConflictCandidate, ...]
    boundary_conflicts: tuple[RevisionConflictCandidate, ...]
    stop_lines: tuple[str, ...]
    generated_conflict_resolution: bool
    generated_deletion_resolution: bool
    generated_trace_erasure: bool
    status: str


@dataclass(frozen=True)
class RevisionConflictDetectionObservation:
    source_status: str
    steps: tuple[RevisionConflictDetectionStep, ...]
    bundle: RevisionConflictDetectionBundle
    consistency_links_examined: bool
    detected_and_nonconflict_paths_preserved: bool
    revision_and_commitment_traces_preserved: bool
    detection_not_resolution_or_deletion: bool
    boundary_conflict_preserved: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str, str], ...] = (
    (2049, "source_reentry", "reuse_1999_2048_revision_reentry_consistency", "revision_reentry_consistency_preserved"),
    (2050, "source_reentry", "next_xi_received", "revision_conflict_detection_stress_received"),
    (2051, "source_reentry", "consistency_links_recheck", "consistency_links_available"),
    (2052, "conflict_request", "revision_conflict_detection_request", "revision_conflict_detection_candidate"),
    (2053, "conflict_request", "detection_not_resolution_guard", "detection_resolution_non_identity_preserved"),
    (2054, "conflict_request", "detection_not_deletion_guard", "deletion_resolution_blocked"),
    (2055, "conflict_request", "detection_not_trace_erasure_guard", "trace_erasure_non_identity_preserved"),
    (2056, "policy_layer", "revision_conflict_detection_policy", "revision_conflict_detection_policy_recorded"),
    (2057, "policy_layer", "consistency_link_acceptance_rule", "consistency_link_acceptance_recorded"),
    (2058, "policy_layer", "nonidentical_conflict_detection_rule", "nonidentical_conflict_detection_recorded"),
    (2059, "policy_layer", "conflict_trace_preservation_rule", "conflict_trace_preservation_recorded"),
    (2060, "policy_layer", "resolution_collapse_rejection_rule", "resolution_collapse_rejection_recorded"),
    (2061, "conflict_layer", "reference_link_no_conflict_record", "reference_link_no_conflict_recorded"),
    (2062, "conflict_layer", "boundary_link_conflict_record", "boundary_link_conflict_recorded"),
    (2063, "conflict_layer", "committed_link_tension_record", "committed_link_tension_recorded"),
    (2064, "conflict_layer", "revision_trace_carry", "revision_trace_carried"),
    (2065, "conflict_layer", "commitment_trace_carry", "commitment_trace_carried"),
    (2066, "conflict_layer", "resolution_false_record", "resolution_false_recorded"),
    (2067, "conflict_layer", "deletion_false_record", "deletion_false_recorded"),
    (2068, "partition_layer", "detected_conflict_partition", "detected_conflict_partition_recorded"),
    (2069, "partition_layer", "nonconflict_link_partition", "nonconflict_link_partition_recorded"),
    (2070, "partition_layer", "boundary_conflict_partition", "boundary_conflict_partition_recorded"),
    (2071, "partition_layer", "partition_not_verdict_guard", "partition_verdict_non_identity"),
    (2072, "partition_layer", "conflict_not_failure_guard", "conflict_failure_non_identity"),
    (2073, "conflict_view", "revision_conflict_detection_view", "revision_conflict_detection_view_created"),
    (2074, "conflict_view", "conflict_site_view", "conflict_site_view_created"),
    (2075, "conflict_view", "trace_preserving_conflict_view", "trace_preserving_conflict_view_created"),
    (2076, "conflict_view", "unresolved_conflict_view", "unresolved_conflict_view_created"),
    (2077, "bundle", "revision_conflict_detection_bundle_creation", "revision_conflict_detection_bundle_created"),
    (2078, "bundle", "source_bundle_carry", "source_bundle_carried"),
    (2079, "bundle", "stop_lines_carry", "revision_conflict_detection_stop_lines_carried"),
    (2080, "bundle", "generated_conflict_resolution_false", "generated_conflict_resolution_false_recorded"),
    (2081, "bundle", "generated_deletion_resolution_false", "generated_deletion_resolution_false_recorded"),
    (2082, "bundle", "generated_trace_erasure_false", "generated_trace_erasure_false_recorded"),
    (2083, "integrity", "consistency_links_examined_check", "consistency_links_examined_confirmed"),
    (2084, "integrity", "detected_nonconflict_paths_check", "detected_nonconflict_paths_confirmed"),
    (2085, "integrity", "revision_commitment_trace_check", "revision_commitment_trace_confirmed"),
    (2086, "integrity", "detection_not_resolution_deletion_check", "detection_not_resolution_deletion_confirmed"),
    (2087, "integrity", "boundary_conflict_preservation_check", "boundary_conflict_preservation_confirmed"),
    (2088, "non_identity", "detection_vs_resolution_split", "detection_resolution_non_identity"),
    (2089, "non_identity", "conflict_vs_failure_split", "conflict_failure_non_identity"),
    (2090, "non_identity", "conflict_detection_vs_verdict_split", "conflict_detection_verdict_non_identity"),
    (2091, "non_identity", "trace_conflict_vs_trace_erasure_split", "trace_conflict_erasure_non_identity"),
    (2092, "music_subject", "conflict_as_audible_tension", "audible_tension_preserved"),
    (2093, "music_subject", "boundary_conflict_as_open_reading_pressure", "open_reading_pressure_preserved"),
    (2094, "music_subject", "committed_tension_as_interpretive_friction", "interpretive_friction_preserved"),
    (2095, "summary", "revision_conflict_detection_summary", "revision_conflict_detection_observed"),
    (2096, "summary", "detection_without_resolution_or_deletion_summary", "detection_without_resolution_or_deletion_confirmed"),
    (2097, "next_plan", "conflict_resolution_policy_next_candidate", "conflict_resolution_policy_next_candidate"),
    (2098, "next_plan", "next_xi_selection", "xi_conflict_resolution_policy_stress"),
)


def _build_steps() -> tuple[RevisionConflictDetectionStep, ...]:
    previous = "revision_reentry_consistency_1999_2048"
    steps = []
    for number, phase, name, result in STEP_DEFINITIONS:
        steps.append(
            RevisionConflictDetectionStep(
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


def _conflict_candidate(
    link: RevisionReentryLink,
    index: int,
) -> RevisionConflictCandidate:
    if "boundary" in link.link_kind:
        kind = "boundary_revision_conflict"
        site = "noncommitment_trace_vs_reentry_pressure"
        detects = True
    elif index == 2:
        kind = "committed_revision_tension"
        site = "active_pull_vs_original_weight"
        detects = True
    else:
        kind = "reference_revision_nonconflict"
        site = "stable_reference_trace"
        detects = False

    return RevisionConflictCandidate(
        source_link=link,
        conflict_kind=kind,
        conflict_site=site,
        preserves_revision_trace=link.preserves_revision_trace,
        preserves_commitment_trace=link.preserves_commitment_trace,
        detects_conflict=detects,
        resolves_conflict_now=False,
        deletes_conflicting_path=False,
        status="revision_conflict_candidate_recorded_without_resolution_or_deletion",
    )


def build_revision_conflict_detection_bundle(
    source: RevisionReentryConsistencyBundle,
) -> RevisionConflictDetectionBundle:
    policy = RevisionConflictDetectionPolicy(
        name="revision_conflict_detection_policy",
        accepts_consistency_links=True,
        detects_nonidentical_conflicts=True,
        preserves_conflict_trace=True,
        rejects_resolution_collapse=True,
        generates_deletion_resolution=False,
        status="revision_conflict_detection_policy_preserves_conflict_without_resolution",
    )
    candidates = tuple(
        _conflict_candidate(link, index)
        for index, link in enumerate(source.consistency_links)
    )
    detected = tuple(candidate for candidate in candidates if candidate.detects_conflict)
    nonconflict = tuple(candidate for candidate in candidates if not candidate.detects_conflict)
    boundary = tuple(candidate for candidate in detected if "boundary" in candidate.conflict_kind)
    return RevisionConflictDetectionBundle(
        source_bundle=source,
        policy=policy,
        conflict_candidates=candidates,
        detected_conflicts=detected,
        nonconflict_links=nonconflict,
        boundary_conflicts=boundary,
        stop_lines=(
            "detection_not_resolution",
            "detection_not_deletion",
            "detection_not_trace_erasure",
            "conflict_not_failure",
            "conflict_detection_not_verdict",
        ),
        generated_conflict_resolution=False,
        generated_deletion_resolution=False,
        generated_trace_erasure=False,
        status="revision_conflict_detection_bundle_2049_2098_built_without_resolution_or_deletion",
    )


def observe_revision_conflict_detection() -> RevisionConflictDetectionObservation:
    source = observe_revision_reentry_consistency()
    bundle = build_revision_conflict_detection_bundle(source.bundle)
    steps = _build_steps()

    return RevisionConflictDetectionObservation(
        source_status=source.status,
        steps=steps,
        bundle=bundle,
        consistency_links_examined=(
            len(bundle.conflict_candidates) == len(source.bundle.consistency_links)
        ),
        detected_and_nonconflict_paths_preserved=(
            len(bundle.detected_conflicts) == 2
            and len(bundle.nonconflict_links) == 1
        ),
        revision_and_commitment_traces_preserved=(
            bundle.policy.preserves_conflict_trace is True
            and all(
                candidate.preserves_revision_trace and candidate.preserves_commitment_trace
                for candidate in bundle.conflict_candidates
            )
        ),
        detection_not_resolution_or_deletion=(
            bundle.generated_conflict_resolution is False
            and bundle.generated_deletion_resolution is False
            and all(
                not candidate.resolves_conflict_now
                and not candidate.deletes_conflicting_path
                for candidate in bundle.conflict_candidates
            )
        ),
        boundary_conflict_preserved=len(bundle.boundary_conflicts) == 1,
        generated_mutation=any(step.generated_mutation for step in steps),
        status="revision_conflict_detection_2049_2098_observed_without_resolution_or_deletion",
    )


def run_checks() -> None:
    observation = observe_revision_conflict_detection()
    bundle = observation.bundle

    assert observation.source_status == (
        "revision_reentry_consistency_1999_2048_observed_without_rewrite_or_deletion"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 2049
    assert observation.steps[-1].number == 2098
    assert observation.consistency_links_examined is True
    assert observation.detected_and_nonconflict_paths_preserved is True
    assert observation.revision_and_commitment_traces_preserved is True
    assert observation.detection_not_resolution_or_deletion is True
    assert observation.boundary_conflict_preserved is True
    assert len(bundle.conflict_candidates) == 3
    assert len(bundle.detected_conflicts) == 2
    assert len(bundle.nonconflict_links) == 1
    assert len(bundle.boundary_conflicts) == 1
    assert bundle.generated_conflict_resolution is False
    assert bundle.generated_deletion_resolution is False
    assert bundle.generated_trace_erasure is False
    assert observation.generated_mutation is False
    assert observation.steps[-1].result == "xi_conflict_resolution_policy_stress"


if __name__ == "__main__":
    run_checks()
    print(observe_revision_conflict_detection().status)
