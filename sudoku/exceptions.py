class SudokuError(Exception):
    pass

class InvalidValue(SudokuError):
    """
    A user inputs an invalid value.
    """
    def __str__(self):
        return "Invalid input: value must be between 0 and 9."


class FixedValue(SudokuError):
    """
    A user attempts to change a fixed value.
    """
    def __str__(self):
        return "This cell is fixed and cannot be modified."

class ConflictValue(SudokuError):
    """
    A user attempts to update a cell in conflict with row, column, and box.
    """
    def __str__(self):
        return "Move causes a conflict in row, column, or box."
