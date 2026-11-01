"""Чисті бізнес-функції над незмінною моделлю Account."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

from .model import Account, Transaction


def deposit(
    account: Account, amount: float, tx_id: str, desc: str = "Deposit"
) -> Account:
    if amount <= 0:
        raise ValueError("Deposit amount must be positive")
    return account.add_transaction(Transaction(tx_id, amount, desc))


def withdraw(
    account: Account, amount: float, tx_id: str, desc: str = "Withdrawal"
) -> Account:
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")
    if account.balance - amount < 0:
        raise ValueError("Insufficient funds")
    return account.add_transaction(Transaction(tx_id, -amount, desc))


def block_account(account: Account) -> Account:
    return account.block()


def add_flag(account: Account, flag: str) -> Account:
    return account.add_flag(flag)


def calculate_total_inflow(account: Account) -> float:
    return sum(tx.amount for tx in account.transactions if tx.amount > 0)


def calculate_total_outflow(account: Account) -> float:
    return abs(sum(tx.amount for tx in account.transactions if tx.amount < 0))


def source(meta: Mapping[str, str]) -> str:
    return meta.get("source", "unknown")


def freeze(obj: Any) -> Any:
    if isinstance(obj, Mapping):
        if isinstance(obj, MappingProxyType):
            return obj
        copied = {k: freeze(v) for k, v in obj.items()}
        return MappingProxyType(copied)
    if isinstance(obj, (set, frozenset)):
        return frozenset(freeze(x) for x in obj)
    if isinstance(obj, (list, tuple)):
        return tuple(freeze(x) for x in obj)
    return obj
