import pathlib
import random
from typing import List, Tuple, Optional, Set, Union

def group(values: List, n: int) -> List[List]:
    return [values[i:i+n] for i in range(0, len(values), n)]

def create_grid(puzzle: str) -> List[List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    return group(digits, 9)

def read_sudoku(path: Union[str, pathlib.Path]) -> List[List[str]]:
    path = pathlib.Path(path)
    with open(path) as f:
        puzzle = f.read()
    return create_grid(puzzle)

def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    return grid[pos[0]]

def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    return [grid[i][pos[1]] for i in range(len(grid))]

def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    row, col = pos
    block_row = (row // 3) * 3
    block_col = (col // 3) * 3
    result = []
    for i in range(3):
        for j in range(3):
            result.append(grid[block_row + i][block_col + j])
    return result

def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                return (i, j)
    return None

def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    values = set(str(i) for i in range(1, 10))
    row_values = set(get_row(grid, pos))
    col_values = set(get_col(grid, pos))
    block_values = set(get_block(grid, pos))
    return values - row_values - col_values - block_values

def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    pos = find_empty_positions(grid)
    if not pos:
        return [row[:] for row in grid]
    
    for value in find_possible_values(grid, pos):
        grid[pos[0]][pos[1]] = value
        if solve(grid):
            return grid
        grid[pos[0]][pos[1]] = '.'
    
    return None

def check_solution(solution: List[List[str]]) -> bool:
    if not solution:
        return False
    
    for i in range(9):
        row = set(solution[i])
        if row != set(str(j) for j in range(1, 10)):
            return False
    
    for j in range(9):
        col = set(solution[i][j] for i in range(9))
        if col != set(str(j) for j in range(1, 10)):
            return False
    
    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            block = set()
            for i in range(3):
                for j in range(3):
                    block.add(solution[block_row + i][block_col + j])
            if block != set(str(j) for j in range(1, 10)):
                return False
    
    return True

def generate_sudoku(N: int) -> List[List[str]]:
    empty = [['.' for _ in range(9)] for _ in range(9)]
    solved = solve(empty)
    
    if not solved:
        return empty
    
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    
    for i, j in positions[:81 - N]:
        solved[i][j] = '.'
    
    return solved

def display(grid: List[List[str]]) -> None:
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end=' ')
            if j in [2, 5]:
                print('|', end=' ')
        print()
        if i in [2, 5]:
            print('------+-------+------')

if __name__ == "__main__":
    for filename in ("puzzle1.txt", "puzzle2.txt", "puzzle3.txt"):
        grid = read_sudoku(filename)
        print(f"\n{filename}:")
        display(grid)
        solution = solve(grid)
        if solution and check_solution(solution):
            print("✓ Решение найдено")
            display(solution)
        else:
            print("✗ Решение не найдено")
