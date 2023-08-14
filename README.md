First iteration
Only look at single candidate constraint from same row, column and square
Solves 89 of first 99 puzzles
Solves 8100 of first 9999 puzzles

Next iteration
99 of 99
9733 of 9999

Next iteration: add simple random step
solves about 9837 of 9999

Things to eplxore
best random move: field that has the shortest list of candidates, and try each possible candidate before moving to the next field


Using python-constraint solves all 10k puzzles.
https://github.com/python-constraint/python-constraint

Stats 
BacktrackingSolver
{'solved': 9999, 'not_solved': 0}
python main.py  67.84s user 0.31s system 98% cpu 1:09.12 total

RecursiveBackTrackingSolver
{'solved': 9999, 'not_solved': 0}
python main.py  69.30s user 0.27s system 98% cpu 1:10.29 total

MinConflictsSolver
stopped after 20 minutes ...
tried a few simple puzzles, does not find ways to solve them....
