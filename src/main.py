import copy
from graph_coloring import GraphColoring
from sudoku import Sudoku
from visualizer import Visualizer
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
from sudoku_visualizer import SudokuVisualizer
from pynput.keyboard import Controller, Key 
from sys import setrecursionlimit

from webbrowser import open as webopen


def benchmark_times():
    print("Starting time benchmark")
    print(
        "Average time to 20-color a 40 vertex graph:",
        test_time(GraphColoring.generate(), 40),
    )
    print(
        "Average time to find a hamiltonian cycle on a 25 vertex graph:",
        test_time(HamiltonianCycle.generate(), 25),
    )
    print(
        "Average time to solve a 9x9 sudoku:",
        test_time(Sudoku.generate(), 9),
    )


"""runs loop for displaying output"""


def graph_vis():
    print("STARTING VISUAL EPICNESS")
    color_graph = GraphColoring(0, [], [], 3)
    
    webopen('http://localhost:8050')
    vis = Visualizer(color_graph)
    correct_end, color_graph = vis.show()



def visualize_sudoku():
    vis = SudokuVisualizer()
    action = input("Would you like to generate a random sudoku(1), or input one yourself(2)?")
    sz = 9
    sud = Sudoku.initializeRandomly(sz)
    if (action == "1"):
        sud = Sudoku.initializeRandomly(sz)
    elif (action == "2"):
        sud = Sudoku.initializeFromInput()
        if sud is None:
            return
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
