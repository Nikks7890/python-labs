from types import MappingProxyType

import pytest

from lab03.model import Account, Transaction


@pytest.fixture
def base_transactions() -> tuple[Transaction, ...]:
    return (
        Transaction("tx-1", 1000.0, "Initial deposit"),
        Transaction("tx-2", -200.0, "Coffee"),
    )


@pytest.fixture
def original_account(base_transactions: tuple[Transaction, ...]) -> Account:
    return Account(
        id="ACC-001",
        owner="Ivan Petrenko",
        balance=800.0,
        transactions=base_transactions,
        flags=frozenset({"standard"}),
        meta=MappingProxyType({"source": "mobile_app", "branch": "kyiv-01"}),
    )
