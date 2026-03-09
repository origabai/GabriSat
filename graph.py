"""
An undirected graph
edges = array of edges, each of which is an array
of size 2 containing indices of the vertices it connects (0-indexed)
"""
class Graph:
    def __init__(self, num_nodes, edges):
        self.num_nodes = num_nodes
        self.edges = edges
    
    def generateRandom(self):
        pass