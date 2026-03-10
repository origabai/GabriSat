from dash import Dash, html, Input, Output, State, dcc
import dash_cytoscape as cyto
import _thread

"""
provides utils for graph_visualizer.py
"""
class GraphUtils:
    
    def __init__(self, app : Dash, vis_object):
        self.vis_object = vis_object
        
        app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('btn-add-node', 'n_clicks'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(self.add_node)
        
        app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('btn-add-edge', 'n_clicks'),
            State('input-edge-source', 'value'),
            State('input-edge-target', 'value'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(self.add_edge)
        
        app.callback(
            Output('erase_toggled', 'data'),
            Output('btn-erase', 'style'),
            Input('btn-erase', 'n_clicks')
        )(self.switch_erasing_mode)
        
        app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('interactive-graph', 'tapNodeData'),
            State('interactive-graph', 'elements'),
            State('multi-colour-selector', 'value'),
            State('erase_toggled', 'data'),
            prevent_initial_call=True
        )(self.process_node_click)
        
        app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('interactive-graph', 'tapEdgeData'),
            State('interactive-graph', 'elements'),
            State('erase_toggled', 'data'),
            prevent_initial_call=True
        )(self.erase_clicked_edge)
        
        app.callback(
            Output('btn-end', 'children'),
            Input('btn-end', 'n_clicks'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(self.end_visualization)
    '''
    provides utils for graph_visualizer.py
    '''
    
    
    '''
    returns the standard layout of the html file given the default elements
    '''
    @staticmethod
    def generate_initial_data(nodes, edges, colors):
        initial_data = []
        
        for node in range(nodes):
            initial_data.append({'data' : {'id': str(node), 'label' : str(node), 'color': colors[node]}})
        
        for edge in edges:
            initial_data.append({'data' : {'source': str(edge[0]), 'target': str(edge[1])}})
        
        return initial_data
        
    
    @staticmethod
    def default_layout(initial_elements):
        return html.Div([
            html.H3("Dynamic Graph Editor"),
            
            dcc.Store(id="erase_toggled", storage_type='memory', data = {'toggled' : False}),
            dcc.Store(id="color_current", storage_type='memory', data = {'colour' : None}),
            
            # Control Panel for Adding Nodes
            html.Div([
                #dcc.Input(id='input-node-id', type='text', placeholder='New Node ID (e.g., C)'),
                #dcc.Input(id='input-node-label', type='text', placeholder='Node Label'),
                html.Button('Add Node', id='btn-add-node', n_clicks=0, style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'})
            ], style={'marginBottom': '10px'}),
            
            # Control Panel for Adding Edges
            html.Div([
                dcc.Input(id='input-edge-source', type='text', placeholder='Source Node ID'),
                dcc.Input(id='input-edge-target', type='text', placeholder='Target Node ID'),
                html.Button('Add Edge', id='btn-add-edge', n_clicks=0, style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'})
            ], style={'marginBottom': '20px'}),

            html.Div([
                html.Button('Erase button', id='btn-erase', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0)
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.Button('End visualization', id='btn-end', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0)
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.Label("Change node colour"),
                dcc.Dropdown(
                    id='multi-colour-selector',
                    options=[
                        # 'label' is what the user sees, 'value' is what Python receives
                        {'label': 'None (none selected)', 'value': None},
                        {'label': 'grey (no colour)', 'value': 'grey'},
                        {'label': 'red (0)', 'value': 'red'},
                        {'label': 'green (1)', 'value': 'green'},
                        {'label': 'blue (2)', 'value': 'blue'},
                        {'label': 'yellow (3)', 'value': 'yellow'},
                        {'label': 'purple (4)', 'value': 'purple'},
                        {'label': 'pink (5)', 'value': 'pink'},
                        {'label': 'magenta (6)', 'value': 'magenta'},
                        {'label': 'lime (7)', 'value': 'lime'},
                        {'label': 'cyan (8)', 'value': 'cyan'},
                    ],
                    value=[None], # The default selected array
                    multi=False,  # This strictly enforces multiple-choice behavior
                    style={'width': '300px', 'marginTop': '5px'}
                )
            ]),

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
    
    def add_node(self, n_clicks, current_elements):
        #finds existing nodes
        current_nodes = [int(element['data']['id']) for element in current_elements if 'target' not in element['data']]
        #finds next node to add
        next_id = min(set(range(1,len(current_nodes)+2))-set(current_nodes))
        # Construct the new node dictionary and append it to the state
        new_node = {'data': {'id': str(next_id), 'label': str(next_id), 'color' : "grey"}}
        current_elements.append(new_node)
        
        return current_elements
        
        
    def add_edge(self, n_clicks, source_id, target_id, current_elements):
        if not source_id or not target_id:
            return current_elements # Do nothing if source/target are empty
        
        # Construct the new edge dictionary and append it to the state
        new_edge = {'data': {'source': source_id, 'target': target_id}}
        if {'data': {'source': target_id, 'target': source_id}} not in current_elements and new_edge not in current_elements:
            current_elements.append(new_edge)
        
        return current_elements
        
        
    def switch_erasing_mode(self, n_clicks):
        if n_clicks%2 == 0:
            return {'toggled' : False}, {'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'}
        else:
            return {'toggled' : True}, {'backgroundColor': 'red', 'color': 'black', 'padding': '10px'}
        
        
    def process_node_click(self, tapped_node, current_elements, selected_colour ,erase_mode):
        # Base case: The app just loaded, and no node has been clicked yet.
        if tapped_node is None:
            return current_elements
        
        if erase_mode['toggled']:
            
            # Extract the mathematical or topological data from the dictionary
            node_id = tapped_node.get('id', 'Unknown')
            #node_label = tapped_node.get('label', 'No Label')
            # Return formatted HTML to update the DOM
            return [element for element in current_elements if not(
                    element['data']['id'] == node_id or
                    ('source' in element['data'] and element['data']['source'] == node_id) or
                    ('target' in element['data'] and element['data']['target'] == node_id))
                    ]   
        else:
            if selected_colour is None:
                return current_elements
            
            # Extract the mathematical or topological data from the dictionary
            node_id = str(tapped_node.get('id', 'Unknown'))
            
            elements = [element for element in current_elements if element['data']['id'] != node_id]
            elements.append({'data' : {'id' : node_id, 'label' : node_id, 'color' : selected_colour}})
            #node_label = tapped_node.get('label', 'No Label')
            # Return formatted HTML to update the DOM
            return elements 
    
    
    
    def erase_clicked_edge(self, tapped_edge, current_elements, erase_mode):
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
    
    
    def end_visualization(self, n_clicks, elements):
        if n_clicks == 0:
            return 0
        
        
        #counts the edges and vertices of the graph
        nodes = set([])
        self.vis_object.edges = []
        for element in elements:
            if 'source' not in element['data']:
                nodes.add(int(element['data']['id']))
                self.vis_object.color_storage_for_termination.append([int(element['data']['id']), self.vis_object.color_to_num(element['data']['color'])])
            else:
                self.vis_object.edges.append([int(element['data']['source']), int(element['data']['target'])])
        missing_nodes = set(range(max(nodes))) - nodes
        missing_list = sorted(list(missing_nodes), reverse=True)
            
        #then, removes non existant vertices to comply with graph_coloring problem
        for node in missing_list:
            for edge in self.vis_object.edges:
                for index in [0,1]:
                    if int(edge[index]) > node:
                        edge[index] -= 1
            for color_node in self.vis_object.color_storage_for_termination:
                if color_node[0] > node:
                    color_node[0] -= 1
            
            
                
        #and now - terminate the process!
        _thread.interrupt_main()
        #os.kill(os.getpid(), signal.SIGINT)
        return 0