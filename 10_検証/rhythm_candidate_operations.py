"""単純なリズム候補と制約の最小検証。

4/4の一定グリッド上で、表拍・裏拍だけを候補とする。
和声・音高・アクセントの意味は導入しない。
"""


BOUNDARY = {
    "meter": "4/4",
    "grid": "一定グリッド",
}
CANDIDATES = ("表拍", "裏拍")


def candidate_space(boundary: dict[str, str]) -> tuple[str, ...]:
    """今回の境界に対応する閉じた実験用候補空間を返す。"""
    if boundary != BOUNDARY:
        raise ValueError("この実験で定義していない境界です")
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
    candidates = candidate_space(BOUNDARY)
    changed = constrain_candidates(
        candidates,
        current="表拍",
        change_current=True,
    )
    impossible = constrain_candidates(
        candidates,
        current="表拍",
        change_current=True,
        target="休符",
    )

    assert candidates == ("表拍", "裏拍")
    assert changed["candidates"] == ("裏拍",)
    assert changed["target_specified"] is False
    assert changed["status"] == "locally_resolved"
    assert impossible["candidates"] == ()
    assert impossible["status"] == "no_candidate"


def main() -> None:
    run_checks()
    candidates = candidate_space(BOUNDARY)
    changed = constrain_candidates(
        candidates,
        current="表拍",
        change_current=True,
    )
    impossible = constrain_candidates(
        candidates,
        current="表拍",
        change_current=True,
        target="休符",
    )

    print("[B_4/4 + change(current)]")
    print(" ", "current=", changed["current"])
    print(" ", "target_specified=", changed["target_specified"])
    print(" ", "candidates=", changed["candidates"])
    print(" ", "status=", changed["status"])
    print("[B_4/4 + change(current) + target=休符]")
    print(" ", "candidates=", impossible["candidates"])
    print(" ", "status=", impossible["status"])


if __name__ == "__main__":
    main()
