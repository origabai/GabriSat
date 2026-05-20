from dash import Dash, html, Input, Output, State, dcc, ALL, MATCH
from dash_extensions import EventListener
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
            Output('graph-wrapper', 'children', allow_duplicate=True),
            Output('nodes-list', 'children', allow_duplicate=True),
            Input('btn-add-node', 'n_clicks'),
            State('interactive-graph', 'elements'),
            State('nodes-list', 'children'),
            prevent_initial_call=True
        )(helper_object.add_node)
        
        helper_object.app.callback(
            Output('current_mode', 'data', allow_duplicate=True),
            Output('btn-erase', 'style', allow_duplicate=True),
            Output('btn-add-edge', 'style', allow_duplicate=True),
            Output('graph-wrapper', 'children', allow_duplicate=True),
            Input('btn-erase', 'n_clicks'),
            State('current_mode', 'data'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(helper_object.switch_erasing_mode)
        
        
        helper_object.app.callback(
            Output('current_mode', 'data', allow_duplicate=True),
            Output('btn-erase', 'style', allow_duplicate=True),
            Output('btn-add-edge', 'style', allow_duplicate=True),
            Output('graph-wrapper', 'children', allow_duplicate=True),
            Input('btn-add-edge', 'n_clicks'),
            State('current_mode', 'data'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(helper_object.switch_adding_mode)
        
        helper_object.app.callback(
            Output('graph-wrapper', 'children', allow_duplicate=True),
            Output('nodes-list', 'children', allow_duplicate=True),
            Output('current_mode', 'data', allow_duplicate=True),
            Input('interactive-graph', 'tapNodeData'),
            State('interactive-graph', 'elements'),
            State('multi-colour-selector', 'children'),
            State('current_mode', 'data'),
            State('color_num_selector', 'value'),
            State('end-task-selector', 'data'),
            State('nodes-list', 'children'),
            prevent_initial_call=True
        )(helper_object.process_node_click)
        
        helper_object.app.callback(
            Output('graph-wrapper', 'children', allow_duplicate=True),
            Input('interactive-graph', 'tapEdgeData'),
            State('interactive-graph', 'elements'),
            State('current_mode', 'data'),
            prevent_initial_call=True
        )(helper_object.process_edge_click)
        
        helper_object.app.callback(
            Output('fail-message', 'children', allow_duplicate=True),
            Output('sudoku-fail-message', 'children', allow_duplicate=True),
            Output('graph-wrapper', 'children', allow_duplicate=True),
            Output('sudoku-board', 'children', allow_duplicate=True),
            Output('current_mode', 'data', allow_duplicate=True),
            Output('btn-add-edge', 'style', allow_duplicate=True),
            Input('btn-end1', 'n_clicks'),
            Input('btn-end2', 'n_clicks'),
            State('interactive-graph', 'elements'),
            State('color_num_selector', 'value'),
            State('end-task-selector', 'data'),
            State('sudoku-board', 'children'),
            State('sudoku-size-selector', 'value'),
            State('current_mode', 'data'),
            prevent_initial_call=True
        )(helper_object.do_task)
        
        helper_object.app.callback(
            Output('graph-wrapper', 'children', allow_duplicate=True),
            Output('nodes-list', 'children', allow_duplicate=True),
            Output('current_mode', 'data', allow_duplicate=True),
            Output('btn-add-edge', 'style', allow_duplicate=True),
            Input('btn-random', 'n_clicks'),
            State('interactive-graph', 'elements'),
            State('graph-size-input', 'value'),
            State('nodes-list', 'children'),
            prevent_initial_call=True
        )(helper_object.generate_random_graph)
        
        helper_object.app.callback(
            Output('graph-wrapper', 'children', allow_duplicate=True),
            Output('multi-colour-selector', 'children'),
            Output('multi-colour-selector', 'style'),
            Output('current_mode', 'data', allow_duplicate=True),
            Input('color_num_selector', 'value'),
            State('interactive-graph', 'elements'),
            State('multi-colour-selector', 'children'),
            State('current_mode', 'data'),
            prevent_initial_call=True
        )(helper_object.handle_color_num_change)

        helper_object.app.callback(
            Output('graph-div', 'style', allow_duplicate=True),
            Output('sudoku-div', 'style', allow_duplicate=True),
            Output('coloring-div', 'style', allow_duplicate=True),
            Output('graph-wrapper', 'children', allow_duplicate=True),
            Input('end-task-selector', 'data'),
            State('graph-div', 'style'),
            State('sudoku-div', 'style'),
            State('coloring-div', 'style'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(helper_object.switch_problem)

        helper_object.app.callback(
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
            State('sudoku-num-input', 'children'),
            prevent_initial_call=True
        )(helper_object.sudoku_cell_clicked)

        helper_object.app.callback(
            Output('sudoku-board', 'children', allow_duplicate=True),
            Input('generate-random-board', 'n_clicks'),
            State('sudoku-size-selector', 'value'),
            prevent_initial_call=True
        )(helper_object.generate_random_sudoku)

        helper_object.app.callback(
            Output('sudoku-board', 'children', allow_duplicate=True),
            Input('sudoku-board-clear', 'n_clicks'),
            State('sudoku-size-selector', 'value'),
            prevent_initial_call=True
        )(helper_object.clear_sudoku_board)
        
        helper_object.app.callback(
            Output('input-edge-source', 'max', allow_duplicate=True),
            Output('input-edge-target', 'max', allow_duplicate=True),
            Input('nodes-list', 'children'),
            prevent_initial_call=True
        )(helper_object.nodes_list_changed)
        
        helper_object.app.callback(
            Output('end-task-selector', 'data', allow_duplicate=True),
            Output('btn-hamcycle', 'style', allow_duplicate=True),
            Output('btn-graphcoloring', 'style', allow_duplicate=True),
            Output('btn-sudoku', 'style', allow_duplicate=True),
            Input('btn-hamcycle', 'n_clicks'),
            Input('btn-graphcoloring', 'n_clicks'),
            Input('btn-sudoku', 'n_clicks'),
            prevent_initial_call=True
        )(helper_object.select_problem)

        helper_object.app.callback(
            Output("sudoku-num-input", "children", allow_duplicate=True),
            Output('sudoku_num_last_modified', 'data', allow_duplicate=True),
            Input("sudoku-num-input", "children"),
            Input('sudoku-keypress-listener', 'n_events'),
            Input('sudoku-keypress-listener', 'event'),
            State('sudoku_num_last_modified', 'data'),
            State('sudoku-size-selector', 'value'),
            prevent_initial_call=True,
        )(helper_object.handle_keypress_sudoku)
        
        helper_object.app.callback(
            Output("multi-colour-selector", "children", allow_duplicate=True),
            Output("multi-colour-selector", "style", allow_duplicate=True),
            Input('coloring-keypress-listener', 'n_events'),
            Input('coloring-keypress-listener', 'event'),
            State('color_num_selector', 'value'),
            prevent_initial_call=True
        )(helper_object.handle_keypress_coloring)

        helper_object.app.callback(
            Output('graph-wrapper', 'children', allow_duplicate=True),
            Output('nodes-list', 'children', allow_duplicate=True),
            Output('current_mode', 'data', allow_duplicate=True),
            Output('btn-add-edge', 'style', allow_duplicate=True),
            Input('btn-clear-graph', 'n_clicks'),
            prevent_initial_call=True
        )(helper_object.clear_graph)

        helper_object.app.callback(
            Output('graph-wrapper', 'children', allow_duplicate=True),
            Input('btn-clear-coloring', 'n_clicks'),
            State('interactive-graph', 'elements'),
            prevent_initial_call=True
        )(helper_object.clear_coloring)

        helper_object.app.callback(
            Output('fail-message', 'children', allow_duplicate=True),
            Output('sudoku-fail-message', 'children', allow_duplicate=True),
            Input('graph-wrapper', 'children'),
            Input('sudoku-board', 'children'),
            prevent_initial_call=True
        )(helper_object.clear_fail_message)


    '''
    this is default layout of the UI
    '''
    default_layout = html.Div([
        html.H1("SAT solver"),
        
        #storage for togglable button presses
        dcc.Store(id="current_mode", storage_type='memory', data = {'current_mode' : None, 'previous_click' : None, 'previous_color' : None}),
        dcc.Store(id="color_current", storage_type='memory', data = {'colour' : None}),


        # storage for the last time the sudoku number changed
        dcc.Store(id="sudoku_num_last_modified", storage_type='memory', data = {'time' : 0}),

        #do task selector and button
        html.Div([
            html.Button('Hamiltonian Cycle', id='btn-hamcycle', n_clicks=0 ,style={ 'backgroundColor': 'green', 'color': 'black', 'padding': '10px'}),
            html.Button('Graph Coloring', id='btn-graphcoloring', n_clicks=0 ,style={ 'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'}),
            html.Button('Sudoku', id='btn-sudoku', n_clicks=0 ,style={ 'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'}),
            dcc.Store(id='end-task-selector', data='HAMPATH')
        ], className='task-selector', style={'marginBottom': '20px'}),
        
        #everything graph related
        html.Div([
            html.Datalist(id='nodes-list', children=[]), # children of type html.Option(value="some string")
            
            # control panel for everything else
            html.Div([
                dcc.Input(id='graph-size-input', style={'width': '250px', 'marginRight':'10px'},  type='number', min=5, max=50, step=1, placeholder='random graph size'),
                html.Button('Generate random graph', id='btn-random', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0),
                html.Button('Clear graph', id='btn-clear-graph', n_clicks=0 ,style={ 'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'}),
                html.Button('Add node', id='btn-add-node', n_clicks=0 ,style={ 'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'}),
                html.Button('Add edge', id='btn-add-edge', n_clicks=0, style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'}),
                html.Button('Erase', id='btn-erase', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0),
                html.Button('Solve!', id='btn-end1', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'} ,n_clicks=0),
                html.Div("", id='fail-message', style={'color': 'red', 'minWidth': '180px', 'height': '40px', 'display': 'flex', 'alignItems': 'center', 'fontWeight': 'bold', 'position': 'absolute', 'marginLeft': '12px'})
            ], id='control-panel2', style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginBottom': '20px', 'position': 'relative'}),
            # coloring stuff
            html.Div([
                html.Div([
                    html.Button('Clear coloring', id='btn-clear-coloring', n_clicks=0 ,style={ 'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px', 'marginRight':'10px'}),
                    dcc.Input(id='color_num_selector', style={'width': '200px', 'marginRight':'10px'},  type='number', min=1, max=9, step=1, placeholder='max colors'),
                    html.Label("Change node color", id = 'label_2', style={'marginRight':'10px', 'marginBottom':'0'}),
                    html.H2("red", id="multi-colour-selector", style={'margin':'0', 'marginRight':'10px', 'width': '100px', 'textAlign': 'left', 'color': 'red', 'marginBottom':'0'}),
                    html.Div(
                        [
                            html.Button("Legend", id="legend-btn", className="legend-btn"),
                            html.Div(
                                [
                                    html.Div([html.Span(className="color-box grey"), "0 - Erase"], className="legend-row"),
                                    html.Div([html.Span(className="color-box red"), "1"], className="legend-row"),
                                    html.Div([html.Span(className="color-box green"), "2"], className="legend-row"),
                                    html.Div([html.Span(className="color-box blue"), "3"], className="legend-row"),
                                    html.Div([html.Span(className="color-box yellow"), "4"], className="legend-row"),
                                    html.Div([html.Span(className="color-box purple"), "5"], className="legend-row"),
                                    html.Div([html.Span(className="color-box pink"), "6"], className="legend-row"),
                                    html.Div([html.Span(className="color-box magenta"), "7"], className="legend-row"),
                                    html.Div([html.Span(className="color-box lime"), "8"], className="legend-row"),
                                    html.Div([html.Span(className="color-box cyan"), "9"], className="legend-row"),
                                ],
                                className="legend-popup",
                            ),
                        ],
                        className="legend-wrap",
                    ),
                    EventListener(
                        id="coloring-keypress-listener",
                        events=[{"event": "keydown", "props": ["key", "code"]}]
                    ),
                ], id='coloring-div', style={'display': 'none', 'alignItems':'center', 'marginRight': '20px', 'marginBottom': '0px'}),
            ], className='button-row', style={'margin':'0','marginBottom': '10px'}),

            # the canvas - for graph display
            html.Div(id='graph-wrapper', children=[
                cyto.Cytoscape(
                    id='interactive-graph',
                    elements=[],
                    layout = {
                        'name': 'random',
                        'fit': True,
                        'padding': 60,
                        'animate': False,
                    },
                    style={'width': '800px', 'height': '500px', 'border': '1px solid black'},
                    stylesheet=[
                        # Basic styling to make labels visible
                        {'selector': 'node', 'style': {'label': 'data(id)', 'text-valign': 'center', 'background-color': 'data(color)'}},
                        {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'none', 'line-color' : 'data(color)'}}
                    ])
            ]),
        ], id='graph-div', style={'display': 'block'}),

        # everything sudoku related
        html.Div([
            #label for the following dropdown
            html.Div([
                html.Label("Please choose a size for the sudoku:"),
                #choice for size of sudoku
                dcc.Dropdown(
                    id='sudoku-size-selector',
                    options = [{'label': 'None (none selected)', 'value': '0'},
                        {'label': '4x4', 'value': '4'},
                        {'label': '9x9', 'value': '9'},
                        {'label': '16x16', 'value': '16'},
                        {'label': '25x25', 'value': '25'},],
                    value='0', # The default selected array
                    multi=False,  # This strictly enforces multiple-choice behavior
                    style={'width': '300px'},
                    clearable=False,
                ),
            ], className='sudoku-size-container', style={'marginBottom': '20px'}),

            # a div for the sudoku board and similar elements, to be revealed only when a size is selected
            html.Div([

                html.Div([
                    # a button for randomly initializing the board
                    html.Button(
                        'Generate random board',
                        id='generate-random-board',
                        n_clicks=0,
                        style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px', 'marginRight': '10px'}
                    ),
                    # sudoku clear button
                    html.Button(
                        'Clear board',
                        id='sudoku-board-clear',
                        n_clicks=0,
                        style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px', 'marginRight': '10px'}
                    ),
                    # the number choice for the sudoku
                    html.Div([
                        html.Label("current number", id="sudoku-num-input-label", style={'margin':'0'}),
                        html.H2("1", id="sudoku-num-input", style={'margin':'0'}),
                    ]),
                    html.Div(
                        [
                            html.Button("Info", id="legend-btn2", className="legend-btn"),
                            html.Div(
                                [
                                    html.Div("Type 0 to erase"),
                                    html.Div("Type any other number to input it"),
                                ],
                                className="legend-popup",
                            )
                        ],
                        className="legend-wrap",
                    ),
                    html.Button('Solve!', id='btn-end2', style={'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px','marginRight':'20px'} ,n_clicks=0),
                    html.Div("", id='sudoku-fail-message', style={'color': 'red', 'minWidth': '180px', 'height': '40px', 'display': 'flex', 'alignItems': 'center', 'fontWeight': 'bold', 'position': 'absolute', 'marginLeft': '12px'})
                ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginBottom': '20px', 'position': 'relative'}),


                # the sudoku board itself, initialized in UI_utils
                html.Div(id='sudoku-board', style={'display': 'none'}),
                EventListener(
                    id="sudoku-keypress-listener",
                    events=[{"event": "keydown", "props": ["key", "code"]}]
                ),

            ], id='sudoku-board-div', style={'display': 'none'}),
        ], id='sudoku-div', style={'display': 'none'}), # start hidden
    ], id="default-layout")

    
    