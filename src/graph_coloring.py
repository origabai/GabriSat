from graph import Graph
from constants import DEFAULT_SOLVER
from random import randint
from SAT_reducible_problem import SATReducibleProblem


class GraphColoring(Graph, SATReducibleProblem):
    # colors is an array representing the initial colors, or None if no color is set
    def __init__(
        self,
        num_nodes: int,
        edges: list[list[int]],
        colors: list[int],
        max_colors: int,
        satsolver=DEFAULT_SOLVER,
    ):
        Graph.__init__(self, num_nodes, edges)
        SATReducibleProblem.__init__(self, satsolver)
        self.colors = colors
        self.max_colors = max_colors

    @classmethod
    def generate(
        self, num_of_nodes: int = 2, max_colors: int = 2, solver=DEFAULT_SOLVER
    ):
        g = GraphColoring(
            num_of_nodes, 0, [], max_colors, satsolver=solver
        )  # max colors is a random constant fraction
        g.generate_interesting_graph()
        return g

    # generates a random graph, and random coloring
    def generate_random(self):
        super().generate_random()
        self.colors = []
        for i in range(self.num_nodes):
            if randint(0, 1) == 0:
                self.colors.append(None)
            else:
                self.colors.append(randint(0, self.max_colors - 1))

    """
    Generates a dense graph with num_nodes nodes(which was given to __init__),
    and with coloring number ~ max_colors
    """

    def generate_interesting_graph(self):
        group = [randint(0, self.max_colors - 1) for i in range(self.num_nodes)]
        self.colors = [None for i in range(self.num_nodes)]
        self.edges = []
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if group[i] != group[j]:
                    if randint(0, 3) < 3:
                        self.edges.append([i, j])

    """
    initalizes a graph from input in the following format:
    num_nodes
    num_edges
    A[0] B[0]
    A[1] B[1]
    ...
    A[num_edges-1] B[num_edges-1]

    and colors in the following format:

    max_colors
    C[0]
    C[1]
    ...
    C[num_nodes]

    where C[i] can be -1 if the node is not assigned a color
    """

    def generate_from_input(self):
        super().generate_from_input()
        self.max_colors = int(input("Input max colors: "))
        self.colors = []
        for i in range(self.num_nodes):
            color = int(
                input("input color of node " + str(i) + " or -1 if unassigned: ")
            )
            if color == -1:
                self.colors.append(None)
            else:
                self.colors.append(color)

    # returns an array of numbers representing colors of a valid coloring, or None if none exists
    def solve(self) -> list[int] | None:
        sat = self.reduce_to_SAT()

        solution: list[bool] | None = sat.solve()

        return self.reconstruct_solution_from_reduction(solution)

    # reduces the problem to a SAT, returns a SAT solver of the type self has
    def reduce_to_SAT(self):
        sat = self.solver(self.max_colors * self.num_nodes)
        # add general clauses for color relations
        for i in range(self.num_nodes):
            sat.addClause([i * self.max_colors + j for j in range(self.max_colors)], [])
            for j in range(self.max_colors):
                for k in range(j + 1, self.max_colors):
                    sat.addClause(
                        [], [i * self.max_colors + j, i * self.max_colors + k]
                    )

        # add clauses to satisfy edge constraints
        for edge in self.edges:
            for j in range(self.max_colors):
                sat.addClause(
                    [], [edge[0] * self.max_colors + j, edge[1] * self.max_colors + j]
                )

        # add clauses to satisfy inital colors
        for i in range(self.num_nodes):
            if self.colors[i] is None:
                continue
            for j in range(self.max_colors):
                if self.colors[i] == j:
                    sat.addClause([i * self.max_colors + j], [])
                else:
                    sat.addClause([], [i * self.max_colors + j])
        return sat

    # takes a solution from the reduction to a SAT problem and returns a solution to this problem
    def reconstruct_solution_from_reduction(
        self, solution: list[bool] | None
    ) -> list[int] | None:
        if solution is None:
            return None
        answer = self.colors
        for i in range(self.num_nodes):
            for j in range(self.max_colors):
                if solution[i * self.max_colors + j]:
                    answer[i] = j
                    break
        return answer
