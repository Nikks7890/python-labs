"""Тести для чисел Фібоначчі та кешу."""

from algorithms import fib, fib_iter


def test_fib_small() -> None:
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    got = [fib(i) for i in range(10)]
    assert got == expected


def test_fib_iter_matches() -> None:
    for n in range(50):
        assert fib(n) == fib_iter(n)


def test_cache_clear() -> None:
    fib.cache_clear()
    assert fib(0) == 0
