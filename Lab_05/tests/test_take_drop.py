from itertools import count, islice

import pytest

from streams import drop, naturals, take


def test_take_drop_on_count():
    xs = count(1)
    assert take(5, xs) == [1, 2, 3, 4, 5]
    # xs вже просунутий до 6
    assert take(3, xs) == [6, 7, 8]


def test_drop_then_take():
    xs = drop(10, count(0))
    assert list(islice(xs, 3)) == [10, 11, 12]


def test_take_zero():
    assert take(0, count()) == []


def test_take_more_than_length():
    assert take(10, [1, 2, 3]) == [1, 2, 3]


def test_drop_more_than_length():
    assert list(drop(10, [1, 2, 3])) == []


def test_drop_zero():
    assert list(drop(0, [1, 2, 3])) == [1, 2, 3]


def test_empty_source():
    assert take(3, []) == []
    assert list(drop(3, [])) == []


def test_negative_n():
    with pytest.raises(ValueError):
        take(-1, [1, 2, 3])
    with pytest.raises(ValueError):
        drop(-1, [1, 2, 3])


def test_naturals():
    assert take(5, naturals()) == [1, 2, 3, 4, 5]
    assert take(3, naturals(10)) == [10, 11, 12]
