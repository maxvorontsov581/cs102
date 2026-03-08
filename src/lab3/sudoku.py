import pathlib
import random
import typing as tp


T = tp.TypeVar("T")


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1, 2, 3, 4], 2)
    [[1, 2], [3, 4]]
    >>> group([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i:i + n] for i in range(0, len(values), n)]


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла (из корня проекта) """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def display(grid: tp.List[tp.List[str]]) -> None:
    """ Красивый вывод судоку """
    size = len(grid)
    block_size = int(size ** 0.5)
    for r, row in enumerate(grid):
        line = ""
        for c, val in enumerate(row):
            line += val + " "
            if (c + 1) % block_size == 0 and c + 1 != size:
                line += "|"
        print(line.rstrip())
        if (r + 1) % block_size == 0 and r + 1 != size:
            print("-" * (size * 2 + block_size - 1))


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """ Возвращает все значения для номера строки, указанной в pos """
    row, _ = pos
    return grid[row]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos """
    _, col = pos
    return [grid[r][col] for r in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos """
    row, col = pos
    block_size = int(len(grid) ** 0.5)  # для 9x9 -> 3
    start_row = (row // block_size) * block_size
    start_col = (col // block_size) * block_size
    return [
        grid[r][c]
        for r in range(start_row, start_row + block_size)
        for c in range(start_col, start_col + block_size)
    ]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле """
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '.':
                return (r, c)
    return None
def find_empty(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    return find_empty_positions(grid)


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """ Вернуть множество всех возможных значений для указанной позиции """
    digits = set("123456789")
    row_vals = set(get_row(grid, pos))
    col_vals = set(get_col(grid, pos))
    block_vals = set(get_block(grid, pos))
    used = row_vals | col_vals | block_vals
    return digits - used


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Поиск решения для указанного пазла (backtracking) """
    empty = find_empty_positions(grid)
    if empty is None:
        # Нет свободных позиций — доска заполнена
        return grid

    row, col = empty
    for val in find_possible_values(grid, (row, col)):
        grid[row][col] = val
        result = solve(grid)
        if result is not None:
            return result
        grid[row][col] = '.'  # откат

    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    n = len(solution)
    digits = set("123456789")

    # строки
    for r in range(n):
        row = solution[r]
        if set(row) != digits:
            return False

    # столбцы
    for c in range(n):
        col = [solution[r][c] for r in range(n)]
        if set(col) != digits:
            return False

    # блоки
    block_size = int(n ** 0.5)
    for br in range(0, n, block_size):
        for bc in range(0, n, block_size):
            block = [
                solution[r][c]
                for r in range(br, br + block_size)
                for c in range(bc, bc + block_size)
            ]
            if set(block) != digits:
                return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """
    Генерация судоку, заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    # стартуем с пустой доски и получаем полное решение
    grid: tp.List[tp.List[str]] = [['.' for _ in range(9)] for _ in range(9)]
    full = solve(grid)
    if full is None:
        raise RuntimeError("Не удалось сгенерировать полное решение")

    puzzle = [row[:] for row in full]

    # ограничиваем N от 0 до 81
    N = max(0, min(81, N))
    to_remove = 81 - N

    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    for i in range(to_remove):
        r, c = cells[i]
        puzzle[r][c] = '.'

    return puzzle


if __name__ == "__main__":
    import time

    for filename in ("puzzle1.txt", "puzzle2.txt", "puzzle3.txt"):
        grid = read_sudoku(filename)
        print(f"Puzzle from {filename}:")
        display(grid)
        start = time.time()
        solution = solve(grid)
        end = time.time()
        print(f"Solved in {end - start:.4f} seconds")
        if solution is not None and check_solution(solution):
            print("Solution is correct")
            display(solution)
        else:
            print("Ooops")
        print()

