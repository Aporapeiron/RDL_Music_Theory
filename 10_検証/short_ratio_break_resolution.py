"""短時間の比破断が観測分解能で検出・見落としされる最小実験。

既知の瞬時周波数モデルには短時間の比破断を含めるが、破断の検出は
Bのサンプル時点だけで行う。したがって、モデルに組み込まれた破断と、
観測時間窓内に破断が存在すること、観測点で検出された破断を別の状態として
記録する。

この実験も未知波形から周波数を推定するものではない。生成されたF(t)は
補助観測であり、主判定は既知軌道をBとΓ_point_ratioでサンプリングした比から
行う。
"""

from dataclasses import dataclass
from math import isclose, pi, sin, sqrt


@dataclass(frozen=True)
class ObservationBoundary:
    """波形をどの時間範囲・分解能・格子位相で観測するかを決めるB。"""

    duration_s: float = 2.0
    sample_rate_hz: int = 10_000
    sampling_phase_s: float = 0.0


@dataclass(frozen=True)
class PointRatioRule:
    """点サンプルされた比から破断を判定するΓ_point_ratio。"""

    ratio_tolerance: float = 1e-9


@dataclass(frozen=True)
class TransientRatioCase:
    """通常比から短時間だけ外れる既知成分モデル。"""

    name: str
    f1_hz: float
    baseline_ratio: float
    transient_ratio: float
    break_start_s: float
    break_end_s: float

    def __post_init__(self) -> None:
        if self.f1_hz <= 0:
            raise ValueError("f1_hz must be positive")
        if self.baseline_ratio <= 0 or self.transient_ratio <= 0:
            raise ValueError("ratios must be positive")
        if not 0 <= self.break_start_s < self.break_end_s:
            raise ValueError("break interval must be positive and ordered")

    @property
    def break_duration_s(self) -> float:
        return self.break_end_s - self.break_start_s

    def ratio_at(self, time_s: float) -> float:
        if self.break_start_s <= time_s < self.break_end_s:
            return self.transient_ratio
        return self.baseline_ratio

    def f1_at(self, time_s: float) -> float:
        del time_s
        return self.f1_hz

    def f2_at(self, time_s: float) -> float:
        return self.f1_at(time_s) * self.ratio_at(time_s)

    def f1_phase_cycles_at(self, time_s: float) -> float:
        return self.f1_hz * time_s

    def f2_phase_cycles_at(self, time_s: float) -> float:
        """破断区間の長さを積分したf2の位相を返す。"""
        clamped_time = max(time_s, 0.0)
        transient_overlap_s = max(
            0.0,
            min(clamped_time, self.break_end_s) - self.break_start_s,
        )
        baseline_cycles = self.f1_hz * self.baseline_ratio * time_s
        correction_cycles = (
            self.f1_hz
            * (self.transient_ratio - self.baseline_ratio)
            * transient_overlap_s
        )
        return baseline_cycles + correction_cycles


@dataclass(frozen=True)
class ResolutionObservation:
    case_name: str
    sample_rate_hz: int
    sample_count: int
    sampling_interval_s: float
    sampling_phase_s: float
    break_duration_s: float
    model_ratio_break_present: bool
    break_intersects_observation_window: bool
    sampled_break_count: int
    sampled_break_detected: bool
    observed_ratio_preserved: bool
    max_observed_ratio_deviation: float
    waveform_peak: float
    waveform_rms: float


def observation_times(boundary: ObservationBoundary) -> tuple[float, ...]:
    if boundary.duration_s <= 0 or boundary.sample_rate_hz <= 0:
        raise ValueError("duration and sample rate must be positive")
    sampling_interval_s = 1 / boundary.sample_rate_hz
    if not 0 <= boundary.sampling_phase_s < sampling_interval_s:
        raise ValueError(
            "sampling_phase_s must be within one sampling interval from zero"
        )
    sample_count = round(boundary.duration_s * boundary.sample_rate_hz)
    return tuple(
        boundary.sampling_phase_s + index / boundary.sample_rate_hz
        for index in range(sample_count)
    )


def synthesize_waveform(
    case: TransientRatioCase, boundary: ObservationBoundary
) -> tuple[float, ...]:
    """積分位相から短時間比破断を含む2成分波形を生成する。"""
    return tuple(
        sin(2 * pi * case.f1_phase_cycles_at(time_s))
        + sin(2 * pi * case.f2_phase_cycles_at(time_s))
        for time_s in observation_times(boundary)
    )


def observe_resolution(
    case: TransientRatioCase,
    boundary: ObservationBoundary,
    rule: PointRatioRule,
) -> ResolutionObservation:
    """Bのサンプル時点をΓ_point_ratioで判定する。"""
    times = observation_times(boundary)
    ratios = tuple(case.f2_at(time_s) / case.f1_at(time_s) for time_s in times)
    ratio_start = ratios[0]
    deviations = tuple(abs(ratio - ratio_start) for ratio in ratios)
    max_deviation = max(deviations)
    sampled_break_count = sum(
        case.break_start_s <= time_s < case.break_end_s for time_s in times
    )
    samples = synthesize_waveform(case, boundary)

    return ResolutionObservation(
        case_name=case.name,
        sample_rate_hz=boundary.sample_rate_hz,
        sample_count=len(times),
        sampling_interval_s=1 / boundary.sample_rate_hz,
        sampling_phase_s=boundary.sampling_phase_s,
        break_duration_s=case.break_duration_s,
        model_ratio_break_present=(
            case.transient_ratio != case.baseline_ratio
        ),
        break_intersects_observation_window=(
            max(0.0, min(case.break_end_s, boundary.duration_s)
                  - max(case.break_start_s, 0.0)) > 0.0
        ),
        sampled_break_count=sampled_break_count,
        sampled_break_detected=max_deviation > rule.ratio_tolerance,
        observed_ratio_preserved=max_deviation <= rule.ratio_tolerance,
        max_observed_ratio_deviation=max_deviation,
        waveform_peak=max(abs(value) for value in samples),
        waveform_rms=sqrt(sum(value * value for value in samples) / len(samples)),
    )


def make_case() -> TransientRatioCase:
    return TransientRatioCase(
        name="short_ratio_break_0_5ms",
        f1_hz=100.0,
        baseline_ratio=1.5,
        transient_ratio=1.6,
        break_start_s=1.23425,
        break_end_s=1.23475,
    )


def run_checks() -> None:
    case = make_case()
    rule = PointRatioRule()
    high = observe_resolution(
        case, ObservationBoundary(sample_rate_hz=10_000), rule
    )
    coarse = observe_resolution(
        case, ObservationBoundary(sample_rate_hz=1_000), rule
    )

    assert isclose(case.break_duration_s, 0.0005, abs_tol=1e-15)
    assert high.model_ratio_break_present is True
    assert coarse.model_ratio_break_present is True
    assert high.break_intersects_observation_window is True
    assert coarse.break_intersects_observation_window is True

    assert high.sampled_break_count == 5
    assert high.sampled_break_detected is True
    assert high.observed_ratio_preserved is False
    assert isclose(high.max_observed_ratio_deviation, 0.1, abs_tol=1e-15)

    assert coarse.sampled_break_count == 0
    assert coarse.sampled_break_detected is False
    assert coarse.observed_ratio_preserved is True
    assert coarse.max_observed_ratio_deviation == 0.0

    assert high.sample_count == 20_000
    assert coarse.sample_count == 2_000
    assert high.waveform_peak > 0
    assert coarse.waveform_rms > 0

    outside_boundary = observe_resolution(
        case,
        ObservationBoundary(
            duration_s=1.0,
            sample_rate_hz=1_000,
        ),
        rule,
    )
    assert outside_boundary.model_ratio_break_present is True
    assert outside_boundary.break_intersects_observation_window is False


def print_observation(observation: ResolutionObservation) -> None:
    print(f"[{observation.case_name}]")
    print(f"  sample_rate_hz={observation.sample_rate_hz}")
    print(f"  sample_count={observation.sample_count}")
    print(f"  sampling_interval_s={observation.sampling_interval_s:.9g}")
    print(f"  sampling_phase_s={observation.sampling_phase_s:.9g}")
    print(f"  break_duration_s={observation.break_duration_s:.9g}")
    print(
        "  model_ratio_break_present="
        f"{observation.model_ratio_break_present}"
    )
    print(
        "  break_intersects_observation_window="
        f"{observation.break_intersects_observation_window}"
    )
    print(f"  sampled_break_count={observation.sampled_break_count}")
    print(f"  sampled_break_detected={observation.sampled_break_detected}")
    print(f"  observed_ratio_preserved={observation.observed_ratio_preserved}")
    print(
        "  max_observed_ratio_deviation="
        f"{observation.max_observed_ratio_deviation:.9g}"
    )
    print(f"  waveform_peak={observation.waveform_peak:.9g}")
    print(f"  waveform_rms={observation.waveform_rms:.9g}")


def main() -> None:
    run_checks()
    case = make_case()
    rule = PointRatioRule()
    print("[case]")
    print(f"  f1_hz={case.f1_hz}")
    print(f"  baseline_ratio={case.baseline_ratio}")
    print(f"  transient_ratio={case.transient_ratio}")
    print(f"  break_start_s={case.break_start_s}")
    print(f"  break_end_s={case.break_end_s}")
    print(f"  ratio_tolerance={rule.ratio_tolerance}")
    for sample_rate_hz in (10_000, 1_000):
        observation = observe_resolution(
            case, ObservationBoundary(sample_rate_hz=sample_rate_hz), rule
        )
        print_observation(observation)


if __name__ == "__main__":
    main()
