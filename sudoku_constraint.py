from __future__ import print_function
from constraint import *
import random

class GameConstraint():

    def __init__(self, values):
        self.values = values
        self.problem = Problem()
        self.solution = None

        self.problem.addVariables(range(81),[1,2,3,4,5,6,7,8,9])

        # row constraints
        for row in range(9):
            self.problem.addConstraint(AllDifferentConstraint(), range(row * 9, row * 9 + 9))

        # # column constraints
        for col in range(9):
            self.problem.addConstraint(AllDifferentConstraint(), range(col, col + 72, 9))

        # # square constraints
        self.problem.addConstraint(AllDifferentConstraint(), [0,1,2,9,10,11,18,19,20])
        self.problem.addConstraint(AllDifferentConstraint(), [3,4,5,12,13,14,21,22,23])
        self.problem.addConstraint(AllDifferentConstraint(), [6,7,8,15,16,17,24,25,26])

        self.problem.addConstraint(AllDifferentConstraint(), [27,28,29,36,37,38,45,46,47])
        self.problem.addConstraint(AllDifferentConstraint(), [30,31,32,39,40,41,48,49,50])
        self.problem.addConstraint(AllDifferentConstraint(), [33,34,35,42,43,44,51,52,53])
        
        self.problem.addConstraint(AllDifferentConstraint(), [54,55,56,63,64,65,72,73,74])
        self.problem.addConstraint(AllDifferentConstraint(), [57,58,59,66,67,68,75,76,77])
        self.problem.addConstraint(AllDifferentConstraint(), [60,61,62,69,70,71,78,79,80])

        # constraints for the values set in the puzzle
        for index in range(81):
            if self.values[index] != 0:
                self.problem.addConstraint(lambda var, value = self.values[index]: var == value, (index,))


    def solve(self):
        self.solution = self.problem.getSolution()
        return(self.solution != None)
    
    def is_solved(self):
        return(self.solution != None)
    
    def draw(self):
        for index in range(1,82):
            print(self.solution[index - 1], end = ' ')
            if index % 3 == 0 and index % 9 != 0:
                print('|', end = ' ')
            if index % 9 == 0:
                print('')
            if index in (27,54):
                print('---------------------')
        print('')
