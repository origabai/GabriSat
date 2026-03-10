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
        
        #TODO make inital data equal to graph
        initial_elements = [
            {'data': {'id': '1', 'label': 'Node A', 'color': 'blue'}},
            {'data': {'id': '2', 'label': 'Node B', 'color': 'red'}},
            {'data': {'source': '1', 'target': '2'}}
        ]
        app = Dash(__name__)
        app.layout = html.Div([
            html.H3("Dynamic Graph Editor"),
            
            dcc.Store(id="erase_toggled", storage_type='memory', data = {'toggled' : False}),
            
            # Control Panel for Adding Nodes
            html.Div([
                #dcc.Input(id='input-node-id', type='text', placeholder='New Node ID (e.g., C)'),
                #dcc.Input(id='input-node-label', type='text', placeholder='Node Label'),
                html.Button('Add Node', id='btn-add-node', n_clicks=0)
            ], style={'marginBottom': '10px'}),
            
            # Control Panel for Adding Edges
            html.Div([
                dcc.Input(id='input-edge-source', type='text', placeholder='Source Node ID'),
                dcc.Input(id='input-edge-target', type='text', placeholder='Target Node ID'),
                html.Button('Add Edge', id='btn-add-edge', n_clicks=0)
            ], style={'marginBottom': '20px'}),

            html.Div([
                html.Button('Erase button', id='btn-erase', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0)
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
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )
        def add_node(n_clicks, current_elements):
            #finds existing nodes
            current_nodes = [int(element['data']['id']) for element in current_elements if 'target' not in element['data']]
            #finds next node to add
            next_id = min(set(range(1,len(current_nodes)+2))-set(current_nodes))
            # Construct the new node dictionary and append it to the state
            new_node = {'data': {'id': str(next_id), 'label': str(next_id)}}
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
        
        @app.callback(
            Output('erase_toggled', 'data'),
            Output('btn-erase', 'style'),
            Input('btn-erase', 'n_clicks')
        )
        def switch_erasing_mode(n_clicks):
            if n_clicks%2 == 0:
                return {'toggled' : False}, {'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'}
            else:
                return {'toggled' : True}, {'backgroundColor': 'red', 'color': 'black', 'padding': '10px'}
        
        @app.callback(
            Output('interactive-graph', 'elements'),
            Input('interactive-graph', 'tapNodeData'),
            State('interactive-graph', 'elements'),
            State('erase_toggled', 'data'),
            prevent_initial_call=True
        )
        def erase_clicked_node(tapped_node, current_elements, erase_mode):
            # Base case: The app just loaded, and no node has been clicked yet.
            if tapped_node is None or not erase_mode['toggled']:
                return current_elements
            
            # Extract the mathematical or topological data from the dictionary
            node_id = tapped_node.get('id', 'Unknown')
            #node_label = tapped_node.get('label', 'No Label')
            # Return formatted HTML to update the DOM
            return [element for element in current_elements if not(
                    element['data']['id'] == node_id or
                    ('source' in element['data'] and element['data']['source'] == node_id) or
                    ('target' in element['data'] and element['data']['target'] == node_id))
                    ]   
        
        @app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('interactive-graph', 'tapEdgeData'),
            State('interactive-graph', 'elements'),
            State('erase_toggled', 'data'),
            prevent_initial_call=True
        )
        def erase_clicked_edge(tapped_edge, current_elements, erase_mode):
            # Base case: The app just loaded, and no node has been clicked yet.
            print("TRYING")
            if tapped_edge is None or not erase_mode['toggled']:
                return current_elements
            print("TRYING AGAIN")
            # Extract the mathematical or topological data from the dictionary
            edge_src = tapped_edge.get('source', 'Unknown')
            edge_target = tapped_edge.get('target', 'Unknown')
            print(edge_src, edge_target)
            #node_label = tapped_node.get('label', 'No Label')
            # Return formatted HTML to update the DOM
            return [element for element in current_elements if not(
                    (('source' in element['data'] and element['data']['source'] == edge_src) and
                    ('target' in element['data'] and element['data']['target'] == edge_target)) or
                    ('source' in element['data'] and element['data']['source'] == edge_target) and
                    ('target' in element['data'] and element['data']['target'] == edge_src))
                    
                    ]   
            
        
        
        
        print("hi?")
        webbrowser.open('http://localhost:8050')
        app.run(debug=True)
        print("bi?")

