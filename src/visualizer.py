from graph_coloring import GraphColoring
from pyvis.network import Network

class Visualizer:
    def __init__(self, graph : GraphColoring, solution = None):
        self.edges = graph.edges
        self.num_nodes = graph.num_nodes
        
        #remembering colours
        if solution:
            numerical_colors = solution
        else:
            numerical_colors = graph.colors
            
        #deciding visualization colours
        self.colors = [self.color_gen(color) for color in numerical_colors]
        
    #to pass the test with flying colors
    def color_gen(self, color : int | None) -> str:
        if color is None:
            return "grey"
        
        COLORS = ["red", "green", "blue", "yellow", "purple", "pink", "purple", "magenta", "lime", "cyan"]
        return COLORS[color % len(COLORS)]
    
    #show result
    def show(self) -> None:
        net = Network()
        labels = [str(i) for i in range(self.num_nodes)]
        net.add_nodes(list(range(self.num_nodes)), color = self.colors, label = labels)
        net.add_edges(self.edges)
        
        net.show('visual.html', notebook = False)