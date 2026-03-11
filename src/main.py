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
        "Average time to 3-color a 6 vertex graph:",
        test_time(GraphColoring.generate(), 6),
    )
    print(
        "Average time to find a hamiltonian cycle on a 4 vertex graph:",
        test_time(HamiltonianCycle.generate(), 4),
    )
    print(
        "Average time to solve a 4x4 sudoku(expert level):",
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
    webopen("http://localhost:8050")
    # driver = webdriver.Brave()
    # driver.get('http://localhost:8050')
    while True:
        # create image
        vis = Visualizer(color_graph, solution, Ham_solution, found_solution)
        # driver.refresh()
        webopen("http://localhost:8050")
        # initialize solutions to none
        solution = None
        found_solution = True
        Ham_solution = None
        color_graph = vis.show()
        # print("TASK IS:", vis.task)
        # depending on the task, solve and update the solution
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
    # sud = Sudoku.initializeRandomly(9)
    sud = Sudoku.initializeFromInput()
    vis.visualize_sudoku(copy.deepcopy(sud.board))
    input("Press enter to calculate solution")
    sol = sud.solve()
    if sol is None:
        print("No solution")
    else:
        vis.visualize_sudoku(sol)
        input("Press enter to exit")


# compares the results of different SAT solvers on randomly generated SATs for num_of_tests tests,
# and prints the results only when some think a solution exists and some don't
# solvers is a list of classes of SAT solvers, num_vars is an int representing
# the desired amount of sat variables to generate randomly, num_clauses is an int
# representing the desired amount of sat clauses to generate randomly
def compare_solvers_on_SATs(
    num_of_tests: int = 100,
    solvers=[TrivialBacktrackingSolver, SAT_backtracking],
    num_vars: int = 20,
    num_clauses: int = 10,
) -> None:
    for _ in range(num_of_tests):
        random_sat: AbstractSATSolver = (
            AbstractSATSolver.generate_random(  # generating SAT
                num_vars, num_clauses, DEFAULT_SOLVER
            )
        )
        sats = [solver(num_vars) for solver in solvers]
        for sat in sats:  # copying the SAT for the different solvers
            for clause in random_sat.clauses:
                sat.addClause(clause.pos_variables.copy(), clause.neg_variables.copy())
        sols = [sat.solve() for sat in sats]  # solving with each solver
        if None in sols and any(
            [sol is not None for sol in sols]
        ):  # solutions don't agree
            for clause in random_sat.clauses:  # printing the test
                print(f"pos: {clause.pos_variables} | neg: {clause.neg_variables}")
            for i in range(len(sats)):  # printing the results
                print(f"{type(sats[i])} got the following solution:")
                print(sols[i])
            return False  # solvers disagree
    return True  # solvers agree


# compares the results of different SAT solvers on randomly generated graph colorings for num_of_tests tests,
# and prints the results only when some think a solution exists and some don't
# solvers is a list of classes of SAT solvers, num_vars is an int representing
# the desired amount of sat variables to generate randomly, num_clauses is an int
# representing the desired amount of sat clauses to generate randomly
def compare_solvers_on_graph_coloring(
    num_of_tests: int = 10,
    solvers=[TrivialBacktrackingSolver, SAT_backtracking],
    num_of_nodes: int = 10,
    max_colors: int = 5,
) -> None:
    for i in range(num_of_tests):
        random_graph: GraphColoring = (
            GraphColoring.generate(  # generating SAT
                num_of_nodes, max_colors, DEFAULT_SOLVER
            )
        )
        print(f"edges: {random_graph.edges}")
        print(f"colors: {random_graph.colors}")
        graphs = [GraphColoring(num_of_nodes, copy.deepcopy(random_graph.edges), random_graph.colors.copy(), max_colors, solver) for solver in solvers]
        sols = [graph.solve() for graph in graphs]  # solving with each solver
        if None in sols and any(
            [sol is not None for sol in sols]
        ):  # solutions don't agree
            print(f"edges: {random_graph.edges}")
            print(f"colors: {random_graph.colors}")
            for i in range(len(graphs)):  # printing the results
                print(f"{type(solvers[i])} got the following solution:")
                print(sols[i])
            return False  # solvers disagree
        print(f"{i + 1} / {num_of_tests} tests looks good")
    return True  # solvers agree



def remove_from_graph(num_of_nodes: int, edges: list[list[int]], to_remove: set[int]):
    to_keep: list[int] = []
    for i in range(num_of_nodes):
        if i not in to_remove:
            to_keep.append(i)
    d = {}
    for i, e in enumerate(sorted(to_keep)):
        d[e] = i
    new_edges: list[list[int]] = []
    for edge in edges:
        a: int = edge[0]
        b: int = edge[1]
        if a not in d.keys() or b not in d.keys():
            continue
        new_edges.append([d[a], d[b]])
    edges.clear()
    for edge in new_edges:
        edges.append(edge)

def main():
    # if compare_solvers_on_graph_coloring(10, [TrivialBacktrackingSolver, SAT_backtracking], 10, 5):
    #     print("yay")
    # num_of_nodes = 10
    # edges = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 9], [2, 5], [2, 6], [2, 7], [2, 9], [3, 4], [3, 7], [4, 5], [4, 6], [4, 7], [5, 7], [5, 8], [5, 9], [6, 7], [6, 8], [7, 8]]
    # to_remove: set[int] = set([0, 1, 5, 8, 9])
    # remove_from_graph(num_of_nodes, edges, to_remove)
    # num_of_nodes -= len(to_remove)
    # colors = [None for _ in range(num_of_nodes)]
    # max_colors = 5
    # print(edges)

    # num_of_nodes = 5
    # edges = [[0, 3], [0, 4], [1, 2], [1, 4], [2, 3], [2, 4], [3, 4]]
    # colors = [None for _ in range(num_of_nodes)]
    # max_colors = 3

    # graph = GraphColoring(num_of_nodes, copy.deepcopy(edges), colors.copy(), max_colors, SAT_backtracking)
    # sat: AbstractSATSolver = graph.reduce_to_SAT()
    # print(len(sat.clauses))
    # print(sat.solve())
    
    # graph1 = GraphColoring(num_of_nodes, copy.deepcopy(edges), colors.copy(), max_colors, TrivialBacktrackingSolver)
    # print(graph1.solve())
    # graph2 = GraphColoring(num_of_nodes, copy.deepcopy(edges), colors.copy(), max_colors, SAT_backtracking)
    # print(graph2.solve())

    # return ####################################
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
