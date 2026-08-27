"""再入commit候補とpush readiness診断境界の最小検証。"""

from dataclasses import dataclass

from interval_module_commit_candidate_reentry import ReenteredCommitCandidateObservation, compare_commit_candidate_reentry
from interval_module_push_readiness_boundary import PushBoundary, PushReadinessDiagnostic, push_boundary_fixture


@dataclass(frozen=True)
class ReenteredPushReadinessObservation:
    commit_observation: ReenteredCommitCandidateObservation
    push_boundary: PushBoundary | None
    push_readiness: PushReadinessDiagnostic | None
    status: str


def diagnose_reentered_push_readiness(commit_obs: ReenteredCommitCandidateObservation, boundary: PushBoundary | None) -> ReenteredPushReadinessObservation:
    commit_candidate = commit_obs.commit_candidate
    if commit_candidate is None:
        return ReenteredPushReadinessObservation(commit_obs, boundary, None, "no_reentered_commit_candidate")
    if boundary is None:
        return ReenteredPushReadinessObservation(commit_obs, None, None, "reentered_push_readiness_not_checked_without_boundary")
    diagnostic = PushReadinessDiagnostic("interval_push_readiness_diagnostic", commit_candidate.label, True, False)
    return ReenteredPushReadinessObservation(commit_obs, boundary, diagnostic, "push_readiness_observed_from_reentered_commit_not_pushed")


def compare_push_readiness_reentry() -> tuple[ReenteredPushReadinessObservation, ReenteredPushReadinessObservation]:
    commit = compare_commit_candidate_reentry()[1]
    return diagnose_reentered_push_readiness(commit, None), diagnose_reentered_push_readiness(commit, push_boundary_fixture())


def run_checks() -> None:
    without_boundary, with_boundary = compare_push_readiness_reentry()
    assert without_boundary.push_readiness is None
    assert with_boundary.push_readiness is not None
    assert with_boundary.push_readiness.ready_to_push is True
    assert with_boundary.push_readiness.git_push_performed is False


if __name__ == "__main__":
    run_checks()
    print(compare_push_readiness_reentry()[1].status)
