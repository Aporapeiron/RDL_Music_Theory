"""同じ12TET上の7半音が、綴りによってP5/d6へ分岐する最小検証。

C4-G4 と C#4-Ab4 は、12TETでは同じ7半音・同じ周波数比になる。
さらに C4-G4 と C4-Abb4 は、両音の絶対音高まで同じである。
しかし音名上のgeneric intervalが異なるため、音程名はP5とd6に分岐する。

これは音程名が周波数比だけでなく、音名・綴りという learned 側の関係構造を
必要とすることを示す。RDL音楽_Coreへは追加しない。
"""

from dataclasses import dataclass
from math import isclose


LETTER_INDEX = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}
LETTER_PITCH_CLASS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
INTERVAL_NAMES = {
    1: "一度",
    2: "二度",
    3: "三度",
    4: "四度",
    5: "五度",
    6: "六度",
    7: "七度",
    8: "八度",
}
PERFECT_EXPECTED = {1: 0, 4: 5, 5: 7, 8: 12}
MAJOR_EXPECTED = {2: 2, 3: 4, 6: 9, 7: 11}


@dataclass(frozen=True)
class SpelledNote:
    letter: str
    accidental: int = 0
    octave: int = 4

    def __post_init__(self) -> None:
        if self.letter not in LETTER_INDEX:
            raise ValueError(f"unknown letter: {self.letter}")
        if self.accidental not in (-2, -1, 0, 1, 2):
            raise ValueError("accidental must be between double-flat and double-sharp")

    @property
    def pitch_class(self) -> int:
        return (LETTER_PITCH_CLASS[self.letter] + self.accidental) % 12

    @property
    def chromatic_index(self) -> int:
        # pitch_classのmod 12後に加えると、B#4/Cb4のような
        # オクターブ境界を跨ぐ異名同音で絶対位置がずれる。
        return 12 * (self.octave + 1) + LETTER_PITCH_CLASS[self.letter] + self.accidental

    @property
    def text(self) -> str:
        accidental = {2: "𝄪", 1: "♯", 0: "", -1: "♭", -2: "𝄫"}[self.accidental]
        return f"{self.letter}{accidental}{self.octave}"


@dataclass(frozen=True)
class SpelledIntervalObservation:
    lower: SpelledNote
    upper: SpelledNote
    ratio: float
    cents: float
    semitones_12tet: int
    generic_number: int
    quality_code: str
    label: str


@dataclass(frozen=True)
class SpellingBoundary:
    """音名・綴りを既知の関係として扱うB。"""

    tuning: str = "12TET"
    known_spelling: bool = True
    ascending: bool = True


DEFAULT_BOUNDARY = SpellingBoundary()


def quality_code(generic_number: int, semitones: int) -> str:
    if generic_number in PERFECT_EXPECTED:
        delta = semitones - PERFECT_EXPECTED[generic_number]
        return {0: "P", -1: "d", 1: "A"}.get(delta, "?")
    if generic_number in MAJOR_EXPECTED:
        delta = semitones - MAJOR_EXPECTED[generic_number]
        return {0: "M", -1: "m", -2: "d", 1: "A"}.get(delta, "?")
    return "?"


def interval_label(generic_number: int, code: str) -> str:
    if code == "P":
        quality = "完全"
    elif code == "M":
        quality = "長"
    elif code == "m":
        quality = "短"
    elif code == "d":
        quality = "減"
    elif code == "A":
        quality = "増"
    else:
        quality = "不明"
    return f"{quality}{INTERVAL_NAMES.get(generic_number, f'{generic_number}度')}"


def observe_spelled_interval(
    lower: SpelledNote,
    upper: SpelledNote,
    boundary: SpellingBoundary = DEFAULT_BOUNDARY,
) -> SpelledIntervalObservation:
    """綴りを含む音程を、12TET距離と音程名へ写像する。"""
    if boundary.tuning != "12TET":
        raise ValueError("this experiment requires 12TET")
    if not boundary.known_spelling or not boundary.ascending:
        raise ValueError("this experiment requires known ascending spellings")
    chromatic_semitones = upper.chromatic_index - lower.chromatic_index
    if chromatic_semitones <= 0:
        raise ValueError("upper note must be higher than lower note")
    diatonic_steps = (
        7 * (upper.octave - lower.octave)
        + LETTER_INDEX[upper.letter]
        - LETTER_INDEX[lower.letter]
    )
    generic_number = diatonic_steps + 1
    code = quality_code(generic_number, chromatic_semitones)
    return SpelledIntervalObservation(
        lower=lower,
        upper=upper,
        ratio=2.0 ** (chromatic_semitones / 12.0),
        cents=100.0 * chromatic_semitones,
        semitones_12tet=chromatic_semitones,
        generic_number=generic_number,
        quality_code=code,
        label=interval_label(generic_number, code),
    )


def print_observation(observation: SpelledIntervalObservation) -> None:
    print(f"[{observation.lower.text}-{observation.upper.text}]")
    print(f"  ratio={observation.ratio:.12f}")
    print(f"  cents={observation.cents:.9f}")
    print(f"  semitones_12tet={observation.semitones_12tet}")
    print(f"  generic_number={observation.generic_number}")
    print(f"  quality_code={observation.quality_code}")
    print(f"  label={observation.label}")


def run_checks() -> None:
    p5 = observe_spelled_interval(
        SpelledNote("C", octave=4),
        SpelledNote("G", octave=4),
    )
    d6 = observe_spelled_interval(
        SpelledNote("C", accidental=1, octave=4),
        SpelledNote("A", accidental=-1, octave=4),
    )
    same_pitch_d6 = observe_spelled_interval(
        SpelledNote("C", octave=4),
        SpelledNote("A", accidental=-2, octave=4),
    )

    # 異名同音によるオクターブ境界を、絶対半音位置として正しく扱う。
    assert SpelledNote("B", accidental=1, octave=4).chromatic_index == 72
    assert SpelledNote("C", octave=5).chromatic_index == 72
    assert SpelledNote("C", accidental=-1, octave=4).chromatic_index == 59
    assert SpelledNote("B", octave=3).chromatic_index == 59

    # 12TET上の物理的な距離は同じ。
    assert p5.semitones_12tet == d6.semitones_12tet == 7
    assert isclose(p5.ratio, d6.ratio, abs_tol=1e-12)
    assert isclose(p5.cents, d6.cents, abs_tol=1e-12)

    # 音名上のgeneric intervalが異なるため、音程名が分岐する。
    assert p5.generic_number == 5
    assert d6.generic_number == 6
    assert p5.quality_code == "P"
    assert d6.quality_code == "d"
    assert p5.label == "完全五度"
    assert d6.label == "減六度"

    # C4-G4とC4-A𝄫4は、下音・上音とも物理音高が同一である。
    assert p5.lower.chromatic_index == same_pitch_d6.lower.chromatic_index
    assert p5.upper.chromatic_index == same_pitch_d6.upper.chromatic_index
    assert p5.semitones_12tet == same_pitch_d6.semitones_12tet == 7
    assert isclose(p5.ratio, same_pitch_d6.ratio, abs_tol=1e-12)
    assert isclose(p5.cents, same_pitch_d6.cents, abs_tol=1e-12)
    assert p5.generic_number == 5
    assert same_pitch_d6.generic_number == 6
    assert p5.label == "完全五度"
    assert same_pitch_d6.label == "減六度"


def main() -> None:
    run_checks()
    p5 = observe_spelled_interval(SpelledNote("C", octave=4), SpelledNote("G", octave=4))
    d6 = observe_spelled_interval(
        SpelledNote("C", accidental=1, octave=4),
        SpelledNote("A", accidental=-1, octave=4),
    )
    same_pitch_d6 = observe_spelled_interval(
        SpelledNote("C", octave=4),
        SpelledNote("A", accidental=-2, octave=4),
    )
    print("[Γ]")
    print("  Γ_chromatic=12TET上の半音距離")
    print("  Γ_generic=音名上の文字間隔")
    print("  Γ_quality=generic intervalと半音距離の差")
    print_observation(p5)
    print_observation(d6)
    print_observation(same_pitch_d6)
    print("[comparison]")
    print(f"  physical_ratio_equal={isclose(p5.ratio, d6.ratio, abs_tol=1e-12)}")
    print(f"  12TET_category_equal={p5.semitones_12tet == d6.semitones_12tet}")
    print(f"  interval_label_equal={p5.label == d6.label}")
    identical_physical_pitch_pair = (
        p5.lower.chromatic_index == same_pitch_d6.lower.chromatic_index
        and p5.upper.chromatic_index == same_pitch_d6.upper.chromatic_index
    )
    print(
        "  identical_physical_pitch_pair="
        f"{identical_physical_pitch_pair}"
    )


if __name__ == "__main__":
    main()
