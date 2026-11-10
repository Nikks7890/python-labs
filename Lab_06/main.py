"""Демо до лабораторної роботи 6 (варіант 5: обмеження частоти викликів)."""

from closures import make_counter, make_logger
from decorators import RateLimitError, rate_limit, timed


def main() -> None:
    log = make_logger("INFO")

    # 1. Замикання-лічильник
    counter = make_counter(10)
    log(f"Лічильник: {counter()}, {counter()}, {counter()}")

    # 2. rate_limit з фальшивим годинником (без реального sleep)
    now = 0.0

    def fake_clock() -> float:
        return now

    @timed("api", unit="us", logger=log)
    @rate_limit(max_calls=3, period=5.0, clock=fake_clock)
    def get_data(n: int) -> int:
        """Повертає подвоєне число."""
        return n * 2

    log("Ліміт: 3 виклики за 5 секунд")
    for t in [0.0, 1.0, 2.0, 3.0, 6.0]:
        now = t
        try:
            res = get_data(int(t))
            log(f"t={t}: результат {res}")
        except RateLimitError as e:
            log(f"t={t}: відмова ({e})")

    # 3. Метадані збереглись завдяки functools.wraps
    log(f"Ім'я функції: {get_data.__name__}, doc: {get_data.__doc__}")


if __name__ == "__main__":
    main()
