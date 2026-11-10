import io
import json
from functools import partial, reduce
from operator import attrgetter, itemgetter, mul
from pathlib import Path

import pytest

from core import (
    add_final,
    clean_and_rank,
    is_allowed,
    pipeline,
    rank,
    team_total,
)
from loaders import load_results
from models import Athlete

RAW = [
    {
        "name": "  anna smith ",
        "country": "usa",
        "points": "95",
        "penalties": "3",
        "age": "22",
    },
    {
        "name": "oleh k",
        "country": "ukraine",
        "points": "92.5",
        "penalties": "1.5",
        "age": "24",
    },
    {
        "name": "tom young",
        "country": "usa",
        "points": "97",
        "penalties": "0.5",
        "age": "15",
    },
    {
        "name": "mia lopez",
        "country": "spain",
        "points": "90",
        "penalties": "7",
        "age": "20",
    },
]
JSON_STR = json.dumps(RAW)


# pipeline
def inc(x: int) -> int:
    return x + 1


def dbl(x: int) -> int:
    return x * 2


def test_pipeline_order() -> None:
    assert pipeline(3, inc, dbl, inc) == 9


def test_pipeline_no_funcs() -> None:
    assert pipeline(5) == 5


def test_reduce_initial() -> None:
    assert reduce(mul, [], 1) == 1


# partial
def test_partial_add_final() -> None:
    f = partial(add_final, 2.0)
    r = f({"points": 10.0, "penalties": 1.0})
    assert r["final_points"] == 8.0


def test_partial_is_allowed() -> None:
    check = partial(is_allowed, 18, 5.0)
    assert check({"age": 20, "penalties": 1.0})
    assert not check({"age": 17, "penalties": 1.0})
    assert not check({"age": 20, "penalties": 6.0})


def test_add_final_no_mutation() -> None:
    r = {"points": 10.0, "penalties": 1.0}
    add_final(1.0, r)
    assert "final_points" not in r


# singledispatch
def test_load_json_str() -> None:
    assert len(load_results(JSON_STR)) == 4


def test_load_str_path(tmp_path: Path) -> None:
    p = tmp_path / "a.json"
    p.write_text(JSON_STR, encoding="utf-8")
    assert load_results(str(p)) == load_results(JSON_STR)


def test_load_path(tmp_path: Path) -> None:
    p = tmp_path / "a.json"
    p.write_text(JSON_STR, encoding="utf-8")
    assert load_results(p) == RAW


def test_load_file(tmp_path: Path) -> None:
    p = tmp_path / "a.json"
    p.write_text(JSON_STR, encoding="utf-8")
    with open(p, encoding="utf-8") as f:
        assert load_results(f) == RAW


def test_load_list() -> None:
    assert load_results(RAW) == RAW


def test_load_list_bad() -> None:
    with pytest.raises(ValueError):
        load_results([1, 2, 3])


def test_load_bad_type() -> None:
    with pytest.raises(TypeError):
        load_results(123)


CSV_TEXT = "name,country,points,penalties,age\nanna,usa,95,3,22\nbob,spain,80,1,19\n"


def test_load_csv_path(tmp_path: Path) -> None:
    p = tmp_path / "a.csv"
    p.write_text(CSV_TEXT, encoding="utf-8")
    assert load_results(p)[0]["name"] == "anna"


def test_load_csv_str_path(tmp_path: Path) -> None:
    p = tmp_path / "a.csv"
    p.write_text(CSV_TEXT, encoding="utf-8")
    assert load_results(str(p)) == load_results(p)


def test_load_csv_file(tmp_path: Path) -> None:
    p = tmp_path / "a.csv"
    p.write_text(CSV_TEXT, encoding="utf-8")
    with open(p, encoding="utf-8", newline="") as f:
        assert len(load_results(f)) == 2


def test_dispatch_textio() -> None:
    assert isinstance(io.StringIO(JSON_STR), io.TextIOBase)
    assert load_results(io.StringIO(JSON_STR)) == RAW


# operator
def test_itemgetter_many_keys() -> None:
    rows = [{"a": 1, "b": 2}, {"a": 1, "b": 1}, {"a": 0, "b": 9}]
    res = sorted(rows, key=itemgetter("a", "b"))
    assert res == [{"a": 0, "b": 9}, {"a": 1, "b": 1}, {"a": 1, "b": 2}]


def test_attrgetter() -> None:
    items = [Athlete("B", "X", 5, 0, 20), Athlete("A", "X", 5, 0, 18)]
    assert [a.name for a in sorted(items, key=attrgetter("age"))] == ["A", "B"]


def test_rank_ties_by_name() -> None:
    rows = [
        {"name": "B", "final_points": 10.0},
        {"name": "A", "final_points": 10.0},
        {"name": "C", "final_points": 20.0},
    ]
    assert [r["name"] for r in rank(rows)] == ["C", "A", "B"]


# clean_and_rank
def test_clean_and_rank() -> None:
    res = clean_and_rank(JSON_STR, top=5)
    names = [r["name"] for r in res]
    assert names == ["Anna Smith", "Oleh K"]  # Tom молодий, Mia багато штрафів
    assert res[0]["final_points"] == 92.0


def test_clean_and_rank_top() -> None:
    assert len(clean_and_rank(JSON_STR, top=1)) == 1


def test_clean_and_rank_empty() -> None:
    assert clean_and_rank([]) == []


def test_team_total() -> None:
    rows = [
        {"country": "Usa", "final_points": 10.0},
        {"country": "Usa", "final_points": 5.0},
        {"country": "Spain", "final_points": 1.0},
    ]
    assert team_total(rows) == {"Usa": 15.0, "Spain": 1.0}
    assert team_total([]) == {}


# total_ordering
def make(fp: float, pts: float = 100.0, name: str = "A") -> Athlete:
    return Athlete(name, "X", pts, pts - fp, 20)


def test_lt_gt() -> None:
    assert make(10) < make(20)
    assert make(20) > make(10)


def test_le_ge() -> None:
    assert make(10) <= make(10)
    assert make(10) >= make(10)
    assert make(10) <= make(20)
    assert make(20) >= make(10)


def test_eq_ne() -> None:
    assert make(10) == make(10)
    assert make(10) != make(11)


def test_tie_break_name() -> None:
    assert make(10, name="A") < make(10, name="B")


def test_sorted_athletes() -> None:
    items = [make(30), make(10), make(20)]
    assert [a.final_points for a in sorted(items)] == [10, 20, 30]


def test_not_implemented() -> None:
    a = make(10)
    assert a.__eq__(5) is NotImplemented
    assert a.__lt__(5) is NotImplemented
    with pytest.raises(TypeError):
        _ = a < 5  # type: ignore[operator]
