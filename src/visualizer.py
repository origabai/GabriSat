from graph_coloring import GraphColoring
import webbrowser
from graphUI_utils import GraphUtils
import logging

from dash import Dash, Input, Output, State

'''
a class that shows a graph, allowing it to be edited visually.

main method is .show() - which actually visualizes the graph.
.show() returns the graph coloring problem which corresponds to what the user has edited
in the editing window.

'''

class Visualizer:
    def __init__(self, graph : GraphColoring, solution = None, Ham_solution = None, found_solution = True):
        self.graph = graph
        self.correct_end = False
        self.edges = self.graph.edges
        self.num_nodes = self.graph.num_nodes
        self.max_colors = self.graph.max_colors
        self.found_solution = found_solution
        
        self.special_edges = None
        
        
        self.special_edges = self.generate_edges(Ham_solution)
        
        self.task = "COLOR"
        self.color_storage_for_termination = []
        self.COLORS = ["red", "green", "blue", "yellow", "purple", "pink", "magenta", "lime", "cyan"]
        #remembering colours
        if solution:
            self.numerical_colors = solution
        else:
            self.numerical_colors = self.graph.colors
            
        #deciding visualization colours
        self.colors = [self.color_gen(color) for color in self.numerical_colors]
        
    #to pass the test with flying colors
    def color_gen(self, color : int | None) -> str:
        if color is None:
            return "grey"
        
        return self.COLORS[color % len(self.COLORS)]
    
    #takes string returns color
    def color_to_num(self, color : str) -> int:
        if color == "grey":
            return None
        else:
            return self.COLORS.index(color)
    
    def generate_edges(self, Ham_solution):
            special = []
            if Ham_solution is not None:
                special = [[Ham_solution[-1],Ham_solution[0]]]
                for i in range(len(Ham_solution)-1):
                    special.append([Ham_solution[i],Ham_solution[i+1]])
            return special
        
        
    #show result
    def show(self) -> tuple[bool, GraphColoring]:
        initial_elements = GraphUtils.generate_initial_data(self.num_nodes, self.edges, self.colors, self.special_edges)
        
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        app = Dash(__name__)
        helper = GraphUtils(app, self)
        app.layout = helper.default_layout(initial_elements, self.found_solution)
        #helper = GraphUtils(app, self)
        #app.layout = helper.default_layout(initial_elements)



        app.run()
        self.color_storage_for_termination.sort(key = lambda tup : tup[0])
        color_array = [element[1] for element in self.color_storage_for_termination]
        #print(self.edges)
        return self.correct_end, GraphColoring(self.num_nodes, self.edges, color_array, self.max_colors)

