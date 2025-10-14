from sudoku import SudokuState
import copy
import csv

def backtrack(sudoku: SudokuState):
    if not sudoku.validate():
        return None
    if sudoku.all_assigned():
        return sudoku
    for i in range(9):
        for j in range(9):
            if sudoku.board[i][j] != None:
                continue
            new_sudoku = SudokuState(copy.deepcopy(sudoku.board))
            for k in range(1, 10):
                new_sudoku.board[i][j] = k
                result = backtrack(new_sudoku)
                if result:
                    return result

def main():
    with open('data/sudoku1.csv') as csv_file:
        reader = csv.reader(csv_file)
        board = [list(map(lambda x: int(x) if x else None, row)) for row in reader]
    sudoku = SudokuState(board)
    print(board)
    print(backtrack(sudoku))

if __name__ == "__main__":
    main()