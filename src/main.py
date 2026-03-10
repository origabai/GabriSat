from graph_coloring import GraphColoring
from sudoku import Sudoku
from visualizer import Visualizer
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
from sudoku_visualizer import SudokuVisualizer

def benchmark_times():
    print("Starting time benchmark")
    print("Average time to 3-color a 6 vertex graph:",test_time(GraphColoring.generate(), 6))
    print("Average time to find a hamiltonian cycle on a 4 vertex graph:",test_time(HamiltonianCycle.generate(), 4))
    print("Average time to solve a 1x1 sudoku(expert level):",test_time(Sudoku.generate(), 1))

def graph_vis():
    print("STARTING VISUAL EPICNESS")
    graph = GraphColoring(6, [[0,1],[0,2],[1,2],[2,3],[2,5],[5,4],[3,4]], [1,2,6,7,None,None], 3)
    vis = Visualizer(graph)
    graph = vis.show()
    solution = graph.solve()
    vis = Visualizer(graph, solution)
    vis.show()

def visualize_sudoku():
    vis = SudokuVisualizer()
    # sud = Sudoku.initializeRandomly(1)
    sud = Sudoku([[None]])
    vis.visualize_sudoku(sud.board)
    input("Press enter to calculate solution")
    # vis.visualize_sudoku(sud.solve())
    sol = sud.solve()
    vis.visualize_sudoku(sol)
    input("Press enter to exit")

def main():
    print("WELCOME TO VERY EPIC SAT SOLVER")
    print("What would you like to do?")
    print("1 - Benchmark solving times")
    print("2 - View graph visualizer")
    print("3 - View sudoku solution")
    action = input("")
    if (action == "1"):
        benchmark_times()
    elif (action == "2"):
        graph_vis()
    elif (action == "3"):
        visualize_sudoku()
    else:
        print("Not a valid option")



if __name__ == "__main__":
    main()