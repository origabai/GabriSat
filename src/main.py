import copy
from graph_coloring import GraphColoring
from sudoku import Sudoku
from visualizer import Visualizer
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
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
        "Average time to find a hamiltonian cycle on a 10 vertex graph:",
        test_time(HamiltonianCycle.generate(), 10),
    )
    print(
        "Average time to solve a 16x16 sudoku:",
        test_time(Sudoku.generate(), 16),
    )


"""runs loop for displaying output"""


def vis():
    print("STARTING VISUAL EPICNESS")
    color_graph = GraphColoring(0, [], [], 3)
    webopen('http://localhost:8050')
    vis = Visualizer(color_graph)
    correct_end = vis.show()


def main():
    setrecursionlimit(3000)
    print("WELCOME TO VERY EPIC SAT SOLVER")
    print("What would you like to do?")
    print("1 - Benchmark solving times")
    print("2 - View visualizer")
    action = input("")
    if action == "1":
        benchmark_times()
    elif action == "2":
        vis()
    else:
        print("Not a valid option")


if __name__ == "__main__":
    main()
