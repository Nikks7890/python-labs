from main import main


def test_main_runs(capsys):
    main()
    out = capsys.readouterr().out
    assert "Лічильник: 11, 12, 13" in out
    assert "відмова" in out
    assert "t=6.0: результат 12" in out
    assert "Ім'я функції: get_data" in out
