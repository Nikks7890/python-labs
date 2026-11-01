"""Головний файл для демонстрації роботи алгоритмів з ЛР4."""

from algorithms import (
    Node,
    bfs_level_order,
    fib,
    fib_iter,
    inorder,
    merge_sort,
    preorder,
    quicksort,
)


def main() -> None:
    print("1. Демонстрація сортування (Варіант 5: Merge Sort)")
    unsorted_arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"Початковий масив: {unsorted_arr}")
    print(f"Merge Sort:       {merge_sort(unsorted_arr)}")
    print(f"Quick Sort:       {quicksort(unsorted_arr)}")
    print(f"Чи змінився оригінал? {unsorted_arr}\n")

    print("2. Демонстрація обходів дерева")
    tree = Node(4, Node(2, Node(1), Node(3)), Node(6, None, Node(7)))
    print(f"Preorder (рекурсивно):  {list(preorder(tree))}")
    print(f"Inorder (рекурсивно):   {list(inorder(tree))}")
    print(f"BFS (ітеративно):       {bfs_level_order(tree)}\n")

    print("3. Демонстрація мемоізації (Фібоначчі)")
    fib.cache_clear()  # Очищаємо кеш перед стартом
    print(f"Fib(10) з кешем: {fib(10)}")
    print(f"Fib(20) з кешем: {fib(20)}")
    print(f"Fib(30) з кешем: {fib(30)}")

    # Показуємо, що кеш дійсно працює
    cache_info = fib.cache_info()
    print(f"Статистика кешу: {cache_info}")

    print(f"Fib(30) без кешу (ітеративно): {fib_iter(30)}")


if __name__ == "__main__":
    main()
