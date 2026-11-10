"""Замикання для лабораторної роботи 6 (варіант 5: обмеження частоти викликів)."""

from collections import deque
from collections.abc import Callable


def make_counter(start: int = 0) -> Callable[[], int]:
    """Лічильник викликів: пам'ятає значення між викликами."""
    value = start

    def inc() -> int:
        nonlocal value  # змінюємо змінну із зовнішньої функції
        value += 1
        return value

    return inc


def make_logger(prefix: str) -> Callable[[str], None]:
    """Логер, який додає префікс до кожного повідомлення."""

    def log(msg: str) -> None:
        print(f"[{prefix}] {msg}")

    return log


def make_window(
    max_calls: int, period: float, clock: Callable[[], float]
) -> Callable[[], bool]:
    """Замикання з часовим вікном.

    Повертає функцію, яка кожного разу відповідає, чи можна зараз
    зробити виклик (True) або ліміт вже вичерпано (False).
    Час викликів зберігається в черзі всередині замикання.
    """
    calls: deque[float] = deque()

    def try_call() -> bool:
        now = clock()
        # прибираємо виклики, які вже вийшли за межі вікна
        while calls and now - calls[0] >= period:
            calls.popleft()
        if len(calls) < max_calls:
            calls.append(now)
            return True
        return False

    return try_call
