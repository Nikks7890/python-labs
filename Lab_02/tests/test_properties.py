from core import Record, build_pipeline


def test_category_bonus() -> None:
    sample = [
        Record(id=1, category="Pro", results=[10.0]),
        Record(id=2, category="Amateur", results=[10.0]),
    ]
    top = build_pipeline(top_n=2, category="Pro", factor=1.5)(sample)
    assert top[0]["id"] == 1
    assert top[0]["score"] == 15.0  # 10 * 1.5 = 15
    assert top[1]["score"] == 10.0


def test_filter_min_score() -> None:
    sample = [
        Record(id=1, results=[10.0]),
        Record(id=2, results=[5.0]),
    ]
    top = build_pipeline(top_n=5, min_score=8.0)(sample)
    assert len(top) == 1
    assert top[0]["id"] == 1
