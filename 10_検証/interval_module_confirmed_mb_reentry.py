"""再入confirmation readinessからconfirmed M_B候補へ接続する最小検証。"""

from dataclasses import dataclass

from interval_module_confirmation_readiness_reentry import (
    ReenteredConfirmationReadinessObservation,
    compare_confirmation_readiness_reentry,
)
from interval_module_confirmed_mb_boundary import (
    ConfirmedIntervalMBCandidate,
    MBConfirmationController,
    confirmation_controller_fixture,
)


@dataclass(frozen=True)
class ReenteredConfirmedMBObservation:
    readiness_observation: ReenteredConfirmationReadinessObservation
    confirmation_controller: MBConfirmationController | None
    confirmed_candidate: ConfirmedIntervalMBCandidate | None
    status: str


def confirm_reentered_mb_candidate(
    readiness: ReenteredConfirmationReadinessObservation,
    controller: MBConfirmationController | None,
) -> ReenteredConfirmedMBObservation:
    diagnostic = readiness.diagnostic
    if diagnostic is None:
        return ReenteredConfirmedMBObservation(readiness, controller, None, "no_reentered_readiness_diagnostic")
    if controller is None:
        return ReenteredConfirmedMBObservation(readiness, None, None, "reentered_confirmed_M_B_not_created_without_controller")
    if not diagnostic.ready_for_confirmation_controller:
        return ReenteredConfirmedMBObservation(readiness, controller, None, "reentered_confirmed_M_B_blocked_not_ready")
    confirmed = ConfirmedIntervalMBCandidate(
        "confirmed_M_B_interval_context_harmony_candidate",
        diagnostic.label,
        True,
        False,
    )
    return ReenteredConfirmedMBObservation(readiness, controller, confirmed, "confirmed_M_B_observed_from_reentered_readiness_not_core_promotion")


def compare_confirmed_mb_reentry() -> tuple[ReenteredConfirmedMBObservation, ReenteredConfirmedMBObservation]:
    readiness = compare_confirmation_readiness_reentry()[1]
    return (
        confirm_reentered_mb_candidate(readiness, None),
        confirm_reentered_mb_candidate(readiness, confirmation_controller_fixture()),
    )


def run_checks() -> None:
    without_controller, with_controller = compare_confirmed_mb_reentry()
    assert without_controller.confirmed_candidate is None
    assert with_controller.confirmed_candidate is not None
    assert with_controller.confirmed_candidate.confirmed_mb is True
    assert with_controller.confirmed_candidate.core_promoted is False


if __name__ == "__main__":
    run_checks()
    print(compare_confirmed_mb_reentry()[1].status)
