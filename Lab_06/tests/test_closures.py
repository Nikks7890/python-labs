from closures import make_counter, make_logger, make_window


def test_counter_default_start():
    c = make_counter()
    assert c() == 1
    assert c() == 2


def test_counter_with_start():
    c = make_counter(10)
    assert c() == 11
    assert c() == 12


def test_counters_are_independent():
    a = make_counter()
    b = make_counter(100)
    a()
    a()
    assert b() == 101
    assert a() == 3


def test_logger_prefix(capsys):
    info = make_logger("INFO")
    info("ready")
    assert capsys.readouterr().out == "[INFO] ready\n"


def test_window_allows_up_to_max():
    allowed = make_window(2, 10.0, lambda: 0.0)
    assert allowed() is True
    assert allowed() is True
    assert allowed() is False


def test_window_frees_place_after_period():
    t = [0.0]
    allowed = make_window(1, 5.0, lambda: t[0])
    assert allowed() is True
    t[0] = 4.9
    assert allowed() is False
    t[0] = 5.0
    assert allowed() is True


def test_windows_are_independent():
    a = make_window(1, 10.0, lambda: 0.0)
    b = make_window(1, 10.0, lambda: 0.0)
    assert a() is True
    assert b() is True
