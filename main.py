from sudoku2 import Game


game = Game()

# game.generate(30)
VALUES = [2,0,4,1,5,0,6,0,0,
          0,0,0,0,8,0,5,0,0,
          0,0,0,2,0,0,0,0,9,
          0,0,5,3,0,0,0,0,2,
          9,0,1,8,0,0,0,6,0,
          7,8,0,6,4,0,1,0,3,
          0,0,0,7,0,9,0,0,0,
          1,0,0,0,3,0,0,4,7,
          5,0,6,0,0,0,0,0,0
          ]

game.grid.set_values(VALUES)
game.grid.draw()
print(game.grid.fields[7*9+2].candidates)
game.grid.step()
game.grid.draw()
#print(game.grid.values(game.grid.row(0)))
#print(game.grid.candidates(game.grid.row(0)))
