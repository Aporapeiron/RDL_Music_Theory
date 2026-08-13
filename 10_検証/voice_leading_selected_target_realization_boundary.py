"""selected targetから既存の具体音実現構造へ接続する最小検証。

43では、外部入力されたtarget候補集合からselected targetが生じる境界を確認した。
44では、新しい声部進行理論を作らず、selected targetを既存14の
target degree -> concrete pitch realization構造へ接続できるかだけを確認する。

    selected target
      -> target degree plan (externally supplied fixture)
      -> existing realization request
      -> degree_to_pitch_realization.realize_pair()
      -> concrete target pair

selected targetはconcrete pitchではない。
"""

from dataclasses import dataclass

from degree_to_pitch_realization import PairRealizationObservation, build_requests, realize_pair
from harmonic_function_target_candidate_boundary import (
    TargetCandidate,
    TargetCandidateObservation,
    build_fixture,
    observe_target_candidates,
)


@dataclass(frozen=True)
class TargetDegreePlan:
    target_chord: str
    context_name: str
    lower_target_degree: int
    upper_target_degree: int
    realization_request_name: str


@dataclass(frozen=True)
class SelectedTargetRealizationConnection:
    selected_target: TargetCandidate
    degree_plan: TargetDegreePlan
    realization: PairRealizationObservation
    generated_by_selected_target: bool


def selected_target_observation() -> TargetCandidateObservation:
    function_observation, candidates = build_fixture()
    return observe_target_candidates(
        function_observation,
        candidates,
        selection_policy="prefer_primary_tonic_resolution",
    )


def fixture_degree_plan_for_selected_target(selected_target: TargetCandidate) -> TargetDegreePlan:
    """selected targetに外部fixtureとしてtarget degree planを接続する。

    selected target labelから音度や具体音を生成しない。
    現在は43のC major targetを、14のA4代表実現requestへ接続するための固定写像である。
    """

    if selected_target.target_chord != "C major":
        raise ValueError(f"no fixture degree plan for {selected_target.target_chord}")
    return TargetDegreePlan(
        target_chord="C major",
        context_name="C major",
        lower_target_degree=3,
        upper_target_degree=1,
        realization_request_name="A4 representative realization",
    )


def connect_to_existing_realization(
    target_observation: TargetCandidateObservation,
) -> SelectedTargetRealizationConnection:
    if target_observation.selected is None:
        raise ValueError("selected target is required before this fixture connection")

    degree_plan = fixture_degree_plan_for_selected_target(target_observation.selected)
    requests = {
        request.name: request
        for request in build_requests()
    }
    realization_request = requests[degree_plan.realization_request_name]
    realization = realize_pair(realization_request)
    return SelectedTargetRealizationConnection(
        selected_target=target_observation.selected,
        degree_plan=degree_plan,
        realization=realization,
        generated_by_selected_target=False,
    )


def run_checks() -> None:
    target_observation = selected_target_observation()
    assert target_observation.status == "selected_target"
    assert target_observation.selected is not None
    assert target_observation.selected.target_chord == "C major"

    connection = connect_to_existing_realization(target_observation)

    # selected targetからtarget degree planは生成していない。外部fixtureとして接続した。
    assert connection.generated_by_selected_target is False
    assert connection.degree_plan.target_chord == connection.selected_target.target_chord
    assert connection.degree_plan.lower_target_degree == 3
    assert connection.degree_plan.upper_target_degree == 1

    request = connection.realization.request
    assert request.name == "A4 representative realization"
    assert request.context.name == "C major"
    assert request.lower.target_degree == connection.degree_plan.lower_target_degree
    assert request.upper.target_degree == connection.degree_plan.upper_target_degree

    # 具体音実現は既存14のB_realization / Γ_spelling / Γ_selectで行う。
    assert tuple(note.text for note in connection.realization.generated_lower_candidates) == (
        "E3",
        "E4",
        "E5",
    )
    assert tuple(note.text for note in connection.realization.generated_upper_candidates) == (
        "C3",
        "C4",
        "C5",
        "C6",
    )
    assert len(connection.realization.admissible_pairs) > 1
    assert tuple(note.text for note in connection.realization.selected) == ("E4", "C5")
    assert (connection.realization.lower_motion, connection.realization.upper_motion) == (-1, 1)

    # selected targetはconcrete pitchではない。
    assert connection.selected_target.target_chord == "C major"
    assert connection.selected_target.target_chord != "E4-C5"


def main() -> None:
    run_checks()
    target_observation = selected_target_observation()
    connection = connect_to_existing_realization(target_observation)
    realization = connection.realization
    print("[pipeline]")
    print("  selected target from 43")
    print("  -> externally supplied target degree plan")
    print("  -> existing 14 realization request")
    print("  -> concrete target pair")
    print(f"  selected_target={connection.selected_target.target_chord}")
    print(f"  generated_by_selected_target={connection.generated_by_selected_target}")
    print(
        "  target_degrees="
        f"{connection.degree_plan.lower_target_degree} / "
        f"{connection.degree_plan.upper_target_degree}"
    )
    print(f"  realization_request={realization.request.name}")
    print(
        "  selected_concrete_target="
        f"{realization.selected[0].text}-{realization.selected[1].text}"
    )
    print(f"  motion={realization.lower_motion} / {realization.upper_motion} semitone")


if __name__ == "__main__":
    main()

