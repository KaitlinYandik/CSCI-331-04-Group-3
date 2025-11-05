import csv
from argparse import ArgumentError

class SudokuState:
    board: list[list[int | None]]

    def __init__(self, board: list[list[int | None]]):
        self.board = board
        if len(board) != 9:
            raise ArgumentError(board, "Sudoku board must have 9 rows")
        if not all(len(row) == 9 for row in board):
            raise ArgumentError(board, "Each row must have 9 elements")

    def validate(self) -> bool:
        for i in range(9):
            row = set()
            col = set()
            box = set()
            for j in range(9):
                row_item = self.board[i][j]
                col_item = self.board[j][i]
                box_item = self.board[3*(i//3)+(j//3)][3*(i%3)+(j%3)]
                if row_item is not None:
                    if row_item in row:
                        return False
                    row.add(row_item)
                if col_item is not None:
                    if col_item in col:
                        return False
                    col.add(col_item)
                if box_item is not None:
                    if box_item in box:
                        return False
                    box.add(box_item)
        return True
    
    def all_assigned(self) -> bool:
        for i in range(9):
            if None in self.board[i]:
                return False
        return True

    def get_value(self, number) -> int | None:
        i = number // 9
        j = number % 9
        return self.board[i][j]

    def __str__(self):
        result = ""
        for (i, row) in enumerate(self.board):
            for cell in row:
                result += f"{cell or '*'} "
            if i != len(self.board) - 1:
                result += '\n'
        return result

if __name__ == '__main__':
    with open('data/sudoku1.csv') as csv_file:
        reader = csv.reader(csv_file)
        board = [list(map(lambda x: int(x) if x else None, row)) for row in reader]
        state = SudokuState(board)
        print(f"Board: \n{state}")
        print(f"Solvable: {state.validate()}")
