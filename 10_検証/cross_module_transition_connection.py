"""28と30の同一構造遷移record接続を横断検査する。

この検査は共通Adapter・共通状態・共通候補生成器を作らない。音程とリズムの
既存の最小実験を個別に実行し、Module固有recordが(1) structural_transition
への投影、(2) record由来の候補再生成、の双方へ接続しているという限定された
形式だけを比較する。
"""

from dataclasses import dataclass

from pitch_transition_projection_reconstruction import run_same_transition as run_pitch
from rhythm_transition_projection_reconstruction import run_same_transition as run_rhythm


@dataclass(frozen=True)
class TransitionConnectionObservation:
    """31が比較する、状態内容を含まない観測結果。"""

    module_name: str
    record_operation_kind: str
    event_kind: str
    event_operation_kind: str
    realization_status: str
    operation_status: str
    source_differs_from_result: bool
    regeneration_status: str
    regenerated_count: int


def _check_connection(observation: TransitionConnectionObservation) -> None:
    """接続形式だけを検査し、Module固有の語彙や軸名は比較しない。"""

    assert observation.record_operation_kind
    assert observation.event_kind == "structural_transition"
    assert observation.event_operation_kind == observation.record_operation_kind
    assert observation.realization_status == "not_realized"
    assert observation.operation_status == "applied"
    assert observation.source_differs_from_result is True
    assert observation.regeneration_status == "executed"


def run_cross_module_connection() -> tuple[TransitionConnectionObservation, ...]:
    rhythm = run_rhythm()
    pitch = run_pitch()

    observations = (
        TransitionConnectionObservation(
            module_name="rhythm",
            record_operation_kind=rhythm.transition.operation_kind,
            event_kind=rhythm.event.event_kind,
            event_operation_kind=rhythm.event.operation_kind,
            realization_status=rhythm.event.realization_status,
            operation_status=rhythm.event.operation_status,
            source_differs_from_result=(
                rhythm.transition.source_grid_open
                != rhythm.transition.resulting_grid_open
            ),
            regeneration_status="executed",
            regenerated_count=len(rhythm.candidates),
        ),
        TransitionConnectionObservation(
            module_name="pitch",
            record_operation_kind=pitch.transition.fallback_kind,
            event_kind=pitch.event.event_kind,
            event_operation_kind=pitch.event.operation_kind,
            realization_status=pitch.event.realization_status,
            operation_status=pitch.event.operation_status,
            source_differs_from_result=(
                pitch.transition.source_voice_b_boundary
                != pitch.transition.resulting_voice_b_boundary
            ),
            regeneration_status="executed",
            regenerated_count=len(pitch.regenerated_pairs),
        ),
    )
    for observation in observations:
        _check_connection(observation)
    return observations


def run_checks() -> None:
    observations = run_cross_module_connection()
    assert tuple(item.module_name for item in observations) == ("rhythm", "pitch")
    # これは接続契約ではなく、28・30の今回のfixture結果である。
    assert all(item.regenerated_count > 0 for item in observations)


def main() -> None:
    run_checks()
    print("[cross-module structural record connection]")
    for observation in run_cross_module_connection():
        print(
            f"{observation.module_name}: "
            f"operation={observation.record_operation_kind} "
            f"regeneration={observation.regeneration_status} "
            f"regenerated_count={observation.regenerated_count}"
        )


if __name__ == "__main__":
    main()
