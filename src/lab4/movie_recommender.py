import sys
from typing import List, Dict, Set, Tuple, Optional

class Movie:
    """Класс фильма"""
    def __init__(self, movie_id: int, title: str):
        self.id = movie_id
        self.title = title
    
    def __eq__(self, other):
        if isinstance(other, Movie):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)
    
    def __repr__(self):
        return f"Movie({self.id}, {self.title})"


class UserHistory:
    """История просмотров пользователя"""
    def __init__(self, movies: List[int]):
        self.movies = movies
        self.movie_set = set(movies)
    
    def get_movies(self) -> List[int]:
        return self.movies
    
    def get_set(self) -> Set[int]:
        return self.movie_set
    
    def __len__(self):
        return len(self.movies)


class MovieDatabase:
    """База данных фильмов"""
    def __init__(self, movies_file: str):
        self.movies: Dict[int, Movie] = {}
        self._load_movies(movies_file)
    
    def _load_movies(self, filename: str):
        """Загрузка фильмов из файла"""
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',', 1)
                if len(parts) == 2:
                    movie_id = int(parts[0].strip())
                    title = parts[1].strip()
                    self.movies[movie_id] = Movie(movie_id, title)
    
    def get_movie(self, movie_id: int) -> Optional[Movie]:
        return self.movies.get(movie_id)
    
    def get_title(self, movie_id: int) -> str:
        movie = self.get_movie(movie_id)
        return movie.title if movie else f"Unknown({movie_id})"


class HistoryDatabase:
    """База данных истории просмотров"""
    def __init__(self, history_file: str):
        self.histories: List[UserHistory] = []
        self._load_histories(history_file)
    
    def _load_histories(self, filename: str):
        """Загрузка историй из файла"""
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                movies = [int(x.strip()) for x in line.split(',') if x.strip()]
                self.histories.append(UserHistory(movies))
    
    def get_all_histories(self) -> List[UserHistory]:
        return self.histories


class Recommender:
    """Система рекомендаций"""
    def __init__(self, movies_file: str, history_file: str):
        self.movies_db = MovieDatabase(movies_file)
        self.history_db = HistoryDatabase(history_file)
    
    def _calculate_similarity(self, user_set: Set[int], history_set: Set[int]) -> float:
        """Вычисляет долю общих фильмов"""
        if not user_set:
            return 0.0
        common = user_set & history_set
        return len(common) / len(user_set)
    
    def _filter_users(self, user_movies: List[int], min_similarity: float = 0.5) -> List[UserHistory]:
        """Отбирает пользователей с достаточным сходством"""
        user_set = set(user_movies)
        similar_users = []
        
        for history in self.history_db.get_all_histories():
            similarity = self._calculate_similarity(user_set, history.get_set())
            if similarity >= min_similarity:
                similar_users.append(history)
        
        return similar_users
    
    def _count_movie_frequency(self, users: List[UserHistory], exclude_set: Set[int]) -> Dict[int, int]:
        """Подсчитывает частоту просмотров фильмов"""
        freq = {}
        for user in users:
            for movie_id in user.get_movies():
                if movie_id not in exclude_set:
                    freq[movie_id] = freq.get(movie_id, 0) + 1
        return freq
    
    def recommend(self, user_input: str, similarity_threshold: float = 0.5) -> Optional[str]:
        """
        Рекомендует фильм на основе ввода пользователя
        Формат ввода: "2,4" (список ID через запятую)
        """
        try:
            # Парсим ввод пользователя
            user_movies = [int(x.strip()) for x in user_input.split(',') if x.strip()]
            user_set = set(user_movies)
            
            # Шаг 1: Выбираем пользователей с >= половиной общих фильмов
            similar_users = self._filter_users(user_movies, similarity_threshold)
            
            if not similar_users:
                return None
            
            # Шаг 2: Исключаем уже просмотренные фильмы
            # Шаг 3: Подсчитываем частоту и выбираем максимум
            freq = self._count_movie_frequency(similar_users, user_set)
            
            if not freq:
                return None
            
            # Выбираем фильм с максимальной частотой
            best_movie_id = max(freq.items(), key=lambda x: x[1])[0]
            
            return self.movies_db.get_title(best_movie_id)
            
        except Exception as e:
            print(f"Ошибка: {e}", file=sys.stderr)
            return None
    
    def recommend_with_weights(self, user_input: str) -> Optional[str]:
        """
        Усложненная версия: учитывает вес в зависимости от доли общих фильмов
        """
        try:
            user_movies = [int(x.strip()) for x in user_input.split(',') if x.strip()]
            user_set = set(user_movies)
            
            # Словарь для взвешенных частот
            weighted_freq = {}
            
            for history in self.history_db.get_all_histories():
                similarity = self._calculate_similarity(user_set, history.get_set())
                
                # Учитываем только пользователей с similarity > 0
                if similarity > 0:
                    for movie_id in history.get_movies():
                        if movie_id not in user_set:
                            # Добавляем с весом similarity
                            weighted_freq[movie_id] = weighted_freq.get(movie_id, 0) + similarity
            
            if not weighted_freq:
                return None
            
            best_movie_id = max(weighted_freq.items(), key=lambda x: x[1])[0]
            return self.movies_db.get_title(best_movie_id)
            
        except Exception as e:
            print(f"Ошибка: {e}", file=sys.stderr)
            return None


def main():
    """Основная функция для запуска из командной строки"""
    if len(sys.argv) > 1:
        # Если передан аргумент - используем упрощенный режим
        movies_file = sys.argv[1] if len(sys.argv) > 1 else "movies.txt"
        history_file = sys.argv[2] if len(sys.argv) > 2 else "history.txt"
    else:
        movies_file = "movies.txt"
        history_file = "history.txt"
    
    recommender = Recommender(movies_file, history_file)
    
    # Читаем ввод пользователя
    user_input = sys.stdin.readline().strip()
    
    # Получаем рекомендацию
    recommendation = recommender.recommend(user_input)
    
    if recommendation:
        print(recommendation)
    else:
        print("Нет подходящей рекомендации")


if __name__ == "__main__":
    main()
