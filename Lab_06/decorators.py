"""Параметризовані декоратори: timed та rate_limit."""

import functools
import time
from collections.abc import Callable
from typing import Literal, ParamSpec, TypeVar

from closures import make_window

P = ParamSpec("P")
R = TypeVar("R")


class RateLimitError(Exception):
    """Виникає, коли перевищено ліміт викликів."""


def timed(
    label: str | None = None,
    *,
    unit: Literal["s", "ms", "us"] = "ms",
    logger: Callable[[str], None] = print,
    clock: Callable[[], float] = time.perf_counter,  # у тестах підміняємо
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Вимірює час виконання функції і пише його в logger."""
    factor = {"s": 1.0, "ms": 1e3, "us": 1e6}[unit]

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        name = label or func.__name__

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            t0 = clock()
            try:
                return func(*args, **kwargs)
            finally:
                # finally, щоб час записався навіть коли була помилка
                dt = (clock() - t0) * factor
                logger(f"[timed] {name} took {dt:.3f} {unit}")

        return wrapper

    return decorator


def rate_limit(
    max_calls: int,
    period: float,
    *,
    clock: Callable[[], float] = time.monotonic,  # у тестах підміняємо
    logger: Callable[[str], None] = lambda _: None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Дозволяє не більше max_calls викликів за period секунд.

    Якщо ліміт перевищено, кидає RateLimitError (функція не виконується).
    """
    if max_calls < 1:
        raise ValueError("max_calls має бути не менше 1")
    if period <= 0:
        raise ValueError("period має бути додатним")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        allowed = make_window(max_calls, period, clock)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if not allowed():
                logger(f"[rate_limit] {func.__name__} заблоковано")
                raise RateLimitError(
                    f"Ліміт перевищено (макс. {max_calls} за {period} с)"
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator
