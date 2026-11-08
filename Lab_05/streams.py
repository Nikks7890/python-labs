"""Лабораторна робота 5. Ліниві обчислення: генератори та itertools.

Варіант 5: рухоме середнє температур.
Усі значення обчислюються лише тоді, коли їх запитали.
"""

from __future__ import annotations

import operator
import random
from collections import deque
from collections.abc import Callable, Iterable, Iterator
from itertools import accumulate, count, dropwhile, islice, takewhile
from typing import TypeVar

T = TypeVar("T")


def fib_stream() -> Iterator[int]:
    """Нескінченний потік чисел Фібоначчі: 0, 1, 1, 2, 3, 5, ..."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def naturals(start: int = 1) -> Iterator[int]:
    """Нескінченний потік натуральних чисел."""
    yield from count(start)


def temperature_stream(
    seed: int | None = None, base: float = 20.0, spread: float = 5.0
) -> Iterator[float]:
    """Нескінченний потік температурних вимірювань (імітація датчика).

    seed потрібен, щоб у тестах результат був однаковий щоразу.
    """
    rng = random.Random(seed)
    while True:
        yield round(rng.gauss(base, spread), 1)



def take(n: int, it: Iterable[T]) -> list[T]:
    """Взяти перші n елементів (повертає список)."""
    if n < 0:
        raise ValueError("n не може бути від'ємним")
    return list(islice(it, n))


def drop(n: int, it: Iterable[T]) -> Iterator[T]:
    """Пропустити перші n елементів і повернути ітератор з рештою."""
    if n < 0:
        raise ValueError("n не може бути від'ємним")
    it = iter(it)
    next(islice(it, n, n), None)  # "промотуємо" n елементів
    return it


def _windows(it: Iterable[T], k: int) -> Iterator[tuple[T, ...]]:
    it = iter(it)
    dq: deque[T] = deque(maxlen=k)

    # наповнюємо перше вікно
    for _ in range(k):
        try:
            dq.append(next(it))
        except StopIteration:
            return  # елементів менше за k - вікон немає

    yield tuple(dq)

    for x in it:
        dq.append(x)  # найстаріший елемент виштовхується сам
        yield tuple(dq)


def sliding_window(it: Iterable[T], k: int) -> Iterator[tuple[T, ...]]:
    """Ліниві ковзні вікна розміру k.

    Перевірку k робимо одразу, а не при першому next(),
    щоб помилка з'являлась там, де її зробили.
    """
    if k <= 0:
        raise ValueError("розмір вікна k має бути додатним")
    return _windows(it, k)


def moving_average(it: Iterable[float], k: int) -> Iterator[float]:
    """Рухоме середнє з вікном k (ліниво).

    sliding_window сам перевіряє k, тому помилка з'явиться одразу.
    """
    windows = sliding_window(it, k)
    return (sum(w) / k for w in windows)


def exceeding(values: Iterable[float], threshold: float) -> Iterator[float]:
    """Усі значення, що строго перевищують поріг."""
    return (x for x in values if x > threshold)


def take_exceeding(values: Iterable[float], threshold: float, n: int) -> list[float]:
    """Перші n значень, що перевищують поріг."""
    return take(n, exceeding(values, threshold))


def first_exceeding(values: Iterable[float], threshold: float) -> float | None:
    """Перше значення вище порога (або None, якщо потік закінчився)."""
    return next(dropwhile(lambda x: x <= threshold, values), None)


def overheat_run(values: Iterable[float], threshold: float) -> Iterator[float]:
    """Перша неперервна ділянка, де значення вище порога.

    dropwhile пропускає все до першого перевищення,
    takewhile зупиняється, коли значення знову падає до порога.
    """
    after_start = dropwhile(lambda x: x <= threshold, values)
    return takewhile(lambda x: x > threshold, after_start)


def prefix_sums(it: Iterable[float]) -> Iterator[float]:
    """Префіксні суми."""
    return accumulate(it)


def prefix_products(it: Iterable[float]) -> Iterator[float]:
    """Префіксні добутки."""
    return accumulate(it, operator.mul)


def prefix_max(it: Iterable[float]) -> Iterator[float]:
    """Максимум, накопичений від початку потоку."""
    return accumulate(it, max)


def take_while(pred: Callable[[T], bool], it: Iterable[T]) -> Iterator[T]:
    """Обгортка над itertools.takewhile."""
    return takewhile(pred, it)


def drop_while(pred: Callable[[T], bool], it: Iterable[T]) -> Iterator[T]:
    """Обгортка над itertools.dropwhile."""
    return dropwhile(pred, it)
