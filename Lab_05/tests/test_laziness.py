from collections.abc import Iterator
from itertools import count

from streams import (
    drop,
    first_exceeding,
    moving_average,
    sliding_window,
    take,
)


def counting_source(log: list[int]) -> Iterator[int]:
    """Нескінченний потік, який записує, скільки елементів з нього взяли."""
    for i in count(1):
        log.append(i)
        yield i


def test_take_is_lazy():
    log: list[int] = []
    assert take(4, counting_source(log)) == [1, 2, 3, 4]
    assert len(log) == 4


def test_drop_is_lazy():
    log: list[int] = []
    rest = drop(5, counting_source(log))
    assert len(log) == 5  # пропустили рівно 5
    assert next(rest) == 6
    assert len(log) == 6


def test_sliding_window_is_lazy():
    log: list[int] = []
    wins = sliding_window(counting_source(log), 3)
    assert len(log) == 0  # поки ніхто не просив - нічого не читали
    next(wins)
    assert len(log) == 3
    next(wins)
    assert len(log) == 4


def test_moving_average_is_lazy():
    log: list[int] = []
    # 5 середніх при k=3 потребують 3 + 4 = 7 елементів
    res = take(5, moving_average(counting_source(log), 3))
    assert len(res) == 5
    assert len(log) == 7


def test_first_exceeding_stops_early():
    log: list[int] = []
    # середні: 2, 3, 4, 5, ... перше > 3.5 це 4 (третє середнє)
    value = first_exceeding(moving_average(counting_source(log), 3), 3.5)
    assert value == 4
    assert len(log) == 5
