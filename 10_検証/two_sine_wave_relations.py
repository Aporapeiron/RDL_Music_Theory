"""2本の正弦波から関係候補を抽出する最小検証。

音名・コード・調性を入力にせず、観測境界Bの内部で
周波数比・共通周期・反復性を調べる。

この実験は、未知波形から成分を推定するスペクトル解析ではない。
2成分を既知の観測成分として与え、
既知成分モデルによる関係候補と、実サンプル列による再帰誤差の補助観測を分けて検査する
最初の足場である。波形関係をRDL音楽_Coreへ追加することは目的としない。
"""

from dataclasses import dataclass
from fractions import Fraction
from math import pi, sin, sqrt


@dataclass(frozen=True)
class ObservationBoundary:
    """波形をどの時間範囲・時間分解能で観測するかを決めるB。"""

    duration_s: float = 4.0
    sample_rate_hz: int = 10_000


@dataclass(frozen=True)
class RelationRule:
    """観測された成分から関係を抽出する実験用規則Γ。"""

    max_denominator: int = 16
    ratio_tolerance: float = 1e-6
    min_repetitions: float = 3.0


@dataclass(frozen=True)
class RelationObservation:
    """2成分間から抽出した関係と、その境界内での判定。"""

    f1_hz: float
    f2_hz: float
    ratio: float
    numerator: int
    denominator: int
    ratio_error: float
    difference_frequency_hz: float
    common_period_candidate_s: float
    observed_repetitions: float
    phase_drift_rad: float
    recurrence_error: float | None
    # 固定周波数の既知成分モデル上での保存関係。
    ratio_preserved: bool
    # Γとduration_sに依存する、有限窓内の短周期再帰候補。
    short_recurrence_candidate: bool


def synthesize_two_sine_wave(
    f1_hz: float, f2_hz: float, boundary: ObservationBoundary
) -> tuple[float, ...]:
    """2本の正弦波を合成し、観測窓内の実サンプル列F(t)を返す。"""
    sample_count = round(boundary.duration_s * boundary.sample_rate_hz)
    return tuple(
        sin(2 * pi * f1_hz * index / boundary.sample_rate_hz)
        + sin(2 * pi * f2_hz * index / boundary.sample_rate_hz)
        for index in range(sample_count)
    )


def normalized_recurrence_error(
    samples: tuple[float, ...], shift_samples: int
) -> float | None:
    """候補周期だけ離した波形の正規化RMSEを計算する。"""
    if shift_samples <= 0 or shift_samples >= len(samples):
        return None

    compared = len(samples) - shift_samples
    squared_error = sum(
        (samples[index] - samples[index + shift_samples]) ** 2
        for index in range(compared)
    ) / compared
    signal_power = sum(value * value for value in samples[:compared]) / compared
    if signal_power == 0:
        return None
    return sqrt(squared_error / signal_power)


def observe_relation(
    f1_hz: float,
    f2_hz: float,
    boundary: ObservationBoundary,
    rule: RelationRule,
) -> RelationObservation:
    """Bのもとで観測し、Γに従って2成分間の関係を抽出する。"""
    if f1_hz <= 0 or f2_hz <= 0:
        raise ValueError("frequencies must be positive")

    ratio = f2_hz / f1_hz
    approximation = Fraction(ratio).limit_denominator(rule.max_denominator)
    numerator = approximation.numerator
    denominator = approximation.denominator
    ratio_error = abs(ratio - numerator / denominator)
    common_period_candidate_s = denominator / f1_hz
    observed_repetitions = boundary.duration_s / common_period_candidate_s
    phase_drift_rad = 2 * pi * abs(
        f2_hz * common_period_candidate_s - numerator
    )

    samples = synthesize_two_sine_wave(f1_hz, f2_hz, boundary)
    shift_samples = round(
        common_period_candidate_s * boundary.sample_rate_hz
    )
    recurrence_error = normalized_recurrence_error(samples, shift_samples)
    # 固定周波数の既知成分モデルでは、周波数比は時間窓をまたいで保存される。
    # これは短い共通周期の有無とは別の関係軸である。
    ratio_preserved = True
    short_recurrence_candidate = (
        ratio_error <= rule.ratio_tolerance
        and observed_repetitions >= rule.min_repetitions
    )

    return RelationObservation(
        f1_hz=f1_hz,
        f2_hz=f2_hz,
        ratio=ratio,
        numerator=numerator,
        denominator=denominator,
        ratio_error=ratio_error,
        difference_frequency_hz=abs(f2_hz - f1_hz),
        common_period_candidate_s=common_period_candidate_s,
        observed_repetitions=observed_repetitions,
        phase_drift_rad=phase_drift_rad,
        recurrence_error=recurrence_error,
        ratio_preserved=ratio_preserved,
        short_recurrence_candidate=short_recurrence_candidate,
    )


def relation_label(observation: RelationObservation) -> str:
    """実験結果の状態を、音楽語彙と分けて表示する。"""
    if observation.short_recurrence_candidate:
        return "short_recurrence_candidate"
    return "no_short_relation_under_boundary"


def run_checks() -> None:
    boundary = ObservationBoundary()
    rule = RelationRule()

    octave = observe_relation(100.0, 200.0, boundary, rule)
    ratio_three_two = observe_relation(100.0, 150.0, boundary, rule)
    near_octave = observe_relation(100.0, 201.0, boundary, rule)
    irrational = observe_relation(100.0, sqrt(2) * 100.0, boundary, rule)

    assert (octave.numerator, octave.denominator) == (2, 1)
    assert octave.ratio_preserved is True
    assert octave.short_recurrence_candidate is True
    assert octave.recurrence_error is not None
    assert octave.recurrence_error < 1e-10

    assert (ratio_three_two.numerator, ratio_three_two.denominator) == (3, 2)
    assert ratio_three_two.ratio_preserved is True
    assert ratio_three_two.short_recurrence_candidate is True
    assert near_octave.ratio_preserved is True
    assert near_octave.short_recurrence_candidate is False
    assert irrational.ratio_preserved is True
    assert irrational.short_recurrence_candidate is False
    assert near_octave.difference_frequency_hz == 101.0
    assert irrational.difference_frequency_hz > 41.0

    wider_rule = RelationRule(max_denominator=128)
    near_octave_wider = observe_relation(100.0, 201.0, boundary, wider_rule)
    assert (near_octave_wider.numerator, near_octave_wider.denominator) == (201, 100)
    assert near_octave_wider.ratio_preserved is True
    assert near_octave_wider.short_recurrence_candidate is True

    short_boundary = ObservationBoundary(duration_s=0.01)
    short_observation = observe_relation(100.0, 150.0, short_boundary, rule)
    assert short_observation.observed_repetitions < 1.0
    assert short_observation.ratio_preserved is True
    assert short_observation.short_recurrence_candidate is False

    coarse_boundary = ObservationBoundary(sample_rate_hz=1_000)
    coarse_observation = observe_relation(100.0, 150.0, coarse_boundary, rule)
    assert coarse_observation.ratio_preserved == ratio_three_two.ratio_preserved
    assert (
        coarse_observation.short_recurrence_candidate
        == ratio_three_two.short_recurrence_candidate
    )


def print_observation(
    name: str, observation: RelationObservation
) -> None:
    print(f"[{name}]")
    print(f"  ratio={observation.ratio:.9f}")
    print(
        "  rational_relation="
        f"{observation.numerator}:{observation.denominator}"
    )
    print(f"  ratio_error={observation.ratio_error:.9g}")
    print(
        "  difference_frequency_hz="
        f"{observation.difference_frequency_hz:.9g}"
    )
    print(
        "  common_period_candidate_s="
        f"{observation.common_period_candidate_s:.9g}"
    )
    print(f"  observed_repetitions={observation.observed_repetitions:.9g}")
    print(f"  phase_drift_rad={observation.phase_drift_rad:.9g}")
    print(f"  recurrence_error={observation.recurrence_error}")
    print(f"  ratio_preserved={observation.ratio_preserved}")
    print(
        "  short_recurrence_candidate="
        f"{observation.short_recurrence_candidate}"
    )
    print(f"  relation_status={relation_label(observation)}")


def main() -> None:
    run_checks()
    boundary = ObservationBoundary()
    rule = RelationRule()
    cases = {
        "100 + 200": (100.0, 200.0),
        "100 + 150": (100.0, 150.0),
        "100 + 201": (100.0, 201.0),
        "100 + sqrt(2)*100": (100.0, sqrt(2) * 100.0),
    }

    print("[boundary]")
    print(f"  duration_s={boundary.duration_s}")
    print(f"  sample_rate_hz={boundary.sample_rate_hz}")
    print("[Γ_ratio_period]")
    print(f"  max_denominator={rule.max_denominator}")
    print(f"  ratio_tolerance={rule.ratio_tolerance}")
    print(f"  min_repetitions={rule.min_repetitions}")
    for name, (f1_hz, f2_hz) in cases.items():
        print_observation(name, observe_relation(f1_hz, f2_hz, boundary, rule))

    print("[Γ change: max_denominator=128]")
    print_observation(
        "100 + 201",
        observe_relation(100.0, 201.0, boundary, RelationRule(max_denominator=128)),
    )
    print("[boundary change: duration_s=0.01]")
    print_observation(
        "100 + 150",
        observe_relation(100.0, 150.0, ObservationBoundary(duration_s=0.01), rule),
    )


if __name__ == "__main__":
    main()
