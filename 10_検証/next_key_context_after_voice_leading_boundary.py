"""voice leading resultからnext key/contextを自動確定しない最小検証。

44では、43のselected targetを既存14の具体音実現構造へ接続した。
45では、その結果として得たconcrete voice leading resultを、
next key/context interpretationへ直結しない境界を確認する。

    voice leading result
      -> next context候補集合 (externally supplied fixture)
      -> interpretation observed
      -> optional selection policy

voice leading resultはnext key/context interpretationではない。
"""

from dataclasses import dataclass

from voice_leading_selected_target_realization_boundary import (
    SelectedTargetRealizationConnection,
    connect_to_existing_realization,
    selected_target_observation,
)


@dataclass(frozen=True)
class VoiceLeadingResult:
    selected_target: str
    concrete_target_pair: tuple[str, str]
    lower_motion: int
    upper_motion: int


@dataclass(frozen=True)
class NextContextCandidate:
    label: str
    tonic: str
    mode: str
    source: str


@dataclass(frozen=True)
class NextContextObservation:
    voice_leading_result: VoiceLeadingResult
    candidates: tuple[NextContextCandidate, ...]
    selected: NextContextCandidate | None
    status: str
    generated_by_voice_leading: bool


def voice_leading_result_from_44() -> VoiceLeadingResult:
    target_observation = selected_target_observation()
    connection = connect_to_existing_realization(target_observation)
    return result_from_connection(connection)


def result_from_connection(connection: SelectedTargetRealizationConnection) -> VoiceLeadingResult:
    realization = connection.realization
    return VoiceLeadingResult(
        selected_target=connection.selected_target.target_chord,
        concrete_target_pair=tuple(note.text for note in realization.selected),
        lower_motion=realization.lower_motion,
        upper_motion=realization.upper_motion,
    )


def fixture_next_context_candidates() -> tuple[NextContextCandidate, ...]:
    """next context候補集合を外部fixtureとして与える。

    E4-C5やmotionから候補を生成しない。
    現在は45の境界確認用に、継続解釈と相対短調的再解釈を並べる。
    """

    return (
        NextContextCandidate(
            label="C major continuation",
            tonic="C",
            mode="major",
            source="continuation_fixture",
        ),
        NextContextCandidate(
            label="A minor reinterpretation",
            tonic="A",
            mode="minor",
            source="reinterpretation_fixture",
        ),
    )


def observe_next_context(
    voice_leading_result: VoiceLeadingResult,
    candidates: tuple[NextContextCandidate, ...],
    selection_policy: str | None = None,
) -> NextContextObservation:
    if not candidates:
        return NextContextObservation(
            voice_leading_result=voice_leading_result,
            candidates=candidates,
            selected=None,
            status="no_context_candidate",
            generated_by_voice_leading=False,
        )

    if selection_policy is None:
        return NextContextObservation(
            voice_leading_result=voice_leading_result,
            candidates=candidates,
            selected=None,
            status="underdetermined",
            generated_by_voice_leading=False,
        )

    if selection_policy != "prefer_continuation_fixture":
        raise ValueError(f"unknown selection_policy: {selection_policy}")

    selected_candidates = [
        candidate
        for candidate in candidates
        if candidate.source == "continuation_fixture"
    ]
    if len(selected_candidates) != 1:
        return NextContextObservation(
            voice_leading_result=voice_leading_result,
            candidates=candidates,
            selected=None,
            status="selection_ambiguous",
            generated_by_voice_leading=False,
        )

    return NextContextObservation(
        voice_leading_result=voice_leading_result,
        candidates=candidates,
        selected=selected_candidates[0],
        status="selected_next_context",
        generated_by_voice_leading=False,
    )


def run_checks() -> None:
    result = voice_leading_result_from_44()
    assert result.selected_target == "C major"
    assert result.concrete_target_pair == ("E4", "C5")
    assert (result.lower_motion, result.upper_motion) == (-1, 1)

    candidates = fixture_next_context_candidates()
    assert len(candidates) == 2
    assert {candidate.label for candidate in candidates} == {
        "C major continuation",
        "A minor reinterpretation",
    }

    unselected = observe_next_context(result, candidates)
    assert unselected.status == "underdetermined"
    assert unselected.selected is None
    assert unselected.generated_by_voice_leading is False

    selected = observe_next_context(
        result,
        candidates,
        selection_policy="prefer_continuation_fixture",
    )
    assert selected.status == "selected_next_context"
    assert selected.selected is not None
    assert selected.selected.label == "C major continuation"
    assert selected.generated_by_voice_leading is False

    empty = observe_next_context(result, tuple())
    assert empty.status == "no_context_candidate"
    assert empty.selected is None
    assert empty.generated_by_voice_leading is False



def main() -> None:
    run_checks()
    result = voice_leading_result_from_44()
    candidates = fixture_next_context_candidates()
    unselected = observe_next_context(result, candidates)
    selected = observe_next_context(
        result,
        candidates,
        selection_policy="prefer_continuation_fixture",
    )

    print("[pipeline]")
    print("  voice leading result from 44")
    print("  -> externally supplied next context candidates")
    print("  -> interpretation observed")
    print("  -> optional selection policy")
    print(f"  selected_target={result.selected_target}")
    print(
        "  concrete_target_pair="
        f"{result.concrete_target_pair[0]}-{result.concrete_target_pair[1]}"
    )
    print(f"  motion={result.lower_motion} / {result.upper_motion} semitone")
    print(f"  generated_by_voice_leading={unselected.generated_by_voice_leading}")
    print(f"  without_policy={unselected.status}")
    print(
        "  with_policy="
        f"{selected.status}: {selected.selected.label if selected.selected else None}"
    )


if __name__ == "__main__":
    main()

