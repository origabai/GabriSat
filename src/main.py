import copy
from graph_coloring import GraphColoring
from sudoku import Sudoku
from visualizer import Visualizer
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
from pynput.keyboard import Controller, Key 
from sys import setrecursionlimit

from webbrowser import open as webopen

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
    vis()


if __name__ == "__main__":
    main()
