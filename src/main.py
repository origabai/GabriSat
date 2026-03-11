import copy
from graph_coloring import GraphColoring
from sudoku import Sudoku
from visualizer import Visualizer
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
from sudoku_visualizer import SudokuVisualizer
from constants import (
    DEFAULT_SOLVER,
    TrivialSATSolver,
    TrivialBacktrackingSolver,
    SAT_backtracking,
)
from SAT import AbstractSATSolver

from webbrowser import open as webopen

def benchmark_times():
    print("Starting time benchmark")
    print(
        "Average time to 10-color a 20 vertex graph:",
        test_time(GraphColoring.generate(), 20),
    )
    print(
        "Average time to find a hamiltonian cycle on a 7 vertex graph:",
        test_time(HamiltonianCycle.generate(), 7),
    )
    print(
        "Average time to solve a 4x4 sudoku(very hard):",
        test_time(Sudoku.generate(), 4),
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
        #create image
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
    action = input("Would you like to generate a random sudoku(1), or input one yourself(2)? (1 or 2)")
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


# compares the results of different SAT solvers and prints the results
# solvers is a list of classes of SAT solvers, num_vars is an int representing
# the desired amount of sat variables to generate randomly, num_clauses is an int
# representing the desired amount of sat clauses to generate randomly
def compare_SATs(
    solvers=[TrivialBacktrackingSolver, SAT_backtracking],
    num_vars: int = 20,
    num_clauses: int = 10,
) -> None:
    random_sat: AbstractSATSolver = AbstractSATSolver.generate_random(  # generating SAT
        num_vars, num_clauses, DEFAULT_SOLVER
    )
    for clause in random_sat.clauses:  # generating clauses for the SAT
        print(f"pos: {clause.pos_variables} | neg: {clause.neg_variables}")
    sats = [solver(num_vars) for solver in solvers]
    for sat in sats:  # copying the SAT for the different solvers
        for clause in random_sat.clauses:
            sat.addClause(clause.pos_variables.copy(), clause.neg_variables.copy())
    sols = [sat.solve() for sat in sats]  # solving with each solver
    for i in range(len(sats)):  # printing the results
        print(f"{type(sats[i])} got the following solution:")
        print(sols[i])


def main():
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
