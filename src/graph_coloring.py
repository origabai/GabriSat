from graph import Graph

class GraphColoring(Graph):
    # colors is an array representing the initial colors, or None if no color is set
    def __init__(self, num_nodes, edges, colors):
        super().__init__(num_nodes, edges)
        self.colors = colors

    def reduceToSAT(self):
        pass

    # returns an array of numbers representing colors of a valid coloring, or None if none exists
    def solve(self, max_colors):
        pass
    
    def initializeFromInput(self):
        pass

    def generateRandom(self):
        pass

