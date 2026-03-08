import unittest
from src.lab3.sudoku import (
    group, get_row, get_col, get_block,
    find_empty_positions, find_possible_values,
    solve, check_solution, generate_sudoku,
    read_sudoku
)

class TestSudoku(unittest.TestCase):
    
    def test_group(self):
        self.assertEqual(group([1,2,3,4], 2), [[1,2], [3,4]])
        self.assertEqual(group([1,2,3,4,5,6,7,8,9], 3), 
                         [[1,2,3], [4,5,6], [7,8,9]])
    
    def test_get_row(self):
        grid = [['1','2','.'], ['4','5','6'], ['7','8','9']]
        self.assertEqual(get_row(grid, (0,0)), ['1','2','.'])
        self.assertEqual(get_row(grid, (1,0)), ['4','5','6'])
    
    def test_get_col(self):
        grid = [['1','2','.'], ['4','5','6'], ['7','8','9']]
        self.assertEqual(get_col(grid, (0,0)), ['1','4','7'])
        self.assertEqual(get_col(grid, (0,1)), ['2','5','8'])
    
    def test_get_block(self):
        grid = [['1','2','3','4','5','6','7','8','9'] for _ in range(9)]
        self.assertEqual(len(get_block(grid, (0,0))), 9)
    
    def test_find_empty_positions(self):
        grid = [['1','2','.'], ['4','5','6'], ['7','8','9']]
        self.assertEqual(find_empty_positions(grid), (0,2))
    
    def test_find_possible_values(self):
        grid = read_sudoku('puzzle1.txt')
        values = find_possible_values(grid, (0,2))
        self.assertTrue(len(values) > 0)
    
    def test_solve_puzzle1(self):
        grid = read_sudoku('puzzle1.txt')
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(check_solution(solution))
    
    def test_solve_puzzle2(self):
        grid = read_sudoku('puzzle2.txt')
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(check_solution(solution))
    
    def test_solve_puzzle3(self):
        grid = read_sudoku('puzzle3.txt')
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(check_solution(solution))
    
    def test_generate(self):
        grid = generate_sudoku(40)
        self.assertEqual(len(grid), 9)
        self.assertEqual(len(grid[0]), 9)

if __name__ == '__main__':
    unittest.main()
