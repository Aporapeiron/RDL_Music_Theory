"""Bから候補空間が生成される条件の最小検証。

Bと候補生成規則Γを分離し、生成後の制約処理とは別に扱う。
音楽固有の規則をCoreへ追加することは目的としない。
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
PITCH_UNIVERSE = frozenset(range(12))
C_MAJOR_SCALE = frozenset((0, 2, 4, 5, 7, 9, 11))
QUALITY_INTERVALS = {
    "major": (0, 4, 7),
    "minor": (0, 3, 7),
    "diminished": (0, 3, 6),
}
QUALITY_SUFFIXES = {"major": "", "minor": "m", "diminished": "dim"}


@dataclass(frozen=True)
class Boundary:
    """候補生成が参照する境界パッケージ。"""

    tonic_pc: int
    pitch_universe: frozenset[int] = PITCH_UNIVERSE


@dataclass(frozen=True)
class StableStructure:
    """Bの内部で保持されている関係構造M_B。"""

    pitch_inventory: frozenset[int]


@dataclass(frozen=True)
class GenerationRule:
    """Bから候補を作るための実験用規則Γ。"""

    root_source: str
    qualities: tuple[str, ...]
    require_scale_closure: bool


@dataclass(frozen=True)
class Candidate:
    root_pc: int
    quality: str

    @property
    def pcs(self) -> frozenset[int]:
        return frozenset(
            (self.root_pc + interval) % 12
            for interval in QUALITY_INTERVALS[self.quality]
        )

    @property
    def label(self) -> str:
        return f"{PITCH_NAMES[self.root_pc]}{QUALITY_SUFFIXES[self.quality]}"


def c_major_state() -> tuple[Boundary, StableStructure]:
    return Boundary(tonic_pc=0), StableStructure(pitch_inventory=C_MAJOR_SCALE)


def roots_for(
    boundary: Boundary, stable: StableStructure, rule: GenerationRule
) -> frozenset[int]:
    if rule.root_source == "stable_pitch_inventory":
        return stable.pitch_inventory
    if rule.root_source == "pitch_universe":
        return boundary.pitch_universe
    raise ValueError(f"unknown root_source: {rule.root_source}")


def generate_candidate_space(
    boundary: Boundary,
    stable: StableStructure,
    rule: GenerationRule | None,
) -> dict[str, object]:
    """B・M_BとΓから候補空間を生成する。Γなしは空集合と区別する。"""
    if rule is None:
        return {
            "generation_status": "under_specified",
            "candidates": (),
        }

    candidates = []
    for root_pc in sorted(roots_for(boundary, stable, rule)):
        for quality in rule.qualities:
            candidate = Candidate(root_pc, quality)
            if rule.require_scale_closure and not candidate.pcs <= stable.pitch_inventory:
                continue
            candidates.append(candidate)

    return {
        "generation_status": "generated",
        "candidates": tuple(candidates),
    }


def labels(result: dict[str, object]) -> list[str]:
    return [candidate.label for candidate in result["candidates"]]


def run_checks() -> None:
    boundary, stable = c_major_state()
    diatonic = GenerationRule(
        root_source="stable_pitch_inventory",
        qualities=("major", "minor", "diminished"),
        require_scale_closure=True,
    )
    all_triads = GenerationRule(
        root_source="pitch_universe",
        qualities=("major", "minor", "diminished"),
        require_scale_closure=False,
    )
    major_diatonic = GenerationRule(
        root_source="stable_pitch_inventory",
        qualities=("major",),
        require_scale_closure=True,
    )

    unspecified = generate_candidate_space(boundary, stable, None)
    generated = generate_candidate_space(boundary, stable, diatonic)
    expanded = generate_candidate_space(boundary, stable, all_triads)
    major_only = generate_candidate_space(boundary, stable, major_diatonic)

    assert unspecified["generation_status"] == "under_specified"
    assert unspecified["candidates"] == ()
    assert generated["generation_status"] == "generated"
    assert labels(generated) == ["C", "Dm", "Em", "F", "G", "Am", "Bdim"]
    assert len(expanded["candidates"]) == 36
    assert labels(major_only) == ["C", "F", "G"]


def main() -> None:
    run_checks()
    boundary, stable = c_major_state()
    rules = {
        "Γなし": None,
        "Γ_diatonic_triad": GenerationRule(
            root_source="stable_pitch_inventory",
            qualities=("major", "minor", "diminished"),
            require_scale_closure=True,
        ),
        "Γ_all_triads": GenerationRule(
            root_source="pitch_universe",
            qualities=("major", "minor", "diminished"),
            require_scale_closure=False,
        ),
        "Γ_major_diatonic": GenerationRule(
            root_source="stable_pitch_inventory",
            qualities=("major",),
            require_scale_closure=True,
        ),
    }

    for name, rule in rules.items():
        result = generate_candidate_space(boundary, stable, rule)
        print(f"[{name}]")
        print(" ", "generation_status=", result["generation_status"])
        print(" ", "candidate_count=", len(result["candidates"]))
        print(" ", "candidates=", labels(result))


if __name__ == "__main__":
    main()
