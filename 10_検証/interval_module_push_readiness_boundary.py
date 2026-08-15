"""commit候補とpush readiness診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_commit_candidate_boundary import (
    CommitCandidateObservation,
    compare_commit_candidate,
)


@dataclass(frozen=True)
class PushBoundary:
    name: str
    generated_by_commit_candidate: bool


@dataclass(frozen=True)
class PushReadinessDiagnostic:
    label: str
    source_commit_candidate_label: str
    ready_to_push: bool
    git_push_performed: bool


@dataclass(frozen=True)
class PushReadinessObservation:
    commit_observation: CommitCandidateObservation
    push_boundary: PushBoundary | None
    push_readiness: PushReadinessDiagnostic | None
    status: str


def commit_observation() -> CommitCandidateObservation:
    return compare_commit_candidate()[1]


def push_boundary_fixture() -> PushBoundary:
    return PushBoundary(
        name="interval_push_boundary_fixture",
        generated_by_commit_candidate=False,
    )


def diagnose_push_readiness(
    commit_obs: CommitCandidateObservation,
    boundary: PushBoundary | None,
) -> PushReadinessObservation:
    commit_candidate = commit_obs.commit_candidate
    if commit_candidate is None:
        return PushReadinessObservation(commit_obs, boundary, None, "no_commit_candidate")
    if boundary is None:
        return PushReadinessObservation(
            commit_obs, None, None, "push_readiness_not_checked_without_boundary"
        )
    diagnostic = PushReadinessDiagnostic(
        label="interval_push_readiness_diagnostic",
        source_commit_candidate_label=commit_candidate.label,
        ready_to_push=True,
        git_push_performed=False,
    )
    return PushReadinessObservation(
        commit_obs, boundary, diagnostic, "push_readiness_diagnostic_observed_not_pushed"
    )


def compare_push_readiness() -> tuple[PushReadinessObservation, PushReadinessObservation]:
    commit = commit_observation()
    return (
        diagnose_push_readiness(commit, None),
        diagnose_push_readiness(commit, push_boundary_fixture()),
    )


def run_checks() -> None:
    without_boundary, with_boundary = compare_push_readiness()
    assert without_boundary.status == "push_readiness_not_checked_without_boundary"
    assert with_boundary.status == "push_readiness_diagnostic_observed_not_pushed"
    assert with_boundary.push_readiness is not None
    assert with_boundary.push_readiness.ready_to_push is True
    assert with_boundary.push_readiness.git_push_performed is False
    assert with_boundary.push_boundary is not None
    assert with_boundary.push_boundary.generated_by_commit_candidate is False


if __name__ == "__main__":
    run_checks()
    print(compare_push_readiness()[1].status)
