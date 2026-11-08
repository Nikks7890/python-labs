# Лабораторна робота №5. Ліниві обчислення: генератори та itertools

## Варіант 5. Рухоме середнє температур

Потік температурних вимірювань обробляється лінивим конвеєром: вікна, рухоме середнє, пошук значень, що перевищують поріг. Значення обчислюються лише в міру запиту, нескінченні потоки завжди обмежуються через `take`, `islice` або `takewhile`.

## Ліниві будівельні блоки (`streams.py`)

- Потоки: `fib_stream()`, `naturals()` і `temperature_stream(seed)` — нескінченні генератори з `yield` / `yield from`. Параметр `seed` робить потік температур відтворюваним у тестах.
- `take(n, it)` повертає перші n елементів, `drop(n, it)` пропускає перші n через `next(islice(it, n, n), None)`. Для `n < 0` кидають `ValueError`.
- `sliding_window(it, k)` — ковзні вікна на основі `deque(maxlen=k)` без матеріалізації потоку. Для `k <= 0` помилка виникає одразу при виклику, а якщо елементів менше за `k`, вікон просто немає.
- `moving_average(it, k)` — рухоме середнє поверх `sliding_window` (генераторний вираз).

## Пошук перевищень порога (`streams.py`)

- `first_exceeding` знаходить перше значення вище порога через `dropwhile`.
- `take_exceeding` бере перші n таких значень.
- `overheat_run` повертає першу неперервну ділянку перегріву: `dropwhile` пропускає все до перевищення, `takewhile` зупиняється, коли значення падає до порога.
- Обгортки `prefix_sums`, `prefix_products`, `prefix_max` (`accumulate`), `take_while`, `drop_while`.

## Структура

```text
Lab_05/
├── README.md
├── ASSIGNMENT.md
├── streams.py
├── main.py
├── report/
├── tests/
│   ├── __init__.py
│   ├── test_accumulate.py
│   ├── test_fib_stream.py
│   ├── test_laziness.py
│   ├── test_main.py
│   ├── test_sliding_window.py
│   ├── test_take_drop.py
│   └── test_temperature.py
├── mypy.ini
├── pyproject.toml
└── requirements.txt
```

## Запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

pytest -q --durations=5
python main.py
mypy .
black .
ruff check .
```

## Висновок про ліниві обчислення

Переваги: пам'ять не залежить від розміру потоку (зберігається лише вікно з k елементів), нескінченні джерела обробляються без додаткових зусиль, а обчислення зупиняється, щойно знайдено потрібне значення. Лінивість перевіряє `tests/test_laziness.py`: наприклад, для 5 середніх при k=3 з джерела зчитується рівно 7 елементів, а `first_exceeding` не читає потік далі першого збігу.

Накладні витрати: генератори мають витрати на кожен `next()`, а результат не можна пройти двічі — після вичерпання потрібно створювати потік заново (або використовувати `tee` з буфером).

