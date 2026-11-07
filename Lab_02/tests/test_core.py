import pytest

from core import (
    Record,
    compose,
    juxt,
    pipe,
    reduce_stats,
    with_best_avg,
    with_score,
)
@pytest.fixture
def sample() -> list[Record]:
    return [
        Record(id=1, name="ivan", category="Pro", results=[9.5, 9.8, 10.0]),
        Record(id=2, name="olena", category="Amateur", results=[8.0, 8.5, 8.2]),
    ]


def test_transformation_no_mutation(sample: list[Record]) -> None:
    res = list(with_best_avg()(sample))
    assert "best" not in sample[0]
    assert res[0]["best"] == 10.0


def test_reduce_empty() -> None:
    assert reduce_stats([]) == {"count": 0.0, "sum_points": 0.0, "avg_points": 0.0}


def test_reduce_stats() -> None:
    recs = [Record(id=1, score=10.0), Record(id=2, score=20.0)]
    stats = reduce_stats(recs)
    assert stats["count"] == 2
    assert stats["sum_points"] == 30.0
    assert stats["avg_points"] == 15.0


def test_compose() -> None:
    f = compose(lambda x: x + 1, lambda x: x * 2)  # type: ignore
    assert f(5) == 11


def test_pipe() -> None:
    f = pipe(lambda x: x + 1, lambda x: x * 2)  # type: ignore
    assert f(5) == 12


def test_juxt() -> None:
    f = juxt(lambda x: x + 1, lambda x: x * 2)  # type: ignore
    assert f(5) == (6, 10)


def test_with_score_formula() -> None:
    rec = Record(id=1, best=10.0, avg=5.0)
    out = list(with_score()([rec]))
    assert out[0]["score"] == pytest.approx(8.0)  # 10*0.6 + 5*0.4
