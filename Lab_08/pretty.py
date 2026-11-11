from __future__ import annotations

from collections.abc import Sequence
from typing import assert_never

from evaluator import history
from model import Command, Delete, Move, ObjectState, Rotate, Scale


def render_command(cmd: Command) -> str:
    match cmd:
        case Move(dx=dx, dy=dy):
            return f"move({dx:g}, {dy:g})"
        case Rotate(angle=a):
            return f"rotate({a:g}°)"
        case Scale(factor=f):
            return f"scale(×{f:g})"
        case Delete():
            return "delete()"
        case unreachable:
            assert_never(unreachable)


def render_state(state: ObjectState) -> str:
    if state.deleted:
        return "<deleted>"
    return (
        f"Object(x={state.x:g}, y={state.y:g}, "
        f"angle={state.angle:g}°, scale={state.scale:g})"
    )


def render_log(commands: Sequence[Command], state: ObjectState | None = None) -> str:
    states = history(commands, state)
    lines = [
        f"{i}. {render_command(c)} -> {render_state(s)}"
        for i, (c, s) in enumerate(zip(commands, states[1:]), start=1)
    ]
    return "\n".join([f"start -> {render_state(states[0])}", *lines])
