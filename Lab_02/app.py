import json

from core import Record


def load_records(filepath: str) -> list[Record]:
    """Завантажує список записів з JSON файлу."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Record(**item) for item in data]  # type: ignore
