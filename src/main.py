import copy
from graph_coloring import GraphColoring
from sudoku import Sudoku
from visualizer import Visualizer
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
from sudoku_visualizer import SudokuVisualizer
from sys import setrecursionlimit

from webbrowser import open as webopen


def benchmark_times():
    print("Starting time benchmark")
    print(
        "Average time to 19-color a 38 vertex graph:",
        test_time(GraphColoring, 38),
    )
    print(
        "Average time to find a hamiltonian cycle on a 23 vertex graph:",
        test_time(HamiltonianCycle, 23),
    )
    print(
        "Average time to solve a 9x9 sudoku:",
        test_time(Sudoku, 9),
    )


"""runs loop for displaying output"""


def graph_vis():
    # bootstrap
    print("STARTING VISUAL EPICNESS")
    color_graph = GraphColoring(0, [], [], 3)
    solution = None
    Ham_solution = None
    found_solution = True
    webopen('http://localhost:8050')
    while True:
        # create image
        vis = Visualizer(color_graph, solution, Ham_solution, found_solution)
        #initialize solutions to none
        solution = None
        found_solution = True
        Ham_solution = None
        correct_end, color_graph = vis.show()
        if not correct_end:
            break
        #depending on the task, solve and update the solution
        match vis.task:
            case "COLOR":
                # solve coloring problem
                solution = color_graph.solve()
                if solution is None:
                    found_solution = False
                continue
            case "HAMPATH":
                # solve hampath problem
                ham_graph = HamiltonianCycle(color_graph.num_nodes, color_graph.edges)
                Ham_solution = ham_graph.solve()
                if Ham_solution is None:
                    found_solution = False
                continue
            case "END":
                # end simulation
                break


def visualize_sudoku():
    vis = SudokuVisualizer()
    action = input("Would you like to generate a random sudoku(1), or input one yourself(2)?")
    sud = Sudoku.initializeRandomly(4)
    if (action == "1"):
        sud = Sudoku.initializeRandomly(4)
    elif (action == "2"):
        sud = Sudoku.initializeFromInput()
    else:
        print("Invalid option >:(")
        return
    
    # make the cells in the right colors
    cellColors = copy.deepcopy(sud.board)
    for i in range(len(sud.board)):
        for j in range(len(sud.board[i])):
            if (sud.board[i][j] is None):
                cellColors[i][j] = "blue"
            else:
                cellColors[i][j] = "black"
    
    vis.visualize_sudoku(sud.board, cellColors)
    input("Press enter to calculate solution")
    sol = sud.solve()
    if sol is None:
        print("No solution")
    else:
        vis.visualize_sudoku(sol, cellColors)
        input("Press enter to exit")





def main():
    setrecursionlimit(3000)
    print("WELCOME TO VERY EPIC SAT SOLVER")
    print("What would you like to do?")
    print("1 - Benchmark solving times")
    print("2 - View graph visualizer")
    print("3 - View sudoku solution")
    action = input("")
    if action == "1":
        benchmark_times()
    elif action == "2":
        graph_vis()
    elif action == "3":
        visualize_sudoku()
    else:
        print("Not a valid option")


if __name__ == "__main__":
    main()
