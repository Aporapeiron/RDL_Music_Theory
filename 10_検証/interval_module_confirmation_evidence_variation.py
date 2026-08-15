"""confirmation evidence差し替えによるreadiness分岐の最小検証。"""

from dataclasses import dataclass

from interval_module_confirmation_readiness_boundary import (
    ConfirmationEvidenceBundle,
    ConfirmationReadinessObservation,
    diagnose_confirmation_readiness,
    gamma_readiness_fixture,
    mb_candidate_observation,
)


@dataclass(frozen=True)
class ConfirmationEvidenceVariationComparison:
    supported: ConfirmationReadinessObservation
    unsupported: ConfirmationReadinessObservation
    same_mb_candidate: bool
    same_gamma: bool
    same_evidence: bool
    same_readiness: bool


def supported_evidence_fixture() -> ConfirmationEvidenceBundle:
    return ConfirmationEvidenceBundle(
        name="supported_confirmation_evidence_fixture",
        replication_scope="fixture_cross_step_replay",
        supports_confirmation_readiness=True,
        generated_by_mb_candidate=False,
    )


def unsupported_evidence_fixture() -> ConfirmationEvidenceBundle:
    return ConfirmationEvidenceBundle(
        name="unsupported_confirmation_evidence_fixture",
        replication_scope="single_path_only",
        supports_confirmation_readiness=False,
        generated_by_mb_candidate=False,
    )


def compare_confirmation_evidence_variation() -> ConfirmationEvidenceVariationComparison:
    mb_obs = mb_candidate_observation()
    gamma = gamma_readiness_fixture()
    supported = diagnose_confirmation_readiness(mb_obs, supported_evidence_fixture(), gamma)
    unsupported = diagnose_confirmation_readiness(
        mb_obs, unsupported_evidence_fixture(), gamma
    )
    return ConfirmationEvidenceVariationComparison(
        supported=supported,
        unsupported=unsupported,
        same_mb_candidate=(
            supported.mb_candidate_observation.mb_candidate
            == unsupported.mb_candidate_observation.mb_candidate
        ),
        same_gamma=supported.gamma_readiness == unsupported.gamma_readiness,
        same_evidence=supported.evidence_bundle == unsupported.evidence_bundle,
        same_readiness=(
            supported.diagnostic.ready_for_confirmation_controller
            == unsupported.diagnostic.ready_for_confirmation_controller
        ),
    )


def run_checks() -> None:
    comparison = compare_confirmation_evidence_variation()
    assert comparison.same_mb_candidate is True
    assert comparison.same_gamma is True
    assert comparison.same_evidence is False
    assert comparison.same_readiness is False
    assert comparison.supported.diagnostic is not None
    assert comparison.unsupported.diagnostic is not None
    assert comparison.supported.diagnostic.confirmed_mb is False
    assert comparison.unsupported.diagnostic.confirmed_mb is False


if __name__ == "__main__":
    run_checks()
    print(compare_confirmation_evidence_variation())
