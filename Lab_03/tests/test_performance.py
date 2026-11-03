"""Вимірювання швидкості pure update для банківських операцій.
Використовує нативний модуль timeit.
"""

import timeit

from lab03.core import deposit, withdraw
from lab03.model import Account


def test_bench_deposit(original_account: Account) -> None:
    n = 1000
    time_taken = timeit.timeit(
        lambda: deposit(original_account, 100.0, "bench-tx"), number=n
    )
    assert (time_taken / n) < 0.001, "Deposit is too slow!"
    print(f"\n[Benchmark] Deposit: {time_taken/n:.6f} sec/op")


def test_bench_withdraw(original_account: Account) -> None:
    n = 1000
    time_taken = timeit.timeit(
        lambda: withdraw(original_account, 50.0, "bench-tx"), number=n
    )
    assert (time_taken / n) < 0.001, "Withdraw is too slow!"
    print(f"\n[Benchmark] Withdraw: {time_taken/n:.6f} sec/op")
