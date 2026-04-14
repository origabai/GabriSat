from graph import Graph
from constants import DEFAULT_SOLVER
from SAT_reducible_problem import SATReducibleProblem
from random import shuffle, randint
from constants import HAMCYCLE_GENERATION_CONST

class HamiltonianCycle(Graph, SATReducibleProblem):
    def __init__(self, num_nodes: int, edges: list[list[int]], satsolver = DEFAULT_SOLVER):
        Graph.__init__(self,num_nodes,edges)
        SATReducibleProblem.__init__(self,satsolver)
    
    def validate(self, sol):
        ssol = sorted(sol)
        # validate it is a permutation
        if (ssol != [i for i in range(len(sol))]):
            return False
        # construct adj matrix
        adj = [[False for i in range(self.num_nodes)] for i in range(self.num_nodes)]
        for e in self.edges:
            adj[e[0]][e[1]] = True
            adj[e[1]][e[0]] = True
        # validate it is a cycle
        for i in range(len(sol)):
            if (not adj[sol[i]][sol[(i+1)%len(sol)]]):
                return False
        return True



    @classmethod
    def generate(self, size = 2, solver = DEFAULT_SOLVER):
        g = HamiltonianCycle(size, [], satsolver=solver)
        # make a random tree, and add HAMCYCLE_GENERATION_CONST*N edges to it
        for i in range(1,size):
            g.edges.append([i, randint(0, i-1)])

        for i in range(HAMCYCLE_GENERATION_CONST*size):
            a = randint(0,size-1)
            b = randint(0, size-1)
            if (a != b):
                g.edges.append([a,b])
        
        # ensure hamcycle
        perm = [i for i in range(size)]
        shuffle(perm)
        for i in range(size):
            g.edges.append([perm[i], perm[(i+1)%size]])
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