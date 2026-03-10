from graph import Graph
from SAT import DEFAULT_SOLVER
from SAT_reducible_problem import SATReducibleProblem

class HamiltonianCycle(Graph, SATReducibleProblem):
    def __init__(self, num_nodes: int, edges: list[list[int]], satsolver = DEFAULT_SOLVER):
        Graph.__init__(self,num_nodes,edges)
        SATReducibleProblem.__init__(self,satsolver)
    
    @classmethod
    def generate(self, size = 2, solver = DEFAULT_SOLVER):
        g = HamiltonianCycle(size, [], satsolver=solver)
        g.generate_random()
        return g

    # returns a hamiltonian cycle if exists, or None otherwise
    def solve(self):
        self.adj = [[False for i in range(self.num_nodes)] for i in range(self.num_nodes)]
        for e in self.edges:
            self.adj[e[0]][e[1]] = True
            self.adj[e[1]][e[0]] = True
        s = self.solver(self.num_nodes * self.num_nodes)
        # ensure it is a permutation
        for i in range(self.num_nodes):
            s.addClause([self.num_nodes*i + j for j in range(self.num_nodes)],[])
            for j in range(self.num_nodes):
                for k in range(j+1,self.num_nodes):
                    s.addClause([],[self.num_nodes*i + j, self.num_nodes*i + k])
                    s.addClause([],[self.num_nodes*j + i, self.num_nodes*k + i])

        # ensure every adjacent pair is connected
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                for k in range(j+1,self.num_nodes):
                    if (self.adj[j][k]):
                        continue
                    s.addClause([],[self.num_nodes*(i) + j, self.num_nodes*((i+1)%self.num_nodes) + k])
                    s.addClause([],[self.num_nodes*((i+1)%self.num_nodes) + j, self.num_nodes*(i) + k])
        
        solution = s.solve()
        if (solution is None):
            return None
        ans = []
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if (solution[self.num_nodes*i + j]):
                    ans.append(j)
                    break
        return ans