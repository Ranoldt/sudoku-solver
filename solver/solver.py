
from sudoku.sudoku import Puzzle
from typing import List

class LogicSolver:
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle

    def get_candidates(self) -> List[List[List[int]]]:
        pass
