"""confirmation readinessとconfirmed M_B候補境界の最小検証。"""

from dataclasses import dataclass

from interval_module_confirmation_readiness_boundary import (
    ConfirmationReadinessObservation,
    compare_confirmation_readiness,
)


@dataclass(frozen=True)
class MBConfirmationController:
    name: str
    reads: tuple[str, str]
    controller_scope: str
    generated_by_readiness: bool


@dataclass(frozen=True)
class ConfirmedIntervalMBCandidate:
    label: str
    source_diagnostic_label: str
    confirmed_mb: bool
    core_promoted: bool


@dataclass(frozen=True)
class ConfirmedMBObservation:
    readiness_observation: ConfirmationReadinessObservation
    confirmation_controller: MBConfirmationController | None
    confirmed_candidate: ConfirmedIntervalMBCandidate | None
    status: str


def readiness_observation() -> ConfirmationReadinessObservation:
    return compare_confirmation_readiness()[1]


def confirmation_controller_fixture() -> MBConfirmationController:
    return MBConfirmationController(
        name="Gamma_interval_M_B_confirmation_controller_fixture",
        reads=("confirmation_readiness_diagnostic", "external_confirmation_controller"),
        controller_scope="fixture_limited_confirmation_not_core_promotion",
        generated_by_readiness=False,
    )


def confirm_mb_candidate(
    readiness: ConfirmationReadinessObservation,
    controller: MBConfirmationController | None,
) -> ConfirmedMBObservation:
    diagnostic = readiness.diagnostic
    if diagnostic is None:
        return ConfirmedMBObservation(readiness, controller, None, "no_readiness_diagnostic")
    if controller is None:
        return ConfirmedMBObservation(
            readiness, None, None, "confirmed_M_B_not_created_without_controller"
        )
    if not diagnostic.ready_for_confirmation_controller:
        return ConfirmedMBObservation(
            readiness, controller, None, "confirmed_M_B_blocked_not_ready"
        )
    confirmed = ConfirmedIntervalMBCandidate(
        label="confirmed_M_B_interval_context_harmony_candidate",
        source_diagnostic_label=diagnostic.label,
        confirmed_mb=True,
        core_promoted=False,
    )
    return ConfirmedMBObservation(
        readiness,
        controller,
        confirmed,
        "confirmed_M_B_interval_candidate_observed_not_core_promotion",
    )


def compare_confirmed_mb_boundary() -> tuple[ConfirmedMBObservation, ConfirmedMBObservation]:
    readiness = readiness_observation()
    without_controller = confirm_mb_candidate(readiness, None)
    with_controller = confirm_mb_candidate(readiness, confirmation_controller_fixture())
    return without_controller, with_controller


def run_checks() -> None:
    without_controller, with_controller = compare_confirmed_mb_boundary()
    assert without_controller.status == "confirmed_M_B_not_created_without_controller"
    assert with_controller.status == "confirmed_M_B_interval_candidate_observed_not_core_promotion"
    assert with_controller.confirmed_candidate is not None
    assert with_controller.confirmed_candidate.confirmed_mb is True
    assert with_controller.confirmed_candidate.core_promoted is False
    assert with_controller.confirmation_controller is not None
    assert with_controller.confirmation_controller.generated_by_readiness is False


if __name__ == "__main__":
    run_checks()
    print(compare_confirmed_mb_boundary()[1])
