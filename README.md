# Group 3: Sudoku
## Group Members
Kaitlin Yandik, Varun Mahesh
## Abstract
Our project was to use a Constraint Satisfaction Problem (CSPs) to solve a sudoku. We also compare plain CSP backtracking with an enhanced version using arc consistency to limit domain sizes, specifically the AC3 algorithm. Our algorithms work on both traditional sudokus and sudokus with different box shapes, known as "region" or "jigsaw" sudokus. Performance is compared using recursion depth at each run.
## How to Run
To run backtracking only, run backtrack.py with the path to a sudoku csv file as an argument.
To run with AC3, run ac3.py with the path to a sudoku csv file as an argument.
To generate graphs, run graph_performance.py.