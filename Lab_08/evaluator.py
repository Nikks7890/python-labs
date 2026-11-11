from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import replace
from functools import reduce
from itertools import accumulate
from typing import Any, assert_never

from model import (
    Command,
    Delete,
    HasKind,
    InvalidCommand,
    Kind,
    Move,
    ObjectDeleted,
    ObjectState,
    Rotate,
    Scale,
    parse_command,
)


def apply(state: ObjectState, cmd: Command) -> ObjectState:
    # чиста функція: повертає новий стан, старий не змінюється
    if state.deleted:
        raise ObjectDeleted(f"object is deleted, cannot apply {cmd.kind}")
    match cmd:
        case Move(dx=dx, dy=dy):
            return replace(state, x=state.x + dx, y=state.y + dy)
        case Rotate(angle=a):
            return replace(state, angle=(state.angle + a) % 360)
        case Scale(factor=f):
            if f <= 0:
                raise InvalidCommand(f"scale factor must be positive: {f}")
            return replace(state, scale=state.scale * f)
        case Delete():
            return replace(state, deleted=True)
        case unreachable:
            assert_never(unreachable)


def run(commands: Iterable[Command], state: ObjectState | None = None) -> ObjectState:
    # згортка всієї послідовності команд
    return reduce(apply, commands, state or ObjectState())


def history(
    commands: Iterable[Command], state: ObjectState | None = None
) -> list[ObjectState]:
    # усі проміжні стани, включно з початковим
    return list(accumulate(commands, apply, initial=state or ObjectState()))


def run_raw(
    raw: Iterable[Mapping[str, Any]], state: ObjectState | None = None
) -> ObjectState:
    return run(map(parse_command, raw), state)


def count_by_kind(items: Iterable[HasKind]) -> dict[Kind, int]:
    # статистика команд за видом
    def add(acc: dict[Kind, int], item: HasKind) -> dict[Kind, int]:
        return {**acc, item.kind: acc.get(item.kind, 0) + 1}

    return reduce(add, items, {})
