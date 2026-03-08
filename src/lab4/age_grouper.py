import sys
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

class Person:
    """Класс респондента"""
    def __init__(self, full_name: str, age: int):
        self.full_name = full_name
        self.age = age
    
    def __repr__(self):
        return f"{self.full_name} ({self.age})"


class AgeGroup:
    """Класс возрастной группы"""
    def __init__(self, min_age: int, max_age: int):
        self.min_age = min_age
        self.max_age = max_age
        self.persons: List[Person] = []
    
    def add_person(self, person: Person):
        """Добавить человека в группу"""
        self.persons.append(person)
    
    def is_in_group(self, age: int) -> bool:
        """Проверяет, попадает ли возраст в группу"""
        return self.min_age <= age <= self.max_age
    
    def sort_persons(self):
        """Сортирует людей по возрасту (убывание) и по ФИО (возрастание при равном возрасте)"""
        self.persons.sort(key=lambda p: (-p.age, p.full_name))
    
    def has_persons(self) -> bool:
        """Есть ли люди в группе"""
        return len(self.persons) > 0
    
    def get_range_str(self) -> str:
        """Возвращает строковое представление диапазона группы"""
        if self.max_age == float('inf'):
            return f"{self.min_age}+"
        elif self.min_age == 0:
            return f"0-{self.max_age}"
        else:
            return f"{self.min_age}-{self.max_age}"
    
    def __repr__(self):
        return f"AgeGroup({self.min_age}-{self.max_age})"


class AgeGrouper:
    """Класс для разбивки по возрастным группам"""
    
    def __init__(self, boundaries: List[int]):
        """
        Инициализация с границами групп
        Пример: [18, 25, 35, 45, 60, 80, 100]
        """
        self.groups: List[AgeGroup] = []
        self._create_groups(boundaries)
    
    def _create_groups(self, boundaries: List[int]):
        """Создает возрастные группы на основе границ"""
        if not boundaries:
            # Если границ нет - одна группа от 0 до бесконечности
            self.groups.append(AgeGroup(0, float('inf')))
            return
        
        # Сортируем границы
        boundaries.sort()
        
        # Первая группа: 0 до первой границы
        self.groups.append(AgeGroup(0, boundaries[0]))
        
        # Промежуточные группы
        for i in range(len(boundaries) - 1):
            self.groups.append(AgeGroup(boundaries[i] + 1, boundaries[i + 1]))
        
        # Последняя группа: от последней границы+1 до бесконечности
        self.groups.append(AgeGroup(boundaries[-1] + 1, float('inf')))
    
    def add_person(self, full_name: str, age: int):
        """Добавляет человека в соответствующую возрастную группу"""
        for group in self.groups:
            if group.is_in_group(age):
                group.add_person(Person(full_name, age))
                return
        
        # Если ни одна группа не подошла (например, возраст > 123)
        # Создаем специальную группу "остальные"
        if not hasattr(self, 'other_group'):
            self.other_group = AgeGroup(0, float('inf'))
        self.other_group.add_person(Person(full_name, age))
    
    def get_sorted_groups(self) -> List[AgeGroup]:
        """Возвращает группы с людьми, отсортированные по убыванию возраста"""
        # Сортируем все группы по убыванию минимального возраста
        groups_with_people = [g for g in self.groups if g.has_persons()]
        
        # Добавляем "другие" если есть
        if hasattr(self, 'other_group') and self.other_group.has_persons():
            groups_with_people.append(self.other_group)
        
        # Сортируем по убыванию минимального возраста
        groups_with_people.sort(key=lambda g: -g.min_age)
        
        # Сортируем людей внутри каждой группы
        for group in groups_with_people:
            group.sort_persons()
        
        return groups_with_people
    
    def print_groups(self, output=sys.stdout):
        """Выводит группы в формате, требуемом в задании"""
        groups = self.get_sorted_groups()
        
        for group in groups:
            range_str = group.get_range_str()
            persons_str = ", ".join(str(p) for p in group.persons)
            print(f"{range_str}: {persons_str}", file=output)


def parse_args() -> List[int]:
    """Парсит аргументы командной строки"""
    if len(sys.argv) < 2:
        return []
    
    try:
        return [int(arg) for arg in sys.argv[1:]]
    except ValueError:
        print("Ошибка: аргументы должны быть числами", file=sys.stderr)
        sys.exit(1)


def main():
    """Основная функция"""
    # Получаем границы групп из аргументов
    boundaries = parse_args()
    
    # Создаем группировщик
    grouper = AgeGrouper(boundaries)
    
    # Читаем входные данные
    for line in sys.stdin:
        line = line.strip()
        if line == "END":
            break
        
        if not line:
            continue
        
        try:
            # Парсим строку: "ФИО,возраст"
            parts = line.rsplit(',', 1)
            if len(parts) != 2:
                continue
            
            full_name = parts[0].strip()
            age = int(parts[1].strip())
            
            grouper.add_person(full_name, age)
            
        except ValueError:
            # Пропускаем некорректные строки
            continue
    
    # Выводим результат
    grouper.print_groups()


if __name__ == "__main__":
    main()
