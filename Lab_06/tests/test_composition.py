import pytest

from decorators import RateLimitError, rate_limit, timed


def test_timed_outside_logs_blocked_calls():
    """timed зверху: час логується і для заблокованих викликів."""
    logs = []
    ticks = iter([0.0, 0.1, 1.0, 1.1])

    @timed("f", logger=logs.append, clock=lambda: next(ticks))
    @rate_limit(1, 10.0, clock=lambda: 0.0)
    def f():
        return 1

    f()
    with pytest.raises(RateLimitError):
        f()
    assert len(logs) == 2

def test_timed_inside_skips_blocked_calls():
    """rate_limit зверху: заблокований виклик до timed навіть не доходить."""
    logs = []
    ticks = iter([0.0, 0.1])

    @rate_limit(1, 10.0, clock=lambda: 0.0)
    @timed("f", logger=logs.append, clock=lambda: next(ticks))
    def f():
        return 1

    f()
    with pytest.raises(RateLimitError):
        f()
    assert len(logs) == 1


def test_composition_keeps_metadata():
    @timed()
    @rate_limit(1, 1.0)
    def f():
        """Докстрінг."""
        return 1

    assert f.__name__ == "f"
    assert f.__doc__ == "Докстрінг."
    assert hasattr(f, "__wrapped__")