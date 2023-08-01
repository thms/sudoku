from sudoku2 import Game
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
def kaggle():
    file = open('sudoku_unsolved.csv','r')
    data = file.readlines()
    file.close()
   # outfile = open('sudoku_unsolved.csv','w')
    stats = {'solved': 0, 'not_solved': 0}
    index = 0
    for puzzle in data:
        values = [int(i) for i in [*puzzle[0 : 81]]]
        game = Game()

        game.grid.set_values(values)
        game.grid.draw()
        # do a number of steps as long as more fields get solved:
        while True:
            if game.grid.step() == 0:
                break

        game.grid.draw()
        print(game.grid.columns[2].candidates)

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

# auto_generate()
# single_game()
kaggle()