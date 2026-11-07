from app import load_records


def test_load_records(tmp_path) -> None:  # type: ignore
    d = tmp_path / "data.json"
    d.write_text(
        '[{"id": 1, "name": "test", "category": "Pro", "results": [5.0]}]',
        encoding="utf-8",
    )

    records = load_records(str(d))
    assert len(records) == 1
    assert records[0]["id"] == 1
