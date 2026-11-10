import pytest

from decorators import timed


def test_timed_uses_clock_and_logger():
    ticks = [0.0, 0.012345]
    logs = []

    @timed("work", unit="ms", logger=logs.append, clock=lambda: ticks.pop(0))
    def work(x):
        return x * x

    assert work(5) == 25
    assert any("work took 12.345 ms" in m for m in logs)


def test_timed_units():
    logs = []

    @timed("a", unit="s", logger=logs.append, clock=iter([0.0, 2.0]).__next__)
    def a():
        return 1

    a()
    assert logs == ["[timed] a took 2.000 s"]


def test_timed_default_label_is_function_name():
    logs = []

    @timed(logger=logs.append, clock=iter([0.0, 1.0]).__next__)
    def my_func():
        return 1

    my_func()
    assert "my_func" in logs[0]


def test_timed_logs_even_on_exception():
    logs = []

    @timed("bad", logger=logs.append, clock=iter([0.0, 0.5]).__next__)
    def bad():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        bad()
    assert len(logs) == 1
    assert "bad took" in logs[0]


def test_timed_keeps_metadata():
    @timed()
    def add(a, b):
        """Додає два числа."""
        return a + b

    assert add.__name__ == "add"
    assert add.__doc__ == "Додає два числа."
    assert hasattr(add, "__wrapped__")


def test_timed_passes_args_and_kwargs():
    @timed(logger=lambda _: None)
    def f(a, b=0):
        return a - b

    assert f(5, b=2) == 3
