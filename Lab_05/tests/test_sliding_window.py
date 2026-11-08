from itertools import count, islice

import pytest

from streams import moving_average, sliding_window, take


def test_windows_basic():
    assert list(sliding_window([1, 2, 3, 4], 3)) == [(1, 2, 3), (2, 3, 4)]


def test_window_sums():
    sums = list(map(sum, sliding_window(range(5), 2)))
    assert sums == [1, 3, 5, 7]


def test_k_bigger_than_length():
    assert list(sliding_window([1, 2], 5)) == []


def test_k_equals_length():
    assert list(sliding_window([1, 2, 3], 3)) == [(1, 2, 3)]


def test_k_one():
    assert list(sliding_window([1, 2, 3], 1)) == [(1,), (2,), (3,)]


def test_empty_source():
    assert list(sliding_window([], 3)) == []


def test_bad_k():
    with pytest.raises(ValueError):
        sliding_window([1, 2, 3], 0)
    with pytest.raises(ValueError):
        sliding_window([1, 2, 3], -2)


def test_window_on_infinite_stream():
    wins = take(3, sliding_window(count(1), 3))
    assert wins == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]


def test_moving_average_basic():
    assert list(moving_average([10, 20, 30, 40], 2)) == [15, 25, 35]


def test_moving_average_k3():
    assert list(moving_average([1, 2, 3, 4, 5], 3)) == pytest.approx([2, 3, 4])


def test_moving_average_short_source():
    assert list(moving_average([1, 2], 3)) == []


def test_moving_average_empty():
    assert list(moving_average([], 2)) == []


def test_moving_average_bad_k():
    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 0)


def test_moving_average_infinite():
    res = list(islice(moving_average(count(1), 3), 4))
    assert res == pytest.approx([2, 3, 4, 5])
