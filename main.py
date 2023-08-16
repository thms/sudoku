from sudoku2 import Game
from sudoku_constraint import GameConstraint
import games

# Auto generate a games that should be solvable: (doesn't quite work yet)
def auto_generate():
    game = Game()
    game.generate(30)
    game.grid.draw()
    game.grid.step()
    game.grid.draw()

# Set a single game
def single_game():
    game = Game()
    game.grid.set_values(games.EASY2)
    game.grid.draw()
    game.grid.step()
    game.grid.draw()
    game.grid.step()
    game.grid.draw()

# read games from Kaggle data set
# each line is one game 81 digits puzzle ',' 81 digits solution, 0 represents an empty field
def game_aware_constraints():
    file = open('sudoku_unsolved.csv','r')
    data = file.readlines()
    file.close()
    #outfile = open('sudoku_unsolved.csv','w')
    stats = {'solved': 0, 'not_solved': 0}
    index = 0
    for puzzle in data:
        values = [int(i) for i in [*puzzle[0 : 81]]]
        game = Game()

        game.grid.set_values(values)
        game.grid.draw()
        game.play()
        game.grid.draw()

        if game.grid.is_solved():
            stats['solved'] += 1
            index += 1
        else:
            stats['not_solved'] +=1
            print('fields filled: ', game.grid.number_of_fields_filled())
            print(index)
            #outfile.writelines(puzzle)
            #break
        print('================================')
    print(stats)
    #outfile.close()

def constraint():
    file = open('sudoku10000.csv','r')
    data = file.readlines()
    file.close()
    stats = {'solved': 0, 'not_solved': 0}
    index = 0
    for puzzle in data:
        values = [int(i) for i in [*puzzle[0 : 81]]]
        game = GameConstraint(values)
        game.solve()
        if game.is_solved():
            stats['solved'] += 1
            index += 1
            game.draw()
        else:
            stats['not_solved'] += 1
        print('================================')
    print(stats)


# auto_generate()
# single_game()
# game_aware_constraints()
constraint()