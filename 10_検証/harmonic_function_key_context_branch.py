"""同一和音がkey contextで異なる和声機能候補へ分岐する最小検証。

この検証では、和音候補を物理音響や声部進行へ拡張しない。
同じrooted chord candidateに異なるkey contextを接続したとき、
degree annotationが分岐し、今回固定した限定的なdegree→function対応表によって
functional annotation候補も分岐することだけを確認する。

    chord candidate
      + key context
      -> degree annotation
      -> functional annotation candidate
      -> targetは未生成のまま保持

function labelはtarget生成器ではない。
"""

from dataclasses import dataclass


PITCH_CLASS = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11,
}

MAJOR_SCALE_DEGREES = {
    0: 1,
    2: 2,
    4: 3,
    5: 4,
    7: 5,
    9: 6,
    11: 7,
}

# 今回のfixture用の限定Γであり、一般的な和声機能規則ではない。
FUNCTION_BY_MAJOR_DEGREE = {
    1: "tonic_candidate",
    2: "predominant_candidate",
    3: "tonic_prolongation_candidate",
    4: "predominant_candidate",
    5: "dominant_candidate",
    6: "tonic_substitute_candidate",
    7: "dominant_leading_candidate",
}


@dataclass(frozen=True)
class ChordCandidate:
    label: str
    root: str
    quality: str
    pitch_classes: frozenset[int]


@dataclass(frozen=True)
class KeyContext:
    label: str
    tonic: str
    mode: str = "major"

    @property
    def tonic_pc(self) -> int:
        return PITCH_CLASS[self.tonic]


@dataclass(frozen=True)
class FunctionObservation:
    chord: ChordCandidate
    key_context: KeyContext
    root_degree: int
    function_annotation: str
    generated_target: None
    generation_status: str


def make_major_triad(root: str) -> ChordCandidate:
    root_pc = PITCH_CLASS[root]
    pcs = frozenset((root_pc, (root_pc + 4) % 12, (root_pc + 7) % 12))
    return ChordCandidate(
        label=f"{root} major triad",
        root=root,
        quality="major",
        pitch_classes=pcs,
    )


def annotate_root_degree(chord: ChordCandidate, key_context: KeyContext) -> int:
    """key context内でrootが何度として読まれるかを返す。

    現在はmajor scaleだけを検証用に固定する。
    key外rootの場合は、この検証の外としてValueErrorにする。
    """

    if key_context.mode != "major":
        raise ValueError("only major key context is modeled in this minimal test")
    relative_pc = (PITCH_CLASS[chord.root] - key_context.tonic_pc) % 12
    if relative_pc not in MAJOR_SCALE_DEGREES:
        raise ValueError(f"{chord.root} is outside {key_context.label}")
    return MAJOR_SCALE_DEGREES[relative_pc]


def annotate_function(
    chord: ChordCandidate, key_context: KeyContext
) -> FunctionObservation:
    """和音候補にkey contextを接続し、機能注釈候補を返す。

    ここではtarget候補を生成しない。
    target生成・選択はcontroller未確定のξとして残す。
    """

    root_degree = annotate_root_degree(chord, key_context)
    function_annotation = FUNCTION_BY_MAJOR_DEGREE[root_degree]
    return FunctionObservation(
        chord=chord,
        key_context=key_context,
        root_degree=root_degree,
        function_annotation=function_annotation,
        generated_target=None,
        generation_status="function_annotated_target_not_generated",
    )


def run_checks() -> None:
    g_major_chord = make_major_triad("G")
    c_major = KeyContext("C major", "C")
    g_major = KeyContext("G major", "G")

    in_c = annotate_function(g_major_chord, c_major)
    in_g = annotate_function(g_major_chord, g_major)

    # 同じ和音候補を使っている。
    assert in_c.chord == in_g.chord
    assert in_c.chord.root == "G"
    assert in_c.chord.quality == "major"
    assert in_c.chord.pitch_classes == in_g.chord.pitch_classes

    # key contextだけでdegree annotationが分岐する。
    assert in_c.root_degree == 5
    assert in_g.root_degree == 1

    # degree annotationに対応するfunction annotationも分岐する。
    assert in_c.function_annotation == "dominant_candidate"
    assert in_g.function_annotation == "tonic_candidate"

    # function annotationはtarget生成器ではない。
    assert in_c.generated_target is None
    assert in_g.generated_target is None
    assert (
        in_c.generation_status
        == in_g.generation_status
        == "function_annotated_target_not_generated"
    )


def print_observation(observation: FunctionObservation) -> None:
    print(f"[{observation.key_context.label}]")
    print(f"  chord={observation.chord.label}")
    print(f"  chord_root={observation.chord.root}")
    print(f"  chord_quality={observation.chord.quality}")
    print(f"  root_degree={observation.root_degree}")
    print(f"  function_annotation={observation.function_annotation}")
    print(f"  generated_target={observation.generated_target}")
    print(f"  generation_status={observation.generation_status}")


def main() -> None:
    run_checks()
    g_major_chord = make_major_triad("G")
    observations = (
        annotate_function(g_major_chord, KeyContext("C major", "C")),
        annotate_function(g_major_chord, KeyContext("G major", "G")),
    )
    print("[pipeline]")
    print("  chord candidate + key context")
    print("  -> degree annotation")
    print("  -> functional annotation candidate")
    print("  -> target remains ungenerated")
    for observation in observations:
        print_observation(observation)
    print("[comparison]")
    print(f"  same_chord_candidate={observations[0].chord == observations[1].chord}")
    print(
        "  root_degrees="
        f"{observations[0].root_degree} / {observations[1].root_degree}"
    )
    print(
        "  function_annotations="
        f"{observations[0].function_annotation} / "
        f"{observations[1].function_annotation}"
    )
    print(
        "  target_generated="
        f"{observations[0].generated_target is not None or observations[1].generated_target is not None}"
    )


if __name__ == "__main__":
    main()

