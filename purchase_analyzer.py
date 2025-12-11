'''def read_purchases(path) -> list[dict]:
    purchases = []
    file = open('purchases.txt')
    for i in file.readlines():
        i = i.split(';')
        meal = {
            'date': i[0],
            'category': i[1],
            'name': i[2],
            'price': i[3],
            'quantity': i[4]
        }
    return meal'''


"""def read_purchases(path: str) -> list[dict]:
    
    #Читает файл с покупками, парсит валидные строки в словари.
    #Пропускает строки с ошибками.
    purchases = []

    with open(path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:  # пропускаем пустые строки
                continue

            # Разделяем строку по точке с запятой
            parts = line.split(';')

            # Проверяем, что в строке ровно 5 полей
            if len(parts) != 5:
                continue

            date_str, category, name, price_str, qty_str = parts

            # Очищаем поля от лишних пробелов
            date_str = date_str.strip()
            category = category.strip()
            name = name.strip()
            price_str = price_str.strip()
            qty_str = qty_str.strip()

            # Проверяем, что дата имеет правильный формат
            if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
                continue

                # Пытаемся преобразовать цену и количество
                try:
                    price = float(price_str) if price_str else 0.0
                    quantity = float(qty_str) if qty_str else 0.0

                    # Проверяем, что цена и количество неотрицательные
                    if price < 0 or quantity <= 0:
                        continue

                    # Вычисляем общую стоимость
                    total = price * quantity

                    purchases.append({
                        'date': date_str,
                        'category': category,
                        'name': name,
                        'price': price,
                        'quantity': quantity,
                        'total': total
                    })

                except (ValueError, TypeError):
                    # Если не удалось преобразовать в числа, пропускаем строку
                    continue

            return purchases"""

import csv
from typing import List, Dict, Any


def read_purchases(path: str) -> List[Dict[str, Any]]:
    """
    Читает файл с покупками, парсит валидные строки в словари.
    Пропускает строки с ошибками.
    """
    purchases = []

    with open(path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:  # пропускаем пустые строки
                continue

            # Разделяем строку по точке с запятой
            parts = line.split(';')

            # Проверяем, что в строке ровно 5 полей
            if len(parts) != 5:
                continue

            date_str, category, name, price_str, qty_str = parts

            # Очищаем поля от лишних пробелов
            date_str = date_str.strip()
            category = category.strip()
            name = name.strip()
            price_str = price_str.strip()
            qty_str = qty_str.strip()

            # Проверяем, что дата имеет правильный формат
            if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
                continue

            # Пытаемся преобразовать цену и количество
            try:
                price = float(price_str) if price_str else 0.0
                quantity = float(qty_str) if qty_str else 0.0

                # Проверяем, что цена и количество неотрицательные
                if price < 0 or quantity <= 0:
                    continue

                # Вычисляем общую стоимость
                total = price * quantity

                purchases.append({
                    'date': date_str,
                    'category': category,
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                    'total': total
                })

            except (ValueError, TypeError):
                # Если не удалось преобразовать в числа, пропускаем строку
                continue

    return purchases


def count_errors(path: str) -> int:
    """
    Возвращает количество строк с ошибками в файле.
    """
    total_lines = 0
    valid_lines = 0

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:  # пустые строки считаем ошибками
                total_lines += 1
                continue

            total_lines += 1

            parts = line.split(';')
            if len(parts) != 5:
                continue

            date_str, category, name, price_str, qty_str = parts

            # Очищаем поля
            date_str = date_str.strip()
            price_str = price_str.strip()
            qty_str = qty_str.strip()

            # Проверяем формат даты
            if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
                continue

            # Проверяем, что цена и количество можно преобразовать в числа
            try:
                price = float(price_str) if price_str else 0.0
                quantity = float(qty_str) if qty_str else 0.0

                if price < 0 or quantity <= 0:
                    continue

                valid_lines += 1

            except (ValueError, TypeError):
                continue

    return total_lines - valid_lines


def total_spent(purchases: List[Dict]) -> float:
    """
    Возвращает общую сумму всех покупок.
    """
    return sum(purchase['total'] for purchase in purchases)


def spent_by_category(purchases: List[Dict]) -> Dict[str, float]:
    """
    Возвращает словарь с суммами трат по категориям.
    """
    result = {}
    for purchase in purchases:
        category = purchase['category']
        result[category] = result.get(category, 0) + purchase['total']
    return result


def top_n_expensive(purchases: List[Dict], n: int = 3) -> List[Dict]:
    """
    Возвращает топ-N самых дорогих покупок.
    """
    # Сортируем по убыванию общей стоимости
    sorted_purchases = sorted(purchases, key=lambda x: x['total'], reverse=True)
    return sorted_purchases[:n]


def write_report(purchases: List[Dict], errors: int, out_path: str) -> None:
    """
    Сохраняет отчет в файл.
    """
    with open(out_path, 'w', encoding='utf-8') as file:
        file.write("=== ОТЧЕТ ПО ПОКУПКАМ ===\n\n")

        file.write(f"Всего строк обработано: {len(purchases) + errors}\n")
        file.write(f"Валидных покупок: {len(purchases)}\n")
        file.write(f"Строк с ошибками: {errors}\n\n")

        file.write(f"Общая сумма покупок: {total_spent(purchases):.2f} EUR\n\n")

        file.write("Расходы по категориям:\n")
        file.write("-" * 30 + "\n")
        category_totals = spent_by_category(purchases)
        for category, total in sorted(category_totals.items()):
            file.write(f"{category:15} {total:8.2f} EUR\n")

        file.write("\n" + "=" * 50 + "\n\n")

        file.write("Топ-3 самых дорогих покупок:\n")
        file.write("-" * 50 + "\n")
        top_purchases = top_n_expensive(purchases, 3)
        for i, purchase in enumerate(top_purchases, 1):
            file.write(f"{i}. {purchase['name']:20} "
                       f"{purchase['date']} "
                       f"{purchase['category']:15} "
                       f"{purchase['price']:6.2f} EUR × "
                       f"{purchase['quantity']:3} = "
                       f"{purchase['total']:6.2f} EUR\n")

        file.write("\n" + "=" * 50 + "\n")
        file.write("Отчет сгенерирован успешно!")




