import unittest
from sudoku2 import Game, Grid, Field, Logger

class TestGrid(unittest.TestCase):

    # runs once before all tests
    @classmethod
    def setUpClass(cls):
        cls.values = [2,0,4,1,5,0,6,0,0,
          0,0,0,0,8,0,5,0,0,
          0,0,0,2,0,0,0,0,9,
          0,0,5,3,0,0,0,0,2,
          9,0,1,8,0,0,0,6,0,
          7,8,0,6,4,0,1,0,3,
          0,0,0,7,0,9,0,0,0,
          1,0,0,0,3,0,0,4,7,
          5,0,6,0,0,0,0,0,0
          ]
        cls.grid = Grid()
        cls.grid.set_values(cls.values)
        
    def test_column_returns_correct_fields(self):
        for column in range(9):
            fields = self.grid.column(column)
            self.assertEqual(len(fields), 9)
            for field in fields:
                self.assertEqual(field.column, column)

    def test_row_returns_correct_fields(self):
        for row in range(9):
            fields = self.grid.row(row)
            self.assertEqual(len(fields), 9)
            for field in fields:
                self.assertEqual(field.row, row)

    def test_square_returns_correct_fields(self):
        for square in range(9):
            fields = self.grid.square(square)
            self.assertEqual(len(fields), 9)
            for field in fields:
                self.assertEqual(field.square, square)

if __name__ == '__main__':
    unittest.main()
