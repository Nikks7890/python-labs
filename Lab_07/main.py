from pathlib import Path

from core import clean_and_rank, team_total
from models import Athlete


def main() -> None:
    print("Топ-3 з JSON:")
    for r in clean_and_rank("sample_data.json", top=3):
        print(r)

    print("\nТоп-3 з CSV (Path):")
    for r in clean_and_rank(Path("sample_data.csv"), top=3):
        print(r)

    # командна сума через reduce (тільки допущені спортсмени)
    allowed = clean_and_rank("sample_data.json", top=100)
    print("\nКомандна сума:", team_total(allowed))

    # порівняння спортсменів
    a = Athlete("Anna", "USA", 95.0, 3.0, 22)
    b = Athlete("Oleh", "Ukraine", 92.5, 1.5, 24)
    print("\nAnna > Oleh:", a > b, "| Anna <= Oleh:", a <= b)
    print("Відсортовано:", sorted([a, b]))


if __name__ == "__main__":
    main()
