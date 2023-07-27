import random


# Purpose: Log events in the game, for debugging and backtracking
class Logger:

  events = []

  @classmethod
  def log(cls, event):
    cls.events.append(event)

  @classmethod
  def show(cls):
    for event in cls.events:
      print event


# Represents a single field of the Sudoku board
class Field:
  
  def __init__(self, row, column, square):
    self.value = None
    self.row = row
    self.column = column
    self.square = square
    self.candidates = [1,2,3,4,5,6,7,8,9]
    # random.shuffle(self.candidates)

  def set_value(self, value):
    self.value = value
    self.candidates = []
    # log event
    Logger.log('[{}, {}]: {}'.format(self.row, self.column, value))

  def __repr__(self):
    if self.value:
      return str(self.value)
    else:
      return ' '

class Sudoku:
  
  areas = [
    # Rows:
    [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8)],
    [(1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8)],
    [(2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8)],
    [(3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,8)],
    [(4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8)],
    [(5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8)],
    [(6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7), (6,8)],
    [(7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (7,8)],
    [(8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8)],
    # Columns:
    [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (8,0)],
    [(0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1)],
    [(0,2), (1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2)],
    [(0,3), (1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (7,3), (8,3)],
    [(0,4), (1,4), (2,4), (3,4), (4,4), (5,4), (6,4), (7,4), (8,4)],
    [(0,5), (1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5)],
    [(0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6), (8,6)],
    [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (8,7)],
    [(0,8), (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8)],
    # Squares:
    [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)],
    [(0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5)],
    [(0,6), (0,7), (0,8), (1,6), (1,7), (1,8), (2,6), (2,7), (2,8)],
    [(3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (5,0), (5,1), (5,2)],
    [(3,3), (3,4), (3,5), (4,3), (4,4), (4,5), (5,3), (5,4), (5,5)],
    [(3,6), (3,7), (3,8), (4,6), (4,7), (4,8), (5,6), (5,7), (5,8)],
    [(6,0), (6,1), (6,2), (7,0), (7,1), (7,2), (8,0), (8,1), (8,2)],
    [(6,3), (6,4), (6,5), (7,3), (7,4), (7,5), (8,3), (8,4), (8,5)],
    [(6,6), (6,7), (6,8), (7,6), (7,7), (7,8), (8,6), (8,7), (8,8)],
    
  ] # list of indices into the grid that form areas for the constraints

  
  
  def __init__(self):
    self.grid = []
    for i in range(9):
      row = []
      for j in range(9):
        row.append(Field(i, j, self.row_and_column_to_square(i, j)))
      self.grid.append(row)

  def row_and_column_to_square(self, row, column):
    index = 0
    for area in self.areas[18:]:
      if (row, column) in area:
        return index
      else:
        index += 1

  def areas_for_field(self, field):
   return [self.areas[field.row], self.areas[9 + field.column], self.areas[18 + field.square]]

  def draw(self):
    i = 0
    for row in self.grid:
      print row[0], row[1], row[2], '|', row[3], row[4], row[5], '|', row[6], row[7], row[8]
      if i in (2,5):
        print '---------------------'
      i += 1

  def fill(self, slots):
    locations = range(81)
    # random.shuffle(locations)
    locations.reverse()
    while slots > 0:
      try:
        slots -= 1
        location = locations.pop()
        field = self.grid[location // 9][location % 9]
        if self.dependent_constraints_violated(field, field.candidates[-1]) == True:
          # remove the candidate that would lead to a violation from the field
          field.candidates.pop()
          # try again next round:
          slots += 1
          locations.append(location)
        else:
          field.set_value(field.candidates.pop())
          self.update_dependent_candidates(field)
      except IndexError:
        slots += 1
        locations.append(location)
      #print Logger.events[-1]
      #print self.grid[1][7].candidates

  # update the dependent areas candidates
  # also updates self, but that trips the exception
  def update_dependent_candidates(self, field):
    areas = self.areas_for_field(field)
    for area in areas:
      for row, column in area:
        try:
          self.grid[row][column].candidates.remove(field.value)
        except ValueError:
          pass

  # test if an action would result in a zero length candidate list
  # returns True if dependent constraints would be violated if ther did the action
  # need to skip self:
  def dependent_constraints_violated(self, field, value):
    areas = self.areas_for_field(field)
    for area in areas:
      for row, column in area:
        # print self.grid[row][column].candidates
        # Skip self in evaluation
        if row == field.row and column == field.column:
          continue
        # violated if the value is the last possible candidate of a dependent field
        if value in self.grid[row][column].candidates and len(self.grid[row][column].candidates) == 1:
          # print 'constraint violation {} {}'.format(row, column)
          return True
    return False

  # do one step of the solution
  # find a field that has only a single candidate, make that the value and update dependent candidates
  # it is possible that we do not find any fields with songle candidates, then we need to guess and backtrack...
  def step(self):
    # find a field that only has a single candidate
    field = None
    updated_fields = 0
    for i in range(9):
      for j in range(9):
        if len(self.grid[i][j].candidates) == 1 and self.grid[i][j].value == None:
          field = self.grid[i][j]
          field.set_value(field.candidates.pop())
          self.update_dependent_candidates(field)
          updated_fields += 1
          break
    return updated_fields


  def stats(self):
    # max and min candidates for empty fields
    min = 10000
    max = 0
    singles = 0
    for row in range(9):
      for column in range(9):
        field = self.grid[row][column]
        if field.value == None and len(field.candidates) < min:
          min = len(field.candidates)
        if field.value == None and len(field.candidates) > max:
          max = len(field.candidates)
        if field.value == None and len(field.candidates) == 1:
          singles += 1
    return [min, max, singles]

class Constraint:
  pass
  
class Game:
  
  def __init__(self, slots):
    self.sudoku = Sudoku()
    self.sudoku.fill(slots)
    self.sudoku.draw()
  
game = Game(13)

# print game.sudoku.stats()
# while game.sudoku.step() > 0:
#   pass
# print ''
# game.sudoku.draw()
# print game.sudoku.stats()
# Logger.show()
