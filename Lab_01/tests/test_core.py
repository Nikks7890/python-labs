"""Тести чистого ядра: референтна прозорість, мутації, Callable-політики."""

from copy import deepcopy
from typing import Callable, Iterable

import pytest

from core import (
    Booking,
    Report,
    base_cost,
    calc_booking,
    combine_discounts,
    flat_fee,
    is_confirmed,
    long_stay_discount,
    make_processor,
    percent_fee,
    season_by_month,
    seasonal_discount,
)


@pytest.fixture
def bookings() -> list[Booking]:
    return [
        {
            "id": 1,
            "guest": "Марія",
            "room_type": "standard",
            "nights": 3,
            "price_per_night": 100.0,
            "month": 7,
            "status": "confirmed",
        },
        {
            "id": 2,
            "guest": "Олег",
            "room_type": "deluxe",
            "nights": 10,
            "price_per_night": 200.0,
            "month": 4,
            "status": "confirmed",
        },
        {
            "id": 3,
            "guest": "Ірина",
            "room_type": "suite",
            "nights": 2,
            "price_per_night": 500.0,
            "month": 4,
            "status": "cancelled",
        },
        {
            "id": 4,
            "guest": "Тарас",
            "room_type": "standard",
            "nights": 1,
            "price_per_night": 90.0,
            "month": 4,
            "status": "pending",
        },
    ]


def _min_nights(n: int) -> Callable[[Booking], bool]:
    # фабрика фільтра: беремо броні не коротші за n ночей
    def policy(b: Booking) -> bool:
        return b["nights"] >= n

    return policy


def _configured(min_nights: int = 1) -> Callable[[Iterable[Booking]], Report]:
    # збираю обробник з типовими для тестів політиками
    return make_processor(
        accept=_min_nights(min_nights),
        discount=seasonal_discount(season_by_month, {"low": 0.1}),
        fee=flat_fee({"standard": 2.0, "deluxe": 3.0, "suite": 4.0}),
    )


# референтна прозорість і відсутність мутацій
def test_referential_transparency(bookings: list[Booking]) -> None:
    p = _configured()
    snapshot = deepcopy(bookings)
    r1 = p(bookings)
    r2 = p(bookings)
    assert r1 == r2
    assert bookings == snapshot


def test_no_mutation(bookings: list[Booking]) -> None:
    snapshot = deepcopy(bookings)
    _configured()(bookings)
    assert bookings == snapshot
    for b in bookings:
        assert "total" not in b
        assert "base_cost" not in b
        assert "tourist_fee" not in b


def test_result_contains_new_objects(bookings: list[Booking]) -> None:
    result = _configured()(bookings)
    assert result["bookings"][0] is not bookings[0]


# фільтрація та правильність
def test_only_confirmed_are_processed(bookings: list[Booking]) -> None:
    result = _configured()(bookings)
    ids = [b["id"] for b in result["bookings"]]
    assert ids == [1, 2]
    assert not is_confirmed(bookings[2])
    assert not is_confirmed(bookings[3])


def test_revenue_is_correct(bookings: list[Booking]) -> None:
    # id1: 300, місяць 7 = high, але у словнику його немає -> 0% знижки
    # id2: 2000, місяць 4 = low, -10% -> 1800, збір 3*10=30 -> 1830
    # разом: 306 + 1830 = 2136
    result = _configured()(bookings)
    assert result["count"] == 2
    assert result["revenue"] == pytest.approx(2136.0)


def test_accept_policy_filters(bookings: list[Booking]) -> None:
    # спочатку тут стояло min_nights=3 і тест падав:
    # id1 має рівно 3 ночі, а порівняння було строге
    result = _configured(min_nights=5)(bookings)
    assert [b["id"] for b in result["bookings"]] == [2]


def test_swapping_policies_changes_result(bookings: list[Booking]) -> None:
    no_policies = make_processor(
        accept=lambda b: True,
        discount=lambda b, p: p,
        fee=lambda b, p: 0.0,
    )
    assert no_policies(bookings)["revenue"] == pytest.approx(2300.0)


def test_empty_bookings() -> None:
    result = _configured()([])
    assert result == {"count": 0, "revenue": 0, "bookings": []}


# окремі чисті функції та фабрики


def test_base_cost_and_pricing_fields(bookings: list[Booking]) -> None:
    assert base_cost(bookings[0]) == 300.0
    priced = calc_booking(bookings[1], lambda b, p: p * 0.5, percent_fee(0.1))
    assert priced["base_cost"] == 2000.0
    assert priced["discount"] == 1000.0
    assert priced["tourist_fee"] == 100.0
    assert priced["total"] == 1100.0


def test_fee_uses_discounted_price(bookings: list[Booking]) -> None:
    # перевіряю, що fee_percent рахується від ціни ПІСЛЯ знижки,
    # а не від базової — це легко переплутати
    priced = calc_booking(bookings[1], lambda b, p: p * 0.5, percent_fee(0.1))
    assert priced["base_cost"] == 2000.0
    assert priced["tourist_fee"] == 100.0  # 10% від 1000, не від 2000


def test_chain_discounts_composes_in_order(bookings: list[Booking]) -> None:
    policy = combine_discounts(
        seasonal_discount(season_by_month, {"low": 0.1}),
        long_stay_discount(7, 0.1),
    )
    assert policy(bookings[1], 1000.0) == pytest.approx(810.0)
    assert policy(bookings[0], 1000.0) == pytest.approx(1000.0)


@pytest.mark.parametrize(
    "month,season",
    [(7, "high"), (1, "winter"), (12, "winter"), (4, "low")],
)
def test_default_season(month: int, season: str) -> None:
    assert season_by_month(month) == season
