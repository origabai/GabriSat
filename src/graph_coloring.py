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

    def validate(self, sol):
        # check all colors are valid
        for x in sol:
            if x < 0 or x >= self.max_colors:
                return False
        # check coloring constraint on all edges
        for e in self.edges:
            if (sol[e[0]] == sol[e[1]]):
                return False
        return True

    @classmethod
    def generate(
        self, num_of_nodes: int = 2, solver=DEFAULT_SOLVER, max_colors: int = None
    ):
        if max_colors is None:
            max_colors = num_of_nodes // 2
        g = GraphColoring(
            num_of_nodes, [], [], max_colors, satsolver=solver
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

        # add colors to satisfy symmetry 
        
        SYMM_CHOICE = True
        temp_colors = []
        
        
        #print("missing colors are:", missing_colors)
        if SYMM_CHOICE:
            missing_colors = self.find_missing_colors()
            #print("I HAVEW ENETERED!!!!")
            degrees = self.find_highest_degree_nodes()
            colors = list(missing_colors)
            
            if len(colors) == self.max_colors:
                temp_colors.append((degrees[0][1], 0))
                self.colors[degrees[0][1]] = 0
            '''
            #print(f"the missing colors are {colors}")
            cur_node = 0
            cur_color = 0
            #print("before:", self.colors)
            while cur_node < self.max_colors and cur_color < len(colors):
                if self.colors[degrees[cur_node][1]] == None:
                    temp_colors.append((degrees[cur_node][1], cur_color))
                    self.colors[degrees[cur_node][1]] = cur_color
                    cur_color += 1
                cur_node += 1
            #print("after:", self.colors)
            '''
        
        
        #add clauses to satisfy initial colors
        for i in range(self.num_nodes):
            if self.colors[i] is None:
                continue
            for j in range(self.max_colors):
                if self.colors[i] == j:
                    sat.addClause([i * self.max_colors + j], [])
                else:
                    sat.addClause([], [i * self.max_colors + j])
                    
        #remove temporary color modifiers:
        
        for vertex, _ in temp_colors:
            self.colors[vertex] = None
        
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
    
    def find_highest_degree_nodes(self) -> list[int]:
        degrees = [[0, i] for i in range(self.num_nodes)]
        for e in self.edges:
            degrees[e[0]][0] += 1
            degrees[e[1]][0] += 1
        degrees.sort(key=lambda tup : tup[0])
        return degrees
    
    def find_missing_colors(self) -> list[int]:
        missing_colors = set(range(self.max_colors))
        for v in self.colors:
            if v is not None:
                try:
                    missing_colors.remove(v)
                except:
                    pass
        return missing_colors