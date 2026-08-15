"""push readiness診断とpublication plan候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_push_readiness_boundary import (
    PushReadinessObservation,
    compare_push_readiness,
)


@dataclass(frozen=True)
class PublicationBranchPolicy:
    name: str
    generated_by_push_readiness: bool


@dataclass(frozen=True)
class PublicationPlanCandidate:
    label: str
    source_push_readiness_label: str
    branch_policy_name: str
    published: bool


@dataclass(frozen=True)
class PublicationPlanObservation:
    push_observation: PushReadinessObservation
    branch_policy: PublicationBranchPolicy | None
    publication_plan: PublicationPlanCandidate | None
    status: str


def push_observation() -> PushReadinessObservation:
    return compare_push_readiness()[1]


def branch_policy_fixture() -> PublicationBranchPolicy:
    return PublicationBranchPolicy(
        name="interval_publication_branch_policy_fixture",
        generated_by_push_readiness=False,
    )


def create_publication_plan(
    push_obs: PushReadinessObservation,
    policy: PublicationBranchPolicy | None,
) -> PublicationPlanObservation:
    diagnostic = push_obs.push_readiness
    if diagnostic is None:
        return PublicationPlanObservation(push_obs, policy, None, "no_push_readiness")
    if policy is None:
        return PublicationPlanObservation(
            push_obs, None, None, "publication_plan_not_created_without_branch_policy"
        )
    plan = PublicationPlanCandidate(
        label="interval_publication_plan_candidate",
        source_push_readiness_label=diagnostic.label,
        branch_policy_name=policy.name,
        published=False,
    )
    return PublicationPlanObservation(
        push_obs, policy, plan, "publication_plan_candidate_observed_not_published"
    )


def compare_publication_plan() -> tuple[
    PublicationPlanObservation, PublicationPlanObservation
]:
    push = push_observation()
    return (
        create_publication_plan(push, None),
        create_publication_plan(push, branch_policy_fixture()),
    )


def run_checks() -> None:
    without_policy, with_policy = compare_publication_plan()
    assert without_policy.status == "publication_plan_not_created_without_branch_policy"
    assert with_policy.status == "publication_plan_candidate_observed_not_published"
    assert with_policy.publication_plan is not None
    assert with_policy.publication_plan.published is False
    assert with_policy.branch_policy is not None
    assert with_policy.branch_policy.generated_by_push_readiness is False


if __name__ == "__main__":
    run_checks()
    print(compare_publication_plan()[1].status)
