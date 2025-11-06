import csv
from queue import Queue

from backtrack import CSP_Sudoku
from sudoku import SudokuState


class AC3Solver(CSP_Sudoku):
    def constraint(self, xi, x, xj, y):
        return xj in self.neighbors[xi] and x != y

    def revise(self, xi, xj):
        revised = False
        for x in set(self.domains[xi]):
            if not any(self.constraint(xi, x, xj, y) for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised

    def ac3(self):
        queue = Queue()
        for arc in ((xi, xj) for xi in self.variables for xj in self.neighbors[xi]):
            queue.put(arc)
        while not queue.empty():
            (xi, xj) = queue.get()
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.put((xi, xk))
        return True


def main():
    with open('data/sudoku1.csv') as csv_file:
        reader = csv.reader(csv_file)
        board = [list(map(lambda x: int(x) if x else None, row)) for row in reader]
    sudoku = SudokuState(board)
    print(f"Board: \n{sudoku}")
    ac3 = AC3Solver(sudoku)
    ac3.ac3()
    print(f"Domains: {ac3.domains}")
    print(f"Solution: \n{ac3.backtracking_search()}")

if __name__ == "__main__":
    main()
