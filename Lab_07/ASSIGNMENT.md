# Завдання. Лабораторна робота №7 — functools та operator
Варіант 5. Результати спортивних змагань: спортсмени з полями `name`, `country`, `points`, `penalties`, `age`. Обчислити `final_points`, відфільтрувати допущених і сформувати рейтинг. `reduce` використати для командної суми, `load_results` — поліморфний завантажувач, `Athlete` — клас з `total_ordering`.

# Вимоги

* Реалізувати `pipeline(value, *funcs)` через `functools.reduce`.
* Використати `functools.partial` щонайменше для двох етапів конвеєра.
* Використати щонайменше два засоби `operator`: `itemgetter`, `attrgetter`, `methodcaller`.
* Реалізувати `load_results` через `@singledispatch` для `str`, `Path`, відкритого файлу та готового списку.
* Підтримати JSON і CSV для файлових джерел.
* Створити клас з `@total_ordering` (`__eq__`, `__lt__`, `NotImplemented` для чужих типів).
* Багатокритеріальне сортування і Top-N.
* pytest-тести для pipeline, partial, singledispatch, operator і всіх операторів порівняння.
* mypy, black, ruff без зауважень, README.md.

# Критерії оцінювання
Коректність, функціональний стиль, використання `functools`/`operator`, стиль і тестування.
