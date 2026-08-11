"""音楽語彙を使わない候補集合と制約の最小検証。

この実験では、候補を単なるラベル A/B/C として扱う。
境界・拍子・音高・和声・リズムの意味は導入しない。
"""


CANDIDATES = ("A", "B", "C")


def candidate_space() -> tuple[str, ...]:
    """純粋集合実験へ直接入力する候補空間 C を返す。"""
    return CANDIDATES


def constrain_candidates(
    candidates: tuple[str, ...],
    *,
    current: str,
    change_current: bool,
    target: str | None = None,
) -> dict[str, object]:
    """現在候補の変更と目標条件を候補空間へ適用する。"""
    result = list(candidates)
    if change_current:
        result = [candidate for candidate in result if candidate != current]
    if target is not None:
        result = [candidate for candidate in result if candidate == target]

    if len(result) == 0:
        status = "no_candidate"
    elif len(result) == 1:
        status = "locally_resolved"
    else:
        status = "underdetermined"

    return {
        "current": current,
        "target_specified": target is not None,
        "candidates": tuple(result),
        "status": status,
    }


def run_checks() -> None:
    candidates = candidate_space()
    changed = constrain_candidates(
        candidates,
        current="A",
        change_current=True,
    )
    targeted = constrain_candidates(
        candidates,
        current="A",
        change_current=True,
        target="C",
    )
    impossible = constrain_candidates(
        candidates,
        current="A",
        change_current=True,
        target="X",
    )
    singleton = constrain_candidates(
        ("B",),
        current="A",
        change_current=False,
    )

    assert candidates == ("A", "B", "C")
    assert changed["candidates"] == ("B", "C")
    assert changed["status"] == "underdetermined"
    assert targeted["candidates"] == ("C",)
    assert targeted["status"] == "locally_resolved"
    assert impossible["candidates"] == ()
    assert impossible["status"] == "no_candidate"
    assert singleton["target_specified"] is False
    assert singleton["status"] == "locally_resolved"


def main() -> None:
    run_checks()
    candidates = candidate_space()

    changed = constrain_candidates(
        candidates,
        current="A",
        change_current=True,
    )
    targeted = constrain_candidates(
        candidates,
        current="A",
        change_current=True,
        target="C",
    )
    impossible = constrain_candidates(
        candidates,
        current="A",
        change_current=True,
        target="X",
    )

    print("[C + change(current)]")
    print(" ", "candidates=", changed["candidates"])
    print(" ", "status=", changed["status"])
    print("[C + change(current) + target=C]")
    print(" ", "candidates=", targeted["candidates"])
    print(" ", "status=", targeted["status"])
    print("[C + change(current) + target=X]")
    print(" ", "candidates=", impossible["candidates"])
    print(" ", "status=", impossible["status"])


if __name__ == "__main__":
    main()
