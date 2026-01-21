from typing import Tuple, List, Callable
import json
import exceptions

class Puzzle:
    def __init__(self, file: str):
        """
        Initializes the Sudoku puzzle board from a JSON file.

        This sets up the board's rows, columns, boxes, and a mask indicating the fixed (non-playable) cells.

        Parameters:
            file (str): Path to the JSON file containing the initial Sudoku puzzle. 
        """
        with open(file, "r") as f:
            self.board = json.load(f)
        # self.rows = self.makeDict(self.get_row)
        # self.columns = self.makeDict(self.get_column)
        # self.boxes = self.makeDict(self.get_box)
        self.mask = self.get_usable_mask()
        self.row_mask, self.col_mask, self.box_mask = self.get_bit_masks()

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the current Sudoku board.

        This method visualizes the board in a grid format with borders and spacing
        to resemble a traditional Sudoku puzzle layout.

        Returns:
            str: A visual representation of the Sudoku board.
        """
        s = []
        for r in range(9):
            s.append("|")
            for i in range(9):
                s.append(f" {self.board[r][i]} |")
            s.append("\n" + "_" * 37 + "\n")
        return "".join(s)
    
    def get_bit_masks(self) -> Tuple[List[int], List[int], List[int]]:
        """
        Builds and returns bitmask representations for all rows, columns, and 3x3 boxes in the Sudoku board.

        Each mask is an integer where bit v (1 << v) is set if digit v (1–9) is present in that row, column, or box.
        These masks allow O(1) checks to determine whether a value can be legally placed in a given cell.
        """
        row = [0] * 9
        col = [0] * 9
        box = [0] * 9

        for r in range(9):
            for c in range(9):
                val = self.board[r][c]
                if val != 0:
                    b = self.get_boxIndex(r,c)
                    bit = 1 << val
                    row[r] |= bit
                    col[c] |= bit
                    box[b] |= bit
        return row, col, box

    
    def get_usable_mask(self) -> List[List[bool]]:
        """
        Generates a mask indicating which cells are editable in the Sudoku board.

        Each cell in the 2D mask is set to True if it is empty (playable), and False if it is fixed (pre-filled).

        Returns:
            List[List[bool]]: A 2D list representing the editable (True) and fixed (False) cells.
        """
        res = []
        for lst in self.board:
            res.append([val == 0 for val in lst])
        return res

    def makeDict(self, func: Callable[[int], List[int]]) -> dict[int, List[int]]:
        """
        Helper method to generate a dictionary mapping indices to Sudoku units (rows, columns, or boxes).

        The dictionary keys are integers (0-8), and the values are lists returned by the provided function.

        Parameters:
            func (Callable[[int], List[int]]): A function that takes an index and returns a 1D list 
            representing a row, column, or box.

        Returns:
            dict[int, List[int]]: A dictionary mapping index to the corresponding unit.
        """
        d = {}
        for i in range(9):
            d[i] = func(i)
        return d

    def get_row(self, index: int) -> list[int]:
        """
        Returns the row at the specified index from the Sudoku board.

        Parameters:
            index (int): The row index (0-8).

        Returns:
            list[int]: A list of integers representing the values in the row.
        """
        return self.board[index]

    def get_column(self, index: int) -> list[int]:
        """
        Returns the column at the specified index from the Sudoku board.

        Parameters:
            index (int): The column index (0-8).

        Returns:
            list[int]: A list of integers represeting th values in the column.
        """
        return [self.board[i][index] for i in range(9)]
    
    def get_boxIndex(self, r: int, c: int) -> int:
        """
        Calculate the box index (0-8) from the row and column indices.

        Parameters:
            r (int): row index (0-8).
            c (int): column index (0-8).

        Returns:
            int: The box index (0-8).
        """
        return c//3 + (r//3 * 3)

    def get_box(self, index: int) -> list[int]:
        """
        Returns the box at the specified index from the Sudoku board.

        Boxes are indexed left-to-right, top-to-bottom (0-8). The returned list contains
        the box's values row by row, left to right.

        Parameters:
            index (int): The box index (0-8).

        Returns:
            list[int]: A list of integers representing the values in the 3x3 box.
        """
        row = index//3 * 3
        column = index%3 * 3
        lst = []
        for i in range(3):
            lst += self.board[row + i][column: column+3]
        return lst

    def is_valid(self, row_index: int, column_index: int, val: int) -> bool:
        """
        Returns True if placing `val` at (row_index, column_index) would not violate Sudoku constraints.

        This is a fast O(1) legality check using bitmasks:
        it ensures `val` (1-9) is not already present in the target row, column, or 3x3 box.
        A value of 0 is treated as "clear the cell" and is always constraint-valid.

        Parameters:
            row_index (int): Row index (0-8).
            column_index (int): Column index (0-8).
            val (int): Value to place (0-9). Use 0 to clear the cell.

        Returns:
            bool: True if the move is allowed by Sudoku rules, False otherwise.
        """
        if val == 0:
            return True
        
        if self.board[row_index][column_index] == val:
            return True

        box_index = self.get_boxIndex(row_index, column_index)
        bit = 1 << val
        if self.row_mask[row_index] & bit:
            return False
        if self.col_mask[column_index] & bit:
            return False
        if self.box_mask[box_index] & bit:
            return False
        return True

    def update(self, r , c, val):
        """
        Attempts to update the cell at (r, c) with a new value if it is valid.

        The update is only allowed if:
        - The value is between 0 and 9 (0 clears the cell)
        - The cell is editable (not fixed)
        - The new value does not violate Sudoku rules (row, column, box)

        Parameters:
            r (int): Row index (0-8)
            c (int): Column index (0-8)
            val (int): Value to assign (0-9)

        Returns:
            str | None: An error message if the update is invalid; None if successful.
        """
        if val not in [0,1,2,3,4,5,6,7,8,9]:
            raise exceptions.InvalidValue()
        
        if self.mask[r][c] == False:
            raise exceptions.FixedValue()
        
        prev = self.board[r][c]
        box = c%3 + (r%3 * 3) # Within a box list
        b = self.get_boxIndex(r,c) # box index

        self.rows[r][c] = val
        self.columns[c][r] = val
        self.boxes[b][box] = val

        if self.is_valid(r,c):
            self.board[r][c] = val
            return None
        
        self.rows[r][c] = prev
        self.columns[c][r] = prev
        self.boxes[b][box] = prev
        raise exceptions.ConflictValue()
        
    def is_solved(self) -> bool:
        """
        Checks if the Sudoku board is completely filled.

        A board is considered solved if there are no empty cells (i.e., no zeros).
        Assumes that all previous updates to the board were valid and followed Sudoku rules.

        Returns:
            bool: True if the board has no empty cells, False otherwise.
        """
        for row in self.board:
            if 0 in row:
                return False
        return True