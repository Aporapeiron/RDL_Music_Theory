"""同一トライトーンが綴り付きの代表進行で異なる方向へ進む最小検証。

F4-B4 と E#4-B4 は、12TET上では同じ音高対・同じ6半音である。
しかし綴りを保持すると、それぞれ A4 / d5 として分岐する。

この実験では、外部から与えた二つの代表的な一半音ずつの反対方向進行を比較する。

    A4: F4 -> E4, B4 -> C5  （外へ開く）
    d5: E#4 -> F#4, B4 -> A#4（内へ狭まる）

ここで確認するのは、同一音響関係が、綴りと外部から与えた解決ターゲットを
含む学習済みの記述構造の中で異なる声部運動として表現されうることだけである。
人間の知覚上の解決感や、A4/d5に対する普遍的な機能和声は確定しない。
"""

from dataclasses import dataclass
from math import isclose

from spelled_interval_divergence import (
    SpelledIntervalObservation,
    SpelledNote,
    observe_spelled_interval,
)


@dataclass(frozen=True)
class ResolutionTargetCandidate:
    """learned側から外部入力された代表的な解決ターゲット。"""

    name: str
    lower: SpelledNote
    upper: SpelledNote


@dataclass(frozen=True)
class MotionObservation:
    lower_motion: int
    upper_motion: int
    direction: str


@dataclass(frozen=True)
class ResolutionObservation:
    name: str
    start: SpelledIntervalObservation
    target: SpelledIntervalObservation
    motion: MotionObservation


def classify_motion(lower_motion: int, upper_motion: int) -> str:
    if lower_motion < 0 < upper_motion:
        return "outward"
    if lower_motion > 0 > upper_motion:
        return "inward"
    if lower_motion == 0 and upper_motion == 0:
        return "static"
    return "other"


def observe_motion(
    start_lower: SpelledNote,
    start_upper: SpelledNote,
    target: ResolutionTargetCandidate,
) -> MotionObservation:
    """与えられたtargetに対する声部運動だけを記述する。"""

    lower_motion = target.lower.chromatic_index - start_lower.chromatic_index
    upper_motion = target.upper.chromatic_index - start_upper.chromatic_index
    return MotionObservation(
        lower_motion=lower_motion,
        upper_motion=upper_motion,
        direction=classify_motion(lower_motion, upper_motion),
    )


def observe_resolution(
    name: str,
    start_lower: SpelledNote,
    start_upper: SpelledNote,
    target: ResolutionTargetCandidate,
) -> ResolutionObservation:
    start = observe_spelled_interval(start_lower, start_upper)
    target_interval = observe_spelled_interval(target.lower, target.upper)
    return ResolutionObservation(
        name=name,
        start=start,
        target=target_interval,
        motion=observe_motion(start_lower, start_upper, target),
    )


def run_checks() -> None:
    # A4/d5からtargetを自動生成せず、代表的候補を外部から与える。
    a4_target = ResolutionTargetCandidate(
        "A4 representative outward candidate",
        SpelledNote("E", octave=4),
        SpelledNote("C", octave=5),
    )
    d5_target = ResolutionTargetCandidate(
        "d5 representative inward candidate",
        SpelledNote("F", accidental=1, octave=4),
        SpelledNote("A", accidental=1, octave=4),
    )
    a4 = observe_resolution(
        "A4",
        SpelledNote("F", octave=4),
        SpelledNote("B", octave=4),
        a4_target,
    )
    d5 = observe_resolution(
        "d5",
        SpelledNote("E", accidental=1, octave=4),
        SpelledNote("B", octave=4),
        d5_target,
    )

    # F4-B4とE#4-B4は、12TET上の同一音高対である。
    assert a4.start.lower.chromatic_index == d5.start.lower.chromatic_index
    assert a4.start.upper.chromatic_index == d5.start.upper.chromatic_index
    assert a4.start.semitones_12tet == d5.start.semitones_12tet == 6
    assert isclose(a4.start.ratio, d5.start.ratio, abs_tol=1e-12)
    assert isclose(a4.start.cents, d5.start.cents, abs_tol=1e-12)

    # 綴り関係を保持すると、同じ6半音がA4/d5へ分岐する。
    assert a4.start.generic_number == 4
    assert d5.start.generic_number == 5
    assert a4.start.quality_code == "A"
    assert d5.start.quality_code == "d"
    assert a4.start.label == "増四度"
    assert d5.start.label == "減五度"

    # 代表進行は各声部が1半音ずつ反対方向へ動く。
    assert a4.motion.lower_motion == -1
    assert a4.motion.upper_motion == 1
    assert a4.motion.direction == "outward"
    assert d5.motion.lower_motion == 1
    assert d5.motion.upper_motion == -1
    assert d5.motion.direction == "inward"

    # ターゲットの音程も、選択した綴りと声部進行を保持している。
    assert a4.target.label == "短六度"
    assert d5.target.label == "長三度"
    assert a4.target.semitones_12tet == 8
    assert d5.target.semitones_12tet == 4


def print_observation(observation: ResolutionObservation) -> None:
    print(f"[{observation.name}]")
    print(
        "  start="
        f"{observation.start.lower.text}-{observation.start.upper.text}"
    )
    print(f"  start_label={observation.start.label}")
    print(
        "  target="
        f"{observation.target.lower.text}-{observation.target.upper.text}"
    )
    print(f"  target_label={observation.target.label}")
    print(f"  lower_motion={observation.motion.lower_motion} semitone")
    print(f"  upper_motion={observation.motion.upper_motion} semitone")
    print(f"  motion_direction={observation.motion.direction}")


def main() -> None:
    run_checks()
    a4_target = ResolutionTargetCandidate(
        "A4 representative outward candidate",
        SpelledNote("E", octave=4),
        SpelledNote("C", octave=5),
    )
    d5_target = ResolutionTargetCandidate(
        "d5 representative inward candidate",
        SpelledNote("F", accidental=1, octave=4),
        SpelledNote("A", accidental=1, octave=4),
    )
    a4 = observe_resolution(
        "A4",
        SpelledNote("F", octave=4),
        SpelledNote("B", octave=4),
        a4_target,
    )
    d5 = observe_resolution(
        "d5",
        SpelledNote("E", accidental=1, octave=4),
        SpelledNote("B", octave=4),
        d5_target,
    )
    print("[Γ]")
    print("  Γ_chromatic=12TET上の半音距離")
    print("  Γ_generic=音名上の文字間隔")
    print("  Γ_quality=generic intervalと半音距離の差")
    print("  Γ_resolution=外部から与えた代表的解決候補")
    print("  Γ_motion=二声部の絶対半音移動方向")
    print_observation(a4)
    print_observation(d5)
    print("[comparison]")
    print(
        "  identical_start_pitch_pair="
        f"{a4.start.lower.chromatic_index == d5.start.lower.chromatic_index and a4.start.upper.chromatic_index == d5.start.upper.chromatic_index}"
    )
    print(f"  start_ratio_equal={isclose(a4.start.ratio, d5.start.ratio, abs_tol=1e-12)}")
    print(f"  start_12TET_category_equal={a4.start.semitones_12tet == d5.start.semitones_12tet}")
    print(f"  start_label_equal={a4.start.label == d5.start.label}")
    print(f"  motion_direction_equal={a4.motion.direction == d5.motion.direction}")


if __name__ == "__main__":
    main()
