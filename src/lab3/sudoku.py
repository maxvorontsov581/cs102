import pathlib
import random
import typing as tp
from typing import Union, Optional, List, Tuple, Set, Any, TypeVar

T = TypeVar('T')

def group(values: List[T], n: int) -> List[List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    """
    return [values[i:i + n] for i in range(0, len(values), n)]

def create_grid(puzzle: str) -> List[List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid

def read_sudoku(path: Union[str, pathlib.Path]) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)

def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos """
    row, _ = pos
    return grid[row]

def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos """
    _, col = pos
    return [grid[row][col] for row in range(len(grid))]

def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos """
    row, col = pos
    block_row = (row // 3) * 3
    block_col = (col // 3) * 3
    return [grid[block_row + i][block_col + j] for i in range(3) for j in range(3)]

def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле """
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '.':
                return (row, col)
    return None

def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество всех возможных значения для указанной позиции """
    all_values = set(str(i) for i in range(1, 10))
    row_values = set(get_row(grid, pos))
    col_values = set(get_col(grid, pos))
    block_values = set(get_block(grid, pos))
    return all_values - row_values - col_values - block_values

def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Поиск решения для указанного пазла """
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    
    for value in find_possible_values(grid, pos):
        row, col = pos
        grid[row][col] = value
        solution = solve(grid)
        if solution:
            return solution
        grid[row][col] = '.'
    
    return None

def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # Проверка строк
    for row in range(9):
        row_values = set(get_row(solution, (row, 0)))
        if row_values != set(str(i) for i in range(1, 10)):
            return False
    
    # Проверка столбцов
    for col in range(9):
        col_values = set(get_col(solution, (0, col)))
        if col_values != set(str(i) for i in range(1, 10)):
            return False
    
    # Проверка блоков 3x3
    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            block_values = set(get_block(solution, (block_row, block_col)))
            if block_values != set(str(i) for i in range(1, 10)):
                return False
    
    return True

def generate_sudoku(N: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов """
    empty_grid = [['.' for _ in range(9)] for _ in range(9)]
    solved_grid = solve(empty_grid)
    
    if not solved_grid:
        return empty_grid
    
    positions = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(positions)
    
    for row, col in positions[:81 - N]:
        solved_grid[row][col] = '.'
    
    return solved_grid

def display(grid: List[List[str]]) -> None:
    """ Вывод Судоку """
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            print(cell, end=' ')
            if j in [2, 5]:
                print('|', end=' ')
        print()
        if i in [2, 5]:
            print('------+-------+------')

if __name__ == "__main__":
    for filename in ("puzzle1.txt", "puzzle2.txt", "puzzle3.txt"):
        grid = read_sudoku(filename)
        print(f"\nСудоку из файла {filename}:")
        display(grid)
        solution = solve(grid)
        if solution and check_solution(solution):
            print("\nРешение:")
            display(solution)
            print("✓ Решение верно!")
        else:
            print("✗ Решение не найдено или неверно")
