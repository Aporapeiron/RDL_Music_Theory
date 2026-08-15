"""core module input candidateと音程Module受理境界の最小検証。

68で得たcore module input candidateを固定し、音程Module側の受理境界Bと
Gamma_interval_module_receptionを与えた場合だけinterval module boundary
input candidateが生じることを確認する。音程Module内部処理は開始しない。

    core module input candidate
      + B_interval_module_reception_fixture
      + Gamma_interval_module_reception_fixture
      -> interval module boundary input candidate
      -> interval module processing remains not started
"""

from dataclasses import dataclass

from base_to_core_music_module_input_adoption_boundary import (
    CoreModuleInputAdoptionObservation,
    compare_core_module_input_adoption,
)


@dataclass(frozen=True)
class IntervalModuleReceptionBoundary:
    name: str
    accepts_module_name: str
    receiver_family: str
    rule_scope: str


@dataclass(frozen=True)
class IntervalModuleReceptionGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class IntervalModuleBoundaryInputCandidate:
    label: str
    source_core_input_label: str
    module_name: str
    interval_module_processing_started: bool
    interval_b_gamma_updated: bool
    interval_label_generated: bool


@dataclass(frozen=True)
class IntervalModuleReceptionObservation:
    core_input_observation: CoreModuleInputAdoptionObservation
    reception_boundary: IntervalModuleReceptionBoundary | None
    reception_gamma: IntervalModuleReceptionGamma | None
    interval_boundary_input: IntervalModuleBoundaryInputCandidate | None
    interval_module_processing_started: bool
    interval_b_gamma_updated: bool
    interval_label_generated: bool
    core_promoted: bool
    status: str
    reception_reason: str | None


@dataclass(frozen=True)
class IntervalModuleReceptionComparison:
    without_gamma: IntervalModuleReceptionObservation
    with_gamma: IntervalModuleReceptionObservation
    same_core_input_candidate: bool
    same_reception_boundary: bool
    same_reception_gamma: bool
    reception_observed: bool
    interval_module_processing_started: bool
    interval_b_gamma_updated: bool
    interval_label_generated: bool
    core_promoted: bool


def core_module_input_observation() -> CoreModuleInputAdoptionObservation:
    return compare_core_module_input_adoption().with_controller


def interval_module_reception_boundary() -> IntervalModuleReceptionBoundary:
    return IntervalModuleReceptionBoundary(
        name="B_interval_module_reception_fixture",
        accepts_module_name="音程_Module",
        receiver_family="pitch_relation_interpretation_receiver",
        rule_scope="fixture_limited_not_general_interval_module_boundary",
    )


def interval_module_reception_gamma() -> IntervalModuleReceptionGamma:
    return IntervalModuleReceptionGamma(
        name="Gamma_interval_module_reception_fixture",
        reads=("core_module_input_candidate", "B_interval_module_reception"),
        rule_scope="fixture_limited_not_interval_module_processing_rule",
    )


def receive_interval_module_input(
    core_input_observation: CoreModuleInputAdoptionObservation,
    reception_boundary: IntervalModuleReceptionBoundary | None,
    reception_gamma: IntervalModuleReceptionGamma | None,
) -> IntervalModuleReceptionObservation:
    core_input = core_input_observation.core_module_input
    if core_input is None:
        return IntervalModuleReceptionObservation(
            core_input_observation=core_input_observation,
            reception_boundary=reception_boundary,
            reception_gamma=reception_gamma,
            interval_boundary_input=None,
            interval_module_processing_started=False,
            interval_b_gamma_updated=False,
            interval_label_generated=False,
            core_promoted=False,
            status="no_core_module_input_candidate",
            reception_reason=None,
        )

    if reception_boundary is None:
        return IntervalModuleReceptionObservation(
            core_input_observation=core_input_observation,
            reception_boundary=None,
            reception_gamma=reception_gamma,
            interval_boundary_input=None,
            interval_module_processing_started=False,
            interval_b_gamma_updated=False,
            interval_label_generated=False,
            core_promoted=False,
            status="core_input_not_received_without_boundary",
            reception_reason=None,
        )

    if reception_gamma is None:
        return IntervalModuleReceptionObservation(
            core_input_observation=core_input_observation,
            reception_boundary=reception_boundary,
            reception_gamma=None,
            interval_boundary_input=None,
            interval_module_processing_started=False,
            interval_b_gamma_updated=False,
            interval_label_generated=False,
            core_promoted=False,
            status="core_input_not_received_without_gamma",
            reception_reason=None,
        )

    if core_input.module_name != reception_boundary.accepts_module_name:
        return IntervalModuleReceptionObservation(
            core_input_observation=core_input_observation,
            reception_boundary=reception_boundary,
            reception_gamma=reception_gamma,
            interval_boundary_input=None,
            interval_module_processing_started=False,
            interval_b_gamma_updated=False,
            interval_label_generated=False,
            core_promoted=False,
            status="core_input_not_accepted_by_interval_boundary",
            reception_reason=None,
        )

    received = IntervalModuleBoundaryInputCandidate(
        label="interval_module_received_pitch_relation_candidate",
        source_core_input_label=core_input.input_label,
        module_name=core_input.module_name,
        interval_module_processing_started=False,
        interval_b_gamma_updated=False,
        interval_label_generated=False,
    )
    return IntervalModuleReceptionObservation(
        core_input_observation=core_input_observation,
        reception_boundary=reception_boundary,
        reception_gamma=reception_gamma,
        interval_boundary_input=received,
        interval_module_processing_started=False,
        interval_b_gamma_updated=False,
        interval_label_generated=False,
        core_promoted=False,
        status="interval_module_boundary_input_observed_not_processed",
        reception_reason="core_input_matches_interval_reception_boundary",
    )


def compare_interval_module_reception() -> IntervalModuleReceptionComparison:
    core_input = core_module_input_observation()
    boundary = interval_module_reception_boundary()
    without_gamma = receive_interval_module_input(
        core_input_observation=core_input,
        reception_boundary=boundary,
        reception_gamma=None,
    )
    with_gamma = receive_interval_module_input(
        core_input_observation=core_input,
        reception_boundary=boundary,
        reception_gamma=interval_module_reception_gamma(),
    )
    return IntervalModuleReceptionComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_core_input_candidate=(
            without_gamma.core_input_observation.core_module_input
            == with_gamma.core_input_observation.core_module_input
        ),
        same_reception_boundary=(
            without_gamma.reception_boundary == with_gamma.reception_boundary
        ),
        same_reception_gamma=without_gamma.reception_gamma == with_gamma.reception_gamma,
        reception_observed=(
            with_gamma.status
            == "interval_module_boundary_input_observed_not_processed"
        ),
        interval_module_processing_started=(
            with_gamma.interval_module_processing_started
        ),
        interval_b_gamma_updated=with_gamma.interval_b_gamma_updated,
        interval_label_generated=with_gamma.interval_label_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_interval_module_reception()
    assert comparison.same_core_input_candidate is True
    assert comparison.same_reception_boundary is True
    assert comparison.same_reception_gamma is False
    assert comparison.reception_observed is True
    assert comparison.interval_module_processing_started is False
    assert comparison.interval_b_gamma_updated is False
    assert comparison.interval_label_generated is False
    assert comparison.core_promoted is False

    assert comparison.without_gamma.status == "core_input_not_received_without_gamma"
    assert comparison.without_gamma.interval_boundary_input is None

    assert (
        comparison.with_gamma.status
        == "interval_module_boundary_input_observed_not_processed"
    )
    assert comparison.with_gamma.interval_boundary_input is not None
    assert comparison.with_gamma.interval_boundary_input.label == (
        "interval_module_received_pitch_relation_candidate"
    )
    assert comparison.with_gamma.interval_boundary_input.module_name == "音程_Module"
    assert (
        comparison.with_gamma.interval_boundary_input.interval_module_processing_started
        is False
    )
    assert comparison.with_gamma.interval_boundary_input.interval_b_gamma_updated is False
    assert comparison.with_gamma.interval_boundary_input.interval_label_generated is False
    assert comparison.with_gamma.reception_reason == (
        "core_input_matches_interval_reception_boundary"
    )


def main() -> None:
    run_checks()
    comparison = compare_interval_module_reception()
    with_gamma = comparison.with_gamma

    print("[pipeline]")
    print("  core module input candidate")
    print("  + B_interval_module_reception_fixture")
    print("  + Gamma_interval_module_reception_fixture")
    print("  -> interval module boundary input candidate")
    print("  -> interval module processing remains not started")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_core_input_candidate={comparison.same_core_input_candidate}")
    print(f"  same_reception_boundary={comparison.same_reception_boundary}")
    print(f"  same_reception_gamma={comparison.same_reception_gamma}")
    print(f"  reception_observed={comparison.reception_observed}")
    print(
        "  core_module_input_candidate="
        + (
            with_gamma.core_input_observation.core_module_input.input_label
            if with_gamma.core_input_observation.core_module_input
            else "None"
        )
    )
    print(
        "  interval_boundary_input="
        + (
            with_gamma.interval_boundary_input.label
            if with_gamma.interval_boundary_input
            else "None"
        )
    )
    print(
        "  interval_module_processing_started="
        f"{comparison.interval_module_processing_started}"
    )
    print(f"  interval_b_gamma_updated={comparison.interval_b_gamma_updated}")
    print(f"  interval_label_generated={comparison.interval_label_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
