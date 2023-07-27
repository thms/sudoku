from sudoku2 import Game
import games

# Auto generate a games that should be solvable: (doesn't quite work yet)
# game = Game()
# game.generate(30)

# Set a single game
# game = Game()
# game.grid.set_values(games.EASY2)

# read games from Kaggle data set
# each line is one game 81 digits puzzle ',' 81 digits solution, 0 represents an empty field
file = open('sudoku100.csv','r')
data = file.readlines()
file.close()
stats = {'solved': 0, 'not_solved': 0}
for puzzle in data:
    values = [int(i) for i in [*puzzle[0 : 81]]]
    game = Game()

    game.grid.set_values(values)
    game.grid.draw()
    game.grid.step()
    game.grid.draw()
    if game.grid.is_solved():
        stats['solved'] += 1
    else:
        stats['not_solved'] +=1
        break
    print('================================')

print(stats)