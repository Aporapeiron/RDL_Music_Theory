"""和声機能注釈とtarget候補集合・選択境界の最小検証。

42では、function annotation candidateを得てもtargetを生成しないことを確認した。
43では、target候補集合を外部入力として与えた場合に、
候補集合の観測と選択規則による採用がどこで分かれるかだけを確認する。

    function annotation candidate
      + externally supplied target candidate set
      -> target candidates observed
      -> Γ_selectがなければunderdetermined
      -> Γ_selectがある場合だけselected target

function annotationはtarget候補集合の生成器ではない。
"""

from dataclasses import dataclass

from harmonic_function_key_context_branch import (
    FunctionObservation,
    KeyContext,
    annotate_function,
    make_major_triad,
)


@dataclass(frozen=True)
class TargetCandidate:
    label: str
    target_chord: str
    source: str


@dataclass(frozen=True)
class TargetCandidateObservation:
    function_observation: FunctionObservation
    candidates: tuple[TargetCandidate, ...]
    selected: TargetCandidate | None
    status: str
    selection_policy: str | None
    generated_by_function: bool


def observe_target_candidates(
    function_observation: FunctionObservation,
    externally_supplied_candidates: tuple[TargetCandidate, ...],
    *,
    selection_policy: str | None = None,
) -> TargetCandidateObservation:
    """外部入力されたtarget候補集合を観測し、必要なら明示ポリシーで選択する。

    target候補集合はfunction annotationから生成しない。
    selection_policyがない場合、候補数が複数ならunderdeterminedとして保持する。
    """

    candidates = externally_supplied_candidates
    selected: TargetCandidate | None = None

    if not candidates:
        status = "no_candidate"
    elif selection_policy is None:
        status = "locally_resolved" if len(candidates) == 1 else "underdetermined"
    elif selection_policy == "prefer_primary_tonic_resolution":
        primary = [candidate for candidate in candidates if candidate.source == "primary"]
        if len(primary) == 1:
            selected = primary[0]
            status = "selected_target"
        elif len(primary) > 1:
            status = "underdetermined"
        else:
            status = "no_candidate"
    else:
        raise ValueError(f"unknown selection policy: {selection_policy}")

    return TargetCandidateObservation(
        function_observation=function_observation,
        candidates=candidates,
        selected=selected,
        status=status,
        selection_policy=selection_policy,
        generated_by_function=False,
    )


def build_fixture() -> tuple[FunctionObservation, tuple[TargetCandidate, ...]]:
    function_observation = annotate_function(make_major_triad("G"), KeyContext("C major", "C"))
    candidates = (
        TargetCandidate(
            label="primary tonic resolution candidate",
            target_chord="C major",
            source="primary",
        ),
        TargetCandidate(
            label="deceptive resolution candidate",
            target_chord="A minor",
            source="alternative",
        ),
    )
    return function_observation, candidates


def run_checks() -> None:
    function_observation, candidates = build_fixture()

    assert function_observation.function_annotation == "dominant_candidate"
    assert function_observation.generated_target is None

    unselected = observe_target_candidates(function_observation, candidates)
    assert unselected.generated_by_function is False
    assert unselected.candidates == candidates
    assert unselected.selected is None
    assert unselected.status == "underdetermined"
    assert unselected.selection_policy is None

    selected = observe_target_candidates(
        function_observation,
        candidates,
        selection_policy="prefer_primary_tonic_resolution",
    )
    assert selected.generated_by_function is False
    assert selected.status == "selected_target"
    assert selected.selected is not None
    assert selected.selected.target_chord == "C major"
    assert selected.selection_policy == "prefer_primary_tonic_resolution"

    singleton = observe_target_candidates(function_observation, candidates[:1])
    assert singleton.status == "locally_resolved"
    assert singleton.selected is None

    empty = observe_target_candidates(function_observation, ())
    assert empty.status == "no_candidate"
    assert empty.selected is None


def print_observation(observation: TargetCandidateObservation) -> None:
    function = observation.function_observation
    print(f"[{function.function_annotation}] {function.key_context.label}")
    print(f"  chord={function.chord.label}")
    print(f"  generated_by_function={observation.generated_by_function}")
    print(f"  selection_policy={observation.selection_policy}")
    print(f"  candidate_count={len(observation.candidates)}")
    print(f"  status={observation.status}")
    selected = observation.selected.target_chord if observation.selected else None
    print(f"  selected_target={selected}")
    print("  candidates=" + ", ".join(candidate.target_chord for candidate in observation.candidates))


def main() -> None:
    run_checks()
    function_observation, candidates = build_fixture()
    print("[pipeline]")
    print("  function annotation candidate")
    print("  + externally supplied target candidate set")
    print("  -> observe candidates")
    print("  -> selection only with explicit Gamma_select")
    unselected = observe_target_candidates(function_observation, candidates)
    selected = observe_target_candidates(
        function_observation,
        candidates,
        selection_policy="prefer_primary_tonic_resolution",
    )
    print_observation(unselected)
    print_observation(selected)
    print("[comparison]")
    print(f"  same_function_observation={unselected.function_observation == selected.function_observation}")
    print(f"  target_generated_by_function={unselected.generated_by_function or selected.generated_by_function}")
    print(f"  statuses={unselected.status} / {selected.status}")


if __name__ == "__main__":
    main()

