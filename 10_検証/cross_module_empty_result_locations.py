"""32・33の空結果がどのModule固有段階で生じたかを比較する。

共通のempty段階語彙は作らない。各Moduleが実際に保持する観測から、生候補が
存在したこと、最終結果が空であること、空にしたModule固有の段階を別々に読む。
"""

from dataclasses import dataclass

from pitch_transition_projection_empty_regeneration import run_empty_regeneration as run_pitch
from rhythm_transition_projection_empty_regeneration import run_empty_regeneration as run_rhythm


@dataclass(frozen=True)
class EmptyResultLocationObservation:
    module_name: str
    raw_candidate_observed: bool
    final_result_empty: bool
    module_empty_evidence: tuple[str, ...]


def run_empty_result_locations() -> tuple[EmptyResultLocationObservation, ...]:
    pitch = run_pitch()
    rhythm = run_rhythm()
    pitch_raw_count = sum(
        len(item.observation.generated_voice_a_candidates)
        + len(item.observation.generated_voice_b_candidates)
        for item in pitch.observations
    )
    return (
        EmptyResultLocationObservation(
            module_name="pitch",
            raw_candidate_observed=pitch_raw_count > 0,
            final_result_empty=sum(
                item.observation.selected is not None
                for item in pitch.observations
            ) == 0,
            module_empty_evidence=tuple(
                sorted(
                    {
                        item.observation.failure_stage
                        for item in pitch.observations
                        if item.observation.failure_stage is not None
                    }
                )
            ),
        ),
        EmptyResultLocationObservation(
            module_name="rhythm",
            raw_candidate_observed=bool(rhythm.raw_candidate_space),
            final_result_empty=not rhythm.constrained_candidates,
            module_empty_evidence=(
                f"current={rhythm.current}",
                f"change_current={rhythm.change_current}",
                f"target={rhythm.target}",
            ),
        ),
    )


def run_checks() -> None:
    observations = run_empty_result_locations()
    assert tuple(item.module_name for item in observations) == ("pitch", "rhythm")
    assert all(item.raw_candidate_observed for item in observations)
    assert all(item.final_result_empty for item in observations)
    assert observations[0].module_empty_evidence == ("B_range_projection",)
    assert observations[1].module_empty_evidence == (
        "current=休符",
        "change_current=True",
        "target=休符",
    )


def main() -> None:
    run_checks()
    print("[cross-module empty result locations]")
    for observation in run_empty_result_locations():
        print(
            f"{observation.module_name}: "
            f"raw_candidate_observed={observation.raw_candidate_observed} "
            f"final_result_empty={observation.final_result_empty} "
            f"module_empty_evidence={observation.module_empty_evidence}"
        )


if __name__ == "__main__":
    main()
