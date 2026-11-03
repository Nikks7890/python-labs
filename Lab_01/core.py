"""Ядро розрахунку бронювань готелю (варіант 5)."""

from __future__ import annotations

from functools import reduce
from typing import Callable, Iterable, Mapping, Sequence, TypedDict


class Booking(TypedDict, total=False):
    id: int
    guest: str
    room_type: str
    nights: int
    price_per_night: float
    month: int          # 1..12
    status: str         #"confirmed" / "pending" / "cancelled"

    # ці поля з'являються тільки після розрахунку
    base_cost: float
    discount: float
    tourist_fee: float
    total: float


class Report(TypedDict):
    count: int
    revenue: float
    bookings: list[Booking]


# типи політик
AcceptFn = Callable[[Booking], bool]
DiscountFn = Callable[[Booking, float], float]
FeeFn = Callable[[Booking, float], float]
SeasonFn = Callable[[int], str]


#прості чисті функції

def base_cost(booking: Booking) -> float:
    # скільки коштує проживання без знижок і зборів
    return booking["nights"] * booking["price_per_night"]


def is_confirmed(booking: Booking) -> bool:
    # .get, бо status може бути відсутнім
    return booking.get("status") == "confirmed"


def calc_booking(booking: Booking, discount: DiscountFn, fee: FeeFn) -> Booking:
    # повертаємо КОПІЮ брони, оригінал не чіпаємо
    gross = base_cost(booking)
    after_discount = discount(booking, gross)
    fee_amount = fee(booking, after_discount)

    return {
        **booking,
        "base_cost": gross,
        "discount": gross - after_discount,
        "tourist_fee": fee_amount,
        "total": after_discount + fee_amount,
    }


def make_report(bookings: Sequence[Booking]) -> Report:
    # округлення робимо лише тут, на етапі звіту
    revenue = sum(b["total"] for b in bookings)
    return {
        "count": len(bookings),
        "revenue": round(revenue, 2),
        "bookings": list(bookings),
    }

#фабрики політик
def season_by_month(month: int) -> str:
    if month in (6, 7, 8):
        return "high"
    if month in (12, 1, 2):
        return "winter"
    return "low"


def seasonal_discount(season_of: SeasonFn, rates: Mapping[str, float]) -> DiscountFn:
    # знижка залежить від сезону заїзду; невідомий сезон -> 0
    def policy(booking: Booking, price: float) -> float:
        rate = rates.get(season_of(booking["month"]), 0.0)
        return price * (1 - rate)

    return policy


def long_stay_discount(min_nights: int, rate: float) -> DiscountFn:
    # знижка за довге проживання
    def policy(booking: Booking, price: float) -> float:
        if booking["nights"] >= min_nights:
            return price * (1 - rate)
        return price

    return policy


def combine_discounts(*policies: DiscountFn) -> DiscountFn:
    # складаємо кілька знижок в одну (композиція)
    def policy(booking: Booking, price: float) -> float:
        return reduce(lambda acc, p: p(booking, acc), policies, price)

    return policy


def flat_fee(by_room: Mapping[str, float], default: float = 0.0) -> FeeFn:
    # туристичний збір: фіксована сума за ніч залежно від типу номера
    def policy(booking: Booking, _price: float) -> float:
        return by_room.get(booking["room_type"], default) * booking["nights"]

    return policy


def percent_fee(rate: float) -> FeeFn:
    # туристичний збір як відсоток від ціни після знижки
    def policy(_booking: Booking, price: float) -> float:
        return price * rate

    return policy


def make_processor(
    *, accept: AcceptFn, discount: DiscountFn, fee: FeeFn
) -> Callable[[Iterable[Booking]], Report]:
    # фабрика: повертає обробник, налаштований під конкретні політики
    def process(bookings: Iterable[Booking]) -> Report:
        priced = [
            calc_booking(b, discount, fee)
            for b in bookings
            if is_confirmed(b) and accept(b)
        ]
        return make_report(priced)

    return process