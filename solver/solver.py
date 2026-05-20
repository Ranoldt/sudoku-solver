
from sudoku.sudoku import Puzzle
from typing import List

class LogicSolver:
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle

    def get_candidates(self) -> List[List[List[int]]]:
        candidates = []
        for r in range(9):
            row_candidates = []
            for c in range(9):
                cand = []
                if self.puzzle.board[r][c] != 0:
                    b = self.puzzle.get_boxIndex(r,c) 
                    seen = self.puzzle.rows[r] + self.puzzle.columns[c] + self.puzzle.boxes[b]
                    cand = [i for i in range(1,10) if i not in seen]
                row_candidates.append(cand)
            candidates.append(row_candidates)
        return candidates