"""時間変化する2成分周波数の関係保存を検査する最小実験。

固定周波数の既知成分モデルから一段進み、各成分の周波数を時間の関数として
与える。周波数そのものではなく、時間変化の中で比が保存されるかを観測する。

この実験も未知波形から周波数を推定するものではない。周波数軌道は既知の
モデルとして与え、そこから波形サンプルF(t)を生成し、モデル上の保存関係と
実サンプル列を分けて記録する。短周期再帰の候補化は06の実験に残し、ここでは
関係保存の軸に集中する。
"""

from dataclasses import dataclass
from math import pi, sin, sqrt


@dataclass(frozen=True)
class ObservationBoundary:
    """時間変化する波形をどの範囲・分解能で観測するかを決めるB。"""

    duration_s: float = 4.0
    sample_rate_hz: int = 10_000


@dataclass(frozen=True)
class RelationRule:
    """時間軌道から保存関係を判定する実験用規則Γ。"""

    ratio_tolerance: float = 1e-9
    frequency_tolerance_hz: float = 1e-9


@dataclass(frozen=True)
class LinearFrequency:
    """線形に変化する瞬時周波数 f(t) = start + slope*t。"""

    start_hz: float
    slope_hz_per_s: float = 0.0

    def at(self, time_s: float) -> float:
        frequency = self.start_hz + self.slope_hz_per_s * time_s
        if frequency <= 0:
            raise ValueError("frequency must remain positive")
        return frequency

    def phase_cycles_at(self, time_s: float) -> float:
        """0秒からの積分周波数。sin(2π f(t)t)ではなく位相を積分する。"""
        return self.start_hz * time_s + 0.5 * self.slope_hz_per_s * time_s**2


@dataclass(frozen=True)
class TimeVaryingCase:
    name: str
    f1: LinearFrequency
    f2: LinearFrequency


@dataclass(frozen=True)
class RelationObservation:
    case_name: str
    f1_start_hz: float
    f1_end_hz: float
    f2_start_hz: float
    f2_end_hz: float
    ratio_start: float
    ratio_end: float
    max_ratio_deviation: float
    max_f1_deviation_hz: float
    max_f2_deviation_hz: float
    f1_value_preserved: bool
    f2_value_preserved: bool
    ratio_preserved: bool
    sample_count: int
    waveform_peak: float
    waveform_rms: float


def observation_times(boundary: ObservationBoundary) -> tuple[float, ...]:
    if boundary.duration_s <= 0 or boundary.sample_rate_hz <= 0:
        raise ValueError("duration and sample rate must be positive")
    sample_count = round(boundary.duration_s * boundary.sample_rate_hz)
    return tuple(index / boundary.sample_rate_hz for index in range(sample_count))


def synthesize_time_varying_two_sine_wave(
    case: TimeVaryingCase, boundary: ObservationBoundary
) -> tuple[float, ...]:
    """積分した位相から時間変化する2本の正弦波を合成する。"""
    return tuple(
        sin(2 * pi * case.f1.phase_cycles_at(time_s))
        + sin(2 * pi * case.f2.phase_cycles_at(time_s))
        for time_s in observation_times(boundary)
    )


def max_absolute_deviation(
    values: tuple[float, ...], reference: float
) -> float:
    return max(abs(value - reference) for value in values)


def observe_relation(
    case: TimeVaryingCase,
    boundary: ObservationBoundary,
    rule: RelationRule,
) -> RelationObservation:
    """Bの時間窓で既知の周波数軌道を観測し、保存関係を抽出する。"""
    times = observation_times(boundary)
    f1_values = tuple(case.f1.at(time_s) for time_s in times)
    f2_values = tuple(case.f2.at(time_s) for time_s in times)
    ratios = tuple(f2 / f1 for f1, f2 in zip(f1_values, f2_values))

    f1_start_hz = f1_values[0]
    f2_start_hz = f2_values[0]
    ratio_start = ratios[0]
    max_f1_deviation_hz = max_absolute_deviation(f1_values, f1_start_hz)
    max_f2_deviation_hz = max_absolute_deviation(f2_values, f2_start_hz)
    max_ratio_deviation = max_absolute_deviation(ratios, ratio_start)

    samples = synthesize_time_varying_two_sine_wave(case, boundary)
    waveform_peak = max(abs(value) for value in samples)
    waveform_rms = sqrt(sum(value * value for value in samples) / len(samples))

    return RelationObservation(
        case_name=case.name,
        f1_start_hz=f1_start_hz,
        f1_end_hz=f1_values[-1],
        f2_start_hz=f2_start_hz,
        f2_end_hz=f2_values[-1],
        ratio_start=ratio_start,
        ratio_end=ratios[-1],
        max_ratio_deviation=max_ratio_deviation,
        max_f1_deviation_hz=max_f1_deviation_hz,
        max_f2_deviation_hz=max_f2_deviation_hz,
        f1_value_preserved=(
            max_f1_deviation_hz <= rule.frequency_tolerance_hz
        ),
        f2_value_preserved=(
            max_f2_deviation_hz <= rule.frequency_tolerance_hz
        ),
        ratio_preserved=max_ratio_deviation <= rule.ratio_tolerance,
        sample_count=len(samples),
        waveform_peak=waveform_peak,
        waveform_rms=waveform_rms,
    )


def make_cases() -> tuple[TimeVaryingCase, ...]:
    return (
        TimeVaryingCase(
            name="A_fixed_values_fixed_ratio",
            f1=LinearFrequency(100.0),
            f2=LinearFrequency(150.0),
        ),
        TimeVaryingCase(
            name="B_moving_values_fixed_ratio",
            f1=LinearFrequency(100.0, 1.0),
            f2=LinearFrequency(150.0, 1.5),
        ),
        TimeVaryingCase(
            name="C_partial_fixed_values_changing_ratio",
            f1=LinearFrequency(100.0),
            f2=LinearFrequency(150.0, 1.0),
        ),
    )


def run_checks() -> None:
    boundary = ObservationBoundary()
    rule = RelationRule()
    observations = {
        case.name: observe_relation(case, boundary, rule)
        for case in make_cases()
    }

    case_a = observations["A_fixed_values_fixed_ratio"]
    assert case_a.f1_value_preserved is True
    assert case_a.f2_value_preserved is True
    assert case_a.ratio_preserved is True
    assert case_a.ratio_start == 1.5
    assert case_a.ratio_end == 1.5

    case_b = observations["B_moving_values_fixed_ratio"]
    assert case_b.f1_value_preserved is False
    assert case_b.f2_value_preserved is False
    assert case_b.ratio_preserved is True
    assert case_b.f1_end_hz > case_b.f1_start_hz
    assert case_b.f2_end_hz > case_b.f2_start_hz
    assert case_b.max_ratio_deviation < 1e-12

    case_c = observations["C_partial_fixed_values_changing_ratio"]
    assert case_c.f1_value_preserved is True
    assert case_c.f2_value_preserved is False
    assert case_c.ratio_preserved is False
    assert case_c.ratio_end > case_c.ratio_start

    assert all(
        observation.sample_count == 40_000
        for observation in observations.values()
    )
    assert all(
        observation.waveform_peak > 0 for observation in observations.values()
    )
    assert all(
        observation.waveform_rms > 0 for observation in observations.values()
    )


def print_observation(observation: RelationObservation) -> None:
    print(f"[{observation.case_name}]")
    print(
        f"  f1_hz={observation.f1_start_hz:.9g}"
        f" -> {observation.f1_end_hz:.9g}"
    )
    print(
        f"  f2_hz={observation.f2_start_hz:.9g}"
        f" -> {observation.f2_end_hz:.9g}"
    )
    print(
        f"  ratio={observation.ratio_start:.9g}"
        f" -> {observation.ratio_end:.9g}"
    )
    print(f"  max_ratio_deviation={observation.max_ratio_deviation:.9g}")
    print(f"  max_f1_deviation_hz={observation.max_f1_deviation_hz:.9g}")
    print(f"  max_f2_deviation_hz={observation.max_f2_deviation_hz:.9g}")
    print(f"  f1_value_preserved={observation.f1_value_preserved}")
    print(f"  f2_value_preserved={observation.f2_value_preserved}")
    print(f"  ratio_preserved={observation.ratio_preserved}")
    print(f"  sample_count={observation.sample_count}")
    print(f"  waveform_peak={observation.waveform_peak:.9g}")
    print(f"  waveform_rms={observation.waveform_rms:.9g}")


def main() -> None:
    run_checks()
    boundary = ObservationBoundary()
    rule = RelationRule()
    print("[boundary]")
    print(f"  duration_s={boundary.duration_s}")
    print(f"  sample_rate_hz={boundary.sample_rate_hz}")
    print("[Γ_ratio_time]")
    print(f"  ratio_tolerance={rule.ratio_tolerance}")
    print(f"  frequency_tolerance_hz={rule.frequency_tolerance_hz}")
    for case in make_cases():
        print_observation(observe_relation(case, boundary, rule))


if __name__ == "__main__":
    main()
