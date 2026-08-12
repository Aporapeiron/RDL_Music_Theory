"""実現制約の競合による候補分岐・候補消滅を観測する最小検証。

14では、候補生成・許容化・選択を分離した。
15では、許容化の途中で候補が消える場合を、選択失敗として一括せず、
どの段階で消えたかを観測結果として保持する。

    target degree
      -> B_realization / Γ_spelling
      -> B_range_projection
      -> Γ_ordering
      -> Γ_select (候補が残った場合だけ)
      -> concrete target or constraint diagnosis

これは14の限定した12TET長音階モデルを再利用する検証であり、
声部範囲や上下関係を音楽一般の普遍的制約とは扱わない。
"""

from dataclasses import dataclass, replace

from degree_to_pitch_realization import (
    PairRealizationRequest,
    RealizationBoundary,
    SpelledNote,
    VoiceRange,
    build_admissible_pairs,
    build_requests,
    filter_voice_range,
    generate_spelled_candidates,
    select_nearest_pair,
)


@dataclass(frozen=True)
class ConstraintObservation:
    """候補生成から許容化までの段階と、消滅位置を保持する。"""

    request: PairRealizationRequest
    generated_lower_candidates: tuple[SpelledNote, ...]
    generated_upper_candidates: tuple[SpelledNote, ...]
    filtered_lower_candidates: tuple[SpelledNote, ...]
    filtered_upper_candidates: tuple[SpelledNote, ...]
    admissible_pairs: tuple[tuple[SpelledNote, SpelledNote], ...]
    selected: tuple[SpelledNote, SpelledNote] | None
    failure_stage: str | None
    failure_reason: str | None

    @property
    def status(self) -> str:
        if self.selected is not None:
            return "selected"
        if not self.filtered_lower_candidates:
            return "constraint_no_candidate"
        if not self.filtered_upper_candidates:
            return "constraint_no_candidate"
        if not self.admissible_pairs:
            return "no_admissible_candidate"
        return "unselected"


def observe_constraints(request: PairRealizationRequest) -> ConstraintObservation:
    """候補消滅の段階を明示したまま、選択可能なら選択する。"""

    generated_lower = generate_spelled_candidates(
        request.context,
        request.lower.target_degree,
        request.lower.boundary.candidate_octaves,
    )
    generated_upper = generate_spelled_candidates(
        request.context,
        request.upper.target_degree,
        request.upper.boundary.candidate_octaves,
    )
    # B_range_projection：B_realizationの声域境界を候補集合へ投影する。
    filtered_lower = filter_voice_range(
        generated_lower,
        request.lower.boundary.voice_range,
    )
    filtered_upper = filter_voice_range(
        generated_upper,
        request.upper.boundary.voice_range,
    )

    if not filtered_lower:
        return ConstraintObservation(
            request,
            generated_lower,
            generated_upper,
            filtered_lower,
            filtered_upper,
            (),
            None,
            "B_range_projection",
            "lower voice range removed every generated candidate",
        )
    if not filtered_upper:
        return ConstraintObservation(
            request,
            generated_lower,
            generated_upper,
            filtered_lower,
            filtered_upper,
            (),
            None,
            "B_range_projection",
            "upper voice range removed every generated candidate",
        )

    # Γ_ordering：声部間の順序関係を候補対へ適用する。
    admissible_pairs = build_admissible_pairs(filtered_lower, filtered_upper)
    if not admissible_pairs:
        return ConstraintObservation(
            request,
            generated_lower,
            generated_upper,
            filtered_lower,
            filtered_upper,
            admissible_pairs,
            None,
            "Γ_ordering",
            "range-surviving candidates cannot satisfy lower < upper",
        )

    return ConstraintObservation(
        request,
        generated_lower,
        generated_upper,
        filtered_lower,
        filtered_upper,
        admissible_pairs,
        select_nearest_pair(request, admissible_pairs),
        None,
        None,
    )


def build_competing_requests() -> tuple[
    PairRealizationRequest,
    PairRealizationRequest,
    PairRealizationRequest,
]:
    """同じ目標音度に、異なる実現境界を与える三ケース。"""

    baseline = build_requests()[1]

    order_conflict = replace(
        baseline,
        name="d5 ordering conflict",
        lower=replace(
            baseline.lower,
            boundary=RealizationBoundary(
                candidate_octaves=(3, 4, 5),
                voice_range=VoiceRange(
                    SpelledNote("F", accidental=1, octave=5),
                    SpelledNote("F", accidental=1, octave=5),
                ),
            ),
        ),
        upper=replace(
            baseline.upper,
            boundary=RealizationBoundary(
                candidate_octaves=(3, 4, 5),
                voice_range=VoiceRange(
                    SpelledNote("A", accidental=1, octave=4),
                    SpelledNote("A", accidental=1, octave=4),
                ),
            ),
        ),
    )

    range_conflict = replace(
        baseline,
        name="d5 lower-range conflict",
        lower=replace(
            baseline.lower,
            boundary=RealizationBoundary(
                candidate_octaves=(3, 4, 5),
                voice_range=VoiceRange(
                    SpelledNote("G", octave=3),
                    SpelledNote("G", octave=3),
                ),
            ),
        ),
    )
    return baseline, order_conflict, range_conflict


def run_checks() -> None:
    baseline, order_conflict, range_conflict = build_competing_requests()
    base = observe_constraints(baseline)
    ordering = observe_constraints(order_conflict)
    ranges = observe_constraints(range_conflict)

    # Γ_spellingの生成結果は、境界競合の三ケースで同じである。
    expected_lower = ("F♯3", "F♯4", "F♯5")
    expected_upper = ("A♯3", "A♯4", "A♯5")
    for observation in (base, ordering, ranges):
        assert tuple(note.text for note in observation.generated_lower_candidates) == expected_lower
        assert tuple(note.text for note in observation.generated_upper_candidates) == expected_upper

    # 通常ケースでは、Γ_orderingを通過した候補からΓ_selectが選択する。
    assert base.status == "selected"
    assert tuple(note.text for note in base.selected) == ("F♯4", "A♯4")
    assert base.failure_stage is None

    # 両声部に候補は残っても、上下関係の競合で許容対が全て消える。
    assert tuple(note.text for note in ordering.filtered_lower_candidates) == ("F♯5",)
    assert tuple(note.text for note in ordering.filtered_upper_candidates) == ("A♯4",)
    assert ordering.admissible_pairs == ()
    assert ordering.status == "no_admissible_candidate"
    assert ordering.selected is None
    assert ordering.failure_stage == "Γ_ordering"

    # 音域競合では、候補対を作る前に一方の候補集合が空になる。
    assert ranges.filtered_lower_candidates == ()
    assert ranges.status == "constraint_no_candidate"
    assert ranges.selected is None
    assert ranges.failure_stage == "B_range_projection"

    # 境界競合は、候補生成そのものの失敗やΓ_selectの別解とは区別する。
    assert ordering.generated_lower_candidates == base.generated_lower_candidates
    assert ordering.generated_upper_candidates == base.generated_upper_candidates
    assert ordering.failure_reason is not None
    assert ranges.failure_reason is not None


def print_observation(observation: ConstraintObservation) -> None:
    print(f"[{observation.request.name}]")
    print(
        "  generated="
        + ",".join(note.text for note in observation.generated_lower_candidates)
        + " / "
        + ",".join(note.text for note in observation.generated_upper_candidates)
    )
    print(
        "  filtered="
        + ",".join(note.text for note in observation.filtered_lower_candidates)
        + " / "
        + ",".join(note.text for note in observation.filtered_upper_candidates)
    )
    print(f"  admissible_pairs={len(observation.admissible_pairs)}")
    if observation.selected is not None:
        print(f"  selected={observation.selected[0].text}-{observation.selected[1].text}")
    else:
        print(f"  status={observation.status}")
        print(f"  failure_stage={observation.failure_stage}")
        print(f"  failure_reason={observation.failure_reason}")


def main() -> None:
    run_checks()
    print("[pipeline]")
    print("  target degree")
    print("  -> B_realization / Γ_spelling")
    print("  -> B_range_projection: voice range")
    print("  -> Γ_ordering: lower < upper")
    print("  -> Γ_select only when admissible pairs remain")
    print("  -> concrete target or constraint diagnosis")
    for request in build_competing_requests():
        print_observation(observe_constraints(request))


if __name__ == "__main__":
    main()
