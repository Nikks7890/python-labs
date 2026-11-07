from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from functools import reduce
from itertools import islice
from typing import Any, TypedDict


class Record(TypedDict, total=False):
    id: int
    name: str
    category: str
    results: list[float]
    best: float
    avg: float
    score: float


def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def _c(x: Any) -> Any:
        for f in reversed(funcs):
            x = f(x)
        return x

    return _c


def pipe(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def _p(x: Any) -> Any:
        for f in funcs:
            x = f(x)
        return x

    return _p


def juxt(*funcs: Callable[[Any], Any]) -> Callable[[Any], tuple[Any, ...]]:
    return lambda x: tuple(f(x) for f in funcs)


def with_best_avg() -> Callable[[Iterable[Record]], Iterator[Record]]:
    def _f(recs: Iterable[Record]) -> Iterator[Record]:
        for r in recs:
            vals = [float(v) for v in (r.get("results") or [])]
            best = max(vals) if vals else 0.0
            avg = sum(vals) / len(vals) if vals else 0.0
            yield {**r, "best": best, "avg": avg}

    return _f


def boost_category(category: str, factor: float) -> Callable[[Iterable[Record]], Iterator[Record]]:
    def _f(recs: Iterable[Record]) -> Iterator[Record]:
        for r in recs:
            best = float(r.get("best", 0.0))
            avg = float(r.get("avg", 0.0))
            if r.get("category") == category:
                best *= factor
                avg *= factor
            yield {**r, "best": best, "avg": avg}

    return _f


def with_score() -> Callable[[Iterable[Record]], Iterator[Record]]:
    def _f(recs: Iterable[Record]) -> Iterator[Record]:
        for r in recs:
            score = float(r.get("best", 0.0)) * 0.6 + float(r.get("avg", 0.0)) * 0.4
            yield {**r, "score": score}

    return _f


def only_admitted(min_score: float) -> Callable[[Iterable[Record]], Iterator[Record]]:
    return lambda recs: (r for r in recs if float(r.get("score", 0.0)) >= min_score)


def normalize_names() -> Callable[[Iterable[Record]], Iterator[Record]]:
    return lambda recs: ({**r, "name": str(r.get("name", "")).strip().title()} for r in recs)


def sort_by_score_desc() -> Callable[[Iterable[Record]], list[Record]]:
    return lambda recs: sorted(
        recs, key=lambda r: (-float(r.get("score", 0.0)), int(r.get("id", 0)))
    )


def take(n: int) -> Callable[[Iterable[Record]], list[Record]]:
    return lambda recs: list(islice(recs, n))


def reduce_stats(recs: Iterable[Record]) -> dict[str, float]:
    init: dict[str, float] = {"count": 0.0, "sum_points": 0.0}

    def _step(acc: dict[str, float], r: Record) -> dict[str, float]:
        return {
            "count": acc["count"] + 1,
            "sum_points": acc["sum_points"] + float(r.get("score", 0.0)),
        }

    acc = reduce(_step, recs, init)
    avg = acc["sum_points"] / acc["count"] if acc["count"] else 0.0
    return {"count": acc["count"], "sum_points": acc["sum_points"], "avg_points": avg}


def build_pipeline(
    top_n: int = 3, category: str = "Pro", factor: float = 1.1, min_score: float = 0.0
) -> Callable[[Iterable[Record]], list[Record]]:
    return pipe(  # type: ignore
        with_best_avg(),
        boost_category(category, factor),
        with_score(),
        only_admitted(min_score),
        normalize_names(),
        sort_by_score_desc(),
        take(top_n),
    )
