import argparse

from app import load_records
from core import build_pipeline, reduce_stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Спортивний рейтинг (Варіант 5)")
    parser.add_argument("--data", type=str, default="sample_data.json", help="Шлях до JSON")
    parser.add_argument("--top", type=int, default=3, help="Кількість у Top-N")
    parser.add_argument("--category", type=str, default="Pro", help="Категорія для бонусу")
    parser.add_argument("--factor", type=float, default=1.1, help="Множник бонусу")
    args = parser.parse_args()

    records = load_records(args.data)
    pipeline = build_pipeline(top_n=args.top, category=args.category, factor=args.factor)
    top = pipeline(records)

    print(
        f"\nТоп-{args.top} спортсменів (бонус категорії '{args.category}' x{args.factor})"
    )
    for r in top:
        print(
            f"  #{r['id']:>2} | {r['name']:<20} | [{r.get('category', ''):<8}] | score = {r['score']:.2f}"
        )

    stats = reduce_stats(top)
    print("\nАгрегація (reduce)")
    print(f"  Кількість: {int(stats['count'])}")
    print(f"  Сума балів: {stats['sum_points']:.2f}")
    print(f"  Середній бал: {stats['avg_points']:.2f}\n")


if __name__ == "__main__":
    main()
