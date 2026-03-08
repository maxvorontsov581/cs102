import re
from collections import Counter
from typing import List, Tuple, Dict, Optional


def parse_order_line(line: str) -> Optional[Tuple[str, str, str, str, str, str]]:
    """Разбирает строку заказа на поля"""
    parts = line.strip().split(';')
    if len(parts) != 6:
        return None
    
    order_id, products, name, address, phone, priority = parts
    
    # Проверяем номер заказа (5 цифр)
    if not re.match(r'^\d{5}$', order_id):
        return None
    
    # Проверяем приоритет
    if priority not in ('MAX', 'MIDDLE', 'LOW'):
        return None
    
    return order_id, products.strip(), name.strip(), address.strip(), phone.strip(), priority.strip()


def validate_phone(phone: str) -> bool:
    """Проверяет формат номера телефона +x-xxx-xxx-xx-xx"""
    return bool(re.match(r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$', phone))


def validate_address(address: str) -> bool:
    """Проверяет, что адрес не пустой"""
    return bool(address.strip())


def count_products(products: str) -> str:
    """Подсчитывает количество каждого продукта и форматирует"""
    items = [item.strip() for item in products.split(',')]
    counter = Counter(items)
    
    result = []
    for product, count in sorted(counter.items()):
        if count == 1:
            result.append(product)
        else:
            result.append(f"{product} x{count}")
    
    return ', '.join(result)


def format_address(address: str) -> str:
    """Форматирует адрес: Регион. Город. Улица"""
    if not address:
        return ''
    
    parts = address.split('.')
    if len(parts) >= 3:
        return '. '.join(parts[1:])  # убираем страну
    return address


def process_orders(filename: str = 'orders.txt') -> None:
    """Главная функция обработки заказов"""
    valid_orders = []
    invalid_orders = []
    
    # Читаем файл
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return
    
    # Обрабатываем каждую строку
    for line_num, line in enumerate(lines, 1):
        parsed = parse_order_line(line)
        if not parsed:
            continue
            
        order_id, products, name, address, phone, priority = parsed
        
        errors = []
        
        # Проверяем адрес
        if not validate_address(address):
            errors.append((1, 'no data'))
        
        # Проверяем телефон
        if not validate_phone(phone):
            errors.append((2, phone))
        
        if errors:
            # Сохраняем ошибки
            for error_type, error_value in errors:
                invalid_orders.append(f"{order_id};{error_type};{error_value}")
        else:
            # Валидный заказ
            valid_orders.append({
                'order_id': order_id,
                'products': count_products(products),
                'name': name,
                'address': format_address(address),
                'phone': phone,
                'priority': priority,
                'country': parsed[3].split('.')[0] if parsed[3] else ''
            })
    
    # Сортируем валидные заказы: сначала по стране, потом по приоритету
    priority_order = {'MAX': 0, 'MIDDLE': 1, 'LOW': 2}
    
    valid_orders.sort(key=lambda x: (
        x['country'],
        priority_order[x['priority']]
    ))
    
    # Сохраняем валидные заказы
    with open('order_country.txt', 'w', encoding='utf-8') as f:
        for order in valid_orders:
            f.write(f"{order['order_id']};"
                   f"{order['products']};"
                   f"{order['name']};"
                   f"{order['address']};"
                   f"{order['phone']};"
                   f"{order['priority']}\n")
    
    # Сохраняем невалидные заказы
    with open('non_valid_orders.txt', 'w', encoding='utf-8') as f:
        for error_line in invalid_orders:
            f.write(error_line + '\n')
    
    print(f"Обработано {len(lines)} строк")
    print(f"Валидных заказов: {len(valid_orders)}")
    print(f"Ошибок: {len(invalid_orders)}")
    print("Файлы order_country.txt и non_valid_orders.txt созданы")


if __name__ == "__main__":
    process_orders()


