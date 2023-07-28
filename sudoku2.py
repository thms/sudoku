from __future__ import print_function
import random
from functools import reduce


# Purpose: Log events in the game, for debugging and backtracking
class Logger:

  events = []

  @classmethod
  def log(cls, event):
    cls.events.append(event)

  @classmethod
  def show(cls):
    for event in cls.events:
      print(event)

# Represents a single field of the Sudoku board
class Field:
  
  def __init__(self, row, column, square):
    self.value = None
    self.row = row # numbered 0..8
    self.column = column # numbered 0..8
    self.square = square # numbered 0..8
    self.candidates = [1,2,3,4,5,6,7,8,9]
    # randomize candidates to make generating games easier
    random.shuffle(self.candidates)

  def set_value(self, value):
    self.value = value
    self.candidates = []
    # log event
    Logger.log('[{}, {}]: {}'.format(self.row, self.column, value))

  def linear_index(self):
    return self.row * 9 + self.column 

  def __repr__(self):
    if self.value:
      return str(self.value)
    else:
      return ' '

# Represents a column of the puzzle, to store candidates and evaluate constraints
class Column:
  def __init__(self, index):
    self.index = index
    self.numbers_to_assign = [1,2,3,4,5,6,7,8,9]
    self.values = [None,None,None,None,None,None,None,None,None] # index == row, value == number
    # Stores for each number (key) in which field (values) it can still be
    self.candidates = {1: [0,1,2,3,4,5,6,7,8],
                       2: [0,1,2,3,4,5,6,7,8],
                       3: [0,1,2,3,4,5,6,7,8],
                       4: [0,1,2,3,4,5,6,7,8],
                       5: [0,1,2,3,4,5,6,7,8],
                       6: [0,1,2,3,4,5,6,7,8],
                       7: [0,1,2,3,4,5,6,7,8],
                       8: [0,1,2,3,4,5,6,7,8],
                       9: [0,1,2,3,4,5,6,7,8]
                      }

  def update(self, grid):
    self.update_from_grid(grid)
    self.assign_values(grid)

  # update state of column from the state of the grid
  def update_from_grid(self, grid):
    for field in grid.column_fields(self.index):
      # if the field in the column has been assigned a value already
      if field.value != None:
        self.values[field.row] = field.value
        self.candidates[field.value] = []
        if field.value in self.numbers_to_assign:
          self.numbers_to_assign.remove(field.value)
        for key in self.candidates.keys():
          if field.row in self.candidates[key]:
            self.candidates[key].remove(field.row)
      else: # field.value == None
        # field is still unassigned, reduce number of candidates from the corresponding row
        # remove field from list of caniddates for the number if the row contains the number
        for row_field in grid.row_fields(field.row):
          if row_field.value != None and row_field.row in self.candidates[row_field.value]:
            self.candidates[row_field.value].remove(row_field.row)


  # if only a single candidate field left for a number, assign it
  # called after updating from grid
  def assign_values(self, grid):
    for number in self.numbers_to_assign:
      if len(self.candidates[number]) == 1:
        row = self.candidates[number].pop()
        grid.field_by_row_and_column(row, self.index).set_value(number)
        self.values[row] = number





# represents all fields, and allows access to rows, columns, and squares
class Grid:

  def __init__(self):
    self.fields = []
    self.columns = []
    for row in range(9):
      for column in range(9):
        self.fields.append(Field(row, column, 0))
        self.columns.append(Column(column))
    self.set_squares()

  def draw(self):
    i = 1
    for field in self.fields:
      print(field, end = ' ')
      if i % 3 == 0 and i % 9 != 0:
        print('|', end = ' ')
      if i % 9 == 0:
        print('')
      if i in (27,54):
        print('---------------------')
      i += 1
    print('')

  # returns all fields in a column from 0 - 8
  def column_fields(self, index):
    return self.fields[index : 81 : 9]

  # return all fields on a columns first, second or third subdivision
  def sub_column_fields(self, index, sub_division):
    return self.column_fields(index)[sub_division * 3 : sub_division * 3 + 3 :1]

  # returns all fields for a row from 0 - 8
  def row_fields(self, index):
    return self.fields[index * 9: index * 9 + 9 : 1]

  # returns all fields in a row's first, second or third subdivision
  def sub_row_fields(self, index, sub_division):
    return self.row_fields(index)[sub_division * 3 : sub_division * 3 + 3 :1]

  # returns all fields in a square from 0 - 8, lef to right, then top to bottom
  def square_fields(self, index):
    if index < 3:
      start = index * 3
    elif index < 6:
      start = 27 + (index - 3) * 3
    else:
      start = 54 + (index - 6) * 3
    return [self.fields[start], self.fields[start + 1], self.fields[start + 2],
    self.fields[start + 9], self.fields[start + 10], self.fields[start + 11],
    self.fields[start + 18], self.fields[start + 19], self.fields[start + 20]]

  # assign the fields to squares
  def set_squares(self):
    for i in range(9):
      for field in self.square_fields(i):
        field.square = i

  # get field in row and column
  def field_by_row_and_column(self, row, column):
    return self.fields[row * 9 + column]

  # returns all filled values for a set of fields:
  def values(self, fields):
    return [field.value for field in fields if field.value != None]

  # returns the uniqe list of candidates from a union of fields
  def candidates(self, fields):
    return list(set([candidate for field in fields for candidate in field.candidates ]))

  # evaluates if setting a field to a value would violate any of the constraints
  # constraints are:
  # no field may end up with an empty candidate list unless it's value has already be set
  # no area's candidates may be less than the number of empty fields in the area
  def dependent_constraints_violated(self, field, value):
    areas = [self.column_fields(field.column), self.row_fields(field.row), self.square_fields(field.square)]
    # test if removing the candidates leaves any field without candidate:
    for area in areas:
      for area_field in area:
        if field == area_field:
          continue
        elif area_field.value == None and len(area_field.candidates) == 1 and area_field.candidates[0] == value:
          return True
    # test if any area has fewer candidates than empty fields left if setting the value:
    for area in areas:
      if (len(self.candidates(area)) - 1) < (9 - len(self.values(area)) - 1):
        return True
    # test sub areas:
    areas = [self.sub_row_fields(field.row, 0), self.sub_row_fields(field.row, 1), self.sub_row_fields(field.row, 2),
              self.sub_column_fields(field.column, 0), self.sub_column_fields(field.column, 1), self.sub_column_fields(field.column, 2)]
    for area in areas:
      print(self.values(area), end = ' - ')
      print(self.candidates(area))
      if field in area:
        if len(set(self.candidates(area)) - set([value])) < (3 - len(set(self.values(area) + [value]))):
          return True
      else:
        if len(set(self.candidates(area)) - set([value])) < (3 - len(self.values(area))):
          return True
    return False

  # update dependent fields candidates when setting a field's value
  # areas are the column, row and square a field is part of
  def update_dependent_candidates(self, field):
    areas = [self.column_fields(field.column), self.row_fields(field.row), self.square_fields(field.square)]
    for area in areas:
      for dependent_field in area:
        try:
          dependent_field.candidates.remove(field.value)
        except ValueError:
          pass

  # iterate over all fields and set the value for those that only have a single candidate left, where there is not already a value set
  def set_single_candidate_fields(self, locations):
    fields_set = 0
    for field in self.fields:
      if len(field.candidates) == 1 and field.value == None:
        #print('single candidate field {}-{}:{}'.format(field.row + 1, field.column + 1, field.candidates[0]))
        field.set_value(field.candidates[0])
        self.update_dependent_candidates(field)
        fields_set += 1
    return fields_set


  # fill the grid with a nset of numbers that do not violate the constraints
  def fill(self, fields_filled):
    locations = [*range(81)]
    random.shuffle(locations)
    locations.reverse()
    tries = 0
    while fields_filled > 0 and tries < 70:
      tries += 1
      try:
        fields_filled -= 1
        location = locations.pop()
        field = self.fields[location]
        print(field.row, field.column)
        if self.dependent_constraints_violated(field, field.candidates[-1]) == True:
          # remove the candidate that would lead to a violation from the field
          print("removing candidate {}".format(field.candidates[-1]))
          field.candidates.pop()
          # try another candidate for the location next round:
          fields_filled += 1
          locations.append(location)
        else:
          field.set_value(field.candidates.pop())
          self.update_dependent_candidates(field)
          self.set_single_candidate_fields(locations)
      except IndexError:
        fields_filled += 1
        locations.append(location)

  # Fill the grid with a given sequence to allow it to solve external puzzles
  # values is a list of field values in order of rows, and update candidates for all fields
  def set_values(self, values):
    index = 0
    for field in self.fields:
      if values[index] == 0:
        index += 1
        continue
      else:
        field.set_value(values[index])
        index += 1
    
    for field in self.fields:
      self.update_dependent_candidates(field)

  # do one step of the solution
  # find a field that has only a single candidate, make that the value and update dependent candidates
  # it is possible that we do not find any fields with single candidates, then we need to guess and backtrack...
  def step(self):
    # find and set all fields with a single candidate, until there are no more left
    while True:
      print('iterating single candidates')
      fields_updated = self.set_single_candidate_fields([*range(81)])
      if fields_updated == 0:
        break
    # apply the column wide constraints
    for column in self.columns:
      column.update(self)
    # print(self.columns[1].numbers_to_assign)
    # print(self.columns[1].values)
    # print(self.columns[1].candidates[3])

  # returns True if all fields have a value assigned to them
  def is_solved(self):
    return all(field.value != None for field in self.fields)
    

# Randomly generate a game and then try and solve it.
class Game:

  def __init__(self):
    self.grid = Grid()
  
  # Set a randomized, but posssible starting point
  def generate(self, fields_filled):
    self.grid.fill(fields_filled)
