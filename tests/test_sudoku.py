import unittest
from src.lab3.sudoku import (
    group, get_row, get_col, get_block,
    find_empty_positions, find_possible_values,
    solve, check_solution, generate_sudoku,
    read_sudoku
)

class TestSudoku(unittest.TestCase):
    
    def test_group(self):
        self.assertEqual(group([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(group([1, 2, 3, 4, 5, 6, 7, 8, 9], 3),
                         [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_get_row(self):
        grid = [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
        self.assertEqual(get_row(grid, (0, 0)), ['1', '2', '.'])
        self.assertEqual(get_row(grid, (1, 0)), ['4', '5', '6'])
        self.assertEqual(get_row(grid, (2, 0)), ['7', '8', '9'])

    def test_get_col(self):
        grid = [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
        self.assertEqual(get_col(grid, (0, 0)), ['1', '4', '7'])
        self.assertEqual(get_col(grid, (0, 1)), ['2', '5', '8'])
        self.assertEqual(get_col(grid, (0, 2)), ['.', '6', '9'])

    def test_get_block(self):
        grid = read_sudoku('puzzle1.txt')
        self.assertEqual(get_block(grid, (0, 1)), 
                         ['5', '3', '.', '6', '.', '.', '.', '9', '8'])
        self.assertEqual(get_block(grid, (4, 7)), 
                         ['.', '.', '3', '.', '.', '1', '.', '.', '6'])
        self.assertEqual(get_block(grid, (8, 8)), 
                         ['2', '8', '.', '.', '.', '5', '.', '7', '9'])

    def test_find_empty_positions(self):
        grid = [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
        self.assertEqual(find_empty_positions(grid), (0, 2))
        grid = [['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']]
        self.assertEqual(find_empty_positions(grid), (1, 1))
        grid = [['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']]
        self.assertEqual(find_empty_positions(grid), (2, 0))
        grid = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        self.assertIsNone(find_empty_positions(grid))

    def test_find_possible_values(self):
        grid = read_sudoku('puzzle1.txt')
        self.assertEqual(set(find_possible_values(grid, (0, 2))), {'1', '2', '4'})
        self.assertEqual(set(find_possible_values(grid, (4, 7))), {'2', '5', '9'})

    def test_solve(self):
        grid = read_sudoku('puzzle1.txt')
        solution = solve(grid)
        self.assertTrue(check_solution(solution))
        
        grid = read_sudoku('puzzle2.txt')
        solution = solve(grid)
        self.assertTrue(check_solution(solution))
        
        grid = read_sudoku('puzzle3.txt')
        solution = solve(grid)
        self.assertTrue(check_solution(solution))

    def test_check_solution(self):
        grid = read_sudoku('puzzle1.txt')
        solution = solve(grid)
        self.assertTrue(check_solution(solution))
        
        # Неправильное решение
        bad_solution = [['5' for _ in range(9)] for _ in range(9)]
        self.assertFalse(check_solution(bad_solution))

    def test_generate_sudoku(self):
        grid = generate_sudoku(40)
        empty_count = sum(1 for row in grid for e in row if e == '.')
        self.assertEqual(empty_count, 41)
        solution = solve(grid)
        self.assertTrue(check_solution(solution))

if __name__ == '__main__':
    unittest.main()
