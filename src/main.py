from graph_coloring import GraphColoring
from sudoku import Sudoku
from visualizer import Visualizer
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
from sudoku_visualizer import SudokuVisualizer
from constants import DEFAULT_SOLVER, TrivialSATSolver
from SAT import AbstractSATSolver, SATClause
import copy


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


def graph_vis():
    print("STARTING VISUAL EPICNESS")
    graph = GraphColoring(
        6,
        [[0, 1], [0, 2], [1, 2], [2, 3], [2, 5], [5, 4], [3, 4]],
        [1, 2, 6, 7, None, None],
        3,
    )
    vis = Visualizer(graph)
    graph = vis.show()
    solution = graph.solve()
    vis = Visualizer(graph, solution)
    vis.show()


def visualize_sudoku():
    vis = SudokuVisualizer()
    sud = Sudoku.initializeRandomly(9)
    # sud = Sudoku([[None]])
    vis.visualize_sudoku(copy.deepcopy(sud.board))
    input("Press enter to calculate solution")
    # vis.visualize_sudoku(sud.solve())
    sol = sud.solve()
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
    # compare_SATs(DEFAULT_SOLVER, TrivialSATSolver, 15, 20)
    # board = [[None for _ in range(4)] for _ in range(4)]
    # board[0][0] = 0
    # board[1][2] = 0
    # board[0][1] = 1
    # board[0][2] = 2
    # board[0][3] = 3
    # board[1][0] = 2
    # board[3][0] = 3
    # sud = Sudoku(board)
    # print(sud.solve())
    # sud = Sudoku.initializeRandomly(4)
    # print(sud.board)
    # print(sud.solve())
    # return  ############################
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
