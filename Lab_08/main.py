import json
from pathlib import Path

from evaluator import count_by_kind, run
from model import (
    Command,
    Delete,
    EditorError,
    Move,
    ObjectState,
    Rotate,
    Scale,
    parse_command,
)
from pretty import render_log, render_state


def main() -> None:
    program: list[Command] = [
        Move(10, 5),
        Rotate(90),
        Scale(2),
        Move(-4, 2.5),
        Rotate(300),
    ]
    start = ObjectState()

    print("Журнал виконання:")
    print(render_log(program, start))
    print("\nПочатковий стан не змінився:", render_state(start))
    print("Статистика команд:", count_by_kind(program))

    # команди з JSON -> ADT через match за словником
    raw = json.loads(Path("sample_commands.json").read_text(encoding="utf-8"))
    commands = [parse_command(r) for r in raw]
    print("\nПрограма з JSON:")
    print(render_log(commands))

    # некоректні дії
    bad_programs: list[list[Command]] = [[Scale(0)], [Delete(), Move(1, 1)]]
    for bad in bad_programs:
        try:
            run(bad)
        except EditorError as e:
            print(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
