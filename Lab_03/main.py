"""Демонстрація роботи незмінної моделі банківського рахунку."""

from types import MappingProxyType

from lab03.core import deposit, withdraw, block_account
from lab03.model import Account, Transaction


def main() -> None:
    account = Account(
        id="ACC-001",
        owner="Veronika",
        balance=1000.0,
        transactions=(),
        flags=frozenset({"standard"}),
        meta=MappingProxyType({"source": "terminal"}),
    )
    print(f"Початковий баланс: {account.balance}")


    new_acc = deposit(account, 500.0, "tx-1")
    print(f"Після депозиту: {new_acc.balance} (старий баланс: {account.balance})")


    new_acc2 = withdraw(new_acc, 200.0, "tx-2")
    print(f"Після зняття: {new_acc2.balance}")


    blocked = block_account(new_acc2)
    print(f"Рахунок заблоковано: {'blocked' in blocked.flags}")


if __name__ == "__main__":
    main()