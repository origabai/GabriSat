from graph_coloring import GraphColoring
from sudoku import Sudoku
from time_tester import test_time
def main():
    print(test_time(GraphColoring.generate(), 6))
    print(test_time(Sudoku.generate(), 3))

if __name__ == "__main__":
    main()