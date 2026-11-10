import csv
import io
import json
from functools import singledispatch
from pathlib import Path
from typing import Any


def _read_path(p: Path) -> list[dict[str, Any]]:
    # за розширенням вирішуємо csv це чи json
    if p.suffix.lower() == ".csv":
        with p.open(encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    return json.loads(p.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


@singledispatch
def load_results(src: Any) -> list[dict[str, Any]]:
    raise TypeError(f"Unsupported type: {type(src)!r}")


@load_results.register
def _(src: str) -> list[dict[str, Any]]:
    s = src.strip()
    if s.startswith("["):
        return json.loads(s)  # type: ignore[no-any-return]
    return _read_path(Path(s))


@load_results.register
def _(src: Path) -> list[dict[str, Any]]:
    return _read_path(src)


@load_results.register
def _(src: io.TextIOBase) -> list[dict[str, Any]]:
    # для відкритого файлу дивимось на його назву
    if str(getattr(src, "name", "")).lower().endswith(".csv"):
        return list(csv.DictReader(src))
    return json.load(src)  # type: ignore[no-any-return]


@load_results.register
def _(src: list) -> list[dict[str, Any]]:  # type: ignore[type-arg]
    if src and not isinstance(src[0], dict):
        raise ValueError("Expected list of dicts")
    return src
