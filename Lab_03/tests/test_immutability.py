"""Тести незмінності, pure-updates та хешованості для банківського рахунку."""

import copy
import dataclasses

import pytest
from lab03.core import (
    add_flag,
    block_account,
    calculate_total_inflow,
    calculate_total_outflow,
    deposit,
    freeze,
    source,
    withdraw,
)
from lab03.model import Account, Transaction


def test_deposit_returns_new_object(original_account: Account) -> None:
    snapshot = copy.deepcopy(original_account)
    new_account = deposit(original_account, 500.0, "tx-3")

    assert new_account is not original_account
    assert original_account == snapshot
    assert len(new_account.transactions) == len(original_account.transactions) + 1
    assert new_account.balance == pytest.approx(original_account.balance + 500.0)


def test_withdraw_returns_new_object(original_account: Account) -> None:
    snapshot = copy.deepcopy(original_account)
    new_account = withdraw(original_account, 100.0, "tx-4")

    assert new_account is not original_account
    assert original_account == snapshot
    assert new_account.balance == pytest.approx(original_account.balance - 100.0)


def test_block_account_returns_new_object(original_account: Account) -> None:
    snapshot = copy.deepcopy(original_account)
    blocked = block_account(original_account)

    assert "blocked" in blocked.flags
    assert "blocked" not in original_account.flags
    assert original_account == snapshot


def test_add_flag_returns_new_object(original_account: Account) -> None:
    snapshot = copy.deepcopy(original_account)
    vip_acc = add_flag(original_account, "vip")

    assert "vip" in vip_acc.flags
    assert "vip" not in original_account.flags
    assert original_account == snapshot


def test_frozen_dataclass_disallows_setattr(original_account: Account) -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        original_account.balance = 99999.0  # type: ignore[misc]


def test_mappingproxy_is_read_only(original_account: Account) -> None:
    with pytest.raises(TypeError):
        original_account.meta["source"] = "hacked"  # type: ignore[index]


def test_transactions_is_tuple(original_account: Account) -> None:
    assert isinstance(original_account.transactions, tuple)
    with pytest.raises(AttributeError):
        original_account.transactions.append(Transaction("tx-x", 1.0))  # type: ignore[attr-defined]


def test_flags_is_frozenset(original_account: Account) -> None:
    assert isinstance(original_account.flags, frozenset)
    with pytest.raises(AttributeError):
        original_account.flags.add("x")  # type: ignore[attr-defined]


def test_account_is_hashable(original_account: Account) -> None:
    other = deposit(original_account, 50.0, "tx-9")
    accounts = {original_account, other}
    assert len(accounts) == 2


def test_transaction_is_hashable() -> None:
    a = Transaction("tx-1", 100.0, "Test")
    b = Transaction("tx-1", 100.0, "Test")
    assert a == b
    assert hash(a) == hash(b)
    assert {a, b} == {a}


def test_freeze_deep_structure() -> None:
    raw = {
        "tags": {"a", "b"},
        "list": [1, 2, {"k": "v"}],
    }
    frozen = freeze(raw)

    with pytest.raises(TypeError):
        frozen["new"] = "x"

    inner_list = frozen["list"]
    assert isinstance(inner_list, tuple)
    assert isinstance(inner_list[-1], type(frozen))


def test_calculate_totals(original_account: Account) -> None:
    assert calculate_total_inflow(original_account) == 1000.0
    assert calculate_total_outflow(original_account) == 200.0


def test_source_meta(original_account: Account) -> None:
    assert source(original_account.meta) == "mobile_app"
    assert source({}) == "unknown"


def test_blocked_account_cannot_add_transaction(original_account: Account) -> None:
    blocked = block_account(original_account)
    with pytest.raises(ValueError, match="blocked account"):
        deposit(blocked, 100.0, "tx-new")


def test_insufficient_funds(original_account: Account) -> None:
    with pytest.raises(ValueError, match="Insufficient funds"):
        withdraw(original_account, 10000.0, "tx-fail")
