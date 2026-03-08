import pathlib
import random
from typing import List, Tuple, Optional, Union

def group(values: List, n: int) -> List[List]:
    return [values[i:i+n] for i in range(0, len(values), n)]

def read_sudoku(path: Union[str, pathlib.Path]) -> List[List[str]]:
    path = pathlib.Path(path)
    with open(path) as f:
        puzzle = f.read()
    digits = [c for c in puzzle if c in "123456789."]
    return group(digits, 9)

def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    return grid[pos[0]]

def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    return [grid[i][pos[1]] for i in range(9)]

def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    row, col = pos
    br, bc = (row // 3) * 3, (col // 3) * 3
    return [grid[br + i][bc + j] for i in range(3) for j in range(3)]

def find_empty(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    for i in range(9):
        for j in range(9):
            if grid[i][j] == '.':
                return (i, j)
    return None

def possible(grid: List[List[str]], pos: Tuple[int, int], num: str) -> bool:
    if num in get_row(grid, pos):
        return False
    if num in get_col(grid, pos):
        return False
    if num in get_block(grid, pos):
        return False
    return True

def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    pos = find_empty(grid)
    if not pos:
        return [row[:] for row in grid]
    
    for num in '123456789':
        if possible(grid, pos, num):
            grid[pos[0]][pos[1]] = num
            if solve(grid):
                return grid
            grid[pos[0]][pos[1]] = '.'
    
    return None

def check_solution(grid: List[List[str]]) -> bool:
    if not grid:
        return False
    
    for i in range(9):
        if set(grid[i]) != set('123456789'):
            return False
    
    for j in range(9):
        if set(grid[i][j] for i in range(9)) != set('123456789'):
            return False
    
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = [grid[br + i][bc + j] for i in range(3) for j in range(3)]
            if set(block) != set('123456789'):
                return False
    
    return True

def generate_sudoku(n: int) -> List[List[str]]:
    empty = [['.' for _ in range(9)] for _ in range(9)]
    full = solve(empty)
    if not full:
        return empty
    
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    
    for i, j in cells[:81 - n]:
        full[i][j] = '.'
    
    return full

def display(grid: List[List[str]]) -> None:
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end=' ')
            if j in (2, 5):
                print('|', end=' ')
        print()
        if i in (2, 5):
            print('------+-------+------')
