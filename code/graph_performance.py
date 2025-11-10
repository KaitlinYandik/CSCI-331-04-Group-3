import csv
from backtrack import CSP_Sudoku
from sudoku import SudokuState
from ac3 import AC3Solver

import matplotlib.pyplot as plt

SUDOKU_FILES = [
    "data/sudoku1.csv",
    "data/sudoku2.csv",
    "data/sudoku3.csv",
    "data/sudoku4.csv",
    "data/sudoku5.csv",
    "data/sudoku6.csv",
    "data/sudoku7.csv",
    "data/sudoku8.csv"
]

def graph():
    number = 1
    for file in SUDOKU_FILES:
        with open(file) as csv_file:
            reader = csv.reader(csv_file)
            board = [list(map(lambda x: int(x) if x else None, row)) for row in reader]
        sudoku = SudokuState(board)
        bt_only_depth = []
        ac3_depth = []
        csp = CSP_Sudoku(sudoku)
        bt_only_depth = csp.backtracking_search(depth_list=bt_only_depth)[1]
        print("Finished backtracking only on " + str(number))
        ac3 = AC3Solver(sudoku)
        ac3.ac3()
        ac3_depth = ac3.backtracking_search(depth_list=ac3_depth)[1]
        print("Finished ac3 backtracking on " + str(number))
        fig, ax = plt.subplots()
        ax.plot(bt_only_depth, label="Backtracking only")
        ax.plot(ac3_depth, label="AC3 first")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Depth")
        ax.set_title("Performance on Sudoku " + str(number))
        fig.legend()
        fig.savefig("data/graph" + str(number) + ".png")
        print("Saved to file")
        number += 1

def main():
    graph()

if __name__ == "__main__":
    main()