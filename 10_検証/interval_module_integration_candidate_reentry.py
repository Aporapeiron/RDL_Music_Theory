"""再入構造破断診断とintegration候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_break_diagnostic_reentry import ReenteredBreakDiagnosticObservation, compare_break_diagnostic_reentry
from interval_module_integration_candidate_boundary import IntegrationCandidate, IntegrationPolicy, integration_policy_fixture


@dataclass(frozen=True)
class ReenteredIntegrationObservation:
    break_observation: ReenteredBreakDiagnosticObservation
    integration_policy: IntegrationPolicy | None
    integration_candidate: IntegrationCandidate | None
    status: str


def create_reentered_integration_candidate(break_obs: ReenteredBreakDiagnosticObservation, policy: IntegrationPolicy | None) -> ReenteredIntegrationObservation:
    diagnostic = break_obs.break_diagnostic
    if diagnostic is None:
        return ReenteredIntegrationObservation(break_obs, policy, None, "no_reentered_break_diagnostic")
    if policy is None:
        return ReenteredIntegrationObservation(break_obs, None, None, "reentered_integration_candidate_not_created_without_policy")
    integration = IntegrationCandidate("interval_no_break_integration_candidate", diagnostic.label, "preserve_boundary_and_register_result", False)
    return ReenteredIntegrationObservation(break_obs, policy, integration, "integration_candidate_observed_from_reentered_break_diagnostic_not_document_update")


def compare_integration_candidate_reentry() -> tuple[ReenteredIntegrationObservation, ReenteredIntegrationObservation]:
    break_obs = compare_break_diagnostic_reentry()[1]
    return create_reentered_integration_candidate(break_obs, None), create_reentered_integration_candidate(break_obs, integration_policy_fixture())


def run_checks() -> None:
    without_policy, with_policy = compare_integration_candidate_reentry()
    assert without_policy.integration_candidate is None
    assert with_policy.integration_candidate is not None
    assert with_policy.integration_candidate.document_update_generated is False


if __name__ == "__main__":
    run_checks()
    print(compare_integration_candidate_reentry()[1].status)
