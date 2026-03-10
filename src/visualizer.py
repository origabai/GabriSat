from graph_coloring import GraphColoring
import webbrowser
from graphUI_utils import GraphUtils


from dash import Dash, Input, Output, State

'''
a class that shows a graph, allowing it to be edited visually.

main method is .show() - which actually visualizes the graph.
.show() returns the graph coloring problem which corresponds to what the user has edited
in the editing window.

'''
class Visualizer:
    def __init__(self, graph : GraphColoring, solution = None):
        self.edges = graph.edges
        self.num_nodes = graph.num_nodes
        self.max_colors = graph.max_colors
        self.color_storage_for_termination = []
        self.COLORS = ["red", "green", "blue", "yellow", "purple", "pink", "magenta", "lime", "cyan"]
        #remembering colours
        if solution:
            self.numerical_colors = solution
        else:
            self.numerical_colors = graph.colors
            
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
        
        
        
    #show result
    def show(self) -> None:
        initial_elements = GraphUtils.generate_initial_data(self.num_nodes, self.edges, self.colors)
        
        app = Dash(__name__)
        app.layout = GraphUtils.default_layout(initial_elements)
        
        
        @app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('btn-add-node', 'n_clicks'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )
        def add_node(n_clicks, current_elements):
            return GraphUtils.add_node(n_clicks, current_elements)



        # Callback to add a new edge
        @app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('btn-add-edge', 'n_clicks'),
            State('input-edge-source', 'value'),
            State('input-edge-target', 'value'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )
        def add_edge(n_clicks, source_id, target_id, current_elements):
            return GraphUtils.add_edge(n_clicks, source_id, target_id, current_elements)
        
        
        
        @app.callback(
            Output('erase_toggled', 'data'),
            Output('btn-erase', 'style'),
            Input('btn-erase', 'n_clicks')
        )
        def switch_erasing_mode(n_clicks):
            return GraphUtils.switch_erasing_mode(n_clicks)
        
        
        
        @app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('interactive-graph', 'tapNodeData'),
            State('interactive-graph', 'elements'),
            State('multi-colour-selector', 'value'),
            State('erase_toggled', 'data'),
            prevent_initial_call=True
        )
        def process_node_click(tapped_node, current_elements, selected_colour ,erase_mode):
            return GraphUtils.process_node_click(tapped_node, current_elements, selected_colour ,erase_mode)
        
        
        
        @app.callback(
            Input('btn-end', 'n_clicks'),
            State('interactive-graph', 'elements'),
        )
        def end_visualization(n_clicks, elements):
            return GraphUtils.end_visualization(n_clicks, elements, self)
        


        webbrowser.open('http://localhost:8050')
        try:
            app.run()
        except KeyboardInterrupt:
            self.color_storage_for_termination.sort(key = lambda tup : tup[0])
            color_array = [element[1] for element in self.color_storage_for_termination]
            
            print(color_array)
            return GraphColoring(self.num_nodes, self.edges, color_array, self.max_colors)

