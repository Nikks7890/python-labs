"""Алгоритми для лабораторної роботи №4 (Варіант 5: Merge Sort)."""

from collections import deque
from collections.abc import Generator
from dataclasses import dataclass
from functools import cache
from random import choice


def merge(left: list[int], right: list[int]) -> list[int]:
    """Допоміжна функція для злиття двох відсортованих списків."""
    result: list[int] = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr: list[int]) -> list[int]:
    """Чистий рекурсивний merge sort без мутації вхідного списку."""
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)


def quicksort(xs: list[int]) -> list[int]:
    """Рекурсивний quicksort для порівняння."""
    if len(xs) <= 1:
        return xs[:]

    p = choice(xs)
    left = [x for x in xs if x < p]
    mid = [x for x in xs if x == p]
    right = [x for x in xs if x > p]

    return quicksort(left) + mid + quicksort(right)


@dataclass(slots=True)
class Node:
    """Вузол бінарного дерева."""

    key: int
    left: "Node | None" = None
    right: "Node | None" = None


def preorder(t: "Node | None") -> Generator[int, None, None]:
    if t is None:
        return
    yield t.key
    yield from preorder(t.left)
    yield from preorder(t.right)


def inorder(t: "Node | None") -> Generator[int, None, None]:
    if t is None:
        return
    yield from inorder(t.left)
    yield t.key
    yield from inorder(t.right)


def postorder(t: "Node | None") -> Generator[int, None, None]:
    if t is None:
        return
    yield from postorder(t.left)
    yield from postorder(t.right)
    yield t.key


def bfs_level_order(t: "Node | None") -> list[int]:
    """Ітеративний обхід у ширину."""
    if not t:
        return []
    q = deque([t])
    out = []
    while q:
        n = q.popleft()
        out.append(n.key)
        if n.left:
            q.append(n.left)
        if n.right:
            q.append(n.right)
    return out


def dfs_preorder_iter(t: "Node | None") -> list[int]:
    """Ітеративний DFS (preorder) з власним стеком."""
    if not t:
        return []
    stack, out = [t], []
    while stack:
        n = stack.pop()
        out.append(n.key)
        if n.right:
            stack.append(n.right)
        if n.left:
            stack.append(n.left)
    return out


@cache
def fib(n: int) -> int:
    """Мемоізоване обчислення чисел Фібоначчі."""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def fib_iter(n: int) -> int:
    """Ітеративна версія Фібоначчі для уникнення ліміту стеку."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
