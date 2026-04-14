from graph import Graph
from constants import DEFAULT_SOLVER
from SAT_reducible_problem import SATReducibleProblem
from random import shuffle, randint

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
        adj = [[False for i in range(size)] for i in range(size)]
        # generate a lot of random edges
        for i in range(size):
            for j in range(i+1,size):
                if (randint(0,1) == 1):
                    adj[i][j] = True
                    adj[j][i] = True
        # force a random permutation to be a cycle
        a = [i for i in range(size)]
        shuffle(a)
        for i in range(size):
            adj[a[i]][a[(i+1)%size]] = True
            adj[a[(i+1)%size]][a[i]] = True
        for i in range(size):
            for j in range(i+1,size):
                if (adj[i][j]):
                    g.edges.append([i,j])
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
    
    # alternative reduction
    def solve2(self):
        s = self.solver(len(self.edges))
        adj_list = [[] for i in range(self.num_nodes)]
        for e in self.edges:
            adj_list[e[0]].append[e[1]]
            adj_list[e[1]].append[e[0]]
        for v in range(self.num_nodes):
            # every 
            for a in range(len(adj_list[v])):
                for b in range(a+1, len(adj_list[v])):
                    for c in range(b+1, len(adj_list[v])):
                        s.addClause([], [adj_list[v][a],adj_list[v][b],adj_list[v][c]])
        