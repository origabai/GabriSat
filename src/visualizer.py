from graph_coloring import GraphColoring
import webbrowser
from graphUI_utils import GraphUtils
import logging

from dash import Dash, Input, Output, State

'''
a class that shows a graph, allowing it to be edited visually.
generate_initial_data
main method is .show() - which actually visualizes the graph.
.show() returns the graph coloring problem which corresponds to what the user has edited
in the editing window.

'''

class Visualizer:
    def __init__(self, graph : GraphColoring, Ham_solution = None):
        self.graph = graph
        self.correct_end = False
        self.COLORS = ["red", "green", "blue", "yellow", "purple", "pink", "magenta", "lime", "cyan"]
        
    #to pass the test with flying colors
    def color_gen(self, color : int | None) -> str:
        if color == -1 or color is None:
            return "grey"
        
        return self.COLORS[color % len(self.COLORS)]
    
    def get_color_at_node(self, node):
        return self.color_gen(self.graph.colors[node])
    
    def generate_color_array(self, color_list : list[int]) -> list[str]:
        if color_list is None:
            color_list = self.graph.colors
        return [self.color_gen(color) for color in color_list]
    
    #takes string returns color
    def color_to_num(self, color : str) -> int:
        if color == "grey":
            return -1
        else:
            return self.COLORS.index(color)
    
    #generate coloured edges from hamiltonian solution
    def generate_edges(self, Ham_solution):
        if Ham_solution is None or Ham_solution == []:
            return []
        
        special = [[Ham_solution[-1],Ham_solution[0]]]
        for i in range(len(Ham_solution)-1):
            special.append([Ham_solution[i],Ham_solution[i+1]])
            
        return special
        
        
    #start up dash - the visual interface
    def show(self) -> tuple[bool, GraphColoring]:
        #set up logger
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        
        #start the app
        app = Dash(__name__)
        helper = GraphUtils(app, self)
        app.layout = helper.layout
        app.run()
        
        #return the graph as it is at the end - and an indicator of success/failure.
        return self.correct_end, self.graph

