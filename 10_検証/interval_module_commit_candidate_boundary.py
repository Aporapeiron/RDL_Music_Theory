"""accepted update recordとcommit候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_update_acceptance_boundary import (
    UpdateAcceptanceObservation,
    compare_update_acceptance,
)


@dataclass(frozen=True)
class CommitBoundary:
    name: str
    generated_by_acceptance: bool


@dataclass(frozen=True)
class CommitCandidate:
    label: str
    source_acceptance_label: str
    git_commit_created: bool


@dataclass(frozen=True)
class CommitCandidateObservation:
    acceptance_observation: UpdateAcceptanceObservation
    commit_boundary: CommitBoundary | None
    commit_candidate: CommitCandidate | None
    status: str


def acceptance_observation() -> UpdateAcceptanceObservation:
    return compare_update_acceptance()[1]


def commit_boundary_fixture() -> CommitBoundary:
    return CommitBoundary(name="interval_commit_boundary_fixture", generated_by_acceptance=False)


def create_commit_candidate(
    acceptance: UpdateAcceptanceObservation,
    boundary: CommitBoundary | None,
) -> CommitCandidateObservation:
    accepted = acceptance.accepted_update
    if accepted is None:
        return CommitCandidateObservation(acceptance, boundary, None, "no_accepted_update_record")
    if boundary is None:
        return CommitCandidateObservation(
            acceptance, None, None, "commit_candidate_not_created_without_boundary"
        )
    candidate = CommitCandidate(
        label="interval_documentation_commit_candidate",
        source_acceptance_label=accepted.label,
        git_commit_created=False,
    )
    return CommitCandidateObservation(
        acceptance, boundary, candidate, "commit_candidate_observed_not_git_commit"
    )


def compare_commit_candidate() -> tuple[
    CommitCandidateObservation, CommitCandidateObservation
]:
    acceptance = acceptance_observation()
    return (
        create_commit_candidate(acceptance, None),
        create_commit_candidate(acceptance, commit_boundary_fixture()),
    )


def run_checks() -> None:
    without_boundary, with_boundary = compare_commit_candidate()
    assert without_boundary.status == "commit_candidate_not_created_without_boundary"
    assert with_boundary.status == "commit_candidate_observed_not_git_commit"
    assert with_boundary.commit_candidate is not None
    assert with_boundary.commit_candidate.git_commit_created is False
    assert with_boundary.commit_boundary is not None
    assert with_boundary.commit_boundary.generated_by_acceptance is False


if __name__ == "__main__":
    run_checks()
    print(compare_commit_candidate()[1].status)
