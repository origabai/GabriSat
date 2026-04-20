from graph import Graph
from constants import DEFAULT_SOLVER
from SAT_reducible_problem import SATReducibleProblem
from random import shuffle, randint
from constants import HAMCYCLE_GENERATION_CONST
from DSU import DSU

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
        
        # randomly ensure hamcycle
        if (randint(0,1) == 0):
            perm = [i for i in range(size)]
            shuffle(perm)
            for i in range(size):
                g.edges.append([perm[i], perm[(i+1)%size]])
        return g

    # returns a hamiltonian cycle if exists, or None otherwise
    # bad reduction, 0/10 סייבר
    def solve2(self):
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

    # generates a SAT problem with the initial constraints for the cool reduction
    # and returns it
    def generate_initial_cool_reduction(self):
        self.generate_adjacency_matrix()
        s = self.solver(len(self.edges))

        adj_list = [[] for i in range(self.num_nodes)]
        for i in range(len(self.edges)):
            e = self.edges[i]
            adj_list[e[0]].append(i)
            adj_list[e[1]].append(i)

        for v in range(self.num_nodes):
            # there are strictly less than three חבר'ה connected to every vertex
            for a in range(len(adj_list[v])):
                for b in range(a+1, len(adj_list[v])):
                    for c in range(b+1, len(adj_list[v])):
                        s.addClause([], [adj_list[v][a],adj_list[v][b],adj_list[v][c]])
            # there is at least one edge connected to every vertex
            s.addClause([x for x in adj_list[v]], [])
            # there are at least two vertices connected to every vertex
            for a in range(len(adj_list[v])):
                clause = []
                for b in range(len(adj_list[v])):
                    if a != b:
                        clause.append(adj_list[v][b])
                s.addClause(clause, [])
        return s

    # alternative variation of the cool reduction
    # where all cycles are added as cuts
    # way faster!
    def solve(self):
        # if the graph is not connected, don't even bother
        if not self.is_connected():
            return None
        # ok it's connected 👍
        s = self.generate_initial_cool_reduction()
        # start back-and-forth with the satsolver
        while True:
            sol = s.solve()
            if sol is None:
                return None
            # decompose the graph of the chosen edges into connected components
            ds = DSU(self.num_nodes)
            for i in range(len(self.edges)):
                if (not sol[i]):
                    continue
                e = self.edges[i]
                ds.unite(e[0], e[1])
            if ds.components() == 1:
                # we found a hamcycle!
                neighbors = [[] for i in range(self.num_nodes)]
                for i in range(len(self.edges)):
                    if (not sol[i]):
                        continue
                    e = self.edges[i]
                    neighbors[e[0]].append(e[1])
                    neighbors[e[1]].append(e[0])
                cycle = [0]
                vis = [False for i in range(self.num_nodes)]
                while True:
                    v = cycle[-1]
                    vis[v] = True
                    flag = True
                    for u in neighbors[v]:
                        if (not vis[u]):
                            flag = False
                            cycle.append(u)
                            break
                    if (flag):
                        break
                return cycle
            else:
                # fake hamcycle, need to add everything to cuts
                cycles = [0 for i in range(self.num_nodes)]
                for i in range(self.num_nodes):
                    cycles[ds.find(i)] += 1
                for i in range(self.num_nodes):
                    if cycles[i] == 0:
                        continue
                    clause = []
                    for e in range(len(self.edges)):
                        a = self.edges[e][0]
                        b = self.edges[e][1]
                        if (ds.find(a) == i and ds.find(b) != i) or (ds.find(a) != i and ds.find(b) == i):
                            clause.append(e)
                    s.addClause(clause, [])
