from core import Record, build_pipeline


def test_top_n() -> None:
    sample = [
        Record(id=1, category="Pro", results=[10.0]),
        Record(id=2, category="Pro", results=[9.0]),
        Record(id=3, category="Pro", results=[8.0]),
    ]
    top = build_pipeline(top_n=2)(sample)
    assert len(top) == 2
    assert top[0]["id"] == 1
    assert top[1]["id"] == 2


def test_sort_two_keys() -> None:
    # Однаковий score, різні id -> сортує за id
    sample = [
        Record(id=5, category="Pro", results=[10.0]),
        Record(id=2, category="Pro", results=[10.0]),
    ]
    top = build_pipeline(top_n=2)(sample)
    assert top[0]["id"] == 2
