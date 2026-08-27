"""再入accepted update recordとcommit候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_commit_candidate_boundary import CommitBoundary, CommitCandidate, commit_boundary_fixture
from interval_module_update_acceptance_reentry import ReenteredUpdateAcceptanceObservation, compare_update_acceptance_reentry


@dataclass(frozen=True)
class ReenteredCommitCandidateObservation:
    acceptance_observation: ReenteredUpdateAcceptanceObservation
    commit_boundary: CommitBoundary | None
    commit_candidate: CommitCandidate | None
    status: str


def create_reentered_commit_candidate(acceptance: ReenteredUpdateAcceptanceObservation, boundary: CommitBoundary | None) -> ReenteredCommitCandidateObservation:
    accepted = acceptance.accepted_update
    if accepted is None:
        return ReenteredCommitCandidateObservation(acceptance, boundary, None, "no_reentered_accepted_update_record")
    if boundary is None:
        return ReenteredCommitCandidateObservation(acceptance, None, None, "reentered_commit_candidate_not_created_without_boundary")
    candidate = CommitCandidate("interval_documentation_commit_candidate", accepted.label, False)
    return ReenteredCommitCandidateObservation(acceptance, boundary, candidate, "commit_candidate_observed_from_reentered_acceptance_not_git_commit")


def compare_commit_candidate_reentry() -> tuple[ReenteredCommitCandidateObservation, ReenteredCommitCandidateObservation]:
    acceptance = compare_update_acceptance_reentry()[1]
    return create_reentered_commit_candidate(acceptance, None), create_reentered_commit_candidate(acceptance, commit_boundary_fixture())


def run_checks() -> None:
    without_boundary, with_boundary = compare_commit_candidate_reentry()
    assert without_boundary.commit_candidate is None
    assert with_boundary.commit_candidate is not None
    assert with_boundary.commit_candidate.git_commit_created is False


if __name__ == "__main__":
    run_checks()
    print(compare_commit_candidate_reentry()[1].status)
