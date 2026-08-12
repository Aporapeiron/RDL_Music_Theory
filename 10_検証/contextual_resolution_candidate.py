"""既選択の解決targetを文脈・音度役割・learned tendencyへ分解する最小検証。

12では、A4/d5に対するtargetを外部から与えた。
13では、その代表例を次の部品へ分解して保持し、整合を確認する。

    selected target (already provided)
      + context
      + role assignment
      + learned tendency
      + spelled target realization
      -> target candidate observation
      -> Γ_motion

ここで確認するのは、既知音楽理論の代表的な遷移記述を、既に選択された具体的targetの
内部要素として操作的に分解できることだけである。
音程ラベル単独からの普遍的target生成、知覚機構、文化横断的な法則は扱わない。
"""

from dataclasses import dataclass
from math import isclose

from spelled_interval_divergence import (
    SpelledIntervalObservation,
    SpelledNote,
    observe_spelled_interval,
)
from tritone_spelling_resolution import MotionObservation, classify_motion


@dataclass(frozen=True)
class Context:
    name: str
    target_chord: str


@dataclass(frozen=True)
class LearnedTendency:
    name: str
    source_degree: int
    target_degree: int


@dataclass(frozen=True)
class VoiceRolePath:
    """既に選択されたtargetと、その役割・tendencyの注釈。"""

    voice: str
    start: SpelledNote
    target: SpelledNote
    source_degree: int
    target_degree: int
    tendency: LearnedTendency


@dataclass(frozen=True)
class ContextualResolutionPlan:
    """具体的targetまで既に与えられた検証用の固定計画。"""

    name: str
    context: Context
    interval_label: str
    lower_path: VoiceRolePath
    upper_path: VoiceRolePath


@dataclass(frozen=True)
class ResolutionTargetCandidate:
    name: str
    lower: SpelledNote
    upper: SpelledNote
    context: Context


@dataclass(frozen=True)
class ResolutionObservation:
    plan: ContextualResolutionPlan
    start: SpelledIntervalObservation
    target: SpelledIntervalObservation
    motion: MotionObservation


def annotate_selected_target(
    plan: ContextualResolutionPlan,
) -> ResolutionTargetCandidate:
    """既に選択されたtargetを、文脈内の注釈とともに保持する。

    `target`は`VoiceRolePath`へ先に与えられている。ここでは文脈・音度役割・
    learned tendencyとの整合を確認し、そのtargetを候補観測として束ね直す。
    文脈やtendencyから具体音を導出する処理ではない。
    """

    assert plan.lower_path.tendency.source_degree == plan.lower_path.source_degree
    assert plan.lower_path.tendency.target_degree == plan.lower_path.target_degree
    assert plan.upper_path.tendency.source_degree == plan.upper_path.source_degree
    assert plan.upper_path.tendency.target_degree == plan.upper_path.target_degree
    return ResolutionTargetCandidate(
        name=f"{plan.name} target candidate",
        lower=plan.lower_path.target,
        upper=plan.upper_path.target,
        context=plan.context,
    )


def observe_plan(plan: ContextualResolutionPlan) -> ResolutionObservation:
    target = annotate_selected_target(plan)
    start = observe_spelled_interval(plan.lower_path.start, plan.upper_path.start)
    target_interval = observe_spelled_interval(target.lower, target.upper)
    lower_motion = target.lower.chromatic_index - plan.lower_path.start.chromatic_index
    upper_motion = target.upper.chromatic_index - plan.upper_path.start.chromatic_index
    motion = MotionObservation(
        lower_motion=lower_motion,
        upper_motion=upper_motion,
        direction=classify_motion(lower_motion, upper_motion),
    )
    return ResolutionObservation(
        plan=plan,
        start=start,
        target=target_interval,
        motion=motion,
    )


def build_plans() -> tuple[ContextualResolutionPlan, ContextualResolutionPlan]:
    leading_tone_to_tonic = LearnedTendency("leading tone rises to tonic", 7, 1)
    fourth_to_third = LearnedTendency("fourth lowers to third", 4, 3)

    c_major = Context("C major representative dominant-to-tonic context", "C major")
    a4_plan = ContextualResolutionPlan(
        name="A4 in C major",
        context=c_major,
        interval_label="A4",
        lower_path=VoiceRolePath(
            "lower",
            SpelledNote("F", octave=4),
            SpelledNote("E", octave=4),
            4,
            3,
            fourth_to_third,
        ),
        upper_path=VoiceRolePath(
            "upper",
            SpelledNote("B", octave=4),
            SpelledNote("C", octave=5),
            7,
            1,
            leading_tone_to_tonic,
        ),
    )

    f_sharp_major = Context("F♯ major representative dominant-to-tonic context", "F♯ major")
    d5_plan = ContextualResolutionPlan(
        name="d5 in F♯ major",
        context=f_sharp_major,
        interval_label="d5",
        lower_path=VoiceRolePath(
            "lower",
            SpelledNote("E", accidental=1, octave=4),
            SpelledNote("F", accidental=1, octave=4),
            7,
            1,
            leading_tone_to_tonic,
        ),
        upper_path=VoiceRolePath(
            "upper",
            SpelledNote("B", octave=4),
            SpelledNote("A", accidental=1, octave=4),
            4,
            3,
            fourth_to_third,
        ),
    )
    return a4_plan, d5_plan


def run_checks() -> None:
    a4_plan, d5_plan = build_plans()
    a4 = observe_plan(a4_plan)
    d5 = observe_plan(d5_plan)

    # 12TET物理モデル上の開始音高対は同一である。
    assert a4.start.lower.chromatic_index == d5.start.lower.chromatic_index
    assert a4.start.upper.chromatic_index == d5.start.upper.chromatic_index
    assert a4.start.semitones_12tet == d5.start.semitones_12tet == 6
    assert isclose(a4.start.ratio, d5.start.ratio, abs_tol=1e-12)
    assert isclose(a4.start.cents, d5.start.cents, abs_tol=1e-12)

    # 綴りを保持すると、同じ6半音はA4/d5へ分岐する。
    assert a4.start.label == "増四度"
    assert d5.start.label == "減五度"
    assert a4.plan.interval_label == "A4"
    assert d5.plan.interval_label == "d5"

    # targetは既にplanへ与えられており、ここではその内部要素との整合を確認する。
    assert a4.target.lower.text == "E4"
    assert a4.target.upper.text == "C5"
    assert d5.target.lower.text == "F♯4"
    assert d5.target.upper.text == "A♯4"
    assert a4.target.label == "短六度"
    assert d5.target.label == "長三度"

    assert a4.plan.context.target_chord == "C major"
    assert d5.plan.context.target_chord == "F♯ major"
    assert (a4.plan.lower_path.source_degree, a4.plan.lower_path.target_degree) == (4, 3)
    assert (a4.plan.upper_path.source_degree, a4.plan.upper_path.target_degree) == (7, 1)
    assert (d5.plan.lower_path.source_degree, d5.plan.lower_path.target_degree) == (7, 1)
    assert (d5.plan.upper_path.source_degree, d5.plan.upper_path.target_degree) == (4, 3)

    # targetが確定した後のΓ_motionは機械的に抽出される。
    assert a4.motion.lower_motion == -1
    assert a4.motion.upper_motion == 1
    assert a4.motion.direction == "outward"
    assert d5.motion.lower_motion == 1
    assert d5.motion.upper_motion == -1
    assert d5.motion.direction == "inward"


def print_observation(observation: ResolutionObservation) -> None:
    plan = observation.plan
    print(f"[{plan.interval_label}] {plan.context.name}")
    print(f"  start={observation.start.lower.text}-{observation.start.upper.text}")
    print(f"  start_label={observation.start.label}")
    print(f"  target={observation.target.lower.text}-{observation.target.upper.text}")
    print(f"  target_chord={plan.context.target_chord}")
    print(
        "  roles="
        f"{plan.lower_path.source_degree}->{plan.lower_path.target_degree},"
        f"{plan.upper_path.source_degree}->{plan.upper_path.target_degree}"
    )
    print(f"  lower_motion={observation.motion.lower_motion} semitone")
    print(f"  upper_motion={observation.motion.upper_motion} semitone")
    print(f"  motion_direction={observation.motion.direction}")


def main() -> None:
    run_checks()
    a4_plan, d5_plan = build_plans()
    a4 = observe_plan(a4_plan)
    d5 = observe_plan(d5_plan)
    print("[pipeline]")
    print("  selected target + context / role / learned tendency")
    print("  -> decomposition and consistency observation")
    print("  -> Γ_motion")
    print_observation(a4)
    print_observation(d5)
    print("[comparison]")
    print(
        "  identical_start_pitch_pair="
        f"{a4.start.lower.chromatic_index == d5.start.lower.chromatic_index and a4.start.upper.chromatic_index == d5.start.upper.chromatic_index}"
    )
    print(
        "  target_contexts="
        f"{a4.plan.context.target_chord} / {d5.plan.context.target_chord}"
    )
    print(f"  motion_directions={a4.motion.direction} / {d5.motion.direction}")


if __name__ == "__main__":
    main()
