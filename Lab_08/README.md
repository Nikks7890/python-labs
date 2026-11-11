# Лабораторна робота №8. Алгебраїчні типи даних

## Варіант 5. Команди графічного редактора

Модель команд редактора як алгебраїчний тип даних: `Command = Move | Rotate | Scale | Delete`. Послідовність команд інтерпретується чистими функціями над незмінним станом `ObjectState`. Кожна команда повертає новий стан, вхідні дані не змінюються.

## Модель (`model.py`)

- `Move(dx, dy)`, `Rotate(angle)`, `Scale(factor)`, `Delete()` — `@dataclass(frozen=True)`, кожен має поле `kind` з типом `Literal[...]`.
- `Command: TypeAlias = Move | Rotate | Scale | Delete` — сума варіантів (sum type).
- `Kind = Literal["move", "rotate", "scale", "delete"]` — обмежений набір назв команд.
- `ObjectState(x, y, angle, scale, deleted)` — незмінний стан об'єкта.
- `HasKind` — `Protocol` зі структурним контрактом (властивість `kind`).
- `parse_command(data)` — розбір словника (JSON) у `Command` через mapping-патерни `match/case`.
- Помилки: `EditorError` → `InvalidCommand`, `ObjectDeleted`.

## Обчислення (`evaluator.py`)

- `apply(state, cmd)` — `match/case` для кожної команди; `assert_never` у гілці `case unreachable` змушує mypy перевіряти вичерпність. Кут по модулю 360, множник масштабу має бути більшим за 0, після `Delete` будь-яка команда дає `ObjectDeleted`.
- `run(commands, state)` — згортка через `reduce`.
- `history(commands, state)` — усі проміжні стани через `accumulate`.
- `run_raw(raw, state)` — виконання списку словників (наприклад, з JSON).
- `count_by_kind(items)` — статистика за видом команди (приймає будь-що, що відповідає `HasKind`).

## Відображення (`pretty.py`)

`render_command`, `render_state` та `render_log` (покроковий журнал виконання).

## Структура

```text
Lab_08/
├── README.md
├── ASSIGNMENT.md
├── model.py
├── evaluator.py
├── pretty.py
├── main.py
├── sample_commands.json
├── report/
├── tests/
│   ├── __init__.py
│   └── test_lab08.py
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

`match/case` разом із `Union`-псевдонімом дає чисту й читабельну інтерпретацію команд, а `assert_never` робить так, що додавання нового вузла без оновлення `apply` та `render_command` помітить `mypy --strict`. `Literal` обмежує набір назв команд, `Protocol` описує структурний контракт без успадкування, а `frozen=True` гарантує незмінність: кожна команда створює новий стан.
