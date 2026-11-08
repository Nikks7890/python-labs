import pytest

from streams import (
    drop_while,
    exceeding,
    first_exceeding,
    moving_average,
    overheat_run,
    take,
    take_exceeding,
    take_while,
    temperature_stream,
)

READINGS = [18, 19, 21, 24, 27, 30, 26, 22, 19]


def test_temperature_stream_is_repeatable_with_seed():
    assert take(5, temperature_stream(seed=1)) == take(5, temperature_stream(seed=1))


def test_temperature_stream_differs_without_same_seed():
    assert take(5, temperature_stream(seed=1)) != take(5, temperature_stream(seed=2))


def test_first_exceeding_found():
    avgs = moving_average(READINGS, 3)
    assert first_exceeding(avgs, 25) == pytest.approx(27.0)


def test_first_exceeding_not_found():
    assert first_exceeding([1, 2, 3], 10) is None


def test_first_exceeding_empty():
    assert first_exceeding([], 10) is None


def test_exceeding_is_strict():
    assert list(exceeding([10, 11, 9, 12], 10)) == [11, 12]


def test_take_exceeding():
    avgs = moving_average(READINGS, 3)
    assert take_exceeding(avgs, 25, 2) == pytest.approx([27.0, 83 / 3])


def test_take_exceeding_on_infinite_stream():
    stream = moving_average(temperature_stream(seed=7, base=30, spread=3), 3)
    res = take_exceeding(stream, 25, 4)
    assert len(res) == 4
    assert all(x > 25 for x in res)


def test_overheat_run():
    avgs = moving_average(READINGS, 3)
    assert list(overheat_run(avgs, 25)) == pytest.approx([27.0, 83 / 3, 26.0])


def test_overheat_run_no_overheat():
    assert list(overheat_run([1, 2, 3], 10)) == []


def test_take_while_drop_while_wrappers():
    assert list(take_while(lambda x: x < 3, [1, 2, 3, 1])) == [1, 2]
    assert list(drop_while(lambda x: x < 3, [1, 2, 3, 1])) == [3, 1]
