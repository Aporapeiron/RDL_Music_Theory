"""再入confirmation evidence差し替えによるreadiness分岐の最小検証。"""

from dataclasses import dataclass

from interval_module_confirmation_readiness_boundary import ConfirmationEvidenceBundle, gamma_readiness_fixture
from interval_module_confirmation_readiness_reentry import (
    ReenteredConfirmationReadinessObservation,
    diagnose_reentered_confirmation_readiness,
)
from interval_module_mb_candidate_reentry import compare_mb_candidate_reentry


@dataclass(frozen=True)
class ReenteredConfirmationEvidenceVariationComparison:
    supported: ReenteredConfirmationReadinessObservation
    unsupported: ReenteredConfirmationReadinessObservation
    same_mb_candidate: bool
    same_gamma: bool
    same_evidence: bool
    same_readiness: bool


def supported_evidence_fixture() -> ConfirmationEvidenceBundle:
    return ConfirmationEvidenceBundle("supported_confirmation_evidence_fixture", "fixture_cross_step_replay", True, False)


def unsupported_evidence_fixture() -> ConfirmationEvidenceBundle:
    return ConfirmationEvidenceBundle("unsupported_confirmation_evidence_fixture", "single_path_only", False, False)


def compare_confirmation_evidence_variation_reentry() -> ReenteredConfirmationEvidenceVariationComparison:
    mb_obs = compare_mb_candidate_reentry()[1]
    gamma = gamma_readiness_fixture()
    supported = diagnose_reentered_confirmation_readiness(mb_obs, supported_evidence_fixture(), gamma)
    unsupported = diagnose_reentered_confirmation_readiness(mb_obs, unsupported_evidence_fixture(), gamma)
    assert supported.diagnostic is not None
    assert unsupported.diagnostic is not None
    return ReenteredConfirmationEvidenceVariationComparison(
        supported,
        unsupported,
        supported.mb_candidate_observation.mb_candidate == unsupported.mb_candidate_observation.mb_candidate,
        supported.gamma_readiness == unsupported.gamma_readiness,
        supported.evidence_bundle == unsupported.evidence_bundle,
        supported.diagnostic.ready_for_confirmation_controller == unsupported.diagnostic.ready_for_confirmation_controller,
    )


def run_checks() -> None:
    comparison = compare_confirmation_evidence_variation_reentry()
    assert comparison.same_mb_candidate is True
    assert comparison.same_gamma is True
    assert comparison.same_evidence is False
    assert comparison.same_readiness is False
    assert comparison.supported.diagnostic.confirmed_mb is False
    assert comparison.unsupported.diagnostic.confirmed_mb is False


if __name__ == "__main__":
    run_checks()
    print("reentered_confirmation_evidence_variation_changes_readiness_not_confirmation")
