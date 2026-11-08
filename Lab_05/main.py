"""Демо до лабораторної роботи 5 (варіант 5: рухоме середнє температур)."""

from itertools import islice

from streams import (
    drop,
    fib_stream,
    first_exceeding,
    moving_average,
    overheat_run,
    prefix_sums,
    sliding_window,
    take,
    take_exceeding,
    temperature_stream,
)


def main() -> None:
    print("Лабораторна робота 5, варіант 5: рухоме середнє температур\n")

    # 1. Базові речі: Фібоначчі, take, drop
    print("Перші 10 чисел Фібоначчі:", take(10, fib_stream()))
    print("Пропустили 5, взяли 8:   ", take(8, drop(5, fib_stream())))

    # 2. Потік температур (з seed, щоб результат повторювався)
    temps = take(10, temperature_stream(seed=42))
    print("\nПерші 10 температур:", temps)

    # 3. Ковзні вікна
    print("Вікна по 3:", list(islice(sliding_window(temps, 3), 3)), "...")

    # 4. Рухоме середнє
    k = 3
    averages = take(8, moving_average(temperature_stream(seed=42), k))
    print(f"Рухоме середнє (k={k}):", [round(a, 2) for a in averages])

    # 5. Пошук перевищення порога
    threshold = 21.0
    first = first_exceeding(moving_average(temperature_stream(seed=42), k), threshold)
    print(f"\nПерше середнє вище {threshold}:", round(first, 2) if first else None)

    top = take_exceeding(moving_average(temperature_stream(seed=42), k), threshold, 5)
    print(f"Перші 5 середніх вище {threshold}:", [round(x, 2) for x in top])

    # 6. Неперервна ділянка перегріву (на фіксованих даних)
    readings = [18, 19, 21, 24, 27, 30, 26, 22, 19]
    avgs = moving_average(readings, 3)
    print("\nДані:", readings)
    run = [round(x, 2) for x in overheat_run(avgs, 25)]
    print("Ділянка, де середнє > 25:", run)

    # 7. Префіксні суми (accumulate)
    print("Префіксні суми:", list(prefix_sums(readings)))


if __name__ == "__main__":
    main()
