import unittest
import io
import sys
from src.lab4.age_grouper import Person, AgeGroup, AgeGrouper

class TestPerson(unittest.TestCase):
    def test_person_creation(self):
        p = Person("Иванов Иван", 25)
        self.assertEqual(p.full_name, "Иванов Иван")
        self.assertEqual(p.age, 25)
    
    def test_person_repr(self):
        p = Person("Иванов Иван", 25)
        self.assertEqual(repr(p), "Иванов Иван (25)")


class TestAgeGroup(unittest.TestCase):
    def test_group_creation(self):
        group = AgeGroup(18, 25)
        self.assertEqual(group.min_age, 18)
        self.assertEqual(group.max_age, 25)
        self.assertEqual(len(group.persons), 0)
    
    def test_is_in_group(self):
        group = AgeGroup(18, 25)
        self.assertTrue(group.is_in_group(18))
        self.assertTrue(group.is_in_group(20))
        self.assertTrue(group.is_in_group(25))
        self.assertFalse(group.is_in_group(17))
        self.assertFalse(group.is_in_group(26))
    
    def test_add_person(self):
        group = AgeGroup(18, 25)
        p = Person("Иванов Иван", 25)
        group.add_person(p)
        self.assertEqual(len(group.persons), 1)
        self.assertEqual(group.persons[0], p)
    
    def test_sort_persons(self):
        group = AgeGroup(18, 25)
        group.add_person(Person("А", 25))
        group.add_person(Person("Б", 20))
        group.add_person(Person("В", 25))
        group.sort_persons()
        # Должно быть: сначала возраст 25 (А и В в алфавитном порядке), потом 20
        self.assertEqual(group.persons[0].full_name, "А")
        self.assertEqual(group.persons[1].full_name, "В")
        self.assertEqual(group.persons[2].full_name, "Б")
    
    def test_get_range_str(self):
        self.assertEqual(AgeGroup(0, 18).get_range_str(), "0-18")
        self.assertEqual(AgeGroup(19, 25).get_range_str(), "19-25")
        self.assertEqual(AgeGroup(101, float('inf')).get_range_str(), "101+")


class TestAgeGrouper(unittest.TestCase):
    def test_create_groups(self):
        grouper = AgeGrouper([18, 25, 35, 45, 60, 80, 100])
        self.assertEqual(len(grouper.groups), 8)  # 7 границ = 8 групп
        
        # Проверяем диапазоны
        ranges = [g.get_range_str() for g in grouper.groups]
        expected = ["0-18", "19-25", "26-35", "36-45", "46-60", "61-80", "81-100", "101+"]
        self.assertEqual(ranges, expected)
    
    def test_create_groups_empty(self):
        grouper = AgeGrouper([])
        self.assertEqual(len(grouper.groups), 1)
        self.assertEqual(grouper.groups[0].get_range_str(), "0+")
    
    def test_add_person(self):
        grouper = AgeGrouper([18, 25, 35])
        grouper.add_person("Иванов Иван", 20)
        grouper.add_person("Петров Петр", 30)
        grouper.add_person("Сидоров Сидор", 40)
        
        groups = grouper.get_sorted_groups()
        self.assertEqual(len(groups), 3)
    
    def test_sorting_order(self):
        grouper = AgeGrouper([18, 35, 60])
        grouper.add_person("Молодой", 15)
        grouper.add_person("Средний", 40)
        grouper.add_person("Пожилой", 70)
        
        groups = grouper.get_sorted_groups()
        # Должно быть от старших к младшим
        self.assertEqual(groups[0].min_age, 61)  # 61+
        self.assertEqual(groups[1].min_age, 36)  # 36-60
        self.assertEqual(groups[2].min_age, 0)   # 0-18
    
    def test_example_from_task(self):
        # Тест из примера в задании
        grouper = AgeGrouper([18, 25, 35, 45, 60, 80, 100])
        
        data = [
            ("Кошельков Захар Брониславович", 105),
            ("Дьячков Нисон Иринеевич", 88),
            ("Иванов Варлам Якунович", 88),
            ("Старостин Ростислав Ермолаевич", 50),
            ("Ярилова Розалия Трофимовна", 29),
            ("Соколов Андрей Сергеевич", 15),
            ("Егоров Алан Петрович", 7),
        ]
        
        for name, age in data:
            grouper.add_person(name, age)
        
        groups = grouper.get_sorted_groups()
        
        # Проверяем количество групп с людьми
        self.assertEqual(len(groups), 5)
        
        # Проверяем первую группу (101+)
        self.assertEqual(groups[0].get_range_str(), "101+")
        self.assertEqual(len(groups[0].persons), 1)
        self.assertEqual(groups[0].persons[0].full_name, "Кошельков Захар Брониславович")
        
        # Проверяем вторую группу (81-100)
        self.assertEqual(groups[1].get_range_str(), "81-100")
        self.assertEqual(len(groups[1].persons), 2)
        self.assertEqual(groups[1].persons[0].full_name, "Дьячков Нисон Иринеевич")
        self.assertEqual(groups[1].persons[1].full_name, "Иванов Варлам Якунович")


if __name__ == '__main__':
    unittest.main()
