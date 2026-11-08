from itertools import islice

from streams import drop, fib_stream, take


def test_first_10():
    assert list(islice(fib_stream(), 10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_take_from_fib():
    assert take(5, fib_stream()) == [0, 1, 1, 2, 3]


def test_drop_then_take_fib():
    assert take(8, drop(5, fib_stream())) == [5, 8, 13, 21, 34, 55, 89, 144]


def test_two_streams_are_independent():
    a = fib_stream()
    b = fib_stream()
    assert take(3, a) == [0, 1, 1]
    assert take(3, b) == [0, 1, 1]
