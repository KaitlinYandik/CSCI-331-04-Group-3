from sudoku import SudokuState
import copy
import csv

class CSP_Sudoku:
    def __init__(self, sudoku: SudokuState):
        self.state = sudoku
        self.variables = set(range(0, 81))
        self.domains = {}
        for box in self.variables:
            already_there = sudoku.get_value(box)
            if already_there is not None:
                self.domains[box] = [already_there]
            else:
                self.domains[box] = set(range(1, 10))
        self.neighbors = {}
        for box in self.variables:
            self.neighbors[box] = set(filter(lambda x: x // 9 == box // 9 or x % 9 == box % 9 or (box // 3 % 3 == x // 3 % 3 and box // 9 // 3 == x // 9 // 3), list(range(0, 81))))
            self.neighbors[box].remove(box)

    def select_unassigned_variable(self, assignment: SudokuState):
        result = None
        for var in self.variables:
            if assignment.get_value(var) is None and (result is None or len(self.domains[var]) < len(self.domains[result])):
                result = var
        return result

    def backtracking_search(self, sudoku_state: SudokuState = None):
        sudoku_state = sudoku_state or self.state
        if sudoku_state.all_assigned():
            return sudoku_state
        var = self.select_unassigned_variable(sudoku_state)
        for value in self.domains[var]:
            new_state = SudokuState(copy.deepcopy(sudoku_state.board))
            new_state.board[var // 9][var % 9] = value
            if new_state.validate():
                result = self.backtracking_search(new_state)
                if result:
                    return result

def main():
    with open('data/sudoku1.csv') as csv_file:
        reader = csv.reader(csv_file)
        board = [list(map(lambda x: int(x) if x else None, row)) for row in reader]
    sudoku = SudokuState(board)
    print(board)
    csp = CSP_Sudoku(sudoku)
    print(csp.backtracking_search().board)

if __name__ == "__main__":
    main()