from collections.abc import Callable, Iterable
from functools import partial, reduce
from operator import itemgetter, methodcaller
from typing import Any

Row = dict[str, Any]

get_name = itemgetter("name")
get_country = itemgetter("country")
get_points = itemgetter("points")
get_penalties = itemgetter("penalties")
get_age = itemgetter("age")

strip = methodcaller("strip")
title = methodcaller("title")


def pipeline(value: Any, *funcs: Callable[[Any], Any]) -> Any:
    # пропускаємо значення через усі функції по черзі
    return reduce(lambda acc, f: f(acc), funcs, value)


def mapf(fn: Callable[[Any], Any]) -> Callable[[Iterable[Any]], Any]:
    return partial(map, fn)


def filt(pred: Callable[[Any], bool]) -> Callable[[Iterable[Any]], Any]:
    return partial(filter, pred)


def normalize(r: Row) -> Row:
    # чистимо рядок: пробіли, регістр, типи
    return {
        "name": title(strip(get_name(r))),
        "country": title(strip(get_country(r))),
        "points": float(get_points(r)),
        "penalties": float(get_penalties(r)),
        "age": int(get_age(r)),
    }


def add_final(coef: float, r: Row) -> Row:
    # final_points = points - penalties * coef (новий словник, старий не міняємо)
    return {**r, "final_points": get_points(r) - get_penalties(r) * coef}


def is_allowed(min_age: int, max_penalties: float, r: Row) -> bool:
    return bool(get_age(r) >= min_age and get_penalties(r) <= max_penalties)


def top_n(n: int) -> Callable[[list[Row]], list[Row]]:
    return lambda items: items[:n]


def team_total(rows: Iterable[Row]) -> dict[str, float]:
    # командна сума очок по країнах через reduce
    def add(acc: dict[str, float], r: Row) -> dict[str, float]:
        c = get_country(r)
        return {**acc, c: acc.get(c, 0.0) + r["final_points"]}

    return reduce(add, rows, {})


def rank(rows: list[Row]) -> list[Row]:
    # спочатку за name, потім за final_points (сортування стабільне)
    by_name = sorted(rows, key=itemgetter("name"))
    return sorted(by_name, key=itemgetter("final_points"), reverse=True)


def clean_and_rank(
    src: Any,
    top: int = 3,
    coef: float = 1.0,
    min_age: int = 16,
    max_penalties: float = 5.0,
) -> list[Row]:
    from loaders import load_results

    return pipeline(
        src,
        load_results,
        mapf(normalize),
        mapf(partial(add_final, coef)),
        filt(partial(is_allowed, min_age, max_penalties)),
        list,
        rank,
        top_n(top),
    )
