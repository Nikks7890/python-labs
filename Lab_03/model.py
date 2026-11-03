"""Незмінна доменна модель банківського рахунку. Варіант 5"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Any


@dataclass(frozen=True, slots=True)
class Transaction:
    """Одна транзакція по рахунку.
    amount > 0 — поповнення (credit), amount < 0 — списання (debit).
    """

    tx_id: str
    amount: float
    description: str = ""


@dataclass(frozen=True, slots=True)
class Account:
    """Банківський рахунок. Усі 'зміни'  через dataclasses.replace."""

    id: str
    owner: str
    balance: float
    transactions: tuple[Transaction, ...]
    flags: frozenset[str]
    meta: Mapping[str, str]

    def is_blocked(self) -> bool:
        return "blocked" in self.flags

    def transaction_count(self) -> int:
        return len(self.transactions)

    def add_transaction(self, tx: Transaction) -> Account:
        """Додає транзакцію та оновлює баланс. Повертає новий об'єкт."""
        if self.is_blocked():
            raise ValueError("Cannot add transaction to a blocked account")

        new_balance = round(self.balance + tx.amount, 2)
        return replace(
            self, balance=new_balance, transactions=self.transactions + (tx,)
        )

    def add_flag(self, flag: str) -> Account:
        """Додає прапорець (наприклад, 'vip', 'blocked')."""
        return replace(self, flags=self.flags | frozenset({flag}))

    def block(self) -> Account:
        """Блокує рахунок."""
        return self.add_flag("blocked")

    def with_meta(self, key: str, value: str) -> Account:
        """Оновлює метадані. Копіюємо dict, бо MappingProxyType незмінний."""
        new_meta = dict(self.meta)
        new_meta[key] = value
        return replace(self, meta=MappingProxyType(new_meta))

    def __hash__(self) -> int:
        return hash(
            (
                self.id,
                self.owner,
                self.balance,
                self.transactions,
                self.flags,
                tuple(sorted(self.meta.items())),
            )
        )

    def __deepcopy__(self, memo: dict[int, Any]) -> Account:
        from copy import deepcopy

        new_meta = dict(deepcopy(dict(self.meta), memo))
        return Account(
            id=self.id,
            owner=self.owner,
            balance=self.balance,
            transactions=deepcopy(self.transactions, memo),
            flags=deepcopy(self.flags, memo),
            meta=MappingProxyType(new_meta),
        )
