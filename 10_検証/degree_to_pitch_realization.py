"""音度遷移を、明示した境界・綴り・声部規則で具体音へ実現する最小検証。

13では、具体的targetは計画へ先に与えられていた。
14では、実現境界が許す候補空間から綴り付き候補を生成し、
許容条件と別の選択規則を分けて候補を一つ選ぶ。

    inherited learned transition
      -> target degree
      -> B_realization: candidate octaves / voice range
      -> Γ_spelling: spelled candidates
      -> Γ_admissible: range / ordering
      -> Γ_select: minimum motion
      -> concrete target pair

これは限定した12TET長音階モデルと一つの声部選択規則の検証であり、
機能和声や人間の作曲判断の一般モデルではない。
"""

from dataclasses import dataclass

from spelled_interval_divergence import SpelledNote


@dataclass(frozen=True)
class MajorContext:
    name: str
    scale: tuple[tuple[str, int], ...]

    def note_for_degree(self, degree: int, octave: int) -> SpelledNote:
        if not 1 <= degree <= 7:
            raise ValueError("major-scale degree must be between 1 and 7")
        letter, accidental = self.scale[degree - 1]
        return SpelledNote(letter, accidental=accidental, octave=octave)


@dataclass(frozen=True)
class VoiceRange:
    low: SpelledNote
    high: SpelledNote

    def contains(self, note: SpelledNote) -> bool:
        return self.low.chromatic_index <= note.chromatic_index <= self.high.chromatic_index


@dataclass(frozen=True)
class RealizationBoundary:
    """B_realization：候補オクターブと声部範囲を宣言する境界。"""

    candidate_octaves: tuple[int, ...]
    voice_range: VoiceRange


@dataclass(frozen=True)
class VoiceRealizationRequest:
    voice: str
    start: SpelledNote
    target_degree: int
    boundary: RealizationBoundary


@dataclass(frozen=True)
class PairRealizationRequest:
    name: str
    context: MajorContext
    lower: VoiceRealizationRequest
    upper: VoiceRealizationRequest


@dataclass(frozen=True)
class PairRealizationObservation:
    request: PairRealizationRequest
    generated_lower_candidates: tuple[SpelledNote, ...]
    generated_upper_candidates: tuple[SpelledNote, ...]
    filtered_lower_candidates: tuple[SpelledNote, ...]
    filtered_upper_candidates: tuple[SpelledNote, ...]
    admissible_pairs: tuple[tuple[SpelledNote, SpelledNote], ...]
    selected: tuple[SpelledNote, SpelledNote]

    @property
    def lower_motion(self) -> int:
        return self.selected[0].chromatic_index - self.request.lower.start.chromatic_index

    @property
    def upper_motion(self) -> int:
        return self.selected[1].chromatic_index - self.request.upper.start.chromatic_index


def generate_spelled_candidates(
    context: MajorContext,
    target_degree: int,
    candidate_octaves: tuple[int, ...],
) -> tuple[SpelledNote, ...]:
    """Γ_spelling：音度とオクターブを綴り付き音へ写像する。"""

    return tuple(context.note_for_degree(target_degree, octave) for octave in candidate_octaves)


def filter_voice_range(
    candidates: tuple[SpelledNote, ...],
    voice_range: VoiceRange,
) -> tuple[SpelledNote, ...]:
    return tuple(note for note in candidates if voice_range.contains(note))


def build_admissible_pairs(
    lower_candidates: tuple[SpelledNote, ...],
    upper_candidates: tuple[SpelledNote, ...],
) -> tuple[tuple[SpelledNote, SpelledNote], ...]:
    """Γ_admissible：範囲通過後に上下声部の順序を満たす対を作る。"""

    return tuple(
        (lower, upper)
        for lower in lower_candidates
        for upper in upper_candidates
        if lower.chromatic_index < upper.chromatic_index
    )


def select_nearest_pair(
    request: PairRealizationRequest,
    admissible_pairs: tuple[tuple[SpelledNote, SpelledNote], ...],
) -> tuple[SpelledNote, SpelledNote]:
    """Γ_select：許容候補から合計絶対移動量を最小化して選ぶ。"""

    if not admissible_pairs:
        raise ValueError("no admissible target pair")

    return min(
        admissible_pairs,
        key=lambda pair: (
            abs(pair[0].chromatic_index - request.lower.start.chromatic_index)
            + abs(pair[1].chromatic_index - request.upper.start.chromatic_index),
            abs(pair[0].chromatic_index - request.lower.start.chromatic_index),
            pair[0].chromatic_index,
            pair[1].chromatic_index,
        ),
    )


def select_highest_pair(
    admissible_pairs: tuple[tuple[SpelledNote, SpelledNote], ...],
) -> tuple[SpelledNote, SpelledNote]:
    """比較用の別Γ：上下声部を候補集合の高い側へ置く。"""

    if not admissible_pairs:
        raise ValueError("no admissible target pair")
    return max(
        admissible_pairs,
        key=lambda pair: (pair[0].chromatic_index, pair[1].chromatic_index),
    )


def realize_pair(request: PairRealizationRequest) -> PairRealizationObservation:
    """B_realizationから候補を展開し、許容化・選択までを順に行う。"""

    lower_all = generate_spelled_candidates(
        request.context,
        request.lower.target_degree,
        request.lower.boundary.candidate_octaves,
    )
    upper_all = generate_spelled_candidates(
        request.context,
        request.upper.target_degree,
        request.upper.boundary.candidate_octaves,
    )
    lower_filtered = filter_voice_range(lower_all, request.lower.boundary.voice_range)
    upper_filtered = filter_voice_range(upper_all, request.upper.boundary.voice_range)
    admissible_pairs = build_admissible_pairs(lower_filtered, upper_filtered)
    return PairRealizationObservation(
        request=request,
        generated_lower_candidates=lower_all,
        generated_upper_candidates=upper_all,
        filtered_lower_candidates=lower_filtered,
        filtered_upper_candidates=upper_filtered,
        admissible_pairs=admissible_pairs,
        selected=select_nearest_pair(request, admissible_pairs),
    )


C_MAJOR = MajorContext(
    "C major",
    (("C", 0), ("D", 0), ("E", 0), ("F", 0), ("G", 0), ("A", 0), ("B", 0)),
)

F_SHARP_MAJOR = MajorContext(
    "F♯ major",
    (("F", 1), ("G", 1), ("A", 1), ("B", 0), ("C", 1), ("D", 1), ("E", 1)),
)


def build_requests() -> tuple[PairRealizationRequest, PairRealizationRequest]:
    a4 = PairRealizationRequest(
        "A4 representative realization",
        C_MAJOR,
        VoiceRealizationRequest(
            "lower",
            SpelledNote("F", octave=4),
            target_degree=3,
            boundary=RealizationBoundary(
                candidate_octaves=(3, 4, 5),
                voice_range=VoiceRange(SpelledNote("C", octave=3), SpelledNote("E", octave=5)),
            ),
        ),
        VoiceRealizationRequest(
            "upper",
            SpelledNote("B", octave=4),
            target_degree=1,
            boundary=RealizationBoundary(
                candidate_octaves=(3, 4, 5, 6),
                voice_range=VoiceRange(SpelledNote("G", octave=3), SpelledNote("C", octave=6)),
            ),
        ),
    )
    d5 = PairRealizationRequest(
        "d5 representative realization",
        F_SHARP_MAJOR,
        VoiceRealizationRequest(
            "lower",
            SpelledNote("E", accidental=1, octave=4),
            target_degree=1,
            boundary=RealizationBoundary(
                candidate_octaves=(3, 4, 5),
                voice_range=VoiceRange(SpelledNote("C", octave=3), SpelledNote("G", octave=5)),
            ),
        ),
        VoiceRealizationRequest(
            "upper",
            SpelledNote("B", octave=4),
            target_degree=3,
            boundary=RealizationBoundary(
                candidate_octaves=(3, 4, 5),
                voice_range=VoiceRange(SpelledNote("G", octave=3), SpelledNote("C", octave=6)),
            ),
        ),
    )
    return a4, d5


def run_checks() -> None:
    a4_request, d5_request = build_requests()
    a4 = realize_pair(a4_request)
    d5 = realize_pair(d5_request)

    # 音度と候補オクターブから、同じ音度でも複数の具体音が生成される。
    assert tuple(note.text for note in d5.generated_lower_candidates) == ("F♯3", "F♯4", "F♯5")
    assert tuple(note.text for note in d5.generated_upper_candidates) == ("A♯3", "A♯4", "A♯5")
    assert set(d5.filtered_lower_candidates) <= set(d5.generated_lower_candidates)
    assert set(d5.filtered_upper_candidates) <= set(d5.generated_upper_candidates)

    # 選択前の候補集合と、音域・上下関係を通過した候補対は別である。
    assert len(d5.admissible_pairs) > 1
    assert all(lower.chromatic_index < upper.chromatic_index for lower, upper in d5.admissible_pairs)

    # Γ_selectの最小移動で、13の具体targetを再生成できる。
    assert tuple(note.text for note in a4.selected) == ("E4", "C5")
    assert tuple(note.text for note in d5.selected) == ("F♯4", "A♯4")

    assert (a4.lower_motion, a4.upper_motion) == (-1, 1)
    assert (d5.lower_motion, d5.upper_motion) == (1, -1)

    # learned transitionだけでは選択は完了しない。同じ候補集合に別のΓ_selectを適用すると別候補になる。
    highest = select_highest_pair(d5.admissible_pairs)
    assert tuple(note.text for note in highest) == ("F♯5", "A♯5")
    assert highest != d5.selected

    # 実現器は音程ラベルを入力していない。
    assert not hasattr(d5_request, "interval_label")


def print_observation(observation: PairRealizationObservation) -> None:
    request = observation.request
    lower_degree = request.lower.target_degree
    upper_degree = request.upper.target_degree
    print(f"[{request.name}] context={request.context.name}")
    print(f"  target_degrees={lower_degree} / {upper_degree}")
    print(
        "  generated_lower_candidates="
        + ",".join(note.text for note in observation.generated_lower_candidates)
    )
    print(
        "  generated_upper_candidates="
        + ",".join(note.text for note in observation.generated_upper_candidates)
    )
    print(
        "  selected="
        + f"{observation.selected[0].text}-{observation.selected[1].text}"
    )
    print(f"  motion={observation.lower_motion} / {observation.upper_motion} semitone")


def main() -> None:
    run_checks()
    a4_request, d5_request = build_requests()
    a4 = realize_pair(a4_request)
    d5 = realize_pair(d5_request)
    print("[pipeline]")
    print("  inherited learned tendency -> target degree")
    print("  -> B_realization: candidate octaves / voice range")
    print("  -> Γ_spelling: spelled candidates")
    print("  -> Γ_admissible: range / ordering")
    print("  -> Γ_select: minimum motion")
    print("  -> concrete target")
    print_observation(a4)
    print_observation(d5)


if __name__ == "__main__":
    main()
