import unittest
import pathlib
from src.lab3.sudoku import (
    group, get_row, get_col, get_block, 
    find_empty_positions, find_possible_values,
    solve, check_solution, generate_sudoku,
    read_sudoku
)

class SudokuTestCase(unittest.TestCase):

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
        block_0_1 = get_block(grid, (0, 1))
        expected_0_1 = ['5', '3', '.', '6', '.', '.', '.', '9', '8']
        self.assertEqual(block_0_1, expected_0_1)

        block_4_7 = get_block(grid, (4, 7))
        expected_4_7 = ['.', '.', '3', '.', '.', '1', '.', '.', '6']
        self.assertEqual(block_4_7, expected_4_7)

        block_8_8 = get_block(grid, (8, 8))
        expected_8_8 = ['2', '8', '.', '.', '.', '5', '.', '7', '9']
        self.assertEqual(block_8_8, expected_8_8)

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
        values_pos_0_2 = find_possible_values(grid, (0, 2))
        self.assertEqual(set(values_pos_0_2), {'1', '2', '4'})
        values_pos_4_7 = find_possible_values(grid, (4, 7))
        self.assertEqual(set(values_pos_4_7), {'2', '5', '9'})

    def test_solve(self):
        grid = read_sudoku('puzzle1.txt')
        solution = solve(grid)
        expected_solution = [
            ['5', '3', '4', '6', '7', '8', '9', '1', '2'],
            ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
            ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
            ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
            ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
            ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
            ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
            ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
            ['3', '4', '5', '2', '8', '6', '1', '7', '9']
        ]
        self.assertEqual(solution, expected_solution)
        self.assertTrue(check_solution(solution))

    def test_check_solution(self):
        correct_solution = [
            ['5', '3', '4', '6', '7', '8', '9', '1', '2'],
            ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
            ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
            ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
            ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
            ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
            ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
            ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
            ['3', '4', '5', '2', '8', '6', '1', '7', '9']
        ]
        self.assertTrue(check_solution(correct_solution))
        
        incorrect_solution = [
            ['5', '5', '4', '6', '7', '8', '9', '1', '2'],
            ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
            ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
            ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
            ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
            ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
            ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
            ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
            ['3', '4', '5', '2', '8', '6', '1', '7', '9']
        ]
        self.assertFalse(check_solution(incorrect_solution))

    def test_generate_sudoku(self):
        grid_40 = generate_sudoku(40)
        empty_count = sum(1 for row in grid_40 for e in row if e == '.')
        self.assertEqual(empty_count, 41)
        solution = solve(grid_40)
        self.assertTrue(check_solution(solution))
        
        grid_1000 = generate_sudoku(1000)
        empty_count = sum(1 for row in grid_1000 for e in row if e == '.')
        self.assertEqual(empty_count, 0)
        solution = solve(grid_1000)
        self.assertTrue(check_solution(solution))
        
        grid_0 = generate_sudoku(0)
        empty_count = sum(1 for row in grid_0 for e in row if e == '.')
        self.assertEqual(empty_count, 81)
        solution = solve(grid_0)
        self.assertTrue(check_solution(solution))

if __name__ == '__main__':
    unittest.main()
