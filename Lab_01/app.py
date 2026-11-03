"""Оболонка побічних ефектів: формує дані, викликає ядро, друкує звіт"""

from core import (
    Booking,
    Report,
    combine_discounts,
    flat_fee,
    long_stay_discount,
    make_processor,
    season_by_month,
    seasonal_discount,
)

SAMPLE: list[Booking] = [
    {
        "id": 1,
        "guest": "Олена",
        "room_type": "standard",
        "nights": 3,
        "price_per_night": 80.0,
        "month": 7,
        "status": "confirmed",
    },
    {
        "id": 2,
        "guest": "Андрій",
        "room_type": "deluxe",
        "nights": 7,
        "price_per_night": 150.0,
        "month": 1,
        "status": "confirmed",
    },
    {
        "id": 3,
        "guest": "Ірина",
        "room_type": "suite",
        "nights": 2,
        "price_per_night": 300.0,
        "month": 4,
        "status": "cancelled",
    },
    {
        "id": 4,
        "guest": "Максим",
        "room_type": "standard",
        "nights": 1,
        "price_per_night": 70.0,
        "month": 10,
        "status": "confirmed",
    },
]


def min_nights(n: int):
    # фабрика фільтра: беремо броні не коротші за n ночей
    def policy(booking: Booking) -> bool:
        return booking.get("nights", 0) >= n

    return policy


def render_report(report: Report) -> str:
    lines = [
        f"#{b['id']} {b['guest']:<8} база={b['base_cost']:>8.2f} "
        f"знижка={b['discount']:>7.2f} збір={b['tourist_fee']:>6.2f} "
        f"разом={b['total']:>8.2f}"
        for b in report["bookings"]
    ]
    lines.append(f"Бронювань: {report['count']}, дохід: {report['revenue']:.2f}")
    return "\n".join(lines)


def main() -> None:
    # сезонні знижки: high і low; зимою менше
    season_rates = {"low": 0.15, "winter": 0.05, "high": 0.20}

    processor = make_processor(
        accept=min_nights(2),
        discount=combine_discounts(
            seasonal_discount(season_by_month, season_rates),
            long_stay_discount(min_nights=7, rate=0.10),
        ),
        fee=flat_fee({"standard": 1.5, "deluxe": 2.5, "suite": 4.0}),
    )
    print(render_report(processor(SAMPLE)))


if __name__ == "__main__":
    main()
