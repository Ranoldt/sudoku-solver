from typing import List, Callable
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
        self.rows = self.makeDict(self.get_row)
        self.columns = self.makeDict(self.get_column)
        self.boxes = self.makeDict(self.get_box)
        self.mask = self.get_mask()

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
    
    def get_mask(self) -> List[List[bool]]:
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

    def is_valid(self, row_index: int, column_index: int) -> bool:
        """
        Checks if the row, column, and box at the given cell are currently valid.

        This method is typically called after a board update. It builds lists of the non-zero values
        in the corresponding row, column, and 3x3 box. If any of those lists contain duplicates, 
        the state is considered invalid.

        Parameters:
            row_index (int): The row index (0-8).
            column_index (int): The column index (0-8).

        Returns:
            bool: True if all related units are valid (no duplicates), False otherwise.
        """
        box_index = self.get_boxIndex(row_index, column_index)
        row = [val for val in self.rows[row_index] if val != 0]
        column  = [val for val in self.columns[column_index] if val != 0]
        box = [val for val in self.boxes[box_index] if val != 0]

        if len(row) != len(set(row)):
            return False
        if len(column) != len(set(column)):
            return False
        if len(box) != len(set(box)):
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
        self.boxes[box][b] = prev
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