import unittest
from src.lab3.sudoku import *

class TestSudoku(unittest.TestCase):
    
    def test_group(self):
        self.assertEqual(group([1,2,3,4], 2), [[1,2], [3,4]])
        self.assertEqual(group([1,2,3,4,5,6,7,8,9], 3), 
                         [[1,2,3], [4,5,6], [7,8,9]])
    
    def test_read(self):
        grid = read_sudoku('puzzle1.txt')
        self.assertEqual(len(grid), 9)
        self.assertEqual(len(grid[0]), 9)
    
    def test_find_empty(self):
        grid = [['1','2','3','4','5','6','7','8','9'] for _ in range(9)]
        self.assertIsNone(find_empty(grid))
        grid[0][2] = '.'
        self.assertEqual(find_empty(grid), (0,2))
    
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

if __name__ == '__main__':
    unittest.main()
