import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from evaluator import apply, count_by_kind, history, run, run_raw
from model import (
    Command,
    Delete,
    EditorError,
    HasKind,
    InvalidCommand,
    Move,
    ObjectDeleted,
    ObjectState,
    Rotate,
    Scale,
    parse_command,
)
from pretty import render_command, render_log, render_state


# ADT та незмінність
def test_nodes_are_frozen() -> None:
    m = Move(1, 2)
    with pytest.raises(FrozenInstanceError):
        setattr(m, "dx", 5)  # noqa: B010


def test_kind_literals() -> None:
    assert Move(1, 1).kind == "move"
    assert Rotate(10).kind == "rotate"
    assert Scale(2).kind == "scale"
    assert Delete().kind == "delete"


def test_nodes_equality() -> None:
    assert Move(1, 2) == Move(1, 2)
    assert Move(1, 2) != Move(2, 1)
    assert hash(Move(1, 2)) == hash(Move(1, 2))


def test_default_state() -> None:
    s = ObjectState()
    assert (s.x, s.y, s.angle, s.scale, s.deleted) == (0.0, 0.0, 0.0, 1.0, False)


# apply: match/case для кожної команди
def test_apply_move() -> None:
    assert apply(ObjectState(), Move(3, -2)) == ObjectState(x=3, y=-2)


def test_apply_rotate_wraps() -> None:
    s = apply(ObjectState(angle=350), Rotate(20))
    assert s.angle == 10


def test_apply_rotate_negative() -> None:
    assert apply(ObjectState(), Rotate(-90)).angle == 270


def test_apply_scale() -> None:
    assert apply(ObjectState(scale=2), Scale(1.5)).scale == 3


def test_apply_delete() -> None:
    assert apply(ObjectState(), Delete()).deleted is True


def test_apply_no_mutation() -> None:
    s = ObjectState(x=1)
    apply(s, Move(5, 5))
    assert s == ObjectState(x=1)


@pytest.mark.parametrize("factor", [0, -1, -0.5])
def test_scale_invalid(factor: float) -> None:
    with pytest.raises(InvalidCommand):
        apply(ObjectState(), Scale(factor))


def test_command_after_delete() -> None:
    deleted = apply(ObjectState(), Delete())
    for cmd in (Move(1, 1), Rotate(1), Scale(2), Delete()):
        with pytest.raises(ObjectDeleted):
            apply(deleted, cmd)


def test_errors_hierarchy() -> None:
    assert issubclass(InvalidCommand, EditorError)
    assert issubclass(ObjectDeleted, ValueError)


# run / history
PROGRAM: list[Command] = [Move(10, 5), Rotate(90), Scale(2), Move(-4, 2.5)]


def test_run_sequence() -> None:
    assert run(PROGRAM) == ObjectState(x=6, y=7.5, angle=90, scale=2)


def test_run_empty() -> None:
    assert run([]) == ObjectState()


def test_run_custom_start() -> None:
    assert run([Move(1, 1)], ObjectState(x=5, y=5)) == ObjectState(x=6, y=6)


def test_run_ends_with_delete() -> None:
    assert run([Move(1, 1), Delete()]).deleted


def test_run_error_in_middle() -> None:
    with pytest.raises(ObjectDeleted):
        run([Delete(), Move(1, 1)])


def test_history_length_and_last() -> None:
    states = history(PROGRAM)
    assert len(states) == len(PROGRAM) + 1
    assert states[0] == ObjectState()
    assert states[-1] == run(PROGRAM)


def test_history_empty() -> None:
    assert history([]) == [ObjectState()]


def test_run_accepts_iterator() -> None:
    assert run(iter(PROGRAM)) == run(PROGRAM)


# parse_command
def test_parse_all_kinds() -> None:
    assert parse_command({"kind": "move", "dx": "1", "dy": 2}) == Move(1, 2)
    assert parse_command({"kind": "rotate", "angle": 45}) == Rotate(45)
    assert parse_command({"kind": "scale", "factor": 2}) == Scale(2)
    assert parse_command({"kind": "delete"}) == Delete()


@pytest.mark.parametrize(
    "bad",
    [{}, {"kind": "fly"}, {"kind": "move", "dx": 1}, {"kind": "rotate"}],
)
def test_parse_invalid(bad: dict[str, object]) -> None:
    with pytest.raises(InvalidCommand):
        parse_command(bad)


def test_run_raw_json(tmp_path: Path) -> None:
    p = tmp_path / "cmds.json"
    p.write_text(json.dumps([{"kind": "move", "dx": 2, "dy": 3}]), encoding="utf-8")
    raw = json.loads(p.read_text(encoding="utf-8"))
    assert run_raw(raw) == ObjectState(x=2, y=3)


# Protocol та статистика
def test_count_by_kind() -> None:
    assert count_by_kind(PROGRAM) == {"move": 2, "rotate": 1, "scale": 1}
    assert count_by_kind([]) == {}


def test_protocol_structural() -> None:
    class Fake:
        @property
        def kind(self) -> str:
            return "move"

    items: list[HasKind] = [Move(1, 1), Delete()]
    assert [i.kind for i in items] == ["move", "delete"]
    assert Fake().kind == "move"


# pretty
def test_render_command() -> None:
    assert render_command(Move(1, 2.5)) == "move(1, 2.5)"
    assert render_command(Rotate(90)) == "rotate(90°)"
    assert render_command(Scale(2)) == "scale(×2)"
    assert render_command(Delete()) == "delete()"


def test_render_state() -> None:
    assert render_state(ObjectState(1, 2, 90, 2)) == (
        "Object(x=1, y=2, angle=90°, scale=2)"
    )
    assert render_state(ObjectState(deleted=True)) == "<deleted>"


def test_render_log() -> None:
    log = render_log([Move(1, 1), Delete()])
    lines = log.split("\n")
    assert lines[0].startswith("start ->")
    assert lines[1] == "1. move(1, 1) -> Object(x=1, y=1, angle=0°, scale=1)"
    assert lines[2] == "2. delete() -> <deleted>"
