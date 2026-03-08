import unittest
import tempfile
import os
from src.lab4.movie_recommender import Movie, UserHistory, MovieDatabase, HistoryDatabase, Recommender

class TestMovie(unittest.TestCase):
    def test_movie_creation(self):
        movie = Movie(1, "Тестовый фильм")
        self.assertEqual(movie.id, 1)
        self.assertEqual(movie.title, "Тестовый фильм")
    
    def test_movie_equality(self):
        m1 = Movie(1, "Фильм 1")
        m2 = Movie(1, "Фильм 1")
        m3 = Movie(2, "Фильм 2")
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)


class TestUserHistory(unittest.TestCase):
    def test_history_creation(self):
        history = UserHistory([1, 2, 3])
        self.assertEqual(history.get_movies(), [1, 2, 3])
        self.assertEqual(history.get_set(), {1, 2, 3})
    
    def test_history_len(self):
        history = UserHistory([1, 2, 3, 4])
        self.assertEqual(len(history), 4)


class TestMovieDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        self.temp_file.write("1,Фильм 1\n2,Фильм 2\n3,Фильм 3\n")
        self.temp_file.close()
        self.db = MovieDatabase(self.temp_file.name)
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_load_movies(self):
        self.assertEqual(len(self.db.movies), 3)
        self.assertIsNotNone(self.db.get_movie(1))
        self.assertEqual(self.db.get_title(1), "Фильм 1")
        self.assertEqual(self.db.get_title(2), "Фильм 2")
        self.assertEqual(self.db.get_title(3), "Фильм 3")
        self.assertEqual(self.db.get_title(999), "Unknown(999)")


class TestHistoryDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        self.temp_file.write("1,2,3\n4,5,6\n7,8,9,10\n")
        self.temp_file.close()
        self.db = HistoryDatabase(self.temp_file.name)
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_load_histories(self):
        histories = self.db.get_all_histories()
        self.assertEqual(len(histories), 3)
        self.assertEqual(histories[0].get_movies(), [1, 2, 3])
        self.assertEqual(histories[1].get_movies(), [4, 5, 6])
        self.assertEqual(histories[2].get_movies(), [7, 8, 9, 10])


class TestRecommender(unittest.TestCase):
    def setUp(self):
        # Создаем временные файлы для тестов
        self.movies_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        self.movies_file.write("1,Мстители: Финал\n2,Хатико\n3,Дюна\n4,Унесенные призраками\n")
        self.movies_file.close()
        
        self.history_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        self.history_file.write("2,1,3\n1,4,3\n2,2,2,2,2,3\n")
        self.history_file.close()
        
        self.recommender = Recommender(self.movies_file.name, self.history_file.name)
    
    def tearDown(self):
        os.unlink(self.movies_file.name)
        os.unlink(self.history_file.name)
    
    def test_recommend_basic(self):
        # Тест из примера: 2,4 -> Дюна
        result = self.recommender.recommend("2,4")
        self.assertEqual(result, "Дюна")
    
    def test_recommend_empty_input(self):
        result = self.recommender.recommend("")
        self.assertIsNone(result)
    
    def test_recommend_no_match(self):
        result = self.recommender.recommend("999")
        self.assertIsNone(result)
    
    def test_recommend_with_weights(self):
        result = self.recommender.recommend_with_weights("2,4")
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
