from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol, TypeAlias

Kind: TypeAlias = Literal["move", "rotate", "scale", "delete"]


class EditorError(ValueError):
    """Базова помилка графічного редактора."""


class InvalidCommand(EditorError):
    pass


class ObjectDeleted(EditorError):
    pass


@dataclass(frozen=True)
class Move:
    dx: float
    dy: float
    kind: Literal["move"] = field(default="move", init=False)


@dataclass(frozen=True)
class Rotate:
    angle: float
    kind: Literal["rotate"] = field(default="rotate", init=False)


@dataclass(frozen=True)
class Scale:
    factor: float
    kind: Literal["scale"] = field(default="scale", init=False)


@dataclass(frozen=True)
class Delete:
    kind: Literal["delete"] = field(default="delete", init=False)


Command: TypeAlias = Move | Rotate | Scale | Delete


@dataclass(frozen=True)
class ObjectState:
    x: float = 0.0
    y: float = 0.0
    angle: float = 0.0
    scale: float = 1.0
    deleted: bool = False


class HasKind(Protocol):
    # структурний контракт: будь-який об'єкт з «читабельним» kind
    @property
    def kind(self) -> Kind: ...


def parse_command(data: Mapping[str, Any]) -> Command:
    # розбір словника (наприклад, з JSON) через mapping-патерни
    match data:
        case {"kind": "move", "dx": dx, "dy": dy}:
            return Move(float(dx), float(dy))
        case {"kind": "rotate", "angle": angle}:
            return Rotate(float(angle))
        case {"kind": "scale", "factor": factor}:
            return Scale(float(factor))
        case {"kind": "delete"}:
            return Delete()
        case _:
            raise InvalidCommand(f"Unknown command: {dict(data)!r}")
