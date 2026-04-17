# disjoint set union data structure
class DSU:
    def __init__(self, n):
        self.n = n
        self.par = [i for i in range(n)]
        # num. of connected components
        self.comps = n

    # get the representative of the connected component containing v
    def find(self, v):
        if self.par[v] == v:
            return v
        self.par[v] = self.find(self.par[v])
        return self.par[v]

    # add an edge between u and v
    # returns True if they were in different componenets, and False otherwise
    def unite(self, v, u):
        v = self.find(v)
        u = self.find(u)
        if u == v:
            return False
        self.comps -= 1
        self.par[v] = u
        
    # returns number of connected components in the graph
    def components(self):
        return self.comps
        