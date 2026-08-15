"""構造破断診断とintegration候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_break_diagnostic_boundary import (
    BreakDiagnosticObservation,
    compare_break_diagnostic,
)


@dataclass(frozen=True)
class IntegrationPolicy:
    name: str
    generated_by_break_diagnostic: bool


@dataclass(frozen=True)
class IntegrationCandidate:
    label: str
    source_break_diagnostic_label: str
    integration_kind: str
    document_update_generated: bool


@dataclass(frozen=True)
class IntegrationObservation:
    break_observation: BreakDiagnosticObservation
    integration_policy: IntegrationPolicy | None
    integration_candidate: IntegrationCandidate | None
    status: str


def break_observation() -> BreakDiagnosticObservation:
    return compare_break_diagnostic()[1]


def integration_policy_fixture() -> IntegrationPolicy:
    return IntegrationPolicy(
        name="interval_integration_policy_fixture",
        generated_by_break_diagnostic=False,
    )


def create_integration_candidate(
    break_obs: BreakDiagnosticObservation,
    policy: IntegrationPolicy | None,
) -> IntegrationObservation:
    diagnostic = break_obs.break_diagnostic
    if diagnostic is None:
        return IntegrationObservation(break_obs, policy, None, "no_break_diagnostic")
    if policy is None:
        return IntegrationObservation(
            break_obs, None, None, "integration_candidate_not_created_without_policy"
        )
    integration = IntegrationCandidate(
        label="interval_no_break_integration_candidate",
        source_break_diagnostic_label=diagnostic.label,
        integration_kind="preserve_boundary_and_register_result",
        document_update_generated=False,
    )
    return IntegrationObservation(
        break_obs, policy, integration, "integration_candidate_observed_not_document_update"
    )


def compare_integration_candidate() -> tuple[IntegrationObservation, IntegrationObservation]:
    break_obs = break_observation()
    return (
        create_integration_candidate(break_obs, None),
        create_integration_candidate(break_obs, integration_policy_fixture()),
    )


def run_checks() -> None:
    without_policy, with_policy = compare_integration_candidate()
    assert without_policy.status == "integration_candidate_not_created_without_policy"
    assert with_policy.status == "integration_candidate_observed_not_document_update"
    assert with_policy.integration_candidate is not None
    assert with_policy.integration_candidate.document_update_generated is False
    assert with_policy.integration_policy is not None
    assert with_policy.integration_policy.generated_by_break_diagnostic is False


if __name__ == "__main__":
    run_checks()
    print(compare_integration_candidate()[1].status)
