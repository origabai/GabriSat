from graph_coloring import GraphColoring
from sudoku import Sudoku
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
def main():
    print(test_time(GraphColoring.generate(), 5))
    print(test_time(Sudoku.generate(), 2))
    print(test_time(HamiltonianCycle.generate(), 4))

if __name__ == "__main__":
    main()