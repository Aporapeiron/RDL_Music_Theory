"""24〜26の動態境界を横断して再確認する最小検証。

各Moduleのprojectorや状態を共通化せず、既存検証器を個別に実行して、
三イベント境界とoperation_kindの保持を横断契約候補として検査する。
"""

from dynamic_adapter_boundary import (
    _events_of_kind as interval_events_of_kind,
    build_exhausted_state_without_import_side_effects,
    project_state as project_interval_state,
)
from exhaustion_fallback_observation import observe_action_set_exhaustion
from fallback_state_adoption import adopt_reopen_voice_B_boundary
from rhythm_boundary_reconstruction import run_boundary_reconstruction
from rhythm_dynamic_adapter import (
    _build_state as build_rhythm_state,
    _events_of_kind as rhythm_events_of_kind,
    project_state as project_rhythm_state,
)
from state_rebased_reexploration import run_step

EVENT_KINDS = (
    "observation",
    "structural_transition",
    "realized_transition",
)


def _check_event_contract(events: tuple[object, ...]) -> None:
    kinds = {getattr(event, "event_kind") for event in events}
    assert kinds <= set(EVENT_KINDS)
    assert all(getattr(event, "operation_kind") for event in events)
    assert all(
        getattr(event, "event_kind") != "observation"
        or getattr(event, "realization_status") == "not_realized"
        for event in events
    )
    assert all(
        getattr(event, "event_kind") != "structural_transition"
        or getattr(event, "realization_status") == "not_realized"
        for event in events
    )
    assert all(
        getattr(event, "event_kind") != "realized_transition"
        or getattr(event, "realization_status") == "realized"
        for event in events
    )


def _check_fixture_coverage(events: tuple[object, ...]) -> None:
    """今回のfixtureが三分類を一度ずつ含むことを別に確認する。"""

    kinds = {getattr(event, "event_kind") for event in events}
    assert kinds == set(EVENT_KINDS)


def _interval_events() -> tuple[object, ...]:
    exhausted = build_exhausted_state_without_import_side_effects()
    reopened = adopt_reopen_voice_B_boundary(
        exhausted,
        observe_action_set_exhaustion(exhausted),
    )
    _, _, _, continued = run_step(reopened)
    return project_interval_state(continued)


def _rhythm_events() -> tuple[object, ...]:
    return project_rhythm_state(build_rhythm_state())


def run_checks() -> None:
    interval_events = _interval_events()
    rhythm_events = _rhythm_events()
    _check_event_contract(interval_events)
    _check_event_contract(rhythm_events)
    _check_fixture_coverage(interval_events)
    _check_fixture_coverage(rhythm_events)

    assert interval_events_of_kind(interval_events, "structural_transition")
    assert rhythm_events_of_kind(rhythm_events, "structural_transition")

    boundary_run = run_boundary_reconstruction()
    assert boundary_run.observations[0].candidates == ()
    assert boundary_run.observations[1].candidates == ("休符",)
    assert boundary_run.structural_transitions[0].resulting_grid_open is True


def main() -> None:
    run_checks()
    interval_events = _interval_events()
    rhythm_events = _rhythm_events()
    print("[cross-module dynamic invariants]")
    for label, events in (("interval", interval_events), ("rhythm", rhythm_events)):
        print(
            label,
            {
                kind: len(
                    tuple(
                        event
                        for event in events
                        if event.event_kind == kind
                    )
                )
                for kind in EVENT_KINDS
            },
        )
    print("rhythm_boundary_effect=closed:() -> open:(休符,)")


if __name__ == "__main__":
    main()
