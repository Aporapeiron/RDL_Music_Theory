"""DynamicSearchStateの三断面を比較用signatureとして観測する。"""

from pitch_no_effect_controller_boundary import run_controller_boundary
from state_signature_views import (
    observe_signatures,
    same_for_candidate_generation,
    same_for_controller,
    same_for_history,
)


def run_checks() -> None:
    run = run_controller_boundary()
    source = observe_signatures(run.source_state)
    resulting = observe_signatures(run.resulting_state)

    assert run.source_state.state_id == run.resulting_state.state_id
    assert same_for_candidate_generation(run.source_state, run.resulting_state)
    assert not same_for_controller(run.source_state, run.resulting_state)
    assert same_for_history(run.source_state, run.resulting_state)

    # controller差の最小原因を、署名全体でなく既存fieldとしても残す。
    assert run.source_state.last_change_axes != run.resulting_state.last_change_axes
    assert run.source_state.last_policy_name == run.resulting_state.last_policy_name
    assert run.source_state.last_branch_kind == run.resulting_state.last_branch_kind


def main() -> None:
    run_checks()
    run = run_controller_boundary()
    source = observe_signatures(run.source_state)
    resulting = observe_signatures(run.resulting_state)
    print("[state signature observation]")
    print(f"state_id_same={run.source_state.state_id == run.resulting_state.state_id}")
    print(f"candidate_generation_same={source.candidate_generation == resulting.candidate_generation}")
    print(f"controller_same={source.controller == resulting.controller}")
    print(f"history_same={source.history == resulting.history}")


if __name__ == "__main__":
    main()
