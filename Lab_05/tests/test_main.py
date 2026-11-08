from main import main


def test_main_runs(capsys):
    main()
    out = capsys.readouterr().out
    assert "варіант 5" in out
    assert "[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]" in out
    assert "Префіксні суми" in out
