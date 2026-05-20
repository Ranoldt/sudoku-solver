
from sudoku.sudoku import Puzzle
from typing import List

class LogicSolver:
    def __init__(self, puzzle: Puzzle):
        """
        Initializes the logical Sudoku solver.

        Parameters:
            puzzle (Puzzle): The Puzzle object containing the Sudoku board
            and validation logic.
        """
        self.puzzle = puzzle
        self.steps = []

    def get_candidates(self) -> List[List[List[int]]]:
        """
        Generates all possible candidate values for each cell in the Sudoku board.

        Filled cells contain an empty list [].
        Empty cells contain a list of all valid digits that can legally
        be placed in that position according to Sudoku rules.

        Returns:
            List[List[List[int]]]:
                A 9x9 nested list where each cell contains a list of candidates.
        """
        candidates = []
        for r in range(9):
            row_candidates = []

            for c in range(9):
                cand = []

                if self.puzzle.board[r][c] == 0:
                    for val in range(1, 10):
                        if self.puzzle.is_valid(r, c, val):
                            cand.append(val)

                row_candidates.append(cand)

            candidates.append(row_candidates)
        return candidates
    
    def naked_single(self) -> bool:
        """
        Applies the Naked Single solving technique.

        A naked single occurs when an empty cell has exactly one
        possible candidate value.

        If found, the value is placed into the puzzle immediately.

        Returns:
            bool:
                True if a value was successfully placed.
                False if no naked singles were found.
        """
        candidates = self.get_candidates()

        for r in range(9):
            for c in range(9):
                if len(candidates[r][c]) == 1:
                    val = candidates[r][c][0]
                    self.puzzle.update(r, c, val)

                    self.steps.append({
                        "technique": "Naked Single",
                        "row": r,
                        "col": c,
                        "value": val
                    })

                    return True
                
        return False
    
    def solve_step(self) -> bool:
        """
        Attempts to make one logical solving move.

        Returns:
            bool: True if a move was made, False if no available technique worked.
        """
        if self.naked_single():
            return True

        return False
    
    def solve(self) -> bool:
        """
        Repeatedly applies solving techniques until the puzzle is solved
        or no more progress can be made.

        Returns:
            bool: True if the puzzle was solved, False if the solver got stuck.
        """
        while not self.puzzle.is_solved():
            if not self.solve_step():
                return False
            
        return True
    
        
