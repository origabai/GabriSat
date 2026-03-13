from dash import Dash, html, Input, Output, State, dcc
import dash_cytoscape as cyto

class GraphUILayout():
    def __init__(self, helper_object):
        self.helper_object = helper_object
        '''
        handles input/layout for functions in GraphUtils object.
        '''
        helper_object.app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('btn-add-node', 'n_clicks'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(helper_object.add_node)
        
        helper_object.app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('btn-add-edge', 'n_clicks'),
            State('input-edge-source', 'value'),
            State('input-edge-target', 'value'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(helper_object.add_edge)
        
        helper_object.app.callback(
            Output('erase_toggled', 'data'),
            Output('btn-erase', 'style'),
            Input('btn-erase', 'n_clicks')
        )(helper_object.switch_erasing_mode)
        
        helper_object.app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('interactive-graph', 'tapNodeData'),
            State('interactive-graph', 'elements'),
            State('multi-colour-selector', 'value'),
            State('erase_toggled', 'data'),
            State('color_num_selector', 'value'),
            State('end-task-selector', 'value'),
            prevent_initial_call=True
        )(helper_object.process_node_click)
        
        helper_object.app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('interactive-graph', 'tapEdgeData'),
            State('interactive-graph', 'elements'),
            State('erase_toggled', 'data'),
            prevent_initial_call=True
        )(helper_object.process_edge_click)
        
        helper_object.app.callback(
            Output('success_message', 'children', allow_duplicate=True),
            Output('success_message', 'style', allow_duplicate=True),
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('btn-end', 'n_clicks'),
            State('interactive-graph', 'elements'),
            State('color_num_selector', 'value'),
            State('end-task-selector', 'value'),
            prevent_initial_call=True
        )(helper_object.do_task)
        
        helper_object.app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('btn-random', 'n_clicks'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(helper_object.generate_random_graph)
        
        helper_object.app.callback(
            Output('multi-colour-selector', 'options'),
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('color_num_selector', 'value'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(helper_object.handle_color_num_change)
        
        helper_object.app.callback(
            Output('label_1', 'style'),
            Output('label_2', 'style'),
            Output('multi-colour-selector', 'style'),
            Output('color_num_selector', 'style'),
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('end-task-selector', 'value'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(helper_object.handle_mode_change)
        
        
    
    default_layout = html.Div([
        html.H3("Visual graph editor"),
        html.H3("welcome to graphUI!", id='success_message' ,style = {'color' : 'black'}),
        
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
                
                value="HAMPATH", # The default selected array
                multi=False,  # This strictly enforces multiple-choice behavior
                style={'width': '300px', 'marginTop': '5px'}
            ),
        ], style={'marginBottom': '20px'}),
        
        html.Div([
            html.Label("colors in coloring", id = 'label_1', style={'display': 'none'}),
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
                value=str(3), # The default selected array
                multi=False,  # This strictly enforces multiple-choice behavior
                style={'display' : 'none'}
            ),
            html.Label("Change node color", id = 'label_2', style = {'display' : 'none'}),
            dcc.Dropdown(
                id='multi-colour-selector',
                options = [{'label': 'None (none selected)', 'value': None},
                    {'label': 'grey (no colour)', 'value': 'grey'},
                    {'label': 'red (0)', 'value': 'red'},
                    {'label': 'green (1)', 'value': 'green'},
                    {'label': 'blue (2)', 'value': 'blue'}],
                value=None, # The default selected array
                multi=False,  # This strictly enforces multiple-choice behavior
                style={'display' : 'none'}
            ),
        ]),
        # The Cytoscape Canvas
        cyto.Cytoscape(
            id='interactive-graph',
            elements=[],
            layout={'name': 'cose'}, # Force-directed physics layout
            style={'width': '800px', 'height': '500px', 'border': '1px solid black'},
            stylesheet=[
                # Basic styling to make labels visible
                {'selector': 'node', 'style': {'label': 'data(id)', 'text-valign': 'center', 'background-color': 'data(color)'}},
                {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'none', 'line-color' : 'data(color)'}}
            ]
        )
    ])
    