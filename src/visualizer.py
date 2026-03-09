from graph_coloring import GraphColoring
from pyvis.network import Network
import webbrowser


from dash import Dash, html, Input, Output, State, dcc
import dash_cytoscape as cyto


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
        '''
        net = Network()
        labels = [str(i) for i in range(self.num_nodes)]
        net.add_nodes(list(range(self.num_nodes)), color = self.colors, label = labels)
        net.add_edges(self.edges)
        
        net.show('visual.html', notebook = False)
        '''
        
        initial_elements = [
            {'data': {'id': '1', 'label': 'Node A', 'color': 'blue'}},
            {'data': {'id': '2', 'label': 'Node B', 'color': 'red'}},
            {'data': {'source': '1', 'target': '2'}}
        ]
        app = Dash(__name__)
        app.layout = html.Div([
            html.H3("Dynamic Graph Editor"),
            
            # Control Panel for Adding Nodes
            html.Div([
                dcc.Input(id='input-node-id', type='text', placeholder='New Node ID (e.g., C)'),
                dcc.Input(id='input-node-label', type='text', placeholder='Node Label'),
                html.Button('Add Node', id='btn-add-node', n_clicks=0)
            ], style={'marginBottom': '10px'}),
            
            # Control Panel for Adding Edges
            html.Div([
                dcc.Input(id='input-edge-source', type='text', placeholder='Source Node ID'),
                dcc.Input(id='input-edge-target', type='text', placeholder='Target Node ID'),
                html.Button('Add Edge', id='btn-add-edge', n_clicks=0)
            ], style={'marginBottom': '20px'}),


            # The Cytoscape Canvas
            cyto.Cytoscape(
                id='interactive-graph',
                elements=initial_elements,
                layout={'name': 'cose'}, # Force-directed physics layout
                style={'width': '800px', 'height': '500px', 'border': '1px solid black'},
                stylesheet=[
                    # Basic styling to make labels visible
                    {'selector': 'node', 'style': {'label': 'data(id)', 'text-valign': 'center', 'background-color': 'data(color)'}},
                    {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'none'}}
                ]
            )
        ])
        @app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('btn-add-node', 'n_clicks'),
            State('input-node-id', 'value'),
            State('input-node-label', 'value'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )
        def add_node(n_clicks, node_id, node_label, current_elements):
            if not node_id:
                return current_elements # Do nothing if ID is empty
            
            # Construct the new node dictionary and append it to the state
            new_node = {'data': {'id': node_id, 'label': node_id}}
            current_elements.append(new_node)
            
            return current_elements


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
            if not source_id or not target_id:
                return current_elements # Do nothing if source/target are empty
            
            # Construct the new edge dictionary and append it to the state
            new_edge = {'data': {'source': source_id, 'target': target_id}}
            current_elements.append(new_edge)
            
            return current_elements
        
        print("hi?")
        webbrowser.open('http://localhost:8050')
        app.run(debug=True)
        print("bi?")

