"""音程Module selected consistencyとmodule state record境界の最小検証。"""

from dataclasses import dataclass

from interval_module_context_harmony_consistency_selection import (
    ContextHarmonyConsistencySelectionObservation,
    compare_consistency_selection,
)


@dataclass(frozen=True)
class IntervalModuleStateRecordBoundary:
    name: str
    record_scope: str
    generated_by_selected_consistency: bool


@dataclass(frozen=True)
class IntervalModuleStateRecordGamma:
    name: str
    reads: tuple[str, str]
    rule_scope: str


@dataclass(frozen=True)
class IntervalModuleStateRecordCandidate:
    label: str
    source_selected_consistency_label: str
    record_scope: str
    confirmed_mb: bool
    core_promoted: bool


@dataclass(frozen=True)
class IntervalModuleStateRecordObservation:
    consistency_selection_observation: ContextHarmonyConsistencySelectionObservation
    record_boundary: IntervalModuleStateRecordBoundary | None
    gamma_state_record: IntervalModuleStateRecordGamma | None
    state_record: IntervalModuleStateRecordCandidate | None
    confirmed_mb: bool
    core_promoted: bool
    status: str
    record_reason: str | None


@dataclass(frozen=True)
class IntervalModuleStateRecordComparison:
    without_gamma: IntervalModuleStateRecordObservation
    with_gamma: IntervalModuleStateRecordObservation
    same_selected_consistency: bool
    same_record_boundary: bool
    same_gamma_state_record: bool
    state_record_observed: bool
    confirmed_mb: bool
    core_promoted: bool


def consistency_selection_observation() -> ContextHarmonyConsistencySelectionObservation:
    return compare_consistency_selection().with_controller


def record_boundary_fixture() -> IntervalModuleStateRecordBoundary:
    return IntervalModuleStateRecordBoundary(
        name="B_interval_module_state_record_fixture",
        record_scope="context_harmony_consistency_record",
        generated_by_selected_consistency=False,
    )


def gamma_state_record_fixture() -> IntervalModuleStateRecordGamma:
    return IntervalModuleStateRecordGamma(
        name="Gamma_interval_module_state_record_fixture",
        reads=("selected_consistency", "external_record_boundary"),
        rule_scope="fixture_limited_not_confirmed_M_B_or_core_promotion_rule",
    )


def create_state_record(
    consistency_selection: ContextHarmonyConsistencySelectionObservation,
    record_boundary: IntervalModuleStateRecordBoundary | None,
    gamma_state_record: IntervalModuleStateRecordGamma | None,
) -> IntervalModuleStateRecordObservation:
    selected = consistency_selection.selected_consistency
    if selected is None:
        return IntervalModuleStateRecordObservation(
            consistency_selection_observation=consistency_selection,
            record_boundary=record_boundary,
            gamma_state_record=gamma_state_record,
            state_record=None,
            confirmed_mb=False,
            core_promoted=False,
            status="no_selected_consistency_candidate",
            record_reason=None,
        )
    if record_boundary is None:
        return IntervalModuleStateRecordObservation(
            consistency_selection_observation=consistency_selection,
            record_boundary=None,
            gamma_state_record=gamma_state_record,
            state_record=None,
            confirmed_mb=False,
            core_promoted=False,
            status="state_record_not_created_without_record_boundary",
            record_reason=None,
        )
    if gamma_state_record is None:
        return IntervalModuleStateRecordObservation(
            consistency_selection_observation=consistency_selection,
            record_boundary=record_boundary,
            gamma_state_record=None,
            state_record=None,
            confirmed_mb=False,
            core_promoted=False,
            status="state_record_not_created_without_gamma",
            record_reason=None,
        )

    record = IntervalModuleStateRecordCandidate(
        label="interval_module_context_harmony_state_record_candidate",
        source_selected_consistency_label=selected.label,
        record_scope=record_boundary.record_scope,
        confirmed_mb=False,
        core_promoted=False,
    )
    return IntervalModuleStateRecordObservation(
        consistency_selection_observation=consistency_selection,
        record_boundary=record_boundary,
        gamma_state_record=gamma_state_record,
        state_record=record,
        confirmed_mb=False,
        core_promoted=False,
        status="interval_module_state_record_candidate_observed_not_confirmed",
        record_reason="selected_consistency_and_external_record_boundary_read_by_Gamma_interval_module_state_record",
    )


def compare_state_record_creation() -> IntervalModuleStateRecordComparison:
    consistency_selection = consistency_selection_observation()
    boundary = record_boundary_fixture()
    without_gamma = create_state_record(consistency_selection, boundary, None)
    with_gamma = create_state_record(
        consistency_selection, boundary, gamma_state_record_fixture()
    )
    return IntervalModuleStateRecordComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_selected_consistency=(
            without_gamma.consistency_selection_observation.selected_consistency
            == with_gamma.consistency_selection_observation.selected_consistency
        ),
        same_record_boundary=without_gamma.record_boundary == with_gamma.record_boundary,
        same_gamma_state_record=(
            without_gamma.gamma_state_record == with_gamma.gamma_state_record
        ),
        state_record_observed=(
            with_gamma.status
            == "interval_module_state_record_candidate_observed_not_confirmed"
        ),
        confirmed_mb=with_gamma.confirmed_mb,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_state_record_creation()
    assert comparison.same_selected_consistency is True
    assert comparison.same_record_boundary is True
    assert comparison.same_gamma_state_record is False
    assert comparison.state_record_observed is True
    assert comparison.confirmed_mb is False
    assert comparison.core_promoted is False
    assert comparison.without_gamma.status == "state_record_not_created_without_gamma"
    assert comparison.without_gamma.state_record is None
    assert comparison.with_gamma.state_record is not None
    assert comparison.with_gamma.state_record.label == (
        "interval_module_context_harmony_state_record_candidate"
    )
    assert comparison.with_gamma.state_record.confirmed_mb is False
    assert comparison.with_gamma.state_record.core_promoted is False
    assert comparison.with_gamma.record_boundary is not None
    assert comparison.with_gamma.record_boundary.generated_by_selected_consistency is False


def main() -> None:
    run_checks()
    comparison = compare_state_record_creation()
    with_gamma = comparison.with_gamma
    print("[pipeline]")
    print("  selected consistency candidate")
    print("  + external record boundary")
    print("  + Gamma_interval_module_state_record_fixture")
    print("  -> interval module state record candidate")
    print("  -> confirmed M_B and Core promotion remain False")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_selected_consistency={comparison.same_selected_consistency}")
    print(f"  same_record_boundary={comparison.same_record_boundary}")
    print(f"  same_gamma_state_record={comparison.same_gamma_state_record}")
    print(f"  state_record_observed={comparison.state_record_observed}")
    print(
        "  state_record="
        + (with_gamma.state_record.label if with_gamma.state_record else "None")
    )
    print(f"  confirmed_mb={comparison.confirmed_mb}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
