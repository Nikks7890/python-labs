"""Тести для Merge Sort (Варіант 5)."""

from algorithms import merge_sort


def test_merge_sort_basic() -> None:
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]
    assert merge_sort([3, 2, 1]) == [1, 2, 3]
    assert merge_sort([5, 2, 8, 1, 9]) == [1, 2, 5, 8, 9]


def test_merge_sort_no_mutation() -> None:
    original = [3, 1, 4, 1, 5]
    sorted_arr = merge_sort(original)
    assert original == [3, 1, 4, 1, 5]  # Оригінал не змінився
    assert sorted_arr == [1, 1, 3, 4, 5]
