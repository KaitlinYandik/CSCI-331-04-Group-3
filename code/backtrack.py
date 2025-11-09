from sudoku import SudokuState
import copy
import csv

class CSP_Sudoku:
    def __init__(self, sudoku: SudokuState):
        self.state = sudoku
        self.variables = set(range(0, 81))
        self.domains = {}
        self.neighbors = sudoku.get_neighbors()
        for box in self.variables:
            already_there = sudoku.get_value(box)
            if already_there is not None:
                self.domains[box] = set()
                self.domains[box].add(already_there)
            else:
                self.domains[box] = set(range(1, 10))

    def select_unassigned_variable(self, assignment: SudokuState):
        result = None
        for var in self.variables:
            if assignment.get_value(var) is None and (result is None or len(self.domains[var]) < len(self.domains[result])):
                result = var
        return result

    def backtracking_search(self, sudoku_state: SudokuState = None, current_depth=1, depth_list: list=None) -> SudokuState | tuple[SudokuState, list]:
        sudoku_state = sudoku_state or self.state
        if depth_list:
            depth_list.append(current_depth)
        if sudoku_state.all_assigned():
            if depth_list:
                return sudoku_state, depth_list
            return sudoku_state
        var = self.select_unassigned_variable(sudoku_state)
        for value in self.domains[var]:
            new_state = sudoku_state.copy()
            new_state.board[var // 9][var % 9] = value
            if new_state.validate():
                result = self.backtracking_search(new_state, current_depth + 1, depth_list)
                if result:
                    return result

def main():
    with open('data/sudoku1.csv') as csv_file:
        reader = csv.reader(csv_file)
        board = [list(map(lambda x: int(x) if x else None, row)) for row in reader]
    sudoku = SudokuState(board)
    csp = CSP_Sudoku(sudoku)
    print(f"Board: \n{sudoku}")
    print(f"Domains: {csp.domains}")
    print(f"Solution: \n{csp.backtracking_search()}")

if __name__ == "__main__":
    main()