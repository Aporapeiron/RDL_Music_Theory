"""C majorの候補集合と制約の最小検証。

12平均律・根位置三和音を参照空間とし、
境界の保存、現在候補の変更、目標条件が候補集合へどう作用するかだけを扱う。
stabilize / destabilize や安定度の順位付けは扱わない。
"""

from dataclasses import dataclass


PITCH_NAMES = (
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
)
C_MAJOR_SCALE = frozenset((0, 2, 4, 5, 7, 9, 11))
QUALITY_INTERVALS = {
    "major": (0, 4, 7),
    "minor": (0, 3, 7),
    "diminished": (0, 3, 6),
}
QUALITY_SUFFIXES = {"major": "", "minor": "m", "diminished": "dim"}


@dataclass(frozen=True)
class Chord:
    degree: int | None
    label: str
    root_pc: int
    quality: str
    intervals: tuple[int, int, int]

    @property
    def pcs(self) -> frozenset[int]:
        return frozenset((self.root_pc + interval) % 12 for interval in self.intervals)

    @property
    def identity(self) -> tuple[int, str]:
        return (self.root_pc, self.quality)

    def features(self) -> dict[str, object]:
        return {
            "degree": self.degree,
            "label": self.label,
            "root": PITCH_NAMES[self.root_pc],
            "root_pc": self.root_pc,
            "quality": self.quality,
            "pcs": tuple(sorted(self.pcs)),
        }


def make_chord(
    root_pc: int, quality: str, degree: int | None = None, label: str | None = None
) -> Chord:
    intervals = QUALITY_INTERVALS[quality]
    if label is None:
        label = f"{PITCH_NAMES[root_pc]}{QUALITY_SUFFIXES[quality]}"
    return Chord(degree, label, root_pc, quality, intervals)


def all_root_position_triads() -> tuple[Chord, ...]:
    """12根音×3種類の、実験用の参照候補空間を返す。"""
    return tuple(
        make_chord(root_pc, quality)
        for root_pc in range(12)
        for quality in QUALITY_INTERVALS
    )


def c_major_chords() -> tuple[Chord, ...]:
    """C major境界を保存したときに残る根位置三和音を返す。"""
    degree_specs = (
        (1, 0, "major", "I / C"),
        (2, 2, "minor", "ii / Dm"),
        (3, 4, "minor", "iii / Em"),
        (4, 5, "major", "IV / F"),
        (5, 7, "major", "V / G"),
        (6, 9, "minor", "vi / Am"),
        (7, 11, "diminished", "vii° / Bdim"),
    )
    return tuple(
        make_chord(root_pc, quality, degree, label)
        for degree, root_pc, quality, label in degree_specs
    )


def candidate_space(*, preserve_b_cmaj: bool) -> tuple[Chord, ...]:
    """保存条件の有無による候補空間を返す。"""
    if preserve_b_cmaj:
        # 度数ラベルを保持した候補から、B_Cmajの保存条件を適用する。
        return tuple(
            chord for chord in c_major_chords() if chord.pcs <= C_MAJOR_SCALE
        )
    return all_root_position_triads()


def constrain_candidates(
    candidates: tuple[Chord, ...],
    *,
    current: Chord,
    change_current: bool,
    target: tuple[int, str] | None = None,
) -> dict[str, object]:
    """現在候補の変更と目標条件を候補空間へ適用する。"""
    result = list(candidates)
    if change_current:
        result = [chord for chord in result if chord.identity != current.identity]
    if target is not None:
        result = [chord for chord in result if chord.identity == target]

    if len(result) == 0:
        status = "no_candidate"
    elif len(result) == 1:
        status = "locally_resolved"
    else:
        status = "underdetermined"

    return {
        "current": current,
        "target_specified": target is not None,
        "candidates": tuple(result),
        "status": status,
    }


def labels(result: dict[str, object]) -> list[str]:
    return [chord.label for chord in result["candidates"]]


def format_chord(chord: Chord) -> str:
    features = chord.features()
    return (
        f"{features['label']}: root_pc={features['root_pc']} "
        f"quality={features['quality']} pcs={features['pcs']}"
    )


def run_checks() -> None:
    preserved = candidate_space(preserve_b_cmaj=True)
    expanded = candidate_space(preserve_b_cmaj=False)
    current = next(chord for chord in preserved if chord.degree == 1)

    changed = constrain_candidates(
        preserved, current=current, change_current=True
    )
    targeted = constrain_candidates(
        preserved,
        current=current,
        change_current=True,
        target=(7, "major"),
    )
    expanded_changed = constrain_candidates(
        expanded, current=current, change_current=True
    )

    assert len(preserved) == 7
    assert len(changed["candidates"]) == 6
    assert changed["status"] == "underdetermined"
    assert labels(targeted) == ["V / G"]
    assert targeted["status"] == "locally_resolved"
    impossible = constrain_candidates(
        preserved,
        current=current,
        change_current=True,
        target=(0, "major"),
    )
    assert impossible["candidates"] == ()
    assert impossible["status"] == "no_candidate"
    singleton = constrain_candidates(
        (next(chord for chord in preserved if chord.degree == 5),),
        current=current,
        change_current=True,
    )
    assert singleton["status"] == "locally_resolved"
    assert len(expanded) == 36
    assert len(expanded_changed["candidates"]) == 35


def main() -> None:
    run_checks()
    preserved = candidate_space(preserve_b_cmaj=True)
    expanded = candidate_space(preserve_b_cmaj=False)
    current = next(chord for chord in preserved if chord.degree == 1)

    print("[preserve(B_Cmaj)]", len(preserved), [chord.label for chord in preserved])

    changed = constrain_candidates(
        preserved, current=current, change_current=True
    )
    print("[change(current) + preserve(B_Cmaj)]")
    print(" ", "status=", changed["status"])
    print(" ", "candidates=", labels(changed))

    targeted = constrain_candidates(
        preserved,
        current=current,
        change_current=True,
        target=(7, "major"),
    )
    print("[change(current) + preserve(B_Cmaj) + target=V]")
    for chord in targeted["candidates"]:
        print(" ", format_chord(chord))
    print(" ", "status=", targeted["status"])

    expanded_changed = constrain_candidates(
        expanded, current=current, change_current=True
    )
    print("[change(current) without preserve(B_Cmaj)]")
    print(" ", "candidate_space=", len(expanded))
    print(" ", "candidates=", len(expanded_changed["candidates"]))
    print(" ", "status=", expanded_changed["status"])


if __name__ == "__main__":
    main()
