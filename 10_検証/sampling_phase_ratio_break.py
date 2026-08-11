"""同じsample_rateでも観測格子の開始位相で破断検出が変わる最小実験。

08の既知モデルとΓ_point_ratioをそのまま使い、Bのsampling_phase_sだけを
変える。これにより、分解能だけでなく観測格子の配置も、何が観測されたかを
決める条件であることを確認する。
"""

from math import isclose

from short_ratio_break_resolution import (
    ObservationBoundary,
    PointRatioRule,
    ResolutionObservation,
    make_case,
    observe_resolution,
)


SAMPLE_RATE_HZ = 1_000
BASE_SAMPLING_PHASE_S = 0.0
SHIFTED_SAMPLING_PHASE_S = 0.0005


def make_observations() -> tuple[ResolutionObservation, ResolutionObservation]:
    case = make_case()
    rule = PointRatioRule()
    base = observe_resolution(
        case,
        ObservationBoundary(
            sample_rate_hz=SAMPLE_RATE_HZ,
            sampling_phase_s=BASE_SAMPLING_PHASE_S,
        ),
        rule,
    )
    shifted = observe_resolution(
        case,
        ObservationBoundary(
            sample_rate_hz=SAMPLE_RATE_HZ,
            sampling_phase_s=SHIFTED_SAMPLING_PHASE_S,
        ),
        rule,
    )
    return base, shifted


def run_checks() -> None:
    base, shifted = make_observations()

    assert base.sample_rate_hz == shifted.sample_rate_hz == SAMPLE_RATE_HZ
    assert base.sample_count == shifted.sample_count
    assert base.sampling_interval_s == shifted.sampling_interval_s
    assert base.sampling_phase_s == BASE_SAMPLING_PHASE_S
    assert shifted.sampling_phase_s == SHIFTED_SAMPLING_PHASE_S

    assert base.model_ratio_break_present is True
    assert shifted.model_ratio_break_present is True
    assert base.break_intersects_observation_window is True
    assert shifted.break_intersects_observation_window is True

    assert base.sampled_break_count == 0
    assert base.sampled_break_detected is False
    assert base.observed_ratio_preserved is True
    assert base.max_observed_ratio_deviation == 0.0

    assert shifted.sampled_break_count == 1
    assert shifted.sampled_break_detected is True
    assert shifted.observed_ratio_preserved is False
    assert isclose(shifted.max_observed_ratio_deviation, 0.1, abs_tol=1e-15)


def print_observation(label: str, observation: ResolutionObservation) -> None:
    print(f"[{label}]")
    print(f"  sample_rate_hz={observation.sample_rate_hz}")
    print(f"  sample_count={observation.sample_count}")
    print(f"  sampling_interval_s={observation.sampling_interval_s:.9g}")
    print(f"  sampling_phase_s={observation.sampling_phase_s:.9g}")
    print(f"  model_ratio_break_present={observation.model_ratio_break_present}")
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


def main() -> None:
    run_checks()
    base, shifted = make_observations()
    print("[case]")
    print(f"  sample_rate_hz={SAMPLE_RATE_HZ}")
    print("  only sampling_phase_s changes")
    print_observation("phase_0", base)
    print_observation("phase_0.5ms", shifted)


if __name__ == "__main__":
    main()
