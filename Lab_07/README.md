# Лабораторна робота №7. functools та operator

## Варіант 5. Результати спортивних змагань

Дані про спортсменів (`name`, `country`, `points`, `penalties`, `age`) обробляються конвеєром у функціональному стилі: завантаження, очищення, обчислення `final_points`, фільтр допущених, сортування і Top-N. Явних циклів майже немає, вхідні дані не змінюються.

## Конвеєр (`core.py`)

- `pipeline(value, *funcs)` — пропускає значення через функції по черзі за допомогою `reduce`.
- `mapf(fn)` і `filt(pred)` — обгортки над `map` і `filter` через `partial`.
- `normalize` — прибирає пробіли (`methodcaller("strip")`), робить `title`, приводить типи. Поля беремо через `itemgetter`.
- `add_final(coef, r)` — рахує `final_points = points - penalties * coef`. Коефіцієнт штрафу фіксуємо через `partial`.
- `is_allowed(min_age, max_penalties, r)` — допуск за віком і штрафами, параметри теж через `partial`.
- `team_total` — командна сума очок по країнах через `reduce` (нові словники, без мутації).
- `rank` — сортування за `final_points` ↓ та `name` ↑: спочатку сортуємо за `name`, потім за `final_points` з `reverse=True` (сортування стабільне).
- `clean_and_rank(src, top=3)` — збирає весь конвеєр і повертає Top-N.

## Поліморфне завантаження (`loaders.py`)

`load_results` — `@singledispatch` з реалізаціями для `str`, `Path`, відкритого текстового файлу (`io.TextIOBase`) і `list`. Для рядка: якщо починається з `[` — це JSON, інакше — шлях. Для файлів за розширенням вибирається JSON або CSV (`csv.DictReader`). Для інших типів кидається `TypeError`, для списку не зі словників — `ValueError`.

## Порівняння (`models.py`)

Клас `Athlete` з `@total_ordering`: порядок за `final_points`, потім `points`, потім `name`. Реалізовано `__eq__` і `__lt__`, для чужих типів повертається `NotImplemented`, решту операторів додає декоратор.

## Структура

```text
Lab_07/
├── README.md
├── ASSIGNMENT.md
├── core.py
├── loaders.py
├── models.py
├── main.py
├── sample_data.json
├── sample_data.csv
├── report/
├── tests/
│   ├── __init__.py
│   └── test_lab07.py
├── mypy.ini
├── pyproject.toml
└── requirements.txt
```

## Запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

pytest -q
python main.py
mypy .
black .
ruff check .
```

## Висновок

`partial` дозволяє зафіксувати параметри (коефіцієнт штрафу, мінімальний вік) і не писати lambda у конвеєрі, `reduce` дає універсальну згортку, `operator` робить код коротшим за lambda. `singledispatch` дає один інтерфейс для різних джерел даних, а `total_ordering` економить код у порівняннях. Обмеження: `singledispatch` дивиться лише на тип першого аргументу, а `reduce` без початкового значення ламається на порожніх даних.
