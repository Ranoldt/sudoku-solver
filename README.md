# Sudoku Solver

A Python project to represent, validate, and solve Sudoku puzzles using human-style logical techniques.  
Eventually extensible to support variants like Killer Sudoku.

## Project Structure
```
sudoku_solver/
├── main.py # Entry point to load and interact with puzzles
├── puzzle.json # Sample puzzle data
│
├── sudoku/ # Core puzzle logic
│ ├── sudoku.py # Puzzle class
│ ├── exceptions.py # Custom exceptions
│ └── init.py
│
├── solver/ # Logical solving strategies
│ ├── solver.py
│ └── init.py
```

## Project Goals
- Represent Sudoku puzzles with constraint validation  
- Build a human-style solver using logical techniques  
- Eventually integrate ML to mimic human solving strategies  
- Extend to Killer Sudoku and other variants  
