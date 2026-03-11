from constants import TrivialBacktrackingSolver, TrivialSATSolver, SAT_backtracking, DEFAULT_SOLVER
from SAT import AbstractSATSolver
from graph_coloring import GraphColoring
import copy

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
        random_graph: GraphColoring = GraphColoring.generate(  # generating SAT
            num_of_nodes, max_colors, DEFAULT_SOLVER
        )
        print(f"edges: {random_graph.edges}")
        print(f"colors: {random_graph.colors}")
        graphs = [
            GraphColoring(
                num_of_nodes,
                copy.deepcopy(random_graph.edges),
                random_graph.colors.copy(),
                max_colors,
                solver,
            )
            for solver in solvers
        ]
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


# takes a graph and a list of indexes representing nodes and removes all edges containing these nodes,
# and then changes the rest of the indexes so they don't have any gaps
# num_of_nodes is the number of nodes in the graph, edges is the edges of the graph,
# to_remove is a set of the indexes to remove
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