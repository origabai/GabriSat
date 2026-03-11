import copy
from graph_coloring import GraphColoring
from sudoku import Sudoku
from visualizer import Visualizer
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
from sudoku_visualizer import SudokuVisualizer
from constants import DEFAULT_SOLVER, TrivialSATSolver
from SAT import AbstractSATSolver

from webbrowser import open as webopen

def benchmark_times():
    print("Starting time benchmark")
    print(
        "Average time to 3-color a 6 vertex graph:",
        test_time(GraphColoring.generate(), 6),
    )
    print(
        "Average time to find a hamiltonian cycle on a 4 vertex graph:",
        test_time(HamiltonianCycle.generate(), 4),
    )
    print(
        "Average time to solve a 1x1 sudoku(expert level):",
        test_time(Sudoku.generate(), 1),
    )



'''runs loop for displaying output'''
def graph_vis():
    #bootstrap
    print("STARTING VISUAL EPICNESS")
    color_graph = GraphColoring(6, [[0,1],[0,2],[1,2],[2,3],[2,5],[5,4],[3,4]], [1,2,6,7,None,None], 3)
    solution = None
    Ham_solution = None
    webopen('http://localhost:8050')
    #driver = webdriver.Brave()
    #driver.get('http://localhost:8050')
    while True:
        #create image
        vis = Visualizer(color_graph, solution, Ham_solution)
        #driver.refresh()
        webopen('http://localhost:8050')
        #initialize solutions to none
        solution = None
        Ham_solution = None
        color_graph = vis.show()
        #print("TASK IS:", vis.task)
        #depending on the task, solve and update the solution
        match vis.task:
            case 'COLOR':
                #solve coloring problem
                solution = color_graph.solve()
                continue
            case "HAMPATH":
                #solve hampath problem
                ham_graph = HamiltonianCycle(color_graph.num_nodes,color_graph.edges)
                Ham_solution = ham_graph.solve()
                continue
            case "END":
                #end simulation
                break


def visualize_sudoku():
    vis = SudokuVisualizer()
    sud = Sudoku.initializeRandomly(4)
    vis.visualize_sudoku(copy.deepcopy(sud.board))
    input("Press enter to calculate solution")
    sol = sud.solve()
    if sol is None:
        print("No solution")
    else:
        vis.visualize_sudoku(sol)
        input("Press enter to exit")


def compare_SATs(
    solver1=DEFAULT_SOLVER,
    solver2=TrivialSATSolver,
    num_vars: int = 20,
    num_clauses: int = 10,
):
    solvers = [solver1, solver2]
    random_sat: AbstractSATSolver = AbstractSATSolver.generate_random(
        num_vars, num_clauses, DEFAULT_SOLVER
    )
    for clause in random_sat.clauses:
        print(f"pos: {clause.pos_variables} | neg: {clause.neg_variables}")
    sats = [solver(num_vars) for solver in solvers]
    for sat in sats:
        for clause in random_sat.clauses:
            sat.addClause(clause.pos_variables.copy(), clause.neg_variables.copy())
    sols = [sat.solve() for sat in sats]
    for i in range(len(sats)):
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
