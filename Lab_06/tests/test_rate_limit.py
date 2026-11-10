import pytest

from decorators import RateLimitError, rate_limit


def make_func(max_calls, period, t, logs=None):
    """Допоміжна функція: декорована функція з фальшивим годинником t."""
    logger = logs.append if logs is not None else (lambda _: None)

    @rate_limit(max_calls, period, clock=lambda: t[0], logger=logger)
    def f(x=1):
        """Документація."""
        return x * 2

    return f


def test_allows_calls_within_limit():
    t = [0.0]
    f = make_func(3, 10.0, t)
    assert f() == 2
    assert f(5) == 10
    assert f() == 2


def test_blocks_when_limit_exceeded():
    t = [0.0]
    f = make_func(2, 10.0, t)
    f()
    f()
    with pytest.raises(RateLimitError):
        f()


def test_boundary_just_before_end_of_window():
    t = [0.0]
    f = make_func(1, 5.0, t)
    f()
    t[0] = 4.999
    with pytest.raises(RateLimitError):
        f()


def test_boundary_exactly_at_end_of_window():
    t = [0.0]
    f = make_func(1, 5.0, t)
    f()
    t[0] = 5.0
    assert f() == 2


def test_window_slides():
    t = [0.0]
    f = make_func(2, 10.0, t)
    f()  # t=0
    t[0] = 6.0
    f()  # t=6
    t[0] = 10.0  # перший виклик вийшов з вікна, другий ще ні
    f()
    with pytest.raises(RateLimitError):
        f()


def test_blocked_calls_are_not_counted():
    t = [0.0]
    f = make_func(1, 5.0, t)
    f()
    for _ in range(3):
        with pytest.raises(RateLimitError):
            f()
    t[0] = 5.0
    assert f() == 2


def test_function_not_called_when_blocked():
    calls = []
    t = [0.0]

    @rate_limit(1, 10.0, clock=lambda: t[0])
    def f():
        calls.append(1)

    f()
    with pytest.raises(RateLimitError):
        f()
    assert len(calls) == 1


def test_exception_inside_function_counts_as_call():
    t = [0.0]

    @rate_limit(1, 10.0, clock=lambda: t[0])
    def bad():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        bad()
    with pytest.raises(RateLimitError):
        bad()


def test_logger_gets_message_on_block():
    t = [0.0]
    logs = []
    f = make_func(1, 10.0, t, logs)
    f()
    with pytest.raises(RateLimitError):
        f()
    assert logs == ["[rate_limit] f заблоковано"]


def test_state_is_separate_for_each_function():
    t = [0.0]
    f = make_func(1, 10.0, t)
    g = make_func(1, 10.0, t)
    f()
    assert g() == 2


def test_keeps_metadata():
    f = make_func(1, 1.0, [0.0])
    assert f.__name__ == "f"
    assert f.__doc__ == "Документація."
    assert hasattr(f, "__wrapped__")


def test_bad_parameters():
    with pytest.raises(ValueError):
        rate_limit(0, 1.0)
    with pytest.raises(ValueError):
        rate_limit(-1, 1.0)
    with pytest.raises(ValueError):
        rate_limit(1, 0)
    with pytest.raises(ValueError):
        rate_limit(1, -5.0)
