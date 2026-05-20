from sudoku.sudoku import Puzzle
from solver.solver import LogicSolver

puzzle = Puzzle("puzzle.json")
solver = LogicSolver(puzzle)

print("Before:")
print(puzzle)

solved = solver.solve()

print("After:")
print(puzzle)

print("Solved:", solved)

for step in solver.steps:
    print(step) 