import pytest
import tempfile
import os
from purchase_analyzer import (
    read_purchases,
    count_errors,
    total_spent,
    spent_by_category,
    top_n_expensive
)


def create_test_file(content: str) -> str:
    """Создает временный файл с заданным содержимым."""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(content)
    return f.name


def test_read_valid_purchases():
    """Тест чтения валидных покупок."""
    content = """2025-09-01;food;Milk;1.20;2
2025-09-01;transport;Bus;1.50;4"""

    filename = create_test_file(content)
    try:
        purchases = read_purchases(filename)

        assert len(purchases) == 2
        assert purchases[0]['date'] == '2025-09-01'
        assert purchases[0]['category'] == 'food'
        assert purchases[0]['name'] == 'Milk'
        assert purchases[0]['price'] == 1.20
        assert purchases[0]['quantity'] == 2.0
        assert purchases[0]['total'] == 2.40

        assert purchases[1]['category'] == 'transport'
        assert purchases[1]['total'] == 6.0

    finally:
        os.unlink(filename)


def test_skip_invalid_lines():
    """Тест пропуска строк с ошибками."""
    content = """2025-09-01;food;Milk;1.20;2
2025-09-01;food;Bread;0.85
2025-09-02;transport;Bus;abc;4
2025-09-03;food;Cheese;3.75;1
2025-09-04;food;Eggs;2.50;-1"""

    filename = create_test_file(content)
    try:
        purchases = read_purchases(filename)

        # Должны быть прочитаны только 2 валидные строки
        assert len(purchases) == 2
        assert purchases[0]['name'] == 'Milk'
        assert purchases[1]['name'] == 'Cheese'

    finally:
        os.unlink(filename)


def test_count_errors():
    """Тест подсчета ошибок."""
    content = """2025-09-01;food;Milk;1.20;2
2025-09-01;food;Bread;0.85
2025-09-02;transport;Bus;abc;4

2025-09-03;food;Cheese;3.75;1
2025-09-04;food;Eggs;2.50;-1"""

    filename = create_test_file(content)
    try:
        errors = count_errors(filename)

        # Всего строк: 6 (включая пустую строку)
        # Валидные: Milk и Cheese = 2 строки
        # Ошибки: 6 - 2 = 4
        assert errors == 4

    finally:
        os.unlink(filename)


def test_total_spent():
    """Тест вычисления общей суммы."""
    purchases = [
        {'total': 10.0},
        {'total': 5.5},
        {'total': 3.2}
    ]

    total = total_spent(purchases)
    assert total == 18.7


def test_spent_by_category():
    """Тест группировки по категориям."""
    purchases = [
        {'category': 'food', 'total': 10.0},
        {'category': 'transport', 'total': 5.5},
        {'category': 'food', 'total': 3.2},
        {'category': 'entertainment', 'total': 8.0}
    ]

    categories = spent_by_category(purchases)

    assert len(categories) == 3
    assert categories['food'] == 13.2
    assert categories['transport'] == 5.5
    assert categories['entertainment'] == 8.0


def test_top_n_expensive():
    """Тест поиска топ-N самых дорогих покупок."""
    purchases = [
        {'name': 'A', 'total': 5.0},
        {'name': 'B', 'total': 15.0},
        {'name': 'C', 'total': 10.0},
        {'name': 'D', 'total': 3.0},
        {'name': 'E', 'total': 8.0}
    ]

    top3 = top_n_expensive(purchases, 3)

    assert len(top3) == 3
    assert top3[0]['name'] == 'B'
    assert top3[1]['name'] == 'C'
    assert top3[2]['name'] == 'E'
    assert top3[0]['total'] == 15.0


def test_top_n_with_small_list():
    """Тест поиска топ-N, когда покупок меньше чем N."""
    purchases = [
        {'name': 'A', 'total': 5.0},
        {'name': 'B', 'total': 3.0}
    ]

    top5 = top_n_expensive(purchases, 5)

    assert len(top5) == 2
    assert top5[0]['name'] == 'A'


def test_empty_file():
    """Тест обработки пустого файла."""
    content = ""

    filename = create_test_file(content)
    try:
        purchases = read_purchases(filename)
        errors = count_errors(filename)

        assert len(purchases) == 0
        assert errors == 0

    finally:
        os.unlink(filename)


def test_file_with_only_bad_lines():
    """Тест файла только с ошибочными строками."""
    content = """2025-09-01;food;Bread;0.85
2025-09-02;transport;Bus;abc;4;extra
bad format
"""

    filename = create_test_file(content)
    try:
        purchases = read_purchases(filename)
        errors = count_errors(filename)

        assert len(purchases) == 0
        assert errors == 4  # 3 строки + пустая строка в конце

    finally:
        os.unlink(filename)