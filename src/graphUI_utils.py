from dash import Dash, html, Input, Output, State, dcc
import dash_cytoscape as cyto
import _thread
from random import randint
from graph_coloring import GraphColoring
from constants import RandomGraphMinSize, RandomGraphMaxSize, ColourSelectorOptions
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
            State('color_num_selector', 'value'),
            State('end-task-selector', 'value'),
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
            State('color_num_selector', 'value'),
            State('end-task-selector', 'value'),
            prevent_initial_call=True
        )(self.end_visualization)
        
        app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('btn-random', 'n_clicks'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(self.generate_random_graph)
        
        app.callback(
            Output('multi-colour-selector', 'options'),
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('color_num_selector', 'value'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(self.handle_color_num_change)
        
        app.callback(
            Output('label_1', 'style'),
            Output('label_2', 'style'),
            Output('multi-colour-selector', 'style'),
            Output('color_num_selector', 'style'),
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('end-task-selector', 'value'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(self.handle_mode_change)
    '''
    provides utils for graph_visualizer.py
    '''
    
    
    '''
    returns the standard layout of the html file given the default elements
    '''
    @staticmethod
    def generate_initial_data(nodes, edges, colors, special_edges = None):
        initial_data = []
        
        #generates nodes in initial_data
        for node in range(nodes):
            initial_data.append({'data' : {'id': str(node), 'label' : str(node), 'color': colors[node]}})
        
        #adds edges -  special edges are a list of edges to colour green. long if statement for undigraph support
        for edge in edges:
            if special_edges is not None and (edge in special_edges or [edge[1], edge[0]] in special_edges):
                initial_data.append({'data' : {'source': str(edge[0]), 'target': str(edge[1]), 'color' : 'ForestGreen'}})
            else:
                initial_data.append({'data' : {'source': str(edge[0]), 'target': str(edge[1]), 'color' : 'grey'}})
        
        return initial_data
        
    
    def default_layout(self, initial_elements, found_solution):
        #this part determines success message
        message = "Everything good, proceed!"
        message_style = {'color' : 'green'}
        if not found_solution:
            message = "No solution found!"
            message_style = {'color' : 'red'}
        
        #changes default label and selector style for vanishing elements depending on starting mode
        if self.vis_object.special_edges is not None:
            default_type = "HAMPATH"
            default_label_style = {'display': 'none'}
            default_selector_style = {'display': 'none', 'width': '300px', 'marginTop': '5px'}
        else: 
            default_type = "COLOR"
            default_label_style = {'display': 'block'}
            default_selector_style = {'display': 'block', 'width': '300px', 'marginTop': '5px'}
        
        
        return html.Div([
            html.H3("Visual graph editor"),
            html.H3(f"{message}", style = message_style),
            
            dcc.Store(id="erase_toggled", storage_type='memory', data = {'toggled' : False}),
            dcc.Store(id="color_current", storage_type='memory', data = {'colour' : None}),
            
            # Control Panel for Adding Nodes
            html.Div([
                html.Button('Add node', id='btn-add-node', n_clicks=0 ,style={ 'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'})
            ], style={'marginBottom': '10px'}),
            
            # Control Panel for Adding Edges
            html.Div([
                dcc.Input(id='input-edge-source', type='text', placeholder='Source Node ID'),
                dcc.Input(id='input-edge-target', type='text', placeholder='Target Node ID'),
                html.Button('Add edge', id='btn-add-edge', n_clicks=0, style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'})
            ], style={'marginBottom': '20px'}),

            html.Div([
                html.Button('Erase button', id='btn-erase', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0),
                html.Button('Generate random graph', id='btn-random', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0)
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.Button('Do task', id='btn-end', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0),
                html.Label("  Select task:"),
                dcc.Dropdown(
                    id='end-task-selector',
                    options=[
                        # 'label' is what the user sees, 'value' is what Python receives
                        {'label': 'coloring', 'value': "COLOR"},
                        {'label': 'hampath', 'value': "HAMPATH"},
                        {'label': 'end simulation', 'value': "END"},
                    ],
                    
                    value=default_type, # The default selected array
                    multi=False,  # This strictly enforces multiple-choice behavior
                    style={'width': '300px', 'marginTop': '5px'}
                ),
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.Label("colors in coloring", id = 'label_1', style=default_label_style),
                dcc.Dropdown(
                    id='color_num_selector',
                    options=[
                        # 'label' is what the user sees, 'value' is what Python receives
                        {'label': '1', 'value': '1'},
                        {'label': '2', 'value': '2'},
                        {'label': '3', 'value': '3'},
                        {'label': '4', 'value': '4'},
                        {'label': '5', 'value': '5'},
                        {'label': '6', 'value': '6'},
                        {'label': '7', 'value': '7'},
                        {'label': '8', 'value': '8'},
                    ],
                    value='3', # The default selected array
                    multi=False,  # This strictly enforces multiple-choice behavior
                    style=default_selector_style
                ),
                html.Label("Change node color", id = 'label_2', style = default_label_style),
                dcc.Dropdown(
                    id='multi-colour-selector',
                    options=[
                        # 'label' is what the user sees, 'value' is what Python receives
                        {'label': 'None (none selected)', 'value': None},
                        {'label': 'grey (no colour)', 'value': 'grey'},
                        {'label': 'red (0)', 'value': 'red'},
                        {'label': 'green (1)', 'value': 'green'},
                        {'label': 'blue (2)', 'value': 'blue'},
                        #{'label': 'yellow (3)', 'value': 'yellow'},
                        #{'label': 'purple (4)', 'value': 'purple'},
                        #{'label': 'pink (5)', 'value': 'pink'},
                        #{'label': 'magenta (6)', 'value': 'magenta'},
                        #{'label': 'lime (7)', 'value': 'lime'},
                        #{'label': 'cyan (8)', 'value': 'cyan'},
                    ],
                    value=[None], # The default selected array
                    multi=False,  # This strictly enforces multiple-choice behavior
                    style=default_selector_style
                ),
                
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
                    {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'none', 'line-color' : 'data(color)'}}
                ]
            )
        ])
    
    def add_node(self, n_clicks, current_elements):
        #finds existing nodes
        current_nodes = [int(element['data']['id']) for element in current_elements if 'target' not in element['data']]
        #finds next node to add
        next_id = min(set(range(0,len(current_nodes)+2))-set(current_nodes))
        # Construct the new node dictionary and append it to the state
        new_node = {'data': {'id': str(next_id), 'label': str(next_id), 'color' : "grey"}}
        current_elements.append(new_node)
        
        return current_elements
        
        
    def add_edge(self, n_clicks, source_id, target_id, current_elements):
        if not source_id or not target_id:
            return current_elements # Do nothing if source/target are empty
        
        # Construct the new edge dictionary and append it to the state
        new_edge = {'data': {'source': source_id, 'target': target_id, 'color' : 'grey'}}
        if {'data': {'source': target_id, 'target': source_id, 'color' : 'grey'}} and {'data': {'source': target_id, 'target': source_id, 'color' : 'ForestGreen'}} not in current_elements and new_edge not in current_elements:
            current_elements.append(new_edge)
        
        return current_elements
        
        
    def switch_erasing_mode(self, n_clicks):
        if n_clicks%2 == 0:
            return {'toggled' : False}, {'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'}
        else:
            return {'toggled' : True}, {'backgroundColor': 'red', 'color': 'black', 'padding': '10px'}
        
    
    
    
    def handle_mode_change(self, new_mode, current_elements):
        #changing to hampath - we need to clear all colors of the graph's nodes.
        if new_mode == "HAMPATH":
            if current_elements is not None and current_elements != []:
                new_elements = []
                for element in current_elements:
                    if element['data']['color'] == "ForestGreen":
                        new_elements.append(element)
                    else:
                        new_element = element
                        element['data']['color'] = "grey"
                        new_elements.append(new_element)
            else:
                new_elements = []
            #returns cleared out nodes and hides color parts
            return  {'display': 'none'}, {'display': 'none'}, {'display': 'none', 'width': '300px', 'marginTop': '5px'}, {'display': 'none', 'width': '300px', 'marginTop': '5px'}, new_elements

        elif new_mode == "COLOR":
            #when switching to color we need to clear out all coloured edges
            if current_elements is not None and current_elements != []:
                new_elements = []
                for element in current_elements:
                    if element['data']['color'] == "ForestGreen":
                        new_element = element
                        element['data']['color'] = "grey"
                        new_elements.append(new_element)
                    else:
                        new_elements.append(element)
            else:
                new_elements = []
            #unhides the color stuff from the html page
            return  {'display': 'block'}, {'display': 'block'}, {'display': 'block', 'width': '300px', 'marginTop': '5px'}, {'display': 'block', 'width': '300px', 'marginTop': '5px'}, current_elements

        else:
            #this is the mode for finishing simulation
            return  {'display': 'none'}, {'display': 'none'}, {'display': 'none', 'width': '300px', 'marginTop': '5px'}, {'display': 'none', 'width': '300px', 'marginTop': '5px'}, current_elements
    
    #checks if an element is of a colour alligning with the selected one.
    def check_element_compliance(self, element, color):
        try:
            return self.vis_object.color_to_num(element['data']['color']) < int(color) 
        except:
            return True
        
        
    #handles colour number change
    def handle_color_num_change(self, value, current_elements):
        #when no graph does trivial stuff to avoid iteration error
        if current_elements is None or current_elements == []:
            return ColourSelectorOptions[:int(value)+2], []
        
        #changes up the values of all nodes
        new_elements = []
        for element in current_elements:
            if self.check_element_compliance(element, value):
                new_elements.append(element)
            else:
                new_element = element
                element['data']['color'] = "grey"
                new_elements.append(new_element)
                
        #also changes the settings of the options
        return ColourSelectorOptions[:int(value)+2], new_elements
        
    def process_node_click(self, tapped_node, current_elements, selected_colour ,erase_mode, max_num, current_mode):
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
            trivial_conditions = current_mode != "COLOR" or selected_colour[0] is None 
            if trivial_conditions or (selected_colour != "grey" and self.vis_object.color_to_num(selected_colour) > int(max_num) - 1):
                return current_elements
            
            # Extract the mathematical or topological data from the dictionary
            node_id = str(tapped_node.get('id', 'Unknown'))
            
            elements = [element for element in current_elements if element['data']['id'] != node_id]
            elements.append({'data' : {'id' : node_id, 'label' : node_id, 'color' : selected_colour}})
            #node_label = tapped_node.get('label', 'No Label')
            # Return formatted HTML to update the DOM
            return elements 
    
    '''
    generates random graph
    '''
    def generate_random_graph(self, n_clicks, current_elements):
        #handles automatic activation at creation
        if n_clicks == 0:
            return current_elements
        #generates and updates new graph
        new_graph = GraphColoring.generate(size = randint(RandomGraphMinSize, RandomGraphMaxSize))
        return GraphUtils.generate_initial_data(new_graph.num_nodes, new_graph.edges, new_graph.num_nodes*["grey"])
    
    
    def erase_clicked_edge(self, tapped_edge, current_elements, erase_mode):
        # Base case: The app just loaded, and no node has been clicked yet.
        if tapped_edge is None or not erase_mode['toggled']:
            return current_elements
        # Extract the mathematical or topological data from the dictionary
        edge_src = tapped_edge.get('source', 'Unknown')
        edge_target = tapped_edge.get('target', 'Unknown')
        #node_label = tapped_node.get('label', 'No Label')
        # Return formatted HTML to update the DOM
        return [element for element in current_elements if not(
            (('source' in element['data'] and element['data']['source'] == edge_src) and
            ('target' in element['data'] and element['data']['target'] == edge_target)) or
            ('source' in element['data'] and element['data']['source'] == edge_target) and
            ('target' in element['data'] and element['data']['target'] == edge_src))    
            ] 
    
    
    def end_visualization(self, n_clicks, elements, max_colors, problem):
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
            
            
        self.vis_object.task = problem
        self.vis_object.max_colors = int(max_colors[0])
        self.vis_object.num_nodes = len(nodes)
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
        self.vis_object.correct_end = True
        _thread.interrupt_main()
        #os.kill(os.getpid(), signal.SIGINT)
        return "you can now refresh!"