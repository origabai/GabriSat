from random import randint

"""
An undirected graph
edges = array of edges, each of which is an array
of size 2 containing indices of the vertices it connects (0-indexed)
"""
class Graph:
    def __init__(self, num_nodes: int, edges: list[list[int]]):
        self.num_nodes = num_nodes
        self.edges = edges
    
    # generates a random graph
    def generate_random(self):
        self.edges = []
        for i in range(self.num_nodes):
            for j in range(i+1,self.num_nodes):
                if (randint(0,1) == 1):
                    self.edges.append([i,j])
    
    """
    initalizes a graph from input in the following format:
    num_nodes
    num_edges
    A[0] B[0]
    A[1] B[1]
    ...
    A[num_edges-1] B[num_edges-1]
    """
    def generate_from_input(self):
        self.num_nodes = input("Enter num of nodes: ")
        num_edges = input("Enter num of edges: ")
        self.edges = []
        for i in range(num_edges):
            edge = input("Enter edge: ").split(" ")
            edge = [int(s) for s in edge]
            self.edges.append(edge)
