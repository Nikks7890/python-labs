"""Приклад мутабельної моделі рахунку для порівняння."""


class MutableAccount:
    def __init__(self, id: str, owner: str, balance: float):
        self.id = id
        self.owner = owner
        self.balance = balance
        self.transactions = []
        self.flags = set()
        self.meta = {}

    def deposit(self, amount: float) -> None:
        """Змінює стан 'на місці' (in-place)."""
        self.balance += amount
        self.transactions.append(f"Deposit: {amount}")

    def withdraw(self, amount: float) -> None:
        """Змінює стан 'на місці' (in-place)."""
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transactions.append(f"Withdraw: {amount}")