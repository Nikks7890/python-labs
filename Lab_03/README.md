# Лабораторна робота №3. Нездатні до змін структури даних (immutability) у Python

## Варіант 5. Банківський рахунок

Предметна модель (рахунок і транзакції з прапорцями та метаданими) переведена на незмінні структури. Усі зміни стану виконуються як pure updates: функції повертають нові об'єкти й не змінюють вхідні.

## Незмінна модель (`model.py`)

- `Account`, `Transaction` — `@dataclass(frozen=True, slots=True)`.
- Історія транзакцій — `tuple`; прапорці (`flags`) — `frozenset`.
- Метадані — `MappingProxyType` над копією словника (у методі `with_meta`).
- Для `Account` реалізовано кастомний `__hash__` (перетворює `meta` в `tuple`) та `__deepcopy__` (для коректної роботи з `copy.deepcopy`), тому всі сутності хешовані й підходять як ключі `dict` та елементи `set`.

## Pure-оновлення (`core.py`)

`deposit`, `withdraw`, `block_account`, `add_flag` (через `dataclasses.replace`, операції `frozenset` і конкатенацію `tuple`); розрахунки `calculate_total_inflow`, `calculate_total_outflow`; глибоке заморожування `freeze`; функції-хелпери `source`.

## Структура

```text
lab03/
├── README.md
├── lab03/
│   ├── __init__.py
│   ├── model.py
│   └── core.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_immutability.py
│   └── test_performance.py
├── mypy.ini
├── pyproject.toml
└── requirements.txt
```
## Запуск
```bash
pip install -r requirements.txt
pytest -q --durations=5
mypy .
black --check .
ruff check .
```
## Висновок про незмінність
Переваги: немає прихованих змін стану, тести прості (порівняння з еталонним екземпляром), сутності хешовані, а тому працюють як ключі; frozen-класи та MappingProxyType захищають дані на рівні мови.

Накладні витрати: кожне оновлення створює новий об'єкт. У мікробенчмарку tests/test_performance.py (5000 ланцюжків, по три оновлення на кожну) мутабельний варіант виконався за ≈ 0.008 с, незмінний — за ≈ 0.115 с, тобто приблизно в 14 разів повільніше. В абсолютних числах це ≈ 23 мкс на ланцюжок оновлень, що для бізнес-логіки несуттєво. Час усього набору тестів при цьому лишається близько 2–3 с (pytest --durations=5).
