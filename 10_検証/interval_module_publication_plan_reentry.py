"""再入push readiness診断とpublication plan候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_publication_plan_boundary import PublicationBranchPolicy, PublicationPlanCandidate, branch_policy_fixture
from interval_module_push_readiness_reentry import ReenteredPushReadinessObservation, compare_push_readiness_reentry


@dataclass(frozen=True)
class ReenteredPublicationPlanObservation:
    push_observation: ReenteredPushReadinessObservation
    branch_policy: PublicationBranchPolicy | None
    publication_plan: PublicationPlanCandidate | None
    status: str


def create_reentered_publication_plan(push_obs: ReenteredPushReadinessObservation, policy: PublicationBranchPolicy | None) -> ReenteredPublicationPlanObservation:
    diagnostic = push_obs.push_readiness
    if diagnostic is None:
        return ReenteredPublicationPlanObservation(push_obs, policy, None, "no_reentered_push_readiness")
    if policy is None:
        return ReenteredPublicationPlanObservation(push_obs, None, None, "reentered_publication_plan_not_created_without_branch_policy")
    plan = PublicationPlanCandidate("interval_publication_plan_candidate", diagnostic.label, policy.name, False)
    return ReenteredPublicationPlanObservation(push_obs, policy, plan, "publication_plan_observed_from_reentered_push_readiness_not_published")


def compare_publication_plan_reentry() -> tuple[ReenteredPublicationPlanObservation, ReenteredPublicationPlanObservation]:
    push = compare_push_readiness_reentry()[1]
    return create_reentered_publication_plan(push, None), create_reentered_publication_plan(push, branch_policy_fixture())


def run_checks() -> None:
    without_policy, with_policy = compare_publication_plan_reentry()
    assert without_policy.publication_plan is None
    assert with_policy.publication_plan is not None
    assert with_policy.publication_plan.published is False


if __name__ == "__main__":
    run_checks()
    print(compare_publication_plan_reentry()[1].status)
