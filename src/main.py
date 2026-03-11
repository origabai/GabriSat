from graph_coloring import GraphColoring
from sudoku import Sudoku
from visualizer import Visualizer
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
from sudoku_visualizer import SudokuVisualizer
from webbrowser import open as webopen
from selenium import webdriver

def benchmark_times():
    print("Starting time benchmark")
    print("Average time to 3-color a 6 vertex graph:",test_time(GraphColoring.generate(), 6))
    print("Average time to find a hamiltonian cycle on a 4 vertex graph:",test_time(HamiltonianCycle.generate(), 4))
    print("Average time to solve a 1x1 sudoku(expert level):",test_time(Sudoku.generate(), 1))


'''runs loop for displaying output'''
def graph_vis():
    #bootstrap
    print("STARTING VISUAL EPICNESS")
    color_graph = GraphColoring(0, [], [], 3)
    solution = None
    Ham_solution = None
    found_solution = True
    webopen('http://localhost:8050')
    while True:
        #create image
        vis = Visualizer(color_graph, solution, Ham_solution, found_solution)
        #initialize solutions to none
        solution = None
        found_solution = True
        Ham_solution = None
        color_graph = vis.show()
        #depending on the task, solve and update the solution
        match vis.task:
            case 'COLOR':
                #solve coloring problem
                solution = color_graph.solve()
                if solution is None:
                    found_solution = False
                continue
            case "HAMPATH":
                #solve hampath problem
                ham_graph = HamiltonianCycle(color_graph.num_nodes,color_graph.edges)
                Ham_solution = ham_graph.solve()
                if Ham_solution is None:
                    found_solution = False
                continue
            case "END":
                #end simulation
                break

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