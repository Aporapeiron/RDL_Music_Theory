"""周波数比を12TET上の半音数まで分解する最小検証。

純正比 3:2 と 12TET の 2^(7/12) を比較し、
周波数比・セント座標・12TET上の半音数を分離して表示する。

この実験は7半音で停止し、音名・綴りを必要とする音程名の判定は扱わない。

ここでの 12TET 写像は既知の記述規則であり、人間の知覚カテゴリーを
直接測定するものではない。RDL音楽_Coreへは追加しない。
"""

from dataclasses import dataclass
from math import isclose, log2


@dataclass(frozen=True)
class IntervalObservation:
    """対象側の周波数関係と、12TETまでの記述上の写像。"""

    f1_hz: float
    f2_hz: float
    ratio: float
    cents: float
    semitones_12tet: int
    residual_cents: float


@dataclass(frozen=True)
class IntervalBoundary:
    """今回の観測で、何を既知として比較するかを表すB。"""

    known_components: bool = True
    component_count: int = 2
    stationary_frequency: bool = True
    direction: str = "f2/f1"


DEFAULT_BOUNDARY = IntervalBoundary()


def observe_interval(
    f1_hz: float,
    f2_hz: float,
    boundary: IntervalBoundary = DEFAULT_BOUNDARY,
) -> IntervalObservation:
    """対象の周波数比を、連続座標と12TET半音数へ写像する。"""
    if f1_hz <= 0 or f2_hz <= 0:
        raise ValueError("frequencies must be positive")
    if not boundary.known_components or boundary.component_count != 2:
        raise ValueError("this experiment requires two known components")
    if not boundary.stationary_frequency or boundary.direction != "f2/f1":
        raise ValueError("this experiment requires stationary f2/f1 comparison")
    ratio = f2_hz / f1_hz
    cents = 1200.0 * log2(ratio)
    semitones = round(12.0 * log2(ratio))
    residual_cents = cents - 100.0 * semitones
    return IntervalObservation(
        f1_hz=f1_hz,
        f2_hz=f2_hz,
        ratio=ratio,
        cents=cents,
        semitones_12tet=semitones,
        residual_cents=residual_cents,
    )


def print_observation(name: str, observation: IntervalObservation) -> None:
    print(f"[{name}]")
    print(f"  ratio={observation.ratio:.12f}")
    print(f"  cents={observation.cents:.9f}")
    print(f"  semitones_12tet={observation.semitones_12tet}")
    print(f"  residual_cents={observation.residual_cents:+.9f}")


def run_checks() -> None:
    pure = observe_interval(100.0, 150.0)
    equal = observe_interval(100.0, 100.0 * 2 ** (7.0 / 12.0))
    pure_transposed = observe_interval(200.0, 300.0)

    # 物理比は異なるが、12TET上の記述カテゴリーは一致する。
    assert not isclose(pure.ratio, equal.ratio, rel_tol=0.0, abs_tol=1e-12)
    assert pure.semitones_12tet == 7
    assert equal.semitones_12tet == 7
    assert isclose(pure.cents, 701.955000865, abs_tol=1e-9)
    assert isclose(equal.cents, 700.0, abs_tol=1e-9)
    assert isclose(pure.residual_cents, 1.955000865, abs_tol=1e-9)
    assert isclose(equal.residual_cents, 0.0, abs_tol=1e-9)

    # 絶対周波数を変えても、比に基づく記述は保存される。
    assert isclose(pure.ratio, pure_transposed.ratio, abs_tol=1e-12)
    assert isclose(pure.cents, pure_transposed.cents, abs_tol=1e-9)
    assert pure.semitones_12tet == pure_transposed.semitones_12tet


def main() -> None:
    run_checks()
    pure = observe_interval(100.0, 150.0)
    equal = observe_interval(100.0, 100.0 * 2 ** (7.0 / 12.0))
    pure_transposed = observe_interval(200.0, 300.0)

    print("[Γ]")
    print("  Γ_ratio=f2/f1")
    print("  Γ_cents=1200*log2(ratio)")
    print("  Γ_12TET_round=round(12*log2(ratio))")
    print("  Γ_interval_name=未適用（音名・綴りが必要）")
    print_observation("pure 3:2", pure)
    print_observation("12TET 2^(7/12)", equal)
    print_observation("transposed 200:300", pure_transposed)
    print("[comparison]")
    print(f"  physical_ratio_equal={isclose(pure.ratio, equal.ratio, abs_tol=1e-12)}")
    print(
        "  12TET_category_equal="
        f"{pure.semitones_12tet == equal.semitones_12tet}"
    )


if __name__ == "__main__":
    main()
