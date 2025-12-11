'''file = open('purchases.txt')
content = file.readline()
print(content)
#file.close()
content = content.split(';')
print(content)
meal = {
    'date' : content[0],
    'category' : content[1],
    'name' : content[2],
    'price': content[3],
    'quantity' : content[4]
}
print(meal)
for i in file.readlines():
    i = i.split(';')
    meal = {
        'date': i[0],
        'category': i[1],
        'name': i[2],
        'price': i[3],
        'quantity': i[4]
    }
    print(meal)'''

import sys
from purchase_analyzer import (
    read_purchases,
    count_errors,
    total_spent,
    spent_by_category,
    top_n_expensive,
    write_report
)


def main():
    input_file = "purchases.txt"
    output_file = "report.txt"

    print(f"Анализ файла {input_file}...")

    try:
        # Читаем валидные покупки
        purchases = read_purchases(input_file)
        print(f"Найдено валидных покупок: {len(purchases)}")

        # Считаем ошибки
        errors = count_errors(input_file)
        print(f"Найдено строк с ошибками: {errors}")

        # Выводим общую сумму
        total = total_spent(purchases)
        print(f"Общая сумма покупок: {total:.2f} EUR")

        # Выводим расходы по категориям
        print("\nРасходы по категориям:")
        categories = spent_by_category(purchases)
        for category, amount in sorted(categories.items()):
            print(f"  {category:15} {amount:8.2f} EUR")

        # Выводим топ-3 покупки
        print("\nТоп-3 самых дорогих покупок:")
        top_purchases = top_n_expensive(purchases, 3)
        for i, purchase in enumerate(top_purchases, 1):
            print(f"{i}. {purchase['name']:20} {purchase['total']:6.2f} EUR")

        # Сохраняем отчет в файл
        write_report(purchases, errors, output_file)
        print(f"\nОтчет сохранен в файл {output_file}")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден!")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()