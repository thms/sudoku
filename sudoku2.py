from __future__ import print_function
import random

# Represents a single field of the Sudoku board
class Field:
  
  def __init__(self, row, column, square):
    self.value = None
    self.row = row
    self.column = column
    self.square = square
    self.candidates = [1,2,3,4,5,6,7,8,9]
    random.shuffle(self.candidates)

  def set_value(self, value):
    self.value = value
    self.candidates = []
    # log event
    # Logger.log('[{}, {}]: {}'.format(self.row, self.column, value))

  def __repr__(self):
    if self.value:
      return str(self.value)
    else:
      return ' '


# represents all fields, and allows access to rows, columns, and squares
class Grid:

  def __init__(self):
    self.fields = []
    for row in range(9):
      for column in range(9):
        self.fields.append(Field(row, column, 0))
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
  def column(self, index):
    return self.fields[index : index + 81 : 9]

  # return all fields on a columns first, second or third subdivision
  def sub_column(self, index, sub_division):
    return self.column(index)[sub_division * 3 : sub_division * 3 + 3 :1]

  # returns all fields for a row from 0 - 8
  def row(self, index):
    return self.fields[index * 9 : index * 9 + 9 : 1]

  # returns all fiels in a row's first, second or third subdivision
  def sub_row(self, index, sub_division):
    return self.row(index)[sub_division * 3 : sub_division * 3 + 3 :1]

  # returns all fields in a square
  def square(self, index):
    if index < 3:
      start = index * 3
    elif index < 6:
      start = 27 + (index - 3) * 3
    else:
      start = 54 + (index - 6) * 3
    return [self.fields[start], self.fields[start + 1], self.fields[start + 2],
    self.fields[start + 9], self.fields[start + 10], self.fields[start + 11],
    self.fields[start + 18], self.fields[start + 19], self.fields[start + 20]]

  def set_squares(self):
    for i in range(9):
      for field in self.square(i):
        field.square = i

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
    areas = [self.column(field.column), self.row(field.row), self.square(field.square)]
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
    areas = [self.sub_row(field.row, 0), self.sub_row(field.row, 1), self.sub_row(field.row, 2),
              self.sub_column(field.column, 0), self.sub_column(field.column, 1), self.sub_column(field.column, 2)]
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
  def update_dependent_candidates(self, field):
    areas = [self.column(field.column), self.row(field.row), self.square(field.square)]
    for area in areas:
      for dependent_field in area:
        try:
          dependent_field.candidates.remove(field.value)
        except ValueError:
          pass

  # iterate over all fields and set th value for those that only have a single candidate left
  # TODO: remove from locations ....
  def set_single_candidate_fields(self, locations):
    i = 0
    for field in self.fields:
      if len(field.candidates) == 1:
        print('single candidate field {}-{}'.format(field.row, field.column))
        field.set_value(field.candidates[0])
        self.update_dependent_candidates(field)
        locations.remove(i)
      i += 1


  # fill the grid
  def fill(self, fields_filled):
    locations = range(81)
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



class Game:

  def __init__(self, fields_filled):
    self.grid = Grid()
    self.grid.fill(fields_filled)

game = Game(30)

game.grid.draw()
#print(game.grid.values(game.grid.row(0)))
#print(game.grid.candidates(game.grid.row(0)))
