import copy
import csv
from argparse import ArgumentError
from ac3 import AC3Solver
from sudoku import SudokuState


class RegionSudokuState(SudokuState):
    ANSI_COLOR_CODES = [
        '\x1b[31m', '\x1b[32m', '\x1b[33m',
        '\x1b[34m', '\x1b[35m', '\x1b[36m'
    ]
    areas: list[list[int]]

    def __init__(self, board: list[list[int | None]], areas: list[list[int]]):
        super().__init__(board)
        if len(areas) != len(board):
            raise ArgumentError(areas, "Areas must be the same as the board")
        if not all(len(area_row) == len(row) for (area_row, row) in zip(areas, board)):
            raise ArgumentError(areas, "Areas must be the same as the board")
        self.areas = areas

    def validate(self) -> bool:
        for i in range(9):
            row = set()
            col = set()
            for j in range(9):
                row_item = self.board[i][j]
                col_item = self.board[j][i]
                if row_item is not None:
                    if row_item in row:
                        return False
                    row.add(row_item)
                if col_item is not None:
                    if col_item in col:
                        return False
                    col.add(col_item)
        area_set = [set() for _ in range(9)]
        for i in range(0, 81):
            value = self.get_value(i)
            if value is None:
                continue
            area_value = self.get_area(i)
            if value in area_set[area_value]:
                return False
            area_set[area_value].add(value)
        return True

    def get_area(self, number) -> int | None:
        i = number // 9
        j = number % 9
        return self.areas[i][j]

    def get_area_color(self, area_num):
        return self.ANSI_COLOR_CODES[area_num%len(self.ANSI_COLOR_CODES)]

    def get_neighbors(self) -> dict[int, set[int]]:
        neighbors = {}
        for box in range(0, 81):
            neighbors[box] = set(filter(lambda x: x // 9 == box // 9 or x % 9 == box % 9 or self.get_area(x) ==
                            self.get_area(box), list(range(0, 81))))
            neighbors[box].remove(box)
        return neighbors

    def copy(self):
        return RegionSudokuState(copy.deepcopy(self.board), self.areas)

    def __str__(self):
        result = ""
        for (i, (area_row, row)) in enumerate(zip(self.areas, self.board)):
            for (cell_area, cell) in zip(area_row, row):
                result += f"{self.get_area_color(cell_area)}{cell or '*'} "
            if i != len(self.board) - 1:
                result += '\n'
            result += '\x1b[0m'
        return result

if __name__ == '__main__':
    with open('data/region_sudoku1.csv') as csv_file:
        reader = csv.reader(csv_file)
        rows = [row for row in reader]
        board = [list(map(lambda x: int(x) if x else None, row)) for row in rows[:9]]
        areas = [list(map(lambda x: int(x) if x else None, row)) for row in rows[9:]]
    sudoku = RegionSudokuState(board, areas)
    print(f"Board: \n{sudoku}")
    ac3 = AC3Solver(sudoku)
    ac3.ac3()
    print(f"Domains: {ac3.domains}")
    print(f"Solution: \n{ac3.backtracking_search()}")
