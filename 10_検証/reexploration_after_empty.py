"""空集合後の再探索分岐を観測する最小検証。

15では、候補がどの段階で消えたかを診断した。
16では、同じ空集合状態から、B変更・Γ変更・上流target変更を別分岐として
再適用し、それぞれが異なる候補集合と具体targetへ戻りうることを記録する。

empty under current B / Γ
      -> B change      -> new candidates
      -> Γ change      -> relaxed relation
      -> upstream target change -> new target candidates

これは、どの分岐を優先するかを決める規則ではない。
その優先順位と採用条件は未解決のまま保持する。
"""

from dataclasses import dataclass, replace

from degree_to_pitch_realization import (
    PairRealizationRequest,
    RealizationBoundary,
    SpelledNote,
    VoiceRange,
    build_requests,
    filter_voice_range,
    generate_spelled_candidates,
    select_nearest_pair,
)


@dataclass(frozen=True)
class ChangeAxes:
    """枝が実際に変更した対象を、枝名から独立して保持する。"""

    boundary_changed: bool = False
    relation_changed: bool = False
    upstream_target_changed: bool = False


@dataclass(frozen=True)
class ReexplorationObservation:
    """再探索一回分の候補段階と分岐理由を保持する。"""

    branch_kind: str
    change_layer: str
    change_axes: ChangeAxes
    action: str
    pitch_ordering_rule: str
    request: PairRealizationRequest
    generated_voice_a_candidates: tuple[SpelledNote, ...]
    generated_voice_b_candidates: tuple[SpelledNote, ...]
    filtered_voice_a_candidates: tuple[SpelledNote, ...]
    filtered_voice_b_candidates: tuple[SpelledNote, ...]
    admissible_voice_pairs: tuple[tuple[SpelledNote, SpelledNote], ...]
    selected: tuple[SpelledNote, SpelledNote] | None
    failure_stage: str | None
    failure_reason: str | None

    @property
    def status(self) -> str:
        if self.selected is not None:
            return "selected"
        if not self.filtered_voice_a_candidates or not self.filtered_voice_b_candidates:
            return "constraint_no_candidate"
        if not self.admissible_voice_pairs:
            return "no_admissible_candidate"
        return "unselected"


def build_pitch_ordered_pairs(
    voice_a_candidates: tuple[SpelledNote, ...],
    voice_b_candidates: tuple[SpelledNote, ...],
) -> tuple[tuple[SpelledNote, SpelledNote], ...]:
    """Γ_ordering：voice A/Bの実音高がA < Bとなる候補対を作る。

    候補対のタプル位置は声部ID（voice A, voice B）を保持する。
    ここで比較しているのは声部IDではなく、各候補の実音高である。
    """

    return tuple(
        (voice_a, voice_b)
        for voice_a in voice_a_candidates
        for voice_b in voice_b_candidates
        if voice_a.chromatic_index < voice_b.chromatic_index
    )


def observe_request(
    request: PairRealizationRequest,
    *,
    branch_kind: str,
    change_layer: str,
    change_axes: ChangeAxes,
    action: str,
    pitch_ordering_rule: str = "strict_voice_a_pitch_lt_voice_b_pitch",
) -> ReexplorationObservation:
    """一つのB・Γ条件で候補を再展開する。"""

    # 14のPairRealizationRequestはlower/upperという既存フィールドを持つ。
    # 16ではそれを声部IDとして受け、物理的上下はpitch_ordering_ruleに分離する。
    voice_a_request = request.lower
    voice_b_request = request.upper

    generated_voice_a = generate_spelled_candidates(
        request.context,
        voice_a_request.target_degree,
        voice_a_request.boundary.candidate_octaves,
    )
    generated_voice_b = generate_spelled_candidates(
        request.context,
        voice_b_request.target_degree,
        voice_b_request.boundary.candidate_octaves,
    )
    filtered_voice_a = filter_voice_range(
        generated_voice_a,
        voice_a_request.boundary.voice_range,
    )
    filtered_voice_b = filter_voice_range(
        generated_voice_b,
        voice_b_request.boundary.voice_range,
    )

    if not filtered_voice_a:
        return ReexplorationObservation(
            branch_kind=branch_kind,
            change_layer=change_layer,
            change_axes=change_axes,
            action=action,
            pitch_ordering_rule=pitch_ordering_rule,
            request=request,
            generated_voice_a_candidates=generated_voice_a,
            generated_voice_b_candidates=generated_voice_b,
            filtered_voice_a_candidates=filtered_voice_a,
            filtered_voice_b_candidates=filtered_voice_b,
            admissible_voice_pairs=(),
            selected=None,
            failure_stage="B_range_projection",
            failure_reason="voice A range removed every generated candidate",
        )
    if not filtered_voice_b:
        return ReexplorationObservation(
            branch_kind=branch_kind,
            change_layer=change_layer,
            change_axes=change_axes,
            action=action,
            pitch_ordering_rule=pitch_ordering_rule,
            request=request,
            generated_voice_a_candidates=generated_voice_a,
            generated_voice_b_candidates=generated_voice_b,
            filtered_voice_a_candidates=filtered_voice_a,
            filtered_voice_b_candidates=filtered_voice_b,
            admissible_voice_pairs=(),
            selected=None,
            failure_stage="B_range_projection",
            failure_reason="voice B range removed every generated candidate",
        )

    if pitch_ordering_rule == "strict_voice_a_pitch_lt_voice_b_pitch":
        admissible_voice_pairs = build_pitch_ordered_pairs(
            filtered_voice_a,
            filtered_voice_b,
        )
    elif pitch_ordering_rule == "allow_crossed_voice_pitches":
        # Γの変更を観測するための比較条件。音楽的妥当性は主張しない。
        admissible_voice_pairs = tuple(
            (voice_a, voice_b)
            for voice_a in filtered_voice_a
            for voice_b in filtered_voice_b
        )
    else:
        raise ValueError(f"unknown pitch ordering rule: {pitch_ordering_rule}")

    if not admissible_voice_pairs:
        return ReexplorationObservation(
            branch_kind=branch_kind,
            change_layer=change_layer,
            change_axes=change_axes,
            action=action,
            pitch_ordering_rule=pitch_ordering_rule,
            request=request,
            generated_voice_a_candidates=generated_voice_a,
            generated_voice_b_candidates=generated_voice_b,
            filtered_voice_a_candidates=filtered_voice_a,
            filtered_voice_b_candidates=filtered_voice_b,
            admissible_voice_pairs=admissible_voice_pairs,
            selected=None,
            failure_stage="Γ_ordering",
            failure_reason="current ordering rule removed every candidate pair",
        )

    return ReexplorationObservation(
        branch_kind=branch_kind,
        change_layer=change_layer,
        change_axes=change_axes,
        action=action,
        pitch_ordering_rule=pitch_ordering_rule,
        request=request,
        generated_voice_a_candidates=generated_voice_a,
        generated_voice_b_candidates=generated_voice_b,
        filtered_voice_a_candidates=filtered_voice_a,
        filtered_voice_b_candidates=filtered_voice_b,
        admissible_voice_pairs=admissible_voice_pairs,
        selected=select_nearest_pair(request, admissible_voice_pairs),
        failure_stage=None,
        failure_reason=None,
    )


def build_seed_request() -> PairRealizationRequest:
    """同じ空集合から三分岐を作るための最小seed。"""

    base = build_requests()[1]
    return replace(
        base,
        name="reexploration seed: ordering conflict",
        lower=replace(
            base.lower,
            start=SpelledNote("A", accidental=1, octave=4),
            target_degree=3,
            boundary=RealizationBoundary(
                candidate_octaves=(4,),
                voice_range=VoiceRange(
                    SpelledNote("E", accidental=1, octave=4),
                    SpelledNote("A", accidental=1, octave=4),
                ),
            ),
        ),
        upper=replace(
            base.upper,
            start=SpelledNote("F", accidental=1, octave=4),
            target_degree=1,
            boundary=RealizationBoundary(
                candidate_octaves=(4,),
                voice_range=VoiceRange(
                    SpelledNote("F", accidental=1, octave=4),
                    SpelledNote("F", accidental=1, octave=4),
                ),
            ),
        ),
    )


def build_reexploration_observations() -> tuple[
    ReexplorationObservation,
    ReexplorationObservation,
    ReexplorationObservation,
    ReexplorationObservation,
]:
    """seedと、B・Γ・targetの三つの再探索分岐を構成する。"""

    seed = build_seed_request()
    initial = observe_request(
        seed,
        branch_kind="initial_empty",
        change_layer="current_state",
        change_axes=ChangeAxes(),
        action="keep current B and Γ",
    )

    b_changed = replace(
        seed,
        name="reexploration branch: reopen B",
        lower=replace(
            seed.lower,
            boundary=RealizationBoundary(
                candidate_octaves=(3, 4),
                voice_range=VoiceRange(
                    SpelledNote("E", accidental=1, octave=3),
                    SpelledNote("A", accidental=1, octave=4),
                ),
            ),
        ),
    )
    b_branch = observe_request(
        b_changed,
        branch_kind="B_change",
        change_layer="realization_layer",
        change_axes=ChangeAxes(boundary_changed=True),
        action="reopen voice A candidate octave and voice range",
    )

    gamma_branch = observe_request(
        seed,
        branch_kind="Γ_change",
        change_layer="realization_layer",
        change_axes=ChangeAxes(relation_changed=True),
        action="relax the voice A pitch < voice B pitch relation",
        pitch_ordering_rule="allow_crossed_voice_pitches",
    )

    target_changed = replace(
        seed,
        name="reexploration branch: shift target degree",
        lower=replace(seed.lower, target_degree=7),
    )
    target_branch = observe_request(
        target_changed,
        branch_kind="upstream_target_change",
        change_layer="upstream_target_layer",
        change_axes=ChangeAxes(upstream_target_changed=True),
        action="replace upstream target degree 3 -> 7, then rerun realization",
    )

    return initial, b_branch, gamma_branch, target_branch


def run_checks() -> None:
    initial, b_branch, gamma_branch, target_branch = build_reexploration_observations()

    # 同じseedでは、候補生成後の範囲投影までは同じで、Γ_orderingで空になる。
    assert initial.generated_voice_a_candidates == (SpelledNote("A", accidental=1, octave=4),)
    assert initial.generated_voice_b_candidates == (SpelledNote("F", accidental=1, octave=4),)
    assert initial.filtered_voice_a_candidates == initial.generated_voice_a_candidates
    assert initial.filtered_voice_b_candidates == initial.generated_voice_b_candidates
    assert initial.admissible_voice_pairs == ()
    assert initial.status == "no_admissible_candidate"
    assert initial.failure_stage == "Γ_ordering"
    assert initial.change_axes == ChangeAxes()

    # Bを開くと、同じtarget degreeから新しい候補集合が生じる。
    assert tuple(note.text for note in b_branch.generated_voice_a_candidates) == (
        "A♯3",
        "A♯4",
    )
    assert tuple(note.text for note in b_branch.filtered_voice_a_candidates) == (
        "A♯3",
        "A♯4",
    )
    assert b_branch.status == "selected"
    assert tuple(note.text for note in b_branch.selected) == ("A♯3", "F♯4")
    assert b_branch.change_layer == "realization_layer"
    assert b_branch.change_axes == ChangeAxes(boundary_changed=True)
    assert b_branch.pitch_ordering_rule == "strict_voice_a_pitch_lt_voice_b_pitch"

    # Γを変えると、元の候補を残したままcrossed pitchを比較対象にできる。
    assert gamma_branch.generated_voice_a_candidates == initial.generated_voice_a_candidates
    assert gamma_branch.generated_voice_b_candidates == initial.generated_voice_b_candidates
    assert gamma_branch.admissible_voice_pairs == (
        (SpelledNote("A", accidental=1, octave=4), SpelledNote("F", accidental=1, octave=4)),
    )
    assert gamma_branch.status == "selected"
    assert tuple(note.text for note in gamma_branch.selected) == ("A♯4", "F♯4")
    assert gamma_branch.change_layer == "realization_layer"
    assert gamma_branch.change_axes == ChangeAxes(relation_changed=True)
    assert gamma_branch.pitch_ordering_rule == "allow_crossed_voice_pitches"

    # 上流targetを変えると、BとΓを維持したまま実現層を再実行できる。
    assert target_branch.request.lower.target_degree == 7
    assert tuple(note.text for note in target_branch.generated_voice_a_candidates) == ("E♯4",)
    assert target_branch.status == "selected"
    assert tuple(note.text for note in target_branch.selected) == ("E♯4", "F♯4")
    assert target_branch.change_layer == "upstream_target_layer"
    assert target_branch.change_axes == ChangeAxes(upstream_target_changed=True)
    assert target_branch.pitch_ordering_rule == "strict_voice_a_pitch_lt_voice_b_pitch"

    # 三分岐は同じ初期空集合の後続候補だが、再探索方針そのものはまだ選択しない。
    assert {b_branch.branch_kind, gamma_branch.branch_kind, target_branch.branch_kind} == {
        "B_change",
        "Γ_change",
        "upstream_target_change",
    }


def print_observation(observation: ReexplorationObservation) -> None:
    print(f"[{observation.branch_kind} / {observation.change_layer}] {observation.action}")
    print(
        "  change_axes="
        f"boundary:{observation.change_axes.boundary_changed} / "
        f"relation:{observation.change_axes.relation_changed} / "
        f"upstream_target:{observation.change_axes.upstream_target_changed}"
    )
    print(
        "  generated_voice_A="
        + ",".join(note.text for note in observation.generated_voice_a_candidates)
        + " / "
        + ",".join(note.text for note in observation.generated_voice_b_candidates)
    )
    print(
        "  filtered_voice_A="
        + ",".join(note.text for note in observation.filtered_voice_a_candidates)
        + " / "
        + ",".join(note.text for note in observation.filtered_voice_b_candidates)
    )
    print(f"  pitch_ordering_rule={observation.pitch_ordering_rule}")
    print(f"  admissible_voice_pairs={len(observation.admissible_voice_pairs)}")
    if observation.selected is not None:
        print(f"  selected={observation.selected[0].text}-{observation.selected[1].text}")
    else:
        print(f"  status={observation.status}")
        print(f"  failure_stage={observation.failure_stage}")


def main() -> None:
    run_checks()
    print("[cycle]")
    print("  empty under current B / Γ")
    print("  -> B_change -> new candidate set")
    print("  -> Γ_change -> alternative relation")
    print("  -> upstream_target_change -> new target candidate")
    for observation in build_reexploration_observations():
        print_observation(observation)


if __name__ == "__main__":
    main()
