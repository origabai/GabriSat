from dash import Dash, html, Input, Output, State, dcc, ALL, MATCH
import dash_cytoscape as cyto

class UILayout():
    def __init__(self, helper_object):
        self.helper_object = helper_object
        '''
        handles input/layout for functions in UIUtils object.
        In order to communicate with UI, a function has to have helper_object.app.callback
        run on it.
        
        The init function handles this - all functions that either accept input are produce output
        to the ui, are called here.
        
        the format is as such: 
        "Input" determines a parameter that is passed to the function and calls it when changed
        "State" determined a parameter that is passed to the function but it's update doesnt cause the function to run
        "Output" is the element of UI that is changed by the function - it's return value is passed to the  corresponding field.
        '''
        helper_object.app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Output('interactive-graph', 'layout', allow_duplicate=True),
            Output('nodes-list', 'children', allow_duplicate=True),
            Input('btn-add-node', 'n_clicks'),
            State('interactive-graph', 'elements'),
            State('nodes-list', 'children'),
            prevent_initial_call=True
        )(helper_object.add_node)
        
        helper_object.app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Output('interactive-graph', 'layout', allow_duplicate=True),
            Output('success_message', 'children', allow_duplicate=True),
            Output('success_message', 'style', allow_duplicate=True),
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
            Output('interactive-graph', 'layout', allow_duplicate=True),
            Output('nodes-list', 'children', allow_duplicate=True),
            Input('interactive-graph', 'tapNodeData'),
            State('interactive-graph', 'elements'),
            State('multi-colour-selector', 'value'),
            State('erase_toggled', 'data'),
            State('color_num_selector', 'value'),
            State('end-task-selector', 'value'),
            State('nodes-list', 'children'),
            prevent_initial_call=True
        )(helper_object.process_node_click)
        
        helper_object.app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Output('interactive-graph', 'layout', allow_duplicate=True),
            Input('interactive-graph', 'tapEdgeData'),
            State('interactive-graph', 'elements'),
            State('erase_toggled', 'data'),
            prevent_initial_call=True
        )(helper_object.process_edge_click)
        
        helper_object.app.callback(
            Output('success_message', 'children', allow_duplicate=True),
            Output('success_message', 'style', allow_duplicate=True),
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Output('interactive-graph', 'layout', allow_duplicate=True),
            Output('sudoku-board', 'children', allow_duplicate=True),
            Input('btn-end', 'n_clicks'),
            State('interactive-graph', 'elements'),
            State('color_num_selector', 'value'),
            State('end-task-selector', 'value'),
            State('sudoku-board', 'children'),
            State('sudoku-size-selector', 'value'),
            prevent_initial_call=True
        )(helper_object.do_task)
        
        helper_object.app.callback(
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Output('interactive-graph', 'layout', allow_duplicate=True),
            Output('nodes-list', 'children', allow_duplicate=True),
            Input('btn-random', 'n_clicks'),
            State('interactive-graph', 'elements'),
            State('graph-size-input', 'value'),
            State('nodes-list', 'children'),
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
            Output('success_message', 'children', allow_duplicate=True),
            Output('success_message', 'style', allow_duplicate=True),
            Output('graph-div', 'style', allow_duplicate=True),
            Output('sudoku-div', 'style', allow_duplicate=True),
            Output('coloring-div', 'style', allow_duplicate=True),
            Output('interactive-graph', 'elements', allow_duplicate=True),
            Input('end-task-selector', 'value'),
            State('graph-div', 'style'),
            State('sudoku-div', 'style'),
            State('coloring-div', 'style'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(helper_object.switch_problem)

        helper_object.app.callback(
            Output('success_message', 'children', allow_duplicate=True),
            Output('success_message', 'style', allow_duplicate=True),
            Output('sudoku-board-div', 'style', allow_duplicate=True),
            Output('sudoku-board', 'children', allow_duplicate=True),
            Output('sudoku-board', 'style', allow_duplicate=True),
            Output('sudoku-board', 'key', allow_duplicate=True),
            Output('sudoku-num-input', 'max', allow_duplicate=True),
            Input('sudoku-size-selector', 'value'),
            State('sudoku-board-div', 'style'),
            State('sudoku-board', 'children'),
            State('sudoku-board', 'style'),
            State('sudoku-board', 'key'),
            prevent_initial_call=True
        )(helper_object.change_sudoku_size)

        helper_object.app.callback(
            Output({'type': 'sudoku-cell', 'row': MATCH, 'col': MATCH, 'version': MATCH}, 'children', allow_duplicate=True),
            Output({'type': 'sudoku-cell', 'row': MATCH, 'col': MATCH, 'version': MATCH}, 'style', allow_duplicate=True),
            Input({'type': 'sudoku-cell', 'row': MATCH, 'col': MATCH, 'version': MATCH}, 'n_clicks'), # any sudoku cell
            State({'type': 'sudoku-cell', 'row': MATCH, 'col': MATCH, 'version': MATCH}, 'children'),
            State({'type': 'sudoku-cell', 'row': MATCH, 'col': MATCH, 'version': MATCH}, 'style'),
            State('sudoku-size-selector', 'value'),
            State('sudoku-num-input', 'value'),
            prevent_initial_call=True
        )(helper_object.sudoku_cell_clicked)

        helper_object.app.callback(
            Output('success_message', 'children', allow_duplicate=True),
            Output('success_message', 'style', allow_duplicate=True),
            Output('sudoku-board', 'children', allow_duplicate=True),
            Input('generate-random-board', 'n_clicks'),
            State('sudoku-size-selector', 'value'),
            prevent_initial_call=True
        )(helper_object.generate_random_sudoku)

        helper_object.app.callback(
            Output('input-edge-source', 'style', allow_duplicate=True),
            Input('input-edge-source', 'value'),
            Input('nodes-list', 'children'),
            prevent_initial_call=True
        )(helper_object.add_edge_input_changed)
        
        helper_object.app.callback(
            Output('input-edge-target', 'style', allow_duplicate=True),
            Input('input-edge-target', 'value'),
            Input('nodes-list', 'children'),
            prevent_initial_call=True
        )(helper_object.add_edge_input_changed)
        
        helper_object.app.callback(
            Output('input-edge-source', 'max', allow_duplicate=True),
            Output('input-edge-target', 'max', allow_duplicate=True),
            Input('nodes-list', 'children'),
            prevent_initial_call=True
        )(helper_object.nodes_list_changed)
        
        
        
    '''
    this is default layout of the UI
    '''
    default_layout = html.Div([
        html.H3("SAT solver UI"),
        html.H3("welcome to SAT UI!", id='success_message' ,style = {'color' : 'black'}),
        
        #storage for togglable button presses
        dcc.Store(id="erase_toggled", storage_type='memory', data = {'toggled' : False}),
        dcc.Store(id="color_current", storage_type='memory', data = {'colour' : None}),
        

        #do task selector and button
        html.Div([
            html.Button('Do task', id='btn-end', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0),
            html.Label("  Select task:"),
            dcc.Dropdown(
                id='end-task-selector',
                options=[
                    # 'label' is what the user sees, 'value' is what Python receives
                    {'label': 'coloring', 'value': "COLOR"},
                    {'label': 'hampath', 'value': "HAMPATH"},
                    {'label': 'sudoku', 'value': "SUDOKU"},
                    {'label': 'end simulation', 'value': "END"},
                ],
                
                value="HAMPATH", # The default selected array
                multi=False,  # This strictly enforces multiple-choice behavior
                style={'width': '300px', 'marginTop': '5px'}
            ),
        ], style={'marginBottom': '20px'}),
        
        #everything graph related
        html.Div([
            # add node button
            html.Div([
                html.Button('Add node', id='btn-add-node', n_clicks=0 ,style={ 'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'})
            ], style={'marginBottom': '10px'}),
            
            # Control Panel for Adding Edges
            html.Div([
                dcc.Input(id='input-edge-source', type='number', min=0, max=0, step=1, placeholder='Source Node ID', debounce=True, autoComplete='on', list='nodes-list'),
                dcc.Input(id='input-edge-target', type='number', min=0, max=0, step=1, placeholder='Target Node ID', debounce=True, autoComplete='on', list='nodes-list'),
                html.Datalist(id='nodes-list', children=[]), # children of type html.Option(value="some string")
                html.Button('Add edge', id='btn-add-edge', n_clicks=0, style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'})
            ], id='control-panel',style={'marginBottom': '20px'}),
            
            # random graph size input
            dcc.Input(id='graph-size-input', type='number', min=1, max=50, step=1, placeholder='Size of the random generated graph'),

            # erase and random button
            html.Div([
                html.Button('Erase button', id='btn-erase', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0),
                html.Button('Generate random graph', id='btn-random', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0)
            ], style={'marginBottom': '20px'}),
            
            #colors in colors control panel
            html.Div([
                html.Label("colors in coloring", id = 'label_1'),
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
                ),
                html.Label("Change node color", id = 'label_2'),
                dcc.Dropdown(
                    id='multi-colour-selector',
                    options = [{'label': 'None (none selected)', 'value': None},
                        {'label': 'grey (no colour)', 'value': 'grey'},
                        {'label': 'red (0)', 'value': 'red'},
                        {'label': 'green (1)', 'value': 'green'},
                        {'label': 'blue (2)', 'value': 'blue'}],
                    value=None, # The default selected array
                    multi=False,  # This strictly enforces multiple-choice behavior
                ),
            ], id='coloring-div', style={'display': 'none'}),
            # the canvas - for graph display
            cyto.Cytoscape(
                id='interactive-graph',
                elements=[],
                layout={'name': 'cose'}, # Force-directed physics layout
                style={'width': '800px', 'height': '500px', 'border': '1px solid black'},
                stylesheet=[
                    # Basic styling to make labels visible
                    {'selector': 'node', 'style': {'label': 'data(id)', 'text-valign': 'center', 'background-color': 'data(color)'}},
                    {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'none', 'line-color' : 'data(color)'}}
                ])
        ], id='graph-div', style={'display': 'block'}),

        # everything sudoku related
        html.Div([
            #label for the following dropdown
            html.Label("Please choose a size for the sudoku:"),
            #choice for size of sudoku
            dcc.Dropdown(
                id='sudoku-size-selector',
                options = [{'label': 'None (none selected)', 'value': '0'},
                    {'label': '4x4', 'value': '4'},
                    {'label': '9x9', 'value': '9'},
                    {'label': '16x16', 'value': '16'},
                    {'label': '25x25', 'value': '25'},],
                value=None, # The default selected array
                multi=False,  # This strictly enforces multiple-choice behavior
                style={'width': '300px'},
                clearable=False,
                persistence=True,
                persistence_type='session',
            ),
            # a div for the sudoku board and similar elements, to be revealed only when a size is selected
            html.Div([
                # a button for randomly initializing the board
                html.Button(
                    'Generate random board',
                    id='generate-random-board',
                    n_clicks=0,
                    style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px', 'marginTop': '20px'}
                ),
                # the number choice for the sudoku
                html.Div([
                    html.Label("number to place (0 for nothing)"),
                    dcc.Input(
                        id='sudoku-num-input',
                        min=0,
                        max=0, # a temporary value 
                        step=1,
                        type='number',
                        placeholder='number to place',
                    ),
                ], style={'width': '300px', 'marginTop': '20px'}),
                # the sudoku board itself, initialized in UI_utils
                html.Div(id='sudoku-board', style={'display': 'none'})
            ], id='sudoku-board-div', style={'display': 'none'}),
        ], id='sudoku-div', style={'display': 'none'}), # start hidden
    ])

    
    